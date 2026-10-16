#!/usr/bin/env bash
# gui-skills installer for macOS/Linux. Idempotent: safe to run again.
set -eu

REPO_URL="https://github.com/guillequinterot/gui-skills.git"
REPO_DIR=""
ALIAS_ARG=""
HOME_DIR="${HOME:-}"
NO_HOOK=0

usage() {
  cat <<'USAGE'
Uso: bash tools/install.sh [opciones]

  --alias NOMBRE     tu alias (minúsculas, números, guion); si falta se pregunta
  --repo-dir RUTA    dónde está o dónde clonar el repo (por defecto: este clon, o ~/gui-skills)
  --repo-url URL     de dónde clonar si aún no existe (por defecto: GitHub guillequinterot/gui-skills)
  --home RUTA        usa otra carpeta como HOME (pruebas)
  --no-hook          no instala el aviso de actualización de SessionStart
  -h, --help         esta ayuda
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --alias) ALIAS_ARG="${2:-}"; shift 2 ;;
    --repo-dir) REPO_DIR="${2:-}"; shift 2 ;;
    --repo-url) REPO_URL="${2:-}"; shift 2 ;;
    --home) HOME_DIR="${2:-}"; shift 2 ;;
    --no-hook) NO_HOOK=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Opción desconocida: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[ -n "$HOME_DIR" ] || { echo "No encuentro la carpeta HOME." >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Falta git. Instálalo y vuelve a correr este script." >&2; exit 1; }

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SELF_ROOT=$(dirname "$SCRIPT_DIR")
if [ -z "$REPO_DIR" ]; then
  if [ -d "$SELF_ROOT/.git" ] && [ -d "$SELF_ROOT/skills" ]; then
    REPO_DIR="$SELF_ROOT"
  else
    REPO_DIR="$HOME_DIR/gui-skills"
  fi
fi
GUI_DIR="$HOME_DIR/.gui-skills"
SKILLS_DIR="$HOME_DIR/.claude/skills"
BACKUP="$GUI_DIR/backup-$(date +%Y%m%d-%H%M%S)"
BACKUP_MADE=0

say() { printf '%s\n' "$*"; }
ensure_backup() { if [ "$BACKUP_MADE" -eq 0 ]; then mkdir -p "$BACKUP"; BACKUP_MADE=1; fi; }
json_esc() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
    PY="$cand"; break
  fi
done

# 1. Clone
if [ -d "$REPO_DIR/.git" ]; then
  say "[1/6] Repo ya clonado en $REPO_DIR"
else
  if [ -e "$REPO_DIR" ] && [ -n "$(ls -A "$REPO_DIR" 2>/dev/null)" ]; then
    echo "$REPO_DIR existe y no es un clon de git. Elige otra ruta con --repo-dir." >&2; exit 1
  fi
  say "[1/6] Clonando $REPO_URL en $REPO_DIR"
  if ! git clone "$REPO_URL" "$REPO_DIR"; then
    echo "No se pudo clonar. Si ves 401/403, revisa la sección Credenciales del README." >&2; exit 1
  fi
fi
[ -d "$REPO_DIR/skills" ] || { echo "No hay carpeta skills/ en $REPO_DIR; ¿es el repo correcto?" >&2; exit 1; }
REPO_DIR=$(cd "$REPO_DIR" && pwd)

# 2. Private config (outside the repo)
mkdir -p "$GUI_DIR"
if [ -f "$GUI_DIR/config.json" ]; then
  say "[2/6] config.json ya existe (no se toca)"
else
  ALIAS_VAL="$ALIAS_ARG"
  if [ -z "$ALIAS_VAL" ]; then
    if [ -t 0 ]; then
      printf 'Tu alias (se usa en tus commits y ramas, p. ej. "ana"): '
      read -r ALIAS_VAL
    else
      echo "Falta --alias (no hay terminal para preguntar)." >&2; exit 1
    fi
  fi
  ALIAS_VAL=$(printf '%s' "$ALIAS_VAL" | tr '[:upper:] ' '[:lower:]-')
  if ! printf '%s' "$ALIAS_VAL" | grep -Eq '^[a-z0-9][a-z0-9_-]{1,30}$'; then
    echo "Alias inválido: usa 2 a 31 caracteres, minúsculas, números, guion o guion bajo." >&2; exit 1
  fi
  printf '{\n  "alias": "%s",\n  "repo_path": "%s"\n}\n' "$(json_esc "$ALIAS_VAL")" "$(json_esc "$REPO_DIR")" > "$GUI_DIR/config.json"
  say "[2/6] Creado $GUI_DIR/config.json (alias: $ALIAS_VAL)"
fi
if [ ! -f "$GUI_DIR/private-terms.txt" ]; then
  cat > "$GUI_DIR/private-terms.txt" <<'TERMS'
# Lista PRIVADA de términos que nunca deben entrar al repo gui-skills (vive solo en esta computadora).
# Una entrada por línea. Texto plano = coincidencia sin distinguir mayúsculas, palabra completa.
# Prefijo "re:" = expresión regular (Python), distingue mayúsculas.
# Las líneas que empiezan con # son comentarios.
#
# Ejemplos (bórralos y escribe los tuyos: tus clientes, marcas, personas, dominios):
# NombreDeUnCliente
# re:PROY-\d{3}
TERMS
  say "      Creada la plantilla $GUI_DIR/private-terms.txt (escribe ahí tus clientes y marcas)"
fi
if [ ! -f "$GUI_DIR/equivalencias.md" ]; then
  cat > "$GUI_DIR/equivalencias.md" <<'EQ'
# Equivalencias código de caso -> cliente (SOLO en esta computadora, nunca en el repo)

| Código de caso | Cliente / proyecto real |
|---|---|
EQ
fi

# 3. Link skills
say "[3/6] Enlazando skills en $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"
LINKED=0; KEPT=0
for dir in "$REPO_DIR"/skills/*/; do
  [ -d "$dir" ] || continue
  name=$(basename "$dir")
  src="${dir%/}"
  if [ ! -f "$src/SKILL.md" ]; then
    say "      - $name: sin SKILL.md, se omite"; continue
  fi
  target="$SKILLS_DIR/$name"
  if [ -L "$target" ]; then
    if [ "$(readlink "$target")" = "$src" ] || [ "$(cd "$target" 2>/dev/null && pwd -P)" = "$(cd "$src" && pwd -P)" ]; then
      say "      = $name: ya enlazada"; KEPT=$((KEPT + 1)); continue
    fi
    ensure_backup
    printf '%s -> %s\n' "$name" "$(readlink "$target")" >> "$BACKUP/enlaces-reemplazados.txt"
    rm "$target"
  elif [ -e "$target" ]; then
    ensure_backup
    mv "$target" "$BACKUP/$name"
    say "      * $name: copia anterior movida a $BACKUP/$name"
  fi
  ln -s "$src" "$target"
  if [ ! -L "$target" ]; then
    echo "No se pudo crear un enlace simbólico real en $target. En Windows usa tools/install.ps1." >&2; exit 1
  fi
  say "      + $name"; LINKED=$((LINKED + 1))
done

# 4. Git config
say "[4/6] Configurando git en el clon"
git -C "$REPO_DIR" config core.hooksPath .githooks
[ -f "$REPO_DIR/.githooks/pre-commit" ] && chmod +x "$REPO_DIR/.githooks/pre-commit"
if [ -z "$(git -C "$REPO_DIR" config --local --get user.name || true)" ]; then
  ALIAS_NOW=$(sed -n 's/.*"alias"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$GUI_DIR/config.json" | head -n 1)
  [ -n "$ALIAS_NOW" ] && git -C "$REPO_DIR" config user.name "$ALIAS_NOW"
fi
if [ -z "$(git -C "$REPO_DIR" config --local --get user.email || true)" ]; then
  ALIAS_NOW=$(sed -n 's/.*"alias"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$GUI_DIR/config.json" | head -n 1)
  [ -n "$ALIAS_NOW" ] && git -C "$REPO_DIR" config user.email "$ALIAS_NOW@gui-skills.local"
fi

# 5. SessionStart hook
if [ "$NO_HOOK" -eq 1 ]; then
  say "[5/6] Hook de actualización omitido (--no-hook)"
elif [ -z "$PY" ]; then
  say "[5/6] No encuentro Python 3.9+, omito el hook. Instala Python y vuelve a correr este script."
else
  say "[5/6] Hook SessionStart en $HOME_DIR/.claude/settings.json"
  "$PY" "$REPO_DIR/tools/settings_hook.py" --settings "$HOME_DIR/.claude/settings.json" \
    --python "$PY" --script "$REPO_DIR/tools/check_update.py" --backup-dir "$BACKUP"
fi

# 6. Summary
say "[6/6] Listo. Enlaces nuevos: $LINKED, ya correctos: $KEPT."
[ "$BACKUP_MADE" -eq 1 ] && say "Respaldos en: $BACKUP"
say ""
say "Falta un paso manual: abre $HOME_DIR/.claude/CLAUDE.md y pega el bloque de"
say "  $REPO_DIR/templates/CLAUDE-snippet.md"
say "(el instalador no edita tu CLAUDE.md). Después reinicia Claude Code."
