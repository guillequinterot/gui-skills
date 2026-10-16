# Análisis: skill genmedia-video-editor (Google Cloud Platform / vertex-ai-creative-studio)

Ruta base: `experiments/mcp-genmedia/` del repo GoogleCloudPlatform/vertex-ai-creative-studio.
Nota de verificación: WebFetch pasa por un modelo pequeño. El SKILL.md se pidió "verbatim" y salió coherente (3.6 KB, coincide con el tamaño de la API). Los comandos de `compositing_recipes.md` y los filtros de `resize_commands.go` / `loudnorm_commands.go` se obtuvieron como bloques de código. Aun así, ninguno está verificado byte a byte contra el archivo crudo (marcados [resumen-modelo]).

## 1. Qué hace, herramientas, estado, licencia

- Es una skill MUY delgada (3.6 KB, un solo SKILL.md). Es un "rol + guía de uso" sobre dos servidores MCP en Go: `mcp-veo-go` (generación de video con Veo 3/3.1) y `mcp-avtool-go` (envoltorio de ffmpeg/ffprobe con 12 tools).
- NO enseña a editar con criterio creativo. Es un mapeo "intención -> tool MCP" con unas pocas reglas. Toda la lógica ffmpeg vive dentro del binario Go, no en la skill.
- Servicios Google: Veo (video), Gemini Image, Gemini TTS/Chirp 3 HD, Lyria (música), GCS opcional para I/O (URIs `gs://`). Auth: Application Default Credentials.
- Licencia Apache 2.0. El README dice "not an officially supported Google product". Estado: activo. Últimos commits en la carpeta skills: 2026-05-23 a 2026-06-04 (autor G. Hussain Chinoy). Es un `experiments/`, sin garantía de estabilidad.
- Skills hermanas: agent-aware-cli, build-mcp-genmedia, genmedia-audio-engineer, genmedia-image-artist, genmedia-producer (orquestador), genmedia-voice-director, install-mcp-genmedia, story-generator.

## 2. Estructura y organización de la skill

- Carpeta `skills/genmedia-video-editor/` con solo `SKILL.md` (sin scripts, sin referencias, sin assets). Sigue el "Agent Skills Open Standard".
- Frontmatter: `name: genmedia-video-editor`, `description: "Expert in video composition, editing, and format conversion using mcp-avtool-go and mcp-veo-go"`, `allowed-tools` con 9 tools (Veo t2v, i2v, extend, overlay, concat, gif, combine audio/video). La lista exacta no está literal, viene de un resumen.
- Cuerpo: prompt de rol ("You are a specialized video editor and compositor") y secciones: Cinematic Video Generation, Image-on-Video Overlay, GIF Generation, Clip Concatenation, Audio-Video Sync, Technical Tips.
- Disparadores: solo la `description`. No hay lista de frases gatillo.
- Instalación: `gemini skills install <url>`, `/skills link`, o copiar a `.agents/skills/` (Antigravity) o `~/.gemini/antigravity/skills/`. Está pensada para Gemini CLI / Antigravity, pero el formato SKILL.md es portable.

## 3. TÉCNICAS DE ANIMACIÓN Y MOVIMIENTO

Hallazgo honesto: esta skill casi no tiene técnicas de animación. No hay easing, Ken Burns, zoompan, xfade, subtítulos animados, keyframes ni guía de ritmo. Lo poco aplicable:

**a) Movimiento delegado a la IA generativa (SKILL.md)**
- Fórmula de cinco partes para prompts Veo: Cinematografía ("high-angle long shot"), Sujeto, Acción, Contexto, Estilo ("vintage 16mm film"). El movimiento de cámara se pide en la parte de cinematografía del prompt, no con parámetros.
- Audio en prompt: diálogo entre comillas; efectos entre corchetes `[loud thunder]`.
- `negative_prompt` ("blurry", "static", "distorted faces").
- Transiciones entre planos: `veo_first_last_to_video` (dos keyframes -> Veo interpola). Consistencia de personaje: `veo_ingredients_to_video` / `veo_reference_to_video` con hasta 3 imágenes. Modelo rápido `veo-3.1-lite-generate-001` (720p/1080p).
- Producer skill: para video >8 s, escenas de 5-8 s; bumpers Lyria de 5 s con `afade` de entrada/salida (mencionado, sin comando). [resumen-modelo]

