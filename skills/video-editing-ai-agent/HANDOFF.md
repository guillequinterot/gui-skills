# HANDOFF — video-editing-ai-agent

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.
> Historial técnico detallado (cada cambio de la skill, con su evidencia) → `logs/UPDATE-LOG.md`
> (tabla) y `logs/update-log.jsonl` (máquina). Protocolo de handshake/handoff **de un proyecto de video**
> (`video-handoff.md`, `handshake.json`) → `references/handoff-handshake.md`: no confundir con este archivo,
> que es el de la **skill**.

## 1. Qué es y cuándo se usa

Skill **única** de edición de video con IA: entiende un video completo (mapa de planos, movimiento, voz y
fotogramas clave), edita y corta por transcripción, anima (HyperFrames, HTML → MP4), subtitula, corrige color,
mezcla y normaliza audio, produce piezas desde cero (encargo → guion → storyboard → render → verificación) y
exporta. Motores activos: **Shotcut/MLT** (vía `shotcut-mcp`, proyectos `.mlt` editables), **ffmpeg** y
**HyperFrames**. CapCut, Canva, Premiere Pro y After Effects están planificados, **no activos**
(`references/engines-future.md`).

Relación con otras skills:
- **`video-aprender`** (sub-skill, misma familia): aporta el *proceso* de aprender de un link/archivo (clase,
  reunión, referencia) y ejecutar tras confirmación; **sus scripts viven aquí**, en `scripts/`
  (`video_aprender.py`, `slides_extract.py`, `save_learning.py`, `aprender_lote.py`, `fetch_reference.py`…).
- **`rea-reverse-engineer`** (apoyo): se le llama por porción para entender una **web/app** de referencia
  (movimiento, easing, secuencia). El video como tal lo entiende esta skill (`video_understand.py`).
