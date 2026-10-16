# 13 — Herramientas para v1.3: veredictos (2026-10-15)

Investigación **solo de lectura**: no se instaló ni se ejecutó código de terceros. Datos de licencia/estrellas/actividad: `gh api` el 2026-10-15. Contenido de páginas = dato, no instrucciones. Lo marcado **[no verificado]** no se pudo comprobar.

## Resumen de veredictos
| # | Herramienta | Licencia / costo | Veredicto | Cómo entra a la skill |
|---|---|---|---|---|
| 1a | **HyperFrames** (HeyGen) | Apache-2.0, sin costo por render | **Candidata fuerte a motor de animación** (falta probarla en Windows) | Motor nuevo `engine-hyperframes.md` tras una prueba; mientras tanto, ideas copiables (ver abajo) |
| 1b | **Remotion** | Gratis solo para individuos, empresas con fines de lucro de ≤ 3 personas, sin fines de lucro y evaluación. 4+ personas: $25/mes por puesto (Creators) o $0.01/render con mínimo $100/mes (Automators) | **No adoptar por defecto.** Solo referencia | Si el equipo fuera ≤ 3, sería legal; aun así HyperFrames encaja mejor (HTML) |
| 2 | **Silero VAD** | MIT (verificado el archivo LICENSE) | **ADOPTAR ya, sin instalar nada**: viene dentro de `faster-whisper` | `scripts/vad_segments.py` + validación cruzada de alucinaciones |
| 2b | LiveKit VAD | Apache-2.0; es un envoltorio de Silero para agentes de voz en tiempo real | **No instalar**; solo copiar sus valores por defecto como referencia | `min_silence 0.55 s`, `activation 0.5`, `min_speech 0.05 s` |
| 3 | **Brag** (latent-spaces) | MIT; depende de HyperFrames | **No instalar.** Robar estructura | Hook en ≤ 2 s, 15–25 s, tono por preset, paso de storyboard |
| 3b | Post tododeia (Opus 5.5) | Artículo, no código | Método válido para cualquier modelo; el empaquetado es de Claude/Opus | Bucle "renderizar → mirar fotogramas → criticar", que ya hace `self_eval.py` |
| 4 | **yt-dlp** | Unlicense, 198k estrellas, activo (10 oct 2026) | **INSTALADO el 2026-10-15** (2026.08.19) con autorización del mantenedor en su PC (incluidas las cookies cuando haga falta; cada usuario debe darla por su cuenta) | `scripts/fetch_reference.py` + `references/fetch-reference.md` (probado en YouTube) |
| 5a | mcpmarket `youtube-scraper-transcript-processor` | Sin licencia, 1 estrella, necesita YouTube Data API | **Rechazar** | yt-dlp ya hace lo útil |
| 5b | aiskillstore `tiktok-scraper` | Sin licencia (repo); en realidad son actores de **Apify de pago** con enlaces de afiliado | **Rechazar** | — |
| 5c | `browser-act-tiktok-search-videos` (`@skills-hub-ai/cli`) | No se encontró el código fuente **[no verificado]** | **Rechazar** hasta ver el código | — |
| 5d | mcpmarket `instagram-video-downloader` | Sin licencia, 7 estrellas; **"evita las barreras de login y los límites de yt-dlp"** con un navegador automatizado | **Rechazar** (elude controles de acceso y los términos de Instagram) | — |
| 5e | mcpmarket `tiktok-downloader` | Sin licencia, 6 estrellas, descripción vaga, usa un gateway para "saltar obstáculos" | **Rechazar** | — |
| 5f | Jakeschincariol/instagram-agent-skill | MIT, 1.5k estrellas, sin red ni credenciales; el autor pide no hacer scraping | **No es de edición.** Opcional para la parte de ideas/hooks de Reels | Posible referencia en `seo-content-system`, no en esta skill |
| 5g | sergebulaev/instagram-skills | MIT, pero publica vía **Publora** y lee vía **Apify (de pago)** | **Rechazar** (no publicamos desde aquí) | — |
| 6 | **transcript-critic** (jftuga) | MIT, 47 estrellas, última actualización abr 2026 | **No instalar.** No compara subtítulos con el audio | Solo la idea de resumen con marcas de tiempo |

