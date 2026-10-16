# 02 · Límites y trucos del conector Canva (aprendidos, no supuestos)

Verificado en el caso `caso-diplomas-01` (2026-10-08/09) con el conector Canva de la sesión (servidor `<id-del-conector>`). Cada punto indica el síntoma y qué hacer. Si el conector cambia, re-verificar y registrar en `CHANGELOG.md`.

## A · Importación de HTML (`import-design-from-url`)

| # | Hecho | Qué hacer |
|---|---|---|
| A1 | Necesita **URL HTTPS pública con certificado válido**. No acepta rutas locales. | Hosting temporal (`03`). Un subdominio sin SSL válido falla (curl 60): usar el dominio raíz o uno con certificado válido. |
| A2 | Convierte **texto en texto real** con fuente, tamaño, peso, cursiva, color, `letter-spacing`, alineación e interlineado. `fontRef` correcto para Montserrat y Playfair Display. | Es la razón de usar este camino y no `add_text` por API. |
| A3 | **No descarga imágenes** (`<img>`, `background-image`). El `.page{background}` llega como un rectángulo de página completa. | Subir assets aparte y colocarlos (3.3–3.6). `update_fill` sobre ese rectángulo. |
| A4 | **SVG inline** (`<svg><path/></svg>`) se importa como relleno de imagen reemplazable (p. ej. el subrayado de pincel). | Aprovecharlo para trazos/líneas decorativas. |
| A5 | `border` → 4 rectángulos finos; sin `border-radius`. | Borrar los 4 e `insert_shape` con path redondeado. |
| A6 | `text-transform:uppercase` se pierde si el div tiene hijos con otro estilo (`<i>`). La 1.ª región puede tomar el tamaño del hijo. | Escribir en mayúsculas en origen o corregir con `find_and_replace_text` + `format_text`. |
| A7 | `transform`, gradientes, sombras, `filter`: no fiables. | Prohibidos en el HTML (lint). Centrar con `left` explícito; hornear efectos a imagen. |
| A8 | Cada importación **crea un diseño nuevo** en la cuenta; no hay herramienta para borrarlo. | Importar lo mínimo; avisar al usuario de los intermedios. |
| A9 | Tamaño del diseño = tamaño de la página HTML (`custom`); `presentation` si 1920×1080. | Fijar `.page{width,height}` en px reales. |
| A10 | `data-label` de la página pasa a ser el **título de página** en Canva (y se conserva al pasar la página con `merge-designs`). | Nombrar bien las páginas; `edit-design` no puede renombrarlas después. |
| A11 | **Fuentes**: solo resuelve las de la biblioteca pública de Canva (Roboto sí). La fuente del Brand Kit (p. ej. una fuente institucional de la marca) **no** se asigna con ningún nombre de `font-family`, con o sin `@font-face` (15 pruebas) → fallback tipo Arial. | Ver `08` §4: decidir con el usuario; no subir TTF. |
| A12 | Un HTML con páginas de **tamaños distintos** importa como **un solo diseño de tamaños mixtos**. | Un HTML por programa con las páginas en orden. |

## B · Edición (`edit-design`)

| # | Hecho | Qué hacer |
|---|---|---|
| B1 | **No existe operación para fuente ni espaciado entre letras.** `format_text` solo: color, tamaño, negrita/cursiva, subrayado, alineación, interlineado, listas, enlace. `add_text` crea con la fuente por defecto. | No crear texto nuevo por API cuando importa la fuente de marca; importar HTML. Si hay que añadir texto, avisar al usuario de que la fuente la cambia él en Canva. |
| B2 | `format_text` afecta **a todo el cuadro** (todas las regiones). | Para cambiar una parte: `find_and_replace_text` (respeta región) o dividir en dos cuadros. |
| B3 | `locator_id` = `PAGEID-ELEMENTID`; los ids **cambian** tras `merge-designs` / reimportación. | Releer con `read-design` + transacción antes de editar. |
| B4 | Todo lo insertado (`insert_fill`, `insert_shape`) entra **en primer plano**. | `layer_element back`: ornamentos primero, fondo al final. |
| B5 | `update_fill` sobre un rect conserva posición/z-order y escala la imagen a ~1,02× (sangrado de ~20 px). | Usarlo para el fondo. Para imágenes que deben quedar exactas, `insert_fill`. |
| B6 | `insert_fill` acepta `left/top/width/height` y respeta la proporción; si das una proporción distinta, **estira**. | Calcular alto = ancho × (h/w del archivo). |
| B7 | `insert_shape.path` solo `M L H V C S A Z`. Sin `color` ⇒ sin relleno (útil para marcos). | Marcos redondeados con arcos `A`. |
| B8 | Cada llamada devuelve `edits_unverified` + miniatura baja resolución: **hay que mirar** antes de seguir. | No encadenar 10 páginas a ciegas. |
| B9 | `commit` y `cancel` van **solos** (sin operaciones). `update_title` va como operación normal. | Última llamada = commit. |
| B10 | Una transacción abierta y no confirmada **no** se guarda. | Siempre cerrar con commit o cancel. |
| B11 | `update_fill` con un SVG falla («Only raster images…»). | `insert_fill` del SVG y borrar el marcador, o subir PNG grande. |
| B12 | `update_fill` agranda la imagen ~2 %. | `crop_media` con `left:0, top:0, width:W, height:H` del propio elemento (coordenadas relativas al elemento). |
| B13 | `edit-design` no renombra páginas existentes (`update_title` = título del diseño; `add_page.title` solo para páginas nuevas). | Reemplazar páginas por importadas con `data-label` correcto. |
| B14 | `update_title` exige `page_index`. | Pasarlo siempre. |

