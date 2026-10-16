"""qa_visual.py — capturas por tramos de una página a un ancho de dispositivo (Chrome headless + iframe) y montajes.

  python qa_visual.py <url> <ancho> <alto_total> <prefijo> [cols]
Genera <carpeta>/shots/<prefijo>_seg*.png (tramos) y <prefijo>_mNN.png (montajes de columnas). <carpeta> = $GUI_QA_DIR
o, por defecto, la carpeta temporal del sistema (gui-skills-qa). Chrome: variable CHROME o la ruta de Windows.
"""
import os, subprocess, sys, tempfile
from PIL import Image

# Carpeta de trabajo fuera de la skill (HTML puente, perfil de Chrome y capturas)
sc = os.environ.get("GUI_QA_DIR") or os.path.join(tempfile.gettempdir(), "gui-skills-qa")
os.makedirs(os.path.join(sc, "shots"), exist_ok=True)
url, w, total, pref = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
chrome = os.environ.get("CHROME") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # CHROME: ruta propia (macOS/Linux)
SEG = 12000
segs = []
y = 0
i = 0
while y < total:
    h = min(SEG, total - y)
    html = os.path.join(sc, "wrap_%s_%d.html" % (pref, i))
    open(html, "w", encoding="utf-8").write(
        '<!doctype html><html><body style="margin:0;background:#777;overflow:hidden">'
        '<iframe src="%s" style="width:%dpx;height:%dpx;border:0;background:#fff;margin-top:-%dpx"></iframe></body></html>' % (url, w, total, y))
    out = os.path.join(sc, "shots", "%s_seg%d.png" % (pref, i))
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=%d,%d" % (max(w, 500), h), "--user-data-dir=" + os.path.join(sc, "chromeprof"),
                    "--virtual-time-budget=30000", "--screenshot=" + out, "file:///" + html.replace("\\", "/")],
                   capture_output=True, timeout=240)
    segs.append(out)
    y += SEG
    i += 1
# unir tramos
full = None
imgs = [Image.open(s).convert("RGB").crop((0, 0, w, min(SEG, total - k * SEG))) for k, s in enumerate(segs)]
H = sum(im.height for im in imgs)
full = Image.new("RGB", (w, H), "white")
yy = 0
for im in imgs:
    full.paste(im, (0, yy))
    yy += im.height
# recortar el blanco final
px = full.load()
last = H - 1
while last > 0 and all(px[x, last] == (255, 255, 255) for x in range(0, w, 7)):
    last -= 1
full = full.crop((0, 0, w, min(H, last + 40)))
full.save(os.path.join(sc, "shots", pref + "_full.png"))
print("altura real:", full.height)
# montajes: columnas de 1700 px de alto
colh = 1700
per = cols * colh
n = 0
for y0 in range(0, full.height, per):
    m = Image.new("RGB", (cols * w + (cols - 1) * 12, colh), (120, 120, 120))
    for c in range(cols):
        yc = y0 + c * colh
        if yc >= full.height:
            break
        m.paste(full.crop((0, yc, w, min(yc + colh, full.height))), (c * (w + 12), 0))
    m.save(os.path.join(sc, "shots", "%s_m%02d.png" % (pref, n)))
    n += 1
print("montajes:", n)
