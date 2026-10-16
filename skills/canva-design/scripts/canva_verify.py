"""canva_verify.py — verificación visual del resultado en Canva (obligatoria antes de dar un trabajo por terminado).

  python -I canva_verify.py download <carpeta_salida> <url1> <url2> ...   # URLs que devuelve export-design (png, una por página)
  python -I canva_verify.py compare  <html_pagina.png> <canva_pagina.png> [--max 15]
  python -I canva_verify.py sheet    <salida.png> <img1> <img2> ... [--w 1000]

`compare` da la diferencia media (0-255). Referencia del caso `caso-diplomas-01`: 8-10 entre el HTML renderizado y la
exportación de Canva (diferencias esperadas: antialiasing de texto y el ajuste de ~0,1 em del "11"). >15 = revisar a ojo
(capas fuera de sitio, imagen que falta, texto partido).
"""
import argparse, os, sys, urllib.request
from PIL import Image, ImageChops, ImageStat

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def download(a):
    os.makedirs(a.out, exist_ok=True)
    for i, u in enumerate(a.urls, 1):
        f = os.path.join(a.out, f"canva-pag-{i}.png")
        urllib.request.urlretrieve(u, f)
        print(f, Image.open(f).size)


def compare(a):
    x = Image.open(a.a).convert("RGB"); y = Image.open(a.b).convert("RGB")
    if x.size != y.size:
        print("TAMAÑOS DISTINTOS", x.size, y.size); sys.exit(2)
    d = ImageChops.difference(x, y)
    m = sum(ImageStat.Stat(d).mean) / 3
    print(f"diferencia media = {m:.2f}  bbox={d.getbbox()}")
    sys.exit(0 if m <= a.max else 1)


def sheet(a):
    ims = [Image.open(f).convert("RGB") for f in a.imgs]
    th = int(ims[0].height * a.w / ims[0].width)
    S = Image.new("RGB", (a.w, th * len(ims)), "white")
    for i, im in enumerate(ims):
        S.paste(im.resize((a.w, th)), (0, i * th))
    S.save(a.out); print(a.out, S.size)


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="c", required=True)
s = sp.add_parser("download"); s.add_argument("out"); s.add_argument("urls", nargs="+"); s.set_defaults(f=download)
s = sp.add_parser("compare"); s.add_argument("a"); s.add_argument("b"); s.add_argument("--max", type=float, default=15); s.set_defaults(f=compare)
s = sp.add_parser("sheet"); s.add_argument("out"); s.add_argument("imgs", nargs="+"); s.add_argument("--w", type=int, default=1000); s.set_defaults(f=sheet)
a = ap.parse_args(); a.f(a)
