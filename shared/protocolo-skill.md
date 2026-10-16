# Protocolo común de las skills de gui-skills

Toda skill de este repo sigue estos tres pasos. Cada `SKILL.md` lo enlaza al inicio con el bloque
"Protocolo gui-skills" (ver `templates/bloque-protocolo-skill.md`) y no lo repite entero.

Rutas: `<repo>` es el clon local de gui-skills (lo dice `~/.gui-skills/config.json` → `repo_path`;
si no existe el archivo, es la carpeta dos niveles arriba de esta skill). `<skill>` es
`<repo>/skills/<nombre>`.

---

## Paso 0 — Antes de arrancar: ¿la skill está al día?

1. Corre `python <repo>/tools/check_update.py --quiet` (una vez por sesión; si el hook `SessionStart`
   ya lo corrió y dejó su aviso en esta sesión, no lo repitas).
2. Lee la salida:
   - `AL_DIA` → sigue.
   - `ATRASADA n` → dile al usuario "hay n cambios nuevos de la skill en GitHub" y ofrece
     `git -C <repo> pull --ff-only`. Si acepta, haz el pull **antes** de leer el resto de la skill.
   - `CAMBIOS_LOCALES` → hay cambios sin subir en el clon: avísalo y no hagas pull hasta que el usuario
     decida (subirlos con un PR o descartarlos).
   - `SIN_RED` o `SIN_CREDENCIAL` → sigue con la copia local y dilo en una línea.
3. Lee `<skill>/HANDSHAKE.md` (estado vivo: versión, herramientas verificadas, pendientes) y la sección
   "Registro de trabajos" de `<skill>/HANDOFF.md` (las últimas 10 entradas como mínimo) antes de actuar.
   No confíes en tu conocimiento general sobre una herramienta si el HANDSHAKE dice otra cosa.

## Paso 1 — Durante el trabajo: privacidad

- Los clientes, marcas, personas, dominios, correos, teléfonos, direcciones, textos y archivos de un
  cliente **nunca** se escriben en el repo. En el repo un caso se nombra solo con un código:
  `caso-<tipo>-<NN>` (p. ej. `caso-web-universidad-01`). La equivalencia código → cliente la guarda cada
  persona en su PC (`~/.gui-skills/equivalencias.md`), nunca en el repo.
- Nada de rutas personales (`C:\Users\<nombre>`, `D:\<carpeta-personal>`): usa `~`, `<repo>`, `<skill>`
  o `<carpeta-del-proyecto>`.
- Nada de tokens, claves, contraseñas ni cookies. Si la tarea necesita una credencial, va al gestor de
  credenciales del sistema o a un archivo fuera del repo.
- Los archivos del proyecto del cliente (briefs, entregables, capturas) viven en la carpeta del proyecto
  del usuario, no en la skill.

## Paso final — Al cerrar un trabajo: memoria

Cuando un trabajo queda **terminado o implementado y el usuario lo da por bueno**, se registra siempre
(regla aprobada por el mantenedor; no hace falta pedir permiso cada vez, solo avisar que se registró):

1. Escribe la entrada en el HANDOFF de cada skill que intervino:
   `python <repo>/tools/log_job.py --skill <nombre> --caso <código> --hecho "..." --bien "..." --mal "..." [--incidencia "..."] [--regla-candidata "..."]`
   El script anonimiza contra `~/.gui-skills/private-terms.txt`, pasa el escáner de privacidad y agrega
   la entrada al final de "Registro de trabajos" (nunca reescribe entradas anteriores). Si el script no
   está disponible, agrega la entrada a mano siguiendo `templates/entrada-de-trabajo.md`.
2. Si cambió el estado vivo de la skill (una herramienta nueva verificada, un pendiente resuelto, una
   versión nueva), actualiza `HANDSHAKE.md`.
3. Una **regla candidata** no es regla todavía: pasa a `SKILL.md` o a las referencias solo cuando se
   repite en dos o más trabajos o el mantenedor la aprueba. Al promoverla, anótalo en el HANDOFF.
4. Si el usuario tiene Obsidian (`obsidian_vault` en `~/.gui-skills/config.json`, o el MCP de Obsidian
   responde), registra además allí, **con los nombres reales** si quiere (su vault es privado):
   la nota del proyecto y, si el cambio es de la herramienta, la nota de registro de skills que indique
   `obsidian_registry_note`. Sin Obsidian, este punto se salta sin más.
5. Ofrece subir el registro: commit en una rama `aporte/<alias>/<tema>` y PR (ver `CONTRIBUTING.md`).
   El hook `pre-commit` vuelve a pasar el escáner; si bloquea, se corrige el texto, nunca se salta el hook.

## Qué NO hacer

- No editar `seo-content-system-web-hosted/` a mano: se regenera con `tools/build_hosted.py`.
- No reescribir ni borrar entradas viejas del "Registro de trabajos": se agregan correcciones como
  entradas nuevas.
- No convertir una observación de un solo trabajo en regla global.
