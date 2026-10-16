# Análisis: 6missedcalls/video-editing-skill

Verificación: SKILL.md y todos los scripts (.sh) leídos LITERALMENTE desde raw.githubusercontent.com. Estructura, licencia y estrellas vía API/WebFetch. README (13 KB) solo revisado por encabezados (grep); su contenido coincide con SKILL.md.

## 1. Qué es, estado, licencia
- Skill mínima de edición por lenguaje natural: trim, jump cuts (quita silencios), subtítulos quemados (Whisper + 3 estilos), texto superpuesto, cambio de velocidad, y un orquestador que las encadena. Bash + ffmpeg + whisper opcional. Sin Python propio, sin nube.
- Compatible declarado: OpenClaw, Claude Code, Codex.
- Licencia MIT. 35 estrellas, 7 forks, 1 issue abierto. Creado 2026-02-26, último push 2026-02-27, 3 commits: proyecto de un día, sin mantenimiento demostrado. Madurez baja.
- NO tiene: animación, keyframes, transiciones, zoom, easing, ni ninguna integración con editores (Shotcut/MLT/CapCut/Premiere/AE).

## 2. Estructura
```
SKILL.md (3.5 KB) · README.md · LICENSE · .github/PULL_REQUEST_TEMPLATE.md
scripts/ edit.sh (orquestador) trim.sh jumpcut.sh transcribe.sh caption.sh overlay-text.sh onboard.sh
```
- SKILL.md: título + uso con ejemplos en lenguaje natural + tabla de capacidades + tabla de scripts + sección "Agent Instructions" (7 reglas). Sin frontmatter YAML visible (empieza con `# Video Editing`), por lo que no define `name`/`description` de disparo; el disparo depende del instalador/agente. Debilidad frente a estándar de skills.
- Sin carpeta `references/`; el conocimiento vive en el SKILL.md y en las cabeceras de cada script (usage extraído con `sed -n` de los comentarios).
- Reglas de agente útiles: parsear la petición en operaciones; usar edit.sh para multi-operación y scripts sueltos para una; caption por defecto "standard"; whisper "base" por defecto, "medium/large" si es largo/ruidoso; SIEMPRE reportar ruta de salida y duración.

## 3. Técnicas de movimiento/animación (lo poco que hay, con origen)
Casi nada de animación real; sí hay parámetros de ritmo y tipografía reutilizables.

**Ritmo / cortes (scripts/jumpcut.sh)**
- Detección: `-af silencedetect=noise=-30dB:d=0.5 -f null -`; parseo de `silence_start/silence_end` del stderr.
- Defaults: umbral -30 dB, silencio mínimo 0.5 s, padding 0.1 s. README sugiere más agresivo (-35 dB, 0.8 s) o más conservador. Segmento termina en silence_start+padding; el siguiente empieza en silence_end-padding.
- Cortes con `-c copy -avoid_negative_ts make_zero` + concat demuxer. PROBLEMA: cortar con copy solo es exacto en keyframes; produce cortes imprecisos/glitches de audio-video. Para nuestra skill: re-codificar o usar `trim/atrim + concat` filter, o mejor generar cortes en MLT (playlist de clips con in/out).

**Velocidad (scripts/edit.sh, paso Speed)**
- Vídeo `setpts=(1/factor)*PTS`; audio `atempo` encadenado (atempo solo admite 0.5–2.0 en la versión usada por el script, se encadenan factores: >2 => `atempo=2.0,...`; <0.5 => `atempo=0.5,...`). Útil como fórmula.

**Subtítulos (scripts/caption.sh)** — filtro `subtitles=` con `force_style` ASS:
- hormozi: `FontName=Arial Black,FontSize=28,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H80000000,Outline=3,Shadow=2,Alignment=10,MarginV=40`
- standard: Arial 20, Outline 1, Shadow 1, Alignment=2, BorderStyle=4, MarginV=30 (caja semitransparente)
- minimal: Helvetica Neue 16, Outline 1, Shadow 0, Alignment=1 (abajo-izq), MarginL 40, MarginV 20
- LIMITACIÓN IMPORTANTE: el estilo "hormozi" es solo estético (grande, centrado, contorno). NO hace palabra por palabra ni resaltado animado: usa el SRT de Whisper por frases (Whisper CLI sin `--word_timestamps`). Es un nombre engañoso. Para animación real de subtítulos hay que generar ASS con tags `\k`/`\t`/`\fad`, o SRT por palabra (Whisper `--word_timestamps True --max_words_per_line 1`).
- Alineación ASS: usa numpad (2=abajo centro, 1=abajo izq); Alignment=10 en ASS/libass NO es un valor válido de numpad estándar (SSA legacy: 9-11 = centro-medio; puede funcionar solo con semántica SSA). No verificado en ejecución; recomendaría `Alignment=5` en ASS.
- Escape de rutas para el filtro subtitles: barras invertidas, `:` y `'` (función `escape_path`). En Windows (`C:\...`) hay que escapar `C\:`; el script no cubre backslashes de Windows bien.

