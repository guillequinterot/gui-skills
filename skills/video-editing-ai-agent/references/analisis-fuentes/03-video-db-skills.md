# Análisis: github.com/video-db/skills

Nota de método: se leyeron README (vía página del repo), python/SKILL.md, reference/editor.md, editor-reference.md, use-cases.md, generative.md, streaming.md, sandbox.md, .mcp.json, plugin.json, ws_listener.py y los commits recientes. No se leyeron a fondo capture*, rtstream*, indexing*, search*, migration ni legacy (irrelevantes para edición). Las lecturas pasaron por un modelo resumidor de WebFetch, así que los valores son fieles al resumen, no verificados línea a línea.

## 1. Qué es, herramientas, estado, licencia

- Es una skill para agentes (Claude Code, Cursor, Copilot) sobre el servicio cloud **VideoDB** (SDK Python `videodb>=0.5.0`, paquete v1.3.0). NO es un repo de edición local: no usa ffmpeg, Remotion, Premiere ni MLT. Todo corre en la nube de VideoDB y requiere API key (`VIDEO_DB_API_KEY`).
- Foco real: "Ver, entender, actuar": captura de pantalla/mic, ingesta (YouTube, URLs, RTSP, archivos), análisis (voz, escenas, objetos, OCR, marcas), indexado y búsqueda semántica de momentos, subtítulos, clips, overlays, generación (imagen, video 5-8 s, música, SFX, TTS, doblaje/traducción), streams HLS instantáneos.
- Edición: hay un editor de timeline en la nube (Timeline/Track/Clip/Asset) sin render local; devuelve un HLS.
- Estado: MIT, ~120 estrellas, 8 forks, 84 commits; actividad reciente (commits 2026-09-07 y 2026-09-11: plugin de Claude con MCP alojado `https://mcp.videodb.io/mcp`). Proyecto vivo.
- Soporta macOS, Linux y Windows (PowerShell), con reservas (ver sección 5).

## 2. Estructura y organización

```
.claude-plugin/{plugin.json, marketplace.json}   .mcp.json   LICENSE  README.md
python/SKILL.md  python/.env.example
python/reference/  api-reference, capture(+-reference), editor(+-reference), generative,
                   indexing(+-reference), rtstream(+-reference), sandbox(+-reference),
                   search(+-reference), streaming, use-cases, migration, legacy/*
python/scripts/ws_listener.py
```

- Frontmatter de SKILL.md: `name: videodb`, `description` de una línea, `allowed-tools: Read Grep Glob Bash(python:*)`, `argument-hint: "[task description]"`. Frontmatter mínimo y con lista de herramientas permitidas restringida (buena práctica).
- Disparadores: 5 bloques de intención dentro del cuerpo (percepción de escritorio, ingesta, entender+indexar, edición de timeline, monitoreo en vivo).
- Carga progresiva: SKILL.md trae prompts canónicos + tabla "necesito -> método"; los docs de `reference/` se abren solo para patrones avanzados. Patrón doble por tema: `x.md` (guía/uso) + `x-reference.md` (API exacta). Carpeta `legacy/` + `migration.md` para código v1.
- Tabla de errores conocidos en SKILL.md (AuthenticationError, usar `.compile()` en lugar de `.stream_url`, timeout de reframe, `force=True`). Rutas resueltas con `CLAUDE_SKILL_DIR` (commit reciente) para instalación por marketplace.

## 3. Técnicas de animación y movimiento

Aviso claro: **el repo casi no contiene técnicas de animación**. No hay curvas de easing, keyframes, Ken Burns, zooms, expresiones ffmpeg ni guía de ritmo/cortes. Lo aplicable es el modelo de parámetros declarativos del editor y los presets de subtítulos.

