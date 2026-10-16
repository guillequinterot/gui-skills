# 05 · Assets que se hornean (porque Canva no los importa desde HTML)

Todo con `scripts/bake_assets.py` (probado: 6 de 7 salidas idénticas byte a byte a las del caso real). Idea común: **el HTML es la fuente de verdad del texto y la composición; el arte raster/vectorial se genera aparte y entra a Canva como imagen.**

| Subcomando | Qué produce | Cuándo | Parámetros clave |
|---|---|---|---|
| `panel` | Panel de color con **borde de pincel seco** (cerdas, flecos, salpicaduras) | Layout dividido (opción C de v1) | `--w --h --edge --color --seed` |
| `swoosh` | **Pincelada horizontal** a sangre con degradé tonal vino→profundo→marca→vivo, textura de cerdas y borde seco | Cabecera de color (opción D de v2) | `--w --h --base --slope --seed` |
| `triangles` | **Mosaico low-poly** (Delaunay) que se disuelve en blanco; SVG + PNG 2x | Bloque geométrico (opción F de v2) | `--w --h --cell --fade-from --fade-len --seed` |
| `marble` | Recorte vertical de foto de **pintura fluida**, remapeando violetas/naranjas a rojos de marca | Panel de textura (opción E de v2) | `--src --crop-x --w --h` |
| `canvas-bg` | **Lienzo** casi blanco (foto de tela de stock, aclarada, contraste ×0,42) | Fondo sutil "lienzo" | `--src --x --y --mean --contrast` |
| `vignette` | Fondo oscuro con **luz radial** | Opción oscura (placa) | `--inner --mid --outer --cx --cy` |
| `logo` | SVG vectorial + PNG recortado de un artboard de `.ai`/PDF | Logo oficial sin Illustrator | `--src --page` (en `caso-diplomas-01`: 0 plano, 3 contorno blanco) |

## Reglas

- **Salida a 2x** del tamaño CSS donde hay textura (PNG/JPG), para que en Canva no se vea blando al exportar a imprenta.
- Colocar en Canva con el tamaño **CSS** (no el del archivo): `pincelada-roja-tonal.png` es 4000×1700 y va a 2000×850.
- **Borde de pincel realista**: cerdas = rachas por fila/columna con longitud correlacionada (2–11 px) y rotura de borde con ruido alargado en el sentido del arrastre; salpicaduras = elipses pequeñas más allá del borde. Lo "goteante" (cerdas verticales largas) parece sangre: la versión buena arrastra en horizontal con borde de cerdas **paralelas** al arrastre.
- **Corte de página en vectores copiados** (p. ej. trazos del brochure): el vector tiene bordes de página visibles. Se resuelve desvaneciendo ese lado con un umbral de ruido alargado en la dirección del trazo (ver `ejemplos/caso-diplomas-01/scripts-originales/bake.py`) y colocando el asset de modo que el otro corte quede fuera del lienzo.
- **Fill-rule**: al reconstruir paths de un PDF, usar `nonzero` (no `evenodd`) o aparecen huecos tipo tablero de ajedrez.
- **Logo**: sacar del `.ai` oficial (PyMuPDF abre `.ai` PDF-compatibles): artboard plano para fondo claro; con contorno blanco para fondos oscuros o rojos (el logotipo negro desaparece sobre rojo/vino).
- **Stock** (Magnific/Freepik MCP): `stock_search` → `stock_download` (el flag `ai_generated: excluded` no es fiable; mirar la imagen). Registrar id usado (`caso-diplomas-01`: lienzo `1273386`, mármol rojo `15644183`) y descartados. Ver saldo con `account_balance` antes de descargas premium. Los originales pesados (38 MB) no se copian a la skill: re-descargar por id.
- **Triángulos**: `random` depende del orden de llamadas; con distinta versión del script la malla no es idéntica a la del caso (el asset original del caso no se sube al repo).

## Pasar un vector del PDF/AI a SVG propio

`scripts/pdf_pages.py vectors <archivo> --page N` lista dibujos y colores; filtrar por color de relleno (p. ej. rojo de los trazos = (0.885, 0.207, 0.172)), reconstruir `d` desde `items` (`l`, `c`, `re`, `qu`) y recolorear al rojo oficial. Código: `ejemplos/caso-diplomas-01/scripts-originales/streak.py`.