**Texto overlay (scripts/overlay-text.sh)** — `drawtext`:
- Posiciones (margen 20 px): center `x=(w-text_w)/2:y=(h-text_h)/2`; top `y=20`; bottom `y=h-text_h-20`; esquinas análogas.
- Visibilidad temporal: `enable='between(t,START,END)'`; por defecto duración 5 s; fontsize 48; caja `box=1:boxcolor=black@0.5:boxborderw=10`.
- SIN animación: ni fade ni slide. Fórmulas propias posibles con drawtext (alpha expresión: `alpha='if(lt(t,S+0.3),(t-S)/0.3,1)'`; y con `y='h-... + ...*(1-easeOut)'`), pero NO están en este repo (propuesta mía, no verificada aquí).

**Zoom/Ken Burns, transiciones, keyframes, easing:** inexistentes en el repo.

## 4. Flujo y handoff/estado/logs
- Pipeline fijo: trim → jumpcut → speed → caption → overlay (edit.sh). Cada paso escribe `step_N.ext` en un `mktemp -d` con `trap 'rm -rf' EXIT`; salida final `--output`. Patrón simple de "archivo actual" encadenado (CURRENT_FILE/next_intermediate).
- Cada script imprime `Output: <ruta>`; jumpcut imprime original -> editado y % ahorrado. El agente debe informar ruta y duración.
- `onboard.sh`: chequea dependencias (ffmpeg, ffprobe, whisper), instala por symlink/copia en `~/.openclaw/skills` y `~/.claude/skills`, `--uninstall`, self-test e instrucciones por SO (Windows: `choco install ffmpeg`).
- NO hay handoff entre herramientas, ni estado persistente, ni logs de actualización, ni manifest de proyecto. Los intermedios se borran (no se conserva historial ni versiones).

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Estructura de "Agent Instructions" (parsear -> elegir script -> reportar salida y duración).
- Detección de silencios con silencedetect y parámetros por defecto (-30 dB/0.5 s/0.1 s) como fuente de una lista de cortes que luego se aplique como clips MLT/Shotcut (mejor que recortar con ffmpeg).
- Fórmula setpts + cadena de atempo (en MLT: propiedad `speed` de producer `timewarp`).
- Presets de estilo ASS como punto de partida (corrigiendo Alignment y añadiendo animación real).
- Patrón onboard/doctor (chequeo de dependencias + instalación por symlink) y directorio temporal con trap.
- Regla: Whisper base por defecto, modelos mayores para audio largo/ruidoso; `--language es` para nuestro caso.

Descartar / mejorar:
- `-c copy` para cortes precisos; nombres engañosos ("hormozi"); ausencia de frontmatter; overlays sin animación; sin logs/estado.
- Todo el conjunto es bash: en Windows requiere Git Bash; rutas con `:` y espacios frágiles. Usar PowerShell/Python o llamadas ffmpeg directas con listas de argumentos.

Riesgos:
- Seguridad: bajo (scripts locales, sin red; onboard usa symlinks en directorios de skills; texto del usuario en drawtext con escape parcial: riesgo de inyección de filtros si el texto viene de contenido no confiable; uso de `awk "BEGIN{...$1...}"` con valores sin validar = inyección posible).
- Dependencias: ffmpeg con libass (subtitles) y freetype (drawtext); fuentes "Arial Black"/"Helvetica Neue" pueden no existir en Windows/Linux (fallback silencioso).
- Mantenimiento: repo de 1 día, 35 estrellas; tratar como referencia, no como dependencia.

Veredicto: valor bajo para animación; útil solo como esqueleto de pipeline ffmpeg y de instrucciones para agentes. Las técnicas de motion (zoom, easing, transiciones, subtítulos animados) deben salir de otros repos.
