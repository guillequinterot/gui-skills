# CHANGELOG — rea-reverse-engineer

## 1.0.2 — 2026-10-16
- Migrada al repo gui-skills: carpeta renombrada a `rea-reverse-engineer` (antes con espacios), bloque «Protocolo gui-skills» en `SKILL.md`, `HANDOFF.md` y `HANDSHAKE.md` en el formato común (con «Registro de trabajos»), rutas personales reemplazadas por `~`, `<repo>` y `<carpeta-del-proyecto>`, Obsidian pasa a ser opcional.
- Estado del MCP `rea` actualizado: registrado el 2026-10-15 con Node 24 portátil; handshake stdio verificado (207 herramientas) y servidor **conectado en una sesión de Claude Code el 2026-10-16**; ninguna herramienta de análisis ejecutada aún.
- `scripts/install.py` ahora comprueba el enlace al repo (`--check`) y copia solo con `--copy`/`--codex`; `scripts/handshake.py` busca el Node portátil `node-v24*` por patrón.
- Capturas de la web de terceros de `ejemplos/rea-tools/` retiradas del repo (`ejemplos/README.md`); se conservan `probe.md` y `probe.json`.
- Se retiró `_respaldo/` (copias de otras skills y del `CLAUDE.md` del mantenedor; no van al repo).

## 1.0.1 — 2026-10-15
- REA registrado como MCP en Claude Code (`claude mcp add rea --scope user`, comando `cmd.exe /d /c <HOME>\.claude\mcp-servers\node-v24.22.0-win-x64\npx.cmd -y rea-agents@6.5.0 mcp` (`<HOME>` = carpeta personal del usuario)) con **Node 24.22.0 portátil** (SHA-256 verificado; Node del sistema intacto, 22.15.0). `setup --client claude_code --yes` instaló además la skill upstream `reverse-engineer-anything`.
- Verificado por stdio con el Node del sistema: `initialize` (rea 6.5.0) y `tools/list` = 207 herramientas.
- `handshake.py` reconoce el Node portátil.
- Copias de seguridad: `~/.claude.json.bak-2026-10-15-pre-rea` y `~/.claude.json.rea.backup` (contienen tokens de otros MCP: no moverlas a carpetas de proyecto).

## 1.0.0 — 2026-10-15
- Creada como skill propia de **apoyo**, llamada por porción por otras skills (diseño, SEO, video y cualquier otra).
- Contrato de llamada de 5 campos, **Ficha de referencia** (observado/inferido/desconocido, mantener/adaptar/evitar) y plantilla.
- Escalera N0–N3; **sonda N1** `scripts/web_probe.py` (probada en rea.tools: estructura, tipografía, paleta, movimiento, SEO, red, crudo vs renderizado).
- Recetas por consumidor (`references/03`), REA upstream (`references/04`, rea-agents 6.5.0, commit `42fc6c5`), límites (`references/05`).
- `handshake.py` e `install.py` (núcleo: SKILL.md, references, scripts, templates).
- Enrutamiento añadido a `direct-visual-design`, `seo-content-system`, `video-editing-ai-agent` y `~/.claude/CLAUDE.md` (respaldos en `_respaldo/2026-10-15/`).
- **REA no instalado ni ejecutado** (decisión pendiente de Guille; Node 22.15.0 < 22.19).
