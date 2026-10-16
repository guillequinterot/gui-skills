#!/usr/bin/env python3
"""Hoja resumen de un programa: python -I make_sheet.py <carpeta-programa>  → previews/00-resumen.jpg
(Post c1/c2, Historia c1/c2 arriba; Banner c1/c2 abajo). Omite lo que no exista."""
import os
import sys

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
prog = sys.argv[1] if len(sys.argv) > 1 else '01-programa'
pv = os.path.join(ROOT, prog, 'previews')


def th(name, h):
    p = os.path.join(pv, name)
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert('RGB')
    return im.resize((round(im.width * h / im.height), h))


row_a = [i for i in (th('post_1.png', 520), th('post_2.png', 520), th('historia_1.png', 520), th('historia_2.png', 520)) if i]
row_b = [i for i in (th('banner_1.png', 300), th('banner_2.png', 300)) if i]
W = max(sum(i.width for i in row_a) + 10 * (len(row_a) + 1), sum(i.width for i in row_b) + 10 * (len(row_b) + 1))
sh = Image.new('RGB', (W, 860), (28, 28, 28))
x = 10
for i in row_a:
    sh.paste(i, (x, 10))
    x += i.width + 10
x = 10
for i in row_b:
    sh.paste(i, (x, 540))
    x += i.width + 10
sh.save(os.path.join(pv, '00-resumen.jpg'), quality=88)
print(os.path.join(pv, '00-resumen.jpg'))
