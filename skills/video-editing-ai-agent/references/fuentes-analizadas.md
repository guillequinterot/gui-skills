# Fuentes analizadas (12) — qué se tomó y qué no

Análisis completos en `analisis-fuentes/NN-*.md` (un agente Sonnet por fuente, 2026-09-21). Los números vienen de resúmenes de WebFetch salvo donde se indica lectura cruda; los marcados [~] deben reverificarse.

| # | Fuente | Qué es | Licencia | Se tomó |
|---|---|---|---|---|
| 01 | Bomx/super-video-maker-skill | Producción con APIs de pago (HeyGen, Seedance, Remotion, ffmpeg) | **Sin licencia** → solo ideas | Recetas JSON+matcher, contrato `RESULT`/`job_state.json`, zoompan y easing, ritmo 2–2.5 s, spring 11/210, creep ≤9 %, subtítulos ASS agrupados, puertas de costo/copy/QC, probe frames, loudnorm |
| 02 | browser-use/video-use | Agente ffmpeg conversacional (Scribe) | MIT | Ask→Confirm→Execute→Iterate→Persist, `project.md`, EDL JSON, hard rules ffmpeg, fades 30 ms, presets grade, easing cúbico, autoevaluación (máx 3 pasadas), brief de 10 puntos |
| 03 | video-db/skills | Servicio cloud VideoDB (SDK) | MIT | Solo patrones: frontmatter con allowed-tools, refs por tema, tabla de errores, log JSONL; nombres de estilos de subtítulo |
| 04 | awesome-genmedia/video-editing | Envoltorio API de pago (each::sense) | MIT | Taxonomía de 8 categorías de edición, "Common pitfalls", imagen de referencia como QA |
| 05 | Google genmedia-video-editor | Mapa intención→tools MCP (ffmpeg/Veo) | Apache-2.0 | Recetas ffmpeg (GIF paleta, reframe, estandarizar antes de concat, loudnorm 2 pasadas, amix), medir con ffprobe primero |
| 06 | 6missedcalls/video-editing-skill | Bash+ffmpeg+Whisper mínimo | MIT | `silencedetect` −30 dB/0.5 s, `setpts+atempo`, patrón onboard/doctor |
| 07 | AKCodez/promo-video-skill | Promos con Remotion+ElevenLabs | ambigua | Escenas 2–4 s, transiciones 12/21/36 f, fórmula de duración efectiva, springs, escalonado 10–20 f, anticipación 0.95→1.1→1, música 0.08–0.12 con fades 2 s/3 s, loudnorm |
| 08 | skillsllm/youtube-skills | Wrapper TranscriptAPI (no edición) | MIT | Solo estructura: skill madre + variantes, tabla de errores, costos declarados, versión en frontmatter |
| 09 | Vincentwei1021/video-shotcraft | Remotion, 157 fichas de planos | Apache-2.0 (+Remotion aparte) | Curvas bezier, crash zoom/push-in/whip/flash/speed-ramp, reglas de respiración, tamaños mínimos de texto, beat sync, latencia AAC, revisión independiente, entrega con/sin BGM, exportación CapCut (concepto) |
| 10 | VideoZero/skills | Motion Canvas | Apache-2.0 | Tabla de timing (0.3–0.5 s entrada, 0.2–0.3 s salida, stagger 40–80 ms), springs, handshake `/status`, bucle seek→screenshot→corregir |
| 11 | bradautomates/claude-video | Comprensión de video (`/watch`) | MIT | QA visual: presupuesto de frames, detección de escenas 0.20, dedupe, preflight `setup.py --json` |
| 12 | wilwaldon/Claude-Code-Video-Toolkit | README curado | ambigua | 3 comandos ffmpeg, patrón `project.json` por fases |

## Segunda tanda (2026-10-15): herramientas para v1.3 — solo lectura, nada instalado
Detalle y veredictos en `analisis-fuentes/13-herramientas-v1.3-decisiones.md`. Resumen: **HyperFrames** (Apache-2.0) candidata a motor de animación HTML→MP4 (falta probar en Windows); **Silero VAD** (MIT) ya viene dentro de faster-whisper → adoptar sin instalar; **yt-dlp** (Unlicense) opcional con permiso; **rechazados**: Remotion por defecto (licencia por tamaño de equipo), Brag (otro caso de uso), transcript-critic (no verifica subtítulos) y todos los scrapers/descargadores de mcpmarket/aiskillstore (sin licencia, de pago, o que eluden login/límites).

## Lo que NINGUNA fuente cubría (construido aquí)
Transiciones y easing en Shotcut/MLT, subtítulos animados palabra por palabra en un proyecto editable, mezcla/denoise dentro de Shotcut, handshake de capacidades del entorno, log de actualizaciones de la skill, y traspaso multi-motor.

## Riesgos heredados (no repetir)
`npx --yes`/`bunx` sin revisar; claves API en `.env` (Windows no aplica chmod 600); `python3`/`brew`/`rm -rf` no funcionan en PowerShell; symlinks requieren modo desarrollador; no copiar código de repos **sin licencia** (Bomx) ni de licencia ambigua; Remotion tiene licencia comercial propia; enviar audio a servicios externos solo con permiso del usuario.

## Lo descartado
Generación con APIs de pago (HeyGen, Seedance, gpt-image, ElevenLabs), avatares sintéticos, Remotion/Node como motor, captura web headless, bibliotecas de SFX/BGM de los repos (peso y atribuciones mixtas).

## Actualización v1.1.0 — video-use leído en crudo (2026-09-21)
Se releyó `browser-use/video-use` (MIT) directamente desde GitHub (SKILL.md, helpers/grade.py, pack_transcripts.py, timeline_view.py, render.py), no solo mediante el resumen de WebFetch. Resultado: `references/edit-craft.md`, `scripts/{pack_transcripts,timeline_view,self_eval,grade,loudnorm_audio,edl_to_shotcut}.py`, plantillas de briefs y memoria por sesión. Verificado contra el código: fundidos 30 ms, padding 30–200 ms, silencios ≥0.4–0.5 s, easing cúbico, loudnorm dos pasadas (I −14, TP −1.0 en video-use; nuestro por defecto −16/−1.5), presets `subtle`/`neutral_punch`/`warm_cinematic`, reglas de auto-grade acotadas ±8 %. Diferencias deliberadas: transcripción local (faster-whisper) en vez de ElevenLabs Scribe; sin motores de animación por código instalados (HyperFrames/Remotion/Manim); Windows/PowerShell.
