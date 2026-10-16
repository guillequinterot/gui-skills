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
