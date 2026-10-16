# HANDSHAKE — video-editing-ai-agent

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.
> No confundir con `scripts/handshake.py`, que comprueba las **capacidades reales de la máquina en que se
> corre** y escribe `<proyecto>/handshake.json`: este archivo recoge lo que se **verificó una vez, en el PC del
> mantenedor**; el script dice qué hay en el tuyo.

| Campo | Valor |
|---|---|
| Versión | 1.4.0 (`scripts/handshake.py` → `skill_version`) |
| Última actualización | 2026-10-16 por guille (migración al repo gui-skills) |
| Skill principal / padre | ninguna (es la skill única de video) |
| Llama a | `rea-reverse-engineer` (por porción, para entender una web/app de referencia); `video-aprender` (sub-skill: aprender de un link/archivo) |
| La llaman | `video-aprender` (usa sus scripts); `direct-visual-design` y `seo-content-system` cuando el entregable es video |

## Herramientas y su estado verificado

Todo lo de esta tabla se verificó **solo en el Windows 11 del mantenedor** (Ryzen 7 3700U, 13.9 GB RAM; Whisper
corre en CPU). Para tu máquina: `python scripts/handshake.py --project <carpeta>` y
`python scripts/selftest.py`.

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| Shotcut 26.8.1 + MLT 7.41.0 | verificado | 2026-09-21 | `winget install --id Meltytech.Shotcut`; el ffmpeg incluido **no** trae `drawtext`/`ass`/`subtitles` |
| `shotcut-mcp` 1.5.6 (MIT) | verificado | 2026-09-21 | Registrado a mano (`claude mcp add-json --scope user shotcut …`); `/plugin install` no dejó el plugin. `shotcut_doctor` → `tested` |
| ffmpeg n8.1.2 (el de Shotcut) | verificado | 2026-10-15 | Tres bloqueos conocidos: `alimiter` tras `amix`, `sidechaincompress` con duraciones distintas, dos grafos `asplit+amix` (ver `logs/UPDATE-LOG.md`) |
| HyperFrames 0.8.162 (Apache-2.0) | verificado en Windows | 2026-10-16 | `npx --yes hyperframes@0.8.162`; requiere Node ≥ 22, headless shell de Playwright, FFmpeg por variable de entorno, telemetría desactivada (`references/engine-hyperframes.md`) |
| `faster-whisper` 1.2.1 (`small`, CPU) | verificado | 2026-10-16 | ≈ 1× el tiempo del audio; `hotwords` soportado; incluye Silero VAD |
| Silero VAD (dentro de faster-whisper) | verificado | 2026-10-15 | `scripts/vad_segments.py`; valida cruzado la transcripción |
| `yt-dlp` 2026.08.19 | parcial | 2026-10-16 | YouTube e Instagram **público** OK sin cookies; **cookies, TikTok, videos > 1 h: sin probar**. Requiere autorización personal de cada usuario (ver HANDOFF §2) |
| PyMuPDF 1.27 | verificado | 2026-10-15 | Solo para `--slides` (PDF de diapositivas) |
| `selftest.py` | verificado | 2026-10-16 | 35/35 en el PC del mantenedor, repetido sobre la copia del repo tras la migración (87 s) |
| CapCut / Canva / Premiere Pro / After Effects | sin probar | — | Stubs `not_configured` (`references/engines-future.md`); no prometer capacidades |
| macOS / Linux | sin probar | — | Nada de la skill se ha ejecutado fuera de Windows; las rutas de `handshake.py` y el instalador `.ps1` son de Windows |

## Capacidades confirmadas

- Comprensión de video completo (mapa de planos, movimiento, voz, silencios, fotogramas clave con presupuesto, hojas de contacto) con 3 videos reales y un video largo de 10 min (144 planos).
- Edición por EDL → proyecto de Shotcut (`edl_to_shotcut.py`), color por clip (`grade.py`), subtítulos palabra por palabra en Shotcut, mezcla de música y normalización de loudness (objetivo ≈ −16 LUFS).
- Piezas desde cero con HyperFrames: render 1080×1920 y 1080×1170, `--batch` con variables, `snapshot`, push entre páginas con `cut_dip.py` (hueco 0 %), música al compás con `beat_grid.py` (122 BPM medidos, fase +0 ms).
- Biblioteca de videos aprobados (`save_approved.py`: `add` exige cita textual; `suggest`/`recipe` al empezar) — 1 entrada (V001, anonimizada).
- `video-aprender` (modos `contenido`, `reunion`, `estilo`): clase pública del MIT OCW (8 min, ecuaciones verificadas con Python), 11 reels públicos de Instagram en lote (26.2 min), clase sintética y pizarra sintética (6/6 estados).

## Pendientes abiertos

- [ ] Carve (`carve_music.py`) frente a EQ estático y regla «No sidechain» — necesita una pieza con voz en off y escuchar 3 versiones.
- [ ] Subtítulos con `hf_captions.py` **renderizados** en HyperFrames (la agrupación está probada; el render no).
- [ ] Preferencia estética con/sin empuje de cámara en fotos — el usuario aprobó la pieza sin elegir (V001).
- [ ] Bloques instalables del catálogo de HyperFrames (solo se probó la búsqueda `catalog --query`).
- [ ] Sincronía de la rejilla de compás **confirmada a oído** (solo medida).
- [ ] Cookies de yt-dlp, TikTok y videos de más de 1 h.
- [ ] `video-aprender`: una reunión real con varias personas (sin diarización), grabaciones de pantalla reales (solo sintéticas), cuándo conviene el modelo `medium` en vez de `small` + glosario, OCR de cifras de gráficos, procesar 2 reels en paralelo.
- [ ] Activar CapCut/Canva/Premiere/After Effects solo con su checklist de `references/engines-future.md`.
- [ ] Verificar la skill en macOS/Linux y con otro usuario (nadie más la ha instalado aún).

## Límites conocidos

- Claude **no oye ni ve video**: lee texto (transcripción) e imágenes (fotogramas). No se oye música ni efectos; el movimiento es una medida, no semántica; Whisper alucina sobre música (el script lo marca `SOSPECHOSO`).
- «Gradual/animado» es una heurística; con stop-motion genera falsos cortes.
- Sin diarización: no se sabe quién habla.
- Un `.py` con una ruta de Windows pegada puede corromperse (`\v` → tabulador vertical): se detectó y corrigió en esta migración (`fetch_reference.py`, `video_understand.py`, `install-shotcut-stack.ps1`).
- Rutas y comandos de `install/` y de `engine-hyperframes.md` están escritos para Windows.
