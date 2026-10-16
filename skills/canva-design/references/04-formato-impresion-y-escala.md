# 04 · Formato, impresión y escala tipográfica

## Convención de píxeles

- **Pieza física → 100 px/cm.** 20×14 cm = **2000×1400 px**; 21×29,7 = 2100×2970; A4 horizontal = 2970×2100. 100 px/cm ≈ 254 ppi: suficiente para exportar a imprenta; si el proveedor pide 300 ppi, exportar el PDF/PNG de Canva con más resolución (el diseño vectorial/texto escala; los assets rasterizados horneados a 2x quedan ~254-508 ppi efectivos).
- **Pantalla** (1920×1080 etc.): los px de Canva son los del diseño.
- Pedir al usuario la **medida real** (marco, papel, placa). En `caso-diplomas-01` la foto del marco traía "20 cm × 14 cm" → formato 10:7.

## Escala de impresión (a 100 px/cm)

| Elemento | px | cm | pt aprox. |
|---|---|---|---|
| Cuerpo de texto | 28–32 | 0,28–0,32 | 8–9 |
| Cita/destacado (serif cursiva) | 36–44 | 0,36–0,44 | 10–12,5 |
| Cierre/llamada (bold) | 30–34 | 0,30–0,34 | 8,5–9,5 |
| Firma (nombre / cargo) | 24 / 19 | 0,24 / 0,19 | 7 / 5,5 |
| Nombre del homenajeado | 100–125 | 1,0–1,25 | 28–35 |
| Numeral héroe | 290–470 | 2,9–4,7 | — |
| Etiqueta tracking ancho | 28–34 | — | 8–9,5 |

**Error ya cometido y corregido:** el diseño de pantalla (1920×1080) usaba cuerpo de 22–25 px; a 20 cm de ancho habría sido ≈6,5 pt. Al pasar a una medida física se **re-escala la tipografía**, no solo el lienzo.

## Márgenes y seguridad

- Texto y logo a ≥ **50 px (5 mm)** de cada borde; sangrado: si la imprenta lo pide, ampliar el lienzo **+3 mm por lado (= 30 px a 100 px/cm)** y extender los fondos.
- Un marco físico (como el de 20×14 cm de `caso-diplomas-01`) recorta ~5–8 mm: no pegar texto al borde.
- Elementos a sangre (pincelada arriba, mármol a la derecha): dejar que sobresalgan del lienzo (posiciones negativas) para que no se vea el corte del asset.

## Proporción y reencuadre

Al pasar de un formato a otro **recomponer**, no estirar: la jerarquía, el reparto vertical y los saltos de línea cambian (10:7 es más alto que 16:9). Ejemplo: en 2000×1400 cabe una pincelada de 55 % de la altura + 8 líneas de texto; en 1920×1080 no.

## Contraste y color

Ratios WCAG calculados (2026-10-09):
- Blanco sobre rojo marca `#DA111C`: **5,15** (ok); sobre vivo `#F2343B`: **3,94** (solo texto grande ≥ 24 px); sobre profundo `#8E0F1B`: 9,4.
- Coral `#FF6B5E` sobre vino `#4E0814`: **5,49**; sobre `#2A050C`: 6,68 (ok). Crema `#F6E4E6` sobre vino: 12,5.
- Texto en tonos sobre blanco: marca `#DA111C` 5,15 (bold/grande), profundo `#8E0F1B` 9,4, vino `#4E0814` 15,3. El cuerpo va en `#1A1A1A`.
- Paleta tonal aprobada (colega, 2026-10-08): vino `#4E0814` · profundo `#8E0F1B` · marca `#DA111C` · vivo `#F2343B` · coral `#FF6B5E` (solo sobre oscuro). El rojo de marca sigue siendo el protagonista.
