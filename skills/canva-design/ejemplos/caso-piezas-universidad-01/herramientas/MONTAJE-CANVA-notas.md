# Notas del montaje de prueba en Canva — Programa 1 (programa modelo)

Fecha: 2026-10-09. Ejecutado con la skill `canva-design` (pipeline fase 3). Todo se hizo sobre una **copia** del Canva de trabajo; el original solo se leyó (su `updated_at` no cambió).

## 0. Diseños creados en la cuenta (el original NO se tocó)

| Rol | ID | Notas |
|---|---|---|
| Copia de trabajo (resultado final a revisar) | `<id>` | «TEST montaje – copia del Canva de trabajo (1/4)». 63 págs: p1 portada intacta, **p2–7 = programa 1 nuevo**, p8… = resto del original sin tocar. (enlace en la nota de proyecto del usuario) |
| Importado A (6 págs mixtas, con `insert_fill`+`layer_element`) | `<id>` | «TEST montaje (6 paginas mixtas) - importado + assets» |
| Importado B (6 págs mixtas, flujo optimizado con marcadores) | `<id>` | «TEST montaje optimizado (placeholders)». **Es la fuente de las páginas 2–7 de la copia.** |
| Sonda de fuentes 1 | `<id>` | descartable |
| Sonda de fuentes 2 | `<id>` | descartable |

Las 4 últimas (importados + sondas) no se pueden borrar con las herramientas del conector: quedan en la cuenta del usuario (borrarlas a mano). Total importaciones: 4 (límite sugerido ~6).

IDs de assets subidos a la biblioteca de Canva (reutilizables en los otros programas): logo lockup blanco SVG `<id>` · persona.png `<id>` · bg-post-c1 `<id>` · bg-post-c2 `<id>` · bg-historia-c1 `<id>` · bg-historia-c2 `<id>` · bg-banner-c1 `<id>` · bg-banner-c2 `<id>`.

## 1. Resultados clave (resumen)

1. **Un solo HTML con páginas de tamaños distintos SÍ importa** como un único diseño de tamaños mixtos (6 páginas: 1080², 1080×1920, 1200×628 — dimensiones exactas, una por `data-document-role="page"`). No hace falta un HTML por formato.
2. **El título de página sale del `data-label` del HTML** (`N-F-slug-marca-c1`…) y **se conserva** al pasar las páginas con `merge-designs`. `edit-design` NO tiene operación para renombrar una página (`update_title` solo renombra el diseño; `add_page` admite `title` solo para páginas nuevas vacías). Las páginas andamio antiguas conservan su título viejo («01-post-<marca>-…»): no se pueden renombrar → por eso conviene **reemplazarlas** con páginas importadas, no editarlas.
3. **Mecanismo de inserción que funciona: `merge-designs` `modify_existing_design` + `insert_pages`** (tamaños distintos respetados; los ids de página/elemento cambian; los títulos se conservan). Ver §3 (orden invertido y 1 operación por llamada).
4. **FUENTE: NO se puede lograr la fuente de marca con el importador.** Ningún nombre de `font-family` probado mapea a la fuente del Brand Kit (todo cae en el fallback `YACgEZ1cb1Q,0`, una sans tipo Arial; «Roboto» sí mapea, o sea que el importador solo resuelve fuentes de la biblioteca pública de Canva, no las del Brand Kit). Detalle en §4.
5. Fidelidad verificada por exportación: todo coincide con los previews del HTML (fondo, persona, capas, chips, botón, barra, logo) **excepto el tipo de letra** (más ancha → cambian los saltos de línea y en la historia c2 el titular de 6 líneas pisa el párrafo).

## 2. Preflight y herramientas

