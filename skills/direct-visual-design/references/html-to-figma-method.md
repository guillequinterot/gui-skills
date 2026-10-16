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
