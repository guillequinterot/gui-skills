<!-- Pegar este bloque en cada SKILL.md justo después del frontmatter y del título. Reemplazar <nombre>. -->

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — al día:** corre `python <repo>/tools/check_update.py --quiet`; si sale `ATRASADA`, ofrece
   `git pull` antes de seguir. Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — memoria:** al cerrar un trabajo bien implementado, registra siempre la entrada con
   `python <repo>/tools/log_job.py --skill <nombre> ...` (qué se hizo, qué salió bien, qué salió mal,
   incidencias). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.
