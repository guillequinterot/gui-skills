<!-- Pega todo lo que sigue (desde la línea "## gui-skills") en tu ~/.claude/CLAUDE.md. El instalador no edita ese archivo. -->

## gui-skills (skills compartidas)

Estas 9 skills viven en el repo privado **gui-skills**: `direct-visual-design`, `canva-design`,
`design-illustrator`, `rea-reverse-engineer`, `video-editing-ai-agent`, `video-aprender`,
`web-go-high-level-ia`, `seo-content-system` y `seo-content-system-web-hosted`.

- **Fuente canónica:** el clon local del repo. Su ruta es `repo_path` en `~/.gui-skills/config.json`
  (por defecto `~/gui-skills`). Las carpetas en `~/.claude/skills/<skill>` son enlaces a ese clon, no
  copias: **no las reemplaces ni les pegues archivos sueltos encima**. Cualquier cambio a una skill se hace
  en el clon, dentro de una rama `aporte/<alias>/<tema>` (nunca directo en `main`).
- **Paso 0 (antes de usar cualquiera de estas skills):** sigue `shared/protocolo-skill.md` del clon. Corre
  `python <repo>/tools/check_update.py --quiet`; si sale `ATRASADA`, avisa y ofrece `git pull --ff-only`
  antes de seguir; si sale `CAMBIOS_LOCALES`, no hagas pull. Luego lee el `HANDSHAKE.md` de la skill y el
  "Registro de trabajos" de su `HANDOFF.md`. Un hook `SessionStart` ya hace esta comprobación al abrir la
  sesión; si su aviso ya apareció, no la repitas.
- **Paso final (al cerrar un trabajo terminado y aprobado):** registra siempre la entrada con
  `python <repo>/tools/log_job.py --skill <nombre> --caso <código> --hecho "..." --bien "..." --mal "..."`
  en el HANDOFF de cada skill que intervino, y actualiza el `HANDSHAKE.md` si cambió el estado vivo.
  Avisa al usuario que quedó registrado.
- **Obsidian es opcional:** si el usuario tiene un vault configurado (`obsidian_vault` en
  `~/.gui-skills/config.json`) o el MCP de Obsidian responde, registra también allí (nota del proyecto y
  registro de skills). Si no, sigue sin él y no lo menciones como un error.
- **Privacidad (regla dura):** en el repo, los clientes se nombran solo con un código `caso-<tipo>-<NN>`.
  Nunca escribas en el repo nombres de clientes, marcas, personas, dominios, correos, teléfonos, rutas
  personales, tokens ni claves. La equivalencia código -> cliente vive solo en
  `~/.gui-skills/equivalencias.md`. Si `log_job.py` o el hook `pre-commit` bloquean, corrige el texto;
  no saltes el hook.
- **Aportes:** crea una rama `aporte/<alias>/<tema>`, haz commit y abre un Pull Request hacia `main`; lo
  revisa el mantenedor. No empujes directo a `main` y no reescribas entradas viejas del registro. Reglas
  completas en `CONTRIBUTING.md`.
- **No edites a mano** `skills/seo-content-system-web-hosted/`: se regenera con `tools/build_hosted.py`.