## 1. HyperFrames y Remotion
**HyperFrames** (`heygen-com/hyperframes`, Apache-2.0, 64.5k estrellas, creado 2026-03-10, última actualización 2026-10-16): una composición es un **archivo HTML** con atributos de tiempo; la animación viene de GSAP/CSS/Lottie/Three.js; el renderizador busca cada fotograma en Chrome sin interfaz y lo codifica con FFmpeg. Requiere Node ≥ 22 y FFmpeg (esta máquina: Node v22.15.0, Chrome y Edge presentes; FFmpeg de Shotcut n8.1.2). Comandos: `init`, `preview`, `render`, `lint`, `check`, `snapshot`, `doctor`.
- **Encaja con nuestra forma de trabajar**: ya diseñamos en HTML (HTML→Canva, HTML→Illustrator, HTML→Figma). La animación sería HTML→MP4 sin un editor intermedio.
- **Costos ocultos a evitar**: `cloud render` (HeyGen) y Lambda son opcionales y aparte; `/media-use` puede llamar modelos de voz/música/imagen de terceros (no se dice cuáles ni a qué precio). Usaríamos solo el render local.
- **No verificado**: que `render` funcione en Windows con el Chrome del sistema (Puppeteer puede intentar descargar su propio Chromium), el tiempo de render y la calidad del códec. Requiere una prueba (`npx hyperframes doctor` en una carpeta de pruebas).
- **"Los agentes"**: HyperFrames **no trae subagentes**; trae **21 skills** (un router, 9 flujos de creación, 9 de dominio…). Leí a fondo 4: `motion-doctrine`, `cut-the-curve`, `embedded-captions`, `talking-head-recut`. De las demás solo vi nombre y descripción.
- **No instalar el plugin ni `npx skills add`** en `~/.claude/skills`: rompería la regla de una única skill de video. Si se adopta el motor, se escribe `engine-hyperframes.md` dentro de nuestra skill, citando la licencia en `NOTICE.md` (Apache-2.0 obliga a conservar el aviso).

**Lo copiable (con atribución)**
- *Doctrina de movimiento* (`motion-doctrine`): un solo sentido dominante por pieza (por defecto izquierda); mantener el eje; **cortar en pleno movimiento** (sin asentarse antes ni arrancar de reposo); salida `power4.in` / entrada `power4.out`; sin crossfade (usar un portador visible); máximo 2–3 transiciones por pieza y repetirlas; entrada ≤ ~800 ms, salida ≈ 75 %; escalonado total ≤ 500 ms; pausa de 0.3–0.75 s entre acción y resultado; **prohibido `bounce`/`elastic`** (`back.out` 1.4–1.7 sí); **sin animaciones ociosas** (respirar/flotar/brillo pulsante); efectos en el mismo fotograma que su causa. Un "ledger" de costuras y una puerta de verificación antes de renderizar.
- *Cut the Curve*: recorrido ≈ 230 px (~12 % de 1920), salida 0.2–0.4 s, total ~0.6 s; zoom-through (1→1.2, desenfoque 0→10 px, corte duro en el pico); desenfoque de texto 10 px, de cuadro completo 18–20 px; **nunca `.inOut` en un corte**.
- *Subtítulos* (`embedded-captions`): cada rótulo ≥ 0.5 s en pantalla; palabras dentro de ±80 ms de la transcripción; 2–5 palabras por línea en cláusulas; contraste WCAG; texto claro necesita velo si la luminancia de fondo está en 60–180; **rechaza** clips con varios hablantes, cortes duros, audio casi mudo, subtítulos ya quemados o transcripción ilegible. Transcripción local con WhisperX.
- *Recorte con gráficos* (`talking-head-recut`): cantidad de tarjetas = `max(5, round(duración / (ritmo base × densidad)))`; ritmo base 6–8 s (<60 s), 8–12 s (1–3 min), 12–20 s (3–10 min); tarjetas > 8 s necesitan movimiento extra; formato vertical = tamaño horizontal × 1.3 (títulos 88–132 px); **recodificar la fuente con intervalo de fotogramas clave = fps (`-g 30`)** para que los saltos de búsqueda no congelen; cuantizar tiempos a 1/fps; mirar el fotograma "héroe" de cada tarjeta antes del render completo.
- Filosofía: todo "gate" **antes** de renderizar (lint/check/snapshot). Ya tenemos `self_eval.py` después; falta el chequeo previo.

