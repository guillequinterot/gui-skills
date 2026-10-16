# Protocolo común de las skills de gui-skills

Toda skill de este repo sigue estos pasos. Cada `SKILL.md` lo enlaza al inicio con el bloque
"Protocolo gui-skills" (ver `templates/bloque-protocolo-skill.md`) y no lo repite entero.

Rutas: `<repo>` es el clon local de gui-skills (lo dice `~/.gui-skills/config.json` → `repo_path`;
si no existe el archivo, es la carpeta dos niveles arriba de esta skill). `<skill>` es
`<repo>/skills/<nombre>`.

---

## Paso 0 — Cada vez que se usa la skill: ¿está al día?

No es "una vez por sesión": se corre **cada vez que se invoca o se vuelve a usar la skill**, porque una
sesión larga puede quedar atrás de GitHub aunque el hook `SessionStart` ya haya actualizado al abrirla.

1. Corre `python <repo>/tools/check_update.py --quiet --pull`. Compara con GitHub y, si el clon está atrasado
   **y es seguro** (sin cambios locales, sin commits sin subir, en `main`), hace `git pull --ff-only` solo.
2. Lee la primera palabra de la salida:
   - `AL_DIA` → sigue.
   - `ACTUALIZADA n` → se descargaron n cambios. Dilo en una línea y **vuelve a leer el `SKILL.md`** de la
     skill (y su `HANDSHAKE.md`) antes de seguir: pudo cambiar lo que ya habías leído.
   - `ATRASADA n` → hay cambios nuevos pero no se pudieron bajar solos (la salida dice por qué): dilo en una
     línea y ofrece `git -C <repo> pull --ff-only`.
   - `CAMBIOS_LOCALES` → hay cambios sin subir en el clon: avísalo y **no actualices**; que el usuario decida
     (publicarlos con un PR o descartarlos).
   - `SIN_RED` o `SIN_CREDENCIAL` → sigue con la copia local y dilo en una línea.
3. Si la salida trae una línea `AVISO: hay aportes sin publicar: ...`, corre
   `python <repo>/tools/publish_job.py --reintentar` (preaprobado: sube esas ramas y abre sus PR) y cuéntale
   al usuario el resultado.
4. Lee `<skill>/HANDSHAKE.md` (estado vivo: versión, herramientas verificadas, pendientes) y la sección
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

## Paso final — Al cerrar un trabajo: registrar y publicar (obligatorio y preaprobado)

Cuando un trabajo queda **terminado o implementado y el usuario lo da por bueno**, se hacen siempre estos
pasos, **sin pedir permiso** (regla aprobada por el mantenedor): solo se informa el resultado.

1. Escribe la entrada en el HANDOFF de cada skill que intervino:
   `python <repo>/tools/log_job.py --skill <nombre> --caso <código> --hecho "..." --bien "..." --mal "..." [--incidencia "..."] [--regla-candidata "..."]`
   El script anonimiza contra `~/.gui-skills/private-terms.txt`, pasa el escáner de privacidad y agrega
   la entrada al final de "Registro de trabajos" (nunca reescribe entradas anteriores). Si el script no
   está disponible, agrega la entrada a mano siguiendo `templates/entrada-de-trabajo.md`.
2. Si cambió el estado vivo de la skill (una herramienta nueva verificada, un pendiente resuelto, una
   versión nueva), actualiza `HANDSHAKE.md`.
3. **Publica en GitHub, solo, sin preguntar:** `python <repo>/tools/publish_job.py --tema <caso-o-tema>`
   (p. ej. `--tema caso-web-universidad-01`). Con los cambios aún sin commitear en `main`, crea la rama
   `aporte/<alias>/<fecha>-<tema>`, hace commit (el hook `pre-commit` vuelve a pasar el escáner), sube la
   rama y abre el Pull Request. Los amigos obtienen un PR que revisa el mantenedor; el mantenedor puede
   añadir `--merge` para fusionarlo de inmediato. Nunca empuja a `main` ni fuerza nada.
4. Cuéntale al usuario el resultado, según la primera palabra de la salida:
   - `PR_CREADO <url>` → PR abierto para revisión del mantenedor; pásale el enlace.
   - `PUBLICADO <url>` → PR fusionado en `main` (solo con `--merge`).
   - `PR_MANUAL <url>` → la rama ya está en GitHub pero el PR no se pudo abrir solo: el usuario lo abre en ese enlace.
   - `PENDIENTE <rama>` → no hubo red o credencial; el trabajo quedó guardado en la rama local y se subirá
     con `publish_job.py --reintentar` (el Paso 0 lo recuerda en cada uso de la skill).
   - `BLOQUEADO` → el escáner de privacidad rechazó el texto: corrige lo que señala (nunca se salta el hook)
     y vuelve a correr el comando.
   - `SIN_CAMBIOS` → no había nada que publicar.
5. Una **regla candidata** no es regla todavía: pasa a `SKILL.md` o a las referencias solo cuando se
   repite en dos o más trabajos o el mantenedor la aprueba. Al promoverla, anótalo en el HANDOFF.
6. **Obsidian es opcional.** Si el usuario lo tiene (`obsidian_vault` en `~/.gui-skills/config.json`, o el MCP
   de Obsidian responde), registra además allí, **con los nombres reales** si quiere (su vault es privado):
   la nota del proyecto y, si el cambio es de la herramienta, la nota de registro de skills que indique
   `obsidian_registry_note`. Sin Obsidian, este punto se salta sin más.

La privacidad (Paso 1) sigue mandando: si `log_job.py`, `publish_job.py` o el hook `pre-commit` bloquean, se
corrige el texto; nunca se salta el hook. Si trabajaste directamente sobre una rama `aporte/...` (no sobre
`main`), `publish_job.py` no aplica: sube esa rama con `--reintentar` o con git (ver `CONTRIBUTING.md`).

## Qué NO hacer

- No editar `seo-content-system-web-hosted/` a mano: se regenera con `tools/build_hosted.py`.
- No reescribir ni borrar entradas viejas del "Registro de trabajos": se agregan correcciones como
  entradas nuevas.
- No convertir una observación de un solo trabajo en regla global.
