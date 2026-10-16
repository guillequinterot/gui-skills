#!/usr/bin/env python3
"""Motor de diseño de series — genera los 3 HTML Canva-ready (post / historia / banner) de UN programa
con 2 diseños (c1 = Copy IN 1, c2 = Copy IN 2) a partir de una configuración por programa.

Uso desde un módulo de programa (la config por programa lleva: n, slug, folder, copy_row, palette, assets, variants; ver README del ejemplo):
    import motor_series as E
    E.build(cfg)

Qué hace: parsea el copy del sheet (titular / texto / datos separados por «|» / CTA), mide el texto con las
TTF reales de la fuente de marca, fluye la columna sin solapes (auto-ajusta el tamaño si no cabe), hornea el fondo
(foto + scrim) y emite HTML con capas absolutas, texto real y sin transform/gradiente/background:url.
Contenido de la pieza = SOLO el copy del sheet + barra de sede y lockup de la marca (decisión del usuario).
Layouts: 'overlay' (foto a sangre + scrim + columna de texto + persona opcional) y 'split' (panel de color +
foto/persona al otro lado). side='left' → texto a la izquierda; side='right' → espejo.
"""
import json
import os
import re
from PIL import Image, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
FONTS = os.path.join(ROOT, '_comun', 'fonts')
COPYS = os.path.join(os.path.dirname(ROOT), '03 - Contenidos', 'copys-anuncios.json')
LOGO_RATIO = 704.95 / 2730.4

FORMATS = {  # nombre: (letra, W, H, footer_top, footer_h, archivo)
    'post': ('P', 1080, 1080, 944, 136, 'post-1080x1080'),
    'historia': ('H', 1080, 1920, 1560, 160, 'historia-1080x1920'),
    'banner': ('B', 1200, 628, 548, 80, 'banner-1200x628'),
}

# ---------------------------------------------------------------- texto
_FW = {300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}
_fc = {}


def font(w, size):
    k = (w, round(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONTS, f'FuenteMarca-{_FW[w]}.ttf'), round(size))
    return _fc[k]


def tw(t, w, s):
    return font(w, s).getlength(t)


def wrap_lines(text, w, size, width):
    """lista de líneas (greedy por palabras; respeta saltos de línea explícitos)."""
    out = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split(' '):
            t = (cur + ' ' + word).strip()
            if tw(t, w, size) > width * 0.98 and cur:
                out.append(cur)
                cur = word
            else:
                cur = t
        out.append(cur)
    return out


# ---------------------------------------------------------------- parseo del copy
def parse_copy(raw):
    """→ dict(head, body, chips[list[str]], cta). Devuelve anomalías en 'warn'."""
    warn = []
    paras = [x.strip() for x in re.split(r'\n\s*\n', (raw or '').strip()) if x.strip()]
    # línea de datos con el CTA pegado en la línea siguiente (un solo salto): separarlos
    fixed = []
    for i, ptxt in enumerate(paras):
        if '|' in ptxt and '\n' in ptxt and i >= 2:
            first, rest = ptxt.split('\n', 1)
            fixed += [first.strip(), rest.strip()]
            warn.append('datos y CTA venían en el mismo párrafo (se separaron)')
        else:
            fixed.append(ptxt)
    paras = fixed
    d = dict(head='', body='', chips=[], cta='', warn=warn)
    if len(paras) != 4:
        warn.append(f'estructura inesperada: {len(paras)} párrafos (esperados 4)')
    if not paras:
        return d
    d['head'] = paras[0]
    if len(paras) >= 2:
        d['body'] = paras[1]
    if len(paras) >= 3:
        d['chips'] = [c.strip() for c in paras[2].split('|') if c.strip()]
    if len(paras) >= 4:
        d['cta'] = paras[3]
    return d