## C · Posicionamiento: Canva ≠ navegador

| # | Hecho | Compensación |
|---|---|---|
| C1 | Con `line-height:1`, Canva coloca el glifo ~**0,1 em más abajo** que Chrome (Montserrat ExtraBold). | `top_canva = top_html − 0,1·font-size` en numerales/títulos grandes. Verificado a 290, 300, 350 y 470 px. |
| C2 | Cuadros con ancho justo **parten** la línea ("Y" / "Color"). | Ancho de caja ≥ 1,15 × ancho real del texto (`resize_element`). |
| C3 | Alturas de caja las calcula Canva (`height` autocalculado); no fijar alto en texto. | Solo `width`. |
| C4 | `letterSpacing` se conserva (0,62 = 0,62 em). | Sin truco necesario. |

## D · Otras herramientas

| Herramienta | Hecho |
|---|---|
| `merge-designs` | **Una sola operación por llamada** (error literal «Only a single operation per merge request is supported»). `insert_pages` desde otro diseño (tamaños distintos OK; conserva tamaño y título); con `after_page_number` las páginas quedan en **orden invertido** → `move_pages` con `from_page_numbers` en orden inverso; ids cambian tras cada operación; `delete_pages` es permanente → aprobación por operación. |
| `copy-design` | Copia un diseño completo (mismo título; renombrar con `update_title`+`commit`). Úsalo para probar merges/ediciones sin tocar el original. |
| `upload-asset-from-url` | Acepta JPG/PNG/SVG; devuelve `asset id` y dimensiones. 5 MB y 4000×1700 PNG funcionaron. |
| `export-design` | `png` con `width/height` exactos devuelve una URL por página (caducan en horas): descargar enseguida. Con **tamaños mixtos NO pasar width/height** (da cada página a su tamaño nativo); `pages:[…]` exporta un subconjunto. |
| `read-design` | `open_transaction:true` + `design_content` da todos los elementos; sin transacción solo lectura. `thumbnails` baja resolución. Un diseño de 6 páginas con transacción pesa ~55k caracteres (se desborda a archivo): para leer solo títulos/tamaños usar `element_ids:["LBnoexiste"]` y cerrar con `edit-design finalize:"cancel"`. |
| `list-brand-kits` | ~30k tokens (todos los kits de la cuenta) y **no** lista fuentes: evitarlo. |
| `resolve-shortlink` | `canva.link/xxxx` → URL completa del diseño; `read-design` acepta el id `DA…`. |

## E · Navegador y render local

- El **navegador integrado del panel** abre archivos locales como instantánea `data:`: no carga imágenes relativas ni Google Fonts → no sirve para QA. Usar `scripts/render_html.sh` (Chrome headless). Desde `bash` directo; desde `subprocess` de Python hubo capturas en blanco con Edge.
- Google Fonts debe cargar (internet) para que el render muestre Montserrat/Playfair.

## F · Rutas alternativas (NO ejercitadas — verificar antes de prometer)

El conector expone más herramientas que no se usaron: `generate-design`, `create-design`, `generate-design-structured`, `autofill-design`, brand templates, `resize-design`, `copy-design`, comentarios, `search-designs`, `list-brand-kits`. Antes de usar una: `ToolSearch` para cargar su esquema, probar en un diseño de prueba, y documentar resultado y límites en `CHANGELOG.md` + `HANDSHAKE.md`. Hasta entonces, el camino por defecto es el pipeline de `01`.
