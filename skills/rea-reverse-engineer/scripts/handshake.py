"""handshake.py — preflight de rea-reverse-engineer. Solo LEE: no instala ni cambia nada.

  python -I handshake.py [--json]

Comprueba: Node (vs. mínimo de REA), CLI `rea`, npx, navegador (Chrome/Edge), Python+Playwright,
registro de REA como MCP en Claude, skill instalada y enrutamiento desde otras skills.
"""
import json, os, re, shutil, subprocess, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HOME = os.path.expanduser("~")
REA_NODE_RANGES = [(22, 19), (24, 11)]  # ^22.19 || ^24.11 || >=26


def run(cmd, t=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=t, shell=False)
        return (r.stdout or r.stderr).strip()
    except Exception as e:
        return None


def node_ok(v):
    m = re.match(r"v?(\d+)\.(\d+)", v or "")
    if not m:
        return None
    M, n = int(m.group(1)), int(m.group(2))
    if M >= 26:
        return True
    return any(M == a and n >= b for a, b in REA_NODE_RANGES)


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def main():
    res = {}
    # Node portátil (REA exige >=22.19): se busca en ~/.claude/mcp-servers/node-v24*-<plataforma>/ (Windows: node.exe; Mac/Linux: bin/node)
    import glob
    cands = glob.glob(os.path.join(HOME, ".claude", "mcp-servers", "node-v24*", "node.exe")) + glob.glob(os.path.join(HOME, ".claude", "mcp-servers", "node-v24*", "bin", "node"))
    portable = sorted(cands)[-1] if cands else os.path.join(HOME, ".claude", "mcp-servers", "node-v24.<x>-<plataforma>", "node.exe")
    nv = run(["node", "-v"])
    pv = run([portable, "-v"]) if os.path.exists(portable) else None
    res["node"] = {"version": nv, "cumple_minimo_de_REA": node_ok(nv), "portatil_para_REA": pv, "portatil_cumple": node_ok(pv), "nota": "REA exige ^22.19 || ^24.11 || >=26; el MCP usa el Node portátil"}
    res["npx"] = bool(shutil.which("npx") or shutil.which("npx.cmd"))
    res["rea_cli_en_PATH"] = shutil.which("rea") or shutil.which("rea.cmd")
    chrome = [p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                          "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/chromium") if os.path.exists(p)]
    res["navegadores"] = chrome
    try:
        import playwright  # noqa
        res["playwright"] = getattr(playwright, "__version__", "sí")
    except Exception:
        res["playwright"] = None
    mcp = read(os.path.join(HOME, ".claude", "mcp.json")) + read(os.path.join(HOME, ".claude.json"))
    res["rea_registrado_como_MCP"] = bool(re.search(r'"rea(-agents)?"\s*:', mcp)) or "rea-agents" in mcp
    res["skill_rea_upstream_instalada"] = os.path.isdir(os.path.join(HOME, ".claude", "skills", "reverse-engineer-anything"))
    inst = os.path.join(HOME, ".claude", "skills", "rea-reverse-engineer")
    res["esta_skill_instalada"] = os.path.isfile(os.path.join(inst, "SKILL.md"))
    route = {}
    for n in ("direct-visual-design", "seo-content-system", "video-editing-ai-agent"):
        route[n] = "rea-reverse-engineer" in read(os.path.join(HOME, ".claude", "skills", n, "SKILL.md"))
    res["enrutamiento_instalado"] = route
    res["claude_md_global"] = "rea-reverse-engineer" in read(os.path.join(HOME, ".claude", "CLAUDE.md"))
    niveles = {"N0": True, "N1": bool(chrome) and bool(res["playwright"]),
               "N2": bool(res["rea_registrado_como_MCP"] or res["rea_cli_en_PATH"]) and (bool(res["node"]["cumple_minimo_de_REA"]) or bool(res["node"]["portatil_cumple"])),
               "N3": False}
    res["niveles_disponibles"] = niveles
    if a_json := ("--json" in sys.argv):
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    print("== rea-reverse-engineer · handshake ==")
    for k, v in res.items():
        print(f"- {k}: {v}")
    print("\nN3 nunca se marca disponible: depende del motor por objetivo (Ghidra/JADX…) y se decide por tarea.")
    if not niveles["N2"]:
        print("N2 no disponible: REA no está conectado (o Node < mínimo). Registrarlo requiere aprobación del usuario (references/04).")


if __name__ == "__main__":
    main()
