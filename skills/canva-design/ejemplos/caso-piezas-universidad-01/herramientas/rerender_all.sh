#!/bin/bash
# Re-renderiza los 36 programas (3 HTML c/u), regenera hojas resumen y corre el lint. Uso: bash rerender_all.sh [lista de carpetas]
cd "$(dirname "$0")"
SK=~/.claude/skills/canva-design/scripts
DIRS="$@"; [ -z "$DIRS" ] && DIRS=$(cd .. && ls -d [0-9][0-9]-*/ | tr -d '/')
for d in $DIRS; do
  bash render_programa.sh "$d" >/dev/null 2>&1
  python -I make_sheet.py "$d" >/dev/null 2>&1
  e=0
  for fm in "post-1080x1080 1080 1080" "historia-1080x1920 1080 1920" "banner-1200x628 1200 628"; do set -- $fm
    r=$(python -I $SK/lint_html_for_canva.py ../$d/$1.html --w $2 --h $3 2>&1 | grep -c "\[ERROR\]\|ERROR")
    e=$((e+r))
  done
  echo "$d lint_errores=$e"
done
echo FIN
