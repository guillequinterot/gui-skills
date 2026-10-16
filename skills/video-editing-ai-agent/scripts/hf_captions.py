#!/usr/bin/env python
"""Subtitulos por grupos de palabras para una composicion HyperFrames, a partir de words.json (transcribe_words.py).

Aplica las reglas de calidad de references/captions-subtitles.md (adaptadas de HyperFrames, Apache-2.0):
  - grupos de 2-5 palabras, cortando en clausulas (puntuacion) y en pausas;
  - cada rotulo >= 0.5 s en pantalla (si no cabe, se une al siguiente);
  - tiempos = los de las palabras (dentro de +-80 ms de la transcripcion), cuantizados a 1/fps;
  - nunca se solapan dos rotulos.
El copy oficial manda sobre la transcripcion: corrige el TEXTO de las palabras en words.json (no sus tiempos) antes de generar.

Uso:
  python hf_captions.py words.json [--key clip.mp4] [--offset 0.0] [--fps 30] [--max-words 5] [--min-words 2]
                        [--min-dur 0.5] [--gap 0.35] [--max-dur 2.6] [-o captions]
Salida (prefijo -o, por defecto ./captions):
  captions.json            grupos {id, start, end, text, words:[{w,s,e}]}
  captions-snippet.html    <div> de los rotulos + codigo GSAP (fromTo, 'cortar' al final) para pegar en index.html
No renderiza nada. Verifica con `npx hyperframes check` y mirando fotogramas (references/engine-hyperframes.md).
"""
import argparse, html, json, os, sys

PUNCT = ".,;:!?…"


def group_words(words, fps=30, max_words=5, min_words=2, min_dur=0.5, gap=0.35, max_dur=2.6):
    q = lambda t: round(round(t * fps) / fps, 4)
    # 1) clausulas: se corta tras puntuacion o en una pausa >= gap
    clauses, cur = [], []
    for w in words:
        if cur and (w["s"] - cur[-1]["e"] >= gap or cur[-1]["w"].rstrip()[-1:] in PUNCT):
            clauses.append(cur)
            cur = []
        cur.append(w)
    if cur:
        clauses.append(cur)

    # 2) cada clausula se reparte en grupos EQUILIBRADOS de <= max_words (6 -> 3+3, 8 -> 4+4): sin palabras huerfanas
    groups = []
    for cl in clauses:
        k = -(-len(cl) // max_words)            # ceil
        # una clausula larga en el tiempo tambien se parte
        while k < len(cl) and (cl[-1]["e"] - cl[0]["s"]) / k > max_dur:
            k += 1
        base, extra = divmod(len(cl), k)
        i = 0
        for j in range(k):
            n = base + (1 if j < extra else 0)
            groups.append(cl[i:i + n])
            i += n

    # une los grupos demasiado cortos (< min_words palabras o < min_dur s) con un vecino, SIN pasar de max_words
    def span(g):
        return g[-1]["e"] - g[0]["s"]

    def too_short(g):
        return len(g) < min_words or span(g) < min_dur

    changed = True
    while changed:
        changed = False
        for i, g in enumerate(groups):
            if not too_short(g):
                continue
            nxt = groups[i + 1] if i + 1 < len(groups) else None
            prv = groups[i - 1] if i > 0 else None
            can_next = nxt is not None and len(g) + len(nxt) <= max_words and nxt[0]["s"] - g[-1]["e"] < gap * 2
            can_prev = prv is not None and len(prv) + len(g) <= max_words and g[0]["s"] - prv[-1]["e"] < gap * 2
            if can_next and (not can_prev or (nxt[0]["s"] - g[-1]["e"]) <= (g[0]["s"] - prv[-1]["e"])):
                groups[i] = g + nxt
                del groups[i + 1]
                changed = True
                break
            if can_prev:
                groups[i - 1] = prv + g
                del groups[i]
                changed = True
                break

    out = []
    for i, g in enumerate(groups):
        start = q(g[0]["s"])
        nxt_start = q(groups[i + 1][0]["s"]) if i + 1 < len(groups) else None
        end = max(q(g[-1]["e"]), q(start + min_dur))
        if nxt_start is not None:
            end = min(end, q(nxt_start - 1 / fps))      # nunca solapar con el siguiente
            end = max(end, start + 1 / fps)
        out.append({"id": f"cap{i + 1:02d}", "start": start, "end": q(end),
                    "text": " ".join(w["w"].strip() for w in g), "words": [{"w": w["w"], "s": w["s"], "e": w["e"]} for w in g]})
    return out


def snippet(groups, fade=0.08):
    els = "\n".join(f'  <div id="{g["id"]}" class="cap">{html.escape(g["text"])}</div>' for g in groups)
    js = ["// subtitulos: cada rotulo aparece en su start y se CORTA en su end (opacidad + visibility en elementos NO clip)"]
    for g in groups:
        js.append(f'tl.fromTo("#{g["id"]}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: {fade}, ease: "power3.out" }}, {g["start"]});')
        js.append(f'tl.set("#{g["id"]}", {{ opacity: 0, visibility: "hidden" }}, {g["end"]});')
    css = ("/* estilo minimo; el diseno real viene de direct-visual-design / la marca. Zona segura Reels: y entre ~250 y ~1500 de 1920 */\n"
           ".cap { position: absolute; left: 60px; right: 60px; bottom: 420px; text-align: center; opacity: 0; visibility: visible;\n"
           "       font: 800 64px/1.15 Inter, Arial, sans-serif; color: #fff; text-shadow: 0 3px 12px rgba(0,0,0,.55); }")
    return f"<!-- pegar dentro de #root, SIN class=\"clip\" y con ids unicos -->\n{els}\n\n<style>\n{css}\n</style>\n\n<script>\n" + "\n".join(js) + "\n</script>\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words"); ap.add_argument("--key"); ap.add_argument("--offset", type=float, default=0.0)
    ap.add_argument("--fps", type=int, default=30); ap.add_argument("--max-words", type=int, default=5)
    ap.add_argument("--min-words", type=int, default=2); ap.add_argument("--min-dur", type=float, default=0.5)
    ap.add_argument("--gap", type=float, default=0.35); ap.add_argument("--max-dur", type=float, default=2.6)
    ap.add_argument("-o", "--output", default="captions")
    a = ap.parse_args()
    data = json.load(open(a.words, encoding="utf-8"))
    words = data.get(a.key) if a.key else next(iter(data.values()))
    if not words:
        sys.exit("words.json sin palabras para esa clave")
    words = [{"w": w["w"], "s": w["s"] + a.offset, "e": w["e"] + a.offset} for w in words]
    groups = group_words(words, a.fps, a.max_words, a.min_words, a.min_dur, a.gap, a.max_dur)
    json.dump(groups, open(a.output + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(a.output + "-snippet.html", "w", encoding="utf-8").write(snippet(groups))
    sizes = [len(g["words"]) for g in groups]
    short = [g["id"] for g in groups if g["end"] - g["start"] < a.min_dur - 1e-6]
    print(f"{len(words)} palabras -> {len(groups)} rotulos ({min(sizes)}-{max(sizes)} palabras; media {sum(sizes) / len(sizes):.1f})")
    if short:
        print("AVISO: rotulos < min-dur (suelen ser el ultimo o los pegados a otro):", ", ".join(short))
    print("escrito:", a.output + ".json", "y", a.output + "-snippet.html")


if __name__ == "__main__":
    main()
