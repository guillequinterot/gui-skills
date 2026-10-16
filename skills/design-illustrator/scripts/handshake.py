#!/usr/bin/env python
"""handshake.py — preflight de design-illustrator: ¿esta máquina puede ejecutar el proceso?

  python -I handshake.py [--font Poppins] [--port 18412]

Comprueba (solo lectura, no abre Illustrator ni modifica nada):
  1. Sistema: Windows (el control de Illustrator va por COM).
  2. Illustrator instalado (versiones en C:\\Program Files\\Adobe) y servidor COM registrado (Illustrator.Application).
  3. La fuente del diseño instalada en Windows (por defecto Poppins). SIN ella Illustrator sustituye la fuente al abrir.
  4. Python: PyMuPDF (fitz), Pillow, numpy, playwright (+ chromium).
  5. MCP de Illustrator: puerto escuchando y si RESPONDE (POST de 4 s sin credenciales; no se imprime ningún token).
  6. Configuración de Claude: si el servidor 'illustrator' está registrado en ~/.claude.json.
Imprime OK / AVISO / FALLO por línea y un resumen. Código de salida 1 si hay algún FALLO.
"""
import argparse
import glob
import json
import os
import platform
import socket
import sys
import urllib.request

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


def main():
    global fails
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default="Poppins")
    ap.add_argument("--port", type=int, default=18412)
    a = ap.parse_args()

    if platform.system() == "Windows":
        line("OK", "Windows (COM disponible)")
    else:
        line("FALLO", f"{platform.system()}: el proceso usa COM de Windows; en macOS habría que portarlo a AppleScript/JXA")

    vers = sorted(glob.glob(r"C:\Program Files\Adobe\Adobe Illustrator*"))
    if vers:
        line("OK", "Illustrator instalado: " + ", ".join(os.path.basename(v) for v in vers))
        if any("Beta" in v for v in vers):
            line("AVISO", "Hay una versión Beta: COM puede arrancar la Beta (v31) en vez de la estable; comprobar con app.version")
    else:
        line("FALLO", "No se encontró Illustrator en C:\\Program Files\\Adobe")
    try:
        import winreg
        winreg.CloseKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Illustrator.Application"))
        line("OK", "Servidor COM 'Illustrator.Application' registrado")
    except Exception:
        line("FALLO", "COM 'Illustrator.Application' no registrado (abrir Illustrator una vez como usuario normal)")

    fonts_dirs = [r"C:\Windows\Fonts", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")]
    found = [f for d in fonts_dirs for f in glob.glob(os.path.join(d, "*")) if a.font.lower() in os.path.basename(f).lower()]
    # La fuente también puede venir de Adobe Fonts (Creative Cloud): no deja archivos con su nombre. Si Illustrator ya está abierto,
    # se le pregunta por COM (no se lanza Illustrator desde aquí).
    in_ai = None
    try:
        import subprocess
        running = "Illustrator.exe" in subprocess.run(["tasklist"], capture_output=True, text=True).stdout
        if running:
            ps = ("$ai = New-Object -ComObject Illustrator.Application; try { $null = $ai.DoJavaScript(\"app.textFonts.getByName('%s-Regular').name\"); 'SI' } catch { 'NO' }" % a.font)
            out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=60).stdout.strip()
            in_ai = out.endswith("SI")
    except Exception:
        pass
    if in_ai:
        line("OK", f"Fuente {a.font}-Regular disponible EN Illustrator" + (f" (+ {len(found)} archivos en Windows)" if found else " (Adobe Fonts u otra ruta)"))
    elif found:
        line("OK", f"Fuente {a.font} instalada en Windows ({len(found)} archivos)")
    elif in_ai is False:
        line("FALLO", f"Fuente {a.font} NO disponible en Illustrator: la sustituiría. Instalarla (Google Fonts o Adobe Fonts) y reiniciar Illustrator")
    else:
        line("AVISO", f"No se pudo comprobar la fuente {a.font}: no hay archivos en Windows y Illustrator no está abierto (si viene de Adobe Fonts es normal). Abrir Illustrator y repetir")

    for mod, pip in (("fitz", "PyMuPDF"), ("PIL", "Pillow"), ("numpy", "numpy"), ("playwright", "playwright")):
        try:
            __import__(mod)
            line("OK", f"Python: {pip}")
        except Exception:
            line("FALLO", f"Python: falta {pip} (pip install {pip})")

    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", a.port))
        line("OK", f"MCP de Illustrator: algo escucha en el puerto {a.port}")
        s.close()
        req = urllib.request.Request(f"http://127.0.0.1:{a.port}/v1/mcp", data=b'{"jsonrpc":"2.0","id":1,"method":"ping"}',
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=4) as r:
                line("OK", f"MCP responde (HTTP {r.status})")
        except urllib.error.HTTPError as e:
            line("OK", f"MCP responde (HTTP {e.code}: pide credenciales, normal)")
        except Exception as e:
            line("AVISO", f"MCP acepta conexión pero NO responde ({type(e).__name__}). Verificado el 2026-10-10: se queda colgado; usar COM (references/04)")
    except Exception:
        line("AVISO", f"MCP de Illustrator: nada escucha en {a.port} (activar «MCP y herramientas» en Illustrator si se quiere usar)")

    cfg = os.path.expanduser("~/.claude.json")
    try:
        d = json.load(open(cfg, encoding="utf-8"))
        names = list((d.get("mcpServers") or {}).keys())
        if any("illustrator" in n.lower() for n in names):
            line("OK", "Claude: servidor MCP de Illustrator registrado (alcance usuario)")
        else:
            line("AVISO", "Claude: MCP de Illustrator no registrado (ver references/04 para el comando; el token sale del panel «MCP y herramientas»)")
    except Exception:
        line("AVISO", "No se pudo leer ~/.claude.json")

    print("\nRESUMEN:", "TODO LISTO" if fails == 0 else f"{fails} FALLO(S): corregir antes de ejecutar el proceso")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
