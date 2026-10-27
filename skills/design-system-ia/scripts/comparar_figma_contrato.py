"""comparar_figma_contrato.py — compara las propiedades de un componente de Figma con su contrato.

  python -I comparar_figma_contrato.py contrato.json figma.json

figma.json es el resultado de una LECTURA DE SOLO CONSULTA (use_figma, con figma:figma-use cargada antes) de
`componentPropertyDefinitions` del conjunto de variantes, guardado en un archivo. Formatos aceptados:
  1) {"component": "Button", "properties": { "variant": {"type": "VARIANT", "defaultValue": "primary",
                                                           "variantOptions": ["primary", "secondary"]},
                                             "isLoading": {"type": "VARIANT", "defaultValue": "false",
                                                           "variantOptions": ["false", "true"]},
                                             "children#12:3": {"type": "TEXT", "defaultValue": "Button"} }}
  2) solo el objeto «properties»
  3) una lista [{"name": ..., "type": ..., "defaultValue": ..., "variantOptions": [...]}, ...]
El ORDEN de las claves es el que Figma entrega: se usa para comprobar el orden.
Se ignora el sufijo «#id» de Figma y el punto final de los ayudantes solo-Figma (p. ej. «icon.»).

Qué comprueba (referencia 05, secciones 4, 7 y 8)
  1. Props del contrato que no existen en Figma (se exceptúan los manejadores onXxx, que no tienen propiedad en Figma,
     y las props cuyo nombre aparece en una excepción aprobada de figma.approvedExceptions[].what).
  2. Propiedades de Figma que no están en el contrato (se exceptúan figma.figmaOnlyProps, p. ej. «state»).
  3. Valores por defecto distintos (en Helix, el contrato decía size=m y Figma s).
  4. Opciones distintas en las props de tipo unión de literales ('a' | 'b').
  5. Orden: las propiedades VARIANT van primero y en el mismo orden que el contrato.
  6. Eje de estados: figma.stateAxis del contrato debe estar contenido en las opciones de «state».

Qué NO comprueba: colores, espaciado, variables enlazadas, anillo de foco ni nada visual (la auditoría visual sigue
siendo manual, referencia 05 sección 8). «Sin diferencias» solo dice que las PROPIEDADES coinciden.
Salida: 0 sin diferencias; 1 con diferencias; 2 uso o lectura.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comun as c  # noqa: E402

MANEJADOR = re.compile(r"^on[A-Z]")
LITERAL = re.compile(r"'([^']*)'|\"([^\"]*)\"")


def normalizar_nombre(n):
    n = re.sub(r"#.*$", "", str(n)).strip()
    return n.rstrip(".")


def es_ayudante(n):
    return str(re.sub(r"#.*$", "", str(n))).strip().endswith(".")


def leer_figma(datos):
    """Devuelve lista ordenada de dicts {name, type, default, options, ayudante}."""
    if isinstance(datos, dict) and "properties" in datos:
        datos = datos["properties"]
    salida = []
    if isinstance(datos, dict):
        for k, v in datos.items():
            v = v if isinstance(v, dict) else {}
            salida.append({"name": normalizar_nombre(k), "ayudante": es_ayudante(k), "type": v.get("type"),
                           "default": v.get("defaultValue"), "options": v.get("variantOptions") or v.get("options")})
    elif isinstance(datos, list):
        for v in datos:
            salida.append({"name": normalizar_nombre(v.get("name", "")), "ayudante": es_ayudante(v.get("name", "")),
                           "type": v.get("type"), "default": v.get("defaultValue"),
                           "options": v.get("variantOptions") or v.get("options")})
    else:
        raise ValueError("formato de Figma no reconocido")
    return salida


def como_texto(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v).strip().lower()


def opciones_del_tipo(tipo):
    lits = [a or b for a, b in LITERAL.findall(str(tipo))]
    return lits if lits else None


def comparar(contrato, figma):
    dif = []
    props = [p for p in contrato.get("props", []) if isinstance(p, dict)]
    ext = contrato.get("figma") or {}
    solo_figma = set(ext.get("figmaOnlyProps") or [])
    excepciones = " ".join(str(e.get("what", "")) for e in (ext.get("approvedExceptions") or []) if isinstance(e, dict))
    por_nombre = {f["name"]: f for f in figma if not f["ayudante"]}

    # 1) contrato -> Figma
    for p in props:
        n = p.get("name", "")
        if MANEJADOR.match(n):
            continue
        if n not in por_nombre:
            if re.search(r"\b" + re.escape(n) + r"\b", excepciones):
                continue
            dif.append(f"falta en Figma: la prop «{n}» del contrato no tiene propiedad")
            continue
        f = por_nombre[n]
        # 3) defaults
        if p.get("default") is not None and f["default"] is not None and como_texto(p["default"]) != como_texto(f["default"]):
            dif.append(f"valor por defecto distinto en «{n}»: contrato {p['default']!r}, Figma {f['default']!r}")
        # 4) opciones
        op_contrato = opciones_del_tipo(p.get("type"))
        if op_contrato and f["options"]:
            a, b = set(map(como_texto, op_contrato)), set(map(como_texto, f["options"]))
            if a != b:
                dif.append(f"opciones distintas en «{n}»: solo en contrato {sorted(a - b)}, solo en Figma {sorted(b - a)}")
    # 2) Figma -> contrato
    nombres_contrato = {p.get("name") for p in props}
    for f in figma:
        if f["ayudante"] or f["name"] in nombres_contrato or f["name"] in solo_figma:
            continue
        dif.append(f"propiedad solo-Figma sin aprobar: «{f['name']}» no está en el contrato ni en figma.figmaOnlyProps")
    # 5) orden: VARIANT primero y en el orden del contrato
    tipos = [f["type"] for f in figma if not f["ayudante"]]
    vistas_no_variant = False
    for t in tipos:
        if t != "VARIANT":
            vistas_no_variant = True
        elif vistas_no_variant:
            dif.append("orden: hay propiedades VARIANT después de otras que no lo son (las variantes van primero)")
            break
    orden_contrato = [p["name"] for p in props if p.get("name") in por_nombre]
    orden_figma = [f["name"] for f in figma if not f["ayudante"] and f["name"] in set(orden_contrato)]
    if orden_contrato != orden_figma:
        dif.append(f"orden distinto: contrato {orden_contrato}, Figma {orden_figma}")
    # 6) eje de estados
    eje = ext.get("stateAxis") or []
    if eje:
        estado = por_nombre.get("state")
        if not estado:
            dif.append("el contrato declara un eje de estados (figma.stateAxis) y Figma no tiene la propiedad «state»")
        else:
            falta = [s for s in eje if como_texto(s) not in set(map(como_texto, estado["options"] or []))]
            if falta:
                dif.append(f"el eje «state» de Figma no dibuja: {falta}")
    return dif


def main(argv=None):
    c.configurar_salida()
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        return c.SALIDA_USO if args and args[0] not in ("-h", "--help") else c.SALIDA_OK
    try:
        contrato = c.leer_json(args[0])
        figma = leer_figma(c.leer_json(args[1]))
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        return c.SALIDA_USO
    dif = comparar(contrato, figma)
    nombre = contrato.get("name", args[0])
    if dif:
        print(f"[DIFERENCIAS] {nombre}: {len(dif)}")
        for d in dif:
            print(f"   - {d}")
    else:
        print(f"[OK] {nombre}: las propiedades de Figma coinciden con el contrato ({len(figma)} propiedad(es) leídas).")
    print("Alcance: propiedades, valores por defecto, opciones, orden y eje de estados. No comprueba nada visual.")
    return c.SALIDA_HALLAZGOS if dif else c.SALIDA_OK


if __name__ == "__main__":
    sys.exit(main())
