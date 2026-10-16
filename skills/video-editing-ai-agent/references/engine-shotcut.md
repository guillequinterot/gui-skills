# Motor Shotcut (MLT) vía shotcut-mcp

Verificado en: Shotcut 26.8.1 + MLT 7.41.0 + shotcut-mcp 1.5.6 (solo en el Windows 11 del mantenedor; macOS/Linux sin probar). Repo: matrodrigs/shotcut-mcp (MIT).

## Instalación (lo que funcionó)
Los comandos `/plugin marketplace add` + `/plugin install` **no dejaron el plugin instalado**. Sí funcionó:
1. `git clone https://github.com/matrodrigs/shotcut-mcp` en `~/.claude/mcp-servers/shotcut-mcp` (en Windows, `%USERPROFILE%\.claude\mcp-servers\shotcut-mcp`).
2. Registro global (ámbito usuario) con `claude mcp add-json --scope user shotcut '<json>'` — `type: stdio`, `command: python`, `args: [<ruta>\scripts\shotcut_mcp_server.py]`, `env: SHOTCUT_PATH, SHOTCUT_MELT_PATH, SHOTCUT_FFMPEG_PATH, SHOTCUT_FFPROBE_PATH`. (Con `-e` variádico el comando falla; usar `add-json`.)
3. Reiniciar la sesión: las tools (`mcp__shotcut__*`) aparecen como deferred → cargarlas con ToolSearch (`select:...`).
4. Comprobar con `shotcut_status` y `shotcut_doctor` (debe decir `tested`).
Sin `SHOTCUT_MCP_ALLOWED_ROOTS` el acceso a rutas es global (decisión del usuario).

## Flujo de edición
`create_project` (probar el metraje antes de elegir resolución/fps) → `inspect_project` (revisión + `item_ref`) → `edit_project` con `expected_revision` (lote de hasta 500 ops) → `render_contact_sheet`/`render_preview` → (solo si lo piden) `start_render` + `render_status`.
- No usar `force`. Ante conflicto de revisión, reinspeccionar.
- `plan_project_edit` = dry run.
- Cada edición exitosa ya valida con melt.

## Operaciones y trampas verificadas
- **Perfil**: Reel = 1080×1920, 30 fps. Los clips se rellenan con `transition.fill=1` (afín).
- **Recorte/ritmo**: cada clip con `in_frame/out_frame` (o `in_seconds`).
- **Transiciones** (`add_transition`, service `luma`, `audio_crossfade:true`): SOLAPAN clips. Duración total = suma − suma de transiciones. El clip derecho pierde `duration` al principio pero esos frames se reproducen dentro de la transición. Servicios útiles vistos: `luma`, `mix`, `qtblend`, `frei0r.sleid0r_*` (push/slide/wipe). `item_ref` = clip **izquierdo**.
- **animate_clip**: canal `transform` exige en CADA keyframe `center_x, center_y, scale, rotation_degrees` (0.5/0.5/1/0 = sin cambio); `opacity` y `volume_db` son canales aparte. `interpolation: smooth` (para easing usa 4–5 keyframes intermedios; ver `ease_keyframes.py`). Keyframes relativos al clip.
- **Zoom anclado arriba** (cabeza en tercio superior): `center_y = a + s·(0.5 − a)` con `a≈0.22`. Para zoom centrado `center_y=0.5`.
- **Texto animado** = `add_generator generator:text` (producer color transparente + filtro `dynamictext`). Propiedades: `family, size, weight, fgcolour, bgcolour (#aarrggbb), olcolour, outline (máx 3 px), align, pad`. Geometría por defecto `10%/10%:80%x80%`, centrado vertical → posiciónalo con `animate_clip` (`center_y 0.68` ≈ tercio inferior seguro para Reels). Banda oscura de legibilidad: `bgcolour #a6000000`, `pad 26`.
- **Subtítulos SRT** (`set_subtitle_track`, `burn_in:true`, `style{family,size,weight,fgcolour,olcolour,outline,halign,valign,geometry}`): estáticos y compartidos por toda la pista; sin animación por frase. Para animación usa clips de texto.
- **Logo/overlay**: PNG con transparencia en pista `Overlays` (`add_track` video) + `animate_clip` opacity (fade in/out).
- **Audio**: pista `add_track kind:audio` + `add_clip`; `animate_clip` con `volume_db` da automatización de volumen (bajar música bajo la voz, subir en la pantalla final).
- **Limpieza de voz**: `add_filter target:clip service:rnnoise properties{mix:0.9}` (RNNoise). Medir antes/después (ver `audio-mix.md`).
- **Volumen con fades: usa `interpolation: "linear"`**. Con `smooth`, una subida brusca (p. ej. −48→−3 dB en 9 f) hace que la curva se pase por encima del nivel en el tramo plano (medido +3 dB sobre lo esperado, picos > 0 dBFS). Verifica siempre: diferencia export−fuente por ventanas de 0.5 s debe ser plana.
- **Pista de música con clip reemplazado**: `remove_item` con `ripple:false` deja un hueco (el proyecto se duplica de duración). Para rehacer, `remove_track` + `add_track` + `add_clip mode:overwrite`.
- **Ganancia**: `animate_clip` con `volume_db` constante en 2 keyframes (0 y 60) sube +N dB.
- **Velocidad**: `set_clip_speed` / `set_clip_speed_map` (timeremap) para rampas.
- **Diagnóstico**: `analyze_media_quality` (silencio, negros, freezes, loudness), `probe_media`, `diagnose_color_workflow` (HDR).
- **Lotes grandes** (decenas de clips): escribir un script Python que hable con el servidor por stdio (`scripts/shotcut_mcp_call.py`) en vez de pegar JSON enorme en el chat.

