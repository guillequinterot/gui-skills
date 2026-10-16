"""split_pages.py — corta una captura alta (páginas apiladas) en una imagen por página + hoja de contacto.

Uso: python -I split_pages.py captura.png --w 2000 --h 1400 --prefix pag [--sheet hoja.png --sheet-w 1000]
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("png"); ap.add_argument("--w", type=int, required=True); ap.add_argument("--h", type=int, required=True)
ap.add_argument("--prefix", default="pag"); ap.add_argument("--sheet"); ap.add_argument("--sheet-w", type=int, default=1000)
a = ap.parse_args()
im = Image.open(a.png).convert("RGB")
n = im.height // a.h
files = []
for i in range(n):
    f = f"{a.prefix}_{i+1}.png"
    im.crop((0, i * a.h, a.w, (i + 1) * a.h)).save(f); files.append(f); print(f)
if a.sheet and files:
    th = int(a.h * a.sheet_w / a.w)
    S = Image.new("RGB", (a.sheet_w, th * len(files)), "white")
    for i, f in enumerate(files):
        S.paste(Image.open(f).resize((a.sheet_w, th)), (0, i * th))
    S.save(a.sheet); print(a.sheet)
