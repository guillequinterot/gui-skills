#!/usr/bin/env python
"""verify_fidelity.py — comprueba que el maestro de Illustrator es idéntico al diseño original.

  python -I verify_fidelity.py --raw <proyecto>/export/pdf --master <proyecto>/export/illustrator/maestro.ai [--tol 6000]

Por cada lámina (orden alfabético de --raw = orden de las mesas de trabajo / páginas del maestro):
  1. PIXELES: renderiza el PDF original (Chromium) y la página del maestro y cuenta los píxeles que difieren (> 60 de suma RGB).
     Un valor de unos pocos miles sobre 2 millones es suavizado del texto; una página en blanco da ~todos los píxeles.
  2. CARACTERES: compara el conjunto de letras de ambos (sin espacios) -> detecta texto perdido, cambiado o añadido.
El maestro puede ser el .ai (con «Crear archivo compatible con PDF») o el PDF multipágina guardado desde Illustrator.
Sale con código 1 si alguna lámina supera la tolerancia o cambian los caracteres.
"""
import argparse
import glob
import os
import re
import sys
from collections import Counter

import fitz
import numpy as np
from PIL import Image

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def render(page, zoom=1.0):
    pm = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    return np.asarray(Image.frombytes("RGB", (pm.width, pm.height), pm.samples)).astype(int)


def chars(page):
    return Counter(re.sub(r"\s+", "", page.get_text().replace(" ", "")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--master", required=True)
    ap.add_argument("--tol", type=int, default=6000)
    a = ap.parse_args()
    raws = sorted(f for f in glob.glob(os.path.join(a.raw, "*.pdf")) if not os.path.basename(f).startswith("_"))
    m = fitz.open(a.master)
    print(f"láminas originales: {len(raws)} | páginas del maestro: {len(m)}")
    if len(m) < len(raws):
        sys.exit("El maestro tiene menos páginas que láminas originales")
    res, bad_chars = [], []
    for i, f in enumerate(raws):
        r = fitz.open(f)[0]
        d = int((np.abs(render(r) - render(m[i])).sum(axis=2) > 60).sum())
        res.append((d, os.path.basename(f)))
        if chars(r) != chars(m[i]):
            bad_chars.append(os.path.basename(f))
    res.sort(reverse=True)
    print("peores diferencias de píxeles:", res[:6])
    print(f"todas dentro de tolerancia ({a.tol}):", all(n < a.tol for n, _ in res))
    print("láminas con diferencia de caracteres:", bad_chars or "ninguna")
    sys.exit(0 if all(n < a.tol for n, _ in res) and not bad_chars else 1)


if __name__ == "__main__":
    main()