**b) Comandos ffmpeg reutilizables (compositing_recipes.md, [resumen-modelo])**
- GIF de dos pasadas: paso 1 `-vf "fps=F,scale=iw*S:-1:flags=lanczos+accurate_rnd+full_chroma_inp,palettegen" pal.png`; paso 2 `-i in -i pal.png -lavfi "fps=F,scale=...[x]; [x][1:v] paletteuse" out.gif`. Defaults recomendados 15 fps y factor 0.33.
- Overlay: `-filter_complex "[0:v][1:v]overlay=X:Y"`. La skill enseña a calcular X/Y desde el tamaño real: esquina inferior derecha = `W-w : H-h`. Es estático, sin fades ni animación.
- Estandarización previa a concat: `scale=W:H:force_original_aspect_ratio=decrease,pad=W:H:0:0,fps=N -c:v libx264 -preset medium -crf 23 -c:a aac -ar R -ac C -b:a 192k`; luego concat demuxer `-f concat -safe 0 -i list.txt -c copy`. Solo cortes secos: ninguna transición.
- Trim: `-ss T -i in -t D -c copy -avoid_negative_ts make_zero` (rápido, cae en el keyframe previo) vs re-encode (exacto por fotograma).
- Reframe (resize_commands.go, [resumen-modelo]): pad `scale=W:H:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=W:H:(ow-iw)/2:(oh-ih)/2:color=C,setsar=1`; crop `scale=W:H:force_original_aspect_ratio=increase:force_divisible_by=2,crop=W:H,setsar=1`. Dimensiones redondeadas a par (mínimo 2). Útil para 16:9 -> 9:16 y 1:1.
- Audio: `volume=XdB`; mezcla `amix=inputs=N:duration=longest`; combinar video+audio `-map 0 -map 1:a -c:v copy -shortest` (mix automático con ajustes dB por pista según el README).
- Loudness EBU R128 en dos pasadas: pass1 `loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json`; pass2 añade `measured_I/TP/LRA/thresh`, `offset`, `linear=true`. Defaults -16 LUFS (web/social) y -23 LUFS (broadcast).

**Lo que falta y habría que aportar con otras fuentes:** curvas de easing, zoompan/Ken Burns, xfade, drawtext/ASS animado, keyframes MLT, ritmo/BPM, safe zones.

## 4. Flujo de trabajo, handoff, estado y logs

- Patrón "inspeccionar antes de actuar": `ffmpeg_get_media_info` (ffprobe JSON) antes de overlay, sync audio o filtros complejos. Regla textual: "Always check media info before attempting complex filters".
- Sync audio/video: medir duración de audio -> igualar duración del video -> combinar.
- Producer skill: orquestador que delega en herramientas/skills especializadas; reintentar una vez en timeout, luego reducir duración y avisar al usuario; URIs GCS completas (`gs://`). Story-generator coordina subagentes en paralelo.
- NO hay handoff formal, estado persistente, manifiesto de proyecto, logs de cambios ni handshake. El README de skills no documenta memoria compartida. El repo tiene tests Go (nombre de salida, resize, loudnorm, trim) y un `verify.sh`, lo que es un buen patrón de validación de la herramienta, no de la skill.
- Salida por defecto `.mp4` H.264 por compatibilidad.

## 5. Reutilizar, descartar, riesgos

**Reutilizar**
- Estructura: SKILL.md corto + tools deterministas detrás (la lógica en el tool, la skill solo dice cuándo usarlo).
- Las recetas ffmpeg listadas arriba, sobre todo reframe pad/crop con `force_divisible_by=2`, paleta GIF de dos pasadas, loudnorm de dos pasadas y trim copy vs re-encode.
- Regla "medir antes de filtrar" y de igualar duración de audio y video.
- Estandarizar todos los clips (resolución/fps/audio) antes de concatenar.
- Estrategia de fallo: reintento único, degradar y avisar.
- Cinco partes + negative prompt si se integra generación con Veo (opcional).

**Descartar**
- Todo lo ligado a Veo/Lyria/Gemini/GCS/ADC (costo y dependencia Google) salvo que el usuario lo pida.
- Instalación vía Gemini CLI / Antigravity.
- El `-c copy` del concat tras estandarizar: sirve, pero no permite transiciones.

**Riesgos**
- Alcance muy corto: no cubre animación, texto, ritmo, keyframes ni handoff. No sirve como base de conocimiento de motion; hay que complementarlo con otras fuentes.
- No editorial: no toca proyectos de Shotcut/MLT, CapCut, Premiere ni AE. Solo ffmpeg lineal.
- Windows: el binario Go y ffmpeg funcionan, pero requieren ffmpeg en PATH (o `MCP_CUSTOM_PATH`); el script instalador es bash. Cuidar rutas con espacios y `concat -safe 0` en list.txt.
- Seguridad: los comandos se ejecutan con URIs de entrada arbitrarias (locales o GCS); usar rutas fijas dentro de la carpeta del proyecto. Repo experimental, licencia Apache 2.0 (se puede reutilizar con atribución del aviso), sin soporte oficial.
- Costo: Veo/Lyria/TTS son de pago por uso; ffmpeg local no tiene costo.
- Recomendación para la skill propia: mantener herramienta ffmpeg como "backend", y añadir aparte un manifiesto de proyecto (JSON/MD con estado, versión, herramienta activa), un registro de cambios, y el protocolo de handoff por herramienta (Shotcut/MLT, CapCut, Canva, Premiere, AE), que aquí no existe.
