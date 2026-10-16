"""pdf_pages.py — renderiza páginas de PDF / .ai (PDF-compatible) con PyMuPDF y arma hojas de contacto.
Sirve para ANALIZAR la línea gráfica de una marca (manual, brochure, calendario) sin abrir Illustrator.

  python -I pdf_pages.py render <origen.pdf|.ai> <prefijo_salida> [--max 12] [--width 1400]
  python -I pdf_pages.py sheet  "<glob>_p*.png" <hoja.png> [--cols 3] [--tw 700] [--range 1-9]
  python -I pdf_pages.py vectors <origen> --page 0     # cuántos dibujos/imágenes vectoriales tiene la página

Nota: si un .ai pesa cientos de MB, igual abre (los .ai de `caso-diplomas-01` eran PDF-compatibles).
"""
import argparse, glob, re, sys


def render(a):
    import fitz
    d = fitz.open(a.src); print(a.src, "páginas:", len(d))
    for i in range(min(a.max, len(d))):
        p = d[i]; z = a.width / p.rect.width
        pix = p.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
        f = f"{a.out}_p{i+1}.png"; pix.save(f); print(f, pix.width, pix.height)


def sheet(a):
    from PIL import Image
    files = sorted(glob.glob(a.glob), key=lambda s: int(re.findall(r"_p(\d+)", s)[-1]))
    if a.range:
        x, y = map(int, a.range.split("-")); files = files[x - 1:y]
    ims = [Image.open(f).convert("RGB") for f in files]
    th = max(int(im.height * a.tw / im.width) for im in ims)
    rows = (len(ims) + a.cols - 1) // a.cols
    S = Image.new("RGB", (a.cols * a.tw, rows * th), "white")
    for i, im in enumerate(ims):
        S.paste(im.resize((a.tw, int(im.height * a.tw / im.width))), ((i % a.cols) * a.tw, (i // a.cols) * th))
    S.save(a.out); print(a.out, S.size, len(ims))


def vectors(a):
    import fitz
    p = fitz.open(a.src)[a.page]
    dr = p.get_drawings()
    print("rect", p.rect, "dibujos", len(dr), "imágenes", len(p.get_images()))
    for i, x in enumerate(dr[:20]):
        print(i, x["type"], x["rect"], x.get("fill"), len(x["items"]))


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="c", required=True)
s = sp.add_parser("render"); s.add_argument("src"); s.add_argument("out"); s.add_argument("--max", type=int, default=12); s.add_argument("--width", type=int, default=1400); s.set_defaults(f=render)
s = sp.add_parser("sheet"); s.add_argument("glob"); s.add_argument("out"); s.add_argument("--cols", type=int, default=3); s.add_argument("--tw", type=int, default=700); s.add_argument("--range"); s.set_defaults(f=sheet)
s = sp.add_parser("vectors"); s.add_argument("src"); s.add_argument("--page", type=int, default=0); s.set_defaults(f=vectors)
a = ap.parse_args(); a.f(a)
