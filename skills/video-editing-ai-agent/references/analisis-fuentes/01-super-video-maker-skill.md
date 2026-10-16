# Análisis: Bomx/super-video-maker-skill

Fuente: https://github.com/Bomx/super-video-maker-skill (API de GitHub + raw.githubusercontent.com).

Advertencia de método: WebFetch devuelve resúmenes generados por un modelo pequeño, no el texto crudo. Los valores numéricos son consistentes entre archivos, pero algunos comandos (por ejemplo `zoomPan` con mayúscula en el digest de SKILL.md) parecen re-formateados. Antes de reutilizar un comando, verifícalo con `ffmpeg` real. Donde hay conflicto, prevalece FFMPEG_PLAYBOOK.md.

## 1. Qué hace, herramientas, estado y licencia

- Skill de producción de video con IA para agentes (Claude Code, Cursor). Su formato estrella es el "avatar explainer": avatar sintético + capturas/pruebas + b-roll + subtítulos + CTA. También cubre UGC ads, demos de pantalla, explainers sin cara y reutilización de video largo.
- Herramientas que orquesta:
  - HeyGen (avatares)
  - Seedance 2.5 vía fal.ai (b-roll)
  - OpenAI `gpt-image-2` (imágenes) y Whisper (tiempos por palabra)
  - ElevenLabs (voz y música)
  - Remotion (React, movimiento) y HyperFrames (HTML/GSAP)
  - ffmpeg (composición, subtítulos ASS, QC)
  - Grabación de navegador (`agent_browser_recorder.py`)
  - Pillow (máscaras y badges)
- Es una skill **de generación con APIs de pago**. Solo una parte es edición de timeline: ffmpeg y Remotion.
- Repo: Python + TS, 279 estrellas, 43 forks, creado el 2026-05-17, último push 2026-08-09, 2 issues abiertos. **Sin licencia declarada**, así que por defecto todos los derechos están reservados. Úsalo como inspiración y no copies código literal a un producto propio.

## 2. Estructura y organización de la skill

Raíz (una sola skill grande):

- `SKILL.md` (44 KB) es el núcleo: reglas y flujo.
- `README.md`, `REFERENCE.md` (43 KB, capacidades y ruteo de proveedores) y `WORKFLOW_EXAMPLES.md`.
- Playbooks temáticos:
  - `FFMPEG_PLAYBOOK.md`
  - `REMOTION_VIDEO_GUIDE.md`
  - `LIVING_CANVAS_PLAYBOOK.md`
  - `MOTION_COLLAGE_STYLE.md`
  - `TABLETOP_EXPLAINER_PLAYBOOK.md`
  - `REVIEW_VIDEO_PLAYBOOK.md`
  - `VIDEO_COPY_PLAYBOOK.md`
  - `SPOKEN_VO_HUMANIZER.md`
  - `HOOK_PLAYBOOK_ARTICLE_SPRINT.md`
  - `HYPERREALISTIC_IMAGE_SOP.md`
  - `SEEDANCE_AVATAR_ROI.md`
- `commands/` (3 slash-commands), `recipes/` (18 JSON + `schema.json`), `tools/` (scripts Python CLI), `workflows/` (ejemplos ejecutables con `plan.example.json`), `remotion-template/`, `hyperframes-template/`, `tests/`, `references/`.

Frontmatter de SKILL.md:

- `name: super-video-maker`.
- La `description` es larga y lista disparadores por herramienta: "make/edit/repurpose/caption/soundtrack video" con HeyGen, Seedance, UGC, Remotion, ffmpeg, variantes sociales.
- Declara variables de entorno (`HEYGEN_API_KEY`, `FALAI_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`).
- Incluye sección "When NOT to use": solo una imagen, solo transcripción, o pasos manuales de Premiere/DaVinci.

Progresión de carga (divulgación progresiva declarada en SKILL.md):

1. Antes de generar nada: `VIDEO_COPY_PLAYBOOK` (sección 11), `SPOKEN_VO_HUMANIZER`, `HOOK_PLAYBOOK`.
2. Ruteo por receta: `recipes/README.md` + `tools/video_recipes.py` (`list`, `match --goal`, `plan --recipe`).
3. Playbook de formato solo si la receta lo requiere.
4. `REFERENCE.md` para proveedores y `WORKFLOW_EXAMPLES.md` para recorridos completos.

Schema de receta (`recipes/schema.json`):

