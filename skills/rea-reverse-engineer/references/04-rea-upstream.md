# 04 · REA upstream (morluto/rea)

Fuente leída el 2026-10-15 desde el repositorio (API de GitHub) y su `SKILL.md`/`docs/`. Las órdenes salen de la documentación de REA; lo que sí se ejecutó (diagnóstico, `setup`, handshake MCP por stdio) está en `HANDSHAKE.md` y `HANDOFF.md`. **Ninguna herramienta de análisis de REA se ha ejecutado todavía.**

## Qué es
«Reverse engineer anything with agents, from app behavior down to native binaries». Servidor **MCP** y **CLI** (`rea`) que devuelven **Evidence** (resultados con fuentes, límites y desconocidos) para que el agente explique cómo funciona un programa. Análisis local; los resultados llegan al modelo (política de datos del proveedor).

| Dato | Valor (2026-10-15) |
|---|---|
| Repositorio / sitio | `github.com/morluto/rea` · `rea.tools` |
| Licencia | MIT (lo de terceros conserva la suya: `THIRD_PARTY_NOTICES.md`) |
| npm | `rea-agents` **6.5.0** (repo coincide: `git+https://github.com/morluto/rea.git`; bin `rea`) |
| Commit `main` verificado | `42fc6c5` (2026-10-16 02:09Z) · 273 637 estrellas / 68 851 forks según la API |
| Requisitos | Node.js `^22.19 \|\| ^24.11 \|\| >=26` (el Node del sistema del mantenedor, v22.15.0, está por debajo; **se usa un Node 24.22.0 portátil**) |
| Clientes soportados por `setup` | claude_code, claude_desktop, codex, cursor, gemini_cli, antigravity, vscode, windsurf… |

> ⚠ **Si el Node del sistema es < 22.19, no lo uses para REA** (caso del PC del mantenedor: 22.15.0). El registro apunta al `npx.cmd` (o `npx`) de un Node portátil con ruta absoluta y sin espacios, p. ej. `~/.claude/mcp-servers/node-v24.<x>-<plataforma>/`. Si se mueve esa carpeta, el MCP deja de arrancar: re-registrar con `claude mcp remove rea --scope user` y `claude mcp add rea --scope user -- cmd.exe /d /c <ruta-al-node-portátil>\npx.cmd -y rea-agents@6.5.0 mcp` (en Windows con Git Bash anteponer `MSYS_NO_PATHCONV=1`, o `/d` `/c` se convierten en `D:/` `C:/`; en Mac/Linux el comando es `<ruta>/bin/npx -y rea-agents@6.5.0 mcp` sin `cmd.exe`). Actualizar REA = cambiar la versión fijada y re-registrar.

## Instalación y estado (verificado solo en el PC del mantenedor, Windows 11)

**Estado en el PC del mantenedor (2026-10-15, con su aprobación): REGISTRADO como MCP `rea` en Claude Code (alcance usuario, `~/.claude.json`) con un Node 24.22.0 portátil en `~/.claude/mcp-servers/node-v24.22.0-win-x64`.** Comando: `cmd.exe /d /c <ese>\npx.cmd -y rea-agents@6.5.0 mcp`. `initialize` + `tools/list` por stdio: 207 herramientas; el servidor **conectó en una sesión de Claude Code el 2026-10-16**; sin probar con una herramienta de análisis. N0–N1 no lo necesitan. El CLI `rea` sigue fuera del `Path` (usar el `npx` del Node portátil o las herramientas MCP). **Cada usuario debe aprobar por separado** su propio registro y la instalación del Node portátil.

Camino prudente (cada paso con aprobación del usuario):
1. **Diagnóstico sin cambiar nada** (puede descargar el paquete a la caché de npm):
   `npx -y rea-agents@latest doctor --client claude_code --json`
2. **Plan de solo lectura**: `npx -y rea-agents@latest setup --client claude_code --dry-run --json` → mostrar al usuario rutas, copias de respaldo y la skill que reemplazaría.
3. **Aplicar** solo con su sí: `npx -y rea-agents@latest setup --client claude_code --yes` y **reiniciar** Claude Code; comprobar que las herramientas REA aparecen en la sesión.
4. Anotar en `HANDSHAKE.md` de esta skill: fecha, versión, cliente, cambios (y en el registro de skills de Obsidian, si el usuario lo usa).

**Resultado real en el PC del mantenedor, 2026-10-15** (pasos 1–2 ejecutados con aprobación; nada aplicado): `doctor` no sano y `setup --dry-run` → `needs_human`, **plan vacío**, porque Node 22.15.0 < 22.19. Además REA no pudo leer `~/.claude.json` y otras configs («Selected input changed while being read», causa sin determinar, posible particularidad de Windows). N2 sigue sin estar disponible hasta resolver ambas cosas.

