#!/usr/bin/env python
"""export_pdf.py — HTML (una lámina por archivo) -> PDF vectorial con texto vivo, a tamaño exacto en puntos.

  python -I export_pdf.py --root <carpeta del proyecto> [--pages "paginas/p*.html"] [--out export/pdf] [--size 1920x1080] [--combine]

Salida: <out>/<nombre>.pdf (una página del tamaño --size en pt; 1 px = 1 pt en Illustrator) e <out>/_informe.txt
(tamaño de página, fuentes incrustadas, imágenes raster). Con --combine, además <out>/_combinado.pdf.

Truco de escala: Chromium convierte 1 px = 0,75 pt. Se imprime una página de (W/0,75) x (H/0,75) px con scale = 4/3, de modo
que el maquetado sigue siendo de W x H px y el PDF sale a W x H pt sin reescalar (el texto sigue siendo texto).

OJO: estos PDF son un INTERMEDIO. Al abrirlos en Illustrator cada letra es un texto suelto. Hay que pasarlos por
ai_pipeline.ps1 (ver references/01 y 02).
Requiere: playwright (chromium) y PyMuPDF (fitz). Poppins u otra fuente web: el HTML debe poder cargarla (internet o @font-face local).
"""
import argparse
import pathlib
import sys

import fitz
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--pages", default="paginas/p[0-9][0-9]-*.html")
    ap.add_argument("--out", default="export/pdf")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--combine", action="store_true")
    ap.add_argument("files", nargs="*", help="archivos concretos (opcional; sustituye a --pages)")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    out = root / a.out
    out.mkdir(parents=True, exist_ok=True)
    W, H = (int(v) for v in a.size.lower().split("x"))
    files = [pathlib.Path(f).resolve() for f in a.files] if a.files else sorted(root.glob(a.pages))
    if not files:
        sys.exit("No hay HTML que exportar: revisa --root / --pages")
    pdfs = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        for f in files:
            pg.goto(f.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            dst = out / (f.stem + ".pdf")
            pg.pdf(
                path=str(dst),
                width=f"{round(W / 0.75)}px",
                height=f"{round(H / 0.75)}px",
                scale=4 / 3,
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                page_ranges="1",
            )
            pdfs.append(dst)
        br.close()
    informe = []
    for p in pdfs:
        d = fitz.open(p)
        pg0 = d[0]
        fonts = sorted({fo[3].split("+")[-1] for fo in pg0.get_fonts()})
        informe.append(f"{p.name}: {len(d)} pág · {pg0.rect.width:.0f} x {pg0.rect.height:.0f} pt · fuentes {fonts} · raster {len(pg0.get_images())}")
        d.close()
    if a.combine:
        comb = fitz.open()
        for p in pdfs:
            d = fitz.open(p)
            comb.insert_pdf(d)
            d.close()
        comb.save(out / "_combinado.pdf", garbage=3, deflate=True)
        informe.append(f"_combinado.pdf: {len(comb)} páginas")
        comb.close()
    (out / "_informe.txt").write_text("\n".join(informe), encoding="utf-8")
    print("\n".join(informe))


if __name__ == "__main__":
    main()