def icon_for(label):
    l = label.lower()
    if '$' in l:
        return 'coin'
    if 'hora' in l or 'intensidad' in l:
        return 'hourglass'
    if 'cupo' in l or 'participantes' in l or 'grupo' in l:
        return 'users'
    if re.search(r'lunes|martes|miércoles|miercoles|jueves|viernes|sábado|sabado|domingo|inicia|a\.m\.|p\.m\.|[0-9]:[0-9]{2}', l):
        return 'calendar'
    if 'presencial' in l:
        return 'pin'
    if 'virtual' in l or 'modalidad' in l:
        return 'monitor'
    return 'check'


ICONS = {
    'monitor': '<rect x="2.5" y="4" width="19" height="12.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M8 21h8M12 16.5V21" fill="none" stroke="{c}" stroke-width="2"/>',
    'hourglass': '<path d="M6 3h12M6 21h12M7 3c0 5 5 6 5 9s-5 4-5 9M17 3c0 5-5 6-5 9s5 4 5 9" fill="none" stroke="{c}" stroke-width="2"/>',
    'users': '<circle cx="9" cy="8" r="3.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M2.5 20c0-4 3-6 6.5-6s6.5 2 6.5 6M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.2c2.4.8 3.8 2.8 3.8 5.8" fill="none" stroke="{c}" stroke-width="2"/>',
    'coin': '<circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M15 8.5c-.7-1-1.8-1.5-3-1.5-1.8 0-3 .9-3 2.2 0 3 6 1.5 6 4.6 0 1.3-1.3 2.2-3 2.2-1.3 0-2.5-.5-3.2-1.6M12 5.5V7M12 17v1.5" fill="none" stroke="{c}" stroke-width="2"/>',
    'calendar': '<rect x="3" y="5" width="18" height="16" fill="none" stroke="{c}" stroke-width="2"/><path d="M3 10h18M8 3v4M16 3v4" fill="none" stroke="{c}" stroke-width="2"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="{c}" stroke-width="2"/>',
    'check': '<circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="{c}" stroke-width="2"/>',
}


def icon_svg(name, size, color):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{size}" height="{size}">'
            + ICONS[name].format(c=color) + '</svg>')


# ---------------------------------------------------------------- imágenes
def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cover(im, w, h, fx, fy):
    s = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * s) + 1, round(im.height * s) + 1), Image.LANCZOS)
    x, y = round((r.width - w) * fx), round((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))


def scrim(base, kind, color, strength):
    import numpy as np
    w, h = base.size
    x = np.arange(w, dtype=float)[None, :].repeat(h, 0)
    lo = 0.22
    if kind == 'left':
        a = strength * (1 - np.minimum(1.0, x / (w * 0.85))) ** 1.1 + lo
    elif kind == 'right':
        a = strength * (1 - np.minimum(1.0, (w - x) / (w * 0.85))) ** 1.1 + lo
    else:
        a = np.full((h, w), 0.20 + 0.15 * strength)
    a = np.clip(a, 0, 0.95)
    arr = np.asarray(base.convert('RGB'), dtype=float)
    tint = np.array(hex2rgb(color), dtype=float)[None, None, :]
    return Image.fromarray((arr * (1 - a[..., None]) + tint * a[..., None]).round().astype('uint8'))


def scrim_plateau(base, kind, color, strength):
    """Scrim con MESETA (texto legible a todo el ancho de la columna) y degradado suave hacia el lado de la imagen (agente 33–36, integrado 2026-10-09)."""
    import numpy as np
    w, h = base.size
    tall = h > w * 1.3
    p = 0.80 if tall else 0.60
    x = np.arange(w, dtype=float)[None, :].repeat(h, 0)
    if kind == 'flat':
        a = np.full((h, w), 0.20 + 0.15 * strength)
    else:
        u = x / w if kind == 'left' else (w - x) / w
        t = np.clip((u - p) / (1.0 - p + 1e-9), 0, 1)
        t = t * t * (3 - 2 * t)
        a = strength * (1 - t) + 0.12 * t
    a = np.clip(a, 0, 0.96)
    arr = np.asarray(base.convert('RGB'), dtype=float)
    tint = np.array(hex2rgb(color), dtype=float)[None, None, :]
    return Image.fromarray((arr * (1 - a[..., None]) + tint * a[..., None]).round().astype('uint8'))


