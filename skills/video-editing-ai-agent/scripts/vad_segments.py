#!/usr/bin/env python
"""Voz / pausas con Silero VAD (modelo incluido en faster-whisper; sin torch, sin descargas, 100 % local).

Para que sirve en esta skill:
  - tiempos fiables de habla y de pausas (aire muerto) para cortar por transcripcion o quitar silencios;
  - validar cruzado la transcripcion: un segmento de Whisper sin voz detectada debajo es una alucinacion probable;
  - saber si un video tiene voz o solo musica/ambiente (speech_ratio).

Uso:
  python vad_segments.py video_o_audio.mp4 [--threshold 0.5] [--min-silence 0.3] [--min-speech 0.15] [--pad 0.06]
                         [--pause-min 0.4] [-o vad.json] [--words words.json --key clip.mp4]
Salida: JSON {speech:[[s,e]], pauses:[[s,e,dur]], speech_ratio, params} + resumen en pantalla.
Valores por defecto: 0.5 (umbral de activacion, igual que LiveKit/Silero), pausas >= 0.4 s (oficio de corte de edit-craft.md).
Para CORTAR, deja 30-200 ms de margen (edit-craft.md); --pad es solo el relleno del detector.
Modelo: Silero VAD (MIT, snakers4/silero-vad) en la version que trae faster-whisper (assets/silero_vad_v6.onnx).
"""
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import pcm_mono  # noqa: E402

SR = 16000


def detect(x, threshold=0.5, min_silence=0.3, min_speech=0.15, pad=0.06):
    """x: audio mono float32 a 16 kHz. Devuelve lista de (inicio, fin) en segundos."""
    from faster_whisper.vad import get_speech_timestamps, VadOptions
    opts = VadOptions(threshold=threshold, min_speech_duration_ms=int(min_speech * 1000),
                      min_silence_duration_ms=int(min_silence * 1000), speech_pad_ms=int(pad * 1000))
    return [(c["start"] / SR, c["end"] / SR) for c in get_speech_timestamps(x.astype(np.float32), opts)]


def pauses_from(speech, dur, pause_min=0.4):
    """Huecos entre tramos de voz (incluye el inicio y el final) de al menos pause_min segundos."""
    edges = [(0.0, 0.0)] + list(speech) + [(dur, dur)]
    out = []
    for (_, e0), (s1, _) in zip(edges[:-1], edges[1:]):
        if s1 - e0 >= pause_min:
            out.append((round(e0, 2), round(s1, 2), round(s1 - e0, 2)))
    return out


def analyze(path, threshold=0.5, min_silence=0.3, min_speech=0.15, pad=0.06, pause_min=0.4):
    x = pcm_mono(path, None, None, SR)
    dur = x.size / SR
    speech = detect(x, threshold, min_silence, min_speech, pad)
    total = sum(e - s for s, e in speech)
    return {"duration": round(dur, 2),
            "speech": [(round(s, 2), round(e, 2)) for s, e in speech],
            "pauses": pauses_from(speech, dur, pause_min),
            "speech_seconds": round(total, 2), "speech_ratio": round(total / dur, 3) if dur else 0.0,
            "params": {"threshold": threshold, "min_silence": min_silence, "min_speech": min_speech, "pad": pad, "pause_min": pause_min}}


def overlap_ratio(speech, a, b):
    """Fraccion de [a,b] que cae dentro de voz detectada (0..1)."""
    if b <= a:
        return 0.0
    got = sum(max(0.0, min(e, b) - max(s, a)) for s, e in speech)
    return min(1.0, got / (b - a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media"); ap.add_argument("-o", "--output")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--min-silence", type=float, default=0.3)
    ap.add_argument("--min-speech", type=float, default=0.15)
    ap.add_argument("--pad", type=float, default=0.06)
    ap.add_argument("--pause-min", type=float, default=0.4)
    ap.add_argument("--words", help="JSON de transcribe_words.py: marca palabras fuera de voz detectada")
    ap.add_argument("--key", help="clave del clip dentro de --words")
    a = ap.parse_args()
    media = os.path.abspath(a.media)
    if not os.path.exists(media):
        sys.exit("no existe: " + media)
    r = analyze(media, a.threshold, a.min_silence, a.min_speech, a.pad, a.pause_min)
    print(f"{os.path.basename(media)}: {r['duration']}s, voz {r['speech_seconds']}s ({r['speech_ratio'] * 100:.0f}%), "
          f"{len(r['speech'])} tramos, {len(r['pauses'])} pausas >= {a.pause_min}s")
    for s, e, d in r["pauses"]:
        print(f"  pausa {s:7.2f} -> {e:7.2f}  ({d:.2f}s)")
    if r["speech_ratio"] < 0.1:
        print("  AVISO: casi sin voz; es musica/ambiente. Cualquier texto de Whisper en este audio es sospechoso.")
    if a.words:
        data = json.load(open(a.words, encoding="utf-8"))
        words = data.get(a.key) if a.key else next(iter(data.values()))
        bad = [w for w in words if overlap_ratio(r["speech"], w["s"], w["e"]) < 0.3]
        r["words_outside_speech"] = bad
        print(f"  palabras de Whisper sin voz debajo: {len(bad)} de {len(words)}" + (" -> " + " ".join(w["w"] for w in bad[:15]) if bad else ""))
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
        print("guardado:", a.output)


if __name__ == "__main__":
    main()
