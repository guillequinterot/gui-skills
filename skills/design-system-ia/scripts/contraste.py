"""contraste.py — contraste WCAG 2.x entre colores, en claro y oscuro, SIN redondear antes de comparar.

  python -I contraste.py "#1a1a1a" "#ffffff" [--tipo normal|grande|no-texto]
  python -I contraste.py --pares pares.json

Fórmula (WCAG 2.x, verificada en la página de luminancia relativa del W3C el 2026-10-27):
  canal = valor8bits / 255
  lineal = canal / 12.92 si canal <= 0.04045; si no, ((canal + 0.055) / 1.055) ** 2.4
     (la página oficial nombra 0.03928 y su aviso de erratas dice que el valor correcto es 0.04045;
      con colores de 8 bits la diferencia no es significativa)
  L = 0.2126 R + 0.7152 G + 0.0722 B
  contraste = (L_claro + 0.05) / (L_oscuro + 0.05)
Umbrales (WCAG 2.2 AA): 1.4.3 texto normal 4,5:1 y grande 3:1; 1.4.11 objetos que no son texto 3:1.
Un valor se muestra con 2 decimales, pero se COMPARA sin redondear (4,499 no pasa).

Formato de pares.json:
  {"pares": [
     {"nombre": "texto sobre superficie", "tipo": "normal",
      "texto":  {"claro": "#1a1a1a", "oscuro": "#f5f5f5"},
      "fondo":  {"claro": "#ffffff", "oscuro": "#121212"}},
     {"nombre": "texto deshabilitado", "deshabilitado": true, "texto": {...}, "fondo": {...}}
  ]}
  «tipo»: normal (por defecto), grande o no-texto. Un par «deshabilitado» queda EXENTO (WCAG 1.4.3 exime a los
  componentes inactivos) pero se informa y se documenta. Se comprueban claro y oscuro por separado.
  «temas»: por defecto ["claro", "oscuro"]. Si el sitio solo tiene tema claro, escribe "temas": ["claro"] en la raíz
  del JSON (o en un par) y no hace falta dar el color oscuro; así queda dicho, no omitido por olvido.

Límites: solo colores opacos (#RGB o #RRGGBB). Un color con transparencia hay que aplanarlo antes sobre su fondo.
No juzga tamaño de texto real, imágenes ni degradados.
Salida: 0 si todo pasa o está exento; 1 si algún par falla; 2 por uso o lectura.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _comun as c  # noqa: E402

UMBRALES = {"normal": 4.5, "grande": 3.0, "no-texto": 3.0}
CRITERIO = {"normal": "1.4.3", "grande": "1.4.3", "no-texto": "1.4.11"}


def parsear_color(texto):
    t = str(texto).strip()
    if re.fullmatch(r"#[0-9a-fA-F]{8}|#[0-9a-fA-F]{4}", t):
        raise ValueError(f"{t}: tiene transparencia; aplánalo sobre su fondo antes de medir")
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", t)
    if not m:
        raise ValueError(f"{t!r}: no es un color #RGB o #RRGGBB")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def lineal(v):
        cnl = v / 255.0
        return cnl / 12.92 if cnl <= 0.04045 else ((cnl + 0.055) / 1.055) ** 2.4
    r, g, b = (lineal(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(parsear_color(a)), luminancia(parsear_color(b))
    claro, oscuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (oscuro + 0.05)


def evaluar(tipo, ratio):
    return ratio >= UMBRALES[tipo]


def fmt(ratio):
    return f"{ratio:.2f}:1"


def procesar_pares(datos):
    """Devuelve (filas, fallos). Cada fila: (nombre, tema, ratio, umbral, estado)."""
    filas, fallos = [], 0
    for i, p in enumerate(datos.get("pares", [])):
        nombre = p.get("nombre", f"par {i + 1}")
        tipo = p.get("tipo", "normal")
        if tipo not in UMBRALES:
            raise ValueError(f"{nombre}: tipo desconocido {tipo!r} (normal, grande o no-texto)")
        exento = bool(p.get("deshabilitado"))
        temas = p.get("temas") or datos.get("temas") or ["claro", "oscuro"]
        for tema in temas:
            try:
                t, f = p["texto"][tema], p["fondo"][tema]
            except KeyError:
                filas.append((nombre, tema, None, UMBRALES[tipo], "FALTA el color de este tema"))
                fallos += 1
                continue
            ratio = contraste(t, f)
            if exento:
                estado = "exento (deshabilitado; documéntalo)"
            elif evaluar(tipo, ratio):
                estado = "pasa"
            else:
                estado = "FALLA"
                fallos += 1
            filas.append((nombre, tema, ratio, UMBRALES[tipo], estado))
    return filas, fallos


def main(argv=None):
    c.configurar_salida()
    ap = argparse.ArgumentParser(description="Contraste WCAG entre colores.")
    ap.add_argument("colores", nargs="*", help="dos colores: texto/primer plano y fondo")
    ap.add_argument("--tipo", default="normal", choices=sorted(UMBRALES))
    ap.add_argument("--pares", help="JSON con pares en claro y oscuro")
    args = ap.parse_args(argv)
    try:
        if args.pares:
            filas, fallos = procesar_pares(c.leer_json(args.pares))
            if not filas:
                print("El archivo no tiene pares.", file=sys.stderr)
                return c.SALIDA_USO
            for nombre, tema, ratio, umbral, estado in filas:
                valor = fmt(ratio) if ratio is not None else "—"
                print(f"{nombre} · {tema}: {valor} (mínimo {umbral:g}:1) → {estado}")
            print(f"\n{len(filas)} comprobación(es), {fallos} fallo(s). Criterios: 1.4.3 (texto) y 1.4.11 (no texto), WCAG 2.2 AA.")
            return c.SALIDA_HALLAZGOS if fallos else c.SALIDA_OK
        if len(args.colores) != 2:
            ap.error("indica dos colores o usa --pares")
        ratio = contraste(args.colores[0], args.colores[1])
        ok = evaluar(args.tipo, ratio)
        print(f"{args.colores[0]} sobre {args.colores[1]}: {fmt(ratio)} (mínimo {UMBRALES[args.tipo]:g}:1, criterio {CRITERIO[args.tipo]}) → {'pasa' if ok else 'FALLA'}")
        return c.SALIDA_OK if ok else c.SALIDA_HALLAZGOS
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return c.SALIDA_USO


if __name__ == "__main__":
    sys.exit(main())