def use_plateau_overlay():
    """Activa el scrim con meseta y columnas más estrechas en overlay sin persona (la foto se ve a un lado)."""
    global scrim
    scrim = scrim_plateau
    GEO[('overlay', 'post')].update(nop_head=(56, 620), nop_body=(29, 580), nop_chips=580)
    GEO[('overlay', 'historia')].update(nop_head=(74, 800), nop_body=(40, 780), nop_chips=800)
    GEO[('overlay', 'banner')].update(nop_head=(42, 700), nop_body=(24, 700), nop_chips=700)


# ---------------------------------------------------------------- HTML helpers
def st(**kw):
    return ';'.join(f'{k.replace("_", "-")}:{v}' for k, v in kw.items())


class Page:
    """acumula capas en orden; si mirror, refleja x respecto al ancho de la página."""

    def __init__(self, W, H, mirror=False):
        self.W, self.H, self.mirror, self.items = W, H, mirror, []

    def _mx(self, x, w):
        return self.W - x - w if self.mirror else x

    def rect(self, layer, x, y, w, h, color):
        x = self._mx(x, w)
        self.items.append(f'  <div class="layer" data-layer="{layer}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color}"></div>\n')

    def text(self, layer, x, y, w, size, weight, color, inner, cls='', align='left', lh=1.3, extra=''):
        if align == 'center':
            xx = self._mx(x, w)
        else:
            xx = self._mx(x, w)
        c = f' {cls}' if cls else ''
        self.items.append(f'  <div class="layer{c}" data-layer="{layer}" style="left:{xx}px;top:{y}px;width:{w}px;font-size:{size}px;font-weight:{weight};'
                          f'color:{color};line-height:{lh};text-align:{align};{extra}">{inner}</div>\n')

    def img(self, layer, src, x, y, w, h, alt=''):
        x = self._mx(x, w)
        self.items.append(f'  <img class="layer" data-layer="{layer}" src="{src}" alt="{alt}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">\n')

    def svg(self, layer, x, y, size, name, color):
        x = self._mx(x, size)
        self.items.append(f'  <div class="layer" data-layer="{layer}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px">{icon_svg(name, size, color)}</div>\n')

    def html(self):
        return ''.join(self.items)


