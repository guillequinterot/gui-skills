# Análisis: bradautomates/claude-video (skill /watch)

Nota de verificación: WebFetch devuelve resúmenes de un modelo pequeño. Los archivos se pidieron vía raw.githubusercontent.com, pero los comandos ffmpeg/umbrales citados abajo NO están verificados literalmente; contrastar con el código antes de copiarlos.

## 1. Qué hace, estado, licencia
- Es una skill de COMPRENSIÓN de video, no de edición. `/watch <url|archivo> [pregunta]` descarga con yt-dlp, extrae frames con ffmpeg, obtiene transcripción (subtítulos nativos o Whisper) y entrega todo a Claude para responder.
- Herramientas: Python 3, ffmpeg/ffprobe, yt-dlp, Groq/OpenAI Whisper API. Multi-host: Claude Code (plugin marketplace), Codex, Cursor, Copilot (`npx skills add`), claude.ai (`watch.skill`).
- Actividad: creado 2026-04-24, último push 2026-07-01, v0.2.0 (2026-06-29). ~17.5k estrellas, 194 issues abiertos. Licencia MIT.

## 2. Estructura y organización
- `skills/watch/SKILL.md` (~22 KB) + `scripts/` (watch.py orquestador, frames.py, whisper.py, transcribe.py, download.py, setup.py, config.py, build-skill.sh) + `.skillignore`.
- Raíz: `.claude-plugin/{plugin,marketplace}.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `hooks/hooks.json` + `hooks/scripts/check-setup.sh` (SessionStart), `tests/` (pytest por módulo: dedup, timestamps, whisper, setup, frames...), `CHANGELOG.md`, `AGENTS.md`, `dev-sync.sh`, workflow de release por tag.
- Frontmatter: name `watch`, version 0.2.0, license MIT, allowed-tools Bash/Read/AskUserQuestion. El slash command se deriva del frontmatter (sin wrappers duplicados).
- Patrón clave: la skill es autocontenida; `SKILL_DIR` se resuelve desde la ubicación de SKILL.md, no de variables propias de Claude Code (portabilidad). Versión sincronizada en 3 archivos (SKILL.md, 2 plugin.json).

## 3. Técnicas de video aplicables
(origen: frames.py, watch.py, whisper.py, SKILL.md)
- Muestreo por presupuesto según duración (auto_fps): <=30s 12-30 frames, <=60s 40, <=180s 60, <=600s 80, >600s 100 (tope). Rango enfocado (--start/--end) más denso (x6 si <=5s, x4 si <=15s), fps máx 2.
- Modos de fidelidad `--detail`: transcript (0 frames) / efficient (50 keyframes, `-skip_frame nokey`) / balanced (100, scene-aware) / token-burner (sin tope).
- Detección de escenas: `select='eq(n,0)+gt(scene,0.20)'` + showinfo (primer frame + cambios de escena).
- Escalado: `scale=w='min(res,iw)'...force_divisible_by=2`, JPEG `-q:v 4`; ancho 512 por defecto, 1024 para texto (x4 costo). ~50-80k tokens por 80 frames a 512px.
- Deduplicación: miniaturas 16x16 en gris (una pasada ffmpeg), diferencia media absoluta por píxel, umbral 2.0/255, comparación greedy contra el último frame conservado.
- Frames por cue de transcripción (`--timestamps`): fija frames en momentos absolutos, reservados contra el tope. Cada frame lleva timestamp absoluto y razón (uniform / scene-change / keyframe / transcript-cue).
- Transcripción: subtítulos nativos primero; si no, audio mono 16 kHz MP3 64k (`-vn -ar 16000 -ac 1 -b:a 64k`), Whisper verbose_json con segmentos con tiempo; chunking a 24 MB con offset de timestamps; reintentos con backoff y Retry-After. Groq `whisper-large-v3` preferido, OpenAI `whisper-1` alternativo. Sin whisper local.
- Animación/movimiento/ritmo: NO trata nada de esto (sin transiciones, keyframes de edición ni ritmo). Lo aplicable es la revisión visual y QA:
  - Contact sheet/muestra de frames con timestamp tras renderizar una edición para que el agente "vea" el resultado (equivalente a render_contact_sheet de shotcut-mcp).
  - Scene detection sobre el render para verificar cortes/transiciones en los puntos esperados; dedup para detectar tramos congelados/estáticos.
  - Transcripción del render para verificar subtítulos/voz vs guion y sincronía.
  - Re-inspección enfocada por rango (--start/--end) en zonas con problemas en vez de re-muestrear todo.
  - Frames en cues de audio para comprobar que el visual coincide con la palabra.

## 4. Flujo de trabajo, handoff, estado, logs
- Pipeline: Step 0 preflight (`setup.py --json`, luego `--check` silencioso, exit 0/2/3/4) -> parsear fuente vs pregunta -> watch.py -> leer frames (JPEG) -> responder con citas de timestamp, sin pegar transcripción completa -> limpiar dir temporal (`rm -rf`).
- Salida: reporte Markdown a stdout (metadatos, rango, resumen de frames con motor/candidatos/dedup, lista con timestamps y razón, transcripción). Frames en directorio `watch-*` temporal (o --out-dir).
- Estado/handshake: `~/.config/watch/.env` con `SETUP_COMPLETE=true`, `WATCH_DETAIL`, claves; permisos 0600; el hook SessionStart lo audita y avisa en una línea. Buen patrón de "handshake" de entorno con JSON de estado (`can_proceed`, `first_run`, `missing_binaries`, `platform`).
- Degradación explícita: sin transcripción -> solo frames y se dice al usuario; video largo -> advertencia "sparse scan" y ofrecer re-run enfocado.
- Logs de cambios: CHANGELOG.md por versión (Added/Changed/Fixed/Security/Removed), releases por tag con workflow que empaqueta `watch.skill`. No hay log de ejecución ni handoff entre herramientas.

## 5. Reutilizar / descartar / riesgos
Reutilizar:
- Patrón preflight `--json`/`--check` + hook SessionStart para verificar ffmpeg/melt/Shotcut antes de editar.
- Dial de fidelidad (detail) y presupuesto de frames/tokens para QA visual; frames con timestamp + razón; dedup 16x16; scene threshold ~0.20; foco por rango.
- Chunking/offset de Whisper si se transcribe audio de clips.
- Estructura autocontenida + SKILL_DIR relativo + versión sincronizada + tests pytest + CHANGELOG.
- Modos de fallo documentados explícitamente en SKILL.md.
Descartar:
- Descarga con yt-dlp y soporte de plataformas online (fuera de alcance de edición local), salvo para referencias.
- Dependencia obligatoria de Groq/OpenAI (envía audio a terceros); preferir Whisper local opcional o transcripción bajo consentimiento.
Riesgos:
- Privacidad: audio sale a APIs externas; claves en .env en texto plano (0600 no aplica igual en Windows/NTFS, el chmod es en gran parte inefectivo).
- Windows: setup.py solo imprime comandos winget (`Gyan.FFmpeg`), no instala; el changelog registra bugs previos de consola/emoji y UTF-8 en Windows; SKILL.md usa `python3` y `rm -rf`, que en Windows requieren ajuste (`python`/`py`, Remove-Item). Hardening de argv contra option injection en v0.1.3 (buena práctica a copiar).
- Costo de tokens de imágenes; videos >10 min con cobertura escasa.
- 194 issues abiertos: madurez desigual. Sin nada sobre MLT/Shotcut/CapCut/Premiere/AE: hay que construir el handoff propio.
