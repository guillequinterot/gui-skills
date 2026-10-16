#!/usr/bin/env python
"""handshake.py — preflight de web-go-high-level-ia: ¿esta máquina puede ejecutar el proceso?

  python -I handshake.py [--proyecto "<carpeta-del-proyecto>"]

Solo lectura. Comprueba:
  1. Windows + PowerShell (Set-Clipboard para el pegado).
  2. Node y npm (chequeo de tipos y servidor local).
  3. Edge (capturas headless) y Chrome (Claude in Chrome).
  4. Python: Pillow (opcional, contactos/QA de imágenes).
  5. Si se pasa --proyecto: existen AGENTS.md y README.md del proyecto del constructor (carpeta descargada).
Imprime OK / AVISO / FALLO por línea. Código de salida 1 si hay algún FALLO.
"""
import argparse
import glob
import os
import platform
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

fails = 0


def line(kind, msg):
    global fails
    if kind == "FALLO":
        fails += 1
    print(f"{kind:6} {msg}")


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15, shell=True).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return ""


ap = argparse.ArgumentParser()
ap.add_argument("--proyecto")
a = ap.parse_args()

if platform.system() == "Windows":
    line("OK", "Sistema: Windows (el pegado usa Set-Clipboard de PowerShell; es la ruta verificada)")
else:
    line("AVISO", f"Sistema: {platform.system()} (la receta de pegado está verificada solo en Windows; en macOS el equivalente de Set-Clipboard es pbcopy, sin probar)")
for tool in ("node", "npm"):
    p = shutil.which(tool)
    line("OK" if p else "FALLO", f"{tool}: {run(tool + ' -v') if p else 'no encontrado'}")
edge = glob.glob("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe") + glob.glob("C:/Program Files/Microsoft/Edge/Application/msedge.exe")
line("OK" if edge else "AVISO", "Edge (capturas headless): " + (edge[0] if edge else "no encontrado"))
chrome = (glob.glob("C:/Program Files/Google/Chrome/Application/chrome.exe") + glob.glob("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
          + glob.glob("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") + [p for p in [shutil.which("google-chrome"), shutil.which("chromium")] if p])
line("OK" if chrome else "FALLO", "Chrome (Claude in Chrome NO funciona en Arc): " + (chrome[0] if chrome else "no encontrado"))
try:
    import PIL  # noqa: F401
    line("OK", "Pillow disponible")
except Exception:
    line("AVISO", "Pillow no disponible (solo para QA de imágenes)")

if a.proyecto:
    base = a.proyecto
    cands = glob.glob(os.path.join(base, "**", "AGENTS.md"), recursive=True)
    cands = [c for c in cands if "node_modules" not in c and "_backup" not in c]
    line("OK" if cands else "AVISO", "AGENTS.md del constructor: " + (cands[0] if cands else "no encontrado (¿descargaste la base de código?)"))
    if cands:
        d = os.path.dirname(cands[0])
        line("OK" if os.path.exists(os.path.join(d, "README.md")) else "AVISO", "README.md del proyecto: " + ("presente" if os.path.exists(os.path.join(d, "README.md")) else "falta"))
        line("OK" if os.path.isdir(os.path.join(d, "..", "_backup-original")) else "AVISO", "Respaldo _backup-original junto al proyecto")

print("\nRECORDATORIO: nunca pulsar «Publicar» sin pedido; no usar Ctrl+S; verificar pestaña y primera línea antes de «Guardar».")
print("RESUMEN:", "hay FALLOS" if fails else "listo para trabajar")
sys.exit(1 if fails else 0)