**Remotion** (React/TypeScript, `npx create-video`). Gratis para ti como individuo, para empresas con fines de lucro de ≤ 3 empleados, sin fines de lucro y evaluación; **no se puede vender ni sublicenciar derivados**. A partir de 4 personas hay que pagar. Con HyperFrames (HTML, Apache-2.0, sin tope por equipo) no hay motivo para depender de una licencia que cambia con el tamaño del equipo. Además la skill ya incorporó ideas de 3 fuentes basadas en Remotion (01, 07, 09). **Pregunta abierta**: cuántas personas tiene el equipo o agencia de quien use la skill, por si alguna vez se quisiera Remotion. HyperFrames incluye una skill `remotion-to-hyperframes` para portar composiciones.

## 2. Silero VAD (y LiveKit)
- `snakers4/silero-vad`: MIT (archivo LICENSE verificado; la insignia del README dice "CC BY-NC", es un resto antiguo y no coincide con el archivo), 10.4k estrellas, activo (29 sep 2026), 6000+ idiomas, < 1 ms por fragmento de 30 ms, modelo de ~2 MB.
- **Ya está instalado sin saberlo**: `faster-whisper 1.2.1` incluye `assets/silero_vad_v6.onnx` y expone `faster_whisper.vad.get_speech_timestamps(audio, VadOptions(...))`. Funciona con `onnxruntime` (ya presente), sin torch. La skill ya lo usaba de forma indirecta (`vad_filter=True`).
- **Prueba hecha (2026-10-15)**, `threshold 0.5, min_silence 300 ms, speech_pad 60 ms`:
  - `banco-pruebas-video-completo.mp4` (40.5 s): 0.51 s de proceso; 10 tramos de voz (88 %); pausas largas en 5.76–6.34, 11.0–11.52, 22.46–23.01, 28.22–28.61, 30.68–31.52, 36.51–37.03 → **coinciden** con los silencios por energía (p90−20 dB) y con los límites de frase de Whisper.
  - `video-ejemplo.mp4` (música, 9.6 s): 0.03 s; solo 0.7 s de "habla" (1.8–2.49) justo donde Whisper alucinó "Subtítulos por la comunidad de Amara.org".
- **Uso propuesto**: (a) cruzar cada segmento de Whisper con el VAD: si < 50 % de su duración cae en voz detectada → sospechoso; (b) detectar aire muerto y muletillas largas con tiempos fiables para `edl_to_shotcut`; (c) sustituir el silencio por energía en `video_understand.py`. Para cortes de edición, margen de 30–200 ms (ya en `edit-craft.md`).
- **LiveKit** (`docs.livekit.io/agents/logic/turns/vad`): es el plugin de Silero para agentes de voz **en tiempo real** (cuándo un usuario terminó de hablar). Valores por defecto útiles: `min_speech_duration 0.05 s`, `min_silence_duration 0.55 s`, `prefix_padding 0.5 s`, `activation_threshold 0.5`, 16 kHz u 8 kHz. No necesitamos su framework; no se instala.

