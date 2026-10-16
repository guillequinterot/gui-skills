# Handshake, handoff y log de actualizaciones

> **Ojo:** este archivo describe el handshake/handoff **de un proyecto de video** (`handshake.json`, `video-handoff.md`). El traspaso y el estado de la **skill misma** (qué se decidió, qué se verificó y dónde, registro de trabajos terminados) están en `../HANDOFF.md` y `../HANDSHAKE.md`.

Tres piezas separadas, cada una con su archivo.

## 1. HANDSHAKE = "¿qué puedo hacer aquí y ahora?"
Comprobación de capacidades reales del entorno. Se hace al inicio de cada sesión/proyecto nuevo (y cuando algo falle).
`python scripts/handshake.py --project <carpeta>` escribe `<proyecto>/handshake.json` y lo imprime:
- `engines.shotcut_mcp`: si el servidor está registrado (`claude mcp list`) y Shotcut/melt existen; `engines.ffmpeg`: ruta, versión, filtros clave (`drawtext, ass, subtitles, xfade, zoompan, loudnorm, arnndn, silencedetect`).
- `tools`: python, faster-whisper, Pillow, numpy, ffprobe.
- `engines.hyperframes` (v1.4): `status` (`tested` / `needs_setup`), Node, el headless shell de Playwright, ffmpeg/ffprobe de Shotcut y un **`env_block_git_bash` listo para pegar** (las variables `HYPERFRAMES_*`). `production` (v1.4): qué scripts de producción están, si existe la lista de errores y cuántos **videos aprobados** hay (`approved_videos`).
- `fonts`: Arial/Arial Black/Segoe UI en `C:\Windows\Fonts`.
- `future_engines`: CapCut/Canva/Premiere/After Effects → `not_configured` salvo que un adaptador esté activado y verificado.
- `recommended_engine` y `warnings` (p. ej. "sin drawtext → texto por PNG").
Regla: no asumir capacidades no listadas. Si `handshake.json` tiene <24 h y el entorno no cambió, reutilizarlo.

Handshake de **contenido** (fuente de copy): antes de editar, leer el copy oficial (hoja/brief) y confirmar con el usuario: título, copy en pantalla, teléfonos/CTA, idioma, formato y destino. Registrar cuál fila/versión se usó.

## 2. HANDOFF = "¿dónde quedó el trabajo?"
Archivo `video-handoff.md` en la carpeta del proyecto (plantilla `assets/handoff-template.md`). Es el traspaso entre sesiones, agentes y herramientas. Contiene: objetivo, fuente de copy, motor y versión, archivos (fuentes, proyecto, exportaciones), decisiones (con motivo), estado por pieza, pendientes, próxima acción, riesgos/no verificado, y "cómo retomar" (comandos).
- Al terminar cada tramo de trabajo: actualizarlo **y**, si el usuario usa Obsidian, reflejar lo esencial en la nota de su proyecto.
- Al empezar: leerlo, resumir la última sesión en una frase y confirmar próxima acción.
- Traspaso entre motores (p. ej. Shotcut → CapCut): usar el EDL neutro (`assets/edl-schema.json`) como contrato: fuentes, rangos, capas de texto, audio, transiciones con tiempos en segundos y frames.
- Traspaso a subagentes: brief autocontenido (objetivo en 1 frase; ruta absoluta de salida; spec técnica res/fps/códec; marca; línea de tiempo con easing; anti-lista; entregables; "no hagas preguntas, elige la interpretación más obvia"). Incluye siempre la ruta del handoff.
- Estado de jobs largos (patrón super-video-maker): `job_state.json` con `job_id, status, stage, artifacts, metrics, next_action`; cada herramienta imprime `RESULT: {...}`.

## 3. LOG DE ACTUALIZACIÓN DE LA SKILL
`logs/UPDATE-LOG.md` (tabla) + `logs/update-log.jsonl` (máquina). Sirve para que la skill evolucione según **dónde** y **cómo** se edita.
Registrar con `python scripts/log_update.py --engine shotcut --kind learning --change "..." --evidence "..." [--project X]`.
Tipos: `learning` (aprendizaje verificado), `fix` (corrección de una regla errónea), `engine-add` (nuevo motor), `engine-verify` (motor futuro pasa de stub a verificado), `source` (nueva skill/fuente analizada), `deprecation`.
Reglas:
- Solo registrar lo **comprobado** (medición, preview, error real). Hipótesis → sección "Candidatos" sin promover.
- Un aprendizaje se promueve a regla en `references/` cuando se repite en 2 proyectos o el usuario lo aprueba.
- Cada entrada: fecha, motor, tipo, cambio, evidencia, proyecto, versión de herramientas.
- Además: anótalo en `HANDSHAKE.md` / `HANDOFF.md` de la skill; si el usuario usa Obsidian, también en su registro global de skills.
- Versionado: semver en `logs/UPDATE-LOG.md` (cabecera). Cambios que rompen el flujo → mayor.

