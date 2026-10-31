# Scripts de terceros (vendor)

Copias **sin modificar** de scripts con licencia MIT. Para actualizar: volver a copiar desde el commit nuevo, correr las pruebas de `HANDSHAKE.md` y anotar el cambio en `CHANGELOG.md`. No editar aquí; los arreglos propios van en `scripts/verificar_vectorizado.py` o en un envoltorio.

| Carpeta | Repositorio | Commit | Fecha del commit | Licencia | Archivos |
|---|---|---|---|---|---|
| `pixel2svg-html/` | `github.com/nolangz/pixel2svg-html` | `ab14240` | 2026-06-26 | MIT © 2026 Nolan Lai | `raster_logo_trace.py`, `render_overlay.py`, `svg_path_audit.py`, `fit_ribbon_centerline.py`, `overlay_progress_strip.py`, `svg_to_js_html.py` |
| `logo-design-skill/` | `github.com/kaankiziltug/logo-design-skill` (`skills/logo-design/scripts/`) | `7340903` | 2026-10-20 | MIT © 2026 kaankiziltug | `svglib.py`, `svg_audit.py`, `concept_sheet.py`, `preview_sheet.py`, `presentation_board.py`, `render_png.py`, `export_variants.py` |

Omitido a propósito de `logo-design-skill`: `search_library.py`, `build_catalog.py` y la biblioteca de logos (marcas registradas de terceros). Por eso `preview_sheet.py --refs-industry` y `svg_audit.py` (comparación de complejidad) no tienen datos de biblioteca; el resto funciona.

Notas de uso en Windows: los scripts sueltos que renderizan (`render_overlay.py`, `render_png.py`, `preview_sheet.py`) buscan un navegador con `CHROME_BIN`; `scripts/verificar_vectorizado.py` lo detecta solo.
