#!/usr/bin/env python
"""Autoexamen de un video renderizado ANTES de mostrarlo al usuario (paso 7 del flujo).

Uso:
  python self_eval.py salida.mp4 --boundaries 2.7,7.4,12.5 [--expected-duration 17.2] [--window 1.5] [--out-dir verify]
  --boundaries : tiempos (s) de cortes/transiciones en el video de salida
Hace: duracion vs esperada; negros (blackdetect) y congelados (freezedetect); LUFS/pico; deteccion de
clics de audio en cada corte; genera PNG (timeline_view) en cada corte (+-window), primeros/ultimos 2 s y 3 puntos medios.
Imprime un informe y lista las imagenes a revisar a ojo (Read). Maximo 3 pasadas de correccion: si persiste, avisa al usuario.
Lo que NO puede verificar (sincronia fina, calidad percibida) lo dice explicitamente.
"""
import argparse, os, re, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from _common import FFMPEG, probe_duration, measure_loudness, pcm_mono, run

HERE = os.path.dirname(__file__)


def click_score(x, sr, t, win=0.025, ctx=1.0):
    """razon entre el mayor salto muestra-a-muestra en +-25 ms del corte y el p99 del contexto (>= 3 y salto > 0.15 => sospechoso)"""
    d = np.abs(np.diff(x))
    c = int(t * sr)
    a, b = max(0, c - int(win * sr)), min(len(d), c + int(win * sr))
    if b <= a:
        return 0.0, 0.0
    local = d[a:b].max()
    ctxd = np.concatenate([d[max(0, c - int(ctx * sr)):a], d[b:c + int(ctx * sr)]])
    base = np.percentile(ctxd, 99) if ctxd.size else 1e-6
    return local / max(base, 1e-6), local


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--boundaries", default="")
    ap.add_argument("--expected-duration", type=float); ap.add_argument("--window", type=float, default=1.5)
    ap.add_argument("--out-dir"); ap.add_argument("--words"); ap.add_argument("--key")
    a = ap.parse_args()
    v = os.path.abspath(a.video)
    out_dir = a.out_dir or os.path.join(os.path.dirname(v), "verify")
    os.makedirs(out_dir, exist_ok=True)
    dur = probe_duration(v)
    warns, imgs = [], []
    print(f"archivo: {v}\nduracion: {dur:.2f}s" + (f" (esperada {a.expected_duration:.2f}s)" if a.expected_duration else ""))
    if a.expected_duration and abs(dur - a.expected_duration) > 0.15:
        warns.append(f"duracion {dur:.2f}s difiere de la esperada {a.expected_duration:.2f}s")
    e = run([FFMPEG, "-hide_banner", "-i", v, "-vf", "blackdetect=d=0.2:pix_th=0.10,freezedetect=n=-60dB:d=1.0", "-an", "-f", "null", "-"]).stderr
    blacks = re.findall(r"black_start:([\d.]+).*?black_end:([\d.]+)", e)
    freezes = re.findall(r"freeze_start: ([\d.]+)", e)
    for s, en in blacks:
        warns.append(f"cuadros negros {s}-{en}s")
    for s in freezes:
        warns.append(f"posible congelado desde {s}s (puede ser una toma estatica intencional)")
    I, P = measure_loudness(v)
    print(f"audio: {I} LUFS, pico {P} dBFS")
    if P is not None and P > -1.0:
        warns.append(f"pico {P} dBFS > -1.0 (riesgo de recorte)")
    if I is not None and not (-20.5 <= I <= -13.0):
        warns.append(f"volumen {I} LUFS fuera de -20..-13 (objetivo redes ~-16/-14)")
    bs = [float(x) for x in a.boundaries.split(",") if x.strip()]
    if bs:
        x = pcm_mono(v)
        for t in bs:
            r, loc = click_score(x, 16000, t)
            flag = r >= 3.0 and loc > 0.15
            print(f"  corte {t:.2f}s: salto de audio x{r:.1f} (max {loc:.2f}) {'<-- posible clic' if flag else 'ok'}")
            if flag:
                warns.append(f"posible clic de audio en {t:.2f}s")
    views = [(max(0, t - a.window), min(dur, t + a.window), f"corte_{t:.2f}") for t in bs]
    views += [(0, min(2, dur), "inicio"), (max(0, dur - 2), dur, "final")]
    views += [(max(0, dur * f - 1), min(dur, dur * f + 1), f"medio_{int(f * 100)}") for f in (0.25, 0.5, 0.75)]
    for s, en, name in views:
        o = os.path.join(out_dir, f"{os.path.splitext(os.path.basename(v))[0]}_{name}.png")
        cmd = [sys.executable, os.path.join(HERE, "timeline_view.py"), v, f"{s:.2f}", f"{en:.2f}", "-o", o, "--n-frames", "8"]
        if bs:
            cmd += ["--marks", ",".join(f"{t:.2f}" for t in bs)]
        if a.words:
            cmd += ["--words", a.words] + (["--key", a.key] if a.key else [])
        subprocess.run(cmd, capture_output=True, text=True)
        imgs.append(o)
    print("\nRESULTADO:", "PASS (revisa las imagenes)" if not warns else "REVISAR")
    for w in warns:
        print("  -", w)
    print("\nImagenes a revisar a ojo (discontinuidad visual, subtitulos tapados, overlay desalineado, consistencia de color):")
    for i in imgs:
        print("  ", i)
    print("\nNo verificable con este script: sincronia fina palabra-voz, movimiento, calidad percibida -> dilo al usuario.")


if __name__ == "__main__":
    main()
