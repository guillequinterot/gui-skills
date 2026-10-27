"""vocabulario_check.py — busca sinónimos prohibidos en los ATRIBUTOS REALES de las etiquetas, no en texto suelto.

  python -I vocabulario_check.py --vocabulario vocabulario.md RUTA [RUTA...] [--contratos CARPETA]
                                 [--permitidos type,name] [--bloqueo]

Por qué atributos y no texto: en Helix, un script que busca el nombre como TEXTO dio 12 falsos positivos (la palabra
«default» dentro de un mensaje, «type» dentro de la configuración de un gráfico); la regla que mira atributos reales
atrapó 3 de 3 errores y dijo la alternativa (referencia 03, sección 6).

Qué hace
  1. Lee la tabla «Tabla del vocabulario» de vocabulario.md (columnas Canónico y Prohibidos; «→» marca la alternativa).
     Se ignoran las filas con marcadores de plantilla («<...>»).
  2. Recorre los archivos .html .htm .astro .jsx .tsx .vue .svelte .php .liquid .njk .md .mdx (carpetas, recursivo;
     se saltan node_modules, .git, dist, build, .astro, .next) y lee los atributos de cada etiqueta con un lector
     que respeta comillas y llaves (JSX: onClick={() => a > b} no rompe la etiqueta).
  3. Avisa cuando un atributo es un sinónimo prohibido y dice la alternativa.

Reglas (referencia 03, sección 6)
  - Etiquetas nativas en minúscula (div, button, input): solo se revisan los atributos data-* y aria-*; los demás son
    atributos HTML nativos y no se tocan.
  - Componentes (Mayúscula inicial, con punto o con guion): se revisan todos los atributos.
  - --contratos CARPETA: solo se avisa en componentes que tienen contrato Y declaran la prop canónica (si no la tienen,
    no hay nada que corregir). Los componentes sin contrato se ignoran salvo --incluir-sin-contrato.
  - --permitidos: nombres que son atributos nativos (type, name, title, readonly, open…) y no deben marcarse.
    También se leen de la tabla «Pasos permitidos» del vocabulario.
  - Acepta saltos de línea de Windows (CRLF).

Qué NO hace: no revisa VALORES (size="medium"), ni nombres de componentes, ni eventos escritos con addEventListener,
ni código generado en tiempo de ejecución; no corrige nada. «Sin hallazgos» significa solo que esos atributos no
aparecen en los archivos revisados.

Modo informe (por defecto): sale con 0 aunque haya hallazgos. Modo --bloqueo: sale con 1 si hay hallazgos.
Código 2: uso incorrecto o lectura imposible.
"""
import argparse
import bisect
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comun as c  # noqa: E402

EXTENSIONES = (".html", ".htm", ".astro", ".jsx", ".tsx", ".vue", ".svelte", ".php", ".liquid", ".njk", ".md", ".mdx")
NOMBRE_ATTR = re.compile(r"[A-Za-z_:@][\w:.@\-]*")
NOMBRE_ETIQUETA = re.compile(r"[A-Za-z][\w.:\-]*")
TOKEN = re.compile(r"`([^`]+)`")


# ---------------------------------------------------------------- lectura del vocabulario
def _celdas(linea):
    partes = linea.strip().strip("|").split("|")
    return [p.strip() for p in partes]


def _es_marcador(token):
    return "<" in token or ">" in token


