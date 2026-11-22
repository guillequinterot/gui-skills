#!/usr/bin/env python
"""Verifica un MP4 entregable DECODIFICANDO fotogramas reales (no solo leyendo metadatos): duración exacta, etiquetas de color,
color del fondo en el fotograma 0, costura de bucle a resolución completa, sondas de color en un instante y pico/volumen del audio.

Por qué existe: un video puede salir "bien" en el reproductor y estar mal: el rango de color leído al revés levanta #0a0a0a hasta #171717 (una
caja gris sobre una página oscura), un MP4 sin etiquetas BT.709 cambia de tono según el reproductor, un bucle "cerrado" salta en la costura, el pico tras
AAC pasa de -1 dBTP. Idea de `product-film` (Rieranthony, MIT) y de `cinetic` (Leonxlnx, MIT: BT.709 etiquetado, pico tras el códec),
reimplementada desde cero y con una red de seguridad: si el MP4 no trae etiquetas, se decodifica asumiendo BT.709 / rango TV (el estándar
de la web en HD) y se AVISA, para que el color medido no dependa de la suposición silenciosa de ffmpeg.

Uso:
  python verify_entrega.py pieza.mp4 [--duration 52.8] [--bg 10,10,10] [--bg-at 960,540] [--bg-tol 3] [--probe 9.4:944,800 ...]
                           [--loop] [--matrix bt709|bt601] [--lufs -16 --lufs-tol 1.5] [--json salida.json]
Códigos de salida: 0 = todo bien (los AVISOS no fallan), 1 = algún FALLO, 2 = no se pudo leer el archivo.
Lo que NO verifica: que el tono SE VEA bien (compara números con la intención declarada), el movimiento, ni que el audio SUENE bien.
"""
import argparse, json, os, re, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, FFPROBE, run, measure_loudness  # noqa: E402


def probe(path):
    r = run([FFPROBE, "-v", "error", "-show_entries",
             "stream=index,codec_type,codec_name,width,height,pix_fmt,avg_frame_rate,nb_frames,color_range,color_space,color_transfer,color_primaries,duration:format=duration",
             "-of", "json", str(path)])
    try:
        return json.loads(r.stdout)
    except Exception:
        return {}


def fps_of(v):
    a, _, b = (v.get("avg_frame_rate") or "30/1").partition("/")
    try:
        return float(a) / float(b or 1) or 30.0
    except ValueError:
        return 30.0


def frame_at(path, t, w, h, vf):
    cmd = [FFMPEG, "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-vf", vf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True, timeout=300).stdout
    if len(raw) < w * h * 3:
        return None
    return np.frombuffer(raw[: w * h * 3], dtype=np.uint8).reshape(h, w, 3).astype(int)


def patch(arr, x, y, r=4):
    h, w = arr.shape[:2]
    x0, x1, y0, y1 = max(0, x - r), min(w, x + r + 1), max(0, y - r), min(h, y + r + 1)
    return [int(v) for v in np.median(arr[y0:y1, x0:x1].reshape(-1, 3), axis=0)]


