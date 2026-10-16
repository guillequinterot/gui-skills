---
tags:
  - seo
---

# Instalación y sincronización entre plataformas

## Índice

- Fuente canónica
- Formato común
- Ubicaciones
- Instalación en Claude Code (repo)
- Otros destinos (Codex, Antigravity)
- Versión web (sin sistema de archivos)
- Obsidian y su MCP (opcional)
- Mantenimiento
- Limitaciones

## Fuente canónica

La única fuente de verdad es el repo gui-skills: `<repo>/skills/seo-content-system/` (contiene `SKILL.md`, `references/`, `scripts/`, `assets/`, `agents/`, `hosted-src/`, `HANDOFF.md`, `HANDSHAKE.md` y `memoria/`). Ya no existe una fuente en una bóveda de Obsidian ni un instalador que "refresque" copias desde ella.

Como la instalación se hace con enlaces, no hay copias sueltas que puedan desfasarse. Si por alguna razón existe una copia real (no un enlace) en `~/.claude/skills/seo-content-system/`, el instalador del repo la respalda y la reemplaza por el enlace; antes de hacerlo hay que portar al repo cualquier contenido que solo exista en esa copia.

## Formato común

Codex, Claude Code y Antigravity admiten skills basadas en una carpeta con `SKILL.md`, scripts y referencias.

## Ubicaciones

- Codex personal: `~/.agents/skills/seo-content-system/`
- Codex de proyecto: `.agents/skills/seo-content-system/`
- Antigravity de proyecto: `.agents/skills/seo-content-system/`
- Claude Code personal: `~/.claude/skills/seo-content-system/`
- Claude Code de proyecto: `.claude/skills/seo-content-system/`

Las ubicaciones pueden cambiar; verificar documentación oficial si el producto se actualiza.

## Instalación en Claude Code (repo)

La hace el instalador del repo, para todas las skills a la vez:

```bash
# Windows
powershell -ExecutionPolicy Bypass -File <repo>/tools/install.ps1
# macOS / Linux
bash <repo>/tools/install.sh
```

Crea `~/.claude/skills/seo-content-system` como enlace al clon. Los skills solo cargan al iniciar sesión: reiniciar Claude Code antes de dar por buena la instalación.

## Otros destinos (Codex, Antigravity)

`scripts/install.py` queda como ayudante para destinos que el instalador general no cubre. Parte siempre de esta carpeta del repo y crea enlaces (o copia si el sistema no permite enlaces):

```bash
python scripts/install.py --targets codex --dry-run     # ver destinos sin tocar nada
python scripts/install.py --targets codex,antigravity   # instalar por enlace
python scripts/install.py --scope project --project /ruta/al/proyecto --targets codex
```

Opciones: `--force` respalda (`.bak-AAAAMMDD`) y reemplaza un destino que ya existe; `--vault RUTA` guarda `obsidian_vault` en `~/.gui-skills/config.json`; `--schedule weekly` instala la revisión periódica de novedades (ver `update-governance-and-research.md`). Ya no refresca nada desde una bóveda.

## Versión web (sin sistema de archivos)

Para Claude.ai (Project) o ChatGPT (Custom GPT/Project) existe `skills/seo-content-system-web-hosted/`, **generada** con:

```bash
python <repo>/tools/build_hosted.py          # regenera
python <repo>/tools/build_hosted.py --check  # sale con 1 si lo guardado está desfasado
```

Las partes escritas a mano de esa versión viven en `hosted-src/` dentro de esta skill. Cuando cambie esta skill de forma significativa, regenerar; nunca editar la carpeta generada.

## Obsidian y su MCP (opcional)

Obsidian no es necesario. Si el usuario lo usa y quiere que el agente lea y escriba su bóveda, necesita el MCP de Obsidian. Comprobar si ya está registrado:

```bash
claude mcp get obsidian-mcp-server
```

Si no, registrarlo en scope usuario (disponible en todos los proyectos):

```bash
claude mcp add --scope user obsidian-mcp-server \
  -e MCP_TRANSPORT_TYPE=stdio \
  -e OBSIDIAN_API_KEY=<API_KEY_DE_OBSIDIAN> \
  -e OBSIDIAN_BASE_URL=http://127.0.0.1:27123 \
  -- "C:\Program Files\nodejs\npx.cmd" -y obsidian-mcp-server@latest
```

**Dos errores documentados que hacen que el servidor quede en "connecting" sin dar error:**

1. El nombre `obsidian-mcp-server` va inmediatamente después de `--scope user`, **antes** de cualquier `-e`. Si los flags `-e` se ponen antes del nombre, el parser los interpreta como variables de entorno adicionales y el nombre nunca llega al argumento correcto.
2. En Windows, `command` debe ser la ruta absoluta a `npx.cmd`. Usar solo `"npx"` falla en silencio: Node no resuelve la extensión `.cmd` al lanzar el proceso.

La API key se obtiene en Obsidian → Configuración → Community Plugins → "Local REST API with MCP"; Obsidian debe estar abierto y el servidor HTTP (puerto 27123) habilitado. **La API key nunca se escribe en notas, en archivos de la skill ni en el repo.**

Verificar conexión:

```bash
claude mcp get obsidian-mcp-server   # debe decir Connected
```

## Mantenimiento

Para cambiar una regla de la skill:

1. Editar la skill en el repo (en una rama `aporte/<alias>/<tema>`).
2. Si cambió algo que alimenta la versión web, correr `python <repo>/tools/build_hosted.py`.
3. Correr `python scripts/validate_vault.py` (valida la memoria `memoria/` y, si hay bóveda, también su estructura).
4. Abrir el PR; el escáner de privacidad corre antes del commit.
5. Registrar el cambio en `HANDOFF.md` / `HANDSHAKE.md` si cambia una decisión o el estado.

## Actualizaciones

El aprendizaje diario se guarda en `memoria/` (o en la bóveda) y queda disponible para todos los agentes que usen el clon. No se necesita copiar la skill por cada nota nueva. Cuando se modifica una regla estable: editar, registrar la decisión en `memoria/decisiones/` y abrir el PR.

## Limitaciones

- Ninguna skill puede investigar con el equipo apagado.
- La periodicidad depende de un scheduler del sistema o de la plataforma.
- Los agentes necesitan permisos de lectura/escritura sobre el clon (y sobre la bóveda, si se usa).
- El recopilador no convierte novedades en verdad automáticamente.
- Los accesos a GA4, Search Console o CMS deben configurarse fuera de la skill.
