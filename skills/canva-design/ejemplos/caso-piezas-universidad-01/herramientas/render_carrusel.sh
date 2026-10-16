#!/bin/bash
# Renderiza carrusel-1080x1350.html de un programa (8 láminas) y crea previews/carrusel_N.png + 00-resumen-carrusel.jpg. Uso: bash render_carrusel.sh <carpeta>
set -e
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"; SK=~/.claude/skills/canva-design/scripts
HERE="$(cd "$(dirname "$0")" && pwd -W)"; P="$(cd "$HERE/../$1" && pwd -W)"; mkdir -p "$P/previews"
N=$(grep -c 'data-document-role="page"' "$P/carrusel-1080x1350.html")
UD="$(cygpath -w "$(mktemp -d)")"
"$CH" --user-data-dir="$UD" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,$((N*1350)) --virtual-time-budget=8000 --screenshot="$P/previews/carrusel.png" "file:///$(echo "$P/carrusel-1080x1350.html" | sed 's/ /%20/g')" >/dev/null 2>&1
python -I "$SK/split_pages.py" "$P/previews/carrusel.png" --w 1080 --h 1350 --prefix "$P/previews/carrusel" >/dev/null
python -I - "$P" <<'PY'
import sys,glob,os
from PIL import Image
P=sys.argv[1]; fs=sorted(glob.glob(P+'/previews/carrusel_[0-9]*.png'),key=lambda f:int(f.rsplit('_',1)[1][:-4]))
th=[Image.open(f).convert('RGB').resize((324,405)) for f in fs]
cols=4; rows=(len(th)+cols-1)//cols
sh=Image.new('RGB',(cols*334+10,rows*415+10),(28,28,28))
for i,t in enumerate(th): sh.paste(t,(10+(i%cols)*334,10+(i//cols)*415))
sh.save(P+'/previews/00-resumen-carrusel.jpg',quality=88); print(len(th),'láminas')
PY
