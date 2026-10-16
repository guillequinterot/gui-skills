#!/usr/bin/env python
"""Carve de musica bajo una voz: baja SOLO la banda donde habla la voz y deja intactos graves y agudos.

Por que: bajar todo el volumen de la musica mientras habla la voz (un "duck") deja la musica sin presencia todo el rato.
La voz solo necesita unas bandas (aprox. 250 Hz - 2.5 kHz); el "carve" las libera y la musica sigue sonando como musica.
Idea tomada del skill hyperframes-audio de HeyGen (Apache-2.0; NOTICE.md); implementacion propia con ffmpeg.

Cadena: musica -> acrossover (graves | medios | agudos) ; solo los MEDIOS pasan por sidechaincompress con la VOZ como
control (ataque rapido, liberacion LENTA para que la musica no "salte" de golpe al terminar cada palabra) ; se suman
las tres bandas ; se iguala el nivel de la musica respecto a la voz ; se mezcla con la voz.

Uso:
  python carve_music.py --voice voz.wav --bed musica.mp3 -o mezcla.wav [--strength 0.8] [--bed-offset-db -12]
                        [--split 250,2500] [--bed-only] [--voice-delay 0.0] [--verify]
  --strength     0..1 (0.8 por defecto): profundidad buscada en la banda de la voz (3 + 12 x strength dB; medido con voz y ruido
                 rosa sinteticos: -6.6 dB a 0.3, -9.4 dB a 0.8, -10.2 dB a 1.0; graves y agudos casi intactos)
  --bed-offset-db  nivel de la musica respecto a la voz, en LUFS integrados (por defecto -12; ver audio-mix.md)
  --bed-only     escribe solo la musica ya recortada (para colocarla tu en otro editor)
  --voice-delay  segundos de retraso de la voz respecto a la musica (si la voz no empieza en 0)
  --verify       MIDE el resultado: cambio de nivel (dB) por banda mientras habla la voz frente a la musica sin carve
Trampas conocidas: (1) sidechaincompress se cuelga si voz y musica duran distinto: aqui se igualan con apad; (2) encadenar alimiter justo despues de amix en el mismo grafo SE CUELGA en el ffmpeg de Shotcut n8.1.2; aqui el limitador va en una pasada aparte.
Reglas: la voz NUNCA se procesa contra si misma; si hay varias voces, mezclalas antes en una sola pista.
"""
import argparse, os, subprocess, sys, tempfile
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, measure_loudness, pcm_mono, probe_duration  # noqa: E402

SR = 48000


