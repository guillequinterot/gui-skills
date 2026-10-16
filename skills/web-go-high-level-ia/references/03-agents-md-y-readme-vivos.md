# 03 · `AGENTS.md` y `README.md` vivos (la memoria dentro del proyecto)

La IA del constructor **lee `AGENTS.md` antes de trabajar** (el bloque `VIBE:BEGIN…END` lo pone la plataforma: **conservarlo intacto y arriba**). El `AGENTS.md` que genera el constructor está casi vacío; hay que escribirlo.

## `AGENTS.md` (reglas — cambia poco)
Secciones del caso `caso-web-universidad-01` (plantilla en [`../templates/AGENTS.template.md`](../templates/AGENTS.template.md); la versión real completa vive solo en el proyecto del cliente y no se publica):

0. **Memoria del proyecto: README.md (obligatorio):** leer README antes de cada tarea; **al terminar, actualizarlo sin que lo pidan** (estado, pendientes, próxima acción, fecha, entrada en el registro). «Una tarea no está terminada hasta que el README refleja lo que hiciste.»
1. Qué es el proyecto + tabla de páginas/estado.
2. **Reglas de oro:** no inventar, no prometer, no cambiar lo aprobado, una sola fuente de datos, español/tono, accesibilidad.
3. **Pila y qué NO tocar** (archivos protegidos; no Tailwind/shadcn en páginas de marca; nombres de clase que chocan con Tailwind; sin barra final en URLs).
4. **Mapa del código** (qué hace cada archivo).
5. **Sistema de diseño:** tokens, tipografías, espacio, piezas del kit, motivos de marca, reglas de composición, interacciones ya resueltas.
6. **Imágenes:** solo reales de la marca; siempre `img()`; el CDN renombra → `IMG_URLS`; nombres, `alt`, `width/height`, formato.
7. **Datos y contenido:** oferta vigente, slugs, fechas, qué NO mostrar, enlaces permitidos, pendientes del cliente.
8. **SEO por página:** plantilla de `head()`, schema, `noindex` provisional, enlazado.
9. **Formulario, CRM y medición:** campos, IDs (no cambiar), `data-track`, scripts pendientes.
10. **Cómo agregar páginas** (listado, ficha dinámica, etc.; `<ruta>_.$slug.tsx` para no anidar).
11. **Checklist de revisión** antes de dar algo por terminado (incluye «README actualizado»).

## `README.md` (estado — cambia siempre) = handoff + handshake del proyecto
Plantilla en [`../templates/README.template.md`](../templates/README.template.md); ejemplo sanitizado de la estructura en `../ejemplos/caso-web-universidad-01/README.md`.

1. **Estado actual:** tabla de páginas (ruta, archivo, ✅/🟡/⬜/🔴) y qué funciona.
2. **Handoff:** contexto, decisiones (no reabrir), pendientes del cliente `[ ]`, pendientes técnicos, **«En curso»**, próxima acción.
3. **Handshake:** quién interviene (persona / Claude Code / IA del constructor), **protocolo** (antes: leer; durante: no rediseñar; al terminar: actualizar), formato de una entrada del registro, datos de operación (vista previa, edición manual, no Ctrl+S, no «Publicar»).
4. **Registro de cambios** (solo se agrega): fecha · quién · qué · por qué · cómo se comprobó · qué queda.

## Cómo se mantiene
- La IA del constructor lo actualiza tras cada tarea (orden en `AGENTS.md` §0). Claude Code lo actualiza cuando edita en local y **pega** la versión nueva (esperar a que la IA no esté escribiendo para no pisarla).
- Comprobar de vez en cuando que la IA lo siga cumpliendo (pedirle una tarea pequeña y ver si deja su entrada).
- Si README y código discrepan, **gana el código**: corregir el README.
- Lo largo y de agencia (HANDOFF/HANDSHAKE de la carpeta del proyecto, notas de Obsidian si las usas) **no** se duplica aquí; el README es corto y factual.
