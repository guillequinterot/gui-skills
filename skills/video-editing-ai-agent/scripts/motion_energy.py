#!/usr/bin/env python
"""Energía de movimiento por segundo y tramos casi inmóviles de un video (y comparación A/B entre dos versiones).

Para qué: detectar «aire muerto» en piezas animadas (un gancho congelado, una pausa de 1 s sin señal) y medir cuánto cambia una variante frente a otra
(p. ej. con y sin empuje de cámara). Mide diferencia entre fotogramas consecutivos (0-100 niveles de gris, vista reducida): no dice si el movimiento
es BUENO, solo si lo hay. Un cierre con logo quieto es normal; una pausa en medio de la pieza, no.

Uso:
  python motion_energy.py video.mp4 [video_B.mp4] [--quiet 0.1] [--min-run 0.5] [--json salida.json]
"""
import argparse, json, os, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG  # noqa: E402

W, H = 135, 240


def frames(path):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, timeout=600).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[: n * W * H], dtype=np.uint8).reshape(n, H, W).astype(np.float32)


def fps_of(path):
    from _common import FFPROBE
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    a, _, b = r.stdout.strip().partition("/")
    try:
        return float(a) / float(b or 1)
    except ValueError:
        return 30.0


def analyse(path, quiet, min_run):
    F = frames(path)
    fps = fps_of(path)
    e = np.abs(F[1:] - F[:-1]).mean(axis=(1, 2))
    per = [float(e[int(s * fps): int((s + 1) * fps)].mean()) for s in range(int(len(e) / fps))]
    runs, start = [], None
    for i, v in enumerate(e < quiet):
        if v and start is None:
            start = i
        if not v and start is not None:
            if (i - start) / fps >= min_run:
                runs.append((round(start / fps, 2), round(i / fps, 2)))
            start = None
    if start is not None and (len(e) - start) / fps >= min_run:
        runs.append((round(start / fps, 2), round(len(e) / fps, 2)))
    return {"video": path, "fps": fps, "frames": int(len(F)), "per_second": per, "quiet_frames": int((e < quiet).sum()),
            "quiet_runs": runs, "_e": e}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("video_b", nargs="?")
    ap.add_argument("--quiet", type=float, default=0.1, help="por debajo de esto un fotograma cuenta como quieto")
    ap.add_argument("--min-run", type=float, default=0.5, help="duración mínima (s) de un tramo quieto para avisarlo")
    ap.add_argument("--json")
    a = ap.parse_args()
    A = analyse(a.video, a.quiet, a.min_run)
    B = analyse(a.video_b, a.quiet, a.min_run) if a.video_b else None
    print(f"movimiento medio por segundo (0-100 grises) — {os.path.basename(a.video)}" + (f" | {os.path.basename(a.video_b)}" if B else ""))
    for s, v in enumerate(A["per_second"]):
        row = f"{s:2d}-{s + 1:2d}s  {v:6.2f}"
        if B and s < len(B["per_second"]):
            row += f" | {B['per_second'][s]:6.2f}"
        if v < a.quiet * 1.5:
            row += "   <- casi quieto"
        print(row)
    print(f"fotogramas casi inmóviles: {A['quiet_frames']} de {A['frames'] - 1}; tramos quietos >= {a.min_run} s: {A['quiet_runs'] or 'ninguno'}")
    if B:
        n = min(len(A["_e"]), len(B["_e"]))
        d = [float(np.abs(x - y).mean()) for x, y in zip(frames(a.video)[:n], frames(a.video_b)[:n])]
        fps = A["fps"]
        print("diferencia de imagen entre A y B por segundo:", " ".join(f"{np.mean(d[int(s * fps):int((s + 1) * fps)]):.1f}" for s in range(int(n / fps))))
    if a.json:
        for X in (A, B):
            if X:
                X.pop("_e", None)
        json.dump({"A": A, "B": B}, open(a.json, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
