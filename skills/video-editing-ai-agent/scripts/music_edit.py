#!/usr/bin/env python
"""Mapa de una canción por compases y edición de la música CORTANDO EN COMPASES (la rejilla sigue pareja a través de cada empalme).

Por qué: elegir las secciones por dato (¿en qué compás entran los graves? ¿dónde está el silencio? ¿dónde cae el golpe fuerte?) y no «a oído»,
y acortar una canción sin que el compás se desplace, para que cortes de imagen, golpes y cierre caigan en tiempos fuertes. Idea del flujo
de `product-film` (Rieranthony, MIT: mapa por compás + `audio-edit` con segmentos) y de `cinetic` (Leonxlnx, MIT: la pista se corta en
compases y termina con su propio final), reimplementada aquí. La rejilla (BPM y primer tiempo fuerte) NO se calcula en este script: sale de
`beat_grid.py`, y se confirma a oído antes de dar la sincronía por buena.

  map : python music_edit.py map musica.mp3 --bpm 122 --first-downbeat 1.25 [--beats-per-bar 4] [--bars 40]
        -> tabla compás | inicio | nivel total | graves (<160 Hz) | agudos (>3 kHz) con una barra de texto. Léela para mapear la historia:
        el saludo en un compás escaso, los clics en un compás en silencio, lo apretado donde entra el groove, el cierre donde caen los graves.
  cut : python music_edit.py cut edit.json
        edit.json = {"source": "musica.mp3", "out": "musica-edit.wav", "bpm": 122.0, "firstDownbeat": 1.25, "beatsPerBar": 4,
                     "segments": [{"fromBar": 1, "toBar": 17, "why": "intro y groove"}, {"fromBar": 36, "toBar": 40, "why": "final"}],
                     "joinFadeMs": 5, "fadeOutSeconds": 1.2}
        `toBar` es EXCLUSIVO y los compases se cuentan desde 1 en el primer tiempo fuerte. Las secciones quedan pegadas: el compás k de la
        salida empieza en (k-1)*duración_del_compás. Cada empalme lleva un fundido corto (por defecto 5 ms, sin clic) y el final un fundido largo.
        La duración de la pieza de video debe ser un número ENTERO de compases de la salida (se imprime).
Mide y corta; no oye. Si el empalme suena mal (cambio de acorde, nota cortada), cambia de compás: no hay arreglo automático.
"""
import argparse, json, os, subprocess, sys, wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG  # noqa: E402

SR = 44100


def decode(path, ch=2):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-vn", "-ac", str(ch), "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, timeout=600).stdout
    n = len(raw) // (2 * ch)
    return np.frombuffer(raw[: n * 2 * ch], dtype="<i2").reshape(n, ch).astype(np.float32) / 32768.0


def db(x):
    return 20 * np.log10(max(float(x), 1e-6))


def bar_len(bpm, bpb):
    return 60.0 / bpm * bpb


