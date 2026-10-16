# Instalar Video-Editing-AI-Agent + shotcut-mcp en otro Claude Code

Probado **solo en el Windows 11 del mantenedor** (macOS/Linux sin probar) con: **Shotcut 26.8.1 + MLT 7.41.0 + shotcut-mcp 1.5.6** (commit `f1b78d350a9992296f0b7f11a55c04819ea25730`, 2026-09-12) + Python 3.12 + faster-whisper. Fecha de la guía: 2026-09-21; ampliada a v1.3 el 2026-10-15.

## Qué hay que instalar (resumen)
| # | Componente | Para qué | Tipo |
|---|---|---|---|
| 1 | **Shotcut 26.8.1** | Editor + `melt.exe` + `ffmpeg.exe` incluidos | Programa (winget) |
| 2 | **shotcut-mcp v1.5.6** (matrodrigs/shotcut-mcp) | Servidor MCP que controla proyectos `.mlt` (30 tools) | **MCP** (no plugin) |
| 3 | **Python 3.10+** | Ejecuta shotcut-mcp y los scripts de la skill | Runtime |
| 4 | `faster-whisper`, `pillow`, `numpy` | Transcripción local por palabra, PNG de texto, mediciones | pip |
| 5 | **Skill `video-editing-ai-agent`** | Flujo, biblioteca de movimiento, handshake/handoff/log, agente exportable | Skill (carpeta) |
| 6 | Git | Para clonar shotcut-mcp | Herramienta |
| 7 | **yt-dlp** (`pip install "yt-dlp[default]"`) | Material de referencia (v1.3) con `fetch_reference.py` | pip |
| 8 | *(opcional)* **Node.js ≥ 22 + HyperFrames** (`npx`, sin instalar globalmente) y un `chrome-headless-shell` | Animación compuesta HTML→MP4 (`references/engine-hyperframes.md`) | Runtime / npx |

No hay claves API ni cuentas de pago. La transcripción es local (no sube audio).

> **Plugin vs MCP:** los comandos `/plugin marketplace add matrodrigs/shotcut-mcp` + `/plugin install shotcut-mcp@matrodrigs` **no dejaron el plugin instalado en nuestro equipo** (solo aparecía figma en `installed_plugins.json`). Lo que sí funcionó es el registro manual como servidor MCP (paso 3). Puedes intentar la vía plugin primero; si tras `/reload-plugins` y reiniciar no aparecen `mcp__shotcut__*`, usa el paso 3.

## Vía rápida (script)
En PowerShell, desde la carpeta de esta guía:
```powershell
powershell -ExecutionPolicy Bypass -File .\install\install-shotcut-stack.ps1            # instala todo
powershell -ExecutionPolicy Bypass -File .\install\install-shotcut-stack.ps1 -DryRun    # solo muestra qué haría
powershell -ExecutionPolicy Bypass -File .\install\install-shotcut-stack.ps1 -SkillOnly  # solo copia la skill
```
Luego **reinicia Claude Code** y verifica (sección "Verificación").

## Vía manual (paso a paso)
1. **Shotcut**: `winget install --id Meltytech.Shotcut` (instala en `%LOCALAPPDATA%\Programs\Shotcut`). Confirma `shotcut.exe`, `melt.exe`, `ffmpeg.exe`, `ffprobe.exe` en esa carpeta. Debe ser 26.8.1 (el MCP está probado con 26.6.25 y 26.8.1).
2. **Python y paquetes**: `python --version` (≥3.10). `pip install faster-whisper pillow numpy "yt-dlp[default]"`.
3. **shotcut-mcp**:
   ```powershell
   git clone https://github.com/matrodrigs/shotcut-mcp "$env:USERPROFILE\.claude\mcp-servers\shotcut-mcp"
   # (opcional, reproducible) git -C "$env:USERPROFILE\.claude\mcp-servers\shotcut-mcp" checkout f1b78d350a9992296f0b7f11a55c04819ea25730
   ```
   Registro global (ámbito usuario), ajustando `<USER>` a tu usuario de Windows:
   ```powershell
   $sc = "$env:LOCALAPPDATA\Programs\Shotcut"
   $cfg = @{ type="stdio"; command="python"
     args=@("$env:USERPROFILE\.claude\mcp-servers\shotcut-mcp\scripts\shotcut_mcp_server.py")
     env=@{ SHOTCUT_PATH="$sc\shotcut.exe"; SHOTCUT_MELT_PATH="$sc\melt.exe"; SHOTCUT_FFMPEG_PATH="$sc\ffmpeg.exe"; SHOTCUT_FFPROBE_PATH="$sc\ffprobe.exe" } } | ConvertTo-Json -Depth 5 -Compress
   claude mcp add-json --scope user shotcut $cfg
   ```
   - Usa `add-json`; con `claude mcp add -e ...` el argumento variádico se traga el comando.
   - Sin `SHOTCUT_MCP_ALLOWED_ROOTS` el servidor puede leer/escribir cualquier ruta. Para limitarlo añade `SHOTCUT_MCP_ALLOWED_ROOTS=<tu-carpeta-de-proyectos>` al `env`.
   - Ejecuta esto desde una carpeta que NO sea el repo clonado (el repo trae su propio `.mcp.json` de ámbito proyecto y crea una entrada duplicada `shotcut`).