- `python -I handshake.py` → 14/15 OK (solo faltaba la comprobación de un ejemplo, irrelevante).
- Herramientas Canva (deferred): `ToolSearch select:` con los nombres `mcp__<id-del-conector>__import-design-from-url, upload-asset-from-url, read-design, edit-design, merge-designs, export-design, copy-design, get-export-formats`.
- Ojo: `list-brand-kits` devuelve ~30k tokens (todos los kits de la cuenta) y no lista fuentes: no sirve para averiguar la tipografía; evitarlo.
- `copy-design` (`design_id`) crea copia con el mismo título; se renombró con `edit-design update_title` + `commit` (el `update_title` exige `page_index`).

## 3. Mecanismos y comportamiento del conector (verificado)

### 3.1 Importación (`import-design-from-url`)
- URL `https://<tu-dominio>/_tmp-…/combined.html`, `intended_design_type: "other"`. Resultado: diseño de 6 páginas, tamaños mixtos, `design_type: "unknown"` en las páginas importadas (cosmético).
- `<img>` y `background:url()` NO se importan (como ya se sabía). El `.page{background}` llega como un rect de página completa **debajo** de todo (blanco) → además de los placeholders habrá siempre un rect blanco de fondo; es inofensivo.
- **Truco optimizado (verificado en `<id>`)**: en el HTML sustituir cada `<img>` por un `<div class="layer" style="…;background:#7f7f7f"></div>` (mismo left/top/width/height). El importador los trae como rects con posición exacta **y en el z-order correcto**, así que no hace falta `layer_element` después.
  - `update_fill` sobre el rect placeholder pone la imagen **pero la agranda ~2 %** (imageBox -11 px en un 1080) → corregir con `crop_media` con **`left:0, top:0, width:W, height:H` del propio rect (coordenadas relativas al elemento, no de página)**. (Con coordenadas de página `crop_media` dio un imageBox absurdo de 1600×2374.)
  - **`update_fill` NO acepta SVG** («Only raster images can be used in replacements»): el logo (SVG) se coloca con `insert_fill` (entra al frente, que es lo que se quiere) y se borra su placeholder con `delete_element`. Alternativa: subir el logo como PNG de alta resolución y usar `update_fill`.
- Una llamada `edit-design` por página con todas las operaciones (update_fill+crop_media ×2, delete_element, insert_fill del logo). Varias llamadas a páginas distintas con la misma transacción pueden ir **en paralelo**. Cada respuesta pesa ~7k tokens (devuelve el documento completo).
- Flujo A (el de la skill, 2 llamadas/página): `update_fill` del rect de fondo + `insert_fill` de persona y logo, luego `layer_element back` de la persona (y del panel en las c2) y por último del fondo. También funciona y da el mismo resultado (diferencia de píxeles 0,1–0,4 entre A y B), pero cuesta el doble de llamadas.
- `read-design` con transacción de un diseño de 6 páginas pesa 55k caracteres y se desborda a archivo: se guarda en `…/tool-results/*.txt` (JSON) → leerlo con python (`json.loads(t[t.index('{'):])`) y extraer ids de rects con fill `#7f7f7f`. Para leer **solo los títulos de página** sin elementos: `open_transaction:true`, `fields:["design_content"]`, `page_indices:[…]`, `element_ids:["LBnoexiste"]` → devuelve páginas con `title`/`dimensions` y `elements:[]`. Siempre cerrar con `edit-design finalize:"cancel"`.
- `export-design` `{"type":"png"}` **sin width/height** devuelve cada página a su tamaño nativo (1080², 1080×1920, 1200×628): con tamaños mixtos NO pasar width/height. `pages:[2,…,7]` permite exportar un subconjunto. Descargar con `canva_verify.py download` (nombra `canva-pag-N.png`, hay que renombrar) o con un script propio.

