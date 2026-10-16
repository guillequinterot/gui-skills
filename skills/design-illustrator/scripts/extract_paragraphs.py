#!/usr/bin/env python
"""extract_paragraphs.py — saca del DOM de cada HTML los bloques de texto de varias líneas.

  python -I extract_paragraphs.py --root <carpeta del proyecto> [--pages "paginas/p*.html"] [--out export/dom] [--size 1920x1080]

Salida: <out>/<nombre>.json con la lista de bloques. Los usa ai_pipeline.ps1 para reconstruir cada párrafo como UN texto de
área (texto corrido) en Illustrator, con el mismo ancho de columna y el mismo ajuste de líneas que el navegador.

Un «bloque» es un elemento de bloque (no inline) cuyos hijos son solo texto y <br>. Se parte en «tramos» en cada <br>
(salto forzado); cada tramo se divide en líneas según el maquetado real. Se guarda: x y ancho de la caja de contenido,
alineación, tamaño, interletraje (px), interlineado (px) y, por línea, el texto y su caja vertical (top/bottom).

Límite: bloques con <span>/<b>/<a> en medio (texto con estilos mezclados) NO se detectan; se quedan como líneas sueltas.
"""
import argparse
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

JS = r"""
() => {
  const out = [];
  for (const e of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(e);
    if (cs.display === 'inline' || cs.display === 'none' || cs.visibility === 'hidden') continue;
    const kids = Array.from(e.childNodes);
    let hasText = false, pure = true;
    for (const n of kids) {
      if (n.nodeType === 3) { if (n.textContent.trim()) hasText = true; }
      else if (n.nodeType === 1 && n.tagName === 'BR') { }
      else { pure = false; break; }
    }
    if (!hasText || !pure) continue;
    const runs = [[]];
    for (const n of kids) {
      if (n.nodeType === 1 && n.tagName === 'BR') runs.push([]);
      else if (n.nodeType === 3 && n.textContent.trim()) runs[runs.length - 1].push(n);
    }
    const runLines = [];
    for (const nodes of runs) {
      if (!nodes.length) continue;
      const lines = [];
      for (const tn of nodes) {
        const txt = tn.textContent;
        let cur = null;
        for (let i = 0; i < txt.length; i++) {
          const r = document.createRange();
          r.setStart(tn, i); r.setEnd(tn, i + 1);
          const rects = r.getClientRects();
          if (!rects.length) { if (cur) cur.t += txt[i]; continue; }
          const rc = rects[0];
          if (rc.width === 0 && txt[i] !== ' ' && txt[i] !== ' ') continue;
          if (!cur || Math.abs(rc.top - cur.top) > 3) { cur = { t: '', top: rc.top, bottom: rc.bottom }; lines.push(cur); }
          cur.t += txt[i];
        }
      }
      for (const l of lines) l.t = l.t.replace(/\s+/g, ' ').trim();
      const l2 = lines.filter(l => l.t.length);
      if (l2.length) runLines.push(l2);
    }
    const total = runLines.reduce((s, r) => s + r.length, 0);
    if (total < 2) continue;
    const rect = e.getBoundingClientRect();
    const px = v => parseFloat(v) || 0;
    out.push({
      tag: e.tagName.toLowerCase(),
      x: rect.left + px(cs.borderLeftWidth) + px(cs.paddingLeft),
      w: rect.width - px(cs.borderLeftWidth) - px(cs.borderRightWidth) - px(cs.paddingLeft) - px(cs.paddingRight),
      align: cs.textAlign,
      size: px(cs.fontSize),
      ls: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
      lh: cs.lineHeight === 'normal' ? px(cs.fontSize) * 1.5 : px(cs.lineHeight),
      runs: runLines
    });
  }
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--pages", default="paginas/p[0-9][0-9]-*.html")
    ap.add_argument("--out", default="export/dom")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    out = root / a.out
    out.mkdir(parents=True, exist_ok=True)
    W, H = (int(v) for v in a.size.lower().split("x"))
    files = [pathlib.Path(f).resolve() for f in a.files] if a.files else sorted(root.glob(a.pages))
    total = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        for f in files:
            pg.goto(f.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(200)
            paras = pg.evaluate(JS)
            (out / (f.stem + ".json")).write_text(json.dumps(paras, ensure_ascii=False), encoding="utf-8")
            total += len(paras)
            print(f"{f.stem}: {len(paras)} bloques")
        br.close()
    print("total bloques:", total)


if __name__ == "__main__":
    main()