- Campos: `id`, `name`, `version`, `description`, `best_for`, `not_for`, `platforms`, `aspect_ratios` (16:9, 9:16, 1:1, 4:5), `duration_seconds{min,max,target}`.
- Producción: `stages[{id,title,actions,artifacts,paid_generation}]`, `tools`, `providers`.
- Ruteo y contenido: `routing_keywords`, `routing_negative_keywords`, `script_shape`, `visual_jobs`.
- Cierre: `qc_checks`, `deliverables`, `compliance_notes`.

Es un patrón muy reutilizable: recetas declarativas + matcher + test (`tests/test_video_recipes.py`).

## 3. Técnicas de animación y movimiento

### 3.1 Ken Burns / zoom con ffmpeg (FFMPEG_PLAYBOOK.md, SKILL.md)

- Zoom progresivo suave (video de entrada, `d=1`, por frame):
  `zoompan=z='min(zoom+0.0012,1.08)':x='iw/2-(iw/zoom/2)':y='ih*0.12':d=1:s=1920x1080:fps=30`
- Zoom más agresivo con recorte descentrado:
  `zoompan=z='min(zoom+0.0014,1.16)':x='iw*0.05':y='ih*0.45':d=1:s=1920x1080:fps=30`
- Para stills (SKILL.md): preescalar a 3840x2160 (`scale=...:force_original_aspect_ratio=increase,crop=3840:2160`) y luego `zoompan=z='zoom+0.002':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1920x1080`. El preescalado 2x evita el temblor de zoompan.
- Regla de fill: siempre `force_original_aspect_ratio=increase,crop=W:H`. Nunca rellenar con color (regla de b-roll).
- Mantener el último frame en vez de loopear: `tpad=stop_mode=clone:stop_duration=2` (regla 21: nunca hacer loop de b-roll dentro de un beat).

### 3.2 Zoom con easing, tipo demo de pantalla (tools/demo_video_composer.py)

- `ZOOM_FACTOR=1.8`, `ZOOM_DURATION=2.0 s`, ease-in 0.3 s, ease-out 0.3 s. Canvas 2560x1440, pantalla 1920x1080, 30 fps.
- Curvas (calculadas en Python y aplicadas por frame, no como filtro ffmpeg):
  - `ease_in_out_cubic(t) = 4t³ si t<0.5, si no 1-(-2t+2)³/2`
  - `ease_out_cubic(t) = 1-(1-t)³`
- Click ripple: 0.5 s, radio máx 40 px. Glow del cursor: radio 20 px. Sombra: `GaussianBlur(radius=20)`.
- Idea reutilizable para CapCut/Shotcut: pre-calcular la curva y volcarla como keyframes.

### 3.3 Muelles y easing en Remotion (workflows/living-canvas-explainer/motion-library.tsx)

- Spring por defecto: `damping 11, stiffness 210, mass 1`. Da "pop con leve rebote".
- Cámara rígida: `damping 16, stiffness 250` (completa en ~0.3 s). Reorden de listas: `damping 13, stiffness 200`. Word pop: `damping 10.5, stiffness 230`.
- Interpolaciones siempre con `extrapolate: clamp`.
- Salidas:
  - lineal;
  - ease-out cuadrático `1-(1-p)²`;
  - decaimiento exponencial `exp(-(t)/7)`.
- Duraciones por defecto @30 fps:
  - salida de actor: 10 frames (~0.33 s);
  - ring pulse: 22 frames;
  - glow sweep: 18 frames;
  - pre-flash: 6 frames antes del impacto.
- Micro-rebote al aterrizar: `exp(-(t)/7) * sin(t/1.9) * 0.035` sobre la escala.
- Péndulo: `exp(-t/11) * sin(t/2.6) * 6°`. Entrada de escala: `0.85 + enter*0.15`.
- Creep zoom (nunca un frame estático): `min(0.09, max(0, fr - lastF - 10) * 0.00135)`, es decir ~4 %/s con tope +9 %.
- Motion blur por velocidad con zona muerta: sin blur bajo 3.5 px/frame. Por encima, `blur = min(8, (vel-3.5)*0.28)`. El playbook lo llama "el detalle que separa lo pro de lo plantilla". Los movimientos de menos de 9 frames llevan 1–3 frames de blur direccional.
- Streaks de transición: 12 frames, recorrido ~2700 px.
- `typeOn`: 0.55 cps por defecto (parámetro del código). Word pop con blur de entrada 8 px (18 px en modo POV).
- Presets de spring en REMOTION_VIDEO_GUIDE.md: `snap`, `bounce`, `punch`, `drift`, `gentle`. Helpers: `actor()`, `actorSpring()`, `wordByWord()`, `counterAnimation()`, `continuousZoom()` (lineal), `breathingScale()` (seno).

