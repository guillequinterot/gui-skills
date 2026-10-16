# 08 · Montaje multipieza (varios formatos y programas) y el problema de la fuente de marca

Aprendido en el caso **`caso-piezas-universidad-01`** (2026-10-09): 36 programas × 2 diseños × 3 formatos (Post 1080², Historia 1080×1920, Banner 1200×628) = 216 piezas. Verificado con un montaje real en una **copia** del Canva del usuario (el original no se tocó). Complementa `01` (proceso base) y `02` (límites del conector). Detalle del caso: `ejemplos/caso-piezas-universidad-01/` y `proyectos/caso-piezas-universidad-01.md`.

## 1 · Estrategia general para producir mucho

1. **Un motor, no 216 HTML a mano.** Un script (ver `ejemplos/caso-piezas-universidad-01/herramientas/motor_series.py`) recibe una config por programa (paleta, fotos, variantes) y el texto del sheet, **mide el texto con las TTF reales**, fluye la columna sin solapes (reduce tamaño si no cabe), hornea el fondo (foto + scrim; el HTML no admite gradientes) y emite HTML Canva-ready. Se aprueba un programa de prueba y luego se escala.
2. **Orden de trabajo acordado**: (a) todos los HTML con las imágenes que haya (placeholders donde no hay) → (b) fase de imágenes (stock/Magnific/Adobe) que **reemplaza archivos** y regenera → (c) montaje en Canva por tandas. Así el montaje se hace una sola vez.
3. **Nomenclatura de página** `N-F-slug-<marca>-cX` (N = nº del programa, F = P/H/B, X = variante). Va en `data-label` de cada página del HTML: **Canva la usa como título de página** (ver §3).
4. **Un HTML por programa con sus páginas en orden** (P1,H1,B1,P2,H2,B2) importa como **un solo diseño de tamaños mixtos**; no hace falta un HTML por formato.

**Imágenes por diseño (regla del usuario en `caso-piezas-universidad-01`):** cada diseño (variante c1/c2) lleva SU juego de imágenes, compartido por sus 3 formatos; las dos variantes de un programa no repiten imagen. El motor detecta por convención `assets/img-cX-fondo.jpg` y `img-cX-persona.png` y los antepone a la config: la fase de imágenes (stock/IA) solo suelta archivos con esos nombres y regenera. Masters recomendados: cuadrados ≥ 3000×3000, sujeto centrado con margen, sin texto.

## 2 · Importar varias páginas de tamaños distintos (verificado)

