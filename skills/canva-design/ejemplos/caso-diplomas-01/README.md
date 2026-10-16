# Ejemplo: `caso-diplomas-01` — diplomas HTML → Canva (resumen anónimo)

Caso que originó la skill (2026-10-08/09). El proceso, las decisiones y los errores están en [`../../references/07-caso-diplomas-01.md`](../../references/07-caso-diplomas-01.md); la ficha de la marca, en [`../../proyectos/caso-diplomas-01.md`](../../proyectos/caso-diplomas-01.md).

## Qué había en la carpeta original (y por qué no está aquí)

La carpeta del caso pesaba ~24 MB: tres HTML de la v1 (1920 × 1080) y uno de la v2 (2000 × 1400 = 20 × 14 cm), un HTML combinado para importar, 17 assets (logos, trazos de pincel, mármol, triángulos, fondos), previews, exportaciones de Canva v1 y v2, el handoff y el handshake del proyecto, y 11 scripts de la sesión. **Todo eso lleva la marca, el logo y los textos del cliente**, así que quedó fuera del repo. Lo reutilizable ya está generalizado en `../../scripts/` (`bake_assets.py`, `lint_html_for_canva.py`, `build_import_html.py`, `render_html.sh`, `canva_verify.py`) y en `../../templates/diploma-20x14.template.html`.

Se conservan dos scripts de la sesión, anonimizados, porque documentan técnicas que no están en los generalizados:

| Archivo | Para qué |
|---|---|
| `scripts-originales/streak.py` | Reconstruye un vector (trazos de pincel) a SVG desde los dibujos de un PDF filtrando por color de relleno |
| `scripts-originales/bake.py` | Rasteriza ese SVG y desvanece el borde de corte de página con un umbral de ruido alargado en la dirección del trazo (borde de pincel seco) |

## Especificación de capas de la opción A (v1, 1920 × 1080)

Capas de abajo hacia arriba (`data-layer` en el HTML = nombre sugerido en Canva). Coordenadas = esquina superior izquierda del recuadro, en px del lienzo.

| # | Capa | Tipo | Posición / tamaño | Estilo |
|---|---|---|---|---|
| 01 | Fondo lienzo | Imagen | 0,0 · 1920×1080 | textura de lienzo (stock) aclarada |
| 02 | Trazos sup-der | Imagen | x 1260, y −30 · ancho 700 | PNG con borde de pincel seco |
| 03 | Trazos inf-izq | Imagen | x −60, y ≈ 599 · ancho 560 (sale 40 px por abajo) | PNG |
| 10 | Rótulo superior | Texto | centrado, y 62 | Montserrat SemiBold 28, interletraje +620, mayúsculas, negro |
| 11 | Numeral | Texto | derecha en x 815, y 96 | Montserrat ExtraBold 350, interletraje −45, interlineado 1, color de marca |
| 12 | Título (2 líneas) | Texto | x 845, y 128, ancho 620 | Montserrat ExtraBold 68, interlineado 1.02, negro |
| 12b | Remate del título | Texto | debajo de 12 | conector en Montserrat ExtraBold 76 negro · palabra de marca en serif Bold Italic 76 color de marca |
| 20 | Nombre | Texto | centrado, y 418 | Playfair Display SemiBold Italic 112, negro |
| 21 | Subrayado pincel | Forma/SVG | centrado, y 548, 760×22 | color de marca (reemplazable por un elemento "pincelada" de Canva) |
| 30 | Cita | Texto | centrado, y 588, ancho 1080 | Playfair Medium Italic 32, interlineado 1.38; palabra clave en Bold color de marca |
| 31 | Cuerpo | Texto | centrado, y 700, ancho 1100 | Montserrat Regular 22, interlineado 1.6, tinta `#1A1A1A` |
| 32 | Cierre | Texto | centrado, y 818, ancho 1100 | Montserrat Bold 27, color de marca |
| 40–45 | Firmas ×2 | Línea + 2 textos | líneas x 470 y 1120, y 958, ancho 330 | nombre Montserrat Bold 19 · cargo Montserrat Medium 16 mayúsculas +80 |
| 50 | Logo | SVG/PNG | centrado, y 896, ancho 220 | respetar el área de reserva del manual |

La v2 (20 × 14 cm, 2000 × 1400) repite el esquema con una sola firma, el logo arriba y la tipografía re-escalada para impresión: cuerpo 28–30 px ≈ 8–8,5 pt, citas 36–40 px, nombre 104–124 px (en la v1 el cuerpo medía 22–25 px y se habría visto minúsculo a 20 cm).

## Opciones de diseño presentadas

| Ronda | Opción | Idea | Assets extra |
|---|---|---|---|
| v1 | **A · Lienzo blanco** | Centrado, blanco con trazos de pincel en esquinas | — |
| v1 | **B · Placa negra** | Eco de la placa acrílica de premios: fondo negro, marco redondeado, numeral grande, texto blanco | logo con contorno blanco |
| v1 | **C · Panel pintado** | Panel de color con borde de pincel (numeral grande en blanco) + texto sobre lienzo blanco, alineado a la izquierda | panel con borde de pincel, logo con contorno blanco |
| v2 | **D · Pincelada tonal** | Pincelada horizontal arriba con degradé de la paleta tonal, logo y numeral encima | pincelada tonal, fondo lienzo 2000×1400 |
| v2 | **E · Mármol y vino** | Panel vino a la izquierda, mármol de pintura fluida (stock) a la derecha, textos en blanco/coral | mármol vertical, fondo vino con luz |
| v2 | **F · Triángulos tonales** | Mosaico de triángulos que se disuelve en blanco, numeral blanco gigante, logo arriba de la columna de texto | triángulos tonales (SVG/PNG) |

## Pasos que se siguieron (modelo para casos parecidos)

1. Subir a Canva los assets (logo SVG, trazos PNG, fondos) con `upload-asset-from-url`.
2. Importar el HTML Canva-ready por URL temporal; el importador trae el texto como texto de Canva con interletraje, tamaños y colores.
3. Colocar los assets con `update_fill` / `insert_fill`, ordenar capas con `layer_element`, compensar el numeral (−0,1 em) y ensanchar las cajas con riesgo de partirse.
4. Insertar las páginas en el diseño de destino (o crear uno nuevo si el tamaño difiere) con `merge-designs`, una operación por llamada.
5. Exportar PNG por página y comparar con el render del HTML (`canva_verify.py`); borrar el hosting temporal y comprobar 404.

## Pendientes del caso (a 2026-10-09)

- [ ] Elegir D/E/F y borrar las otras dos páginas.
- [ ] Resolver 11 vs 8 años y la redacción del tercer párrafo (el cliente dio ambos números; se dejaron literales).
- [ ] Definir firmantes, fecha y si hay versión para otro país.
