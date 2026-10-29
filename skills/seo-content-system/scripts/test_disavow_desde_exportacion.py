"""Prueba de disavow_desde_exportacion.py con un CSV falso (sin red). Ejecutar: python -I test_disavow_desde_exportacion.py"""
import os, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
fallos = 0


def ok(c, n):
    global fallos
    print(("OK    " if c else "FALLA ") + n)
    fallos += 0 if c else 1


with tempfile.TemporaryDirectory() as t:
    csvp = os.path.join(t, "e.csv")
    open(csvp, "w", encoding="utf-8").write(
        "Referring page URL,Anchor,Nofollow\n"
        "https://www.mejores-backlinks-seo.shop/p1,High Quality Dofollow Backlinks DA 50 PA 40 Premium PBN,true\n"
        "https://mejores-backlinks-seo.shop/p2,High Quality Dofollow Backlinks DA 50 PA 40 Premium PBN,true\n"
        "https://blog.ejemplo-editorial.com/articulo,mi diseñador favorito,false\n"
        "https://tiendita.xyz/a,ver sitio,false\n")
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "disavow_desde_exportacion.py"), csvp, "--salida", t], capture_output=True, text=True, encoding="utf-8")
    ok(r.returncode == 0, "se ejecuta sin error")
    d = open(os.path.join(t, "disavow.txt"), encoding="utf-8").read()
    rv = open(os.path.join(t, "revision.csv"), encoding="utf-8").read()
    ok("domain:mejores-backlinks-seo.shop" in d, "la granja evidente va al archivo de desautorizacion (agrupada por dominio, sin www)")
    ok("ejemplo-editorial.com" not in d, "un sitio editorial no se desautoriza")
    ok("tiendita.xyz,1,media" in rv and "tiendita.xyz" not in d, "una señal debil queda en revision (media), no en el archivo")
print("\nRESULTADO:", "TODO CORRECTO" if fallos == 0 else "%d fallo(s)" % fallos)
sys.exit(1 if fallos else 0)
