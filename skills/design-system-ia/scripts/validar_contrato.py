"""validar_contrato.py — comprueba la FORMA de contratos de componente y, opcionalmente, su POLÍTICA.

  python -I validar_contrato.py <archivo.json|archivo.md|carpeta> [...] [--esquema RUTA] [--politica] [--estricto]

Qué comprueba
  - JSON: el contrato frente a scripts/contrato.schema.json con un validador mínimo propio.
    Soporta: type, required, properties, additionalProperties, items, enum, pattern, minLength, minItems.
    NO implementa todo JSON Schema 2020-12 (no hay $ref, oneOf, if/then, formatos ni dependencias).
  - Markdown: que el contrato MÍNIMO tenga los 5 campos + los estados que se entregan (references/01, sección 3).
  - --politica: lo que el esquema deja opcional pero el sistema exige (neverUseFor, rationale, governance con
    mayExtendLocally y mustEscalateToDS, a11y con role y wcag que empiece por número y nombre del criterio), y dos
    comprobaciones que hace el verificador de Helix: partes de anatomía en kebab-case y ningún token a la vez en
    allowed y forbidden.
  - El esquema prohíbe campos desconocidos SOLO en la raíz; los objetos anidados admiten campos adicionales.
  - --estricto: además rechaza marcadores de plantilla («<...>», «GENERADO») que sigan sin rellenar.

Qué NO comprueba
  - Que las props del contrato coincidan con el código (eso lo hace vocabulario_check.py solo para nombres) ni con
    Figma (comparar_figma_contrato.py).
  - Que el contenido sea correcto: solo que exista y tenga la forma pedida.

Salida: una línea por archivo y un resumen con conteos. Código 0 sin problemas, 1 con problemas, 2 uso o lectura.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comun as c  # noqa: E402

ESQUEMA_POR_DEFECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contrato.schema.json")

CAMPOS_MINIMO = [
    ("Propósito", r"\*\*Propósito:\*\*"),
    ("Nunca usar para", r"\*\*Nunca usar para:\*\*"),
    ("Justificación", r"\*\*Justificación:\*\*"),
    ("Se adapta en el proyecto", r"\*\*Se adapta en el proyecto:\*\*"),
    ("Se escala al sistema", r"\*\*Se escala al sistema:\*\*"),
    ("Anatomía", r"\*\*Anatomía:\*\*"),
    ("Estados que se entregan", r"\*\*Estados que se entregan[^*]*:\*\*"),
]

WCAG_OFICIAL = re.compile(r"^\d\.\d+\.\d+\s+[A-Z][A-Za-z\- ()]+?(?:,\s*|\s+\()?(A{1,3})\)?$")


# ---------------------------------------------------------------- validador mínimo de JSON Schema
def _tipo_ok(valor, tipo):
    if tipo == "string":
        return isinstance(valor, str)
    if tipo == "boolean":
        return isinstance(valor, bool)
    if tipo == "integer":
        return isinstance(valor, int) and not isinstance(valor, bool)
    if tipo == "number":
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    if tipo == "array":
        return isinstance(valor, list)
    if tipo == "object":
        return isinstance(valor, dict)
    if tipo == "null":
        return valor is None
    return True


def validar(valor, esquema, ruta="$"):
    errores = []
    tipo = esquema.get("type")
    if tipo is not None:
        tipos = tipo if isinstance(tipo, list) else [tipo]
        if not any(_tipo_ok(valor, t) for t in tipos):
            return [f"{ruta}: se esperaba {tipo} y hay {type(valor).__name__}"]
    if "enum" in esquema and valor not in esquema["enum"]:
        errores.append(f"{ruta}: debe ser uno de {esquema['enum']} y es {valor!r}")
    if isinstance(valor, str):
        if "minLength" in esquema and len(valor) < esquema["minLength"]:
            errores.append(f"{ruta}: está vacío")
        if "pattern" in esquema and not re.search(esquema["pattern"], valor):
            errores.append(f"{ruta}: {valor!r} no cumple el patrón {esquema['pattern']}")
    if isinstance(valor, list):
        if "minItems" in esquema and len(valor) < esquema["minItems"]:
            errores.append(f"{ruta}: necesita al menos {esquema['minItems']} elemento(s)")
        if "items" in esquema:
            for i, elem in enumerate(valor):
                errores += validar(elem, esquema["items"], f"{ruta}[{i}]")
    if isinstance(valor, dict):
        for r in esquema.get("required", []):
            if r not in valor:
                errores.append(f"{ruta}: falta el campo obligatorio «{r}»")
        props = esquema.get("properties", {})
        extra = esquema.get("additionalProperties", True)
        for k, v in valor.items():
            if k in props:
                errores += validar(v, props[k], f"{ruta}.{k}")
            elif extra is False:
                errores.append(f"{ruta}: campo desconocido «{k}» (el esquema no admite campos adicionales)")
            elif isinstance(extra, dict):
                errores += validar(v, extra, f"{ruta}.{k}")
    return errores


# ---------------------------------------------------------------- política y marcadores
def politica(contrato):
    problemas = []
    if not contrato.get("neverUseFor"):
        problemas.append("política: falta «neverUseFor» (antipatrones con su alternativa)")
    if not str(contrato.get("rationale", "")).strip():
        problemas.append("política: falta «rationale» (la decisión y su motivo)")
    gob = contrato.get("governance") or {}
    for k in ("mayExtendLocally", "mustEscalateToDS"):
        if not gob.get(k):
            problemas.append(f"política: «governance.{k}» está vacío o falta")
    a11y = contrato.get("a11y") or {}
    if not str(a11y.get("role", "")).strip():
        problemas.append("política: falta «a11y.role»")
    wcag = a11y.get("wcag") or []
    if not wcag:
        problemas.append("política: «a11y.wcag» está vacío")
    for item in wcag:
        if isinstance(item, str) and not c.esta_vacio_o_marcador(item) and not re.match(r"^\d\.\d+\.\d+\s+\S", item):
            problemas.append(f"política: «a11y.wcag» debe empezar por el número del criterio y su nombre oficial: {item!r}")
    for parte in contrato.get("anatomy") or []:
        nombre = parte.get("part") if isinstance(parte, dict) else None
        if isinstance(nombre, str) and not c.esta_vacio_o_marcador(nombre) and not re.match(r"^[a-z][a-z0-9-]*$", nombre):
            problemas.append(f"política: la parte de anatomía {nombre!r} debe estar en kebab-case")
    pol = contrato.get("tokenPolicy") or {}
    if isinstance(pol.get("allowed"), list) and isinstance(pol.get("forbidden"), list):
        for tok in pol["forbidden"]:
            if tok in pol["allowed"]:
                problemas.append(f"política: el token {tok!r} está a la vez en allowed y en forbidden")
    return problemas


def marcadores(valor, ruta="$"):
    salida = []
    if isinstance(valor, str):
        if c.esta_vacio_o_marcador(valor):
            salida.append(f"{ruta}: marcador de plantilla sin rellenar ({valor[:40]!r})")
    elif isinstance(valor, list):
        for i, v in enumerate(valor):
            salida += marcadores(v, f"{ruta}[{i}]")
    elif isinstance(valor, dict):
        for k, v in valor.items():
            salida += marcadores(v, f"{ruta}.{k}")
    return salida


# ---------------------------------------------------------------- contrato mínimo (Markdown)
def validar_minimo(texto, estricto):
    problemas = []
    for nombre, patron in CAMPOS_MINIMO:
        m = re.search(patron + r"([^\n]*)", texto)
        if not m:
            problemas.append(f"falta el campo «{nombre}»")
            continue
        contenido = m.group(1).strip()
        if not contenido and nombre != "Estados que se entregan":
            problemas.append(f"el campo «{nombre}» está vacío")
        elif estricto and ("<" in contenido and ">" in contenido):
            problemas.append(f"el campo «{nombre}» sigue con marcadores de plantilla")
    if not re.search(r"^# \S", texto, re.M):
        problemas.append("falta el título (# Nombre del componente)")
    return problemas


# ---------------------------------------------------------------- ejecución
def procesar(ruta, esquema, args):
    """Devuelve (lista de problemas, tipo)."""
    try:
        if ruta.lower().endswith(".md"):
            return validar_minimo(c.leer_texto(ruta), args.estricto), "mínimo"
        contrato = c.leer_json(ruta)
    except Exception as e:  # noqa: BLE001
        return [f"no se pudo leer: {e}"], "ilegible"
    problemas = validar(contrato, esquema)
    if args.politica:
        problemas += politica(contrato)
    if args.estricto:
        problemas += marcadores(contrato)
    return problemas, "completo"


def main(argv=None):
    c.configurar_salida()
    ap = argparse.ArgumentParser(description="Valida contratos de componente (forma y, opcionalmente, política).")
    ap.add_argument("rutas", nargs="+", help="archivos .json o .md, o carpetas")
    ap.add_argument("--esquema", default=ESQUEMA_POR_DEFECTO, help="ruta al esquema JSON (por defecto, el de la skill)")
    ap.add_argument("--politica", action="store_true", help="exige también lo que el esquema deja opcional")
    ap.add_argument("--estricto", action="store_true", help="rechaza marcadores de plantilla sin rellenar")
    args = ap.parse_args(argv)
    try:
        esquema = c.leer_json(args.esquema)
        archivos = c.listar_archivos(args.rutas, (".json", ".md"))
    except Exception as e:  # noqa: BLE001
        print(f"Error de uso: {e}", file=sys.stderr)
        return c.SALIDA_USO
    archivos = [a for a in archivos if not os.path.basename(a).endswith(".schema.json")]
    if not archivos:
        print("No hay contratos que revisar.", file=sys.stderr)
        return c.SALIDA_USO
    validos = 0
    con_problemas = 0
    for a in archivos:
        problemas, tipo = procesar(a, esquema, args)
        if problemas:
            con_problemas += 1
            print(f"[ERROR] {a} ({tipo})")
            for p in problemas:
                print(f"   - {p}")
        else:
            validos += 1
            print(f"[OK]    {a} ({tipo})")
    print(f"\n{validos} contrato(s) con la forma correcta, {con_problemas} con problemas, {len(archivos)} revisado(s).")
    print("Alcance: forma" + (" y política" if args.politica else "") + ". No comprueba que las props coincidan con el código ni con Figma.")
    return c.SALIDA_HALLAZGOS if con_problemas else c.SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
