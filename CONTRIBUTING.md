# Cómo aportar a gui-skills

Este repo mejora con cada trabajo real. Estas son las reglas para que siga siendo útil y privado.

## 1. La regla del registro: cada trabajo terminado deja una entrada y se publica solo

Cuando un trabajo queda **terminado o implementado y el usuario lo da por bueno**, se registra siempre, en el
`HANDOFF.md` de **cada skill que intervino** (sección "4. Registro de trabajos") y **se publica en GitHub
automáticamente** (sección 3). No hace falta pedir permiso cada vez; solo informar el resultado. Claude lo hace
en el "Paso final" del [protocolo](shared/protocolo-skill.md); tú también puedes hacerlo a mano:

```
python <repo>/tools/log_job.py --skill direct-visual-design --caso caso-web-universidad-01 \
  --hecho "Se maquetó la home en HTML con el sistema de espaciado acordado" \
  --bien "Partir el trabajo por secciones evitó rehacer todo" \
  --mal "El export a PDF rompió una fuente" \
  --incidencia "La fuente se sustituyó; se resolvió incrustándola" \
  --regla-candidata "Incrustar fuentes antes de exportar PDF" \
  --herramientas "Claude Code, Chromium headless"
```

Qué hace el script: pasa tu texto por el escáner de privacidad (con tu `private-terms.txt`); si algo coincide,
**se niega a escribir** y te dice qué campo y qué dato (no reescribe por ti); si todo está limpio, agrega la entrada
justo antes de `<!-- registro:fin -->` con el formato de [`templates/entrada-de-trabajo.md`](templates/entrada-de-trabajo.md)
y, si diste `--regla-candidata`, una fila en la tabla "5. Reglas candidatas". `--dry-run` muestra la entrada sin escribir.
Tu alias sale de `~/.gui-skills/config.json` (o `--alias`).

Cada campo es una sola línea: sé concreto (qué pasó, cuál fue la causa, cómo se resolvió), no un resumen vago.

### Códigos de caso

En el repo un trabajo se nombra **solo con un código**, nunca con el nombre del cliente:

- `caso-<tipo>-<NN>`: tipo en minúsculas y guiones, número de dos dígitos (`caso-web-universidad-01`,
  `caso-diplomas-02`, `caso-reel-01`).
- `banco-pruebas-<tema>`: pruebas propias sin cliente (`banco-pruebas-video`).

El siguiente número libre de un tipo es el siguiente al último que aparece en los HANDOFF. La equivalencia
código -> cliente la guardas tú en `~/.gui-skills/equivalencias.md`, que **no** está en el repo.

### Reglas candidatas y reglas aprobadas

- Una **regla candidata** es lo que aprendiste en un trabajo; vive solo en el registro y en la tabla "5. Reglas
  candidatas (sin aprobar)" de ese HANDOFF.
- Se vuelve **regla aprobada** (pasa a `SKILL.md` o a `references/`) solo cuando **se repite en dos o más casos
  distintos** o **el mantenedor la aprueba**. Al promoverla, se anota en el HANDOFF de la skill (tabla de
  decisiones) con fecha y quién la aprobó.
- Nunca conviertas la observación de un solo trabajo en una regla global.

### Nunca reescribas el registro

Las entradas del registro **solo se agregan al final**. Si una entrada tenía un error, agrega una entrada nueva
que la corrija. No borres ni edites entradas viejas, ni siquiera las tuyas: son la memoria de la skill.

## 2. HANDSHAKE: el estado vivo

Si el trabajo cambió algo del estado de la skill (una herramienta nueva verificada o que dejó de funcionar, un
pendiente resuelto o nuevo, una versión), actualiza su `HANDSHAKE.md`: la tabla de herramientas con fecha de
verificación, "Pendientes abiertos", "Límites conocidos", y "Última actualización" con tu alias. Aquí sí se edita
el contenido (es estado, no historia). Si el HANDSHAKE contradice lo que "sabes" de una herramienta, manda el HANDSHAKE.

## 3. Ramas y Pull Requests

### Lo normal: `publish_job.py` lo hace solo

Con los cambios del trabajo (normalmente las entradas de `log_job.py`) todavía sin commitear en `main`:

```
python <repo>/tools/publish_job.py --tema caso-web-universidad-01
```

