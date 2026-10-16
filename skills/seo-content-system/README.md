# SEO Content System

Skill de estrategia, redacción, auditoría y medición SEO/AEO/GEO. Vive en el repo **gui-skills** (el repo es
la fuente canónica; se instala por enlaces con `tools/install.ps1` / `tools/install.sh`).

- `SKILL.md`: procedimiento. El Paso 0 lee primero `HANDSHAKE.md` / `HANDOFF.md` y la carpeta `memoria/`; la
  bóveda de Obsidian es **opcional** (si el usuario la tiene, se consulta además).
- `references/`: referencias especializadas. `assets/`: plantillas y fuentes oficiales.
- `scripts/`: `capture_learning.py`, `research_update.py`, `scheduler.py`, `validate_vault.py`,
  `editorial_lint.py`, `install.py`. Todos funcionan sin bóveda y guardan en `memoria/`.
- `HANDOFF.md` / `HANDSHAKE.md`: decisiones, registro de trabajos y estado vivo.
- `hosted-src/` + `tools/build_hosted.py`: de aquí se **genera** `skills/seo-content-system-web-hosted/`
  (versión para Claude.ai / ChatGPT sin sistema de archivos). No se edita a mano.
- `WEB-ASSISTANT-PROMPT.md`: mensaje inicial corto para chats web.