### 3.2 `merge-designs` (probado en la copia)
- **Solo se admite UNA operación por llamada** (error literal: «Only a single operation per merge request is supported»), aunque el esquema muestre un array.
- `insert_pages` desde otro diseño de **tamaños distintos**: OK, cada página conserva su tamaño y su título.
- **Orden**: si se da `after_page_number` (inserción en medio), las páginas quedan en **orden INVERTIDO** (con y sin `page_numbers`). Si se omite `after_page_number` (se añade al final) conserva el orden. Solución: tras insertar, **un `move_pages`** con `from_page_numbers` en orden inverso a la posición actual: `{"type":"move_pages","from_page_numbers":[7,6,5,4,3,2],"to_after_page_number":1}` → deja el orden correcto (el orden de la lista de `from_page_numbers` se respeta).
- `delete_pages` OK (en la copia: se borraron los 6 andamios antiguos y mis duplicados de prueba).
- Receta que dejó la copia como está: (1) `insert_pages` `{after_page_number:1, source:{type:"design",design_id:"<id>"}}` → p2–7 invertidas; (2) `move_pages` como arriba; (3) `delete_pages` de los 6 andamios del programa 1 (que quedaron desplazados 6 posiciones). Los ids de página y de elemento cambian tras cada operación: releer antes de editar.
- Alternativa (b), editar los andamios en sitio, **descartada** como mecanismo principal: ver §4.3.

### 3.3 Hosting temporal
- `temp_host.sh upload` **tiene un bug con varios archivos**: `"$@"` dentro del `eval` llega a `tar` como un único argumento («Cannot stat: a b c») y la carpeta remota queda vacía. Solución usada: crear el DIR con `upload` de un archivo suelto o con el comando y subir con `tar -cf - … | ssh … "cd ~/public_html/$DIR && tar -xf -"` (misma llave/host de la skill). Corregido después en el script de la skill (v1.1.0).
- Subidas esta sesión (todas borradas, 404 verificado, 0 carpetas `_tmp-*` restantes en el servidor): `_tmp-<slug>-xxxxxx` (3 HTML + combinado + assets + logo blanco + fuentes TTF + sonda de fuentes), `_tmp-<slug>-probe` (solo `probe2.html`, texto de prueba), `_tmp-<slug>-ph` (solo `combined-ph.html`). Las fuentes TTF y el HTML de sondas son lo único fuera de la lista literal autorizada (3 HTML + assets + _comun); no contenían datos del proyecto.
- Las **fuentes TTF subidas no sirvieron de nada** (el importador ignora `@font-face`); en próximas subidas no hacen falta.

## 4. Fuente (la fuente de marca): lo averiguado

### 4.1 Qué se probó
Importar texto con `font-family` igual al nombre de la familia de marca en todas las variantes razonables: con y sin tilde, junto o separado, con sufijos de peso (`Bold`, `ExtraBold`, `SemiBold`, `Medium`, `Light`, `Regular`, `Heavy`), con una variante `Serif`, con y sin `@font-face` apuntando a los TTF hospedados. **Todos → `fontRef: "YACgEZ1cb1Q,0"`** (fallback). Control: `Roboto` → sí se mapea a Roboto. Pesos CSS 700/800/600 se traducen a `bold/ultrabold/semibold` (bien), pero sobre la fuente fallback.
- Nombre real de la familia en los TTF (nameID 1/16): el de la fuente de marca sin acentos; los pesos Light/Medium/SemiBold/ExtraBold llevan además un nombre de familia propio «<Familia> <peso>».
- `add_text` por API también usa `YACgEZ1cb1Q,0`. `format_text` no tiene fuente (confirmado).

### 4.2 Cuál es la fontRef real de la fuente de marca en el Canva del usuario
En los textos del andamio del usuario: **`<fontRef-de-la-fuente-de-marca>`** (peso `normal` y `heavy`). Renderiza como la fuente de marca (verificado en la exportación del andamio). Además la portada usa `<fontRef-Roboto>` (Roboto). No hay ninguna operación para asignar una fontRef a un texto.

