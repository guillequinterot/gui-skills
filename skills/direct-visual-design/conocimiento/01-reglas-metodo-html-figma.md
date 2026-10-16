# Reglas del método HTML → Figma (Guille)

- **Estado:** aprobado como método general por Guillermo Quintero, 2026-10-09.
- **Alcance:** global (todos los proyectos web que se diseñen en HTML para pasar a Figma).
- **Fuente:** instrucción explícita del usuario en conversación (texto resumido abajo).
- **Versión operativa para la skill:** `references/html-to-figma-method.md`.

## Reglas tal como las definió el usuario (resumen fiel)

| # | Regla | Tipo |
|---|---|---|
| 1 | El diseño es a **1920 px de ancho**; el alto es **Hug** (lo que dé el contenido). | Lienzo |
| 2 | Dentro del body, el contenido va dentro de los 1920 px con **240 px de padding lateral**. | Retícula |
| 3 | **Entre cada sección del website: 80 px de padding superior e inferior** (secciones de contenido; menú/header, hero y footer exentos, siempre en múltiplos de 4). | Ritmo |
| 4 | Todos los paddings, gaps y margins son **múltiplos de 4**; escala habitual **8, 16, 24, 32, 40, 80, 120**. | Espaciado |
| 5 | Cada sección pensada para **Auto Layout** en Figma: **width = Fill, height = Hug**. | Estructura |
| 6 | **Evitar clip content / overflow hidden**; solo en carruseles o donde sea realmente necesario. | Estructura |
| 7 | **Primero HTML, se aprueba, y luego se pasa a Figma** (nunca saltar la aprobación). | Proceso |
| 8 | Colores, tipografías y demás **salen de los estilos que ya existen en el Figma del proyecto (Styles/variables)**; si algo no existe, **siempre preguntar** antes de inventarlo. | Estilos |
| 9 | Al pasar a Figma: **aplicar/anidar los estilos existentes** (color y tipografía) como primarios; **solo crear los que falten**. | Estilos |
| 10 | Si el menú/header u otros componentes ya existen en Figma, se **reutilizan como componente**; el HTML los replica fielmente para mapearlos después. | Componentes |
| 11 | **Exportar imágenes desde Figma** cuando se necesiten y buscar la forma de **colocar imágenes en Figma** al construir allí. | Imágenes |
| 12 | Estas reglas son del **método** (generales). Colores/fuentes concretos de una marca son del **proyecto** y no entran como regla global. | Gobierno |

## Reglas derivadas (propuestas por la skill a partir de las anteriores)

Estado: **aprobadas explícitamente por el usuario (2026-10-09)** junto con los aprendizajes de los ejemplos (ver `memoria/preferencias-generales-aprobadas.md`).

Precisión aprobada: el 80/80 aplica a las **secciones de contenido**; **menú/header y footer quedan exentos** del 80/80 (y el hero, según la instrucción de ajuste del validador; confirmar), pero todo su espaciado sigue siendo múltiplo de 4.

- Usar `gap` y `padding` del contenedor en lugar de `margin` entre hijos (Figma Auto Layout no tiene margins).
- Tipografía y line-height en **px enteros**; evitar `rem` fraccionarios.
- Custom properties con nombres que mapeen 1:1 con los estilos/variables de Figma.
- Un único bloque de tokens; nada de hex o tamaños sueltos en componentes.
- Resetear el padding por defecto de `button` (el navegador añade 1 px / 6 px que rompen la regla de 4).
- Elementos clicables como `<a>`/`<button>`, no `div` con onClick (accesibilidad y mapeo a componentes).
- Interacciones imposibles en Figma (efectos que siguen al cursor, blend modes complejos) se marcan como "solo web" en el handoff.
- Fuentes e imágenes como archivos, no base64 dentro del HTML.

## Protocolo de precedencia (sin cambios respecto a la skill)

1. Instrucción explícita actual del usuario.
2. Guía o brief actual del proyecto (incluido su Figma).
3. Memoria de marca aprobada (`proyectos/`).
4. Preferencia general aprobada (este método, `memoria/preferencias-generales-aprobadas.md`).
5. Heurística profesional (p. ej. `references/web-patterns-from-examples.md`).
6. Estilo propuesto por la IA.

No se promueven correcciones puntuales a reglas globales salvo aprobación explícita, repetición en varios trabajos o guía de marca. Este método entra como global **porque el usuario lo aprobó explícitamente**.

## Ejemplo de valores de proyecto (NO son regla)

Ver `proyectos/caso-landing-industrial-01.md`: paleta y tipografías de caso-landing-industrial-01 como ejemplo de lo que vive en un proyecto y no en el método.
