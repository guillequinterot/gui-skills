#!/bin/bash
# Renderiza los 3 HTML del programa indicado (por defecto 01-programa) con Chrome headless y corta las paginas.
# Uso: bash render_programa.sh [carpeta-programa]    (ruta ABSOLUTA interna: Chrome no resuelve rutas relativas)
set -e
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
SK=~/.claude/skills/canva-design/scripts
HERE="$(cd "$(dirname "$0")" && pwd -W)"
PROG="${1:-01-programa}"
P="$(cd "$HERE/../$PROG" && pwd -W)"
mkdir -p "$P/previews"
shot(){ UD="$(cygpath -w "$(mktemp -d)")"; "$CH" --user-data-dir="$UD" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=$2,$3 --virtual-time-budget=8000 --screenshot="$P/previews/$4.png" "file:///$(echo "$P/$1" | sed 's/ /%20/g')" 2>&1 | grep -i written >/dev/null; }
shot post-1080x1080.html 1080 2160 post;      python -I "$SK/split_pages.py" "$P/previews/post.png" --w 1080 --h 1080 --prefix "$P/previews/post"
shot historia-1080x1920.html 1080 3840 historia; python -I "$SK/split_pages.py" "$P/previews/historia.png" --w 1080 --h 1920 --prefix "$P/previews/historia"
shot banner-1200x628.html 1200 1256 banner;   python -I "$SK/split_pages.py" "$P/previews/banner.png" --w 1200 --h 628 --prefix "$P/previews/banner"