def leer_vocabulario(texto):
    """Devuelve (prohibidos, permitidos). prohibidos: {nombre: [alternativas]}"""
    prohibidos, permitidos = {}, set()
    lineas = texto.split("\n")
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if linea.lstrip().startswith("|"):
            cabecera = _celdas(linea)
            bloque = []
            j = i + 1
            while j < len(lineas) and lineas[j].lstrip().startswith("|"):
                bloque.append(_celdas(lineas[j]))
                j += 1
            minus = [h.lower() for h in cabecera]
            if minus and minus[0].startswith("canónico") and len(minus) > 1 and minus[1].startswith("prohibidos"):
                for fila in bloque:
                    if len(fila) < 2 or set(fila[0]) <= set("-: "):
                        continue
                    canon = [t for t in TOKEN.findall(fila[0]) if not _es_marcador(t)]
                    for grupo in fila[1].split(";"):
                        antes, _, despues = grupo.partition("→")
                        nombres = [t for t in TOKEN.findall(antes) if not _es_marcador(t)]
                        alt = [t for t in TOKEN.findall(despues) if not _es_marcador(t)] or canon
                        for n in nombres:
                            if alt:
                                prohibidos.setdefault(n, [])
                                for a in alt:
                                    if a not in prohibidos[n]:
                                        prohibidos[n].append(a)
            elif minus and minus[0].startswith("nombre") and len(minus) > 1 and "permite" in " ".join(minus):
                for fila in bloque:
                    if fila and not set(fila[0]) <= set("-: "):
                        permitidos.update(t for t in TOKEN.findall(fila[0]) if not _es_marcador(t))
            i = j
        else:
            i += 1
    return prohibidos, permitidos


# ---------------------------------------------------------------- contratos (opcional)
def leer_contratos(carpeta):
    import json
    contratos = {}
    for ruta in c.listar_archivos([carpeta], (".json",)):
        if ruta.endswith(".schema.json"):
            continue
        try:
            d = json.loads(c.leer_texto(ruta))
        except Exception:  # noqa: BLE001
            continue
        if isinstance(d, dict) and d.get("name") and isinstance(d.get("props"), list):
            contratos[d["name"]] = {p.get("name") for p in d["props"] if isinstance(p, dict)}
    return contratos


# ---------------------------------------------------------------- lector de etiquetas
def _saltar_cadena(t, i):
    q = t[i]
    i += 1
    while i < len(t):
        if t[i] == "\\":
            i += 2
            continue
        if t[i] == q:
            return i + 1
        i += 1
    return -1


def _saltar_llaves(t, i):
    prof = 0
    while i < len(t):
        ch = t[i]
        if ch in "\"'`":
            i = _saltar_cadena(t, i)
            if i < 0:
                return -1
            continue
        if ch == "{":
            prof += 1
        elif ch == "}":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1
    return -1


def etiquetas(texto):
    """Genera (nombre_etiqueta, [(atributo, posicion)], posicion_inicio). Solo etiquetas bien formadas."""
    t = re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)), texto, flags=re.S)
    n = len(t)
    i = 0
    while True:
        i = t.find("<", i)
        if i < 0 or i + 1 >= n:
            return
        m = NOMBRE_ETIQUETA.match(t, i + 1)
        if not m or (i > 0 and t[i - 1] == "<"):
            i += 1
            continue
        nombre = m.group(0)
        j = m.end()
        if j < n and t[j] not in " \t\n/>":
            i += 1
            continue
        attrs, ok = [], False
        while j < n:
            while j < n and t[j] in " \t\n":
                j += 1
            if j >= n:
                break
            ch = t[j]
            if ch == ">":
                ok, j = True, j + 1
                break
            if ch == "/" and j + 1 < n and t[j + 1] == ">":
                ok, j = True, j + 2
                break
            if ch == "{":  # atributo extendido {...props}
                j = _saltar_llaves(t, j)
                if j < 0:
                    break
                continue
            ma = NOMBRE_ATTR.match(t, j)
            if not ma:
                break
            attrs.append((ma.group(0), j))
            j = ma.end()
            k = j
            while k < n and t[k] in " \t\n":
                k += 1
            if k < n and t[k] == "=":
                k += 1
                while k < n and t[k] in " \t\n":
                    k += 1
                if k >= n:
                    break
                if t[k] in "\"'":
                    k = _saltar_cadena(t, k)
                elif t[k] == "{":
                    k = _saltar_llaves(t, k)
                else:
                    while k < n and t[k] not in " \t\n>":
                        k += 1
                if k < 0:
                    break
                j = k
        if ok:
            yield nombre, attrs, i, t
            i = j
        else:
            i += 1