### 3.4 Gramática de cámara y ritmo (LIVING_CANVAS_PLAYBOOK.md)

- Ciclo de vida de una tarjeta persistente:
  - entrada 6–12 fr
  - hold 30–80 fr
  - punch a sub-región 6–9 fr, escala 1.08→1.40 (centrado en el área de trabajo)
  - creep-hold 25–80 fr
  - rampa de salida 12–15 fr (1.10→1.23)
  - whip-out 6–9 fr, asimétrico: el "chrome" sale primero
- Métricas de ritmo:
  - nuevo beat visual cada 2.0–2.5 s
  - sub-eventos cada 0.3–0.5 s
  - hold máximo 3.5 s (105 fr)
  - 1–3 cortes duros por 60 s
  - total 55–70 s (lanzamiento) o 40–50 s (cutdown de anuncio)
- Stagger de aterrizaje: titular primero, props +8–10 fr, badges +10–15 fr.
- Overlap: el siguiente elemento entra 4–8 fr antes de que salga el actual. En Remotion, solape de 15–30 fr para evitar "cambio de diapositiva".
- Sincronía con la voz: cada reencuadre debe estar justificado por una palabra del VO con tolerancia ±4 fr @30 fps. El visual puede adelantarse 6–18 fr, nunca retrasarse más de 4. `frame = round(t_whisper * 30)`.
- "Física causal": cada beat con una mecánica distinta (caída, lluvia con rebote, espiral de vacío, squash-stretch con escala 0.28, péndulo). No repetir la misma mecánica en un video.
- Cadenas de transformación: máx. 1–2 por video, separadas 20 s. Fases: gather 15–17 fr, flick 3–4, órbita 10–12, colapso 6–8, burst 16–25. Total ~1.3–1.6 s.
- Reflow: overlap de tarjetas prohibido. La primera cede (-265 px, escala 0.92).
- Catálogo de FX: RingPulse (22 fr, borde 4→1.5 px), GlowSweep (18 fr, banda a 14°), Sparks (10–18 partículas, 26 fr), Embers, Flash (pre-glow 6 fr).
- Tokens visuales: fuente sans geométrica de peso 900/700/500 (sin pesos finos). Tarjetas con radio 22 px y sombra `0 24px 80px rgba(17,17,17,.10)`. Un solo acento por titular. Los pills totalmente redondeados con glow se leen como "plantilla IA", así que usa "Sharp Tags" de radio 3 px.

### 3.5 Collage motion (MOTION_COLLAGE_STYLE.md)

- Beats de 4–6 s, video total de 20–45 s. Un solo movimiento literal por beat.
- Movimiento sutil: bob + parallax suave. Sin morphing de caras. Push-in suave solo como fallback.
- Cortes en los límites de frase del VO, sin transiciones explícitas.

### 3.6 Subtítulos animados

- **ASS/ffmpeg** (tools/video_captioner.py, FFMPEG_PLAYBOOK.md):
  - Arial Black/Bold 64 (16:9) o 52 (Shorts 9:16). El default del script es 95, configurable.
  - `Alignment=2`, `MarginL=MarginR=80`, `MarginV=90`, outline 4–5, shadow 1–2.
  - Palabra activa amarilla `&H0000FFFF`.
  - Presets de posición: top (alignment 8, margen 80), middle (5, 150), bottom (2, 90).
  - Agrupado: máx. 4 palabras y 30 caracteres por línea, corte si hay un hueco de voz >0.7 s, hold de 1.0 s, cushion mínimo 0.12 s por evento.
  - La línea completa permanece visible y se ilumina palabra a palabra, sin ventana deslizante.
  - Quemado con `subtitles='captions.ass'`.
  - Shorts: `scale` → `pad` a 1080x1920 → `drawtext` título (44 px, y=72) → `subtitles`.
- **Remotion** (remotion-template/src/CaptionedTalkingHead.tsx):
  - La palabra activa lleva pop con spring `{damping 18, stiffness 220, mass 0.45}`, escala 0.92→1.04.
  - Pesos 800 (activa) y 600 (inactiva). Fondo `rgba(16,16,20,.58)`, acento `#FF6B2C`.
  - Fuente `min(54, w*0.022)`. Contenedor máx. 1180 px. Padding inferior 6.5 %.
  - Inicio de animación: `floor(w.start*fps)`.
- Whisper para tiempos por palabra: `whisper-1`, `verbose_json`, `timestamp_granularities=word,segment`. Trocea a 600 s y 24 MB.

