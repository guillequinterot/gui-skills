# HANDSHAKE — design-logo-vector

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.0.0 |
| Última actualización | 2026-10-31 por guille |
| Skill principal / padre | `direct-visual-design` |
| Llama a | `design-illustrator` (`.ai`/EPS), `canva-design`, `figma:figma-use`, `freepik-imagegen`/`ckm:design` (conceptos como imagen), `video-editing-ai-agent` (logo animado), `design-system-ia`, `rea-reverse-engineer` (por porción) |
| La llaman | `direct-visual-design` (tabla de enrutamiento, fila «Logos y vectorizado»); `design-illustrator` y `canva-design` la usan como fuente del SVG maestro |

## Siguiente paso recomendado

1. En el primer trabajo real: correr `python -I scripts/handshake.py`, seguir `SKILL.md` y anotar en `CHANGELOG.md` cualquier límite nuevo; después `log_job.py` y `publish_job.py`.
2. Probar *vectorizar* con un logo real del mantenedor (idealmente uno con curvas orgánicas o una cinta) para validar la escalera y la compuerta de suavidad fuera de la prueba sintética.
3. Probar *crear* de punta a punta con un brief real hasta el checkpoint.

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `scripts/handshake.py` | verificado | 2026-10-31 | Windows 11, Python 3.12.10; detecta Chrome, Pillow, numpy, OpenCV |
| `scripts/verificar_vectorizado.py` | verificado (prueba sintética) | 2026-10-31 | Logo geométrico de 2 colores: trazo automático → ROJO (166 rectas, 0 curvas), SVG dibujado con arcos → VERDE. Aún sin caso real |
| `vendor/pixel2svg-html/raster_logo_trace.py` | verificado | 2026-10-31 | Genera `logo.svg`, `metrics.json`, `overlay.png`, `logo.html`; IoU 0,9927 en la prueba pero 166 rectas (por eso es medida, no arte final) |
| `vendor/pixel2svg-html/render_overlay.py` | verificado | 2026-10-31 | Necesita `CHROME_BIN` en Windows si el script se llama suelto (`verificar_vectorizado.py` lo detecta solo) |
| `vendor/pixel2svg-html/svg_path_audit.py` | verificado con límite | 2026-10-31 | Aproxima los arcos SVG (`A/a`) con rectas: avisos de unión falsos; el wrapper los omite si hay arcos |
| `vendor/pixel2svg-html/svg_to_js_html.py` | verificado | 2026-10-31 | Genera el HTML; no se abrió en un navegador real en esta prueba |
| `vendor/pixel2svg-html/fit_ribbon_centerline.py`, `overlay_progress_strip.py` | sin probar | — | Solo `--help` |
| `vendor/logo-design-skill/svg_audit.py` | verificado | 2026-10-31 | Sin la biblioteca no compara complejidad; el resto funciona |
| `vendor/logo-design-skill/render_png.py` | verificado | 2026-10-31 | Backend Chrome; PNG de SVG y captura de HTML |
| `vendor/logo-design-skill/concept_sheet.py`, `preview_sheet.py` | verificado | 2026-10-31 | `--refs-industry` NO disponible (necesita la biblioteca upstream); `--refs` con archivos propios sí |
| `vendor/logo-design-skill/export_variants.py` | verificado | 2026-10-31 | Variantes, `favicon.ico`, set web, manifest |
| `vendor/logo-design-skill/presentation_board.py` | verificado | 2026-10-31 | Con el JSON de ejemplo y un SVG de prueba: 10 diapositivas PNG |
| Rutas con IA (`freepik-imagegen`, `images_to_svg`/`images_generate_svg`) | sin probar | — | Documentadas en `references/06`; revisar créditos y existencia de la herramienta antes de prometerlas |
| Animación de logos (traspaso a `video-editing-ai-agent`) | sin probar | — | Solo está el contrato de traspaso |
| Carga en Codex / Antigravity / VS Code | sin probar | — | — |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Cadena completa de vectorizado sobre un logo sintético: medida → trazo inicial → superposición con IoU → auditoría de curvas → semáforo, en Windows con Chrome headless y sin `cairosvg`.
- Hoja de conceptos del checkpoint, hoja de pruebas, variantes de una tinta, favicon/ícono de app/set web y tablero de presentación con mockups.

## Pendientes abiertos

- [ ] Primer caso real de *vectorizar* y de *crear*; registrar con `log_job.py`.
- [ ] Probar `fit_ribbon_centerline.py` con una cinta real.
- [ ] Confirmar las decisiones marcadas «a confirmar» en `HANDOFF.md` §3 (reexpresión + vendor MIT; sin biblioteca ni generador con API).
- [ ] Decidir si se vendoriza también `pixel2motion` (animación) o si basta con el traspaso a `video-editing-ai-agent`.
- [ ] Probar `images_to_svg` (Freepik/Magnific) como nivel 5 y medir su salida con `verificar_vectorizado.py`.
- [ ] Actualizar el `CLAUDE.md` global del usuario (lista de «diez skills» → once, y un párrafo para esta skill); no se editó desde esta sesión.
- [ ] Revisar `tools/privacy_scan.py` y el CI contra los scripts vendor (ver `CHANGELOG.md`).

## Límites conocidos

- No hay biblioteca de logos de referencia: la estantería usa competidores que el usuario o la sesión reúnan.
- El autovectorizado produce polígonos; solo sirve como medida. La calidad final depende del ajuste manual con curvas.
- Un raster de baja resolución o una foto de un logo obliga a **reconstruir**, no a trazar.
- No sustituye la búsqueda marcaria ni valida licencias de fuentes.
- `.ai`/EPS/PDF editable, Canva y Figma se delegan a sus skills.