## 3b. Acceso y lectura rápidos (recetas medidas; revisar cuando algo cambie)
Dónde se anotó que la skill se acelera según **cómo leer la información y cómo acceder/ejecutar**. Cada línea tiene su medición.
| Situación | Receta | Medido |
|---|---|---|
| Varios links de video para aprender | `aprender_lote.py fuentes.txt -o <proyecto>\… --glosario <dominio> --prefijo X` en **segundo plano** | 11 reels = 26.2 min sin intervención; reanudable |
| Instagram público | `fetch_reference` / `video_aprender URL` **sin cookies** + `-o <proyecto>` (nunca desde la carpeta de la skill) | 11/11 sin cookies |
| Exploración rápida | `--rapido` | −18 % de tiempo, 98.8 % de palabras iguales |
| Jerga del dominio mal oída | `--glosario trading` (hotwords + correcciones); `initial_prompt` **no** (solo 1.ª ventana) | «GARCH» 9/9 bien |
| Pantalla = cámara filmando un monitor | muestreo automático → leer **primero `hoja.jpg`**, luego solo el fotograma de la cifra a resolución completa | 16 fotogramas mostraron los 6 gráficos del reel; ahorra ~16 lecturas |
| Cifra dicha o vista que importa | recalcular con Python **antes** de citar; manda la imagen sobre la voz | 1 afirmación refutada; 51 % (visto) vs 52 % (parecía) |
| Registrar ideas en un proyecto con reglas | leer su plantilla/protocolo primero; handshake controlado = **propuesta**, no edición | caso-trading-01: su verificación de flujo dio 0 errores antes y después |
| Medir el tiempo de una tanda larga | avisar antes; Monitor sobre el log; no sondear | |
Pendiente de medir: TikTok; videos de >1 h; si `--rapido` + glosario basta para siempre (¿cuándo conviene `medium`?); procesar 2 reels en paralelo (sospecha: sin ganancia en 4 núcleos).

## 4. Cierre de una pieza APROBADA → biblioteca (v1.4)
Cuando el usuario aprueba una pieza (con palabras suyas: «genial», «está perfecto», «así está bien»), además del handoff:
1. Guarda su **cita textual** (sin ella no se guarda: `scripts/save_approved.py add --quote "..."`).
2. Separa **lo aprobado explícitamente** de **lo que quedó sin decidir** (p. ej. «con o sin empuje de cámara»: aprobar la pieza no es elegir una variante). Lo sin decidir no se usa como preferencia.
3. Registra **lo bueno** (repetir), **lo malo** (evitar, con su costo) y **lo medido**; las lecciones generales nuevas van además, en una línea con evidencia, a `references/errores-conocidos-y-aciertos.md`.
4. La receta es una **recomendación que nombra su origen**, nunca una orden: en una pieza nueva el usuario y el brief actual mandan.
5. Pieza de **prueba o test** (como V001): se documenta igual, marcando que fue una prueba.
Al **empezar** una pieza nueva: `python scripts/save_approved.py suggest --route R --format F` y leer la lista de errores.

## Ciclo de vida
handshake → handoff (leer) + `errores-conocidos-y-aciertos.md` + `save_approved.py suggest` → trabajo → QA → handoff (escribir) → si el usuario aprobó: `save_approved.py add` → log (si hubo aprendizaje) → «Registro de trabajos» del HANDOFF de la skill (+ nota de Obsidian si la hay).

## Memoria por sesión (v1.1, de video-use `project.md`)
Cada sesión añade un bloque a `video-handoff.md` (sección "Historial de sesiones"):
```
### Sesión N — AAAA-MM-DD
**Estrategia:** un párrafo con el enfoque
**Decisiones:** tomas, cortes, color, animaciones y por qué
**Registro de razonamiento:** una línea por decisión no obvia
**Pendiente:** lo aplazado
```
Al arrancar: léelo y resume la última sesión en una frase antes de preguntar si continuar. Las transcripciones cacheadas y `takes_packed.md` viven en `<proyecto>/edit/` y no se regeneran salvo que cambie la fuente.
Si el proyecto tiene `analisis/<video>/understanding.md` (v1.2), enlázalo en el handoff y no regeneres el mapa salvo que cambie el video (mismo nombre y duración = reutiliza `video-map.json`). El handshake incluye `video_understanding` (ready / transcription).
