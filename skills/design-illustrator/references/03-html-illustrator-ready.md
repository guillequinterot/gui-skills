# 03 · HTML «Illustrator-ready»

Reglas para escribir el HTML de modo que el paso a Illustrator sea limpio. Son además las del método de láminas fijas de `direct-visual-design` (1 hoja = 1 HTML).

## Estructura

- **Una lámina por archivo**, de tamaño fijo (`body` = `W × H`); el nombre de archivo ordena las láminas (`p01-…`, `p02-…`). Sin scroll, sin elementos fuera de la lámina.
- **Texto real**, nunca texto como imagen. Fuentes cargables al imprimir (Google Fonts con internet o `@font-face` a archivo local).
- Una sola familia tipográfica (mejor): menos pesos = menos riesgo de fuente faltante. Usar solo glifos que la fuente tenga (p. ej. Poppins **no** tiene «≥»: escribir «4,5:1 o más»).
- Medidas en múltiplos de 4 y px enteros (método de Guille).

## Bloques de texto (para que se unan en texto corrido)

- Un párrafo = **un elemento de bloque (`p`, `h1`, `div`) cuyo único contenido es texto y `<br>`**. Así `extract_paragraphs.py` lo reconoce y Illustrator lo recibe como **una caja de texto de área**.
- Saltos forzados con `<br>` (cada tramo se reconstruye con salto de párrafo); no usar `&nbsp;` para forzar saltos.
- **Evitar `<span>`/`<b>`/`<a>` dentro de un párrafo** (negritas o colores a media frase): ese bloque queda como líneas sueltas. Si hace falta, separarlo en bloques.
- Letras espaciadas (etiquetas en mayúsculas): `letter-spacing` en CSS; se convierte en tracking de Illustrator. Escribir las mayúsculas en mayúsculas (no `text-transform`).
- Alineación `left`/`center`/`right` por elemento; no `justify`.

## Gráficos

- **Logos y símbolos = SVG** (inline o `<img src=…svg>`) con texto en trazos. Dimensionar por altura, `width:auto`; nunca deformar (salvo un «uso incorrecto» a propósito).
- **Sin** `overflow:hidden`, `clip-path`, `transform`, `box-shadow`, `filter`, `mix-blend-mode`, `backdrop-filter`, gradientes ni `background-image`: generan recortes, rasterizados o efectos que no llegan limpios. Profundidad = color de superficie + borde de 1 px.
- **Evitar `border-radius` combinado con bordes parciales** (un asa/arco dibujado con borde): Chromium lo exporta como un anillo recortado en varios trozos. Dibujarlo como **SVG** (`<path>` con trazo).
- Fotografías = `<img>` real (se rasterizan una vez) o **cuadro gris con etiqueta** (`data-placeholder`) que el usuario sustituye.
- Colores en RGB; los CMYK de imprenta son un paso aparte.

## Verificación en el HTML

- Un validador de proyecto que compruebe: tamaño exacto, nada fuera de márgenes, fuentes cargadas, valores enteros/múltiplos de 4, ausencia de efectos prohibidos (`caso-manual-marca-01`: `validate_pages.py`).
- Después del paso a Illustrator: `ai_audit.ps1` debe dar 0 recortes, 0 invisibles, 0 desbordados.
