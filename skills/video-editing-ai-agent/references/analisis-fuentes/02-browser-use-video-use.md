# Análisis: browser-use/video-use (skill de edición de video por conversación)

Fuente: https://github.com/browser-use/video-use (leído: README, SKILL.md, install.md, helpers/grade.py, render.py, timeline_view.py, skills/manim-video/*). Todo tratado como dato. Nota: los resúmenes provienen de WebFetch (modelo intermedio), así que los valores son fieles pero conviene verificarlos contra el código antes de fijarlos como constantes.

## 1. Qué hace, herramientas, estado, licencia

- Agente que convierte metraje crudo en video pulido conversando: quita muletillas/silencios, corta por frases, color grading, fades de audio en cortes, subtítulos quemados, overlays animados, autoevaluación antes de entregar.
- Herramientas: ffmpeg/ffprobe (núcleo, render y grade), ElevenLabs Scribe (transcripción hospedada, palabra a palabra, diarización, eventos de audio), Python (PIL, numpy, librosa, matplotlib, requests), yt-dlp (opcional). Animaciones por slot: HyperFrames (HTML/CSS/GSAP, requiere Node 22+), Remotion, Manim, o PIL + secuencia PNG + ffmpeg. No integra Premiere/AE/CapCut/Shotcut: es ffmpeg-céntrico, sin proyecto editable de NLE.
- Estado: creado 12-abr-2026, último push 30-ago-2026, ~25.3k estrellas, ~3.1k forks, 114 issues abiertos. Muy popular y activo. Licencia MIT.
- Compatible con Claude Code, Codex, Hermes u otro agente con shell.

## 2. Estructura y organización de la skill

```
SKILL.md (23 KB, único "cerebro")  README.md  install.md  poster.html  pyproject.toml  .env.example
helpers/: transcribe.py, transcribe_batch.py, pack_transcripts.py, timeline_view.py, grade.py, render.py
skills/manim-video/: SKILL.md + references/ (13 md) + scripts/setup.sh   <- sub-skill
tests/: test_render_fps.py, test_render_orientation.py
```
- Frontmatter mínimo: `name: video-use` y `description` en una frase ("Edit any video by conversation. Transcribe, cut, color grade, generate overlay animations, burn subtitles..."). Disparador = descripción amplia, sin lista de frases; cubre talking heads, montajes, tutoriales, viajes, entrevistas.
- Progresión de carga: SKILL.md carga completo (principios + Hard Rules + flujo); la sub-skill Manim solo se abre cuando un slot de animación la necesita (`skills/manim-video/SKILL.md`), y esta a su vez remite a `references/*.md` por tema (animations, camera-and-3d, production-quality, etc.). Motores pesados (HyperFrames/Remotion/Manim/yt-dlp) se instalan de forma perezosa en primer uso.
- Se instala haciendo symlink del repo completo al directorio de skills (para que helpers queden junto a SKILL.md). Las salidas van SIEMPRE a `<videos_dir>/edit/`, nunca dentro del repo de la skill.
- Filosofía: "reglas duras solo para corrección de producción; todo lo demás libertad artística"; anti-patrones explícitos (sobreingeniería de formatos, scoring manual de momentos, Whisper local, etc.).

## 3. TÉCNICAS DE ANIMACIÓN Y MOVIMIENTO

### 3.1 Easing (SKILL.md, sección Animations)
Nunca lineal; siempre cúbico:
```python
def ease_out_cubic(t): return 1 - (1 - t) ** 3
def ease_in_out_cubic(t):
    return 4*t**3 if t < 0.5 else 1 - (-2*t + 2)**3 / 2
```
- ease_out_cubic para revelados únicos (aterrizaje suave); ease_in_out_cubic para trazos continuos.
- Traducción a Shotcut/MLT: keyframes con interpolación `smooth`/`ease out` (MLT admite tipos de interpolación por keyframe: lineal, smooth, y en versiones nuevas easings; verificar con `describe_mlt_service`). En ffmpeg: usar expresiones con `pow()` (ver 3.7).