**Repetición con Node 24 portátil** (carpeta `node-v24.22.0-win-x64`, anteponer al `Path` solo en el comando): `doctor` con Node OK y `setup --client claude_code --dry-run` → `planned`, 2 acciones (MCP en `~/.claude.json` con copia `.rea.backup`; skill upstream). El error de lectura de configs no se repitió. **Ojo:** el MCP se registra como `cmd.exe /d /c npx -y rea-agents@6.5.0 mcp`; ese `npx` sale del `Path` al arrancar, así que con el Node del sistema (22.15.0) fallaría: tras aplicar hay que apuntarlo al `npx.cmd` portátil. Usar siempre `--client claude_code`.

Cuidados:
- `setup` instala **también la skill de REA** (`reverse-engineer-anything`) en el cliente: puede competir con ésta. Decisión vigente (ver HANDOFF): se conservan ambas, pero **la de REA no se invoca directamente**; ésta es la capa de contrato. Si compite en una sesión real, se desactiva la de REA.
- REA no instala Java, Ghidra, IDA, JADX, Binwalk, etc.; cada motor es opcional y por objetivo.
- Descargas de terceros: **nombre de archivo, fuente y tamaño** al pedir permiso; instalar solo desde fuentes oficiales (GitHub `morluto/rea`, rea.tools, npm `rea-agents`).
- Alternativa **sin registrar MCP**: usar el CLI con `npx -y rea-agents@latest <comando> --json`. Ejemplo: `analyze-javascript-application <ruta> --json` (no necesita motor nativo).
- Navegador para REA web: `REA_BROWSER_EXECUTABLE=<ruta a chrome.exe>` (se verifica Chrome 153 en Linux; **Windows sin verificar**).

## Objetivo → herramienta (condensado del SKILL upstream)

| Objetivo | Primera herramienta |
|---|---|
| ASAR / carpeta JS-Electron | `analyze_javascript_application` (resumen primero, luego `inspect_analysis_view`) |
| Paquete ZIP/APK/IPA/MSIX/DMG | `open_binary` → `inspect_artifact` |
| APK (clases, métodos) | `inspect_android_package` (JADX + JDK) |
| .NET | `inspect_managed_artifact` |
| Firmware | `inspect_firmware_regions` / `extract_firmware` (Binwalk/Unblob, Linux) |
| Binario nativo | `open_binary` + Ghidra/IDA/Hopper |
| Página abierta del usuario | `list_browser_targets` → `inspect_web_page` / `observe_web_session` |
| Acción que debe hacer el agente | `capture_browser_scenario` |
| Captura HAR/SAZ/qlog | `inspect_web_network_capture` |
| Scripts de una captura web | `export_web_scripts` → `analyze_javascript_application` |
| Imports de un módulo | `trace_web_module_imports` |
| Cobertura de ejecución | `observe_web_execution` |
| Listeners de un nodo | `inspect_web_event_listeners` |
| Comparar | `compare_web_captures`, `compare_artifacts`, `compare_functions`, `find_changed_behavior` |
| WASM / EVM / Go / Rust / SQLite / pcap / señal | `inspect_wasm_artifact`, `inspect_evm_interface`, `inspect_go_binary`, `inspect_rust_binary`, `inspect_sqlite_database`, `inspect_pcap_capture`, `decode_signal_recording` |
| Verificar una reconstrucción | `verify_reconstruction` |

El árbol real de herramientas lo da `tools/list` del servidor conectado; si el SKILL upstream de `main` describe algo ausente en la versión instalada, manda el servidor.

## Hábitos de trabajo con REA (de su propia guía)
- **Resumen primero** (`detail: "summary"`), luego vistas paginadas; no repetir llamadas idénticas.
- Cada conclusión: **observación / inferencia / desconocido**, con Evidence ID y límites.
- Preguntas amplias: lista de preguntas + evidencia necesaria, trabajar de lo pequeño a lo grande, **libro de hallazgos** (conclusión → Evidence → confianza → desconocidos).
- Una instalación no se repite para todo: diagnosticar la causa (falta registro, falta reinicio, falta motor).
- Cerrar sesiones nativas (`close_binary`) al terminar.

## Plataformas y límites
- **Linux** es la plataforma mejor verificada; macOS y Windows soportan varios objetivos con salvedades (Ghidra en Windows experimental; Hopper en macOS pide diálogo de licencia).
- Procesos/PTY y GDB: Linux/macOS (GDB solo Linux). Paquetes y firmware: mejor en Linux.
- La **comprensión web (N1)** de esta skill **no depende** de nada de esto.

## Referencias upstream
`docs/web-runtime.md`, `docs/browser-observation.md`, `docs/website-script-export.md`, `docs/website-module-trace.md`, `docs/web-network-captures.md`, `docs/mcp-prompts.md`, `docs/cli.md`, `docs/installation.md`; skill: `.agents/skills/reverse-engineer-anything/`.
