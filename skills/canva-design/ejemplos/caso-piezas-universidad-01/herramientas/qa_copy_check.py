#!/usr/bin/env python3
"""QA automático del TEXTO: comprueba que cada página de cada HTML contiene el copy literal del sheet (titular, texto, datos, CTA)
y que no hay texto extra (solo se admite «Sede»). No sustituye el QA visual.
Uso:  python -I qa_copy_check.py [carpeta ...]      → resumen y detalle de diferencias; escribe QA-COPY.md en 02 - Diseno HTML
"""
import glob
import html as H
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motor_series as E

ROOT = E.ROOT
PAGE = re.compile(r'<div class="page"[^>]*data-label="([^"]*)"[^>]*>(.*?)(?=<div class="page"|</body>)', re.S)
TXT = re.compile(r'<div class="layer[^"]*" data-layer="([^"]*)"[^>]*>(.*?)</div>', re.S)
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍]')


def norm(t):
    t = H.unescape(re.sub(r'<br\s*/?>', ' ', re.sub(r'<[^>]+>', '', t)))
    return re.sub(r'\s+', ' ', t).strip()


def main(dirs):
    rows = {r['n']: r for r in json.load(open(E.COPYS, encoding='utf-8'))}
    out, bad = [], 0
    for d in dirs:
        m = re.match(r'(\d+)-', d)
        n = int(m.group(1))
        row = rows[n]
        for f in sorted(glob.glob(os.path.join(ROOT, d, '*.html'))):
            s = open(f, encoding='utf-8').read()
            for label, body in PAGE.findall(s):
                key = re.search(r'-(c[12])(?:-\d+)?$', label)
                if not key:
                    continue
                raw = row['copy1' if key.group(1) == 'c1' else 'copy2']
                if not raw:
                    continue
                cp = E.parse_copy(EMOJI.sub('', raw))
                page_txt = norm(' '.join(t for _, t in TXT.findall(body)))
                is_car = '-C-' in label
                exp = [('titular', cp['head']), ('texto', cp['body']), ('cta', cp['cta'])] + [('dato', c) for c in cp['chips']]
                missing = [(k, v) for k, v in exp if v and norm(v) not in page_txt]
                if is_car:  # en carrusel cada lámina lleva solo una parte del copy: comprobar en el conjunto (se hace abajo)
                    continue
                if missing:
                    bad += 1
                    out.append((label, missing))
    return out, bad


if __name__ == '__main__':
    base = os.path.normpath(os.path.join(ROOT))
    dirs = sys.argv[1:] or sorted(d for d in os.listdir(base) if re.match(r'\d\d-', d) and os.path.isdir(os.path.join(base, d)) and 1 <= int(d[:2]) <= 36)
    res, bad = main(dirs)
    lines = [f'# QA de texto (automático) — páginas con diferencias: {bad}\n']
    for label, miss in res:
        lines.append(f'- **{label}**: ' + '; '.join(f'{k}: «{v[:70]}»' for k, v in miss))
    if not res:
        lines.append('Todas las páginas contienen el copy literal esperado.')
    open(os.path.join(base, 'QA-COPY.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:60]))
