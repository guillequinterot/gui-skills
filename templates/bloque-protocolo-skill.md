<!-- Pegar este bloque en cada SKILL.md justo después del frontmatter y del título. Reemplazar <nombre>. -->

## Protocolo gui-skills (obligatorio)

Esta skill vive en el repo **gui-skills** y sigue [`shared/protocolo-skill.md`](../../shared/protocolo-skill.md):

1. **Paso 0 — cada vez que uses la skill:** corre `python <repo>/tools/check_update.py --quiet --pull`.
   `ACTUALIZADA n` → díselo al usuario en una línea y **vuelve a leer este `SKILL.md`** antes de seguir;
   `CAMBIOS_LOCALES` → avisa y no actualices; `SIN_RED` / `SIN_CREDENCIAL` → sigue con la copia local y dilo.
   Si avisa de aportes sin publicar, corre `python <repo>/tools/publish_job.py --reintentar` (preaprobado).
   Luego lee `HANDSHAKE.md` y el "Registro de trabajos" de `HANDOFF.md`.
2. **Privacidad:** en el repo los clientes solo se nombran con un código `caso-<tipo>-<NN>`; nunca
   nombres, marcas, dominios, correos, rutas personales ni credenciales.
3. **Paso final — obligatorio y preaprobado** (trabajo terminado y aprobado por el usuario; no pidas permiso):
   (1) `python <repo>/tools/log_job.py --skill <nombre> ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.