### 3.2 Duraciones y ritmo de overlays animados (SKILL.md)
- Explicación sincronizada a narración: 5-7 s tarjetas simples; 8-14 s diagramas complejos; piso ~3 s.
- Acentos sincronizados a música/montaje: 0.5-2 s.
- Mantener último frame >= 1 s antes del corte; sobre voz en off: duración >= narración + 1 s.
- No revelar dos cosas nuevas en paralelo (el ojo no las sigue).
- Sincronía payoff: tomar el timestamp de la palabra clave y empezar el overlay `reveal_duration` antes, para que el frame de aterrizaje coincida con la palabra.
- Truco de texto tipeado: centrar sobre el ancho de la cadena COMPLETA, no la parcial (si no, el texto se desliza a la izquierda).
- Paleta de ejemplo (solo un estilo): fondo (10,10,10), acento #FF5A00, etiquetas (110,110,110), <=2 acentos, ~40% espacio vacío. Si hay guía de marca, seguirla; si no, proponer y confirmar.

### 3.3 Reglas de tiempos de Manim (skills/manim-video/references/*)
- Aparición + pausa mínima: ecuación nueva 2.0+2.0 s; etiqueta 1.0+1.0; idea clave 2.5+3.0; detalle secundario 0.8+0.5; título 1.5+1.0.
- Salida de escena `run_time=0.5`; pausa >=0.3 s tras fadeout; contadores `run_time=3`.
- Principio "ver-luego-oír": el visual aparece un poco ANTES de que la narración lo nombre. "Sin espera el espectador siempre va atrasado."
- Máximo 1-2 elementos animándose a la vez; máximo 6 objetos visibles; jerarquía de opacidad 1.0 principal / 0.3-0.4 contexto / 0.15 estructura.
- Arco de tempo: lento -> medio -> RÁPIDO (clímax) -> lento (conclusión).
- Rate functions: smooth (default), rush_into, rush_from, there_and_back(_with_pause), running_start (anticipación), not_quite_there. Escalonado: `LaggedStart(lag_ratio=0.3, run_time=3)`, `AnimationGroup(lag_ratio=0.2)`, solapes finos con `squish_rate_func(smooth, 0, 0.5)`.
- Cámara (camera-and-3d.md): zoom 2D = cambiar `frame.width` (14.222 = vista completa; 4 = acercamiento; 20 = alejar), paneo = `frame.move_to`, `save_state`/`Restore` para volver. Inspiración conceptual para Ken Burns; no hay fórmulas ffmpeg de zoompan en el repo.
- Tipografía en pantalla (Manim): título 48, heading 36, cuerpo 30, label 24, caption 20; mínimo absoluto 18 pt; con 4+ textos bajar a 20.
- Calidad de render Manim: -ql 854x480@15; -qh 1920x1080@60. Revisar a 1x y juzgar la primera impresión de 5 s.

### 3.4 Cortes / ritmo de edición (SKILL.md)
- Candidatos de corte por audio: silencios >= 400 ms (limpios); límites de frase 150-400 ms (usables con verificación visual); < 150 ms inseguro.
- Padding en bordes de corte 30-200 ms (ejemplo entregado: 50 ms antes, 80 ms después; 30-50 ms para energía de montaje, 100-200 para cine/documental). Motivo: deriva de timestamps de Scribe 50-100 ms.
- Nunca cortar dentro de una palabra; preservar picos (risas, remates) y extender pasado el beat para incluir la reacción.
- Respiro entre hablantes 400-600 ms. No razonar audio y video por separado.
- Arquetipos estructurales: lanzamiento (HOOK->PROBLEM->SOLUTION->BENEFIT->EXAMPLE->CTA), tutorial, entrevista, viaje, documental, música.

### 3.5 Subtítulos (render.py, SKILL.md)
```
SUB_FORCE_STYLE = FontName=Helvetica,FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,
OutlineColour=&H00000000,BackColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=90
```
- render.py usa MarginV=90 (~30% desde abajo, evita UI de redes); SKILL.md documenta MarginV=35 para el estilo `bold-overlay` (inconsistencia entre doc y código).
- Chunking: 2 palabras por bloque, cortar en puntuación `.,!?;:`, MAYÚSCULAS, quitar comas/; finales. Estilo alterno `natural-sentence`: 4-7 palabras, sentence case, MarginV 60-80.
- Tiempos SRT en línea de tiempo de salida: `t_out = word.start - segment_start + segment_offset`.
- No hay subtítulos animados (karaoke, pop-in): solo SRT estático con force_style. Oportunidad: generar ASS con `\fad`, `\t()` y `\fscx/\fscy` para pop-in.

