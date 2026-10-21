# Método de entrega HTML → Figma (Guille)

Método **general y aprobado** por Guillermo Quintero (2026-10-09) para sitios y landings que se diseñan primero en HTML y después se construyen en Figma. Aplica a cualquier proyecto web salvo que la instrucción actual o el brief digan otra cosa. Los colores, fuentes y componentes concretos **no** son parte del método: salen del archivo Figma de cada proyecto.

## Contenido

1. Orden obligatorio del trabajo
2. Lienzo y retícula
3. Espaciado
4. Auto Layout desde el HTML
5. Estilos: solo los que existen en Figma
6. Componentes existentes
7. Imágenes
8. Paso a Figma
9. Qué no hacer
10. Relación con la memoria y la precedencia
11. Patrones probados al subir a Figma (2026-10-21)

## 1. Orden obligatorio del trabajo

1. **Leer el Figma del proyecto** antes de escribir HTML: estilos de color y texto, variables, componentes (header/menú, footer, botones, cards) y frames de referencia.
2. **Diseñar en HTML** con esas piezas.
3. **Aprobación del usuario** sobre el HTML. Nunca saltarla.
4. **Pasar a Figma** solo lo aprobado, reutilizando estilos y componentes.
5. QA de fidelidad HTML ↔ Figma.

Si falta el archivo Figma o no hay acceso, decirlo y pedir el enlace o los estilos; no inventar un sistema nuevo.

## 2. Lienzo y retícula

- Frame de página: **1920 px de ancho**, alto **Hug** (lo que dé el contenido).
- El contenido vive dentro de los 1920 con **240 px de padding lateral** → ancho útil **1440 px**.
- En HTML: `body` sin márgenes; cada sección a ancho completo (`width:100%`) con `padding: 80px 240px` (o un wrapper interno equivalente cuyo borde izquierdo quede exactamente en x = 240 a 1920 px).
- Fondos de sección a sangre (full-bleed) son válidos: el fondo ocupa los 1920 y el contenido respeta los 240.
- **Si el Figma del proyecto ya fija otro lienzo** (p. ej. frames de 1440 con contenido de 1200 y márgenes de 120), manda el del proyecto: se usa en HTML y en Figma, y se anota en `proyectos/<caso>.md` como excepción del método. El resto de las reglas (80/80, múltiplos de 4, Fill × Hug) se mantiene.

## 3. Espaciado

- **Entre secciones: 80 px de padding superior y 80 px inferior** en cada **sección de contenido**.
- **Exentos del 80/80:** menú/header, hero y footer (aprobado 2026-10-09; el hero se incluyó en la instrucción de ajuste — confirmarlo si hay duda). Su espaciado interno sigue siendo **múltiplo de 4**.
- Todos los paddings, gaps y margins son **múltiplos de 4**.
- Escala habitual: **8, 16, 24, 32, 40, 80, 120** (se admiten 4, 12, 48, 64 si el proyecto ya los usa; siempre múltiplos de 4).
- Alturas fijas de componentes (botones, inputs, iconos) también en múltiplos de 4 cuando sea posible (40, 48, 56).
- Tipografía en px enteros; evitar `rem` fraccionarios (1.9rem = 30.4px) que en Figma producen estilos con decimales.

## 4. Auto Layout desde el HTML

Cada sección se piensa como un frame de Auto Layout:

| Figma | HTML/CSS equivalente |
|---|---|
| Sección: width **Fill**, height **Hug** | `display:flex; flex-direction:column; width:100%;` sin `height` fija |
| Padding del frame | `padding` del contenedor (no márgenes de los hijos) |
| Gap / spacing between items | `gap` en flex/grid |
| Hijo Fill | `flex:1` / `width:100%` / `1fr` |
| Hijo Hug | ancho/alto por contenido (`width:auto`, `fit-content`) |
| Wrap | `flex-wrap:wrap` |
| Absolute position (dentro de Auto Layout) | `position:absolute` solo para decoraciones/insignias |

