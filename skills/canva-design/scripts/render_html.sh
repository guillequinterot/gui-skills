#!/bin/bash
# render_html.sh — captura un HTML con Chrome headless (FIABLE; el panel del navegador integrado NO sirve:
# abre archivos locales como instantánea `data:` sin cargar imágenes relativas ni Google Fonts).
#
# Uso:  render_html.sh <archivo.html> <ancho> <alto_total> <salida.png>
#   p. ej. 3 páginas de 2000x1400 apiladas:  render_html.sh diplomas.html 2000 4200 out.png
#   luego: python -I split_pages.py out.png --w 2000 --h 1400 --prefix pag
# Llamar DIRECTO desde bash (desde subprocess de Python hubo capturas en blanco intermitentes con Edge).
set -e
HTML="$1"; W="$2"; H="$3"; OUT="$4"
[ -z "$OUT" ] && { echo "uso: render_html.sh <html> <ancho> <alto_total> <salida.png>"; exit 2; }
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
[ -x "$CHROME" ] || CHROME="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
ABS=$(cd "$(dirname "$HTML")" && pwd -W 2>/dev/null || pwd)/$(basename "$HTML")
URL="file:///$(echo "$ABS" | sed 's/ /%20/g')"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$W","$H" --virtual-time-budget=8000 --screenshot="$OUT" "$URL" 2>&1 | grep -i "written" || true
ls -la "$OUT" | awk '{print $5, $9}'
