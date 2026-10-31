"""handshake.py — comprueba en segundos lo que se puede verificar LOCALMENTE antes de trabajar con logos.

  python -I handshake.py

Revisa Python, Pillow/numpy (obligatorios para vectorizar), navegador headless (render de SVG y HTML),
y las herramientas opcionales (OpenCV, potrace, vtracer, cairosvg, Inkscape). Imprime también el valor de
CHROME_BIN que conviene exportar. No instala nada ni toca el sistema. Ver HANDSHAKE.md.
"""
import importlib
import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

rows = []


def chk(name, cond, hint="", required=True):
    tag = "OK   " if cond else ("FALTA" if required else "opc. ")
    rows.append((name, cond, required))
    print(f"[{tag}] {name}" + (f"  — {hint}" if (hint and not cond) else ""))


print("== Python y librerías ==")
chk("Python >= 3.9", sys.version_info >= (3, 9), sys.version.split()[0])
for mod, pip, req in (("PIL", "pillow", True), ("numpy", "numpy", True), ("cv2", "opencv-python", False)):
    try:
        importlib.import_module(mod)
        chk(f"módulo {mod}", True, required=req)
    except Exception:
        chk(f"módulo {mod}", False, f"pip install {pip}", required=req)
try:
    importlib.import_module("cairosvg")
    chk("cairosvg (rasterizador SVG alterno)", True, required=False)
except Exception:
    chk("cairosvg (rasterizador SVG alterno)", False, "en Windows suele faltar libcairo; no hace falta si hay Chrome", required=False)

print("\n== Navegador headless (render de SVG/HTML, superposición, hojas de prueba) ==")
cands = [
    os.environ.get("CHROME_BIN", ""),
    "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
for exe in ("google-chrome", "chromium", "chromium-browser", "chrome"):
    found = shutil.which(exe)
    if found:
        cands.append(found)
chrome = next((c for c in cands if c and os.path.exists(c)), None)
chk("Chrome / Edge / Chromium", bool(chrome), "instalar Chrome; el panel del navegador integrado NO sirve para esto")
if chrome:
    print(f"        CHROME_BIN sugerido: {chrome}")
    print("        (verificar_vectorizado.py y render_png.py lo detectan solos; con los scripts vendor sueltos, expórtalo)")

print("\n== Herramientas de vectorizado opcionales (la skill funciona sin ellas) ==")
for exe in ("potrace", "vtracer", "inkscape", "rsvg-convert", "magick"):
    chk(exe, bool(shutil.which(exe)), "opcional", required=False)

print("\n== Resumen ==")
missing = [n for n, ok, req in rows if req and not ok]
if missing:
    print("FALTA (obligatorio): " + ", ".join(missing))
    sys.exit(1)
print("Todo lo obligatorio está. Lo opcional que falte no bloquea el flujo.")
