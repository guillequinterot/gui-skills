# HANDSHAKE — web-go-high-level-ia

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.3.0 (1.2.0 + migración al repo gui-skills) |
| Última actualización | 2026-10-16 por guille |
| Skill principal / padre | `direct-visual-design` y `seo-content-system` (es sub-skill de las dos) |
| Llama a | `direct-visual-design` (dirección visual, QA de diseño), `seo-content-system` (title, meta, H1, alt, schema, `noindex`, enlazado) |
| La llaman | `direct-visual-design`, `seo-content-system` |

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Claude in Chrome (operar el builder de punta a punta) | verificado | 2026-10-14 | Solo en Chrome (no Arc). El builder vive en un iframe de otro origen: se opera por coordenadas (captura de 1568 × 726). Receta completa en `references/07` §L |
| Pegado por portapapeles en el editor + «Guardar» | verificado | 2026-10-13 | 22 archivos. Con trampas E2–E5 y E9; **nunca Ctrl+S** (escribe una «s») |
| Subida de carpetas e imágenes a Medios con `file_upload` | verificado | 2026-10-14 | 17 fotos; la carpeta nueva se abre con `double_click` por `ref` |
| Emparejar URL de Medios ↔ originales (`scripts/match_cdn.py`) | verificado | 2026-10-14 | 32/32 y 17/17 exactos por SHA-256 |
| `scripts/make_partes.py` (partes genéricas) | verificado | 2026-10-16 | Probado con un proyecto de muestra (3 partes, modos crear / reemplazar / anexar); los generadores específicos que sustituye se usaron en el caso real |
| Chequeo de tipos estricto en copia aparte | verificado | 2026-10-13 | Quedan solo errores de `routeTree.gen.ts` desactualizado (J1) |
| Servidor local (Vite) + capturas con Chrome headless (`scripts/cshot.sh`, `qa_visual.py`, `overflow.html`) | verificado | 2026-10-13 | Edge headless falla si el usuario tiene Edge abierto (F8); Chrome headless no baja de ~500 px de ancho (K6) |
| Preflight (`scripts/handshake.py`) | verificado | 2026-10-13 | Versión original; en esta migración solo se compiló y se ajustó para avisar (no fallar) fuera de Windows |
| `scripts/manifest_imagenes.py` | verificado | 2026-10-13 | Manifiesto desde los `alt` del código (28/32 con descripción en el caso) |
| «Descargar base de código» | verificado | 2026-10-14 | Deja un `.tmp` sin extensión (L6); no extraer `.env` |
| API de GHL para crear páginas | no aplica | 2026-10-13 | No crea páginas: por eso el camino es HTML + kit + partes |
| Windows | verificado | 2026-10-13 | Toda la receta |
| macOS / Linux | sin probar | — | `pbcopy` en lugar de `Set-Clipboard`, rutas de Chrome y coordenadas del editor sin verificar |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Construir una web de campaña completa (Home + listado con filtros + páginas provisionales) en el constructor a partir de HTML aprobado, con tipos estrictos, SEO por ruta y medición real con `data-track`.
- Mantener al día `AGENTS.md` y `README.md` dentro del proyecto como handoff + handshake para la IA del constructor (se escriben y se pegan; ver pendientes sobre su cumplimiento).
- Reconstruir el estado local cuando la IA del constructor reestructura el código al aplicar partes (L5).

## Pendientes abiertos

- [ ] Comprobar que la IA del constructor **cumple** la orden de actualizar el `README.md` tras cada tarea (hasta ahora solo se escribió y se pegó).
- [ ] Invocar la skill en una sesión nueva tras la migración al repo y confirmar que `direct-visual-design` y `seo-content-system` la invocan solas.
- [ ] Documentar cómo se crea un archivo nuevo en el editor (si existe «nuevo archivo»); hoy se le pide a la IA del chat con las partes (07 §L, `AGENTS.md` §10).
- [ ] Probar `scripts/make_partes.py` con un proyecto real del constructor (solo se probó con uno de muestra).
- [ ] Repetir el flujo en un segundo proyecto para convertir las reglas candidatas del `HANDOFF.md` en reglas.
- [ ] Validar la receta en macOS y en otras resoluciones o idiomas del editor.

## Límites conocidos

- **«Publicar» nunca se ha pulsado a propósito**, y **el dominio propio nunca se ha probado**: no se sabe cómo se comporta la publicación ni el `noindex` que inyecta `vibepreview.app` desaparece (E12) hasta que se haga con el permiso expreso del usuario.
- El constructor no deja subir archivos al proyecto: solo imágenes (≤ 5) y texto (≤ 50 000 caracteres por mensaje) en el chat, y edición de código a mano.
- No se puede leer el código del editor con `get_page_text` (iframe de otro origen): hay que descargar la base de código o ver capturas.
- Las coordenadas del editor dependen del tamaño de la ventana de captura; si cambia, tomar una captura completa y recalcular.
- No hay uso verificado en Codex / Antigravity / VS Code ni en macOS.

## Supuestos vigentes

- Claude in Chrome en Chrome (no Arc); el usuario tiene el proyecto abierto en `?view=codeEditor`.
- El usuario sube las carpetas de imágenes a Medios y usa «Insertar enlaces» (o `file_upload` desde Claude in Chrome).
- El portapapeles del sistema se puede sobrescribir (y el usuario también lo usa).