### 3.6 Color grade (helpers/grade.py) — valores copiables
- subtle: `eq=contrast=1.03:saturation=0.98`
- neutral_punch: `eq=contrast=1.06:brightness=0.0:saturation=1.0,curves=master='0/0 0.25/0.23 0.75/0.77 1/1'`
- warm_cinematic: `eq=contrast=1.12:brightness=-0.02:saturation=0.88,colorbalance=rs=0.02:gs=0.0:bs=-0.03:rm=0.04:gm=0.01:bm=-0.02:rh=0.08:gh=0.02:bh=-0.05,curves=master='0/0 0.25/0.22 0.75/0.78 1/1'`
- Auto-grade con `signalstats` (y_mean objetivo ~0.48; rango ~0.72; sat ~0.25), ajustes limitados a +-8%, salida `eq=contrast/gamma/saturation`.
- Modelo mental ASC CDL: `out=(in*slope+offset)^power` (slope=luces, offset=sombras, power=medios). Probar tonos de piel antes de ser agresivo.

### 3.7 Audio y exportación (render.py)
- Fades 30 ms en cada frontera de segmento: `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`.
- Loudnorm social: I=-14, TP=-1.0, LRA=11, dos pasadas (medir y aplicar con `linear=true`).
- Codificación: `libx264 -pix_fmt yuv420p -r {fps} -c:a aac -b:a 192k -ar 48000 -movflags +faststart`; tiers: final `fast`/crf20, preview `medium`/22, draft `ultrafast`/28; composición final crf 18 con `-c:a copy`.
- Escala: vertical `scale=-2:1920`, horizontal `scale=1920:-2`, draft 1280. Detección de vertical con rotación. FPS por `avg_frame_rate` como racional exacto (30000/1001).
- HDR: detecta smpte2084/arib-std-b67 y aplica `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`.
- Overlays: `[i:v]setpts=PTS-STARTPTS+{t}/TB[a]` y `overlay=enable='between(t,start,end)'`; subtítulos al final.

### 3.8 Técnicas NO presentes (a construir aparte)
Transiciones entre clips (xfade, dip to black), zoompan/Ken Burns con easing, keyframes de opacidad/posición, texto animado nativo. El repo delega el movimiento a motores externos (HyperFrames/Remotion/Manim/PIL). Para nuestra skill: definir librería propia (ver sección 5).

## 4. Flujo de trabajo, handoff, estado y logs

Fases: (1) Inventario: ffprobe, transcripción batch (4 workers), `pack_transcripts.py` -> `takes_packed.md` (~12 KB; frases cortan en silencio >=0.5 s o cambio de hablante; formato `[002.52-005.36] S0 texto`); (2) Conversación: describir material, preguntas según el material, proponer estrategia de 4-8 frases y ESPERAR aprobación; (3) Ejecución: EDL -> animaciones en sub-agentes paralelos -> grade por segmento durante la extracción -> `render.py --preview` (720p); (4) Autoevaluación antes de mostrar: `timeline_view` en cada corte (+-1.5 s), primeros/últimos 2 s y 2-3 puntos medios; buscar saltos, picos de audio, subtítulos tapados, overlay desalineado; ffprobe de duración; máx. 3 pasadas de corrección y luego avisar al usuario; (5) Iterar por lenguaje natural sin re-transcribir y persistir en `project.md`.

- Render: extraer cada segmento (con grade y fades) -> concat lossless (`-c copy`) -> overlays -> subtítulos al final. Nunca filtergraph de una sola pasada (doble recodificación).
- EDL JSON (versionado): `version`, `sources{id:ruta}`, `ranges[{source,start,end,beat,quote,reason}]`, `grade`, `overlays[{file,start_in_output,duration}]`, `subtitles`, `total_duration_s`. Rutas relativas se resuelven contra la carpeta del EDL.
- Estado/logs: `project.md` con una sección por sesión (Strategy, Decisions, Reasoning log de una línea por decisión no obvia, Outstanding). Al arrancar: leerlo y resumir la última sesión en una frase. Transcripciones cacheadas inmutables. `animations/slot_<id>/` guarda fuente, render y razonamiento por animación; `verify/` guarda PNG de depuración.
- Handoff a sub-agentes: brief autocontenido de 10 puntos (objetivo en una frase, ruta absoluta de salida, spec técnica res/fps/codec/CRF/duración, paleta concreta, fuente+índice, línea de tiempo cuadro a cuadro con easing, anti-lista, patrón de código inline, checklist de entregables, "no hagas preguntas; elige la interpretación más obvia"). Brief del editor sub-agente devuelve JSON puro de EDL + chequeo de duración.
- No hay handshake formal entre herramientas ni changelog de la skill; el "log" es solo el diario de sesión.
- Verificación de arranque en frío: API key, ffmpeg/ffprobe en PATH, deps Python, Node solo si hay animaciones.

