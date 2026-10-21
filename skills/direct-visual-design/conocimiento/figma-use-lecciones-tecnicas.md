# Lecciones técnicas HTML → Figma con `use_figma` (verificadas 2026-10-09, proyecto caso-landing-industrial-01)

> Origen: paso a Figma de la página agrupadora de caso-landing-industrial-01 (573 nodos, 9 secciones). Son lecciones de **herramienta**, reutilizables en otros proyectos del método de Guille (1920 / 240 / 80, múltiplos de 4, Fill×Hug, solo styles del archivo).

1. **Antes de construir:** inspeccionar el archivo (styles de fill/texto/efecto con sus IDs, componentes, posición libre en la página). Usar los styles que *ya usan los nodos* (los archivos pueden tener duplicados con el mismo nombre).
2. `figma.createAutoLayout()` crea frames con **relleno blanco** y **clip content ON**: poner `fills = []` en los frames transparentes y `clipsContent = false` en todo salvo carruseles (se verificó con una auditoría final).
3. Aplicar styles con `setFillStyleIdAsync`, `setStrokeStyleIdAsync`, `setTextStyleIdAsync`, `setEffectStyleIdAsync`, `setRangeFillStyleIdAsync`. Cargar fuentes antes de tocar texto.
4. Orden: crear → `appendChild` al padre auto-layout → recién entonces `layoutSizing* = FILL/HUG`. `resize()` **resetea** `layoutGrow`/sizing: llamarlo antes.
5. Un hijo `FILL` vertical dentro de un padre `HUG` **no se expande**; usar HUG. Para fijar un elemento abajo en una tarjeta de altura igualada: agrupar el contenido en un frame y usar `primaryAxisAlignItems = 'SPACE_BETWEEN'` (los spacers con `layoutGrow` fallan).
6. Clonar un componente/menú que en el origen es hijo **absoluto**: `layoutPositioning = 'AUTO'` tras insertarlo.
7. Componentes con propiedades: `instancia.setProperties({...})`; el swap de icono por propiedad no funcionó → `hijo.swapComponent(comp)`. Los iconos suelen ser de **trazo**: recolorear con `setStrokeStyleIdAsync`.
8. Iconos propios: `figma.createNodeFromSvg(svg)` + aplicar style a strokes/fills.
9. **Imágenes:** nunca `createImageAsync`. Crear un `RECTANGLE` en su lugar y usar la herramienta `upload_assets` (`nodeIds`, `scaleMode FILL`), luego `curl -X POST -H "Content-Type: …" --data-binary @archivo <submitUrl>`. No clonar nodos con imágenes de otros frames (el clon puede cambiar de foto/altura).
10. Hipervínculos: `texto.setRangeHyperlink(0, n, {type:'URL', value})` (también sobre texto dentro de una instancia); en frames, `reactions` con acción `URL`.
11. Scripts **no idempotentes**: si fallan a medias, borrar lo creado antes de reintentar.
12. Verificación: `get_screenshot` por sección y auditoría por script (fills sin style, text sin style, clip, múltiplos de 4, tamaños Fill/Hug).
13. Un style de gradiente puede **verse distinto** (otra dirección) al aplicarlo a nodos nuevos respecto de un nodo original: comparar y avisar, no sobrescribir con un paint propio.

## Lecciones del 2026-10-19 al 2026-10-21 (proyecto caso-web-salud-01)

> Origen: sitio de salud pasado de HTML aprobado a Figma en tandas (home, 4 internas, blog, móvil, flujo de reserva), con librería propia (variables, 23 estilos de texto, ~35 componentes). Todo verificado con errores reales de `use_figma`.

**Límites del canal (MCP)**

14. **La respuesta de `use_figma` tiene un tope de 48 000 bytes.** Si el `return` lo supera, **los cambios del script no se guardan** («Canvas edits from this run were not committed»). Devolver solo IDs, conteos y medidas; los volcados grandes van en un script de solo lectura aparte y paginado.
15. **Salto de línea manual (U+2028):** escribirlo siempre como `String.fromCharCode(0x2028)` (o `'\u2028'`). Pegado literal en el script, JavaScript lo toma como fin de línea y falla («Unterminated regular expression», «unexpected line terminator»). Y al **devolver** textos que lo contienen, la respuesta del MCP se corta («Failed to parse SSE message … EOF while parsing a string»): reemplazarlo por `⏎` u otra marca antes de devolver.
16. **Espacio duro (U+00A0)** con `String.fromCharCode(0x00A0)` para evitar viudas igual que el `&nbsp;` del HTML. Figma corta las líneas distinto al navegador (Newsreader/Montserrat, por ejemplo): comparar la captura y poner saltos manuales donde el HTML lleva `<br>` o donde el corte difiere.
17. **`figma.mixed` es un símbolo:** leer `fontSize`, `fontName`, `cornerRadius`, etc. de un nodo con valores mezclados y concatenarlo o serializarlo da «cannot convert symbol to string». Comprobar `=== figma.mixed` antes, o leer por rangos con `getStyledTextSegments`.

