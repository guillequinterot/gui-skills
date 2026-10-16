#!/usr/bin/env python
"""Tira de fotogramas + forma de onda de un tramo de video (PNG). Revision visual bajo demanda.

Uso:
  python timeline_view.py video.mp4 INICIO FIN [-o out.png] [--n-frames 10] [--marks 3.1,7.4]
                          [--words words.json --key clip.mp4 --offset 0.0]
--marks : lineas verticales en tiempos del video (p. ej. los cortes/transiciones)
--words : JSON de transcribe_words.py para rotular palabras y sombrear silencios (>=0.4 s)
Sirve para el autoexamen tras renderizar (cortes, saltos, clics de audio). No es una herramienta de barrido.
Idea y disposicion adaptadas de browser-use/video-use (MIT); reescrito para Windows/Shotcut.
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from _common import FFMPEG, pcm_mono

BG, FG, DIM, WAVE, SIL, MARK = (18, 18, 22), (235, 235, 235), (110, 110, 120), (140, 180, 255), (50, 80, 120, 120), (255, 140, 60)


def font(sz):
    for f in (r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def frames(video, a, b, n, d):
    times = [(a + b) / 2] if n == 1 else [a + i * (b - a) / (n - 1) for i in range(n)]
    out = []
    for i, t in enumerate(times):
        p = os.path.join(d, f"f{i:03d}.jpg")
        subprocess.run([FFMPEG, "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-q:v", "4", "-vf", "scale=320:-2", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out.append(p)
    return out


def envelope(video, a, b, samples):
    try:
        x = pcm_mono(video, a, b - a, 16000)
    except Exception:
        return np.zeros(samples)
    if x.size == 0:
        return np.zeros(samples)
    w = max(1, x.size // samples)
    u = (x.size // w) * w
    env = np.sqrt(np.mean(x[:u].reshape(-1, w) ** 2, axis=1))
    env = np.pad(env, (0, max(0, samples - env.size)))[:samples]
    return env / env.max() if env.max() > 0 else env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("start", type=float); ap.add_argument("end", type=float)
    ap.add_argument("-o", "--output"); ap.add_argument("--n-frames", type=int, default=10)
    ap.add_argument("--marks", default=""); ap.add_argument("--words"); ap.add_argument("--key"); ap.add_argument("--offset", type=float, default=0.0)
    a = ap.parse_args()
    video = os.path.abspath(a.video)
    if a.end <= a.start:
        sys.exit("fin debe ser > inicio")
    out = a.output or os.path.join(os.path.dirname(video), "verify", f"{os.path.splitext(os.path.basename(video))[0]}_{a.start:.2f}-{a.end:.2f}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    words = []
    if a.words:
        data = json.load(open(a.words, encoding="utf-8"))
        words = [{"s": w["s"] + a.offset, "e": w["e"] + a.offset, "w": w["w"]} for w in (data.get(a.key) if a.key else next(iter(data.values())))]
        words = [w for w in words if w["e"] > a.start and w["s"] < a.end]
    marks = [float(x) for x in a.marks.split(",") if x.strip()]
    with tempfile.TemporaryDirectory() as tmp:
        imgs = [Image.open(p).convert("RGB") for p in frames(video, a.start, a.end, a.n_frames, tmp)]
    fh = 180
    imgs = [i.resize((int(fh * i.width / i.height), fh), Image.LANCZOS) for i in imgs]
    total = sum(i.width for i in imgs) + 4 * (len(imgs) - 1)
    W = max(1500, total + 100)
    wave_y, wave_h = 50 + fh + 30, 200
    H = wave_y + wave_h + 80
    cv = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(cv, "RGBA")
    d.text((50, 12), f"{os.path.basename(video)}   {a.start:.2f}s -> {a.end:.2f}s   ({a.end - a.start:.2f}s, {len(imgs)} fotogramas)", fill=FG, font=font(20))
    x = 50
    for i in imgs:
        cv.paste(i, (x, 50)); x += i.width + 4
    x0, x1 = 50, 50 + total
    tx = lambda t: int(x0 + (t - a.start) / (a.end - a.start) * (x1 - x0))
    d.rectangle((x0, wave_y, x1, wave_y + wave_h), fill=(28, 28, 34))
    prev = a.start
    for w in words + [{"s": a.end, "e": a.end, "w": ""}]:
        if w["s"] - prev >= 0.4:
            d.rectangle((tx(prev), wave_y, tx(w["s"]), wave_y + wave_h), fill=SIL)
        prev = max(prev, w["e"])
    env = envelope(video, a.start, a.end, max(x1 - x0, 200))
    mid, amp = wave_y + wave_h // 2, wave_h // 2 - 8
    top = [(x0 + int(i * (x1 - x0) / max(1, len(env) - 1)), mid - int(v * amp)) for i, v in enumerate(env)]
    bot = [(px, mid + (mid - py)) for px, py in top]
    d.polygon(top + bot[::-1], fill=(*WAVE, 70)); d.line(top, fill=WAVE); d.line(bot, fill=WAVE)
    last = -999
    for w in words:
        cx = (tx(w["s"]) + tx(w["e"])) // 2
        if cx - last >= 30 and w["w"]:
            d.text((cx + 2, wave_y - 18), w["w"], fill=FG, font=font(12)); last = cx
    for m in marks:
        if a.start <= m <= a.end:
            d.line((tx(m), 44, tx(m), wave_y + wave_h), fill=MARK, width=2)
            d.text((tx(m) + 3, wave_y + wave_h + 4), f"{m:.2f}s", fill=MARK, font=font(12))
    for i in range(7):
        t = a.start + i / 6 * (a.end - a.start)
        d.line((tx(t), wave_y + wave_h + 20, tx(t), wave_y + wave_h + 26), fill=DIM)
        d.text((tx(t) - 22, wave_y + wave_h + 28), f"{t:.2f}s", fill=DIM, font=font(12))
    cv.save(out, "PNG", optimize=True)
    print("guardado:", out)


if __name__ == "__main__":
    main()
