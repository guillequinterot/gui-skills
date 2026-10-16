"""install.py — comprueba/instala el NÚCLEO de la skill en Claude Code (y opcionalmente Codex) y verifica por SHA-256.

En el repo gui-skills la forma normal de instalar es enlazar la carpeta de la skill con `tools/install.ps1` / `tools/install.sh`
(así `git pull` actualiza la skill instalada sin copiar nada). Este script sirve para:

  python -I install.py --check    # ¿~/.claude/skills/rea-reverse-engineer es un enlace a esta carpeta, o una copia igual?
  python -I install.py --copy     # (alternativa sin enlaces) copia el núcleo a ~/.claude/skills/rea-reverse-engineer
  python -I install.py --codex    # además copia el núcleo a ~/.codex/skills/rea-reverse-engineer (Codex no usa enlaces del repo)

Núcleo = SKILL.md + references/ + scripts/ + templates/.  En una copia NO se incluyen: ejemplos/, conocimiento/, memoria/,
proyectos/, HANDOFF.md, HANDSHAKE.md, CHANGELOG.md (viven solo en el repo). La fuente canónica es SIEMPRE la carpeta del repo
(`<repo>/skills/rea-reverse-engineer`); no edites una copia instalada.
"""
import argparse, hashlib, os, shutil, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NAME = "rea-reverse-engineer"
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIRS = ("references", "scripts", "templates")


def files(root):
    out = ["SKILL.md"]
    for d in CORE_DIRS:
        for dp, dn, fn in os.walk(os.path.join(root, d)):
            dn[:] = [x for x in dn if x != "__pycache__"]
            for f in fn:
                if f.endswith(".pyc"):
                    continue
                out.append(os.path.relpath(os.path.join(dp, f), root).replace("\\", "/"))
    return sorted(out)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def is_link_to_src(dst):
    """True si dst resuelve (enlace simbólico / junction) a esta carpeta del repo."""
    try:
        return os.path.realpath(dst) == os.path.realpath(SRC)
    except OSError:
        return False


def sync(dst, check):
    if is_link_to_src(dst):
        print(f"{dst}: enlazada al repo ({SRC}) · nada que copiar")
        return True
    rel = files(SRC)
    bad = 0
    for r in rel:
        s, d = os.path.join(SRC, r), os.path.join(dst, r)
        if not (os.path.exists(d) and sha(s) == sha(d)):
            bad += 1
            if not check:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    extra = [r for r in files(dst) if r not in rel] if os.path.isdir(dst) else []
    if not check:
        for r in extra:
            os.remove(os.path.join(dst, r))
    man = hashlib.sha256("".join(sha(os.path.join(SRC, r)) for r in rel).encode()).hexdigest()[:16]
    print(f"{dst}: {len(rel)} archivos · {'diferencias: ' + str(bad) if check else 'copiados: ' + str(bad)} · sobrantes: {len(extra)} · manifiesto {man}")
    return bad == 0 and not extra


ap = argparse.ArgumentParser()
ap.add_argument("--codex", action="store_true", help="copiar también a ~/.codex/skills")
ap.add_argument("--copy", action="store_true", help="copiar a ~/.claude/skills en vez de enlazar")
ap.add_argument("--check", action="store_true", help="solo comparar fuente vs instalado")
a = ap.parse_args()
claude_t = os.path.expanduser(f"~/.claude/skills/{NAME}")
codex_t = os.path.expanduser(f"~/.codex/skills/{NAME}")
allok = True
if a.check or not (a.copy or a.codex):
    # modo por defecto: solo comprobar (la instalación normal la hace tools/install.*)
    allok &= sync(claude_t, True)
    if not allok:
        print("Sugerencia: corre tools/install.ps1 (o tools/install.sh) del repo para enlazar la skill, o usa --copy.")
else:
    targets = ([claude_t] if a.copy else []) + ([codex_t] if a.codex else [])
    for t in targets:
        sync(t, False)
        allok &= sync(t, True)
print("TODO OK" if allok else "HAY DIFERENCIAS")
sys.exit(0 if allok else 1)