Reglas derivadas:

- **Preferir `gap` y `padding` sobre `margin`.** Figma no tiene margins: un `margin-top` entre título y texto debe expresarse como gap del contenedor padre.
- Anidar como se anidará en Figma: sección → contenedor → grupos (encabezado, contenido, CTA) → elementos.
- Evitar alturas fijas en secciones y cards salvo que el diseño lo exija (carruseles, medios con proporción).
- Proporciones de imagen con `aspect-ratio` (en Figma: frame con proporción o tamaño fijo + imagen Fill).
- Nombres de clase legibles y semánticos (`hero`, `hero__ctas`, `card`) para nombrar capas al pasar.

## 5. Estilos: solo los que existen en Figma

- Colores, tipografías, tamaños, radios y efectos **salen de los Styles/Variables del Figma del proyecto**.
- En HTML declararlos como custom properties con nombres que mapeen 1:1 con Figma (p. ej. `--color-primary` ↔ `color/primary`, `--text-h2` ↔ `Heading/H2`).
- Si algo que el diseño necesita **no existe** en los estilos: **preguntar siempre** antes de inventarlo. Documentar la respuesta (nuevo estilo aprobado o alternativa existente).
- Nunca escribir hex/tamaños sueltos en componentes si existe el estilo; un único archivo/bloque de tokens.

## 6. Componentes existentes

- Si el header/menú, footer, botones u otros ya existen como componente en Figma, el HTML los **replica fielmente** (misma estructura, medidas, estados) para poder mapearlos después a **instancias** del componente.
- No rediseñar un componente existente dentro de una página; si hay que cambiarlo, proponerlo aparte.

## 7. Imágenes

- Cuando se necesiten imágenes del archivo Figma: **exportarlas desde Figma** (assets/nodos) y usarlas en el HTML con nombres descriptivos.
- Al construir en Figma: colocar las imágenes como **rellenos de imagen** de frames/rectángulos (Fill/Crop según el `object-fit`/`object-position` del HTML), subiéndolas con la herramienta disponible en la sesión.
- Verificar en cada sesión qué herramienta de Figma está disponible (conector MCP oficial, plugin, REST) antes de prometer exportar o subir; si no se puede, decirlo.

## 8. Paso a Figma

1. Crear el frame de página 1920 × Hug con Auto Layout vertical, gap 0.
2. Cada sección: frame Fill × Hug, padding 80/240, Auto Layout según el HTML.
3. **Aplicar o anidar los estilos existentes** (color y texto) como primarios; **crear solo los que falten** y que el usuario haya aprobado.
4. Insertar **instancias** de los componentes existentes (header, footer, botones…).
5. Colocar imágenes como rellenos.
6. **Clip content desactivado** salvo carruseles o recortes imprescindibles (máscaras de imagen, sangrados).
7. Nombrar capas con los nombres semánticos del HTML.
8. Comparar captura HTML vs Figma a 1920 y corregir diferencias.

## 9. Qué no hacer

- Saltar la aprobación del HTML.
- Inventar colores/fuentes que no están en Figma sin preguntar.
- Usar `overflow:hidden` / clip como recurso general (solo carruseles o casos realmente necesarios).
- Valores de espaciado fuera de múltiplos de 4 o rem fraccionarios.
- Estilos inline dispersos y overrides con `!important` por selector de atributo (impiden mapear estilos).
- Contenedores a otro ancho (p. ej. 1160 o 1440 con padding interno que desplaza el texto a x = 304) cuando el método pide contenido en x = 240.
- Detalles que Figma no puede representar sin trucos (máscaras complejas, `mix-blend`, efectos que dependen del cursor) sin marcarlos como "solo web" en el handoff.

## 10. Relación con la memoria y la precedencia

Precedencia (de `learning-and-memory.md`): instrucción actual → brief/guía del proyecto → memoria de marca → **este método (preferencia general aprobada)** → heurística → estilo propuesto por la IA.