### 3.7 Otros comandos ffmpeg útiles (FFMPEG_PLAYBOOK.md)

- Normalizar: `fps=30,format=yuv420p`, `libx264 -preset medium -crf 18`, `aac 192k`.
- PiP temporizado: `[1:v]scale=520:-1,setpts=PTS-STARTPTS+5/TB[pip];[0:v][pip]overlay=W-w-48:48:enable='between(t,5,12)'`.
- Chromakey: `chromakey=0x00ff00:0.18:0.08,format=yuva420p`.
- Resaltado: `drawbox=x=120:y=420:w=980:h=96:color=0xFF6B2C@0.92:t=4`.
- Overlay temporizado de PNG: `overlay=48:48:enable='between(t,0,3.2)'`.
- Split-screen: `hstack=inputs=2`.
- Vertical: `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`, o letterbox con `pad=1080:1920:(ow-iw)/2:(oh-ih)/2`.
- Mezcla de música: `[2:a]volume=0.12,apad[music];[1:a][music]amix=inputs=2:duration=first:dropout_transition=2`.
- Loudnorm: `loudnorm=I=-16:TP=-1.5:LRA=11` (-14 LUFS si el contenido es musical).
- Concat seguro: `concat -safe 0` solo tras normalizar fps, tamaño, códec y sample rate.
- Nota: el repo NO documenta `xfade` ni curvas de transición en ffmpeg. Los cortes son duros o resueltos en Remotion. Para transiciones en Shotcut/ffmpeg hay que aportarlas desde otra fuente.

### 3.8 Ritmo de cortes (SKILL.md)

- Regla 31: corte cada 2–4 s en stills de IA y 3–6 s en capturas. Un still de IA no debe pasar de 3.5 s sin cortar.
- Regla 32: cada visual tiene un trabajo editorial: proof, mechanism, consequence, action o transition.
- Regla 22: prioridad de b-roll: captura real > foto stock > Ken Burns > generado.

### 3.9 Audio (LIVING_CANVAS_PLAYBOOK.md)

- Tres stems: cama (~12 s, ganancia 0.30, notch -5 dB a 1.8 kHz, corte con fade de 0.2 s en el punchline), score y bus de SFX (30–60 eventos).
- SFX: `atrim` al largo de la acción y `adelay` al frame exacto. Volumen 0.15–0.6.
- Carve estático de EQ para la voz (1.8 kHz -6 dB, 350 Hz -2 dB). **No usar sidechain**, porque produce bombeo.
- Música 10–11 dB bajo el VO. Programa -16 LUFS, TP ≤ -1.5 dB.
- El TTS emocional genera 40–60 % de aire muerto, así que hay que recortar silencios.

## 4. Flujo de trabajo, handoff, estado y logs

Flujo por etapas (SKILL.md):

- Etapa 0: selección de receta.
- Etapa 1: intake (plataforma, aspecto, duración, activos, marca, CTA, pruebas, límites de cumplimiento).
- Etapa 2: guion + shot list. Por beat: narración exacta, trabajo visual, superficie, antes→acción→después y "reject list".
- Etapa 3: generación de activos.
- Etapa 4: ensamblado de timeline.
- Etapa 5: QC y export.

Puntos clave:

- **Puerta de confirmación de costo** (regla 2): antes de cualquier llamada de pago se muestran proveedor, cantidad, duración y costo.
- **Puerta de copy**: se revisa el copy antes del primer TTS o clip.
- **Layout zones** (1920x1080, definidas por coordenadas):
  - badge arriba-izq. (50,50)
  - PiP arriba-der. (1378,50) de 492x276, radio 24 px
  - banda de subtítulos en los últimos ~140 px
  - la tarjeta final oculta el PiP

Revisión visual:

- `broll_layout_qc.py` genera contact sheets y frames de revisión. Todo lo que no pasa se arregla o reemplaza.
- El playbook de Living Canvas usa **probe frames** en vez de renders completos durante la iteración: entrada (B+3), mitad de cascada, pico del punch (B+punch+2), asentado (B+punch+8), pico de FX, solape de salida.
- Checkpoint de mayor palanca: aprobar UNA sección antes de replicar el patrón a las demás.

Exportación:

- Todo el video se renderiza sin audio y el audio se termina aparte con `-c:v copy` para iterar barato.
- Estándar de export: `libx264 -crf 18 -pix_fmt yuv420p`, `aac 192k`, 30 fps.
- `ffmpeg_qc.py` comprueba existencia, streams, duración, códec (h264/hevc), `yuv420p` y `blackdetect=d=0.5:pix_th=0.10` (máx. 20 hallazgos). Devuelve una línea `RESULT: {json}` con estado `succeeded`, `warning` o `failed`.

