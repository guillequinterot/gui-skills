"""bake_assets.py — genera los assets de arte que Canva NO puede importar desde HTML.

Uso (siempre con -I):
  python -I bake_assets.py <subcomando> [opciones]

Subcomandos (todos probados en el caso `caso-diplomas-01`, 2026-10-08):
  panel      Panel de color con borde de pincel seco (PNG alfa).        --w --h --edge --color --out
  swoosh     Pincelada horizontal con degradé tonal y borde seco.       --w --h --out  [--stops]
  triangles  Mosaico low-poly (Delaunay) que se disuelve en blanco.     --w --h --out  [--seed]
  marble     Recorte vertical de una foto de pintura fluida + remapeo de matiz a rojos.  --src --w --h --out
  canvas-bg  Textura de lienzo casi blanca (desde foto de tela de stock). --src --w --h --out
  vignette   Fondo oscuro con luz radial (vino/negro).                  --w --h --out --inner --mid --outer
  logo       Exporta un artboard de un .ai/PDF a SVG + PNG recortado.   --src --page --svg --png

Todas las medidas son px de Canva (el PNG sale a 2x del tamaño CSS donde se indica).
Requiere: numpy, Pillow, PyMuPDF (fitz), scipy (solo triangles).
"""
import argparse, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def grad(stops, t):
    """stops: [(pos, rgb)]; t: ndarray 0..1 -> rgb"""
    ps = [s[0] for s in stops]
    out = np.zeros(np.shape(t) + (3,))
    for c in range(3):
        out[..., c] = np.interp(t, ps, [s[1][c] for s in stops])
    return out


# Paleta tonal de ejemplo (rojos: vino -> profundo -> marca -> vivo -> coral); sustituir por la de la marca activa
TONAL = [(0, "#4E0814"), (0.30, "#8E0F1B"), (0.62, "#DA111C"), (0.88, "#F2343B"), (1.0, "#FF6B5E")]


def tonal_stops(spec=None):
    pts = spec or TONAL
    return [(p, hexrgb(c)) for p, c in pts]


