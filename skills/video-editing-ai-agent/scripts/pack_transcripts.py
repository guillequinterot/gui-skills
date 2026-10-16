#!/usr/bin/env python
"""Empaqueta transcripciones por palabra en frases legibles (takes_packed.md).

Entrada: JSON de transcribe_words.py {"clip.mp4": [{"s":0.0,"e":0.4,"w":"Good"}, ...], ...}
Salida:  markdown con una linea por frase: [inicio-fin] texto  (rompe en huecos >= --silence o en . ? !)
Es la vista de lectura principal para elegir cortes: precision de palabra con ~1/10 de tokens.
Idea adaptada de browser-use/video-use (MIT).
Uso: python pack_transcripts.py words.json [-o takes_packed.md] [--silence 0.5]
"""
import argparse, json, sys


def phrases(words, thr):
    out, cur = [], []
    for i, w in enumerate(words):
        if cur and w["s"] - cur[-1]["e"] >= thr:
            out.append(cur); cur = []
        cur.append(w)
        if w["w"].rstrip()[-1:] in ".?!":
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words")
    ap.add_argument("-o", "--output", default="takes_packed.md")
    ap.add_argument("--silence", type=float, default=0.5)
    a = ap.parse_args()
    data = json.load(open(a.words, encoding="utf-8"))
    L = ["# Packed transcripts", "", f"Frases: huecos >= {a.silence}s o puntuacion final. Usa [inicio-fin] para direccionar cortes (las palabras de Whisper pueden desviarse 50-100 ms: rellena con padding 30-200 ms).", ""]
    total = 0
    for name, words in data.items():
        ph = phrases(words, a.silence)
        total += len(ph)
        dur = words[-1]["e"] - words[0]["s"] if words else 0
        L.append(f"## {name}  (duracion habla: {dur:.1f}s, {len(ph)} frases)")
        for p in ph:
            L.append(f"  [{p[0]['s']:06.2f}-{p[-1]['e']:06.2f}] " + " ".join(x["w"] for x in p))
        L.append("")
    open(a.output, "w", encoding="utf-8").write("\n".join(L))
    print(f"{len(data)} clips, {total} frases -> {a.output}")


if __name__ == "__main__":
    main()