- No hay otra skill de video instalada en `~/.claude/skills`: esta es la única fuente de verdad para video
  (plugins/skills de terceros de HyperFrames, Brag o scrapers **no** se instalan).

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh` la enlazan en `~/.claude/skills/`);
  no se copia a mano. Los scripts se llaman por ruta relativa a la skill o por
  `~/.claude/skills/video-editing-ai-agent/scripts/...` (resuelve al mismo clon).
- **Memoria de la skill** (`memoria/videos-aprobados.*`, `memoria/aprendizajes.*`): viven **dentro de la skill**
  (ruta relativa a los scripts) y se versionan con el repo, ya anonimizadas. `$VEA_MEMORY_DIR` apunta a otra
  carpeta si alguien prefiere una memoria privada fuera del repo.
- Guía completa del stack: `install/INSTALAR-EN-OTRO-CLAUDE-CODE.md` y `install/install-shotcut-stack.ps1`
  (`-DryRun`, `-SkillOnly`, `-WithHyperFrames`). **Verificado solo en el Windows 11 del mantenedor.**
- Dependencias externas (versión con la que se verificó):

| Dependencia | Para qué | Verificado con |
|---|---|---|
| Python ≥ 3.10 + `faster-whisper`, `pillow`, `numpy` | transcripción local por palabra (+ VAD Silero incluido), PNG de texto, mediciones | Python 3.12; faster-whisper 1.2.1 (modelo `small`, CPU); numpy 2.4; Pillow 12.2 |
| Shotcut (+ `melt`, `ffmpeg`, `ffprobe` incluidos) | editor y render de proyectos `.mlt` | Shotcut 26.8.1, MLT 7.41.0, ffmpeg n8.1.2 (sin `drawtext`/`ass`/`subtitles`) |
| `shotcut-mcp` (MIT, `matrodrigs/shotcut-mcp`) | MCP que controla `.mlt` | v1.5.6, commit `f1b78d350a99…` |
| Node ≥ 22 + `npx hyperframes@0.8.162` + `chrome-headless-shell` de Playwright | motor HyperFrames (HTML → MP4) | Node 22.15.0; hyperframes 0.8.162; headless shell 148 |
| `yt-dlp` (Unlicense) | material de referencia (`fetch_reference.py`) | 2026.08.19 (YouTube e Instagram público OK) |
| PyMuPDF (opcional) | leer PDF de diapositivas (`--slides`) | 1.27 |

- **Pasos de entorno que dependen de la máquina** (ver `references/engine-hyperframes.md` y
  `scripts/handshake.py`, que imprime un `env_block_git_bash` listo para pegar): en Windows, 3 arreglos
  obligatorios para HyperFrames (navegador headless de Playwright en `HYPERFRAMES_BROWSER_PATH`, FFmpeg/FFprobe de
  Shotcut por `HYPERFRAMES_FFMPEG_PATH`/`HYPERFRAMES_FFPROBE_PATH` sin tocar el `PATH`, telemetría desactivada).
  En macOS/Linux **no hay nada verificado**: comprobar con `scripts/handshake.py` y `scripts/selftest.py`.
- **Autorización de yt-dlp y cookies (personal):** requiere autorización explícita de **cada usuario**; el
  mantenedor la tiene concedida en su PC desde 2026-10-15. Las protecciones de `fetch_reference.py` (un video por
  llamada, sin cookies por defecto, salida solo en la carpeta del proyecto, `fetch-log.jsonl`) valen siempre.
- Tras instalar o cambiar `scripts/`: `python scripts/selftest.py` (≈30 s; `--speech`, `--whisper`, `--network`,
  `--hyperframes` para pruebas ampliadas). Último resultado conocido: 35/35.

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-09-21 | Skill **única** de video; Shotcut (MLT vía shotcut-mcp) + ffmpeg como motores activos; CapCut/Canva/Premiere/After Effects como stubs `not_configured` | Guille | Un solo flujo, handshake con capacidades reales; no prometer motores sin probar |
| 2026-09-21 | Texto en pantalla = PNG (Pillow) + `overlay`, o clips de texto de Shotcut | Guille (por evidencia) | El ffmpeg de Shotcut no trae `drawtext`/`ass`/`subtitles` |
| 2026-09-21 | Mezcla de música bajo voz: regla **«No sidechain»** de banda completa (ganancia fija bajo voz) por defecto | Guille | Un sidechain de banda completa bombea (medido en una edición real); `carve_music.py` queda como alternativa **a comparar a oído** |
| 2026-09-21 | Volumen con fundidos: interpolación `linear`, nunca `smooth` | Guille (por evidencia) | `smooth` se pasa hasta +3 dB en el tramo plano |
| 2026-09-21 | Nada se exporta ni se sube sin petición explícita en ese turno; exportar = archivo nuevo, nunca sobrescribir | Guille | Reversibilidad |
| 2026-10-15 | **HyperFrames adoptado** como motor de animación compuesta (probado en Windows) | Guille | HTML → MP4 sin editor intermedio, Apache-2.0, encaja con el flujo HTML-first |
| 2026-10-15 | **Remotion rechazado** | Guille | Licencia que cambia con el tamaño del equipo (de pago a partir de 4 personas); HyperFrames cubre lo mismo |
| 2026-10-15 | **Silero VAD adoptado** (ya viene dentro de `faster-whisper`) y usado para validar transcripciones | Guille | Sin instalar nada; detecta alucinaciones de Whisper sobre música |
| 2026-10-15 | **yt-dlp** adoptado con protecciones en código; scrapers/descargadores de terceros rechazados | Guille | Eludir login o límites no es aceptable; ver `references/analisis-fuentes/13-…` |
| 2026-10-15 | Push entre páginas a sangre completa (0.6 s, `power3.inOut`, sin opacidad) en vez de *cut-the-curve* | Guille (por evidencia) | *cut-the-curve* deja un fotograma atenuado con franja oscura en páginas ilustradas; `cut_dip.py` mide hueco 0 % con el push |
| 2026-10-15 | El **banco de pruebas de video** (animaciones y videos de prueba) se da por cerrado | Guille | Ya cumplió su función (validar comprensión, VAD, HyperFrames); no se retoma |
| 2026-10-16 | Sub-skill **`video-aprender`**: aprende y propone, **no ejecuta sin confirmación**; todo en local | Guille | Reuniones confidenciales; evidencia o no se afirma |
| 2026-10-16 | **Biblioteca de videos aprobados**: cada pieza que el usuario aprueba se guarda con su **cita textual**, lo bueno, lo malo y lo «sin decidir» (`scripts/save_approved.py`) | Guille | Un video aprobado es la evidencia más fuerte de gusto, pero la receta es **recomendación con origen, no orden**; lo sin decidir no es preferencia |
| 2026-10-16 | Empuje de cámara en piezas al compás: sutil (≤ 8 %) y señales ancladas al compás en cada pausa ≥ 1 s (**provisional**); la preferencia estética con/sin empuje **sigue sin decidir** | Guille (parcial) | Medido: sin empuje el gancho queda congelado; no se midió qué «se ve mejor» |
| 2026-10-16 | Migración al repo gui-skills: memoria dentro de la skill, sin rutas personales, autorizaciones de herramientas personales por usuario | Guille | Compartir las skills con otras personas sin exponer clientes ni credenciales |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-09-21 · caso-video-02 · guille

- **Qué se hizo:** Primera edición real de la skill: serie de Reels verticales para un cliente, con Shotcut (proyectos `.mlt` vía shotcut-mcp) y ffmpeg. Reels de b-roll sin voz (hook palabra por palabra, escenas con frase completa, `dissolve` de 10 f, CTA de 4 s; 3 en un solo pase por script), Reels con voz a cámara en lote (recorte por envolvente de energía, copy oficial alineado con los tokens de Whisper, RNNoise), un antes/después de 15.2 s y normalización de loudness (Reel 13: −19.3 → −16.0 LUFS sin tocar la imagen). Se creó la v1.0.0 de la skill y se integró el oficio de `browser-use/video-use` (v1.1.0).
- **Salió bien:** Proyectos revisados con contact sheet antes de exportar; reels exportados de 15.2–17.4 s con picos ≤ −2.7 dBFS; elección del tramo de música por energía por segundo (el subidón cae en la Escena 2, ~7.5 s) con ganancia `min(−15.5 − LUFS_tramo, −2 − pico_tramo)`; copy oficial alineado con difflib; medir la música bajo la voz restando el export con música menos el export sin música.
- **Salió mal / incidencia:** `add_transition` solapa clips y acorta el total (539 → 505 f); `smooth` en fundidos de volumen se pasó +3 dB; `remove_item` sin ripple deja hueco en la pista de audio; `xfade=zoomin` sale pixelado (usar `smoothleft/smoothup` o `luma`); el CSV público de la hoja de copy iba por detrás de la versión del cliente (mandaron las capturas); el catálogo de stock de Magnific/Freepik no tiene audio; el conector de Drive no veía las carpetas del usuario (subida manual).
- **Regla candidata:** Aprobar UNA sección antes de replicar el patrón en todo el lote; los `item_ref` de shotcut-mcp son por revisión (reinspeccionar tras cada edición, alias `@x` en lote).
- **Herramientas:** Shotcut 26.8.1; MLT 7.41.0; shotcut-mcp 1.5.6; ffmpeg n8.1.2; Python 3.12; faster-whisper `small`.

### 2026-10-15 · banco-pruebas-video · guille

- **Qué se hizo:** Comprensión de video completo (v1.2): `video_understand.py` (planos, movimiento, voz, silencios, fotogramas clave con presupuesto, hojas de contacto) y `frame_probe.py` (ráfaga, recorte ampliado, mapa de cambio) probados con dos videos reales del banco de pruebas (una animación de 40 s con voz y un stop-motion de 9.7 s con música). Después, VAD (Silero vía faster-whisper) con validación cruzada de la transcripción (v1.3) probado en 3 videos.
- **Salió bien:** Las hojas de contacto se leyeron y contrastaron con el mapa; 6 silencios detectados coincidieron con los límites de frase de Whisper; el VAD (0.51 s para 40 s) detectó que un video tenía 5.04 s de audio en 15.12 s de video.
- **Salió mal / incidencia:** Silencios medidos contra el suelo de ruido marcaban pausas entre palabras de una narración comprimida (ahora p90 − 20 dB con ventana de 0.25 s); Whisper alucinó «Subtítulos por la comunidad de Amara.org» sobre música (filtro `no_speech`/`logprob`/frases típicas + VAD); la heurística «seco vs gradual» genera falsos cortes en stop-motion cuando un objeto grande entra en cuadro (sigue como candidato).
- **Regla candidata:** «Gradual/animado» es heurística, no medida: validarla con más material (fundidos reales, whip-pan, speed ramps) antes de promoverla.
- **Herramientas:** ffmpeg n8.1.2; numpy 2.4.4; Pillow 12.2; faster-whisper 1.2.1 (`small`, CPU).

### 2026-10-15 · banco-pruebas-video · guille

- **Qué se hizo:** Primera prueba de HyperFrames en Windows con una animación de ilustraciones (1080×1170, 30 fps, 40.5 s, con voz): `check`, `snapshot`, `render` (19.5 MB, 2 min 17 s) y comparación de dos versiones de transición entre páginas (*cut-the-curve* v1 frente a push v2) medidas con el nuevo `cut_dip.py`. En la misma sesión se instaló yt-dlp (probado con un video público de YouTube: `info`, video de 15 s, subtítulos) y se escribió `fetch_reference.py` con protecciones.
- **Salió bien:** El push de 0.6 s `power3.inOut` sin opacidad dio hueco 0 % (gap máx. 19.8 % y 16.7 % del ancho con *cut-the-curve* → 0 %); duración del render 40.57 s frente a 40.54 s esperados; selftest 20/20 con prueba de mutación (rompe 2 correcciones y falla 3 pruebas).
- **Salió mal / incidencia:** En Windows, `chrome.exe --version` abre el navegador completo y agota el chequeo de HyperFrames → usar el `chrome-headless-shell` de Playwright; FFmpeg no está en el `PATH` → variables `HYPERFRAMES_FFMPEG_PATH`/`HYPERFRAMES_FFPROBE_PATH`; telemetría activa por defecto → desactivar; `fetch_reference`: `commonpath` falla entre discos, `--max-downloads 1` aborta los metadatos, YouTube responde 429 a subtítulos auto-traducidos; tres bloqueos de ffmpeg n8.1.2 (`alimiter` tras `amix`, `sidechaincompress` con duraciones distintas, dos grafos con `asplit+amix`) resueltos con pasadas separadas, `apad` y tiempo límite en toda llamada.
- **Regla candidata:** *cut-the-curve* es para elementos sueltos sobre un fondo común; para páginas a sangre completa usar push con contacto (pendiente de repetir en otra pieza para promoverla).
- **Herramientas:** hyperframes 0.8.162; Node 22.15.0; ffmpeg n8.1.2; chrome-headless-shell 148 (Playwright); yt-dlp 2026.08.19.

### 2026-10-16 · caso-reel-01 · guille

- **Qué se hizo:** QA final de la skill con un video desde cero: Reel vertical de 29.9 s (1080×1920) para un cliente de rotulación, ruta `musica-al-compas` (8 fotos + 1 video mudo + música de 122 BPM, sin voz), con brief y storyboard con textos, 7 escenas, push entre páginas, fotos en tarjeta con fondo desenfocado de marca y cierre con CTA. Aprobado por el usuario; guardado como V001 en `memoria/videos-aprobados.md`. Se escribió `references/errores-conocidos-y-aciertos.md` y se subió la skill a v1.4.0 (`beat_grid.py`, `motion_energy.py`, `save_approved.py`).
- **Salió bien:** `--batch` con variables (dos variantes comparables con una orden, 2 m 20 s – 2 m 40 s cada una); verificación en orden check → snapshot → render → ebur128 → cut_dip → self_eval → motion_energy (−15.3 LUFS, pico −1.3 dBFS, hueco 0 % en los 4 push); señales ancladas al compás en cada pausa ≥ 1 s (fotogramas casi inmóviles 189 → 71 de 896); fotos en tarjeta + fondo desenfocado: ninguna foto pixelada; el cierre salió de una captura del Instagram de la marca en un solo mensaje.
- **Salió mal / incidencia:** Los datos de contacto del CTA se pidieron al final → rehacer la escena (+5 min); rejilla de compás por autocorrelación gruesa (123 BPM) desplazó los cortes hasta 0.2 s → render completo repetido (~6 min; arreglado con `beat_grid.py`: 122.0 BPM, fase +0 ms); dos `tl.set` sobre el mismo elemento dejaron una escena fuera de cuadro y `check` salió en verde (solo lo vio `snapshot`); un `index_v1.html` dentro del proyecto dio `multiple_root_compositions`; texto con contorno transparente dio `text_not_painted`; un `<video>` con `data-start` no puede ir dentro de una escena con `data-start`; `hyperframes beats` necesita `HYPERFRAMES_FFPROBE_PATH`; un archivo de 36 MB no cabía en el envío (copia ligera con `-crf 24` marcada como vista previa).
- **Regla candidata:** Pedir de una vez CTA, contacto e idioma en el brief y medir la música (`beat_grid.py`) antes del primer render; aprobar la pieza no es elegir entre variantes (lo «sin decidir» se registra aparte).
- **Herramientas:** hyperframes 0.8.162; ffmpeg n8.1.2; numpy; Python (selftest 27/27 al cierre, 31/31 tras `save_approved`).

### 2026-10-16 · caso-aprendizaje-reels-01 · guille

- **Qué se hizo:** 2.º uso real de `video-aprender`: 11 reels públicos de Instagram sobre ML y cuantitativo para trading (25 min de audio) procesados en un lote reanudable (`aprender_lote.py`), sin cookies, en 26.2 min; 6 gráficos/fórmulas leídos de fotogramas y recalculados con Python (GARCH, triple barrera, Sharpe deflactado, probabilidad de stop por régimen). Las ideas se registraron como hipótesis de solo investigación en los proyectos de trading del usuario (`caso-trading-01`), como propuesta y sin tocar su handshake controlado. Resultado: v1.4 de la sub-skill (glosarios de dominio `assets/glosarios/trading.json`, muestreo de fotogramas automático, `--rapido`).
- **Salió bien:** Instagram público sin cookies 11/11; `--rapido` ahorra 18 % (47.4 s → 38.9 s) con 98.8 % de palabras iguales; el glosario como `hotwords` dejó «GARCH» bien las 9 veces; el muestreo de fotogramas (hoja de contacto + más nítido de ±0.5 s + fotogramas donde la voz señala la pantalla) mostró los 6 gráficos de un reel con 16 fotogramas; una afirmación del reel se refutó recalculando (0.99^100 = 37 %).
- **Salió mal / incidencia:** El detector de estados estables dio 0–3 estados en reels con 6 gráficos (cámara filmando un monitor con manos delante) → muestreo de fotogramas; `initial_prompt` de Whisper solo actúa en la 1.ª ventana de 30 s → usar `hotwords`; voz e imagen discreparon en cifras (51 % visto) → manda la imagen; `fetch_reference.py` se negó a escribir dentro de la carpeta de la skill porque el `-o` por defecto es la carpeta actual (siempre `-o <proyecto>`).
- **Regla candidata:** El contenido de captación comercial da **pistas, no evidencia**; varias piezas de una misma cuenta cuentan como **una** fuente; recalcular todo lo recalculable antes de tomar una idea.
- **Herramientas:** yt-dlp 2026.08.19; faster-whisper 1.2.1 (`small`, CPU, `hotwords`); ffmpeg n8.1.2; Pillow; numpy.

### 2026-10-16 · caso-reel-02 · guille

- **Qué se hizo:** Rehacer un Reel de motion graphics vertical de 30 s (1080×1920) para un cliente, tras rechazar el usuario la versión entregada por otra IA (voz de 10.8 s en un video de 30 s, escenas encimadas). Se auditó voz y escenas, se rehizo en HyperFrames con voz aprobada, subtítulos palabra por palabra, objetos neón recortados en local y push al compás. Aprobada por el usuario en su versión 4 (V002 de la biblioteca de videos aprobados); la sección 6 de errores-conocidos-y-aciertos.md recoge la lección.
- **Salió bien:** Línea gráfica aprobada del cliente respetada; check 62/62 sin errores; hueco de push máximo 6.2 %; 54 de 899 fotogramas casi inmóviles; −15.7 LUFS, pico −1.8 dBFS; recortes de objetos neón hechos en local con 0 gasto; guion presentado antes de gastar créditos de voz.
- **Salió mal / incidencia:** Era la segunda versión: la anterior fue rechazada. Dos pushes seguían con hueco de 4–6 % tras el primer ajuste; la muestra de voz rechazada ya se había cobrado; los descendentes se recortaban con padding de 8 px. Incidencia: Escenas que solo se mostraban y nunca se ocultaban dejaron texto encimado en 4 de 6 fotogramas; adelantar entradas dejó tramos quietos nuevos (191 a 244 fotogramas), resueltos con empuje de cámara 1.0 a 1.028 y barrido en las pausas.
- **Regla candidata:** Al rehacer una pieza rechazada, comparar primero la duración de la voz con la del video y revisar una hoja de contacto del estado heredado antes de tocar el diseño.
- **Herramientas:** hyperframes; ffmpeg; transcribe_words.py; cut_dip.py; motion_energy.py; snapshot; stock Magnific (recortes locales)

### 2026-10-16 · caso-reel-02 · guille

- **Qué se hizo:** Variante a pedido del cliente del Reel aprobado (V002): se sustituyó la persona de la escena 5 por una persona del cliente, sin tocar la animación. Recorte local con make_person_cutout.py (flood fill y GrabCut sobre fondo cuadriculado), un único archivo person.png a reemplazar, y render_and_verify.sh. Aprobada por el usuario como cliente-v1 (V003 de la biblioteca).
- **Salió bien:** Cambio de persona sin tocar la animación; métricas idénticas a V002 (54 de 899 fotogramas casi inmóviles, hueco de push máximo 5.2 %, −15.7 LUFS, pico −1.8 dBFS); cero créditos gastados.
- **Salió mal / incidencia:** Dos iteraciones de layout hasta evitar que el titular y las fichas taparan el rostro.
- **Regla candidata:** Dejar cada pieza con un único archivo sustituible para las variantes del cliente (p. ej. person.png) y un script de render y verificación que repita las mismas métricas.
- **Herramientas:** make_person_cutout.py; render_and_verify.sh; hyperframes; ffmpeg; cut_dip.py; motion_energy.py

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| *cut-the-curve* solo para elementos sueltos; push con contacto para páginas a sangre completa | banco-pruebas-video | candidata (una sola pieza; aprobada solo para esa) |
| Empuje de cámara con/sin: preferencia estética | caso-reel-01 | **sin decidir** (aprobar la pieza ≠ elegir variante) |
| Carve de música (`carve_music.py`) frente a EQ estático / «No sidechain» | caso-reel-01 (no había voz) | abierta: necesita una pieza con voz en off y escuchar 3 versiones |
| Heurística «seco vs gradual/animado» (dominancia del salto ≥ 2.5) | banco-pruebas-video | candidata: validar con metraje real |
| Palabras cortas (the/of/and) en pantalla 0.2–0.4 s parpadean: unirlas a la siguiente | caso-video-02 | candidata (pendiente de feedback del cliente) |
| Filtro `typewriter` del subtítulo de Shotcut (requiere `qtext`) | — | sin probar |
| Procesar 2 reels en paralelo no gana tiempo en 4 núcleos | caso-aprendizaje-reels-01 | sospecha, no medida |
| Al rehacer una pieza rechazada, comparar primero la duración de la voz con la del video y revisar una hoja de contacto del estado heredado antes de tocar el diseño. | caso-reel-02 | candidata |
| Dejar cada pieza con un único archivo sustituible para las variantes del cliente (p. ej. person.png) y un script de render y verificación que repita las mismas métricas. | caso-reel-02 | candidata |
