#!/usr/bin/env python3
"""install_agente.py — instala (enlaza o copia) las skills de gui-skills en la carpeta de skills de OTRA IA y comprueba que están al día.

Para quién: Codex, Grokbot, Gemini/Antigravity, Cursor o cualquier agente que lea skills como carpetas con un SKILL.md.
Claude Code se instala con tools/install.ps1 o tools/install.sh (también configura el aviso de actualización); este script
solo enlaza las carpetas y sirve igual para Claude cuando no se quiere tocar su configuración.

  python tools/install_agente.py --agente codex            # enlaza en ~/.codex/skills (o $CODEX_HOME/skills)
  python tools/install_agente.py --agente claude           # enlaza en ~/.claude/skills
  python tools/install_agente.py --destino RUTA            # otra IA: ruta de SU carpeta de skills
  python tools/install_agente.py --destino RUTA --copiar   # copia en vez de enlazar (la IA o el sistema no admite enlaces)
  python tools/install_agente.py --agente codex --check    # solo informa; código 1 si algo falta o está desactualizado
  python tools/install_agente.py --agente codex --dry-run  # muestra qué haría

Qué hace
  - Recorre skills/*/ del repo (las que tienen SKILL.md). No instala `seo-content-system-web-hosted`: es la versión GENERADA para
    ChatGPT (Project o GPT personalizado), no una skill de agente; se incluye con --incluir-alojada.
  - Enlaza cada skill en la carpeta de la IA (junction en Windows, enlace simbólico en Mac/Linux). Si ya había una CARPETA real con
    ese nombre, la mueve a ~/.gui-skills/backup-<fecha>/<destino>/ antes de enlazar. Si ya era un enlace a otro sitio, lo reapunta.
  - Con --copiar copia la carpeta (sin .git, __pycache__, node_modules ni investigación local): para actualizar hay que traer
    los cambios del repo (check_update.py --pull) y volver a correr este script.
  - Es idempotente: correrlo de nuevo no rompe nada.

Qué NO hace: no guarda credenciales, no toca configuraciones de la IA, no instala hooks ni servidores MCP, no sube nada.
Para ver si el repo está al día: python tools/check_update.py --quiet --pull   (ver shared/protocolo-skill.md).

Salida: una línea por skill (ENLAZADA, COPIADA, YA_OK, RESPALDADA, REAPUNTADA, DESACTUALIZADA, FALTA, ERROR) y un resumen.
Código de salida: 0 todo bien · 1 algo falta o falló · 2 uso incorrecto. Solo biblioteca estándar (Python 3.9 o superior).
"""
import argparse
import datetime
import filecmp
import os
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUIR_COPIA = {".git", "__pycache__", "node_modules", "investigacion", "referencia-helixds"}
NO_INSTALABLES = {"seo-content-system-web-hosted"}


def destino_de(agente):
    home = os.path.expanduser("~")
    if agente == "claude":
        return os.path.join(home, ".claude", "skills")
    if agente == "codex":
        return os.path.join(os.environ.get("CODEX_HOME") or os.path.join(home, ".codex"), "skills")
    return None


def skills_del_repo(repo, incluir_alojada, elegidas):
    base = os.path.join(repo, "skills")
    if not os.path.isdir(base):
        raise FileNotFoundError(f"no existe {base}: ¿es la carpeta del repo gui-skills?")
    out = []
    for n in sorted(os.listdir(base)):
        if not os.path.isfile(os.path.join(base, n, "SKILL.md")):
            continue
        if n in NO_INSTALABLES and not incluir_alojada:
            continue
        if elegidas and n not in elegidas:
            continue
        out.append(n)
    if elegidas:
        faltan = [n for n in elegidas if n not in out]
        if faltan:
            raise FileNotFoundError("skills que no existen en el repo (o no son instalables): " + ", ".join(faltan))
    return out


def es_enlace(ruta):
    """True si ruta es un enlace simbólico o una junction (no una carpeta real)."""
    if os.path.islink(ruta):
        return True
    isj = getattr(os.path, "isjunction", None)
    if isj and isj(ruta):
        return True
    return os.name == "nt" and os.path.exists(ruta) and os.path.realpath(ruta).lower() != os.path.abspath(ruta).lower()