Extraíble (fuente: python/reference/editor.md y editor-reference.md):
- **Transición**: `Transition(in_="fade", out="fade", duration=0.5)`. Único tipo documentado: fade, 0.5 s por defecto. Referencia razonable para crossfade/fade in-out por defecto.
- **Subtítulos animados** (CaptionAsset, `CaptionAnimation`): `box_highlight`, `color_highlight`, `reveal`, `karaoke`, `impact`, `supersize`. Los nombres son un buen vocabulario de estilos (palabra resaltada con caja, cambio de color, aparición progresiva, karaoke, palabra grande de impacto). El repo no da tiempos ni curvas; hay que implementarlos por cuenta propia (ASS con tags de karaoke/transformación, o filtros).
- **Estilo ASS de subtítulos**: colores `&HAABBGGRR` (defecto primario `&H00FFFFFF`, contorno `&H00000000`); fuente por defecto Clear Sans tamaño 30; `outline=1`, `shadow=0`; alineación 9 posiciones; márgenes `margin_l/r/v = 30`; estilo de borde `outline_and_shadow` u `opaque_box`. Útil como base de un preset de subtítulos (Shotcut/ffmpeg pueden consumir ASS).
- **Parámetros de Clip** como modelo de propiedades animables (aquí estáticas): `scale` 0-10 (def. 1), `opacity` 0-1, `offset {x,y}` relativo, `position` en rejilla de 9 zonas, `fit` (crop/contain/cover/none), `crop {top,right,bottom,left}` relativo, `filter` (greyscale, blur, boost, contrast, darken, lighten, muted, negative). Volumen 0-5 en video; 0.2 sugerido para música de fondo bajo voz (ducking manual estático, sin curva).
- **Texto**: TextAsset con font (family/size 48/color/opacity), border, shadow, background (caja con opacidad), alignment, line_spacing. Sirve como checklist de propiedades para un generador de títulos.
- **Resoluciones preset**: `1280x720`, `1920x1080`, `1080x1080`, `608x1080` (vertical). Reframe a vertical/cuadrado/horizontal se hace en servidor.
- Limitaciones del editor: `add_clip` acepta solo segundos enteros; la duración del clip no puede superar el asset; `.length` puede llegar como string (castear a float). No hay keyframes ni easing.

Conclusión: para animación (Ken Burns, easing, ritmo) hay que buscar en otras fuentes; de este repo solo se aprovecha el vocabulario y los valores por defecto arriba indicados.

## 4. Flujo de trabajo, handoff, estado y logs

- Flujo de 3 etapas: Entender (analizadores -> artefactos) -> Indexar -> Recuperar (búsqueda con timestamps y evidencia reproducible). Para edición: indexar palabras habladas -> generar subtítulos -> compilar segmentos en timeline -> `generate_stream()`.
- Revisión visual: no hay render local; la revisión es un reproductor web (`timeline.player_url`) y un HLS que se cachea (segunda llamada devuelve la misma URL). Patrón útil: previsualización inmediata antes de exportar.
- Estado/handoff: sandbox con ciclo `provisioning -> active/alert -> stopped`, `wait_for_ready()` y `GenerationJob.wait()`; se recomienda registrar `sandbox_id` junto con cada job para depuración y reintentos. Se debe llamar `stop()` explícitamente (facturación por tiempo).
- Logs: `scripts/ws_listener.py` escribe eventos en `videodb_events.jsonl` (ISO + Unix timestamp), `videodb_ws_id` y `videodb_ws_pid`, imprime `WS_ID=<id>` en la primera línea de stdout para parseo, con reintentos de backoff exponencial 1-60 s hasta 10 intentos. Patrón JSONL append-only + archivos de PID/ID reutilizable para logs de handoff.
- No hay protocolo de handshake entre herramientas ni changelog propio.

## 5. Reutilizar, descartar, riesgos

Reutilizar:
- Estructura SKILL.md corto + `reference/` por tema con pareja guía/reference, y carga progresiva.
- `allowed-tools` restringido y `argument-hint`.
- Tabla "Error -> arreglo" en la skill.
- Vocabulario de estilos de subtítulos animados; defaults de fade 0.5 s, fit modes, rejilla de 9 posiciones, volumen de fondo 0.2.
- JSONL append-only de eventos con timestamps, ID/PID de proceso, backoff exponencial.
- Registrar identificadores de jobs para reintentos; separar legacy vs. nuevo (`migration.md`).
- Preview inmediato antes de exportar final.

Descartar:
- Todo lo cloud (indexación, búsqueda, RTSP, sandbox, generación): no aplica a Shotcut/ffmpeg locales y añade dependencia y costo.
- El editor de VideoDB como motor: no expone keyframes/easing y limita a segundos enteros.

Riesgos:
- Envía media a un servicio de terceros (privacidad de material de cliente); requiere API key y créditos.
- `.mcp.json` apunta a un MCP remoto (mcp.videodb.io) con autorización propia: no activarlo sin decisión explícita.
- Ejecución de `Bash(python:*)` con SDK externo: dependencia de versión (>=0.5.0, migración v1).
- `ws_listener.py` usa `signal.SIGINT/SIGTERM` y `asyncio.add_signal_handler`, que no funcionan en Windows; ruta por defecto `/tmp`. Si se reutiliza el patrón, adaptar (KeyboardInterrupt, `tempfile`).
- Fuente por defecto "Clear Sans" no viene en Windows; usar una fuente instalada.
