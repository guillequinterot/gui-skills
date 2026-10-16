#!/usr/bin/env python
"""Rejilla de compas de una musica: periodo T y fase t0 ajustados a los golpes REALES (bombo / graves).

Por que existe (fallo real, 2026-10-16, Reel caso-reel-01): una autocorrelacion sencilla da 123 BPM con resolucion gruesa
(un lag entero = 23 ms) y la rejilla se desplaza ~0.2 s tras 60 tiempos: los cortes caen antes que la musica. El ajuste fino
(T en pasos de 0.1 ms + fase) dio 122.0 BPM. `hyperframes beats` tambien dio ~122 BPM pero con ~45 ms de latencia fija y
la lista empezando en el tiempo 1 (usalo como contraste, no como verdad).

Uso:
  python beat_grid.py musica.mp3 [--start 0] [--end 31] [--bpm-min 80] [--bpm-max 170] [--n 64] [-o grid.json]
Salida: T, BPM, t0, puntaje por golpe (confianza) y la tabla n -> segundos. Mide solo el compas, no oye la musica:
confirma a oido (o con un golpe visual en un tiempo fuerte) antes de dar la sincronia por buena.
En video, anticipar el efecto visual ~0.1 s se siente "en sincronia" (motion-doctrine.md §10).
"""
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import pcm_mono  # noqa: E402

SR = 22050
HOP = 128
NFFT = 1024
# El pico del flujo espectral cae ANTES del golpe (la ventana de 46 ms ya lo "ve" venir): medido con un bombo sintetico de
# fase conocida = -40 ms (y `hyperframes beats` muestra el mismo orden de magnitud de latencia, al reves). Se suma a t0.
ONSET_LAG = 0.040


def onset_curve(x):
    """Flujo espectral de la banda grave (bombo). Cada valor va etiquetado en el CENTRO de la ventana."""
    win = np.hanning(NFFT)
    fr = np.lib.stride_tricks.sliding_window_view(x, NFFT)[::HOP]
    low = np.abs(np.fft.rfft(fr * win, axis=1))[:, 1:40].sum(1)
    flux = np.maximum(np.diff(low), 0)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fps = SR / HOP
    times = (np.arange(1, len(low)) * HOP + NFFT / 2) / SR
    return flux, times, fps


def _score(flux, fps, T, t0, tmax):
    k = np.arange(0, int(max(0, (tmax - t0)) / T))
    idx = np.round((t0 + k * T) * fps).astype(int)
    idx = idx[(idx > 1) & (idx < len(flux) - 2)]
    if len(idx) == 0:
        return 0.0, 0
    # tolera +-1 trama (5.8 ms): maximo local
    s = np.maximum.reduce([flux[idx - 1], flux[idx], flux[idx + 1]])
    return float(s.sum()), len(idx)


def fit(x, bpm_min=80, bpm_max=170):
    flux, times, fps = onset_curve(x)
    tmax = len(x) / SR
    Tlo, Thi = 60 / bpm_max, 60 / bpm_min
    # grueso -> fino (pasos de 0.5 ms y 10 ms, luego 0.1 ms y 2 ms)
    best = (-1, 0, 0, 0)
    for T in np.arange(Tlo, Thi, 0.0005):
        for t0 in np.arange(0, T, 0.010):
            s, k = _score(flux, fps, T, t0, tmax)
            if s > best[0]:
                best = (s, T, t0, k)
    _, T0, t00, _ = best
    for T in np.arange(T0 - 0.0008, T0 + 0.0008, 0.0001):
        for t0 in np.arange(max(0, t00 - 0.012), t00 + 0.012, 0.002):
            s, k = _score(flux, fps, T, t0, tmax)
            if s > best[0]:
                best = (s, T, t0, k)
    s, T, t0, k = best
    # sesgo de octava: si la mitad del periodo puntua casi igual por golpe, el pulso real es el mas rapido (solo se avisa)
    s2, k2 = _score(flux, fps, T / 2, t0, tmax)
    return {"T": float(T), "bpm": 60 / float(T), "t0": float(t0) + ONSET_LAG, "score_per_beat": s / max(k, 1),
            "beats_used": int(k), "half_period_score_per_beat": s2 / max(k2, 1)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None, help="analizar solo hasta aqui (s); por defecto todo")
    ap.add_argument("--bpm-min", type=float, default=80)
    ap.add_argument("--bpm-max", type=float, default=170)
    ap.add_argument("--n", type=int, default=64, help="cuantos tiempos listar")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    dur = None if a.end is None else max(0.5, a.end - a.start)
    x = pcm_mono(a.audio, ss=a.start if a.start else None, t=dur, sr=SR).astype(np.float32)
    if len(x) < SR * 4:
        print("Audio demasiado corto para ajustar un compas (< 4 s).")
        sys.exit(2)
    r = fit(x, a.bpm_min, a.bpm_max)
    r["t0"] += a.start
    r["grid"] = [round(r["t0"] + r["T"] * n, 4) for n in range(a.n)]
    r["notes"] = []
    if r["score_per_beat"] < 0.8:
        r["notes"].append("confianza baja: pocos golpes graves claros; no sincronices cortes finos sin confirmar a oido")
    if r["half_period_score_per_beat"] > 0.85 * r["score_per_beat"]:
        r["notes"].append("el medio periodo puntua casi igual: el pulso podria ser el doble de rapido (o la pista tiene contratiempos)")
    print(f"T = {r['T']:.4f} s  ->  {r['bpm']:.2f} BPM   t0 = {r['t0']:.3f} s   golpes usados: {r['beats_used']}   puntaje/golpe: {r['score_per_beat']:.2f}")
    for n_ in r["notes"]:
        print("  AVISO:", n_)
    print("n -> segundos (cada 4 = un compas):", ", ".join(f"{n}:{t:.2f}" for n, t in list(enumerate(r["grid"]))[:: 4][:16]), "...")
    if a.out:
        json.dump(r, open(a.out, "w", encoding="utf-8"), indent=1)
        print("guardado", a.out)


if __name__ == "__main__":
    main()