Estado, handoff y logs:

- Directorio de job `tmp/video_jobs/<job_id>/` con `job_state.json`, entradas, intermedios y finales.
  - Campos: `job_id`, `status`, `stage`, `recipe`, `inputs`, `artifacts`, `metrics`, `next_action`.
  - Los intermedios no se borran hasta que pasa el QC.
- **Contrato RESULT**: cada herramienta imprime `RESULT: {status, stage, job_id, artifacts[], metrics, next_action}`, y en fallo `error` + `debug_log`.
  - Ese `next_action` es el handoff entre etapas.
  - Los errores se muestran amigables y el stack trace va al log.
- `character_card.json` (biblia del personaje UGC): voz, referencias, guardarropa. Es un ejemplo de estado persistente por entidad.
- No hay un log de cambios de la skill ni handshake entre herramientas o plataformas. Eso hay que diseñarlo aparte.
- Antipatrones registrados como aprendizaje (ver 3.9 y 3.4), por ejemplo: la puerta de visibilidad en `enterAt-1` se come la transición, y el cálculo de coordenadas del cursor debe basarse en el layout.

## 5. Qué reutilizar, qué descartar y riesgos

Reutilizar:

1. Arquitectura: SKILL.md corto de reglas + playbooks por formato + recetas JSON con schema + matcher + tests.
2. Contrato `RESULT` y `job_state.json` con `next_action`. Es la base ideal para el handoff entre Shotcut, CapCut, Canva, Premiere y AE.
3. Puertas: intake, costo, copy y QC. Añadir puerta de aprobación de UNA sección antes de replicar.
4. Parámetros de movimiento: spring 11/210, creep ≤9 %, zona muerta de blur 3.5, ritmo 2–2.5 s, hold ≤3.5 s, solape 4–8 fr, tolerancia ±4 fr con la voz. Son traducibles a keyframes de Shotcut/MLT (filtro `affine`/`qtblend`, `rect` animado) con curvas: MLT soporta `smooth`/`ease` en keyframes.
5. Curvas cúbicas precalculadas en Python para volcarlas como keyframes en cualquier editor.
6. Estilo de subtítulos ASS y reglas de agrupado, pensados para ffmpeg o `subtitles`. En Shotcut hay que usar el filtro de subtítulos o texto.
7. Comandos ffmpeg de normalización, loudnorm, concat seguro, blackdetect y contact sheets.
8. Regla de probe frames para revisión sin render completo.
9. Reglas editoriales: trabajo del visual, prioridad de b-roll y anti-"AI slop".

Descartar o dejar opcional:

- Todo lo dependiente de proveedores de pago (HeyGen, Seedance, gpt-image-2, ElevenLabs). Cuestan dinero, dependen de claves y varios modelos son puntuales.
- Reglas de avatar sintético, UGC y biblia de personaje (salvo la parte de divulgación ética).
- Motion library de Remotion, que requiere Node + React, salvo como referencia de números.

Riesgos:

- **Sin licencia**: no copiar código. Reimplementar las ideas con tus propios scripts.
- **Claves API**: `.env` con cuatro o más proveedores. Nunca subirlas ni pegarlas en el chat.
- **Windows**:
  - README instala con `brew install ffmpeg` (macOS). En Windows usar winget o choco.
  - Los scripts usan `python3` y rutas `tmp/`.
  - Escape del path en `subtitles='C\:/...'` es un problema clásico en Windows.
  - La fuente Arial Black debe existir.
  - La guía de Remotion menciona timeouts de `node_modules` en Google Drive; en Windows conviene renderizar desde una carpeta local.
  - Usar `--concurrency=4` y fuentes locales para evitar `delayRender` timeout.
- **zoompan**: es lento y su salida tiembla con stills pequeños. Preescalar 2x. La expresión `zoom+0.002` con `d=300` depende de la versión de ffmpeg.
- **Sin transiciones ffmpeg** (`xfade`) ni easing en filtros. Para Shotcut/MLT hay que complementar con la documentación del propio MLT (`describe_mlt_service`).
- **Ética**: obliga a divulgar avatares sintéticos y no fabricar fuentes o capturas. Mantener esa política.
- Verificar los valores del digest (ver advertencia al inicio) contra los archivos crudos antes de fijarlos como constantes en la skill propia.
