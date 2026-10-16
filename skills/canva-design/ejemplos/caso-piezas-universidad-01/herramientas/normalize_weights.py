#!/usr/bin/env python3
"""Regla tipográfica del proyecto (decisión del usuario, 2026-10-09): UNA familia (la fuente de marca) y SOLO Regular / Bold / Italic,
para que el cambio de fuente en bloque de Canva sea limpio. Este script normaliza los HTML ya generados (idempotente):
  font-weight 600 / 800 / 900 → 700 ;  300 / 500 → 400 ;  y elimina las @font-face de pesos que ya no se usan.
Uso:  python -I normalize_weights.py            (todos los NN-slug/*.html)   |   python -I normalize_weights.py 05-radiologica …
El motor (`motor_series.build`) también lo aplica al escribir cada HTML, así que los módulos nuevos salen ya normalizados.
"""
import glob
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def normalize(html):
    html = re.sub(r'(font-weight\s*:\s*)(600|800|900)\b', r'\g<1>700', html)
    html = re.sub(r'(font-weight\s*:\s*)(300|500)\b', r'\g<1>400', html)
    # quitar @font-face de pesos eliminados (queda 400, 700 y la itálica 400)
    html = re.sub(r"[ \t]*@font-face\{font-family:'Fuente Marca';font-weight:(300|500|600|800);[^}]*\}\n?", '', html)
    return html


def main(args):
    pats = [os.path.join(ROOT, a, '*.html') for a in args] if args else [os.path.join(ROOT, '[0-9][0-9]-*', '*.html')]
    n = 0
    for pat in pats:
        for f in glob.glob(pat):
            s = open(f, encoding='utf-8').read()
            t = normalize(s)
            if t != s:
                open(f, 'w', encoding='utf-8').write(t)
                n += 1
    print(f'{n} HTML normalizados')


if __name__ == '__main__':
    main(sys.argv[1:])