Este método se registró como regla general porque el usuario lo **aprobó explícitamente** como su forma de trabajar. Correcciones puntuales de un proyecto (un color, una excepción de padding) quedan en `proyectos/` de la base de conocimiento o en la nota del proyecto en Obsidian, no aquí.

Checklist operativo y validador: `conocimiento/03-checklist-qa-listo-para-figma.md` y `scripts/validate_figma_ready.py`.

## 11. Patrones probados al subir a Figma (2026-10-21)

Salieron de pasar un sitio completo por tandas (home, internas, blog, versión móvil y un flujo de formulario) en `caso-web-salud-01`. Son **forma de trabajar**; los valores de marca siguen en `proyectos/`. Las lecciones de herramienta (`use_figma`) están en `conocimiento/figma-use-lecciones-tecnicas.md` (puntos 14–31).

### Antes de construir

- **Solo bajo orden del usuario.** No preguntar «¿lo paso a Figma?»: el usuario lo pide cuando el HTML está aprobado.
- **Leer el frame destino tal como está ahora:** el usuario pudo haberlo editado a mano (orden de secciones, overrides, componentes nuevos). Partir de su versión y no pisar sus cambios; si el HTML y el Figma difieren, preguntar cuál manda.
- Si el archivo trae estilos/variables importados de un sitio anterior, **no borrarlos**: renombrarlos con prefijo `_legacy …` y ocultarlos de la publicación, y construir con una colección propia (`Brand`) con code syntax `var(--…)` y descripción de uso en cada variable y estilo.

### Construir

- **Una sección = un frame Fill × Hug** con el mismo nombre que la sección del HTML; medidas, paddings y alturas de texto copiadas del CSS a ese ancho.
- **Componentes de la librería como instancias** (header, footer, cierre, botones, tarjetas). Página interna: instancia del header con el ítem activo por override; cierre y footer por instancia con sus propiedades (p. ej. «Show note»).
- **Bloque que se repite o que el usuario pide como componente → componente con propiedades** (texto, booleanas para partes opcionales, instancias anidadas expuestas) y descripción de uso; en la página, reemplazar el frame suelto por la instancia. Los maestros existentes **solo se cambian con orden explícita**.
- **Sin contenido inventado:** donde falta una foto o un GIF, instancia de un componente `Image placeholder` con la etiqueta «Reference image: …» u «Optional image: …»; las plantillas (blog, artículo) llevan solo textos de ejemplo cortos.
- **Sin viudas también en Figma:** los mismos espacios duros y saltos manuales que el HTML.
- **Modales y flujos:** sobre copias editables de la página de fondo con el backdrop del CSS; si hay que decidir entre formatos (pop-up / página completa), un frame por propuesta, uno junto al otro.

### Después de construir

- **Verificar alturas por sección** contra el HTML al mismo ancho y una captura por frame; anotar las diferencias que queden.
- **Anotar «solo web»** lo que Figma muestra en estado inicial: sticky, hover, carruseles con avance automático, acordeones, pop-ups, scroll suave, versiones responsive que no se pidieron en Figma.
- **Bitácora del proyecto:** cada subida se anota en la carpeta del proyecto (p. ej. `04_figma/figma.md`) con fecha, nombre e ID de los frames y componentes creados o cambiados, medidas finales y diferencias conocidas; y una línea en el README del proyecto (lo más reciente arriba). Es lo que permite retomar en otra sesión sin releer el archivo entero.
- **Versión móvil en Figma solo si se pide**; si no, decirlo al entregar («las versiones móviles siguen solo en el HTML»).
- Si otra persona seguirá el diseño dentro de Figma con su agente, empaquetar las reglas del proyecto en **un único `.md`** (el agente de Figma no acepta carpetas ni imágenes) con colores, tipografía, componentes, reglas móviles y un checklist.