def es_componente(nombre):
    return nombre[0].isupper() or "." in nombre or "-" in nombre


# ---------------------------------------------------------------- revisión
def revisar_archivo(ruta, prohibidos, permitidos, contratos, incluir_sin_contrato):
    texto = c.leer_texto(ruta)
    saltos = [m.start() for m in re.finditer("\n", texto)]
    hallazgos = []
    for nombre, attrs, inicio, _t in etiquetas(texto):
        comp = es_componente(nombre)
        for attr, pos in attrs:
            if attr in permitidos or attr not in prohibidos:
                continue
            if not comp and not attr.startswith(("data-", "aria-")):
                continue
            alternativas = prohibidos[attr]
            if contratos is not None and comp:
                if nombre not in contratos:
                    if not incluir_sin_contrato:
                        continue
                else:
                    alternativas = [a for a in alternativas if a in contratos[nombre]]
                    if not alternativas:
                        continue
            linea = bisect.bisect_left(saltos, pos) + 1
            hallazgos.append((linea, nombre, attr, alternativas))
    return hallazgos


def main(argv=None):
    c.configurar_salida()
    ap = argparse.ArgumentParser(description="Sinónimos prohibidos en atributos reales.")
    ap.add_argument("rutas", nargs="+", help="archivos o carpetas a revisar")
    ap.add_argument("--vocabulario", required=True, help="vocabulario.md del proyecto")
    ap.add_argument("--contratos", help="carpeta con contratos JSON (solo avisa donde el componente declara la prop canónica)")
    ap.add_argument("--incluir-sin-contrato", action="store_true", help="con --contratos, revisa también componentes sin contrato")
    ap.add_argument("--permitidos", default="", help="atributos nativos que no se marcan, separados por comas")
    ap.add_argument("--bloqueo", action="store_true", help="sale con 1 si hay hallazgos (por defecto solo informa)")
    args = ap.parse_args(argv)
    try:
        prohibidos, permitidos = leer_vocabulario(c.leer_texto(args.vocabulario))
        permitidos |= {p.strip() for p in args.permitidos.split(",") if p.strip()}
        contratos = leer_contratos(args.contratos) if args.contratos else None
        archivos = c.listar_archivos(args.rutas, EXTENSIONES)
    except (OSError, FileNotFoundError) as e:
        print(f"Error de uso: {e}", file=sys.stderr)
        return c.SALIDA_USO
    if not prohibidos:
        print("El vocabulario no tiene filas con sinónimos prohibidos rellenados (¿sigue con marcadores «<...>»?).", file=sys.stderr)
        return c.SALIDA_USO
    total, con_hallazgos = 0, 0
    for ruta in archivos:
        try:
            hs = revisar_archivo(ruta, prohibidos, permitidos, contratos, args.incluir_sin_contrato)
        except Exception as e:  # noqa: BLE001
            print(f"[AVISO] no se pudo leer {ruta}: {e}")
            continue
        if hs:
            con_hallazgos += 1
        for linea, nombre, attr, alts in hs:
            total += 1
            print(f"{ruta}:{linea}: <{nombre} {attr}> «{attr}» no es el nombre canónico; usa {' o '.join('«' + a + '»' for a in alts)}")
    print(f"\n{total} hallazgo(s) en {con_hallazgos} de {len(archivos)} archivo(s) revisados · {len(prohibidos)} sinónimo(s) prohibido(s) cargados · modo {'bloqueo' if args.bloqueo else 'informe'}.")
    print("Alcance: atributos de etiquetas. No revisa valores, nombres de componentes ni código generado.")
    return c.SALIDA_HALLAZGOS if (total and args.bloqueo) else c.SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