def ff(args):
    r = subprocess.run([FFMPEG, "-v", "error", "-y"] + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg fallo:\n" + r.stderr[-800:])


def speech_stats(voice):
    """Rangos de voz (VAD) y nivel RMS en dBFS SOLO dentro de la voz."""
    from vad_segments import detect
    x = pcm_mono(voice, None, None, 16000).astype(np.float32)
    segs = detect(x)
    if not segs:
        sys.exit("No se detecto voz en --voice: el carve no tiene nada que proteger. Revisa el archivo.")
    chunks = np.concatenate([x[int(s * 16000): int(e * 16000)] for s, e in segs])
    rms = float(np.sqrt(np.mean(chunks ** 2)))
    return segs, 20 * np.log10(max(rms, 1e-6))


def band_levels(path, segs, split):
    """Nivel (dB) por banda dentro de los rangos de voz, con FFT sobre el audio mono a 16 kHz."""
    x = pcm_mono(path, None, None, 16000).astype(np.float32)
    parts = [x[int(s * 16000): int(e * 16000)] for s, e in segs if int(e * 16000) <= len(x)]
    if not parts:
        return None
    y = np.concatenate(parts)
    spec = np.abs(np.fft.rfft(y * np.hanning(len(y)))) ** 2
    f = np.fft.rfftfreq(len(y), 1 / 16000)
    lo, hi = split
    out = {}
    for name, (a, b) in {"graves": (30, lo), "medios": (lo, hi), "agudos": (hi, 7800)}.items():
        m = (f >= a) & (f < b)
        out[name] = 10 * np.log10(max(float(spec[m].sum()), 1e-12))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", required=True); ap.add_argument("--bed", required=True); ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--strength", type=float, default=0.8); ap.add_argument("--bed-offset-db", type=float, default=-12.0)
    ap.add_argument("--split", default="250,2500"); ap.add_argument("--bed-only", action="store_true")
    ap.add_argument("--voice-delay", type=float, default=0.0); ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    if not 0 <= a.strength <= 1:
        sys.exit("--strength debe estar entre 0 y 1")
    for p in (a.voice, a.bed):
        if not os.path.exists(p):
            sys.exit("no existe: " + p)
    lo, hi = (float(v) for v in a.split.split(","))
    out = os.path.abspath(a.output)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    segs, lv_db = speech_stats(a.voice)
    segs = [(s + a.voice_delay, e + a.voice_delay) for s, e in segs]
    lufs_v, _ = measure_loudness(a.voice)
    lufs_b, _ = measure_loudness(a.bed)
    if lufs_v is None or lufs_b is None:
        sys.exit("no se pudo medir el volumen (LUFS) de la voz o de la musica")
    gain_db = (lufs_v + a.bed_offset_db) - lufs_b                     # iguala la musica respecto a la voz
    depth = 3.0 + 12.0 * a.strength                                    # dB de recorte buscados en la banda de la voz
    ratio = 8.0
    thr_db = lv_db - depth / (1 - 1 / ratio)                           # umbral para que la voz comprima ~depth dB
    thr = min(max(10 ** (thr_db / 20), 0.000976563), 1.0)
    delay = int(a.voice_delay * 1000)
    fmt = f"aformat=sample_rates={SR}:channel_layouts=stereo"
    # sidechaincompress SE CUELGA si la llave (voz) y la entrada (musica) tienen duraciones distintas:
    # se rellenan ambas con silencio hasta la mayor (visto con voz de 9.7 s y musica de 14 s).
    maxdur = max(probe_duration(a.voice) + a.voice_delay, probe_duration(a.bed)) + 0.05
    vchain = fmt + (f",adelay={delay}|{delay}" if delay else "") + f",apad=whole_dur={maxdur:.3f}"
    bchain = f"{fmt},apad=whole_dur={maxdur:.3f}"
    # Paso 1: musica recortada (la voz es SOLO la llave del compresor). Sin asplit: evita el bloqueo del grafo.
    graph1 = (
        f"[0:a]{vchain}[vkey];"
        f"[1:a]volume={gain_db:.2f}dB,{bchain},acrossover=split={lo:g} {hi:g}:order=4th[low][mid][high];"
        f"[mid][vkey]sidechaincompress=threshold={thr:.6f}:ratio={ratio:g}:attack=20:release=450:makeup=1[midc];"
        f"[low][midc][high]amix=inputs=3:normalize=0[final]"
    )
    tmpdir = tempfile.mkdtemp(prefix="carve_")
    bed_c = os.path.join(tmpdir, "bed_carved.wav")
    ff(["-i", a.voice, "-i", a.bed, "-filter_complex", graph1, "-map", "[final]", "-ar", str(SR), bed_c])
    # Paso 2: mezcla voz + musica recortada. NO encadenar alimiter tras amix en el mismo grafo: se CUELGA en el ffmpeg de Shotcut n8.1.2.
    if a.bed_only:
        raw = bed_c
    else:
        graph2 = f"[0:a]{vchain}[v];[1:a]{fmt}[b];[v][b]amix=inputs=2:normalize=0:duration=longest[final]"
        raw = os.path.join(tmpdir, "mix_raw.wav")
        ff(["-i", a.voice, "-i", bed_c, "-filter_complex", graph2, "-map", "[final]", "-ar", str(SR), raw])
    # Paso 3: limitador en pasada aparte (techo 0.95 = -0.4 dBFS)
    ff(["-i", raw, "-af", "alimiter=limit=0.95", "-ar", str(SR), out])
    print(f"voz {lufs_v:.1f} LUFS (nivel en habla {lv_db:.1f} dBFS) | musica {lufs_b:.1f} LUFS -> ganancia {gain_db:+.1f} dB (objetivo {a.bed_offset_db:+.0f} LU respecto a la voz)")
    print(f"carve: banda {lo:g}-{hi:g} Hz, recorte buscado ~{depth:.1f} dB (el real suele ser ~70-100 % de eso: medirlo con --verify), umbral {thr_db:.1f} dBFS, ratio {ratio:g}, ataque 20 ms, liberacion 450 ms")
    print("escrito:", out)

    if a.verify:
        # musica de referencia SIN carve (solo ganancia y mismo formato) vs musica CON carve, ambas medidas dentro de la voz
        ref = os.path.join(tmpdir, "ref.wav")
        ff(["-i", a.bed, "-af", f"volume={gain_db:.2f}dB,{bchain}", ref])
        # solo se mide donde la musica existe (si la voz dura mas, el resto no tiene nada que carvear)
        bed_dur = probe_duration(a.bed)
        vsegs = [(s0, min(e0, bed_dur)) for s0, e0 in segs if s0 < bed_dur - 0.2]
        if len(vsegs) < len(segs) or (segs and segs[-1][1] > bed_dur):
            print(f"  AVISO: la voz dura mas que la musica ({probe_duration(a.voice) + a.voice_delay:.1f} s contra {bed_dur:.1f} s): se mide solo hasta donde hay musica.")
        b0, b1 = band_levels(ref, vsegs, (lo, hi)), band_levels(bed_c, vsegs, (lo, hi))
        if b0 and b1:
            print("VERIFICACION (cambio de la musica mientras habla la voz, respecto a la misma musica sin carve):")
            for k in ("graves", "medios", "agudos"):
                print(f"  {k:<7} {b1[k] - b0[k]:+5.1f} dB")
            print("  Esperado: medios claramente negativos; graves y agudos cerca de 0. Lo que NO se mide aqui: como suena (escuchalo).")
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
