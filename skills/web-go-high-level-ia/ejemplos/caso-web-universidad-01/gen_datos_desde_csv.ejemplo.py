# -*- coding: utf-8 -*-
"""EJEMPLO SANITIZADO del patrón «un generador CSV -> módulo TypeScript» (incidencia J2).

  python gen_datos_desde_csv.ejemplo.py datos.ejemplo.csv salida.ts

Idea: la fuente única es una hoja del cliente (CSV). Las REGLAS DE DATOS del cliente se aplican AL GENERAR,
no dentro del componente, para que el componente solo pinte lo que ya es seguro mostrar:
  - un código oficial solo se publica si su estado es «verificado…»; si no, se omite y la ficha dice
    «Consúltalo en la fuente oficial»;
  - los cupos se copian tal cual (cifra o rango) y NUNCA se suman;
  - lo que no está en la hoja no se inventa.
Si el archivo generado pasa de 50 000 caracteres, se parte en dos módulos (K1): datos y textos largos.
"""
import csv
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")


def fila_a_item(fila):
    verificado = fila["estado_codigo"].strip().lower().startswith("verificado")
    return {
        "id": fila["id"].strip(),
        "slug": fila["nombre"].strip().lower().replace(" ", "-"),
        "nombre": fila["nombre"].strip(),
        "zona": fila["zona"].strip(),
        "codigo": fila["codigo_oficial"].strip() if verificado else None,  # regla: solo si está verificado
        "cupos": fila["cupos"].strip() or None,                              # regla: sin totales
    }


def main(entrada, salida):
    with open(entrada, encoding="utf-8", newline="") as f:
        items = [fila_a_item(r) for r in csv.DictReader(f)]
    ts = ["// GENERADO por gen_datos_desde_csv.py desde la hoja del cliente. No editar a mano: edita la hoja y regenera.",
          "export type Item = { id: string; slug: string; nombre: string; zona: string; codigo: string | null; cupos: string | null };",
          "export const ITEMS: Item[] = " + json.dumps(items, ensure_ascii=False, indent=2) + ";", ""]
    texto = "\n".join(ts)
    if len(texto) > 50000:
        raise SystemExit("el módulo pasa de 50 000 caracteres: sepáralo en datos y textos largos")
    with open(salida, "w", encoding="utf-8", newline="\n") as out:
        out.write(texto)
    print(len(items), "elementos,", len(texto), "caracteres")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