### 4.3 Lo que SÍ conserva la fuente de marca
Editar los **cuadros de texto existentes** del andamio: `find_and_replace_text` + `format_text` (color, tamaño) mantienen `fontRef <fontRef-de-la-fuente-de-marca>` y el peso `heavy` (verificado en una transacción que luego se canceló). Es decir, una **plantilla en Canva con los cuadros de texto ya creados en la fuente de marca** (título en 2 regiones heavy blanco/verde, párrafo, 3–4 chips semibold, botón heavy, «Sede» italic) permitiría rellenar texto por API sin perder la fuente. Los andamios actuales NO sirven (1–2 cuadros por página, sin chips ni botón). **No verificado**: `replace_text` por regiones en un título de dos colores, y duplicar páginas plantilla con `merge-designs`/`copy-design` (que sí clonan páginas completas con su fontRef: deducido de que los andamios copiados conservaron el fontRef de la fuente de marca).

### 4.4 Opciones para el usuario (decisión pendiente)
1. **Cambio manual de fuente en Canva** por página (seleccionar todo el texto → la fuente de marca, ajustando pesos). Coste: 216 páginas. No automatizable con el conector.
2. **Plantilla con la fuente de marca creada una vez por el usuario** (una página por formato y por variante de layout) + relleno por API (§4.3). Requiere diseñar el layout dentro de Canva en vez de HTML; se pierde algo de libertad. Sin verificar de punta a punta.
3. **Aceptar la fuente fallback** solo para borrador y diseñar el HTML con métricas de esa fuente (el generador debe medir con Arial/Arimo, no con la fuente de marca, para que los saltos de línea de Canva coincidan). Contradice la regla de marca (fuente institucional); no recomendado para entrega.
4. Preguntar a Canva/soporte cómo hacer que el importador resuelva fuentes del Brand Kit (p. ej. si hace falta que la fuente esté en el Brand Kit del **equipo** con un nombre concreto). No se pudo comprobar: los nombres probados cubren los lógicos.

**Para el config del programa:** el nombre de familia tal como figura en los TTF (sin acento) es el correcto para el render local y no cambia nada en Canva; no hay un nombre que funcione. Si se elige la opción 3, ensanchar un 8–10 % el ancho de las cajas de texto y medir con Arimo/Liberation Sans.

## 5. Verificación (exportación de la copia, páginas 2–7)

PNG guardados en `01-programa/canva-export/` (`N-F-slug-marca-c1.png` … `N-F-slug-marca-c2.png`, tamaños exactos 1080², 1080×1920, 1200×628).

Diferencia media (0–255) contra `previews/*.png`: post c1 9,1 · historia c1 8,8 · banner c1 8,3 · post c2 8,3 · historia c2 7,2 · banner c2 8,7 (referencia caso-diplomas-01 8–10). Por regiones sin texto: persona/fondo 2,3–5,0; barra con logo 2,3; zona de texto 32 (fuente). Revisadas visualmente lado a lado: fondos, recortes de la persona, paneles, chips con iconos SVG, botón verde, barra «Sede» y lockup de la marca coinciden. Posiciones del texto ≈ 1–2 px más abajo que en Chrome (no se compensó). Capas OK (persona detrás del texto, delante del panel; logo delante).

**No coincide:** (a) tipografía (fallback tipo Arial en vez de la fuente de marca), con efectos: saltos de línea distintos (p. ej. el titular del post c1 cortaba una palabra más tarde que en Chrome), párrafos con 1 línea más y, en **historia c2**, el titular pasa a 6 líneas y toca el párrafo; (b) «Sede» (italic) queda en la fuente fallback.
**No verificado:** edición manual posterior en Canva; el comportamiento con los 9 programas/63 páginas en un solo import; plantilla con la fuente de marca (§4.3); que las otras 36 páginas del original sigan idénticas (solo se comprobó el tamaño y el conteo = 63 páginas; el original no se modificó).

## 6. Resumen de tiempos y costes (para planificar)
- Hosting + import + 8 uploads de assets: ~3 min. Edición de las 6 páginas con el flujo B: 6 llamadas `edit-design` (~7k tokens cada una) + 1 `read-design` pesado (55k car.) + commit. Merge (insert + move + delete): 3 llamadas. Export + descarga + comparación: ~2 min.
- Reutilizar los `asset id` ya subidos evita 8 uploads por programa (falta subir logo negro y las fotos de cada programa).
