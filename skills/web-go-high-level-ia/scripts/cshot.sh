#!/bin/bash
# Captura con Chrome headless y perfil propio (Edge falla si el usuario ya tiene Edge abierto).
#
# Uso:  cshot.sh URL ANCHO ALTO SALIDA.png [CARPETA_DE_TRABAJO]
#   CARPETA_DE_TRABAJO  por defecto ${TMPDIR:-/tmp}/gui-skills-cshot ; ahí quedan chromeprof/ y shots/.
#   CHROME              variable de entorno opcional con la ruta a chrome (o chromium).
# Nota: Chrome headless no baja de ~500 px de ancho de ventana; para móvil usa scripts/overflow.html
# o un iframe del ancho exacto (ver references/07, F7 y K6).
set -u
URL="${1:?falta URL}"; W="${2:?falta ANCHO}"; H="${3:?falta ALTO}"; OUT="${4:?falta SALIDA}"
SC="${5:-${TMPDIR:-/tmp}/gui-skills-cshot}"
mkdir -p "$SC/shots"

if [ -n "${CHROME:-}" ]; then C="$CHROME"
else
  C=""
  for cand in \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$(command -v google-chrome 2>/dev/null)" "$(command -v chromium 2>/dev/null)"; do
    [ -n "$cand" ] && [ -x "$cand" ] && { C="$cand"; break; }
  done
fi
[ -n "$C" ] || { echo "No encuentro Chrome; define la variable CHROME." >&2; exit 1; }

# En Git Bash (Windows) Chrome necesita rutas de Windows; en otros sistemas, rutas normales.
win() { if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi; }

"$C" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$W,$H" --user-data-dir="$(win "$SC/chromeprof")" --virtual-time-budget=25000 \
  --screenshot="$(win "$SC/shots/$OUT")" "$URL" >/dev/null 2>&1
ls -la "$SC/shots/$OUT" | awk '{print $5, $9}'
