#!/usr/bin/env python3
"""prepare_multipage_import.py — prepara HTML Canva-ready de VARIAS páginas (incluso de tamaños distintos) para importarlo a Canva
de una sola vez y poblar las imágenes por API (flujo B, verificado en el caso `caso-piezas-universidad-01`, 2026-10-09).

Qué hace
  1. Lee uno o más HTML cuyas páginas son <div class="page" data-document-role="page" data-label="…" style="width:Wpx;height:Hpx">.
  2. Ordena las páginas (por nomenclatura N-F-slug-…-cX: programa, variante c1/c2, formato P/H/B; o por el orden dado).
  3. Sustituye cada <img> por un <div class="layer"> gris (#7f7f7f) con el MISMO left/top/width/height: el importador lo trae como
     rectángulo con posición exacta y en el z-order correcto → luego se rellena con update_fill (+ crop_media) o insert_fill.
  4. Quita los @font-face (el importador los ignora; las rutas relativas no existirían en el hosting).
  5. Escribe el HTML combinado + un manifiesto JSON (por página: título, tamaño, imágenes con src/posición/tipo) para guiar las llamadas
     a edit-design y la subida de assets.

Uso
  python -I prepare_multipage_import.py OUT.html a.html b.html c.html [--manifest OUT.json] [--order "label1,label2,…"] [--keep-fontface]
Notas
  - Las rutas src se resuelven respecto a cada HTML de entrada y se guardan ABSOLUTAS en el manifiesto (para subir los assets).
  - El logo SVG no admite update_fill: el manifiesto marca kind="svg" → usar insert_fill y borrar el marcador (o subir un PNG).
  - Tras importar: leer los ids con read-design (transacción) buscando rectángulos con fill #7f7f7f.
"""
import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

PAGE_RE = re.compile(r'<div class="page"[^>]*data-document-role="page"[^>]*>', re.S)
IMG_RE = re.compile(r'<img\b([^>]*)>', re.S)
ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
FONTFACE_RE = re.compile(r'\s*@font-face\s*\{[^}]*\}\s*', re.S)
FMT_ORDER = {'P': 0, 'H': 1, 'B': 2, 'C': 3}


def split_pages(html):
    """→ (head, [page_html…]) respetando el anidado de <div>."""
    body_i = html.find('<body')
    body_i = html.find('>', body_i) + 1 if body_i >= 0 else 0
    end_i = html.rfind('</body>')
    head, body = html[:body_i], html[body_i:end_i if end_i > 0 else len(html)]
    pages, pos = [], 0
    for m in PAGE_RE.finditer(body):
        if m.start() < pos:
            continue
        depth, i = 0, m.start()
        for t in re.finditer(r'<(/?)div\b', body[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                j = body.find('>', m.start() + t.start()) + 1
                pages.append(body[m.start():j])
                pos = j
                break
    return head, pages


def sort_key(label):
    # N-F-slug-…-cX  o, para carruseles, N-C-slug-…-cX-L (L = nº de lámina)
    m = re.match(r'^(\d+)-([PHBC])-.*?-c(\d)(?:-(\d+))?$', label or '')
    if not m:
        return (9999, 9, 9, 0, label or '')
    return (int(m.group(1)), int(m.group(3)), FMT_ORDER[m.group(2)], int(m.group(4) or 0), label)


def px(style, prop):
    m = re.search(r'(?<![\w-])' + prop + r'\s*:\s*(-?[\d.]+)px', style)
    return float(m.group(1)) if m else None


def process(html, src_dir, manifest_page, grey):
    def sub(m):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        style = attrs.get('style', '')
        l, t, w, h = (px(style, k) for k in ('left', 'top', 'width', 'height'))
        src = attrs.get('src', '')
        path = os.path.normpath(os.path.join(src_dir, src)) if not re.match(r'^(https?:|data:)', src) else src
        manifest_page['images'].append(dict(layer=attrs.get('data-layer', ''), src=path, left=l, top=t, width=w, height=h,
                                            kind='svg' if src.lower().endswith('.svg') else 'raster', alt=attrs.get('alt', '')))
        layer = attrs.get('data-layer', 'Imagen')
        return (f'<div class="layer" data-layer="{layer}" style="left:{l:g}px;top:{t:g}px;width:{w:g}px;height:{h:g}px;background:{grey}"></div>')
    return IMG_RE.sub(sub, html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--manifest')
    ap.add_argument('--order', help='etiquetas separadas por coma (si no, orden por nomenclatura N-F-slug-…-cX)')
    ap.add_argument('--grey', default='#7f7f7f')
    ap.add_argument('--keep-fontface', action='store_true')
    a = ap.parse_args()
    heads, collected = [], []
    for f in a.inputs:
        html = open(f, encoding='utf-8').read()
        head, pages = split_pages(html)
        heads.append(head)
        for p in pages:
            label = (re.search(r'data-label="([^"]*)"', p) or [None, ''])[1]
            w = re.search(r'style="[^"]*width:(\d+)px', p)
            h = re.search(r'style="[^"]*height:(\d+)px', p)
            mp = dict(label=label, width=int(w.group(1)) if w else None, height=int(h.group(1)) if h else None, images=[], source=os.path.abspath(f))
            collected.append((label, process(p, os.path.dirname(os.path.abspath(f)), mp, a.grey), mp))
    if a.order:
        order = [x.strip() for x in a.order.split(',')]
        collected.sort(key=lambda t: order.index(t[0]) if t[0] in order else 999)
    else:
        collected.sort(key=lambda t: sort_key(t[0]))
    head = heads[0]
    if not a.keep_fontface:
        head = FONTFACE_RE.sub('\n', head)
    body = ''.join(p + '\n' for _, p, _ in collected)
    sizes = {(m['width'], m['height']) for _, _, m in collected}
    head = re.sub(r'<meta name="viewport"[^>]*>', f'<meta name="viewport" content="width={max(s[0] for s in sizes if s[0])}">', head)
    head = re.sub(r'<title>.*?</title>', '<title>Importación multipágina</title>', head, flags=re.S)
    open(a.out, 'w', encoding='utf-8').write(head + body + '</body>\n</html>\n')
    man = dict(output=os.path.abspath(a.out), page_count=len(collected), sizes=sorted(sizes), pages=[m for _, _, m in collected])
    mp = a.manifest or os.path.splitext(a.out)[0] + '.manifest.json'
    json.dump(man, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{a.out}: {len(collected)} páginas, tamaños {sorted(sizes)}; imágenes→marcadores: {sum(len(m["images"]) for _, _, m in collected)}; manifiesto: {mp}')
    for label, _, m in collected:
        print(f'  - {label} ({m["width"]}x{m["height"]}) · {len(m["images"])} imágenes')


if __name__ == '__main__':
    sys.exit(main())
