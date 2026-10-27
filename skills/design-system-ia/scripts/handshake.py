"""handshake.py — comprueba en segundos lo que se puede verificar LOCALMENTE antes de trabajar con design-system-ia.

  python -I handshake.py            # revisa Python, archivos de la skill y scripts
  python -I handshake.py --probar   # además ejecuta las pruebas de los scripts (unittest, sin dependencias)

Lo que NO puede comprobar (vive en la sesión del agente): imprime la lista exacta. Ver HANDSHAKE.md.
Salida: 0 si todo lo local está en orden; 1 si falta algo.
"""
import os
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filas = []


def chk(nombre, cond, pista=""):
    filas.append((nombre, cond))
    print(f"[{'OK   ' if cond else 'FALTA'}] {nombre}" + (f"  — {pista}" if pista and not cond else ""))


def main():
    probar = "--probar" in sys.argv[1:]
    print("== Python ==")
    chk("Python >= 3.9", sys.version_info >= (3, 9), sys.version.split()[0])

    print("\n== Skill ==")
    for p in ("SKILL.md", "HANDOFF.md", "HANDSHAKE.md"):
        chk(p, os.path.exists(os.path.join(SKILL, p)))
    refs = ["01-contrato", "02-tokens-y-nombres", "03-vocabulario-de-props", "04-documentacion-y-entrega",
            "05-figma", "06-listo-para-ia", "07-medicion", "08-gobierno-accesibilidad-estado", "09-arranque-y-operacion"]
    for r in refs:
        chk(f"references/{r}.md", os.path.exists(os.path.join(SKILL, "references", r + ".md")))
    chk("templates/INDICE.md", os.path.exists(os.path.join(SKILL, "templates", "INDICE.md")))
    for s in ("_comun.py", "validar_contrato.py", "contraste.py", "vocabulario_check.py", "comparar_figma_contrato.py", "generar_biblioteca.py", "extraer_modulo.py",
              "contrato.schema.json", "install.py"):
        chk(f"scripts/{s}", os.path.exists(os.path.join(SKILL, "scripts", s)))

    print("\n== Herramientas opcionales ==")
    print("[info ] git: " + ("disponible" if shutil.which("git") else "no está en el PATH (solo hace falta para medir frescura con el historial)"))
    print("[info ] navegador headless / Playwright: NO se usan en esta versión; el cálculo de estado y las pruebas de teclado no existen aún")

    if probar:
        print("\n== Pruebas de los scripts ==")
        res = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", os.path.join(SKILL, "scripts", "tests"), "-p", "test_*.py"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        ultimas = [l for l in (res.stderr or res.stdout).strip().splitlines() if l][-3:]
        for l in ultimas:
            print("   " + l)
        chk("pruebas de los scripts", res.returncode == 0, "ver la salida de arriba")

    print("""
== Lo que se verifica EN LA SESIÓN (no desde aquí) ==
  Figma (solo lectura): cargar figma:figma-use ANTES de cualquier use_figma; los MCP son 'deferred' → ToolSearch.
     Prueba mínima: use_figma de solo lectura sobre un archivo conocido (listar colecciones y modos).
     Escribir en Figma exige previsualizar y recibir la aprobación del usuario.
  Publicación (hosting, Drive, Figma): la skill SIEMPRE pregunta el destino; el hosting exige la autorización de
     cpanel-guillequinterot / ftp-los-creativos por tarea.
  Obsidian (opcional): su MCP puede estar caído; en ese caso se edita la nota directamente y se declara.
  No existe todavía: cálculo automático del estado de un componente, pruebas de teclado ni evaluaciones con IA.
""")
    malos = [n for n, ok in filas if not ok]
    print(f"Resumen: {len(filas) - len(malos)}/{len(filas)} OK" + ("" if not malos else f" · faltan: {', '.join(malos)}"))
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