def make_css(accent):
    fonts = ''.join(f"  @font-face{{font-family:'Fuente Marca';font-weight:{w};src:url('../_comun/fonts/FuenteMarca-{n}.ttf')}}\n"
                    for w, n in ((300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')))
    fonts += "  @font-face{font-family:'Fuente Marca';font-weight:400;font-style:italic;src:url('../_comun/fonts/FuenteMarca-Italic.ttf')}\n"
    return (fonts + "  *{box-sizing:border-box;margin:0;padding:0}\n  html,body{margin:0;background:#1b1b1b}\n"
            "  .page{position:relative;overflow:hidden;font-family:'Fuente Marca',sans-serif;color:#fff;background:#fff;margin:0}\n"
            "  .layer{position:absolute}\n  .head b{font-weight:800;color:%s}\n" % accent)


# ---------------------------------------------------------------- composición
class Flow:
    """columna de texto: calcula y, emite capas en la página."""

    def __init__(self, page, pal, x, y, limit, scale, k):
        self.p, self.pal, self.x, self.y, self.limit, self.s, self.k = page, pal, x, y, limit, scale, k
        self.gaps = 0

    def gap(self, g):
        self.gaps += g
        self.y += round(g * self.k)

    def head(self, text, size, width, accent_part=None, lh=1.12):
        size = round(size * self.s)
        pre, acc = text, ''
        if accent_part:
            pre, acc = accent_part
        shown = f'{pre}<b style="font-weight:800;color:{self.pal["accent"]}">{acc}</b>' if acc else pre
        shown = shown.replace('\n', '<br>')
        n = len(wrap_lines(text, 800, size, width))
        self.p.text('20 Titular', self.x, self.y, width, size, 700, self.pal['text'], shown, cls='head', lh=lh, extra='letter-spacing:-.005em;')
        self.y += round(n * size * lh)

    def body(self, text, size, width, lh=1.34):
        size = round(size * self.s)
        n = len(wrap_lines(text, 400, size, width))
        self.p.text('30 Texto', self.x, self.y, width, size, 400, self.pal['text'], text.replace('\n', '<br>'), lh=lh)
        self.y += round(n * size * lh)

    def chips(self, items, size, maxw, gap=12):
        fs = round(size * self.s)
        ic, pad = round(fs * 1.15), round(fs * .62)
        lh = 1.2
        rowh = round(fs * 2.1)
        cx, cy = self.x, self.y
        rows_end = cy
        for label in items:
            name = icon_for(label)
            inner_w = maxw - 2 * pad - ic - round(fs * .45)
            lines = wrap_lines(label, 600, fs, inner_w)
            labw = round(max(tw(l, 600, fs) for l in lines)) + 4
            cw = pad + ic + round(fs * .45) + labw + pad
            h = max(rowh, round(len(lines) * fs * lh + fs * .9))
            if cx + cw > self.x + maxw and cx > self.x:
                cx = self.x
                cy = rows_end + gap
            self.p.rect('50 Dato fondo', cx, cy, cw, h, self.pal['chip_bg'])
            self.p.svg('51 Icono', cx + pad, cy + (h - ic) // 2, ic, name, self.pal['chip_text'])
            self.p.text('52 Dato', cx + pad + ic + round(fs * .45), cy + round((h - len(lines) * fs * lh) / 2), labw + 30, fs, 600, self.pal['chip_text'],
                        '<br>'.join(lines), lh=lh, extra='white-space:nowrap;')
            rows_end = max(rows_end, cy + h)
            cx += cw + gap
        self.row_end, self.row_y, self.row_h = cx - gap, cy, h
        self.y = rows_end

    def cta(self, text, size, h, inline=None):
        fs = round(size * self.s)
        padx = round(fs * 1.3)
        w = round(tw(text, 800, fs)) + 2 * padx
        if inline is not None and self.row_end + inline + w <= self.x + self.maxw_inline:
            x, y, h = self.row_end + inline, self.row_y, self.row_h
        else:
            x, y, h = self.x, self.y, round(h * self.s)
            self.y += h
        self.p.rect('60 Boton fondo', x, y, w, h, self.pal['cta_bg'])
        self.p.text('61 Boton texto', x, y + round((h - fs * 1.2) / 2), w, fs, 800, self.pal['cta_text'], text, align='center', lh=1.2)


def split_accent(head):
    """(pre, acc): último tramo tras «:» o último enunciado. None si no hay."""
    t = head.strip()
    if ':' in t:
        a, b = t.split(':', 1)
        return (a + ': ', b.strip())
    parts = re.split(r'(?<=[.?!])\s+', t)
    if len(parts) >= 2:
        return (' '.join(parts[:-1]) + ' ', parts[-1])
    return None


GEO = {
    # (layout, formato) -> dict(person=(w,x), col=(x,w), head=(size,width), body=(size,width), chips=(size,maxw), cta=(size,h), y0, panel=(x,w))
    ('overlay', 'post'): dict(person=(560, 520), col=64, head=(58, 620), body=(30, 450), chips=(24, 450), cta=(30, 68), y0=60, nop_head=(60, 880), nop_body=(31, 760), nop_chips=760),
    ('split', 'post'): dict(person=(540, -30), col=548, head=(43, 484), body=(27, 484), chips=(24, 484), cta=(30, 68), y0=60, panel=(500, 580), nop_panel=(430, 650), nop_col=478, nop_w=554),
    ('overlay', 'historia'): dict(person=(680, 400), col=72, head=(78, 900), body=(40, 560), chips=(32, 330), cta=(38, 96), y0=270, nop_head=(80, 936), nop_body=(42, 936), nop_chips=936),
    ('split', 'historia'): dict(person=(600, -110), col=480, head=(58, 528), body=(34, 528), chips=(29, 528), cta=(38, 96), y0=270, panel=(430, 650), nop_panel=(300, 780), nop_col=350, nop_w=660),
    ('overlay', 'banner'): dict(person=(360, 810), col=48, head=(44, 700), body=(25, 700), chips=(22, 700), cta=(25, 54), y0=28, nop_head=(46, 1000), nop_body=(26, 1000), nop_chips=1000),
    ('split', 'banner'): dict(person=(366, -4), col=430, head=(38, 722), body=(24, 722), chips=(21, 722), cta=(25, 54), y0=28, panel=(380, 820), nop_panel=(300, 900), nop_col=346, nop_w=806),
}


def compose(cfg, fmt, key, copy):
    """HTML de una página (programa cfg, formato fmt, variante key 'c1'/'c2')."""
    letter, W, H, ft, fh, fname = FORMATS[fmt]
    var = cfg['variants'][key]
    pal = {**cfg['palette'], **var.get('pal', {})}
    layout, side = var.get('layout', 'overlay'), var.get('side', 'left')
    g = GEO[(layout, fmt)]
    mirror = side == 'right'
    person = var.get('person_img', cfg['assets'].get('person')) if var.get('person', True) else None
    photo = var.get('photo', cfg['assets'].get('photo'))
    # CONVENCIÓN DE IMÁGENES POR DISEÑO (fase Magnific): cada diseño (c1 / c2) tiene SU juego de imágenes, compartido por los 3 formatos.
    # Si existen en assets/ los archivos img-c1-fondo.jpg|png y/o img-c1-persona.png (idem c2), tienen prioridad sobre la config.
    _ad = os.path.join(cfg['folder'], 'assets')
    for _ext in ('jpg', 'png'):
        if os.path.exists(os.path.join(_ad, f'img-{key}-fondo.{_ext}')):
            photo = f'img-{key}-fondo.{_ext}'
            break
    if os.path.exists(os.path.join(_ad, f'img-{key}-persona.png')) and var.get('person', True):
        person = f'img-{key}-persona.png'
    elif photo and photo.startswith(f'img-{key}-fondo') and not var.get('keep_person'):
        person = None            # foto propia del diseño → se descarta el recorte de persona heredado de la config (salvo keep_person=True)
    if photo and photo.startswith(f'img-{key}-fondo'):
        _explicit = 'strip_fit' in var            # config ya calibrada a mano (p. ej. #10, idiomas): no tocar su foco
        var = dict(var)
        if layout == 'split':
            var.setdefault('strip_fit', True)     # panel + franja: recortar la foto a la franja visible
        _fj = os.path.join(_ad, f'img-{key}-foco.json')   # foco opcional por formato: {"post":[x,y],"historia":[x,y],"banner":[x,y]} o {"all":[x,y]}
        if os.path.exists(_fj):
            import json as _json
            _d = _json.load(open(_fj, encoding='utf-8'))
            var['focus'] = {f: tuple(_d.get(f, _d.get('all', (0.5, 0.5)))) for f in ('post', 'historia', 'banner')}
        elif layout == 'split' and not _explicit:
            var['focus'] = {f: (0.5, 0.5) for f in ('post', 'historia', 'banner')}
    label = f"{cfg['n']}-{letter}-{cfg['slug']}-{cfg.get('marca', 'marca')}-{key}"
    pg = Page(W, H, mirror)
    assets_dir = os.path.join(cfg['folder'], 'assets')
    # ---- fondo
    bgname = f'bg-{fmt}-{key}.jpg'
    if photo:
        focus = var.get('focus', {}).get(fmt, (0.5, 0.35))
        kind = ('left' if not mirror else 'right') if layout == 'overlay' else 'flat'
        _src = Image.open(os.path.join(cfg['folder'], 'assets', photo)).convert('RGB')
        if layout == 'split' and var.get('strip_fit'):
            # strip_fit (opt-in): recorta la foto SOLO a la franja visible (el panel tapa el resto), así `focus` encuadra al sujeto en la franja.
            _sw = (g['panel'] if person else g['nop_panel'])[0]          # ancho de la franja de foto (coordenadas sin espejar)
            base = Image.new('RGB', (W, H), pal['bg'])
            base.paste(cover(_src, _sw, H, *focus), (W - _sw if mirror else 0, 0))
        else:
            base = cover(_src, W, H, *focus)
        scrim(base, kind, pal.get('scrim', pal['bg']), var.get('scrim', 0.74)).save(os.path.join(assets_dir, bgname), quality=90)
        pg.items.append(f'  <img class="layer" data-layer="01 Fondo" src="assets/{bgname}" alt="" style="left:0px;top:0px;width:{W}px;height:{H}px">\n')
    else:
        pg.items.append(f'  <div class="layer" data-layer="01 Fondo" style="left:0px;top:0px;width:{W}px;height:{H}px;background:{pal["bg"]}"></div>\n')
    # ---- panel (split)
    if layout == 'split':
        px, pw = g['panel'] if person else g['nop_panel']
        if mirror:
            pg.items.append(f'  <div class="layer" data-layer="02 Panel" style="left:{W - px - pw}px;top:0px;width:{pw}px;height:{ft}px;background:{pal["bg"]}"></div>\n')
        else:
            pg.items.append(f'  <div class="layer" data-layer="02 Panel" style="left:{px}px;top:0px;width:{pw}px;height:{ft}px;background:{pal["bg"]}"></div>\n')
    # ---- persona
    if person:
        im = Image.open(os.path.join(assets_dir, person))
        wv, xv = g['person']
        wv = var.get('person_w', wv)
        hv = round(wv * im.height / im.width)
        pg.img('03 Persona', f'assets/{person}', xv, ft + 8 - hv, wv, hv, 'Persona')
    # ---- columna de texto
    if layout == 'overlay':
        x0 = g['col']
        hs, hw = g['head'] if person else g['nop_head']
        bs, bw = g['body'] if person else g['nop_body']
        cs, cm = g['chips'] if person else (g['chips'][0], g['nop_chips'])
    else:
        x0 = g['col'] if person else g['nop_col']
        hw = bw = cm = g['head'][1] if person else g['nop_w']
        hs, bs, cs = g['head'][0], g['body'][0], g['chips'][0]
    ctas, ctah = g['cta']
    limit = ft - (44 if fmt != 'banner' else 26) - (16 if fmt == 'historia' else 0)
    accent = var.get('accent_split', True)
    ap = split_accent(copy['head']) if accent else None

    colw = max(hw, bw, cm)
    xcol = (W - x0 - colw) if mirror else x0   # la columna se refleja como bloque (no elemento a elemento)

    def run(k, s, y0):
        sub = Page(W, H, False)
        fl = Flow(sub, pal, xcol, y0, limit, s, k)
        fl.maxw_inline = (hw if fmt == 'banner' else 0)
        fl.head(copy['head'], hs, hw, ap); fl.gap(30)
        if copy['body']:
            fl.body(copy['body'], bs, bw); fl.gap(32)
        if copy['chips']:
            fl.chips(copy['chips'], cs, cm, 10 if fmt == 'banner' else 12); fl.gap(14 if fmt == 'banner' else 30)
        if copy['cta']:
            fl.cta(copy['cta'], ctas, ctah, inline=14 if fmt == 'banner' and copy['chips'] else None)
        return fl, sub

    s = 1.0
    while True:
        fl, sub = run(1.0, s, g['y0'])
        if fl.y <= limit or s < 0.55:
            break
        s -= 0.04
    slack = limit - fl.y
    k = 1.0 + min(0.8, max(0.0, slack * 0.8 / fl.gaps)) if fl.gaps and fmt != 'banner' else 1.0
    y0 = g['y0'] + (max(0, slack // 2) if fmt == 'banner' else 0)
    fl, sub = run(k, s, y0)
    ok = fl.y <= limit
    pg.items += sub.items
    # ---- pie
    fb = pal['footer_bg']
    ftxt = pal.get('footer_text', '#FFFFFF')
    tail = fmt == 'historia'
    pg.rect('90 Barra inferior', 0, ft, W, fh if tail else H - ft, fb)
    if tail:
        pg.items.append(f'  <div class="layer" data-layer="89 Zona segura inferior" style="left:0px;top:{ft + fh}px;width:{W}px;height:{H - ft - fh}px;background:{pal.get("tail_bg", pal["bg"])}"></div>\n')
    lw = {'post': 300, 'historia': 380, 'banner': 250}[fmt]
    lh_ = round(lw * LOGO_RATIO)
    pad = {'post': 64, 'historia': 72, 'banner': 48}[fmt]
    ls = {'post': 26, 'historia': 32, 'banner': 20}[fmt]
    # el pie no se espeja: texto a la izquierda, logo a la derecha siempre
    pg.mirror = False
    pg.text('91 Sede', pad, ft + round((fh - ls * 1.2) / 2), 320, ls, 400, ftxt, 'Sede', lh=1.2, extra='font-style:italic;')
    logo = 'blanco' if pal.get('logo', 'blanco') == 'blanco' else 'negro'
    pg.img('92 Logo', f'../_comun/logos/lockup_{logo}.svg', W - pad - lw, ft + round((fh - lh_) / 2), lw, lh_,
           'Logo de la marca')
    print(f"  [{'OK   ' if ok else 'SOBRA'}] {label}: y={fl.y}/{limit} escala={s:.2f}")
    return (f'<div class="page" data-document-role="page" data-label="{label}" id="{label}" style="width:{W}px;height:{H}px">\n'
            + pg.html() + '</div>\n')


def prep_image(src, dst, maxside=2400, alpha=False):
    """copia una imagen fuente al assets del programa (RGB .jpg o RGBA .png), limitando el lado mayor."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src)
    im = im.convert('RGBA' if alpha else 'RGB')
    im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(dst, optimize=True) if alpha else im.save(dst, quality=92)


def build(cfg):
    """cfg: dict(n, slug, folder, copy_row (n del sheet), palette, assets, variants)."""
    rows = {r['n']: r for r in json.load(open(COPYS, encoding='utf-8'))}
    row = rows[cfg['n']]
    copies = {'c1': parse_copy(row['copy1']), 'c2': parse_copy(row['copy2']) if row['copy2'] else None}
    for k, v in cfg.get('copy_override', {}).items():
        copies[k] = v
    os.makedirs(os.path.join(cfg['folder'], 'assets'), exist_ok=True)
    print(f"[{cfg['n']}] {cfg['slug']}")
    for k, c in copies.items():
        if c and c.get('warn'):
            print(f'  AVISO {k}: ' + '; '.join(c['warn']))
    for fmt in ('post', 'historia', 'banner'):
        letter, W, H, ft, fh, fname = FORMATS[fmt]
        pages = ''
        for key in ('c1', 'c2'):
            if copies.get(key) and copies[key]['head']:
                pages += compose(cfg, fmt, key, copies[key])
            else:
                print(f'  (sin copy {key}: página omitida)')
        html = (f'<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width={W}">\n'
                f'<title>Serie · {cfg["n"]} {cfg["slug"]} · {fmt} {W}x{H}</title>\n<style>\n{make_css(cfg["palette"]["accent"])}</style>\n</head>\n<body>\n{pages}</body>\n</html>\n')
        try:
            from normalize_weights import normalize  # regla tipográfica: solo Regular/Bold/Italic
            html = normalize(html)
        except ImportError:
            pass
        with open(os.path.join(cfg['folder'], fname + '.html'), 'w', encoding='utf-8') as f:
            f.write(html)