Qué hace, en orden: actualiza `main` si está atrás (guarda tus cambios, `pull --ff-only`, los devuelve; si chocan,
se detiene sin tocar nada) -> crea la rama `aporte/<alias>/<AAAA-MM-DD>-<tema>` (si existe, agrega `-2`, `-3`...) ->
`git add` y commit (el hook `pre-commit` corre el escáner; si bloquea, devuelve todo a `main` con tus cambios
intactos y avisa `BLOQUEADO`) -> `git push -u origin` (sin force, nunca a `main`) -> abre el Pull Request
(`gh`, o la API de GitHub con tu credencial de git, o te da el enlace de comparación) -> vuelve a `main` limpio.
Solo publica cambios dentro de `skills/`; para tocar `shared/`, `templates/`, `tools/` o la documentación agrega
`--incluir-todo` (y avisa en el PR, porque afecta a todas las skills).

Resultados: `PR_CREADO <url>`, `PUBLICADO <url>` (solo el mantenedor: fusiona el PR y borra la rama; sale con `--merge` o, de forma automática, con
`"mantenedor": true` en `~/.gui-skills/config.json`; `--no-merge` lo evita),
`PR_MANUAL <url>`, `PENDIENTE <rama>` (sin red: queda guardada, se sube con `publish_job.py --reintentar`; el Paso 0
lo avisa en cada uso de una skill), `BLOQUEADO`, `SIN_CAMBIOS`. `--dry-run` muestra los pasos sin hacer nada.

### A mano

1. Trabaja en una rama `aporte/<alias>/<tema>` (ejemplo: `aporte/ana/registro-caso-web-01`):

   ```
   git -C <repo> switch -c aporte/<alias>/<tema>
   ```

2. Haz commit (el hook `pre-commit` corre el escáner; si bloquea, corrige el texto: no se salta el hook) y sube la rama:

   ```
   git -C <repo> add -A
   git -C <repo> commit -m "Registro: caso-web-universidad-01 en direct-visual-design"
   git -C <repo> push -u origin aporte/<alias>/<tema>
   ```

3. Abre un Pull Request hacia `main`. El mantenedor lo revisa (contenido y privacidad) y lo fusiona.
4. Después vuelve a `main` y actualiza: `git -C <repo> switch main` y `git -C <repo> pull --ff-only`.

**No hay protección técnica de `main`**: GitHub Free no permite proteger ramas en repos privados, así que
"no empujar directo a `main`" es un acuerdo entre todos. Un push directo con un error afecta a las 9 skills de todos.

Con la actualización automática (`check_update.py --pull`), tu clon se mantiene al día solo mientras esté limpio y en
`main`: un trabajo a medias en el clon (`CAMBIOS_LOCALES`) detiene la actualización hasta que lo publiques o descartes.

Tu `user.name` en el clon debe ser tu alias (lo fija el instalador) para que cada commit diga quién fue, aunque
el token sea compartido. Usa también un correo no personal (`<alias>@gui-skills.local`).

## 4. Lo que va en un aporte

- Mejoras a una skill (`SKILL.md`, `references/`, `scripts/`) con su razón en la descripción del PR y, si es una
  regla nueva, el caso (código) donde se vio.
- Entradas del registro y cambios de HANDSHAKE.
- Cambios a `tools/`, `shared/` o `templates/`: avisa en el PR, porque afectan a todas las skills.

## 5. La skill generada no se edita a mano

`skills/seo-content-system-web-hosted/` es un derivado de `seo-content-system` (para Claude.ai y ChatGPT). Se
regenera con `python tools/build_hosted.py`. Si lo editas a mano, el cambio se pierde en la siguiente
regeneración y las dos versiones se desalinean. Cambia siempre `seo-content-system` y regenera.

## 6. Antes de abrir el PR

- [ ] Ningún nombre de cliente, marca, persona, dominio, correo, teléfono, ruta personal ni credencial (ver [PRIVACY.md](PRIVACY.md)).
- [ ] Casos solo con código (`caso-<tipo>-<NN>`).
- [ ] No reescribí entradas viejas del registro.
- [ ] Si cambió el estado vivo de una skill, actualicé su `HANDSHAKE.md`.
- [ ] `python tools/privacy_scan.py` pasa en limpio.
- [ ] Si cambiaste las herramientas: `python -m unittest discover -s tests` pasa.
