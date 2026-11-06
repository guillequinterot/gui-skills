# Inbox de aprendizajes (candidatos, NO promovidos)

Un aprendizaje solo pasa a `preferencias-illustrator-aprobadas.md` con aprobación explícita del usuario o repetición en varios casos.

| Fecha | Candidato | Evidencia | Estado |
|---|---|---|---|
| 2026-10-11 | Diseñar los **arcos/asas** como SVG en el HTML para que no nazcan recortes al exportar. | Asa de la bolsa de caso-manual-marca-01: 5 recortes → 1 arco | candidato |
| 2026-10-11 | Generar los **PDF por lámina y el maestro después** de la limpieza y del Tamaño automático (no antes) para no entregar versiones con recortes. | PDF de `export/illustrator/` generados antes de limpiar | candidato |
| 2026-10-11 | Avisar siempre antes de operaciones que **mueven el ratón** o abren Illustrator ~15 min. | Clic automático del cuadro; cierre inesperado de Illustrator | candidato |
| 2026-10-11 | Un solo documento maestro por proyecto (`.ai`) como versión buena; los PDF se regeneran desde él. | Proceso caso-manual-marca-01 | candidato |

## 2026-11-06 · caso-planos-01 (candidatas, sin aprobar)

- Un documento que ya viene de un PDF y está montado se arregla **en sitio** (mismo contenedor, mismo apilado): el flujo de Chromium (todo a la raíz) rompe grupos y recortes.
- Un recorte de página casi siempre «recorta» por culpa de **un solo texto que se sale**: arreglar ese texto libera todos los recortes de página.
- Lo que un recorte esconde por completo se **aparta** a una capa oculta y bloqueada; no se borra en silencio.
- Verificar el texto contra el PDF original por multiconjunto de caracteres (NFKC, sin espacios) es más fiable que mirar.
- Reducir el tamaño de un bloque de texto para que quepa en la página es una decisión de diseño: avisar siempre.

