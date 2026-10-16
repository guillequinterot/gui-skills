#!/usr/bin/env python
"""Normaliza el volumen del AUDIO de un MP4 (dos pasadas loudnorm) sin tocar el video (-c:v copy).

Uso:
  python loudnorm_audio.py entrada.mp4 [-o salida.mp4] [--target -16] [--tp -1.5] [--lra 11] [--social] [--overwrite]
  --social  => -14 LUFS / TP -1.0 (objetivo de YouTube/Instagram/TikTok segun video-use)
Por defecto escribe <entrada>_norm.mp4 (nunca sobrescribe sin --overwrite). Reporta antes/despues.
Patron adaptado de browser-use/video-use (MIT): medir en pasada 1, aplicar con linear=true en pasada 2.
Nota: loudnorm sube la ganancia hasta el objetivo y limita el pico; si el material es muy dinamico puede
caer a modo dinamico. Verifica siempre el resultado (se imprime).
"""
import argparse, json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(__file__))
from _common import FFMPEG, measure_loudness, run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    ap.add_argument("--target", type=float, default=-16.0)
    ap.add_argument("--tp", type=float, default=-1.5)
    ap.add_argument("--lra", type=float, default=11.0)
    ap.add_argument("--social", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    a = ap.parse_args()
    if a.social:
        a.target, a.tp = -14.0, -1.0
    out = a.output or os.path.splitext(a.input)[0] + "_norm.mp4"
    if os.path.exists(out) and not a.overwrite:
        sys.exit(f"ya existe {out} (usa --overwrite o -o otro_nombre)")
    i0, p0 = measure_loudness(a.input)
    print(f"antes:  {i0} LUFS, pico {p0} dBFS")
    r = run([FFMPEG, "-y", "-hide_banner", "-nostats", "-i", a.input, "-vn", "-af", f"loudnorm=I={a.target}:TP={a.tp}:LRA={a.lra}:print_format=json", "-f", "null", "-"])
    s, e = r.stderr.rfind("{"), r.stderr.rfind("}")
    try:
        m = json.loads(r.stderr[s:e + 1])
        filt = (f"loudnorm=I={a.target}:TP={a.tp}:LRA={a.lra}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
                f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    except Exception:
        print("medicion fallida: uso una sola pasada")
        filt = f"loudnorm=I={a.target}:TP={a.tp}:LRA={a.lra}"
    sub = subprocess.run([FFMPEG, "-y", "-hide_banner", "-nostats", "-i", a.input, "-c:v", "copy", "-af", filt, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out],
                         capture_output=True, text=True)
    if sub.returncode != 0:
        sys.exit(sub.stderr[-800:])
    i1, p1 = measure_loudness(out)
    print(f"despues: {i1} LUFS, pico {p1} dBFS  -> {out}")
    if i1 is not None and abs(i1 - a.target) > 1.5:
        print("AVISO: el resultado se aleja >1.5 LU del objetivo (material muy dinamico o limitado por el pico).")


if __name__ == "__main__":
    main()
