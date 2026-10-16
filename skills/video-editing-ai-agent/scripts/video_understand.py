#!/usr/bin/env python
"""Mapa de comprension de un video completo: planos, movimiento, audio, voz y fotogramas clave.

Claude no "ve" video: ve imagenes. Este script convierte un video en un MAPA que cabe en contexto:
  1) detecta planos/cortes (histograma + rejilla de color, refinado al fotograma real),
  2) mide movimiento, brillo y nitidez por plano,
  3) mide audio (envolvente, silencios) y transcribe la voz con marcas de tiempo (faster-whisper, local),
  4) elige fotogramas clave con PRESUPUESTO (--budget) y los junta en hojas de contacto rotuladas,
  5) escribe video-map.md / video-map.json con todo alineado en una sola linea de tiempo.
Despues Claude LEE las hojas (Read) y escribe su comprension en understanding.md (plantilla en assets/).

Uso:
  python video_understand.py video.mp4 [-o carpeta] [--budget 24] [--lang es] [--no-transcribe]
                             [--fps 4] [--model small] [--cut-sensitivity 1.0]
Salida (por defecto <carpeta del video>/analisis/<nombre>/):
  video-map.md, video-map.json, sheets/sheet_01.png..., frames/f_<t>.jpg
No sube nada a ningun servicio. No modifica el video.
Referencia: references/video-comprehension.md
"""
import argparse, json, math, os, subprocess, sys, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, FFPROBE, probe_duration, run  # noqa: E402
try:
    from vad_segments import analyze as vad_analyze, overlap_ratio  # noqa: E402
except Exception:  # faster-whisper ausente: sin VAD
    vad_analyze = overlap_ratio = None

# Whisper "inventa" estas frases sobre musica/ruido (datos de entrenamiento con subtitulos). Si aparecen: sospechoso.
import re
HALLUCINATION = re.compile(r"amara\.org|subt[ií]tulos? (realizados? )?(por|de)|thanks? for watching|gracias por (ver|vuestra)|suscr[ií]b|subscribe|"
                           r"like and subscribe|\bMBC\b|♪|^\W*music\W*$|^\W*m[uú]sica\W*$", re.I)
SMALL = 64            # lado de la miniatura de analisis (px, deformada a cuadrado: solo para metricas)
BG, FG, DIM, ACC = (18, 18, 22), (235, 235, 235), (140, 140, 150), (255, 140, 60)