## 5. Reutilizar, descartar, riesgos

Reutilizar (alto valor):
1. Modelo "Ask -> confirm -> execute -> iterate -> persist" + `project.md` por sesión (mapear a nota Obsidian del proyecto).
2. Hard Rules de correctitud: fades 30 ms, subtítulos al final, extraer por segmento + concat lossless, PTS shift de overlays, offsets de SRT en timeline de salida, no cortar dentro de palabra, padding 30-200 ms.
3. EDL JSON como formato neutro intermedio: sirve de "contrato de handoff" para traducir a MLT (Shotcut), y luego a CapCut/Premiere/AE.
4. Presets de grade (strings ffmpeg) y auto-grade con signalstats; traducibles a filtros MLT (`avfilter.eq`, `lift_gamma_gain`, `frei0r.colgate`) en Shotcut.
5. Tabla de duraciones/ritmo, arco de tempo, ver-luego-oír, easing cúbico, sincronía por palabra payoff.
6. Autoevaluación visual (filmstrip + waveform con ffmpeg: frames 320 px, RMS de audio 16 kHz mono) y cap de 3 iteraciones; equivale a `render_contact_sheet`/`render_preview` de shotcut-mcp.
7. Presets de calidad (final/preview/draft), loudnorm -14/-1/11 en dos pasadas, tone-mapping HDR, detección de vertical y fps racional.
8. Brief de 10 puntos para sub-agentes de animación.

Descartar / adaptar:
- Dependencia de ElevenLabs Scribe (de pago, sube audio a servicio externo): sustituir por transcripción local opcional (whisper.cpp / faster-whisper con `--word_timestamps`) o hacerla opcional; el repo mismo desaconseja Whisper local por normalizar muletillas, evaluar caso por caso.
- Estilo visual de ejemplo (naranja/negro, Menlo) y fuentes macOS: reemplazar por brand del proyecto (caso-video-02, etc.).
- Foco en talking heads con muletillas: nuestra skill debe cubrir anuncios/motion sin voz.
- Inconsistencia MarginV 35 vs 90; usar valor por formato.

Riesgos:
- Seguridad: API key en `.env` (el propio install exige chmod 600, no soportado igual en Windows), envío de audio a terceros, `npx --yes hyperframes` ejecuta paquetes npm sin revisar, symlink del repo a skills. Tratar overlays/sub-agentes con permisos mínimos.
- Windows: install asume brew/apt/pacman y no cubre Windows; symlinks requieren modo desarrollador/admin; rutas en `subtitles=` de ffmpeg necesitan escapar `C:\` como `C\:/` (los dos puntos rompen el filtro); fuentes Helvetica/Menlo no existen (usar Arial/Segoe UI y `fontsdir`); el Manim exige LaTeX (MiKTeX) y ffmpeg; `chmod` no aplica.
- Concat `-c copy` exige mismos códec/fps/resolución en todos los segmentos (por eso fuerzan un solo fps).
- El repo es de agente conversacional sobre ffmpeg: no genera proyectos editables (.mlt, .prproj, .aep). Para Shotcut, usar shotcut-mcp (`inspect_project`, `animate_clip`, `plan_project_edit`, `render_contact_sheet`) y traducir el EDL; en CapCut/Canva/Premiere/AE habrá que escribir adaptadores (p. ej. FCPXML/EDL CMX3600 para Premiere, JSX para AE).
- 114 issues abiertos y proyecto joven (5 meses): las rutas pueden cambiar; fijar commit al reutilizar.

Sugerencia para "Video-Editing-AI-Agent": adoptar EDL + `project.md` + Hard Rules como núcleo común; añadir librería propia de movimiento (Ken Burns con `zoompan` y easing, xfade, texto ASS animado, keyframes MLT) porque este repo no la aporta; añadir registro de handshake por herramienta (capacidades, versión, ruta de proyecto) y un changelog de la skill.
