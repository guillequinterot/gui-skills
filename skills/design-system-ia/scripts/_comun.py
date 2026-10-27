"""_comun.py — utilidades compartidas por los scripts de design-system-ia (solo biblioteca estándar).

Reglas de todos los scripts:
  - Sin dependencias externas (Python 3.9 o superior).
  - Aceptan saltos de línea de Windows (CRLF) y BOM al leer.
  - Salida en UTF-8 aunque la consola de Windows use otra codificación.
  - Código de salida 0 = sin hallazgos; 1 = hay hallazgos; 2 = uso incorrecto o archivo ilegible.
"""
import json
import os
import sys

SALIDA_OK = 0
SALIDA_HALLAZGOS = 1
SALIDA_USO = 2

# Los scripts NO comparan contra el estándar completo: cada uno declara qué comprueba y qué no.


def configurar_salida():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass


def leer_texto(ruta):
    """Lee un archivo de texto: UTF-8 con o sin BOM, CRLF o LF."""
    with open(ruta, "rb") as f:
        datos = f.read()
    try:
        texto = datos.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = datos.decode("latin-1")
    return texto.replace("\r\n", "\n").replace("\r", "\n")


def leer_json(ruta):
    return json.loads(leer_texto(ruta))


def listar_archivos(rutas, extensiones):
    """Expande archivos y carpetas (recursivo) filtrando por extensión; ignora carpetas de dependencias."""
    ignorar = {"node_modules", ".git", "__pycache__", "dist", "build", ".astro", ".next"}
    salida = []
    for ruta in rutas:
        if os.path.isdir(ruta):
            for base, carpetas, archivos in os.walk(ruta):
                carpetas[:] = [c for c in carpetas if c not in ignorar]
                for nombre in sorted(archivos):
                    if nombre.lower().endswith(tuple(extensiones)):
                        salida.append(os.path.join(base, nombre))
        elif os.path.isfile(ruta):
            salida.append(ruta)
        else:
            raise FileNotFoundError(ruta)
    return salida


def esta_vacio_o_marcador(valor):
    """True si el valor sigue siendo un marcador de plantilla («<...>» o «GENERADO»)."""
    if not isinstance(valor, str):
        return False
    v = valor.strip()
    return (v.startswith("<") and v.endswith(">")) or v.startswith("<GENERADO") or "GENERADO:" in v