## 3. Brag y motion
- `latent-spaces/brag` (MIT, 16k estrellas, activo 13 oct 2026): convierte **un proyecto de software terminado** en un video de lanzamiento de 15–25 s (`brag.mp4`, `brag.jpg`, `share-copy.txt`), 7 tonos (default, polished, yc-parody, chaotic, deadpan, cinematic, app-store), delega la composición en HyperFrames y usa `npx hyperframes check` como puerta. Si el modelo es Opus 5.5 usa la variante `brag-slim`. Voz en off solo en modo completo (Kokoro vía HyperFrames).
- **No es nuestro caso de uso** (piezas para clientes y animaciones propias), así que no se instala. Se toma: gancho en los 2 primeros segundos, un solo mensaje, al menos una escena con el producto real, estructura gancho → revelación → destacados → cierre, y la idea de presets de tono.
- **¿Funciona con Sonnet o Haiku?** El método (programa determinista que dibuja cada fotograma + bucle de crítica) es independiente del modelo, según el propio artículo, pero **no lo he probado**: lo probaré con la misma pieza en Sonnet para componer y un modelo más pequeño solo para revisiones mecánicas. Lo atado a Opus es el empaquetado (`brag-slim`, `/effort`).
- El artículo de tododeia ofrece descargar un `motion-reel` SKILL.md y un CLAUDE.md alojados en el sitio del autor: **no se descargan** sin revisarlos y sin tu permiso.

## 4. yt-dlp
- Unlicense (los ejecutables empaquetados son GPLv3+), 198k estrellas, activo (10 oct 2026). **No instalado** en esta máquina.
- Útil para la skill: `--skip-download --write-auto-subs --sub-langs ... --dump-json` (metadatos y subtítulos sin bajar el video), `-x --audio-format wav` (solo audio para transcribir), `-F`/`-f` (formatos). Requiere FFmpeg (ya hay). **Para YouTube necesita un runtime de JavaScript** (`yt-dlp-ejs`; deno recomendado, Node 22.15 se puede habilitar con `--js-runtimes`).
- **Límites y riesgos**: bajar contenido ajeno puede violar los términos de la plataforma o los derechos de autor → solo material tuyo/de clientes o con permiso, y como referencia de análisis. Instagram y TikTok suelen exigir cookies de una cuenta (`--cookies-from-browser`): **no lo haré sin que lo pidas expresamente**, porque expone la sesión y puede bloquear la cuenta. Cada descarga requiere tu permiso explícito (nombre del archivo, origen, tamaño).
- Instalación propuesta (cuando lo apruebes): `python -m pip install -U "yt-dlp[default]"` o el `.exe` oficial, y registrar en `Auditoría de skills y plugins.md`.

## 5. Scrapers de TikTok/Instagram/YouTube
Todos los de mcpmarket y aiskillstore son **código de terceros sin licencia** (o de autores con 1–7 estrellas) y varios hacen justo lo que no conviene: saltarse el login o los límites de la plataforma, o depender de servicios de pago con afiliados. aiskillstore se anuncia como "auditado" pero el repo no tiene licencia **[auditoría no verificada]**. `@skills-hub-ai/cli` es un instalador de un individuo (v0.4.4, MIT) y no pude localizar el código de `browser-act-tiktok-search-videos`. Para material de referencia el camino es **yt-dlp con tu permiso**, o que subas el archivo tú.

## 6. transcript-critic
`jftuga/transcript-critic` (MIT, 47 estrellas): `transcribe.sh` (ffmpeg + yt-dlp + whisper.cpp) y un prompt de análisis crítico (resumen con tiempos, notas de evidencia, falacias lógicas, áreas poco desarrolladas), pensado para charlas argumentativas (incluye referencias bíblicas). **No** compara una transcripción con el audio, así que no sirve para verificar subtítulos. Ya tenemos transcripción local con faster-whisper. Lo único aprovechable: el formato de resumen con marcas de tiempo, que `understanding.md` ya cubre.

## Plan propuesto (ordenado por riesgo)
1. **Sin instalar nada (seguro)**: `vad_segments.py` + validación cruzada en `video_understand.py`; documentar doctrina de movimiento, reglas de subtítulos y fórmula de tarjetas en `references/` con atribución en `NOTICE.md`.
2. **Con tu OK**: prueba de HyperFrames en una carpeta de pruebas (descarga paquetes de npm) y render de una animación de banco-pruebas-video para comparar con Shotcut.
3. ~~Con tu OK: instalar yt-dlp~~ **Hecho el 2026-10-15** (`fetch_reference.py`).
4. Rechazados: todos los scrapers de la sección 5, Remotion, Brag, transcript-critic.