# --------------------------------------------------------------------------- panel
def cmd_panel(a):
    """Panel con borde derecho de pincel seco. 2x de w x h (CSS)."""
    W, H = a.w * 2, a.h * 2
    rng = np.random.default_rng(a.seed)
    y = np.arange(H)
    base = a.edge * 2 + 36 * np.sin(y / 260.0 + 0.6) + 22 * np.sin(y / 93.0 + 2.0) + y * 0.035
    L = np.zeros(H); i = 0
    while i < H:
        h = int(rng.integers(2, 11)); v = rng.random()
        L[i:i + h] = (v ** 2.4) * 200 + (rng.random() < 0.06) * rng.random() * 120
        i += h
    L = np.convolve(L, np.ones(3) / 3, mode="same")
    x = np.arange(W)[None, :]
    edge = (base + L)[:, None]
    gap = rng.random((H // 4 + 1, W // 28 + 1))
    gap = np.asarray(Image.fromarray((gap * 255).astype('uint8')).resize((W, H), Image.BILINEAR)).astype(float) / 255
    fringe = (x - base[:, None]) / np.maximum(L[:, None], 1)
    alpha = ((x < edge) & ~((fringe > 0.45) & (gap > 0.55 - 0.3 * (1 - fringe)))).astype(float)
    img = Image.fromarray((alpha * 255).astype('uint8'))
    dr = ImageDraw.Draw(img)
    for _ in range(34):
        cy = int(rng.integers(0, H)); cx = int(base[cy] + L[cy] + rng.random() * 160 + 10)
        rx = rng.random() * 9 + 2; ry = rng.random() * 4 + 1.5
        dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    img = img.filter(ImageFilter.GaussianBlur(0.9)).point(lambda v: 0 if v < 110 else (255 if v > 150 else int((v - 110) / 40 * 255)))
    rgb = hexrgb(a.color)
    out = np.zeros((H, W, 4), dtype='uint8'); out[..., :3] = rgb.astype('uint8'); out[..., 3] = np.asarray(img)
    Image.fromarray(out, "RGBA").save(a.out); print("panel", a.out, (W, H))


# --------------------------------------------------------------------------- swoosh
def cmd_swoosh(a):
    """Pincelada horizontal a sangre arriba, borde inferior de cerdas secas. PNG a 2x (w x h CSS)."""
    W, H = a.w * 2, a.h * 2
    rng = np.random.default_rng(a.seed)
    x = np.arange(W)
    base = a.base * 2 - a.slope * x + 70 * np.sin(x / 560.0 + 0.5) + 20 * np.sin(x / 190.0 + 1.3)
    y = np.arange(H)[:, None]

    def hnoise(seed, stretch, cell):
        r = np.random.default_rng(seed)
        b = r.random((int(H / cell) + 2, int(W / (cell * stretch)) + 2))
        return np.asarray(Image.fromarray((b * 255).astype('uint8')).resize((W, H), Image.BICUBIC)).astype(float) / 255

    nn = 0.7 * hnoise(3, 70, 5) + 0.3 * hnoise(9, 25, 3)
    nn = (nn - nn.min()) / (nn.max() - nn.min())
    T = 150.0
    dist = (y - base[None, :])
    alpha = np.where(dist < 0, 1.0, np.where(dist < T, (nn ** 1.6 > dist / T).astype(float), 0.0))
    img = Image.fromarray((alpha * 255).astype('uint8'))
    dr = ImageDraw.Draw(img)
    for _ in range(26):
        cx = int(rng.integers(int(W * 0.6), W - 40)); cy = int(base[cx] + T * 0.9 + rng.random() * 120)
        rx = rng.random() * 12 + 3; ry = rng.random() * 4 + 1.5
        dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    img = img.filter(ImageFilter.GaussianBlur(1.1)).point(lambda v: 0 if v < 110 else (255 if v > 150 else int((v - 110) / 40 * 255)))
    mask = np.asarray(img).astype(float) / 255
    xx = np.arange(W)[None, :] / W; yy = np.arange(H)[:, None] / H
    t = np.clip(xx * 0.88 + yy * 0.12 + 0.03 * np.sin(xx * 9), 0, 1)
    col = grad(tonal_stops(), t * np.ones((H, 1)))
    lum = 1 + (nn - 0.5) * 0.16 + (hnoise(5, 120, 2) - 0.5) * 0.08
    col = np.clip(col * lum[..., None], 0, 255)
    Image.fromarray(np.dstack([col, mask * 255]).astype('uint8'), "RGBA").save(a.out)
    print("swoosh", a.out, (W, H))


# --------------------------------------------------------------------------- triangles
def cmd_triangles(a):
    from scipy.spatial import Delaunay
    random.seed(a.seed)
    S = a.cell
    P = []
    for r in range(-1, int(a.h / (S * 0.866)) + 2):
        for c in range(-2, int(a.w / S) + 2):
            P.append((c * S + (S / 2 if r % 2 else 0) + random.uniform(-.17 * S, .17 * S), r * S * 0.866 + random.uniform(-.17 * S, .17 * S)))
    P = np.array(P); tri = Delaunay(P)
    st = tonal_stops(); poly = []
    for simp in tri.simplices:
        p0, p1, p2 = P[simp]
        cx = (p0[0] + p1[0] + p2[0]) / 3; cy = (p0[1] + p1[1] + p2[1]) / 3
        if cx < -400 or cy < -80 or cy > a.h + 100: continue
        fade = 1.0 if cx < a.fade_from else max(0.0, 1.0 - (cx - a.fade_from) / a.fade_len)
        if cx > a.fade_from + 30: fade *= random.choice([1, 1, 0.55, 0.3])
        if fade <= 0.05: continue
        t = float(np.clip(cx / a.w * 0.45 + cy / a.h * 0.45 + random.uniform(-0.2, 0.2), 0, 1))
        rgb = grad([(0, st[0][1]), (0.25, st[1][1]), (0.52, st[2][1]), (0.78, st[3][1]), (1.0, st[4][1])], np.array(t))
        hx = "#%02X%02X%02X" % tuple(int(v) for v in np.clip(rgb, 0, 255))
        poly.append(f'<polygon points="{p0[0]:.1f},{p0[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{hx}" fill-opacity="{fade:.2f}" stroke="{hx}" stroke-opacity="{fade:.2f}" stroke-width="1.2"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {a.w} {a.h}" width="{a.w}" height="{a.h}"><defs><clipPath id="c"><rect width="{a.w}" height="{a.h}"/></clipPath></defs><g clip-path="url(#c)">{"".join(poly)}</g></svg>')
    open(a.out, "w", encoding="utf-8").write(svg)
    import fitz
    d = fitz.open(a.out); pix = d[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=True)
    pix.save(a.out.rsplit('.', 1)[0] + ".png")
    print("triangles", a.out, len(poly))


# --------------------------------------------------------------------------- marble
def cmd_marble(a):
    src = Image.open(a.src).convert("RGB")
    sw, sh = src.size
    cw = int(sh * a.w / a.h)
    box = (a.crop_x, 0, a.crop_x + cw, sh)
    m = src.crop(box).resize((a.w * 2, a.h * 2), Image.LANCZOS)
    hsv = np.asarray(m.convert("HSV")).astype(float)
    h = hsv[..., 0] / 255.0
    h2 = h.copy()
    purple = h > 0.70
    h2[purple] = 0.985 + (h[purple] - 0.70) * 0.05          # violetas/magentas -> rojo vino
    orange = (h < 0.12) & (h >= 0.02)
    h2[orange] = 0.995 + (h[orange] - 0.02) * 0.10          # naranjas -> rojo vivo
    hsv[..., 0] = (h2 % 1.0) * 255
    Image.fromarray(hsv.astype('uint8'), "HSV").convert("RGB").save(a.out, quality=90)
    print("marble", a.out, (a.w * 2, a.h * 2))


# --------------------------------------------------------------------------- canvas-bg
def cmd_canvasbg(a):
    im = Image.open(a.src).convert("L")
    a_ = np.asarray(im.crop((a.x, a.y, a.x + a.w, a.y + a.h))).astype(float)
    b = np.clip(a.mean + (a_ - a_.mean()) * a.contrast, a.floor, 255).astype('uint8')
    Image.fromarray(b).convert('RGB').save(a.out, quality=90)
    print("canvas-bg", a.out, b.shape)


# --------------------------------------------------------------------------- vignette
def cmd_vignette(a):
    yy, xx = np.mgrid[0:a.h, 0:a.w].astype(float)
    d = np.sqrt(((xx - a.w * a.cx) / (a.w * 0.80)) ** 2 + ((yy - a.h * a.cy) / (a.h * 0.85)) ** 2)
    c = grad([(0, hexrgb(a.inner)), (0.5, hexrgb(a.mid)), (1.0, hexrgb(a.outer))], np.clip(d, 0, 1))
    Image.fromarray(c.astype('uint8')).save(a.out, quality=92)
    print("vignette", a.out, (a.w, a.h))


# --------------------------------------------------------------------------- logo
def cmd_logo(a):
    import fitz
    d = fitz.open(a.src); p = d[a.page]
    z = a.px / p.rect.width
    pix = p.get_pixmap(matrix=fitz.Matrix(z, z), alpha=True)
    im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    pad = 4
    bb = (max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))
    im.crop(bb).save(a.png)
    p.set_cropbox(fitz.Rect(bb[0] / z, bb[1] / z, bb[2] / z, bb[3] / z))
    open(a.svg, "w", encoding="utf-8").write(p.get_svg_image(text_as_path=True))
    print("logo", a.svg, a.png, im.crop(bb).size)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("panel"); s.add_argument("--w", type=int, default=760); s.add_argument("--h", type=int, default=1080)
    s.add_argument("--edge", type=int, default=665, help="x (CSS px) donde empieza el borde de pincel"); s.add_argument("--color", default="#DA111C")
    s.add_argument("--seed", type=int, default=11); s.add_argument("--out", required=True); s.set_defaults(f=cmd_panel)

    s = sp.add_parser("swoosh"); s.add_argument("--w", type=int, default=2000); s.add_argument("--h", type=int, default=850)
    s.add_argument("--base", type=int, default=690, help="y (CSS px) del borde inferior a la izquierda"); s.add_argument("--slope", type=float, default=0.135)
    s.add_argument("--seed", type=int, default=21); s.add_argument("--out", required=True); s.set_defaults(f=cmd_swoosh)

    s = sp.add_parser("triangles"); s.add_argument("--w", type=int, default=900); s.add_argument("--h", type=int, default=1400)
    s.add_argument("--cell", type=int, default=230); s.add_argument("--fade-from", dest="fade_from", type=int, default=470); s.add_argument("--fade-len", dest="fade_len", type=int, default=420)
    s.add_argument("--seed", type=int, default=7); s.add_argument("--out", required=True, help="ruta .svg (genera también .png a 2x)"); s.set_defaults(f=cmd_triangles)

    s = sp.add_parser("marble"); s.add_argument("--src", required=True); s.add_argument("--w", type=int, default=820); s.add_argument("--h", type=int, default=1400)
    s.add_argument("--crop-x", dest="crop_x", type=int, default=300); s.add_argument("--out", required=True); s.set_defaults(f=cmd_marble)

    s = sp.add_parser("canvas-bg"); s.add_argument("--src", required=True); s.add_argument("--w", type=int, default=2000); s.add_argument("--h", type=int, default=1400)
    s.add_argument("--x", type=int, default=300); s.add_argument("--y", type=int, default=700)
    s.add_argument("--mean", type=float, default=251); s.add_argument("--contrast", type=float, default=0.42); s.add_argument("--floor", type=int, default=236)
    s.add_argument("--out", required=True); s.set_defaults(f=cmd_canvasbg)

    s = sp.add_parser("vignette"); s.add_argument("--w", type=int, default=2000); s.add_argument("--h", type=int, default=1400)
    s.add_argument("--inner", default="#7A1022"); s.add_argument("--mid", default="#4A0A16"); s.add_argument("--outer", default="#2A050C")
    s.add_argument("--cx", type=float, default=0.30); s.add_argument("--cy", type=float, default=0.35); s.add_argument("--out", required=True); s.set_defaults(f=cmd_vignette)

    s = sp.add_parser("logo"); s.add_argument("--src", required=True); s.add_argument("--page", type=int, default=0, help="artboard (p. ej. 0=plano, 3=contorno blanco; depende del .ai de la marca)")
    s.add_argument("--px", type=int, default=2400); s.add_argument("--svg", required=True); s.add_argument("--png", required=True); s.set_defaults(f=cmd_logo)

    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
