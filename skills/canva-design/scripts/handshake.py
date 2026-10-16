"""handshake.py — comprueba en 5 segundos lo que se puede verificar LOCALMENTE antes de trabajar en Canva.

  python -I handshake.py

Lo que NO puede comprobar (las herramientas MCP viven en la sesión): imprime la lista exacta para cargar con
ToolSearch y la prueba mínima de cada una. Ver HANDSHAKE.md.
"""
import importlib, os, shutil, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = lambda b: "OK " if b else "FALTA"
rows = []


def chk(name, cond, hint=""):
    rows.append((name, cond, hint)); print(f"[{ok(cond)}] {name}" + (f"  — {hint}" if (hint and not cond) else ""))


print("== Python y librerías ==")
chk("Python >= 3.10", sys.version_info >= (3, 10), sys.version.split()[0])
for m, pip in (("fitz", "pymupdf"), ("PIL", "pillow"), ("numpy", "numpy"), ("scipy", "scipy")):
    try:
        importlib.import_module(m); chk(f"módulo {m}", True)
    except Exception:
        chk(f"módulo {m}", False, f"pip install {pip}")

print("\n== Navegador headless (render del HTML) ==")
chromes = ["C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"]
chk("Chrome o Edge", any(os.path.exists(c) for c in chromes), "instalar Chrome; el panel del navegador integrado NO sirve para renderizar archivos locales")

print("\n== Hosting temporal (solo si el usuario lo autoriza) ==")
# Configuración del hosting temporal: variables de entorno CANVA_TMP_* o ~/.gui-skills/config.json
# (claves canva_tmp_host_key, canva_tmp_host, canva_tmp_port, canva_tmp_user, canva_tmp_domain). Nada de esto va al repo.
def _cfg(k):
    try:
        import json
        return json.load(open(os.path.expanduser("~/.gui-skills/config.json"), encoding="utf-8")).get(k, "")
    except Exception:
        return ""
key = os.path.expanduser(os.environ.get("CANVA_TMP_HOST_KEY") or _cfg("canva_tmp_host_key") or "")
if key and os.path.exists(key):
    chk("llave SSH del hosting temporal", True)
else:
    print("[AVISO] hosting temporal sin configurar (CANVA_TMP_HOST_KEY o canva_tmp_host_key en ~/.gui-skills/config.json): sin hosting propio no se puede importar por URL (ver references/03)")
chk("ssh/tar/curl en PATH", all(shutil.which(x) for x in ("ssh", "tar", "curl")))

print("\n== Skill y conocimiento ==")
for p in ("SKILL.md", "references/01-pipeline-html-a-canva.md", "scripts/bake_assets.py", "templates/diploma-20x14.template.html"):
    chk(p, os.path.exists(os.path.join(SKILL, p)))
chk("caso modelo (references/07)", os.path.exists(os.path.join(SKILL, "references", "07-caso-diplomas-01.md")))
vault = _cfg("obsidian_vault")
if vault:  # Obsidian es opcional: solo se comprueba si el usuario lo configuró
    chk("vault de Obsidian (opcional)", os.path.isdir(os.path.expanduser(vault)), "registrar además allí el cambio de herramienta")
chk("skill instalada en Claude Code", os.path.exists(os.path.expanduser("~/.claude/skills/canva-design/SKILL.md")), "python -I scripts/install.py")

print("""
== Herramientas Canva MCP (verificar EN LA SESIÓN; son 'deferred' → ToolSearch antes de usarlas) ==
  ToolSearch  canva      (busca por la palabra; el id del conector depende de tu cuenta). O, con el id de tu conector:
  ToolSearch  select:mcp__<id-del-conector>__import-design-from-url,
              mcp__<id-del-conector>__upload-asset-from-url,
              mcp__<id-del-conector>__read-design,
              mcp__<id-del-conector>__edit-design,
              mcp__<id-del-conector>__merge-designs,
              mcp__<id-del-conector>__export-design,
              mcp__<id-del-conector>__resolve-shortlink
  (el id del servidor puede cambiar entre cuentas y sesiones: si el select no encuentra nada, usa la búsqueda por la palabra 'canva')
  Prueba mínima: resolve-shortlink / read-design sobre un diseño conocido  → si responde, el conector está vivo.
  Pruebas no ejercitadas aún: ver HANDSHAKE.md 'NO verificado'.
""")
bad = [r for r in rows if not r[1]]
print(f"Resumen: {len(rows) - len(bad)}/{len(rows)} OK" + ("" if not bad else f" · faltan: {', '.join(r[0] for r in bad)}"))
sys.exit(1 if bad else 0)