def cmd_map(a):
    x = decode(a.audio, 1)[:, 0]
    bl = bar_len(a.bpm, a.beats_per_bar)
    nbars = int((len(x) / SR - a.first_downbeat) // bl)
    if a.bars:
        nbars = min(nbars, a.bars)
    rows = []
    for k in range(nbars):
        s = int(round((a.first_downbeat + k * bl) * SR))
        seg = x[s: s + int(round(bl * SR))]
        if len(seg) < SR // 4:
            break
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        f = np.fft.rfftfreq(len(seg), 1 / SR)
        tot = np.sqrt(np.mean(seg ** 2))
        lo = np.sqrt(spec[f < 160].sum() / spec.sum() + 1e-12) * tot
        hi = np.sqrt(spec[f > 3000].sum() / spec.sum() + 1e-12) * tot
        rows.append((k + 1, a.first_downbeat + k * bl, db(tot), db(lo), db(hi)))
    print(f"# music_edit map - {os.path.basename(a.audio)}: {a.bpm} BPM, primer tiempo fuerte {a.first_downbeat} s, {a.beats_per_bar} tiempos por compás "
          f"({bl:.3f} s), {len(rows)} compases")
    print("compás | inicio s | total dB | graves dB | agudos dB | nivel total")
    for k, t, tt, lo, hi in rows:
        n = int(max(0, min(40, (tt + 60) * 40 / 60)))
        print(f"{k:6d} | {t:8.2f} | {tt:8.1f} | {lo:9.1f} | {hi:9.1f} | " + "#" * n)
    if rows:
        quiet = [r[0] for r in rows if r[2] < max(x[2] for x in rows) - 18]
        print(f"compases al menos 18 dB bajo el más fuerte: {quiet[:20]}{'...' if len(quiet) > 20 else ''}")
    print("Esto mide energía por compás; para decir dónde está la sección 'del drop' mira cuándo suben los graves y cuándo cae un compás casi en silencio.")


def cmd_cut(a):
    spec = json.load(open(a.edit, encoding="utf-8"))
    bpb = int(spec.get("beatsPerBar", 4))
    bl = bar_len(float(spec["bpm"]), bpb)
    t0 = float(spec["firstDownbeat"])
    fade_j = int(round(float(spec.get("joinFadeMs", 5)) / 1000 * SR))
    x = decode(spec["source"], 2)
    parts, info = [], []
    for i, sg in enumerate(spec["segments"]):
        fb, tb = int(sg["fromBar"]), int(sg["toBar"])
        if tb <= fb or fb < 1:
            raise SystemExit(f"segmento {i + 1}: toBar debe ser mayor que fromBar y fromBar >= 1")
        s = int(round((t0 + (fb - 1) * bl) * SR))
        e = int(round((t0 + (tb - 1) * bl) * SR))
        if e > len(x):
            raise SystemExit(f"segmento {i + 1}: el compás {tb} pasa del final de la canción ({len(x) / SR:.1f} s)")
        seg = x[s:e].copy()
        if len(seg) > 2 * fade_j and fade_j > 0:
            ramp = np.linspace(0, 1, fade_j, dtype=np.float32)[:, None]
            if i > 0:
                seg[:fade_j] *= ramp
            if i < len(spec["segments"]) - 1:
                seg[-fade_j:] *= ramp[::-1]
        parts.append(seg)
        info.append((fb, tb, tb - fb, sg.get("why", "")))
    out = np.concatenate(parts)
    fo = float(spec.get("fadeOutSeconds", 0))
    if fo > 0:
        n = min(len(out), int(round(fo * SR)))
        out[-n:] *= np.linspace(1, 0, n, dtype=np.float32)[:, None]
    pcm = np.clip(out * 32767, -32768, 32767).astype("<i2")
    with wave.open(spec["out"], "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    nb = sum(x[2] for x in info)
    print(f"# music_edit cut -> {spec['out']}: {len(out) / SR:.3f} s = {nb} compases de {bl:.3f} s (la salida empieza en un tiempo fuerte)")
    t = 0.0
    for fb, tb, n, why in info:
        print(f"  compás {fb}-{tb - 1} de la canción -> compases {int(round(t / bl)) + 1}-{int(round(t / bl)) + n} de la salida (desde {t:.3f} s) {why}")
        t += n * bl
    print(f"La duración de la pieza de video debe ser múltiplo de {bl:.3f} s (p. ej. {nb} compases = {nb * bl:.3f} s). Empalmes con fundido de {spec.get('joinFadeMs', 5)} ms: confirma a oído que no cortan una nota.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    m = sp.add_parser("map"); m.add_argument("audio"); m.add_argument("--bpm", type=float, required=True)
    m.add_argument("--first-downbeat", type=float, required=True); m.add_argument("--beats-per-bar", type=int, default=4); m.add_argument("--bars", type=int)
    c = sp.add_parser("cut"); c.add_argument("edit")
    a = ap.parse_args()
    (cmd_map if a.cmd == "map" else cmd_cut)(a)


if __name__ == "__main__":
    main()
