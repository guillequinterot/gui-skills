"""install.py — instala/actualiza el NÚCLEO de la skill en Claude Code (y opcionalmente Codex) y verifica por SHA-256.

  python -I install.py            # instala en ~/.claude/skills/canva-design
  python -I install.py --codex    # además ~/.codex/skills/canva-design
  python -I install.py --check    # solo compara fuente vs instalado

Núcleo = SKILL.md + references/ + scripts/ + templates/.  NO se instalan: ejemplos/, conocimiento/, memoria/, proyectos/,
HANDOFF.md, HANDSHAKE.md, CHANGELOG.md (viven solo en el repo).
En gui-skills la instalación normal la hace el instalador del repo (tools/install.ps1 / tools/install.sh), que ENLAZA
~/.claude/skills/canva-design al clon; este script sirve solo para instalar por copia fuera del repo o para --check.
La fuente canónica es SIEMPRE <repo>/skills/canva-design; no edites la copia instalada.
"""
import argparse, hashlib, os, shutil, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIRS = ("references", "scripts", "templates")


def files(root):
    out = ["SKILL.md"]
    for d in CORE_DIRS:
        for dp, dn, fn in os.walk(os.path.join(root, d)):
            dn[:] = [x for x in dn if x != "__pycache__"]
            for f in fn:
                if f.endswith(".pyc"): continue
                out.append(os.path.relpath(os.path.join(dp, f), root).replace("\\", "/"))
    return sorted(out)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sync(dst, check):
    if os.path.isdir(dst) and os.path.realpath(dst) == os.path.realpath(SRC):
        print(f"{dst}: instalada por enlace al repo (misma carpeta que la fuente): nada que copiar")
        return True
    rel = files(SRC); bad = 0
    for r in rel:
        s, d = os.path.join(SRC, r), os.path.join(dst, r)
        same = os.path.exists(d) and sha(s) == sha(d)
        if not same:
            bad += 1
            if not check:
                os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(s, d)
    # sobrantes en destino
    extra = [r for r in files(dst) if r not in rel] if os.path.isdir(dst) else []
    if not check:
        for r in extra: os.remove(os.path.join(dst, r))
    man = hashlib.sha256("".join(sha(os.path.join(SRC, r)) for r in rel).encode()).hexdigest()[:16]
    print(f"{dst}: {len(rel)} archivos · {'diferencias: ' + str(bad) if check else 'copiados: ' + str(bad)} · sobrantes: {len(extra)} · manifiesto {man}")
    return bad == 0 and not extra


ap = argparse.ArgumentParser(); ap.add_argument("--codex", action="store_true"); ap.add_argument("--check", action="store_true")
a = ap.parse_args()
targets = [os.path.expanduser("~/.claude/skills/canva-design")] + ([os.path.expanduser("~/.codex/skills/canva-design")] if a.codex else [])
allok = True
for t in targets:
    if a.check:
        allok &= sync(t, True)
    else:
        sync(t, False)                        # copia
        allok &= sync(t, True)                # verificación posterior (hash por archivo)
print("TODO OK" if allok else "HAY DIFERENCIAS")
sys.exit(0 if allok else 1)