def verify(a):
    rep = {"video": a.video, "fallos": [], "avisos": [], "ok": []}
    info = probe(a.video)
    streams = info.get("streams") or []
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    au = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not v:
        rep["fallos"].append("no se pudo leer un flujo de video")
        return rep
    w, h, fps = int(v["width"]), int(v["height"]), fps_of(v)
    dur = float((info.get("format") or {}).get("duration") or v.get("duration") or 0)
    rep["spec"] = {"ancho": w, "alto": h, "fps": round(fps, 3), "pix_fmt": v.get("pix_fmt"), "duracion": round(dur, 3), "audio": bool(au)}

    if a.duration is not None:
        tol = a.dur_tol if a.dur_tol is not None else 1.5 / fps
        (rep["ok"] if abs(dur - a.duration) <= tol else rep["fallos"]).append(
            f"duración {dur:.3f} s frente a {a.duration:.3f} s esperados (tolerancia {tol:.3f} s)")

    tags = {k: v.get(k) for k in ("color_range", "color_space", "color_transfer", "color_primaries")}
    rep["etiquetas"] = tags
    untagged = not any(tags.values())
    hd = h >= 720
    if untagged:
        rep["avisos"].append("el MP4 NO trae etiquetas de color: cada reproductor adivina el tono. Reetiqueta al exportar "
                             "(-color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709). "
                             "Aquí se decodifica ASUMIENDO " + ("BT.709" if a.matrix == "bt709" else "BT.601") + " / rango TV.")
    else:
        if hd and tags.get("color_space") not in (None, "bt709"):
            rep["avisos"].append(f"color_space {tags.get('color_space')} en un video HD (se esperaba bt709)")
        if tags.get("color_range") not in (None, "tv", "limited"):
            rep["avisos"].append(f"color_range {tags.get('color_range')}: si el destino espera rango TV el fondo saldrá distinto (mide con --bg)")
        if all(tags.get(k) for k in ("color_range", "color_space")) and tags.get("color_space") == "bt709" and tags.get("color_range") == "tv":
            rep["ok"].append("etiquetas BT.709 / rango TV")

    # decodificación con la matriz declarada (si no hay etiquetas, la asumida): así el número no depende de un valor por defecto oculto
    matrix = "bt709" if a.matrix == "bt709" else "bt601"
    vf = f"scale=in_range=tv:in_color_matrix={matrix}:out_range=pc:out_color_matrix={matrix}:flags=accurate_rnd+full_chroma_int"
    f0 = frame_at(a.video, 0.0, w, h, vf)
    if f0 is None:
        rep["fallos"].append("no se pudo decodificar el fotograma 0")
        return rep
    rep["fotograma0_medio"] = [int(x) for x in f0.reshape(-1, 3).mean(axis=0)]

    if a.bg:
        bg = np.array([int(x) for x in a.bg.split(",")])
        bx, by = (int(x) for x in a.bg_at.split(",")) if a.bg_at else (w // 2, h // 2)
        got = patch(f0, min(bx, w - 1), min(by, h - 1))
        ok = bool(np.all(np.abs(np.array(got) - bg) <= a.bg_tol))
        (rep["ok"] if ok else rep["fallos"]).append(
            f"fondo del fotograma 0 en ({bx},{by}): decodifica {got}, esperado {bg.tolist()} ±{a.bg_tol}"
            + ("" if ok else " — ¿rango de color leído al revés (fondo más claro) o matriz equivocada? No cambies los tokens: arregla la conversión de color"))

    if a.loop:
        cmd = [FFMPEG, "-v", "error", "-ss", f"{max(0.0, dur - 0.5):.3f}", "-i", a.video, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        raw = subprocess.run(cmd, capture_output=True, timeout=300).stdout
        n = len(raw) // (w * h * 3)
        if n:
            last = np.frombuffer(raw[(n - 1) * w * h * 3: n * w * h * 3], dtype=np.uint8).reshape(h, w, 3).astype(int)
            diff = np.abs(f0 - last).max(axis=2)
            noisy = int((diff > 3).sum())
            ok = noisy < 0.001 * w * h and int(diff.max()) < 24
            (rep["ok"] if ok else rep["fallos"]).append(
                f"bucle: último fotograma contra el 0 -> {noisy} px con diferencia > 3, máximo {int(diff.max())} "
                + ("(solo ruido del códec)" if ok else "(la costura SALTA)"))
        else:
            rep["avisos"].append("bucle: no se pudo decodificar el último fotograma")

    for pr in a.probe:
        try:
            when, pt = pr.split(":")
            x, y = (int(q) for q in pt.split(","))
            fr = frame_at(a.video, float(when), w, h, vf)
            rep.setdefault("sondas", []).append({"t": float(when), "x": x, "y": y, "rgb": patch(fr, x, y) if fr is not None else None})
        except Exception as e:  # noqa
            rep["avisos"].append(f"sonda {pr}: {e}")

    if au:
        lufs, peak = measure_loudness(a.video)
        rep["audio"] = {"lufs": lufs, "pico_dbfs": peak}
        if peak is not None:
            (rep["ok"] if peak <= -1.0 else rep["avisos"]).append(
                f"pico del audio tras el códec {peak} dBFS " + ("(≤ -1)" if peak <= -1.0 else "(> -1 dBTP: recodifica el audio con más margen)"))
        if a.lufs is not None and lufs is not None:
            (rep["ok"] if abs(lufs - a.lufs) <= a.lufs_tol else rep["avisos"]).append(
                f"volumen integrado {lufs} LUFS frente a {a.lufs} ±{a.lufs_tol}")
    elif a.audio_required:
        rep["fallos"].append("la pieza debía llevar audio y no tiene flujo de audio")
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("--duration", type=float); ap.add_argument("--dur-tol", type=float)
    ap.add_argument("--bg", help="R,G,B esperado del fondo en el fotograma 0")
    ap.add_argument("--bg-at", help="x,y donde medir el fondo (por defecto el centro)")
    ap.add_argument("--bg-tol", type=int, default=3)
    ap.add_argument("--probe", action="append", default=[], help="t:x,y -> imprime el RGB decodificado (acento, superficie)")
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--matrix", choices=["bt709", "bt601"], default="bt709", help="matriz asumida si el MP4 no trae etiquetas")
    ap.add_argument("--lufs", type=float); ap.add_argument("--lufs-tol", type=float, default=1.5)
    ap.add_argument("--audio-required", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if not os.path.exists(a.video):
        print("ERROR: no existe", a.video); sys.exit(2)
    r = verify(a)
    print(f"# verify_entrega - {os.path.basename(a.video)}  {r.get('spec', '')}")
    for k, sym in (("ok", "OK   "), ("avisos", "AVISO"), ("fallos", "FALLA")):
        for m in r[k]:
            print(f"  {sym} {m}")
    for s in r.get("sondas", []):
        print(f"  sonda t={s['t']} ({s['x']},{s['y']}): {s['rgb']}")
    print("Compara números con la intención declarada; no certifica que el tono se vea bien ni que el audio suene bien.")
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if r["fallos"] else 0)


if __name__ == "__main__":
    main()
