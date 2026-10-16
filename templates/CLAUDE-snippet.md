<!-- Pega todo lo que sigue (desde la línea "## gui-skills") en tu ~/.claude/CLAUDE.md. El instalador no edita ese archivo. -->

## gui-skills (skills compartidas)

Estas 9 skills viven en el repo privado **gui-skills**: `direct-visual-design`, `canva-design`,
`design-illustrator`, `rea-reverse-engineer`, `video-editing-ai-agent`, `video-aprender`,
`web-go-high-level-ia`, `seo-content-system` y `seo-content-system-web-hosted`.

- **Fuente canónica:** el clon local del repo. Su ruta es `repo_path` en `~/.gui-skills/config.json`
  (por defecto `~/gui-skills`). Las carpetas en `~/.claude/skills/<skill>` son enlaces a ese clon, no
  copias: **no las reemplaces ni les pegues archivos sueltos encima**. Cualquier cambio a una skill se hace
  en el clon y se publica con un PR (`publish_job.py` o una rama `aporte/<alias>/<tema>`; nunca un push directo a `main`).
- **Paso 0 (cada vez que uses cualquiera de estas skills, no solo al abrir la sesión):** sigue
  `shared/protocolo-skill.md` del clon. Corre `python <repo>/tools/check_update.py --quiet --pull`: si el
  clon está atrasado y limpio, se actualiza solo. `ACTUALIZADA n` -> díselo al usuario en una línea y vuelve
  a leer el `SKILL.md` de la skill antes de seguir; `CAMBIOS_LOCALES` -> avisa y no actualices;
  `SIN_RED` / `SIN_CREDENCIAL` -> sigue con la copia local y dilo. Si la salida avisa de "aportes sin
  publicar", corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado). Luego lee el
  `HANDSHAKE.md` de la skill y el "Registro de trabajos" de su `HANDOFF.md`. El hook `SessionStart` ya hace
  lo mismo al abrir la sesión (`check_update.py --hook --pull`).
- **Paso final (al cerrar un trabajo terminado y aprobado; obligatorio y preaprobado: no pidas permiso):**
  (1) registra la entrada con
  `python <repo>/tools/log_job.py --skill <nombre> --caso <código> --hecho "..." --bien "..." --mal "..."`
  en el HANDOFF de cada skill que intervino; (2) actualiza el `HANDSHAKE.md` si cambió el estado vivo;
  (3) publícalo con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (crea la rama
  `aporte/<alias>/<fecha>-<tema>`, hace commit, sube y abre el Pull Request; si eres el mantenedor
  (`"mantenedor": true` en `config.json`), tu aporte se integra solo); (4) cuéntale al usuario el resultado: `PR_CREADO <url>`, `PUBLICADO <url>`, `PR_MANUAL <url>`,
  `PENDIENTE` o `BLOQUEADO`.
- **Obsidian es opcional:** si el usuario tiene un vault configurado (`obsidian_vault` en
  `~/.gui-skills/config.json`) o el MCP de Obsidian responde, registra también allí (nota del proyecto y
  registro de skills). Si no, sigue sin él y no lo menciones como un error.
- **Privacidad (regla dura):** en el repo, los clientes se nombran solo con un código `caso-<tipo>-<NN>`.
  Nunca escribas en el repo nombres de clientes, marcas, personas, dominios, correos, teléfonos, rutas
  personales, tokens ni claves. La equivalencia código -> cliente vive solo en
  `~/.gui-skills/equivalencias.md`. Si `log_job.py` o el hook `pre-commit` bloquean, corrige el texto;
  no saltes el hook.
- **Aportes:** todo cambio llega a `main` por un Pull Request que revisa el mantenedor. Para los registros
  de trabajo lo hace `publish_job.py` solo; para cambios a mano usa una rama `aporte/<alias>/<tema>`. No
  empujes directo a `main` y no reescribas entradas viejas del registro. Reglas completas en `CONTRIBUTING.md`.
- **No edites a mano** `skills/seo-content-system-web-hosted/`: se regenera con `tools/build_hosted.py`.
