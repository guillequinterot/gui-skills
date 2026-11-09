#!/usr/bin/env python
"""Audita la SINCRONÍA entre el sonido y la imagen de una pieza, y su nivel, sin oír nada.

Claude no oye. Lo que sí se puede MEDIR: cuándo suenan los golpes (onsets) del audio ya mezclado, a cuántos milisegundos caen de cada
cue de la imagen (un corte, un golpe de texto, una tarjeta que aterriza), con qué frecuencia caería «por azar» y cuál es el volumen y
el pico del MP4 entregado. Lo demás (que SUENE bien) lo decide una persona con auriculares: el script marca los 5 cues más arriesgados
para esa escucha. Ideas de earshot, video-director y huashu-motion (MIT), reimplementadas desde cero con numpy + ffmpeg (sin torch,
sin modelos, sin red).

Uso:
  python sync_audit.py pieza.mp4 --cues cues.json [--fps 30] [--early 45 --late 75] [--json salida.json]
  python sync_audit.py pieza.mp4 --cuts            # los cues son los cortes de IMAGEN detectados en el propio video
  cues.json: [1.0, 2.5] | [{"t": 1.0, "type": "scene_cut"}, {"f": 75, "type": "impact"}] | {"fps": 30, "events": [...]}

Lectura de resultados:
  offset = instante del golpe - instante del cue (ms); negativo = el sonido va ADELANTADO. Se acepta desde -early (45 ms) hasta +late
  (75 ms): el oído tolera mejor un sonido temprano que tardío; un retraso de 2 fotogramas o más ya se nota. Ventana de percepción
  citada por la fuente (ITU-R BT.1359: -45/+125 ms; acentos de películas profesionales entre -45 y +75 ms).
  azar = fracción del tiempo que quedaría «cubierta» por algún golpe con esa tolerancia. Si el audio es denso (música continua), el azar
  sube y una sincronía alta ya no significa nada: compara siempre contra él.
  El volumen objetivo por defecto es -16 LUFS ±1 y pico <= -1.0 dBTP (el de esta skill); para redes con normalización a -14, pasa --lufs -14.
Límites: un golpe de efecto bajo música densa puede quedar tapado por la música (el onset es de la MEZCLA); el detector no sabe QUÉ suena.
"""
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, pcm_mono, measure_loudness, probe_duration  # noqa: E402
import subprocess

SR = 16000
NFFT, HOP = 512, 80          # 32 ms de ventana, 5 ms de paso
BANDS = 32