# ----------------------------------------------------------------------------- utilidades
def font(sz):
    for f in (r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def tc(t):
    t = max(0.0, t)
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def probe(path):
    r = run([FFPROBE, "-v", "error", "-show_entries",
             "format=duration:stream=index,codec_type,codec_name,duration,width,height,avg_frame_rate,r_frame_rate,color_transfer:stream_side_data=rotation",
             "-of", "json", path])
    try:
        d = json.loads(r.stdout)
    except Exception:
        d = {}
    vs = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    au = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    w, h = int(vs.get("width", 0) or 0), int(vs.get("height", 0) or 0)
    rot = 0
    for sd in vs.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(round(float(sd["rotation"]))) % 360
    if rot in (90, 270):
        w, h = h, w
    fr = vs.get("avg_frame_rate") or vs.get("r_frame_rate") or "0/1"
    try:
        n, dn = fr.split("/")
        fps = float(n) / float(dn) if float(dn) else 0.0
    except Exception:
        fps = 0.0
    return {"duration": float(d.get("format", {}).get("duration", 0) or 0) or probe_duration(path),
            "width": w, "height": h, "fps": round(fps, 3), "rotation": rot,
            "codec": vs.get("codec_name"), "hdr": vs.get("color_transfer") in ("smpte2084", "arib-std-b67"),
            "has_audio": au is not None, "audio_codec": (au or {}).get("codec_name"),
            "audio_duration": float((au or {}).get("duration") or 0) or None}


def decode_small(path, fps, start=None, dur=None):
    """Fotogramas reducidos (N,SMALL,SMALL,3) uint8 via ffmpeg (autorrota). Devuelve array y tiempos."""
    cmd = [FFMPEG, "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-i", path, "-an", "-vf", f"fps={fps},scale={SMALL}:{SMALL}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    fs = SMALL * SMALL * 3
    n = len(raw) // fs
    if n == 0:
        return np.zeros((0, SMALL, SMALL, 3), np.uint8)
    return np.frombuffer(raw[: n * fs], np.uint8).reshape(n, SMALL, SMALL, 3)


# ----------------------------------------------------------------------------- planos
def frame_features(fr):
    """Histograma de color 4x4x4 (normalizado) + rejilla 6x6 de color medio, ambos en [0,1]."""
    q = (fr // 64).astype(np.int32)
    idx = q[..., 0] * 16 + q[..., 1] * 4 + q[..., 2]
    hist = np.bincount(idx.ravel(), minlength=64).astype(np.float32) / idx.size
    g = fr.astype(np.float32) / 255.0
    b = SMALL // 6 * 6
    grid = g[:b, :b].reshape(6, b // 6, 6, b // 6, 3).mean(axis=(1, 3)).ravel()
    return hist, grid


def cut_scores(frames):
    n = len(frames)
    feats = [frame_features(f) for f in frames]
    sc = np.zeros(n)
    for i in range(1, n):
        dh = 0.5 * np.abs(feats[i][0] - feats[i - 1][0]).sum()          # 0..1
        dg = float(np.abs(feats[i][1] - feats[i - 1][1]).mean()) * 3.0   # rejilla espacial, reescalada
        sc[i] = max(dh, dg)
    return sc


def detect_cuts(path, frames, fps, sens):
    sc = cut_scores(frames)
    if len(sc) < 3:
        return [], sc
    med = float(np.median(sc[1:]))
    mad = float(np.median(np.abs(sc[1:] - med))) or 0.01
    thr = max(0.28 / sens, med + 8 * mad / sens)
    cand = [i for i in range(1, len(sc)) if sc[i] >= thr and sc[i] >= sc[i - 1] and (i + 1 >= len(sc) or sc[i] >= sc[i + 1])]
    # separacion minima de 0.6 s: se queda el de mayor puntuacion
    cand.sort()
    keep = []
    for i in cand:
        if keep and (i - keep[-1]) / fps < 0.6:
            if sc[i] > sc[keep[-1]]:
                keep[-1] = i
        else:
            keep.append(i)
    cuts = sorted((refine_cut(path, i / fps, fps) for i in keep), key=lambda c: c[0])
    return [(round(c[0], 3), c[1], c[2]) for c in cuts], sc


def refine_cut(path, t, coarse_fps):
    """Afina el corte al fotograma real (decodifica ~0.8 s a 30 fps) y clasifica: seco vs gradual/animado.
    Dominancia = salto maximo / media de los 3 mayores siguientes (sin vecinos). Calibrada con 7 transiciones: heuristica."""
    a = max(0.0, t - 0.4)
    fr = decode_small(path, 30, start=a, dur=0.8)
    if len(fr) < 4:
        return t, "desconocido", 0.0
    s = cut_scores(fr)
    i = int(np.argmax(s))
    m = s.copy(); m[max(0, i - 1): i + 2] = 0
    dom = float(s[i] / max(np.sort(m)[-3:].mean(), 1e-3))
    return a + i / 30.0, ("seco" if dom >= 2.5 else "gradual/animado"), round(dom, 1)


def shot_stats(frames, fps, t0, t1):
    i0, i1 = int(round(t0 * fps)), max(int(round(t1 * fps)), int(round(t0 * fps)) + 1)
    seg = frames[i0:i1]
    if len(seg) == 0:
        return {"motion": 0.0, "brightness": 0.0, "motion_peak_t": t0}
    gray = seg.astype(np.float32).mean(axis=3) / 255.0
    if len(seg) > 1:
        diffs = np.abs(np.diff(gray, axis=0)).mean(axis=(1, 2))
        k = int(np.argmax(diffs))
        return {"motion": float(diffs.mean()), "brightness": float(gray.mean()), "motion_peak_t": round(t0 + (k + 1) / fps, 3)}
    return {"motion": 0.0, "brightness": float(gray.mean()), "motion_peak_t": t0}


def motion_label(m):
    return "estatico" if m < 0.004 else "suave" if m < 0.015 else "medio" if m < 0.04 else "alto"


# ----------------------------------------------------------------------------- audio / voz
def audio_profile(path, dur):
    """Envolvente RMS en dBFS (ventana 0.25 s) y silencios reales: > 20 dB por debajo del nivel de voz (p90).
    Una narracion comprimida ronda -15..-23 dBFS entre palabras: eso NO es silencio."""
    from _common import pcm_mono
    try:
        x = pcm_mono(path, None, None, 16000)
    except Exception:
        return None
    w = 4000
    n = x.size // w
    if n == 0:
        return None
    rms = np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1))
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    level = float(np.percentile(db, 90))
    thr = max(level - 20.0, -70.0)
    sil, s0 = [], None
    for i, v in enumerate(db):
        if v < thr and s0 is None:
            s0 = i
        if v >= thr and s0 is not None:
            if (i - s0) * 0.25 >= 0.4:
                sil.append((s0 * 0.25, i * 0.25))
            s0 = None
    if s0 is not None and (n - s0) * 0.25 >= 0.4:
        sil.append((s0 * 0.25, n * 0.25))
    return {"db": [round(float(v), 1) for v in db], "voice_level_db": round(level, 1), "silence_thr_db": round(thr, 1),
            "silences": [(round(a, 2), round(b, 2)) for a, b in sil], "peak_db": round(float(db.max()), 1)}


def transcribe(path, lang, model_name):
    try:
        from faster_whisper import WhisperModel
    except Exception:
        return None, "faster-whisper no instalado"
    import tempfile
    wav = os.path.join(tempfile.gettempdir(), "vu_audio.wav")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", path, "-vn", "-ar", "16000", "-ac", "1", wav], check=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, info = model.transcribe(wav, language=lang, vad_filter=True, word_timestamps=False)
    out = []
    for sg in segs:
        txt = sg.text.strip()
        why = []
        if sg.no_speech_prob >= 0.6:
            why.append(f"no_speech={sg.no_speech_prob:.2f}")
        if sg.avg_logprob < -1.0:
            why.append(f"logprob={sg.avg_logprob:.2f}")
        if HALLUCINATION.search(txt):
            why.append("frase tipica de alucinacion de Whisper")
        out.append({"s": round(sg.start, 2), "e": round(sg.end, 2), "text": txt, "no_speech": round(float(sg.no_speech_prob), 2),
                    "logprob": round(float(sg.avg_logprob), 2), "suspect": bool(why), "why": "; ".join(why)})
    return {"language": info.language, "language_prob": round(float(info.language_probability), 2), "segments": out}, None


# ----------------------------------------------------------------------------- fotogramas clave
def coverage_keyframes(shots, K, dur):
    """Muchos planos (> 64 y > presupuesto): K ventanas de tiempo iguales, un fotograma por ventana, del plano mas
    relevante (duracion^0.7 x movimiento) que la cubra. Respeta el presupuesto; algunos planos quedan sin fotograma propio."""
    w = lambda s: max(0.05, s["duration"]) ** 0.7 * (1 + 6 * s["motion"])
    kfs = []
    for i in range(K):
        a, b = dur * i / K, dur * (i + 1) / K
        best = None
        for s in shots:
            ov = min(b, s["end"]) - max(a, s["start"])
            if ov > 0:
                sc = w(s) * ov
                if best is None or sc > best[0]:
                    best = (sc, s, max(a, s["start"]), min(b, s["end"]))
        if best:
            _, sh, lo, hi = best
            kfs.append({"t": round(min(max((lo + hi) / 2, 0.0), max(dur - 0.04, 0.0)), 3), "shot": sh["id"], "why": "cobertura"})
    return kfs


def plan_keyframes(shots, budget, dur):
    """Hasta 64 planos: >=1 fotograma por plano (el presupuesto sube si hace falta) y el resto por duracion y movimiento.
    Con mas de 64 planos y mas planos que presupuesto: modo cobertura (respeta el presupuesto)."""
    n = len(shots)
    if n > 64 and n > budget:
        return coverage_keyframes(shots, budget, dur)
    budget = max(budget, n)
    extra = max(0, budget - n)
    weights = np.array([max(0.05, s["duration"]) ** 0.7 * (1 + 6 * s["motion"]) for s in shots])
    alloc = np.ones(n, int)
    if extra and weights.sum() > 0:
        add = np.floor(extra * weights / weights.sum()).astype(int)
        alloc += add
        rest = extra - int(add.sum())
        for i in np.argsort(-weights)[:rest]:
            alloc[i] += 1
    kfs = []
    for s, k in zip(shots, alloc):
        a, b, d = s["start"], s["end"], s["duration"]
        m = min(max(0.12 * d, 0.08), 0.5)
        if k == 1:
            ts = [(a + d / 2, "centro")]
        else:
            ts = [(a + m, "entrada")] + [(a + d * (j / (k - 1)), "intermedio") for j in range(1, k - 1)] + [(b - m, "salida")]
            if k >= 3 and s["motion"] >= 0.015:
                ts[len(ts) // 2] = (s["motion_peak_t"], "pico de movimiento")
        for t, why in ts:
            kfs.append({"t": round(min(max(t, 0.0), max(dur - 0.04, 0.0)), 3), "shot": s["id"], "why": why})
    kfs.sort(key=lambda x: x["t"])
    # dedupe: dos fotogramas a < 0.15 s no aportan
    out = []
    for k in kfs:
        if out and k["t"] - out[-1]["t"] < 0.15:
            continue
        out.append(k)
    return out


def extract_frame(path, t, out, long_side):
    vf = f"scale='if(gt(iw,ih),{long_side},-2)':'if(gt(iw,ih),-2,{long_side})'"
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", vf, "-q:v", "3", out],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sharpness(img):
    g = np.asarray(img.convert("L").resize((256, int(256 * img.height / img.width))), np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


def make_sheets(kfs, frames_dir, sheets_dir, portrait, max_w=1560):
    os.makedirs(sheets_dir, exist_ok=True)
    cols = 4 if portrait else 3
    cw = max_w // cols
    imgs = []
    for k in kfs:
        im = Image.open(k["file"]).convert("RGB")
        ch = int(cw * im.height / im.width)
        imgs.append((k, im.resize((cw, ch), Image.LANCZOS)))
    ch = max(i.height for _, i in imgs)
    label_h = 22
    rows_per = max(1, max_w // (ch + label_h))
    per = cols * rows_per
    sheets = []
    for si in range(0, len(imgs), per):
        chunk = imgs[si: si + per]
        rows = math.ceil(len(chunk) / cols)
        cv = Image.new("RGB", (cols * cw, rows * (ch + label_h)), BG)
        d = ImageDraw.Draw(cv)
        for j, (k, im) in enumerate(chunk):
            x, y = (j % cols) * cw, (j // cols) * (ch + label_h)
            cv.paste(im, (x, y))
            d.text((x + 4, y + ch + 3), f"#{k['n']:02d}  {tc(k['t'])}  plano {k['shot']}", fill=ACC, font=font(14))
            k["sheet"] = len(sheets) + 1
        p = os.path.join(sheets_dir, f"sheet_{len(sheets) + 1:02d}.png")
        cv.save(p, "PNG", optimize=True)
        sheets.append(p)
    return sheets


# ----------------------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("-o", "--out")
    ap.add_argument("--budget", type=int, default=24, help="fotogramas clave totales (>= numero de planos)")
    ap.add_argument("--fps", type=float, default=4.0, help="muestreo de analisis (4 = barato y suficiente)")
    ap.add_argument("--lang", default=None, help="idioma de la voz (es, en...). Por defecto, autodeteccion")
    ap.add_argument("--model", default="small"); ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--cut-sensitivity", type=float, default=1.0, help=">1 detecta mas cortes, <1 menos")
    ap.add_argument("--frame-size", type=int, default=640, help="lado largo de los fotogramas clave")
    a = ap.parse_args()

    video = os.path.abspath(a.video)
    if not os.path.exists(video):
        sys.exit("no existe: " + video)
    stem = os.path.splitext(os.path.basename(video))[0]
    out = os.path.abspath(a.out) if a.out else os.path.join(os.path.dirname(video), "analisis", stem)
    frames_dir, sheets_dir = os.path.join(out, "frames"), os.path.join(out, "sheets")
    for d in (frames_dir, sheets_dir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)

    info = probe(video)
    dur = info["duration"]
    if dur <= 0 or not info["width"]:
        sys.exit("no se pudo leer el video (ffprobe)")
    portrait = info["height"] > info["width"]
    print(f"[1/5] {os.path.basename(video)}  {info['width']}x{info['height']}  {info['fps']} fps  {dur:.2f}s  audio={info['has_audio']}")

    print("[2/5] planos y movimiento ...")
    frames = decode_small(video, a.fps)
    if len(frames) < 2:
        sys.exit("no se pudieron decodificar fotogramas")
    cuts, scores = detect_cuts(video, frames, a.fps, a.cut_sensitivity)
    cuts = [c for c in cuts if 0.2 < c[0] < dur - 0.2]
    bounds = [0.0] + [c[0] for c in cuts] + [dur]
    kinds = ["inicio"] + [c[1] for c in cuts]
    shots = []
    for i in range(len(bounds) - 1):
        t0, t1 = bounds[i], bounds[i + 1]
        st = shot_stats(frames, a.fps, t0, t1)
        shots.append({"id": i + 1, "start": round(t0, 2), "end": round(t1, 2), "duration": round(t1 - t0, 2), "enters_with": kinds[i],
                      "motion": round(st["motion"], 4), "motion_label": motion_label(st["motion"]),
                      "brightness": round(st["brightness"], 3), "motion_peak_t": st["motion_peak_t"]})
    black = [s["id"] for s in shots if s["brightness"] < 0.04]

    print("[3/5] audio y voz ...")
    audio = speech = None
    speech_err = None
    if info["has_audio"]:
        audio = audio_profile(video, dur)
        if not a.no_transcribe:
            try:
                speech, speech_err = transcribe(video, a.lang, a.model)
            except Exception as e:  # noqa
                speech_err = f"{type(e).__name__}: {e}"
    else:
        speech_err = "sin pista de audio"
    vad = None
    if info["has_audio"] and vad_analyze:
        try:
            vad = vad_analyze(video)
        except Exception as e:  # noqa
            print("  VAD no disponible:", e)
    if vad and speech:
        for g in speech["segments"]:
            g["vad_overlap"] = round(overlap_ratio(vad["speech"], g["s"], g["e"]), 2)
            if g["vad_overlap"] < 0.5:
                g["suspect"] = True
                g["why"] = (g["why"] + "; " if g["why"] else "") + f"VAD: solo {g['vad_overlap'] * 100:.0f}% del segmento tiene voz"

    print("[4/5] fotogramas clave ...")
    kfs = plan_keyframes(shots, a.budget, dur)
    for n, k in enumerate(kfs, 1):
        k["n"] = n
        k["file"] = os.path.join(frames_dir, f"f_{n:02d}_{int(k['t'] * 100):05d}.jpg")
        extract_frame(video, k["t"], k["file"], a.frame_size)
    kfs = [k for k in kfs if os.path.exists(k["file"])]
    for k in kfs:
        k["sharpness"] = round(sharpness(Image.open(k["file"])), 1)
    sheets = make_sheets(kfs, frames_dir, sheets_dir, portrait)

    print("[5/5] mapa ...")
    for s in shots:
        s["keyframes"] = [k["n"] for k in kfs if k["shot"] == s["id"]]
        s["speech"] = [g["text"] for g in (speech or {}).get("segments", []) if not g["suspect"] and g["e"] > s["start"] and g["s"] < s["end"]]
        pa = [(x, y) for x, y, _ in vad["pauses"]] if vad else (audio["silences"] if audio else None)
        if pa is not None:
            s["silence_s"] = round(sum(max(0, min(b, s["end"]) - max(a_, s["start"])) for a_, b in pa), 2)
    speech_s = sum(min(g["e"], dur) - g["s"] for g in (speech or {}).get("segments", []) if not g["suspect"])
    gaps = unknowns(info, shots, audio, speech, speech_err, black, kfs, a.budget)

    data = {"video": video, "info": info, "params": {"fps": a.fps, "budget": a.budget, "cut_sensitivity": a.cut_sensitivity},
            "shots": shots, "keyframes": [{k: v for k, v in kf.items() if k != "file"} | {"file": os.path.relpath(kf["file"], out)} for kf in kfs],
            "sheets": [os.path.relpath(s, out) for s in sheets],
            "audio": ({k: v for k, v in audio.items() if k != "db"} | {"db_per_0.25s": audio["db"]}) if audio else None,
            "speech": speech, "vad": vad, "speech_seconds": round(speech_s, 1), "speech_error": speech_err, "gaps": gaps}
    with open(os.path.join(out, "video-map.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    md = render_md(data, out)
    with open(os.path.join(out, "video-map.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\nlisto: {out}\n  planos={len(shots)}  fotogramas={len(kfs)}  hojas={len(sheets)}")
    print("  SIGUIENTE: Read de cada sheets/sheet_NN.png en orden, luego escribir understanding.md (assets/understanding-template.md)")


def ids(lst, n=12):
    lst = list(lst)
    return str(lst[:n]) + (f" (+{len(lst) - n} mas)" if len(lst) > n else "")


def unknowns(info, shots, audio, speech, speech_err, black, kfs, budget):
    g = []
    if not info["has_audio"]:
        g.append("Sin audio: no hay voz ni musica que interpretar.")
    elif info.get("audio_duration") and info["audio_duration"] < info["duration"] - 0.5:
        g.append(f"EL AUDIO ES MAS CORTO QUE EL VIDEO: {info['audio_duration']:.2f} s de audio contra {info['duration']:.2f} s de video. "
                 f"Desde {info['audio_duration']:.1f} s el video queda MUDO (revisar si es intencional o un fallo de exportacion).")
    if not info["has_audio"]:
        pass
    elif speech is None:
        g.append(f"Voz NO transcrita ({speech_err}). Sin transcripcion no se entiende el contenido hablado.")
    elif not [x for x in speech["segments"] if not x["suspect"]]:
        n_sus = len(speech["segments"])
        g.append("No hay voz fiable: el audio es musica/ambiente"
                 + (f" ({n_sus} segmento(s) de Whisper descartados por sospechosos: probable alucinacion sobre musica)" if n_sus else "")
                 + ". Claude NO escucha: musica, efectos y tono se infieren solo por energia (hoja Audio) y por la imagen.")
    elif any(x["suspect"] for x in speech["segments"]):
        g.append(f"{sum(x['suspect'] for x in speech['segments'])} segmento(s) de transcripcion marcados como sospechosos y excluidos de la columna de voz (ver seccion Transcripcion).")
    elif speech["language_prob"] < 0.6:
        g.append(f"Idioma poco seguro ({speech['language']} {speech['language_prob']}): revisar o fijar --lang.")
    if vad_analyze is None:
        g.append("Sin VAD (falta faster-whisper): la validacion cruzada de la transcripcion no se hizo.")
    if info["hdr"]:
        g.append("Video HDR: los colores de los fotogramas pueden verse lavados/sobresaturados (falta tonemap).")
    if black:
        g.append(f"Planos casi negros: {ids(black)}. Puede ser fundido a negro o un fallo.")
    blurry = [k["n"] for k in kfs if k.get("sharpness", 999) < 15]
    if blurry:
        g.append(f"Fotogramas con baja nitidez o color plano (desenfoque, destello, fundido): #{ids(blurry)}. No sacar conclusiones de detalle de ellos; usar frame_probe.py.")
    fast = [s["id"] for s in shots if s["motion_label"] == "alto" and s["duration"] > 1.5]
    if fast:
        g.append(f"Planos con mucho movimiento: {ids(fast)}. 1-3 fotogramas no describen la accion; usar frame_probe.py --span para una rafaga.")
    soft = [x["id"] for x in shots if x["enters_with"] == "gradual/animado"]
    if soft:
        g.append(f"Entradas 'gradual/animado' en los planos {ids(soft)}: clasificacion HEURISTICA (dominancia del salto < 2.5). Confirmar mirando los fotogramas de salida/entrada vecinos.")
    missing = [x["id"] for x in shots if not x.get("keyframes")]
    if missing:
        g.append(f"MODO COBERTURA: {len(missing)} de {len(shots)} planos no tienen fotograma propio (presupuesto {budget}; ~1 fotograma cada {info['duration'] / max(len(kfs), 1):.0f} s). "
                 f"Para mas detalle subir --budget o sondear tramos con frame_probe.py --from A --to B.")
    elif len(kfs) >= budget:
        g.append(f"Se alcanzo el presupuesto de {budget} fotogramas: para mas detalle, subir --budget o sondear tramos con frame_probe.py.")
    g.append("No se mide: sincronia fina labios/audio, calidad de musica/efectos, identidad de personas, texto muy pequeno (usar frame_probe.py --crop/--scale), ni continuidad entre planos que no se ven.")
    return g


def render_md(d, out):
    i = d["info"]
    L = [f"# Mapa del video: {os.path.basename(d['video'])}", "",
         f"- **Formato**: {i['width']}x{i['height']} ({'vertical' if i['height'] > i['width'] else 'horizontal' if i['width'] > i['height'] else 'cuadrado'}), {i['fps']} fps, {tc(i['duration'])} ({i['duration']:.2f}s), codec {i['codec']}",
         f"- **Audio**: {'si (' + str(i['audio_codec']) + ')' if i['has_audio'] else 'no'}"
         + (f"; voz fiable {d['speech_seconds']} s ({d['speech']['language']}, p={d['speech']['language_prob']})" if d.get("speech") and d["speech_seconds"] > 0 else "; sin voz fiable"),
         f"- **Planos**: {len(d['shots'])}  |  **Fotogramas clave**: {len(d['keyframes'])}  |  **Hojas**: {len(d['sheets'])}",
         f"- Generado con muestreo {d['params']['fps']} fps, sensibilidad de cortes {d['params']['cut_sensitivity']}. Los tiempos de corte estan afinados al fotograma; el movimiento es una MEDIDA (diferencia de brillo entre fotogramas), no una interpretacion.", "",
         "## Linea de tiempo por planos", "",
         "| Plano | Entra con | Inicio | Fin | Dur | Movimiento | Silencio | Fotogramas | Voz en el plano |", "|---|---|---|---|---|---|---|---|---|"]
    for s in d["shots"]:
        sp = " / ".join(s["speech"])[:140] if s["speech"] else "—"
        L.append(f"| {s['id']} | {s['enters_with']} | {tc(s['start'])} | {tc(s['end'])} | {s['duration']}s | {s['motion_label']} ({s['motion']}) | {s.get('silence_s', '—')}s | {', '.join('#' + str(n) for n in s['keyframes'])} | {sp} |")
    L += ["", "## Hojas de contacto (LEER EN ORDEN con Read)", ""]
    for n, p in enumerate(d["sheets"], 1):
        ks = [k for k in d["keyframes"] if k["sheet"] == n]
        L.append(f"- `{p}` — fotogramas #{ks[0]['n']}–#{ks[-1]['n']} ({tc(ks[0]['t'])} → {tc(ks[-1]['t'])})")
    L += ["", "## Fotogramas clave", "", "| # | Tiempo | Plano | Motivo | Nitidez | Archivo |", "|---|---|---|---|---|---|"]
    for k in d["keyframes"]:
        L.append(f"| {k['n']} | {tc(k['t'])} ({k['t']}s) | {k['shot']} | {k['why']} | {k['sharpness']} | `{k['file']}` |")
    if d.get("speech") and d["speech"]["segments"]:
        L += ["", "## Transcripcion con tiempos (local, faster-whisper; puede contener errores)", ""]
        for g in d["speech"]["segments"]:
            flag = f"  **[SOSPECHOSO, no usar: {g['why']}]**" if g["suspect"] else ""
            L.append(f"- [{tc(g['s'])}–{tc(g['e'])}] {g['text']}{flag}")
    if d.get("vad"):
        v = d["vad"]
        L += ["", "## Voz y pausas (Silero VAD, local)", "",
              f"- Voz detectada {v['speech_seconds']} s ({v['speech_ratio'] * 100:.0f} % del video) en {len(v['speech'])} tramos.",
              "- Pausas >= " + str(v["params"]["pause_min"]) + " s: " + (", ".join(f"{tc(x)}–{tc(y)} ({z}s)" for x, y, z in v["pauses"]) if v["pauses"] else "ninguna")]
    if d.get("audio"):
        a = d["audio"]
        L += ["", "## Audio", "", f"- Pico {a['peak_db']} dBFS, nivel de voz (p90) {a['voice_level_db']} dBFS, umbral de silencio {a['silence_thr_db']} dBFS (20 dB bajo la voz).",
              "- Silencios por energia >= 0.4 s (secundario; la fuente principal es el VAD): " + (", ".join(f"{tc(x)}–{tc(y)}" for x, y in a["silences"]) if a["silences"] else "ninguno")]
    L += ["", "## Lo que este mapa NO puede decirme (y como cubrirlo)", ""] + [f"- {g}" for g in d["gaps"]]
    L += ["", "## Siguiente paso", "",
          "1. `Read` de cada hoja en orden (cada una cuesta ~1.5–2.5k tokens). 2. Anotar por plano QUE SE VE (visto) / QUE SE INFIERE / QUE NO SE SABE. 3. Para dudas: `frame_probe.py`. 4. Guardar `understanding.md` junto a este mapa.", ""]
    return "\n".join(L)


if __name__ == "__main__":
    main()
