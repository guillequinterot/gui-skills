# -*- coding: utf-8 -*-
"""make_partes.py — arma las «partes» para copiar y pegar en el chat del constructor de GoHighLevel.

  python make_partes.py <config.json>

Lee los archivos REALES del proyecto local (la carpeta descargada del constructor y editada en local) y
escribe PARTE-n-de-N.txt en la carpeta de salida; cada parte ≤ 50 000 caracteres (límite del chat).
Sustituye a los generadores específicos de cada entrega: aquí todo lo propio del proyecto va en el JSON
(ver ejemplos/caso-web-universidad-01/partes.ejemplo.json).

Modos de cada archivo:
  crear       archivo NUEVO: se pega completo («CREA el archivo NUEVO…»)
  reemplazar  archivo existente: se pega completo («REEMPLAZA TODO el contenido…»)
  anexar      bloque AL FINAL de un archivo existente: desde la línea que contiene `desde` hasta el final
  bloque      reemplaza el tramo entre `desde` y `hasta` (sin incluir `hasta`)
  buscar      BUSCA el texto `buscar` y REEMPLÁZALO por `nuevo` (se comprueba que el local ya tiene `nuevo`)

Reglas que conviene mantener (salen de references/07): anexar en vez de reemplazar los archivos que la IA del
constructor también edita (p. ej. el de IMG_URLS); pedirle que compare con el actual antes de reemplazar;
medir CARACTERES, no bytes; la última parte lleva el cierre (comprobaciones + actualizar README.md).
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REGLAS_POR_DEFECTO = [
    "Aplica EXACTAMENTE estos cambios. No rediseñes, no cambies textos, no corrijas ortografía, no cambies nada más.",
    "Crea SOLO los archivos nuevos que se indican. Si por alguna razón no puedes crear un archivo, dímelo y dime cuál; no lo sustituyas por otro.",
    "No toques IMG_URLS, img() ni las imágenes. No toques archivos protegidos (routeTree.gen.ts, .env, vite.config.ts, start.ts, server.ts, integrations/*).",
    "Antes de reemplazar un archivo, compáralo con el actual: si el actual tiene cambios que NO están en este, dímelo y no los pises.",
    "No agregues dependencias.",
]


def leer(proyecto, ruta):
    with open(os.path.join(proyecto, ruta.replace("/", os.sep)), encoding="utf-8") as f:
        return f.read()


def bloque(proyecto, spec):
    f = spec["file"]
    txt = leer(proyecto, f)
    cab = "=" * 78 + "\nARCHIVO: %s\n%s\n" % (f, spec["nota"])
    modo = spec["modo"]
    if modo in ("crear", "reemplazar"):
        return cab + "=" * 78 + "\n" + txt.rstrip("\n") + "\n=== FIN DEL ARCHIVO %s ===\n" % f
    if modo == "anexar":
        i = txt.index(spec["desde"])
        return cab + "=" * 78 + "\n" + txt[i:].rstrip("\n") + "\n=== FIN DEL BLOQUE A AÑADIR (%s) ===\n" % f
    if modo == "bloque":
        i, j = txt.index(spec["desde"]), txt.index(spec["hasta"])
        return cab + "=" * 78 + "\n" + txt[i:j].rstrip("\n") + "\n=== FIN DEL BLOQUE (%s) ===\n" % f
    if modo == "buscar":
        assert spec["nuevo"] in txt, "el archivo local no tiene el cambio: %s" % f
        return cab + "BUSCA exactamente:\n" + spec["buscar"] + "\n\nY REEMPLÁZALO por:\n" + spec["nuevo"] + "\n"
    raise SystemExit("modo desconocido: %s" % modo)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    cfg_path = os.path.abspath(sys.argv[1])
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    base = os.path.dirname(cfg_path)
    proyecto = os.path.normpath(os.path.join(base, cfg["proyecto"]))
    salida = os.path.normpath(os.path.join(base, cfg["salida"]))
    limite = int(cfg.get("limite", 50000))
    titulo = cfg["titulo"]
    reglas = cfg.get("reglas") or REGLAS_POR_DEFECTO
    partes = cfg["partes"]
    n_total = len(partes)
    extras = cfg.get("texto_tras_parte", {})  # {"3": "ELIMINA ESTOS ARCHIVOS…"}
    os.makedirs(salida, exist_ok=True)

    regla_txt = "REGLAS (de AGENTS.md, no las rompas):\n" + "".join("- %s\n" % r for r in reglas)
    for n, specs in enumerate(partes, 1):
        cuerpo = "\n".join(bloque(proyecto, s) for s in specs)
        if n == 1:
            intro = ("%s\n\nPARTE 1 DE %d.\nVoy a mandarte %d partes con código ya escrito y verificado. Aplícalo tal cual.\n"
                     "Aún no hace falta revisar la vista previa: espera a la PARTE %d.\n\n" % (titulo, n_total, n_total, n_total))
        elif n < n_total:
            intro = "%s\n\nPARTE %d DE %d. Sigue aplicando tal cual (puede depender de la anterior).\n\n" % (titulo, n, n_total)
        else:
            intro = "%s\n\nPARTE %d DE %d (la última). Aplica estos cambios y luego haz el cierre.\n\n" % (titulo, n, n_total)
        cierre = ""
        if str(n) in extras:
            cierre += "\n" + "=" * 78 + "\n" + extras[str(n)] + "\n"
        if n == n_total:
            cierre += ("\n" + "=" * 78 + "\nCIERRE (obligatorio)\n" + "=" * 78 + "\n"
                       + "".join("%s\n" % linea for linea in cfg.get("cierre", [
                           "1. Comprueba en la vista previa lo que cambió y que no haya errores en consola.",
                           "2. Actualiza README.md como indica AGENTS.md §0 (estado, pendientes, entrada nueva en el registro).",
                           "3. Respóndeme con un resumen corto y dime si algo no coincidió."])))
        texto = intro + regla_txt + "\n" + cuerpo + cierre
        if len(texto) > limite:
            raise SystemExit("parte %d excede %d caracteres (%d): reparte los archivos en más partes" % (n, limite, len(texto)))
        with open(os.path.join(salida, "PARTE-%d-de-%d.txt" % (n, n_total)), "w", encoding="utf-8", newline="\n") as out:
            out.write(texto)
        print("PARTE", n, len(texto), "caracteres")


if __name__ == "__main__":
    main()