- `import-design-from-url` con un HTML cuyas páginas (`.page[data-document-role=page]`) miden distinto crea **un diseño con páginas de tamaño propio** (1080², 1080×1920, 1200×628 conservados, una por `data-document-role="page"`).
- `<img>` y `background:url()` **no** se importan. **Flujo B (el barato):** `scripts/prepare_multipage_import.py` sustituye cada `<img>` por un `<div>` gris (#7f7f7f) con el **mismo left/top/width/height** y escribe un manifiesto JSON. El importador trae esos rects con posición exacta **y en el z-order correcto** → no hace falta `layer_element`.
- Rellenado por página, **una llamada `edit-design` con todas las operaciones**: `update_fill` del rect placeholder con el asset subido **+ `crop_media`** con `left:0, top:0, width:W, height:H` **del propio elemento** (coordenadas relativas al elemento; `update_fill` agranda la imagen ~2 % y el crop lo corrige; con coordenadas de página da un imageBox absurdo). Varias páginas pueden editarse en paralelo con la misma transacción. Cada respuesta devuelve el documento completo (~7k tokens).
- **El logo SVG no admite `update_fill`** («Only raster images…»): `insert_fill` (entra al frente) y `delete_element` del marcador; o subir un PNG grande y usar `update_fill`.
- El `.page{background}` llega como un rect blanco de página completa **debajo** de todo (inofensivo).
- Flujo A de `01` (update_fill del fondo + insert_fill + layer_element ×2) da el mismo resultado (diferencia de píxeles 0,1–0,4) pero con el doble de llamadas.
- Reutilizar los `asset id` ya subidos (logos, personas) evita subidas repetidas; ids en `proyectos/<marca>.md`.

## 3 · Llevar las páginas al diseño de trabajo del usuario (`merge-designs`)

- **Probar siempre en una COPIA** (`copy-design`, renombrar con `edit-design update_title` + `commit`; `update_title` exige `page_index`). No modificar el original sin aprobación del usuario.
- **Una sola operación por llamada** (error: «Only a single operation per merge request is supported»), aunque el esquema muestre un array.
- `insert_pages` desde otro diseño de **otros tamaños** funciona: cada página conserva tamaño **y título**.
- **Orden invertido** si se da `after_page_number` (inserción en medio); si se omite (añadir al final) conserva el orden. Arreglo: un `move_pages` con `from_page_numbers` en orden inverso de posición: `{"type":"move_pages","from_page_numbers":[7,6,5,4,3,2],"to_after_page_number":1}`.
- `delete_pages` es permanente → solo con aprobación y sobre las páginas exactas (en la copia: los andamios viejos).
- **Receta**: (1) `insert_pages {after_page_number:N, source:{type:"design",design_id:"<importado>"}}` → (2) `move_pages` → (3) `delete_pages` de los andamios antiguos (quedan desplazados). Los ids de página y de elemento **cambian tras cada operación**: releer antes de editar.
- **Títulos de página**: salen del `data-label`. `edit-design` **no puede renombrar** una página existente (`update_title` renombra el diseño; `add_page.title` solo para páginas nuevas vacías). Por eso se **reemplazan** los andamios por páginas importadas, no se editan.
- Leer solo títulos/tamaños sin elementos: `read-design` con `open_transaction:true`, `filter:{fields:["design_content"],page_indices:[…],element_ids:["LBnoexiste"]}`; cerrar con `edit-design finalize:"cancel"`. Un `read-design` completo de 6 páginas pesa ~55k caracteres y se desborda a archivo.
- `list-brand-kits` devuelve ~30k tokens (todos los kits de la cuenta) y **no** lista fuentes: no usarlo para averiguar tipografías.
- `export-design` PNG **sin** `width/height` entrega cada página a su tamaño nativo (con tamaños mixtos no pasar width/height); `pages:[…]` exporta un subconjunto.
- Tope de páginas: el usuario dividió 36 programas en 4 diseños de 63 páginas (7 por programa con portada). **No verificado** el límite de páginas por diseño de Canva; no prometer «todo en un solo Canva» sin comprobarlo y dar al usuario la lista de URLs de los diseños creados.

## 4 · La fuente de marca NO se aplica al importar (hallazgo clave)

- El importador solo resuelve fuentes de la **biblioteca pública** de Canva. La fuente del Brand Kit (p. ej. una fuente institucional del cliente, que tiene su propio `fontRef` en esa cuenta) **no** se asigna: probados 15 nombres de la familia (con y sin tilde, junto, con sufijos de peso: `<Familia>`, `<Familia> ExtraBold`…) con y sin `@font-face` hospedado → todos caen en el fallback (`YACgEZ1cb1Q,0`, sans tipo Arial). Control: `Roboto` sí mapea. `add_text` usa el mismo fallback; **no existe operación para fijar una fuente**.
- Lo que **sí** conserva la fuente de marca: editar cuadros de texto que **ya** están en esa fuente (`find_and_replace_text`, `format_text`) y duplicar/copiar páginas que ya la tienen (`copy-design`, `merge-designs`).
- Consecuencias de diseño: (a) el fallback es **más ancho** → saltos de línea distintos, párrafos con una línea más, titulares que pisan lo de abajo; (b) el texto queda ~1–2 px más abajo que en Chrome. Mitigación: dejar 8–10 % de margen en las cajas; el generador mide con la fuente de marca (render local fiel) pero el usuario debe saber que en Canva hay que cambiar la fuente.
- **Solución adoptada (verificada por el usuario en `caso-piezas-universidad-01`, 2026-10-09):** tras importar, el usuario cambia la fuente desde el panel de fuentes de Canva y **Canva reconoce la fuente de reemplazo y la sustituye en todo el diseño de una vez**. Para que ese reemplazo sea limpio: **una sola familia tipográfica en todo el texto y pocos estilos (Regular, Bold, Italic)**; si la marca tiene más de una familia, **máximo 2 con estilos casi idénticos** (mismos pesos/cursivas, mapeo 1 a 1). Evitar SemiBold/ExtraBold/Medium/Light.
- Alternativas descartadas por ahora: plantilla con cuadros ya en la fuente de marca + relleno por API (`edit-design`/`autofill-design`; sin verificar) y aceptar el fallback para entrega (contradice la marca).
- Tras el reemplazo el texto usa la misma fuente que el HTML → los saltos de línea coinciden; holgura de cajas ~4–5 %.
- No subir las TTF al hosting (el importador las ignora).

## 5 · Costes y tiempos de referencia (1 programa = 6 páginas)

Hosting + import + subida de ~8 assets: ~3 min · 6 llamadas `edit-design` (~7k tokens c/u) + 1 `read-design` pesado · merge (insert + move + delete): 3 llamadas · export + descarga + comparación: ~2 min. Cada importación deja un **diseño intermedio que no se puede borrar por API**: listarlos al usuario (caso-piezas-universidad-01: 4 en la prueba).

## 6 · Verificación (qué esperar)

Diferencia media (0–255) HTML↔exportación: 7–9 en todo; zonas sin texto 2–5; **zona de texto ~32 mientras la fuente sea el fallback** (no es un fallo de montaje). Revisar a ojo: capas (persona detrás del texto, delante del panel; logo delante), chips con iconos, botón, barra inferior, y titulares largos (historia c2 de 6 líneas llegó a tocar el párrafo con el fallback).
