# caso-manual-marca-01 — ficha de Illustrator (manual de marca de 46 láminas)

| Campo | Valor |
|---|---|
| Proyecto | `<carpeta-del-proyecto>/` en la PC del usuario (fuera del repo) |
| Nota Obsidian | En el vault del usuario, si lo usa (fuera del repo) |
| HTML | `paginas/pNN-nombre.html` (46 láminas, 1920 × 1080 px) + `piezas/` (6 piezas) |
| Fuente | Poppins (Light 300 / Regular 400 / Medium 500 / SemiBold 600) — disponible en Illustrator vía Adobe Fonts; en el HTML por Google Fonts |
| Entregables Illustrator | `export/illustrator/caso-manual-marca-01-manual-de-marca.ai` (46 mesas de trabajo, 6 columnas), `caso-manual-marca-01-manual-de-marca.pdf`, `pdf/pNN-nombre.pdf` |
| Estado | `.ai` limpio: 1 028 textos (798 punto / 230 área ajustados), 0 recortes, 0 invisibles, abierto en Illustrator. **PDF generados antes de la limpieza.** |
| Backups | `backups/caso-manual-marca-01-manual-de-marca_antes-de-limpiar-recortes_2026-10-11.ai` |
| Scripts del proyecto (originales) | `scripts/ai_*.ps1`, `ai_fix_text.jsx`, `export_pdf.py`, `extract_paragraphs.py` (las versiones generales son las de esta skill) |

## Decisiones aprobadas

- Solo Poppins en el manual. Mockups vectoriales con HTML/CSS/SVG; fotos y ejemplos de redes = cuadro gris `#D9D9D9`.
- Párrafos = texto de área corrido; Tamaño automático; cero recortes sin sentido (2026-10-11).
- El asa de la bolsa (lámina 41) se redibujó como arco abierto, trazo oliva `#5F5733` de 1 pt.

## Pendientes

- Piezas (`export/piezas/*.pdf`: flyers A5, plantillas de redes) por el proceso.
- Regenerar los PDF desde el `.ai` limpio.
- Sustituir cuadros grises por fotografías (usuario).
- Exportación a Canva (skill `canva-design`) y EPS si se piden.
