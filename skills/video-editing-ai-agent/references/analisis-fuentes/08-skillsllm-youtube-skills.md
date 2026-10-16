# 08 - skillsllm.com/skill/youtube-skills

Aviso de verificacion: todo se leyo via WebFetch (resumenes de modelo pequeno), no archivos crudos literales. No verificado literalmente: endpoints exactos, versiones. Se leyeron: ficha, API de GitHub (arbol y metadatos), README, skills/youtube-full/SKILL.md, references/auth-setup.md, .codex-plugin/plugin.json.

## 1. Que es realmente
- NO es una skill de edicion. Es un toolkit de acceso a YouTube (transcripciones, busqueda, canales, playlists, captions) que envuelve la API comercial de terceros TranscriptAPI.com.
- Ficha: skillsllm, autor ZeroPointRepo (Zero Point Studio), repo https://github.com/ZeroPointRepo/youtube-skills. La ficha dice 311 estrellas; la API de GitHub dice 898 (la ficha esta desactualizada).
- Actividad: creado 2026-02-01, ultimo push 2026-09-21, 4 issues abiertos. Activo.
- Licencia: MIT (repo y plugin.json; la ficha no la indica). Escaneo de seguridad automatico "passed" segun la ficha.
- Agentes: OpenClaw, Hermes, Claude Code, Cursor, Antigravity, Cline, Codex. Instalacion: `npx skills add ZeroPointRepo/youtube-skills --skill youtube-full`.
- Servicio de pago: 100 creditos gratis, luego desde 5 USD/mes. Requiere TRANSCRIPT_API_KEY. Independiente de YouTube/Google.

## 2. Estructura
- 12 skills variantes (transcript, captions, subtitles, video-transcript, yt, youtube-search, youtube-channels, youtube-playlist, youtube-api, youtube-data, transcriptapi, youtube-full) en `clawhub/` (formato ClawHub) y `skills/` (con curl-examples.md por skill).
- Cada skill: SKILL.md (3-13 KB) + references/auth-setup.md (identico, ~7 KB, duplicado 12 veces).
- Extras: .codex-plugin/plugin.json, SECURITY.md, CONTRIBUTING.md, workflow de scanner HOL, dependabot, assets.
- Patron: una skill "full" + variantes finas por intencion, cada una con vocabulario de disparo propio; frontmatter con nombre, version (youtube-full 1.6.2) y requisitos de env.

## 3. Tecnicas de edicion / animacion
- Ninguna. El SKILL.md confirma que no edita, no descarga, no genera subtitulos, capitulos ni miniaturas.
- Aplicable de forma marginal (datos, no tecnica):
  - Transcript JSON con `start` y `duration` por segmento (`include_timestamp`, `format=json|text`): materia prima para generar SRT/VTT o marcar capitulos (skills/youtube-full/SKILL.md). Solo funciona sobre videos YA publicados en YouTube con captions.
  - Metadata devuelve titulo, descripcion, duracion, tags y URLs de miniatura: util para referencia, no para especificaciones de entrega.
- Sin especificaciones de codificacion, resolucion, bitrate ni miniaturas.

## 4. Flujo, handoff, estado, logs
- Flujos simples: Research (buscar, elegir, transcribir) y Monitoring (latest gratuito, luego transcript).
- Manejo de errores documentado por codigo: 401 clave mala, 402 sin creditos, 403/1010 falta User-Agent, 404 sin captions, 429 rate limit. Buen patron: tabla codigo -> causa -> accion.
- Auth con auto-registro: register-cli (email) -> OTP de 6 digitos (10 min) -> verify-cli -> clave permanente; token guardado en archivo temporal para no exponerlo en el output y luego borrado. Persistencia de la clave segun entorno.
- No hay handoff entre agentes, ni estado de proyecto, ni logs de cambios.

## 5. Reutilizar / descartar / riesgos
Reutilizar (patrones, no contenido):
- Estructura "skill madre + variantes por intencion" y tabla de errores codigo -> accion.
- Costos/creditos declarados por operacion antes de ejecutar (analogo: avisar de renders costosos).
- Manejo de secretos: no imprimir tokens, usar archivo temporal y limpiarlo.
- Version en frontmatter y manifiesto por plataforma (.codex-plugin) para el multiplataforma.
- Opcional: usar transcripts de YouTube como insumo de subtitulos/capitulos en un flujo aparte (fuera del nucleo Shotcut/ffmpeg).

Descartar: todo el nucleo (API de transcripciones), la duplicacion de auth-setup x12 y el registro de cuentas por agente.

Riesgos:
- Dependencia de servicio de pago externo de terceros.
- El agente crea una cuenta y guarda una clave en el perfil del shell (superficie sensible; en este entorno crear cuentas esta prohibido para el agente).
- Estrellas de la ficha desactualizadas; fiarse del repo.
- Nada aporta a MLT/ffmpeg/CapCut/Canva/Premiere/After Effects.

Conclusion: valor bajo para Video-Editing-AI-Agent; solo como referencia de organizacion de skills y manejo de errores/secretos.
