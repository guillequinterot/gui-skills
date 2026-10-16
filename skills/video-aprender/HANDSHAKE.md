# HANDSHAKE — video-aprender

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.4 (sigue la versión de los scripts de `video-editing-ai-agent` 1.4.0) |
| Última actualización | 2026-10-16 por guille (migración al repo gui-skills) |
| Skill principal / padre | `video-editing-ai-agent` (sus scripts viven en `../video-editing-ai-agent/scripts/`) |
| Llama a | `video-editing-ai-agent` (scripts, plantillas `assets/*-template.md`, glosarios `assets/glosarios/`) |
| La llaman | `video-editing-ai-agent` (flujo de comprensión y cierre); cualquier pedido de «aprende de este video / analiza esta reunión» |

## Herramientas y su estado verificado

Verificado **solo en el Windows 11 del mantenedor**. `python ../video-editing-ai-agent/scripts/handshake.py`
informa en el bloque `video_aprender` qué scripts, glosarios y PyMuPDF hay en tu máquina.

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `video_aprender.py` (modos `contenido`, `reunion`, `estilo`) | verificado | 2026-10-16 | Contenido: clase pública real (8 min) y clase sintética; estilo: video público de 10 min y un archivo local; reunión: **solo sintética** |
| `aprender_lote.py` | verificado | 2026-10-16 | 11 links de Instagram público, reanudable, 26.2 min |
| `slides_extract.py` | verificado con límites | 2026-10-15 | Pizarra/diapositivas sintéticas 6/6; **no fiable en video de aula ni con una cámara filmando un monitor** (→ muestreo de fotogramas o PDF original) |
| Alineación con PDF (`--slides`, PyMuPDF 1.27) | verificado | 2026-10-15 | Prueba negativa 0 asignaciones; positiva coherencia 0.91; umbrales calibrados con una sola clase |
| `save_learning.py` | verificado | 2026-10-15 | Candidato → aprobado con cita del usuario o ≥ 3 fuentes; `memoria/` dentro de `video-editing-ai-agent` |
| Glosario de dominio `trading` + `hotwords` | verificado | 2026-10-16 | Solo errores **ya vistos**; para otro dominio, crear otro JSON con errores reales |
| `faster-whisper` 1.2.1 (`small`, CPU) | verificado | 2026-10-16 | ≈ 1× el tiempo del audio; `--rapido` −18 % |
| `yt-dlp` 2026.08.19 | parcial | 2026-10-16 | YouTube e Instagram **público** sin cookies OK; **cookies y TikTok sin probar**. Autorización personal por usuario |
| macOS / Linux | sin probar | — | |

## Capacidades confirmadas

- Transcripción local fiel de una clase real y de reels; cifras de gráficos leídas del fotograma y **recalculadas** con Python.
- Lote reanudable de links con resumen (`lote-resumen.md`); un fallo no detiene el lote.
- Muestreo de fotogramas con hoja de contacto cuando no hay estados estables.
- Alineación palabra por palabra de lo dicho con cada estado de la pantalla (`contenido.md`) y propuesta conservadora de diapositivas desde un PDF.

## Pendientes abiertos

- [ ] Una **reunión real** con varias personas (sin diarización: no se sabe quién habla).
- [ ] Grabaciones de pantalla reales (solo sintéticas), videos de **más de 1 h**, **TikTok**, cookies.
- [ ] Recalibrar los umbrales de alineación con PDF con más clases (hoy: 3 tramos de una sola clase).
- [ ] Cuándo conviene el modelo `medium`; procesar 2 reels en paralelo (sospecha: sin ganancia en 4 núcleos).
- [ ] Hotwords largas sobre una charla ajena al dominio (¿sesgo?): no medido.

## Límites conocidos

- No ve ni oye video; Whisper puede **equivocar cifras, nombres propios y siglas** y su marca de «dudoso» no es infalible: contrastar siempre con la imagen.
- No distingue quién habla; un gesto, un tono o un silencio incómodo no se pueden verificar.
- Un video de aula (cámara con profesor y público, 480p) no permite leer ecuaciones: se necesita el archivo de diapositivas original.
- La licencia declarada de un video **no equivale a permiso de uso**; análisis y referencia, no copia; no se republica lo descargado.
- Tiempo: una reunión de 1 h tarda ≈ 1 h de transcripción en una CPU de 4 núcleos; avisar antes y lanzar en segundo plano.