def onsets(x):
    """Tiempos (s) de ataques: flujo espectral tipo «superflux» en log-bandas + umbral robusto (mediana/MAD) + afinado en envolvente de 1 ms."""
    if len(x) < NFFT * 4:
        return []
    win = np.hanning(NFFT)
    fr = np.lib.stride_tricks.sliding_window_view(x, NFFT)[::HOP]
    mag = np.abs(np.fft.rfft(fr * win, axis=1)) + 1e-6
    edges = np.unique(np.round(np.geomspace(2, NFFT // 2, BANDS + 1)).astype(int))
    L = np.stack([20 * np.log10(mag[:, a:b].mean(axis=1)) for a, b in zip(edges[:-1], edges[1:])], axis=1)
    L = np.maximum(L, L.max() - 80)
    ref = np.maximum(np.maximum(L[:-1], np.roll(L[:-1], 1, axis=1)), np.roll(L[:-1], -1, axis=1))   # máximo local de 3 bandas del fotograma previo
    flux = np.maximum(L[1:] - ref, 0).mean(axis=1)
    w = 401
    pad = np.pad(flux, (w // 2, w // 2), mode="edge")
    sw = np.lib.stride_tricks.sliding_window_view(pad, w)[:len(flux)]
    med = np.median(sw, axis=1)
    mad = np.median(np.abs(sw - med[:, None]), axis=1)
    z = (flux - med) / (1.4826 * mad + 0.02 * np.percentile(flux, 99) + 1e-9)
    fmax = float(np.percentile(flux, 99.5))
    peaks = []
    for i in range(5, len(z) - 5):
        if z[i] >= 3.0 and flux[i] >= 0.15 * fmax and z[i] == z[i - 5:i + 6].max():
            peaks.append(i)
    out, last = [], -1
    env = np.abs(x)
    nb = len(env) // 16
    env = env[:nb * 16].reshape(nb, 16).max(axis=1)           # envolvente de 1 ms
    for i in peaks:
        tc = ((i + 1) * HOP + NFFT / 2) / SR
        a, b = max(0, int((tc - 0.045) * 1000)), min(len(env) - 1, int((tc + 0.015) * 1000))
        if b <= a:
            continue
        pk = a + int(np.argmax(env[a:b + 1]))
        f0, f1 = max(0, int((tc - 0.15) * 1000)), max(1, int((tc - 0.05) * 1000))
        floor = float(np.median(env[f0:f1])) if f1 > f0 else 0.0
        if env[pk] < 2.0 * max(floor, 1e-4):          # el golpe debe sobresalir >= 6 dB de la cama local
            continue
        thr = floor + 0.1 * (env[pk] - floor)
        j = pk
        while j > a and env[j - 1] > thr:
            j -= 1
        t = j / 1000.0
        if last < 0 or t - last >= 0.030:
            out.append(round(t, 4)); last = t
    return out


def detect_cuts(path):
    """Cortes de imagen: diferencia media entre fotogramas grises de 96x54 (0..1); pico local > 4x la mediana de ±1 s, o un salto >= 15 %."""
    from _common import probe_stream
    st = probe_stream(path)
    a, _, b = (st.get("avg_frame_rate") or "30/1").partition("/")
    try:
        fps = float(a) / float(b or 1) or 30.0
    except ValueError:
        fps = 30.0
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", "scale=96:54:flags=area,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, timeout=900).stdout
    n = len(raw) // (96 * 54)
    F = np.frombuffer(raw[:n * 96 * 54], dtype=np.uint8).reshape(n, 54 * 96).astype(np.float32)
    d = np.abs(F[1:] - F[:-1]).mean(axis=1) / 255.0
    cuts, last = [], -1.0
    for i in range(1, len(d) - 1):
        lo, hi = max(0, i - int(fps)), min(len(d), i + int(fps) + 1)
        base = float(np.median(d[lo:hi]))
        loc = d[i] >= d[i - 1] and d[i] >= d[i + 1]
        if loc and ((d[i] > 0.012 and d[i] > 4 * base + 0.004) or d[i] >= 0.15):
            t = (i + 1) / fps
            if t - last >= 0.12:
                cuts.append(round(t, 3)); last = t
    return cuts


def load_cues(path, fps):
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, dict):
        fps = d.get("fps", fps)
        d = d.get("events", [])
    cues = []
    for k, c in enumerate(d):
        if isinstance(c, (int, float)):
            cues.append({"t": float(c), "type": "cue", "id": f"c{k}"})
        else:
            t = c.get("t") if c.get("t") is not None else (c["f"] / fps if c.get("f") is not None else None)
            if t is not None:
                cues.append({"t": float(t), "type": c.get("type") or c.get("kind") or "cue", "id": c.get("id") or f"c{k}"})
    return cues


def audit(cues, ons, dur, early_ms, late_ms):
    res = []
    for c in cues:
        near = [(o - c["t"], o) for o in ons if abs(o - c["t"]) <= 0.25]
        if not near:
            res.append({**c, "estado": "sin sonido", "offset_ms": None}); continue
        off = min(near, key=lambda p: abs(p[0]))[0] * 1000
        ok = -early_ms <= off <= late_ms
        est = "ok" if ok else ("cerca" if abs(off) <= 100 else "fuera")
        res.append({**c, "estado": est, "offset_ms": round(off, 1)})
    # azar: fracción del tiempo cubierta por la ventana [o - late, o + early] de algún golpe
    grid = np.arange(0, max(dur, 0.1), 0.005)
    cov = np.zeros(len(grid), dtype=bool)
    for o in ons:
        cov |= (grid >= o - late_ms / 1000) & (grid <= o + early_ms / 1000)
    chance = float(cov.mean()) if len(grid) else 0.0
    return res, chance


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media")
    ap.add_argument("--cues")
    ap.add_argument("--cuts", action="store_true", help="usar como cues los cortes de imagen detectados en el mismo video")
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--early", type=float, default=45.0, help="ms de adelanto aceptados")
    ap.add_argument("--late", type=float, default=75.0, help="ms de retraso aceptados")
    ap.add_argument("--lufs", type=float, default=-16.0)
    ap.add_argument("--lufs-tol", type=float, default=1.0)
    ap.add_argument("--tp", type=float, default=-1.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    if not a.cues and not a.cuts:
        sys.exit("ERROR: indica --cues cues.json o --cuts")
    dur = probe_duration(a.media)
    try:
        x = pcm_mono(a.media, sr=SR)
    except Exception as e:  # noqa
        sys.exit(f"ERROR: no pude leer el audio ({e}); ¿el archivo tiene pista de audio?")
    ons = onsets(x)
    cues = load_cues(a.cues, a.fps) if a.cues else [{"t": t, "type": "corte de imagen", "id": f"cut{k}"} for k, t in enumerate(detect_cuts(a.media))]
    res, chance = audit(cues, ons, dur, a.early, a.late)
    n_ok = sum(1 for r in res if r["estado"] == "ok")
    offs = [r["offset_ms"] for r in res if r["offset_ms"] is not None]
    lufs, tp = measure_loudness(a.media)
    rep = {"media": a.media, "duracion_s": round(dur, 2), "golpes_detectados": len(ons), "golpes_por_s": round(len(ons) / max(dur, 0.1), 2),
           "cues": len(res), "ok": n_ok, "ok_pct": round(100 * n_ok / len(res), 1) if res else None,
           "azar_pct": round(100 * chance, 1), "offset_mediano_ms": round(float(np.median(offs)), 1) if offs else None,
           "sin_sonido": sum(1 for r in res if r["estado"] == "sin sonido"), "lufs": lufs, "pico_dbfs": tp, "detalle": res}
    print(f"# sincronía — {os.path.basename(a.media)}: {rep['golpes_detectados']} golpes en {rep['duracion_s']} s ({rep['golpes_por_s']}/s), {len(res)} cues")
    print(f"{'cue':<10} {'tipo':<16} {'t (s)':>7} {'offset ms':>10}  estado")
    for r in res:
        print(f"{r['id']:<10} {str(r['type'])[:16]:<16} {r['t']:7.3f} {('%+.0f' % r['offset_ms']) if r['offset_ms'] is not None else '   —':>10}  {r['estado']}")
    if res:
        print(f"RESUMEN: {n_ok}/{len(res)} cues con golpe entre -{a.early:.0f} y +{a.late:.0f} ms ({rep['ok_pct']} %), azar {rep['azar_pct']} %; "
              f"offset mediano {rep['offset_mediano_ms']} ms; sin sonido: {rep['sin_sonido']}")
        if rep["azar_pct"] > 40:
            print("  AVISO: el audio es denso (azar > 40 %): una sincronía alta no demuestra nada; mira el offset de cada cue")
        if offs and abs(np.median(offs)) > 30 and len(offs) >= 3:
            print(f"  AVISO: offset mediano {np.median(offs):+.0f} ms: parece un retardo constante (códec o colocación); corrígelo con una constante en la colocación de los efectos")
        risky = sorted(res, key=lambda r: (r["estado"] != "sin sonido", -(abs(r["offset_ms"]) if r["offset_ms"] is not None else 0)))[:5]
        print("PARA ESCUCHAR CON AUDÍFONOS (los 5 más arriesgados): " + ", ".join(f"{r['t']:.2f}s ({r['estado']})" for r in risky))
    if lufs is not None:
        flag = "OK" if abs(lufs - a.lufs) <= a.lufs_tol else "FUERA"
        print(f"volumen: {lufs} LUFS (objetivo {a.lufs} ±{a.lufs_tol}: {flag}); pico {tp} dBFS (tope {a.tp}: {'OK' if tp is not None and tp <= a.tp else 'FUERA'})")
    print("NO VERIFICADO: que suene bien, que el efecto sea el adecuado y que no tape la voz (lo decide una persona escuchando).")
    if a.json:
        json.dump(rep, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