## Render
`start_render` **solo** con petición explícita del usuario en el turno (o resumen aprobado). Presets: `h264-high` (crf 18, aac 192k), `h264-web`, `hevc`, `prores`, etc. `output_path` nuevo, `overwrite:false`. Devuelve `job_id`; sondear `render_status` (o esperar el archivo con un Monitor). Entrega = MP4 + copia exacta del proyecto (`*.render-<id>.mlt`). Verificar con `ffprobe`.

## Estado de los archivos
Backups automáticos en `.shotcut-mcp/backups/`; previews en `.shotcut-mcp/previews/`. El servidor solo ve el proyecto **guardado en disco**: si el usuario tiene el proyecto abierto en la GUI, pídele guardar y evitar guardados concurrentes.

## Añadido en v1.1
- **EDL → proyecto**: `python scripts/edl_to_shotcut.py edl.json --project X.mlt [--transition-frames 10] [--denoise 0.9] [--pad-in 0.05 --pad-out 0.08]`. Crea clips con padding, fundidos de audio de ~30 ms en los cortes duros (keyframes de volumen lineales), marcadores por `beat`, notas con `quote/reason`, color del EDL y (solo con cortes duros) overlays y SRT. Probado con `warm_cinematic` y con `auto`, con y sin transiciones.
- **Color en Shotcut**: MLT del Shotcut trae `avfilter.eq`, `avfilter.colorbalance`, `avfilter.curves` (propiedades con prefijo `av.`; p. ej. `av.contrast`, `av.saturation`, `av.master`). `python scripts/grade.py --mlt-ops warm_cinematic` imprime las ops `add_filter` listas (añade `target:"clip"` e `item_ref`). Otros filtros disponibles: `lift_gamma_gain`, `avfilter.colortemperature`, `avfilter.selectivecolor`, `avfilter.lut3d`.
- **Marcadores**: `add_marker` (`start_frame`, `text`, `color`) para beats/capítulos; `export_marker_chapters`.
- **Timeouts**: `list_mlt_services` puede dar `mlt_repository_timeout` (Shotcut lento al arrancar): reintenta; alternativa `melt -query filters|transitions|producers`.
- **Revisión**: `scripts/self_eval.py` sobre el MP4 exportado con los tiempos de transición como `--boundaries`.