def mismo_sitio(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def quitar_enlace(ruta):
    try:
        os.unlink(ruta)
    except OSError:
        os.rmdir(ruta)


def crear_enlace(fuente, ruta):
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", ruta, fuente], capture_output=True)
        if r.returncode != 0:
            raise OSError((r.stderr or r.stdout).decode("utf-8", errors="replace").strip() or "mklink falló")
    else:
        os.symlink(fuente, ruta, target_is_directory=True)


def copiar_arbol(fuente, ruta):
    def ignorar(_dir, nombres):
        return [n for n in nombres if n in EXCLUIR_COPIA or n.endswith(".pyc")]
    shutil.copytree(fuente, ruta, ignore=ignorar)


def arboles_iguales(a, b):
    """Compara dos carpetas por contenido, ignorando lo que no se copia."""
    def listar(r):
        out = {}
        for base, dirs, files in os.walk(r):
            dirs[:] = [d for d in dirs if d not in EXCLUIR_COPIA]
            for f in files:
                if f.endswith(".pyc"):
                    continue
                out[os.path.relpath(os.path.join(base, f), r)] = os.path.join(base, f)
        return out
    la, lb = listar(a), listar(b)
    if set(la) != set(lb):
        return False
    return all(filecmp.cmp(la[k], lb[k], shallow=False) for k in la)


def respaldar(ruta, destino, nombre, etiqueta):
    marca = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    carpeta = os.path.join(os.path.expanduser("~"), ".gui-skills", f"backup-{marca}", etiqueta)
    os.makedirs(carpeta, exist_ok=True)
    shutil.move(ruta, os.path.join(carpeta, nombre))
    return carpeta


def instalar_una(nombre, repo, destino, copiar, check, dry, etiqueta):
    fuente = os.path.join(repo, "skills", nombre)
    ruta = os.path.join(destino, nombre)
    existe = os.path.lexists(ruta)
    if existe and es_enlace(ruta):
        if mismo_sitio(ruta, fuente):
            if copiar and not check:
                # estaba enlazada y ahora se pide copia: se reemplaza el enlace por una copia
                if dry:
                    return "DRY", f"{nombre}: reemplazaría el enlace por una copia"
                quitar_enlace(ruta)
                copiar_arbol(fuente, ruta)
                return "COPIADA", nombre
            return "YA_OK", f"{nombre} (enlace al repo)"
        if check:
            return "DESACTUALIZADA", f"{nombre}: el enlace apunta a otro sitio ({os.path.realpath(ruta)})"
        if dry:
            return "DRY", f"{nombre}: reapuntaría el enlace"
        quitar_enlace(ruta)
        existe = False
        motivo = "REAPUNTADA"
    elif existe:
        if (copiar or check) and arboles_iguales(fuente, ruta):
            return "YA_OK", f"{nombre} (copia idéntica)"
        if check:
            return "DESACTUALIZADA", f"{nombre}: carpeta real distinta del repo (no es un enlace)"
        if dry:
            return "DRY", f"{nombre}: respaldaría la carpeta existente y la sustituiría"
        carpeta = respaldar(ruta, destino, nombre, etiqueta)
        existe = False
        motivo = "RESPALDADA"
        print(f"RESPALDADA {nombre} → {carpeta}")
    else:
        if check:
            return "FALTA", nombre
        if dry:
            return "DRY", f"{nombre}: la instalaría"
        motivo = None
    os.makedirs(destino, exist_ok=True)
    if copiar:
        copiar_arbol(fuente, ruta)
        return "COPIADA", nombre
    try:
        crear_enlace(fuente, ruta)
        return (motivo if motivo == "REAPUNTADA" else "ENLAZADA"), nombre
    except OSError as e:
        copiar_arbol(fuente, ruta)
        return "COPIADA", f"{nombre} (no se pudo enlazar: {e}; se copió: habrá que repetir este script tras cada actualización)"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Instala las skills de gui-skills en la carpeta de skills de otra IA.")
    ap.add_argument("--agente", choices=["claude", "codex"], help="IA con carpeta de skills conocida")
    ap.add_argument("--destino", help="carpeta de skills de cualquier otra IA (obligatoria si no se da --agente)")
    ap.add_argument("--repo", default=RAIZ, help="carpeta del clon de gui-skills (por defecto, la de este script)")
    ap.add_argument("--skills", help="lista separada por comas; por defecto, todas las instalables")
    ap.add_argument("--copiar", action="store_true", help="copiar en vez de enlazar")
    ap.add_argument("--check", action="store_true", help="solo informar (código 1 si algo falta o está desactualizado)")
    ap.add_argument("--dry-run", action="store_true", help="mostrar qué haría sin cambiar nada")
    ap.add_argument("--incluir-alojada", action="store_true", help="incluir seo-content-system-web-hosted (la versión generada para ChatGPT)")
    a = ap.parse_args(argv)
    destino = os.path.abspath(os.path.expanduser(a.destino)) if a.destino else (destino_de(a.agente) if a.agente else None)
    if not destino:
        ap.error("indica --agente claude|codex o --destino RUTA (la carpeta de skills de tu IA)")
    etiqueta = a.agente or os.path.basename(destino.rstrip("/\\")) or "otra"
    repo = os.path.abspath(os.path.expanduser(a.repo))
    try:
        nombres = skills_del_repo(repo, a.incluir_alojada, [s.strip() for s in a.skills.split(",")] if a.skills else [])
    except FileNotFoundError as e:
        print(f"ERROR {e}", file=sys.stderr)
        return 2
    cuentas = {}
    fallos = 0
    for n in nombres:
        try:
            estado, texto = instalar_una(n, repo, destino, a.copiar, a.check, a.dry_run, etiqueta)
        except Exception as e:  # noqa: BLE001
            estado, texto = "ERROR", f"{n}: {e}"
        cuentas[estado] = cuentas.get(estado, 0) + 1
        if estado in ("ERROR", "FALTA", "DESACTUALIZADA"):
            fallos += 1
        print(f"{estado} {texto}")
    resumen = " · ".join(f"{v} {k}" for k, v in sorted(cuentas.items()))
    print(f"\nDestino: {destino}\nResumen: {len(nombres)} skill(s): {resumen}")
    if not a.check and not a.dry_run and not fallos:
        print("Para actualizar después: python tools/check_update.py --quiet --pull" + ("  y vuelve a correr este script (copias)." if a.copiar else "  (los enlaces ya ven lo nuevo)."))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
