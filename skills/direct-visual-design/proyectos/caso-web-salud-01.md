# caso-web-salud-01

- **Tipo de cliente/marca (genérico):** consulta médica quirúrgica (sitio en inglés de EE. UU.; notas internas en español).
- **Figma (Styles/Variables):** archivo de diseño del proyecto, página principal con un frame por página (`<Página> / Desktop 1440`, `Home / Mobile 390`) y los frames `Components`, `Components / Layout (1440)` y `Accessibility / WCAG 2.2 AA`. Colección de variables `Brand` (color, space, size, radius) con code syntax `var(--…)`; lo importado del sitio anterior quedó como `_legacy …`, oculto y sin borrar.
- **Nota de Obsidian (opcional):** no se usa.

## Excepciones aprobadas al método

- **Lienzo 1440, contenido 1200, márgenes de 120** (el Figma ya venía así), en lugar de 1920/240. Móvil: 390 con márgenes de 24 y secciones de 56.
- Secciones de contenido a 80/80; header, hero y footer exentos.

## Sistema (resumen; la fuente es el Figma)

- **Tipografía:** Newsreader (Display 58/67, H2 40/44, H3 28/36, cita 24/32) y Montserrat (H4 20/28, cuerpo 17/28, cuerpo grande 18/27, pequeño 15/24, botón, eyebrow 14/20 en mayúsculas). Texto mínimo de 14. Estilos `Brand/*` y `Brand/Mobile/*`.
- **Color:** navy-700 `#1B2D5B` (marca), navy-800 `#13214A`, blue-500 `#3B6CC0` (acento en la palabra en cursiva de los títulos), blue-300 `#8FAEE6`, brass-700/500/300 `#85652F`/`#A8854F`/`#C8A774`, cloud `#EFF2F9`, mist `#C9D2E6`, pewter `#646C83`, ink-700/900 `#2A3247`/`#131A2B`.
- **Rasgo de marca:** solo la esquina superior derecha redondeada (botones 20, tarjetas 40, franja de cifras 50, caja de icono 16); las otras tres a 2.
- **Componentes:** header, closing CTA y footer de layout; Button primario/secundario/on brand; Link; Image placeholder; Card/Approach, Study, Quote, Review, Post; Booking card y Booking option; Form field; Progress bar; FAQ item; Filter chip; Chip; Slider arrow; Social/*.
- **Iconos:** Material Symbols Rounded Light (el archivo no tiene la variante Outlined del HTML).

## Decisiones de proyecto (no son regla general)

- Huecos de foto y GIF como `Image placeholder` etiquetados «Reference image: …» hasta que lleguen los materiales; el médico solo aparece con ropa clínica.
- Testimonials y blog en versión **muestra** (no todas las reseñas ni artículos reales).
- Móvil en Figma solo para la home; el resto de las versiones móviles vive en el HTML.
- Flujo de reserva con dos propuestas (pop-up sobre la home / página completa) a la espera de decisión del cliente.
- Bitácora detallada (IDs de nodos, alturas) en la carpeta del proyecto: `04_figma/figma.md`.
