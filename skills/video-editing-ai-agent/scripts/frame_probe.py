#!/usr/bin/env python
"""Sonda de detalle: rafaga de fotogramas en un tramo, o recorte ampliado de una zona. Complementa video_understand.py.

Cuando el mapa no alcanza (texto pequeno, accion rapida, cara, logo, transicion), Claude pide mas vista justo ahi.

Uso:
  python frame_probe.py video.mp4 --at 12.5                      # un fotograma exacto
  python frame_probe.py video.mp4 --at 12.5 --span 2 --n 8       # rafaga: 8 fotogramas entre 11.5 y 13.5 (centrada en --at)
  python frame_probe.py video.mp4 --from 10 --to 14 --n 8        # rafaga entre dos tiempos
  python frame_probe.py video.mp4 --at 5 --crop 0.1,0.7,0.8,0.25 --scale 2   # recorte x,y,ancho,alto en FRACCIONES, ampliado x2
  python frame_probe.py video.mp4 --at 5 --diff 0.5              # fotograma en 5 s + mapa de calor de lo que cambio respecto a 5-0.5 s
Salida: PNG en <carpeta del video>/analisis/<nombre>/probes/ (o -o). Despues: Read del PNG.
La rafaga rotula cada celda con su tiempo; --diff marca en naranja las zonas que se movieron (sirve para ver QUE se mueve).
"""
import argparse, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import FFMPEG, probe_duration  # noqa: E402

BG, ACC = (18, 18, 22), (255, 140, 60)


def font(sz):
    for f in (r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, sz)
    return ImageFont.load_default()


def grab(video, t, out, crop=None, scale=1.0, long_side=900):
    vf = []
    if crop:
        x, y, w, h = crop
        vf.append(f"crop=iw*{w}:ih*{h}:iw*{x}:ih*{y}")
    if crop and scale != 1.0:
        vf.append(f"scale=iw*{scale}:ih*{scale}:flags=lanczos")
    elif not crop:
        vf.append(f"scale='if(gt(iw,ih),{long_side},-2)':'if(gt(iw,ih),-2,{long_side})'")
    cmd = [FFMPEG, "-v", "error", "-y", "-ss", f"{max(t, 0):.3f}", "-i", video, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += [out]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Image.open(out).convert("RGB") if os.path.exists(out) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("-o", "--output")
    ap.add_argument("--at", type=float); ap.add_argument("--span", type=float, default=0.0)
    ap.add_argument("--from", dest="t0", type=float); ap.add_argument("--to", dest="t1", type=float)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--crop", help="x,y,w,h en fracciones 0-1 (p. ej. 0.1,0.7,0.8,0.25)")
    ap.add_argument("--scale", type=float, default=1.0, help="ampliacion del recorte")
    ap.add_argument("--diff", type=float, help="segundos hacia atras para comparar (mapa de cambio)")
    a = ap.parse_args()
    video = os.path.abspath(a.video)
    dur = probe_duration(video)
    crop = tuple(float(v) for v in a.crop.split(",")) if a.crop else None
    if crop and len(crop) != 4:
        sys.exit("--crop necesita 4 valores: x,y,w,h")

    if a.t0 is not None and a.t1 is not None:
        times = [a.t0] if a.n == 1 else [a.t0 + i * (a.t1 - a.t0) / (a.n - 1) for i in range(a.n)]
    elif a.at is not None:
        if a.n > 1 and a.span > 0:
            times = [a.at - a.span / 2 + i * a.span / (a.n - 1) for i in range(a.n)]
        else:
            times = [a.at]
    else:
        sys.exit("indica --at, o --from y --to")
    times = [min(max(t, 0.0), max(dur - 0.04, 0.0)) for t in times]

    stem = os.path.splitext(os.path.basename(video))[0]
    out = a.output or os.path.join(os.path.dirname(video), "analisis", stem, "probes",
                                   f"probe_{times[0]:.2f}" + (f"-{times[-1]:.2f}" if len(times) > 1 else "") + (".crop" if crop else "") + ".png")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        if a.diff:
            t = times[0]
            cur = grab(video, t, os.path.join(tmp, "a.png"), crop, a.scale)
            prev = grab(video, t - a.diff, os.path.join(tmp, "b.png"), crop, a.scale)
            if cur is None or prev is None:
                sys.exit("no se pudo extraer")
            prev = prev.resize(cur.size)
            d = np.abs(np.asarray(cur, np.float32) - np.asarray(prev, np.float32)).mean(axis=2)
            d = d / max(d.max(), 1.0)
            heat = np.asarray(cur, np.float32) * 0.35
            heat[..., 0] += d * 255 * 0.65; heat[..., 1] += d * 140 * 0.65
            hm = Image.fromarray(np.clip(heat, 0, 255).astype(np.uint8))
            cv = Image.new("RGB", (cur.width * 3, cur.height + 24), BG)
            for j, (im, lab) in enumerate(((prev, f"{t - a.diff:.2f}s"), (cur, f"{t:.2f}s"), (hm, "cambio (naranja = se movio)"))):
                cv.paste(im, (j * cur.width, 24)); ImageDraw.Draw(cv).text((j * cur.width + 4, 4), lab, fill=ACC, font=font(14))
            frac = float((d > 0.25).mean())
            cv.save(out, "PNG")
            print(f"guardado: {out}\nzona con cambio fuerte: {frac * 100:.1f}% del cuadro")
            return
        imgs = [grab(video, t, os.path.join(tmp, f"p{i}.png"), crop, a.scale) for i, t in enumerate(times)]
    pairs = [(t, im) for t, im in zip(times, imgs) if im is not None]
    if not pairs:
        sys.exit("no se pudo extraer ningun fotograma")
    if len(pairs) == 1:
        pairs[0][1].save(out, "PNG")
    else:
        cols = min(len(pairs), 4 if pairs[0][1].height > pairs[0][1].width else 3)
        cw = 1560 // cols
        cells = [(t, im.resize((cw, int(cw * im.height / im.width)), Image.LANCZOS)) for t, im in pairs]
        ch = max(c.height for _, c in cells)
        rows = math.ceil(len(cells) / cols)
        cv = Image.new("RGB", (cols * cw, rows * (ch + 22)), BG)
        d = ImageDraw.Draw(cv)
        for j, (t, im) in enumerate(cells):
            x, y = (j % cols) * cw, (j // cols) * (ch + 22)
            cv.paste(im, (x, y)); d.text((x + 4, y + ch + 3), f"{t:.2f}s", fill=ACC, font=font(14))
        cv.save(out, "PNG")
    print("guardado:", out)


if __name__ == "__main__":
    main()