**Instancias y componentes**

18. **No se puede meter nada dentro de una instancia** (`appendChild`/`insertChild` → «New parent is an instance or is inside of an instance») **ni mover sus hijos** (`x`/`y` → «cannot be overridden in an instance: relative-transform»). Si una instancia necesita una parte opcional (texto de ejemplo, icono), se agrega **al componente principal** como capa oculta con propiedad booleana (`Show placeholder`, `Show icon`) + propiedad de texto, apagada por defecto, y se activa en la instancia. Pedir la orden antes de tocar un maestro.
19. `createInstance()` solo existe en `COMPONENT`: para repetir un frame suelto, `clone()`; para reutilizar de verdad, convertirlo antes en componente.
20. **Convertir un bloque aprobado en componente:** crear el componente desde el frame del diseño, añadir propiedades de texto (`Title`, `Label`, `Description`…) con `addComponentProperty` y enlazarlas a los textos (`componentPropertyReferences`), exponer las instancias anidadas (`isExposedInstance = true`) para editar su `Label` desde arriba, escribir la `description` de uso, y **reemplazar en las páginas los frames sueltos por instancias** (luego borrar el frame suelto). Así quedaron Booking card, Card/Approach, Card/Post, Form field y Progress bar.
21. Ítem activo de un menú que es instancia: override de color **y** de peso en la instancia (el resto conserva el peso del maestro); no crear una variante por página.
22. **Cambiar un maestro afecta a todas las páginas** y el clasificador de permisos puede bloquearlo como «Modify Shared Resources»: solo con orden explícita del usuario, y después revisar las alturas de las páginas que lo usan.

**Auto Layout y medidas**

23. Un frame de Auto Layout nuevo y vacío nace con **100 px de alto**: no usar «spacers»; resolver con `gap`, padding o ancho fijo (p. ej. un campo a media columna con ancho fijo en vez de campo + spacer).
24. `minHeight`/`maxHeight` heredados (de un clon o de una edición del usuario) **bloquean `resize()`** sin error: ponerlos en `null` antes.
25. Un clon arrastra alto `FIXED` y paddings del original: tras clonar, revisar `layoutSizingVertical = 'HUG'` y los paddings.
26. **Lo que Auto Layout no expresa** (filas de grilla que abarcan dos, zigzag de línea de tiempo con eje continuo): frame contenedor **sin** Auto Layout con los hijos colocados en las posiciones medidas en el HTML al ancho de diseño (`getBoundingClientRect`), y cada hijo **con** Auto Layout por dentro. Documentar por qué.
27. Los IDs cambian cuando una sección se rehace: volver a leer la estructura antes de usar un ID anotado en una sesión anterior («node … does not exist»).

**Contexto, propuestas y verificación**

28. **Pop-up o modal en contexto:** frame del tamaño del viewport (p. ej. 1440 × 900) con recorte, **copias editables** del header y las primeras secciones de la página de fondo (no una captura plana, aunque el usuario diga «puede ser un screenshot»: ofrecer las copias), un rectángulo `Backdrop` con el mismo color y opacidad del `::backdrop` del CSS y el panel centrado con la sombra del HTML.
29. Varias propuestas del mismo paso (A pop-up / B página): frames hermanos con el mismo contenido y las mismas medidas, nombrados `Propuesta · variante / Desktop <ancho>`.
30. **Verificación por alturas:** medir cada sección del HTML al ancho del frame y comparar con Figma; se dio por buena una diferencia de 0–4 px en páginas de 3000–8000 px. Una captura por sección o frame terminado; no repetir si nada cambió.
31. Fuente de iconos que no existe en el archivo (Material Symbols Outlined): usar la familia disponible más cercana (Rounded Light) y anotarlo como diferencia conocida.
