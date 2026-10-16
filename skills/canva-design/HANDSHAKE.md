# HANDSHAKE — canva-design

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.1.0 (núcleo, 2026-10-09; 1.1.1 y 1.1.2 solo tocaron el ejemplo de serie) |
| Última actualización | 2026-10-16 por guille (migración al repo) |
| Skill principal / padre | `direct-visual-design` |
| Llama a | Principios de `direct-visual-design`; opcionalmente `freepik-imagegen` / Magnific MCP (stock) y una skill de acceso a hosting del usuario |
| La llaman | `direct-visual-design` (tabla de enrutamiento, fila "Cualquier trabajo en Canva"); `design-illustrator` la menciona como hermana |

## Siguiente paso recomendado

1. En el próximo trabajo de Canva real: correr `python -I scripts/handshake.py`, cargar las herramientas con `ToolSearch` y seguir `references/01`; apuntar en `CHANGELOG.md` cualquier límite nuevo.
2. Con el caso `caso-diplomas-01`: cuando el cliente elija D/E/F, borrar las otras 2 páginas (`merge-designs delete_pages`, con aprobación) y actualizar la ficha.
3. Con `caso-piezas-universidad-01`: seguir la ficha del caso; fase actual = HTML → imágenes → montaje por tandas.
4. Probar una de las rutas **no verificadas** (abajo) en un diseño de prueba antes de recomendarla.

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Canva MCP: `import-design-from-url` (HTML multipágina, tamaño custom 2000×1400, `presentation` 1920×1080, páginas de tamaños mixtos) | verificado | 2026-10-09 | Texto real con fuente/tamaño/interletraje; **no** importa imágenes |
| Canva MCP: `upload-asset-from-url` (JPG/PNG/SVG hasta 4000×1700 y ~1,5 MB) | verificado | 2026-10-08 | 12 assets subidos |
| Canva MCP: `read-design`, `edit-design` (`update_fill`, `insert_fill`, `insert_shape`, `layer_element`, `position_element`, `resize_element`, `find_and_replace_text`, `format_text`, `update_title`, `commit`, `crop_media`, `delete_element`) | verificado | 2026-10-09 | Sin operación para fuente ni espaciado; `update_fill` no acepta SVG |
| Canva MCP: `merge-designs` (insert / move / delete pages), `copy-design`, `export-design` PNG por página, `resolve-shortlink`, `list-brand-kits` | verificado | 2026-10-09 | Una operación por llamada; orden invertido con `after_page_number` |
| Hosting temporal por SSH (`temp_host.sh`: subir, verificar, borrar → 404) | verificado | 2026-10-08/09 | La lógica = comandos usados con éxito; el script se probó con `--dry-run` y sintaxis. Requiere configurar `CANVA_TMP_*` (ver `HANDOFF.md` §2) |
| `bake_assets.py` (panel, swoosh, marble, canvas-bg, vignette, logo) | verificado | 2026-10-08 | Reproduce byte a byte 6 de 7 assets reales; `triangles` equivalente (aleatoriedad) |
| `lint_html_for_canva.py`, `build_import_html.py`, `render_html.sh` + `split_pages.py`, `pdf_pages.py`, `canva_verify.py`, `prepare_multipage_import.py` | verificado | 2026-10-09 | Probados con los archivos reales de los dos casos |
| Magnific/Freepik MCP (`stock_search`, `stock_download`, `account_balance`) | verificado | 2026-10-09 | Cada descarga cuesta créditos |
| Frontmatter de `SKILL.md` | verificado | 2026-10-09 | `name` + `description` de 724 caracteres (< 1024), sin `": "` |
| Instalación en Claude Code | verificado | 2026-10-09 | Hoy por enlace desde el repo |
| Activación espontánea ante "Canva" en una sesión nueva | sin probar | — | Se verificó que Claude Code la **listó** tras instalarla; no la activación espontánea ni la invocación por nombre |
| Instalación y uso en Codex / Antigravity / VS Code | sin probar | — | El conector Canva es de la sesión de Claude |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Flujo completo HTML → Canva con todo editable, **demostrado en producción en 4 ejecuciones** (v1 y v2 de `caso-diplomas-01`, y el montaje de prueba y la fase de imágenes de `caso-piezas-universidad-01`); esta skill como tal aún no se ha invocado por nombre en una sesión nueva.
- Importar un HTML con páginas de **tamaños mixtos** como un solo diseño; `merge-designs insert_pages` respeta tamaño y título; `copy-design`; `update_fill` + `crop_media`; `insert_fill` de SVG; export PNG nativo por página.
- Verificación por exportación: diferencia media HTML↔Canva 7–10 (zona de texto ~32 mientras la fuente sea el fallback).
- Contraste WCAG calculado (no estimado) en el caso modelo.

## Pendientes abiertos

- [ ] Probar rutas del conector no ejercitadas: `generate-design`, `create-design`, `generate-design-structured`, `autofill-design`, brand templates, `resize-design`, comentarios, `search-designs`, `get-export-formats`.
- [ ] Probar el pipeline con formatos no horizontales fuera de la serie (post vertical 1080×1350 suelto, historia, A4 vertical) y con plantillas multimarca.
- [ ] Plantilla con cuadros ya en la fuente de marca + relleno por API (`edit-design` / `autofill-design`); reemplazo de fuente en bloque desde el panel de Canva; límite de páginas por diseño; importar 9 programas (54 páginas) de una vez.
- [ ] Ver si Canva Pro/Brand Kit permitiría subir una serif propietaria de marca y usarla (hoy se sustituye por Playfair Display).
- [ ] Decidir si se instala en Codex / Antigravity / VS Code.
- [ ] `caso-diplomas-01`: elegir D/E/F y borrar las otras 2 páginas; resolver 11 vs 8 años, firmante y fecha (decisión del cliente).
- [ ] Sustituir el dominio del hosting temporal por uno con SSL válido solo para pruebas, si el usuario lo consigue.
- [ ] Ejemplo de serie: añadir un config ficticio de programa para que `motor_series.py` se pueda probar sin material de cliente (hoy los configs por programa no están en el repo).

## Límites conocidos

- 100 px/cm como convención de píxeles para piezas físicas.
- Canva compensa el numeral grande ~0,1 em hacia abajo (medido con Montserrat ExtraBold 290–470 px).
- Hosting temporal solo con autorización explícita por tarea; el importador exige HTTPS con certificado válido.
- Los textos del cliente se usan literales.
- Los diseños intermedios que crea la importación no se pueden borrar con las herramientas.
- El importador solo resuelve fuentes de la biblioteca pública de Canva.

## Dónde mirar

- Receta: `references/01-pipeline-html-a-canva.md` · límites: `references/02-...` · caso: `references/07-caso-diplomas-01.md` · serie: `references/08-...`.
- Decisiones y registro de trabajos: `HANDOFF.md` · historial: `CHANGELOG.md`.
- Fichas por caso: `proyectos/INDICE.md`.
