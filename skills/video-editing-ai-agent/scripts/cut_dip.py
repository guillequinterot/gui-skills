#!/usr/bin/env python
"""Mide, con numeros, lo que pasa alrededor de un corte/transicion: bajon de brillo y hueco oscuro.

Sirve para comparar dos versiones de una transicion (p. ej. cut-the-curve con atenuacion vs push) sin fiarse solo del ojo.

Uso:
  python cut_dip.py video.mp4 --cuts 22.87,36.75 [--window 0.5] [--fps 30] [--gap-thr 0.07] [--json out.json]
Por corte, en la ventana [corte-window, corte+window] a --fps fotogramas por segundo:
  dip      : brillo medio minimo / media de los brillos de los fotogramas de borde (1.00 = sin bajon; 0.60 = bajon del 40 %)
  gap_max  : mayor porcentaje del ANCHO del cuadro que queda en columnas "vacias" (todas sus filas casi negras, < --gap-thr)
  gap_frames : cuantos fotogramas tienen algun hueco > 2 % del ancho
  t_dip    : instante del fotograma mas oscuro
Notas: **dip no llega a 1.00 aunque la transicion sea perfecta si las dos escenas tienen distinto brillo** (p. ej. pagina blanca -> selva oscura); el indicador limpio de un hueco/atenuacion es gap_max. El hueco se detecta por columnas de color de fondo oscuro; una escena realmente oscura puede dar falsos huecos
(compara siempre dos versiones del MISMO material). Es una medida, no un juicio estetico: mira los fotogramas.
"""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG  # noqa: E402

W = H = 96


def frames(path, start, dur, fps):
    cmd = [FFMPEG, "-v", "error", "-ss", f"{max(start, 0):.3f}", "-t", f"{dur:.3f}", "-i", path, "-an",
           "-vf", f"fps={fps},scale={W}:{H}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[: n * W * H], np.uint8).reshape(n, H, W).astype(np.float32) / 255.0


def measure(path, cut, window, fps, gap_thr):
    a = max(cut - window, 0.0)
    f = frames(path, a, 2 * window, fps)
    if len(f) < 4:
        return {"cut": cut, "error": "sin fotogramas"}
    mean = f.mean(axis=(1, 2))
    edge = (mean[:3].mean() + mean[-3:].mean()) / 2
    k = int(np.argmin(mean))
    col_empty = (f.max(axis=1) < gap_thr)            # (n, W): columna sin ningun pixel claro
    gap = col_empty.mean(axis=1)                     # fraccion del ancho vacia por fotograma
    return {"cut": cut, "frames": int(len(f)), "dip": round(float(mean[k] / edge), 3), "t_dip": round(a + k / fps, 3),
            "gap_max_pct": round(float(gap.max() * 100), 1), "gap_frames": int((gap > 0.02).sum())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--cuts", required=True)
    ap.add_argument("--window", type=float, default=0.5); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--gap-thr", type=float, default=0.07); ap.add_argument("--json")
    a = ap.parse_args()
    video = os.path.abspath(a.video)
    res = [measure(video, float(c), a.window, a.fps, a.gap_thr) for c in a.cuts.split(",") if c.strip()]
    print(os.path.basename(video))
    for r in res:
        if "error" in r:
            print(f"  corte {r['cut']}: {r['error']}"); continue
        print(f"  corte {r['cut']:>6}s  dip {r['dip']:.2f} (mas oscuro en {r['t_dip']}s)  hueco max {r['gap_max_pct']:>4}% del ancho  en {r['gap_frames']} fotogramas")
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
