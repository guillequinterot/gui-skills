#!/bin/bash
# temp_host.sh — alojamiento TEMPORAL y público para que Canva pueda importar un HTML por URL.
#
# ⚠ REQUIERE AUTORIZACIÓN EXPLÍCITA DEL USUARIO CADA VEZ (publica contenido en internet; la autorización
#   de una tarea no vale para la siguiente). Siempre: subir → importar → BORRAR → verificar 404 → avisar.
#
# Usa el acceso SSH por llave (sin passphrase) a un hosting propio del usuario. Sin tokens, claves, IPs ni usuarios en este archivo:
# todo sale de variables de entorno CANVA_TMP_* o de ~/.gui-skills/config.json (fuera del repo).
#
# Uso:
#   temp_host.sh upload  <slug> <carpeta_base> <archivo1> [archivo2 ...]   (rutas relativas a carpeta_base, se conserva la estructura)
#   temp_host.sh verify  <dir_remoto> <ruta1> [ruta2 ...]
#   temp_host.sh cleanup <dir_remoto>
#   temp_host.sh --dry-run ...   (solo imprime lo que haría)
#
# Notas aprendidas (2026-10-08):
#  - El importador necesita HTTPS con certificado VÁLIDO. Usar el dominio raíz del hosting (o uno con SSL válido); los subdominios de
#    prueba sin certificado fallan (curl error 60). Se sube a la raíz: https://<tu-dominio>/<dir>/
#  - Canva NO descarga las <img> del HTML, pero las imágenes sí deben estar públicas para `upload-asset-from-url`.
#  - Slug con sufijo aleatorio (no listable, no indexable). Borrar al terminar.
#  - v1.1 (2026-10-09): corregido el bug de subida con VARIOS archivos (tar recibia "$@" como un solo argumento). Las fuentes TTF no hace falta subirlas: el importador ignora @font-face.
CFG="$HOME/.gui-skills/config.json"
cfg() { python -I -c "import json,os,sys;print(json.load(open(os.path.expanduser(sys.argv[1]),encoding='utf-8')).get(sys.argv[2],''))" "$CFG" "$1" 2>/dev/null; }
KEY="${CANVA_TMP_HOST_KEY:-$(cfg canva_tmp_host_key)}"
HOST="${CANVA_TMP_HOST:-$(cfg canva_tmp_host)}"; PORT="${CANVA_TMP_PORT:-$(cfg canva_tmp_port)}"; RUSER="${CANVA_TMP_USER:-$(cfg canva_tmp_user)}"
DOMAIN="${CANVA_TMP_DOMAIN:-$(cfg canva_tmp_domain)}"; PORT="${PORT:-22}"
if [ -z "$KEY" ] || [ -z "$HOST" ] || [ -z "$RUSER" ] || [ -z "$DOMAIN" ]; then
  echo "Falta configurar el hosting temporal: define CANVA_TMP_HOST_KEY, CANVA_TMP_HOST, CANVA_TMP_USER, CANVA_TMP_DOMAIN (y CANVA_TMP_PORT)"
  echo "o las claves canva_tmp_host_key / canva_tmp_host / canva_tmp_user / canva_tmp_domain / canva_tmp_port en $CFG (fuera del repo)."
  [ "$1" = "--dry-run" ] || exit 4
fi
KEY="${KEY/#\~/$HOME}"
DRY=0; [ "$1" = "--dry-run" ] && { DRY=1; shift; }
SSH="ssh -o BatchMode=yes -o IdentitiesOnly=yes -i $KEY -p $PORT $RUSER@$HOST"
filter() { grep -v "post-quantum\|store now\|openssh.com/pq\|^\*\*"; }
run() { if [ $DRY = 1 ]; then echo "[dry-run] $*"; else eval "$@"; fi; }

case "$1" in
  upload)
    SLUG="$2"; BASE="$3"; shift 3
    [ -z "$SLUG" ] || [ -z "$BASE" ] || [ $# -eq 0 ] && { echo "uso: upload <slug> <carpeta_base> <archivos...>"; exit 2; }
    DIR="_tmp-${SLUG}-$(head -c 6 /dev/urandom | od -An -tx1 | tr -d ' \n' | head -c 6)"
    echo "DIR=$DIR"
    FILES=""; for f in "$@"; do FILES="$FILES \"$f\""; done   # cada archivo como argumento propio (v1.0 pasaba "$@" como UN argumento y la carpeta quedaba vacia)
    run "(cd \"$BASE\" && tar -cf - $FILES) | $SSH \"mkdir -p ~/public_html/$DIR && cd ~/public_html/$DIR && tar -xf - && chmod -R a+rX . && ls -R . | head -30\" 2>&1 | filter"
    echo "URL_BASE=$DOMAIN/$DIR/"
    ;;
  verify)
    DIR="$2"; shift 2
    for f in "$@"; do run "curl -s -o /dev/null -w \"$f -> %{http_code} %{content_type} %{size_download}\n\" \"$DOMAIN/$DIR/$f\""; done
    ;;
  cleanup)
    DIR="$2"; [ -z "$DIR" ] && { echo "uso: cleanup <dir_remoto>"; exit 2; }
    case "$DIR" in _tmp-*) ;; *) echo "por seguridad solo se borran carpetas que empiezan por _tmp-"; exit 3;; esac
    run "$SSH \"rm -rf ~/public_html/$DIR && ls ~/public_html | grep -c '^$DIR\$'\" 2>&1 | filter"
    run "curl -s -o /dev/null -w \"comprobación pública -> %{http_code} (debe ser 404)\n\" \"$DOMAIN/$DIR/\""
    ;;
  *) sed -n '2,20p' "$0"; exit 2;;
esac
