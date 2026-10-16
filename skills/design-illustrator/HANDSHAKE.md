# HANDSHAKE — design-illustrator

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.0.0 (2026-10-11) |
| Última actualización | 2026-10-16 por guille (migración al repo) |
| Skill principal / padre | `direct-visual-design` |
| Llama a | Principios de `direct-visual-design`; consulta `adobe-suite` solo como referencia de API (ExtendScript / Illustrator MCP) |
| La llaman | `direct-visual-design` (tabla de enrutamiento, fila "Cualquier trabajo en Illustrator"); `canva-design` es su hermana |

## Siguiente paso recomendado

1. En la próxima tarea de Illustrator real: `python -I scripts/handshake.py`, leer `references/01` y `02`, y **avisar al usuario** antes de lanzar `ai_pipeline.ps1`.
2. Pasar las piezas del caso `caso-manual-marca-01` (flyers, redes) por el proceso y regenerar los PDF desde el `.ai` limpio.
3. Probar el MCP de Illustrator cuando responda y anotar sus herramientas en `references/04`.

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Control por COM (`Illustrator.Application`) + ExtendScript (`DoJavaScript`) | verificado | 2026-10-11 | Illustrator Beta 31.0.0, interfaz en español; vía principal |
| MCP de Illustrator (`localhost:18412`) | falla | 2026-10-11 | Acepta la conexión TCP y no responde ni a `initialize` (timeout 40-60 s); `claude mcp list` → «connection timed out»; COM es la vía verificada |
| `export_pdf.py` (PDF de Chromium a W × H pt, escala 4/3, texto vivo, 0 raster) | verificado | 2026-10-11 | 46 láminas de 1920 × 1080 pt |
| `extract_paragraphs.py` (bloques de varias líneas del DOM → JSON) | verificado | 2026-10-11 | |
| `ai_fix_text.jsx` / `ai_pipeline.ps1` (letras → líneas → párrafos de área, maestro con pegado y reintento, limpieza de recortes) | verificado | 2026-10-11 | 489 → 25 textos en una lámina; 8/8 párrafos unidos en la lámina de prueba; 230 en el manual |
| `ai_clean.jsx` / `ai_clean_clips.ps1` (limpieza de recortes sin invisibles ni grupos vacíos) | verificado | 2026-10-11 | 427 → 0; 5 «necesarios» reportados y rehechos a mano |
| `ai_autosize_text.ps1` («Tamaño automático» por clic automatizado) | verificado | 2026-10-11 | 230 cajas en el manual y 3/3 en un documento de prueba; mueve el ratón ~10 s |
| `ai_audit.ps1`, `ai_repair_page.ps1`, `ai_merge_open.ps1` | verificado | 2026-10-11 | 2 láminas rehechas con `ai_repair_page.ps1` |
| `verify_fidelity.py` (píxeles y caracteres) | verificado | 2026-10-11 | Peor lámina 4 697 px de 2 073 600; 0 diferencias de caracteres |
| `handshake.py` (preflight: COM, fuente en Illustrator, librerías, MCP) | verificado | 2026-10-11 | |
| Scripts generalizados (`-Root`, `-Master`, `-OutDir`) | verificado | 2026-10-11 | Prueba con 3 láminas del manual |
| Registro del MCP en Claude (`claude mcp add … --scope user`) | verificado | 2026-10-11 | Quedó registrado; el servidor no responde |
| Instalación en Claude Code | verificado | 2026-10-11 | Hoy por enlace desde el repo |
| Illustrator 2025/2026 estables, interfaz en inglés, otra escala de pantalla | sin probar | — | Los clics del cuadro son proporcionales; el título se busca por «Area Type Options» |
| macOS, Codex / Antigravity / VS Code | sin probar | — | Los scripts dependen de COM (solo Windows) |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Skill verificada de principio a fin con el caso `caso-manual-marca-01` (46 láminas): texto en líneas y párrafos, maestro, limpieza de recortes, Tamaño automático, auditoría y fidelidad.
- Esta skill como tal aún **no se ha invocado en una sesión nueva**.

## Pendientes abiertos

- [ ] Pasar por el proceso las **piezas** del caso (`export/piezas/*.pdf`: flyers A5, plantillas de redes) y regenerar los PDF del maestro desde el `.ai` limpio.
- [ ] Probar el **MCP** cuando responda (¿expone «Tamaño automático» y limpieza?) y documentar sus herramientas.
- [ ] Probar en Illustrator **2025/2026 estables** (solo se ha probado la Beta 31), con la **interfaz en inglés** y otra escala de pantalla.
- [ ] Probar con otra fuente/marca y con un formato no horizontal (post 1080 × 1350).
- [ ] Decidir si se instala en Codex (necesita el comando de MCP con el token por variable de entorno).
- [ ] Soporte de texto con estilos mezclados dentro de un párrafo (hoy queda en líneas sueltas).
- [ ] Comprobar que `direct-visual-design` la invoque sola en una sesión real (la regla está escrita en su `SKILL.md` y en el `CLAUDE.md` del mantenedor).

## Límites conocidos

- 1 px del HTML = 1 pt en Illustrator; entregable RGB (CMYK/sangrado es un paso aparte).
- La fuente debe estar disponible en Illustrator (en el caso modelo, Poppins vía Adobe Fonts; el preflight lo pregunta por COM).
- El usuario debe aceptar que durante `ai_autosize_text.ps1` el ratón se mueva ~10 s y que Illustrator trabaje ~15 min en el proceso largo; siempre se le avisa.
- No cubierto: texto con estilos mezclados, texto vertical, texto sobre trazado, varias familias a la vez, CMYK/sangrado, documentos de más de ~60 láminas (estabilidad de Illustrator Beta en corridas largas).
- Solo se usa texto de área si el ajuste de líneas coincide con el del navegador; si no, quedan líneas sueltas y se informa.

## Dónde mirar

- Receta: `references/01` · defectos: `references/02` · HTML: `references/03` · COM/MCP: `references/04` · QA: `references/05` · caso: `references/06-caso-manual-marca-01.md`.
- Decisiones y registro de trabajos: `HANDOFF.md` · historial: `CHANGELOG.md`.
- Ficha del caso que la originó: `proyectos/caso-manual-marca-01.md`.