4. **Skill**: con el repo gui-skills la instala `tools/install.ps1` / `tools/install.sh` como enlace en `~/.claude/skills/video-editing-ai-agent` (no se copia a mano). Para un solo proyecto: enlaza o copia en `<proyecto>/.claude/skills/`.
5. **Reinicia Claude Code** (las tools MCP nuevas solo aparecen en sesión nueva).

## Pila v1.3 (comprensión de video, referencias, animación)
- **Mapa de comprensión y VAD** no necesitan nada más: usan `faster-whisper` (que ya incluye el modelo Silero VAD), `numpy`, `Pillow` y el ffmpeg de Shotcut.
- **yt-dlp**: el script `fetch_reference.py` lo usa. Para YouTube necesita un motor de JavaScript: **Node ≥ 22** (`--js-runtimes node`, ya lo pone el script). Las **cookies**: Firefox funciona; Chrome/Edge v127+ cifran las cookies y en Windows yt-dlp suele no poder leerlas. Las cookies están implementadas pero **sin probar**; Instagram y TikTok tampoco están probados.
- **HyperFrames (opcional)**: no se instala; se ejecuta con `npx --yes hyperframes@0.8.162`. Requiere **Node ≥ 22**, FFmpeg por variable de entorno y un **`chrome-headless-shell`** (en Windows `chrome.exe --version` abre el navegador completo y HyperFrames se agota). Instalar con `-WithHyperFrames` solo comprueba requisitos y desactiva su telemetría. Detalle y bloque de variables: `references/engine-hyperframes.md`.
- **No instales** el plugin ni las skills de HyperFrames, Brag ni scrapers de terceros en `~/.claude`: la skill de video es la única.

## Verificación
1. `claude mcp list` → `shotcut: ... √ Connected`.
2. En Claude Code: pide "ejecuta shotcut_status y shotcut_doctor". Esperado: `ready: true`, `melt 7.41.0`, doctor `status: tested`, `compatible: true`, sin issues.
3. `python <skill>\scripts\selftest.py` → todas las pruebas OK (añade `--speech`, `--network` o `--hyperframes` para pruebas ampliadas). Luego `python <skill>\scripts\handshake.py` → `recommended_engine: shotcut`; en el ffmpeg de Shotcut aparecerán `drawtext/ass/subtitles = false` (normal: el texto se hace con PNG o clips de texto).
4. Las tools aparecen como diferidas: cárgalas con ToolSearch (`select:mcp__shotcut__inspect_project,...`).

## Exportar el agente editor a un proyecto nuevo
```powershell
python "$env:USERPROFILE\.claude\skills\video-editing-ai-agent\scripts\export_agent.py" --project <carpeta-del-proyecto> --engine shotcut --brand "Marca" --copy-source "URL o ruta del copy"
```
Crea `.claude\agents\video-editor.md`, `video-handoff.md` y `handshake.json`. El subagente aparece tras reiniciar la sesión.

## Otros sistemas / diferencias
- **macOS/Linux**: instala Shotcut desde shotcut.org (o el gestor del sistema), cambia las rutas `SHOTCUT_*` y `python3`. La skill está probada solo en Windows; los scripts usan `%LOCALAPPDATA%` por defecto.
- **Otra versión de Shotcut**: `shotcut_doctor` dirá `untested` (advertencia, no bloquea). Si fallan cosas, instala 26.8.1.
- **Si el ffmpeg de Shotcut cambia**: revisa el handshake; si trae `libass/drawtext`, se pueden usar subtítulos ASS.

## Problemas conocidos
| Síntoma | Causa / solución |
|---|---|
| No aparecen `mcp__shotcut__*` | Falta reiniciar; o el registro no es de ámbito usuario (`claude mcp get shotcut`) |
| `claude mcp add -e` falla | Usa `add-json` |
| Entrada `shotcut` duplicada | Viene del `.mcp.json` del repo clonado; solo aplica si abres Claude Code dentro de esa carpeta |
| `python` no es 3.10+ | Ajusta `command` a la ruta completa del Python correcto |
| Proyecto abierto en la GUI de Shotcut | El servidor solo ve lo guardado en disco: guarda y cierra o evita guardados concurrentes |
| Conector de Google Drive sin acceso | Es otra cuenta; sube los MP4 a mano |
| Música de stock | El catálogo Magnific/Freepik no tiene audio: aporta tu archivo |

## Registro
Cambios de esta instalación: anótalos con `scripts\log_update.py` (motor, tipo, evidencia) y refleja la instalación en tu registro de skills/MCP.


## Memoria del usuario (v1.4)
La carpeta `memoria/` (`videos-aprobados.*`, `aprendizajes.*`) es **dato del usuario**, no código: al reinstalar o actualizar la skill **no la sobrescribas ni la borres**. En una máquina nueva empieza vacía. Tras instalar, corre `python scripts/selftest.py` y `python scripts/handshake.py --json` (mira `engines.hyperframes.status` y `production`).
La ruta de la memoria es `memoria/` dentro de la skill (relativa a los scripts; en el repo gui-skills va versionada y anonimizada) o la carpeta de `$VEA_MEMORY_DIR` si existe. Con la skill instalada como enlace hay una sola memoria.
