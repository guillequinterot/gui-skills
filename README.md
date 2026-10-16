# gui-skills

Repositorio **privado** con las skills de Claude Code de Guille (diseñador) y de los amigos que trabajan con
él. Hay una sola copia de cada skill —este repo—, se instala con enlaces en `~/.claude/skills`, y cada
trabajo terminado deja un registro (qué se hizo, qué salió bien, qué salió mal) que mejora la skill para
todos. Los datos de clientes nunca entran: ver [PRIVACY.md](PRIVACY.md).

## Las 9 skills

| Skill | Para qué sirve | Relación |
|---|---|---|
| `direct-visual-design` | Dirige, crea, evalúa y corrige cualquier trabajo de diseño visual (gráfico, UI/UX o híbrido). | **Skill principal de diseño.** Llama a las tres siguientes según dónde viva el entregable. |
| `canva-design` | Lleva un diseño HTML a Canva dejando todo editable (texto real, capas, verificación por exportación). | Sub-skill de `direct-visual-design`. |
| `design-illustrator` | Lleva un diseño HTML a Adobe Illustrator como archivo limpio y editable (`.ai`, PDF editable). | Sub-skill de `direct-visual-design`. |
| `web-go-high-level-ia` | Construye y mantiene un sitio dentro del constructor de IA de GoHighLevel (AI Studio). | Sub-skill de `direct-visual-design` **y** de `seo-content-system`. |
| `seo-content-system` | Investiga, planifica, redacta, audita y mide contenido para SEO, AEO y GEO. | Llama a `web-go-high-level-ia` cuando el sitio vive en GoHighLevel. |
| `seo-content-system-web-hosted` | Versión de `seo-content-system` para entornos sin archivos (proyectos de Claude.ai, GPT personalizados de ChatGPT). | **Generada**: se produce con `tools/build_hosted.py`; **no se edita a mano**. |
| `video-editing-ai-agent` | Edición de video con IA: cortes por transcripción, motion graphics, subtítulos, color, audio, exportación. | Única skill de video. Sus scripts viven en `video-editing-ai-agent/scripts/`. |
| `video-aprender` | Aprender de un video, clase o reunión con evidencia (cita y marca de tiempo); propone un plan, no lo ejecuta solo. | Sub-skill de `video-editing-ai-agent`; sus scripts están en `video-editing-ai-agent/scripts/`, así que **se instalan juntas**. |
| `rea-reverse-engineer` | Entender cómo está construido un sitio, app o paquete antes de hacer algo parecido (entiende, no copia). | Skill de apoyo: la llaman *por porción* `direct-visual-design`, `seo-content-system`, `video-editing-ai-agent` u otra tarea. |

Cada skill tiene `SKILL.md` (qué hace y cómo), `HANDOFF.md` (instalación, decisiones y registro de
trabajos) y `HANDSHAKE.md` (estado vivo: versión, herramientas verificadas, pendientes).

## Requisitos

- **git** (en Windows, Git for Windows trae Git Credential Manager).
- **Python 3.9 o superior** (las herramientas usan solo la biblioteca estándar).
- **Claude Code**.
- Opcional: **Obsidian** con el plugin Local REST API (si lo tienes, las skills registran también allí; si no, funcionan igual).
- Acceso al repo: un token que te comparte el mantenedor (ver [Credenciales](#credenciales)).

## Instalación en 5 pasos

**1. Instala los requisitos** (git, Python 3.9+, Claude Code) y comprueba `git --version` y `python --version`
(en Mac, `python3 --version`).

**2. Guarda la credencial** que te pasó el mantenedor por mensaje privado, **antes** de clonar:
sigue [Credenciales](#credenciales). Es el paso donde más gente se atora.

**3. Clona el repo.**

```powershell
# Windows (PowerShell)
git clone https://github.com/guillequinterot/gui-skills.git "$HOME\gui-skills"
```

```bash
# Mac / Linux
git clone https://github.com/guillequinterot/gui-skills.git ~/gui-skills
```

**4. Corre el instalador.** Pide tu alias (el nombre corto con el que firmarás tus aportes: minúsculas, sin espacios).

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File "$HOME\gui-skills\tools\install.ps1"
```

```bash
# Mac / Linux
bash ~/gui-skills/tools/install.sh
```

Es seguro correrlo otra vez. Para no usar la actualización automática: `-NoHook` (Windows) o `--no-hook` (Mac).
Para pasar el alias sin preguntar: `-Alias ana` / `--alias ana`. Qué hace:

- crea `~/.gui-skills/config.json` (tu alias y la ruta del clon) y una plantilla `private-terms.txt`;
- enlaza cada skill en `~/.claude/skills/<skill>` (junction en Windows, enlace simbólico en Mac); si ya
  tenías una carpeta con ese nombre, la mueve a `~/.gui-skills/backup-<fecha>/` antes de enlazar;
- activa los hooks de git del clon (`core.hooksPath .githooks`) y fija tu `user.name` y un `user.email`
  no personal (`<alias>@gui-skills.local`) en el clon;
- agrega a `~/.claude/settings.json` un hook `SessionStart` que actualiza las skills solo si hay cambios nuevos
  (conserva tus hooks, reemplaza un hook anterior de gui-skills en vez de duplicarlo y hace una copia de
  seguridad antes de tocar el archivo).

**5. Dos cosas a mano y reinicia Claude Code.**

- Abre `~/.claude/CLAUDE.md` y pega el bloque de [`templates/CLAUDE-snippet.md`](templates/CLAUDE-snippet.md).
  El instalador no edita ese archivo a propósito.
- Abre `~/.gui-skills/private-terms.txt` y escribe, uno por línea, los nombres de **tus** clientes, marcas y
  personas (el formato está en el encabezado del archivo). Ese archivo nunca sale de tu computadora.

`~/.gui-skills/config.json` también acepta, opcionales, `"mantenedor": true` (solo para quien mantiene el repo: sus
aportes se fusionan solos), `obsidian_vault`, `obsidian_registry_note` y
`obsidian_projects_folder` si usas Obsidian.

### Si el instalador falla

- **Mac/Linux:** necesita poder crear enlaces simbólicos (normal en Mac). El script `install.sh` no sirve en
  Git Bash de Windows: en Windows usa `install.ps1`.
- **Windows:** las junctions no piden permisos de administrador. Si PowerShell bloquea el script, usa el
  comando de arriba con `-ExecutionPolicy Bypass`.
- **`403` o `Repository not found` al clonar:** es la credencial; ver la siguiente sección.

## Credenciales

El repo es privado. El mantenedor te comparte **por mensaje privado** un token de GitHub *fine-grained*
limitado solo a este repo (permisos: Contents lectura/escritura, Pull requests lectura/escritura, Metadata
lectura; vence a los 90 días). Reglas:

- El token **no se escribe en ningún archivo del repo ni de una skill**, ni se pega en un chat con Claude:
  vive en el gestor de credenciales del sistema (Windows Credential Manager, llavero de Mac).
- Todos usan el mismo token, así que cada quien fija su identidad en git para que los commits digan quién fue
  (el instalador ya lo hace; a mano sería `git -C ~/gui-skills config user.name "<alias>"` y
  `git -C ~/gui-skills config user.email "<alias>@gui-skills.local"`; no uses tu correo real: queda en el historial).
- Si el token se filtra o vence, se revoca y el mantenedor manda otro (ver el final de esta sección).

### Método recomendado: credencial exclusiva para este repo

Funciona con Git Credential Manager (Windows/Mac) o el llavero del sistema, y **evita el error 403** de la
siguiente subsección. Se hace una sola vez, antes de clonar. Sustituye `<alias>` por tu alias.

1. Dile a git que guarde la credencial de este repo aparte (por ruta, no por sitio) y con tu alias como usuario.
   Usa la URL exacta, con `.git` al final:

   ```
   git config --global credential.https://github.com/guillequinterot/gui-skills.git.useHttpPath true
   git config --global credential.https://github.com/guillequinterot/gui-skills.git.username <alias>
   ```

2. Guarda el token sin que se vea en pantalla ni quede en el historial de la terminal.

   Windows (PowerShell):

   ```powershell
   $t = Read-Host 'Pega el token (no se muestra)' -AsSecureString
   $plain = [System.Net.NetworkCredential]::new('', $t).Password
   "protocol=https`nhost=github.com`npath=guillequinterot/gui-skills.git`nusername=<alias>`npassword=$plain`n" | git credential approve
   Remove-Variable plain, t
   ```

   Mac / Linux:

   ```bash
   read -rs -p 'Pega el token (no se muestra): ' T; echo
   printf 'protocol=https\nhost=github.com\npath=guillequinterot/gui-skills.git\nusername=<alias>\npassword=%s\n\n' "$T" | git credential approve
   unset T
   ```

3. Comprueba sin clonar: `git ls-remote https://github.com/guillequinterot/gui-skills.git` debe listar ramas.
   Si es así, ya puedes seguir con el paso 3 de la instalación.

### Alternativa: GitHub CLI

Copia el token del mensaje y, sin pegarlo en pantalla:

```powershell
# Windows
Get-Clipboard | gh auth login --hostname github.com --with-token; gh auth setup-git
```

```bash
# Mac
pbpaste | gh auth login --hostname github.com --with-token && gh auth setup-git
```

Luego copia otra cosa para borrar el token del portapapeles. Úsala solo si ya tienes `gh` y no te importa que
ese token pase a ser la cuenta activa de `gh` para github.com (si ya tenías otra, vuelve a ella con
`gh auth switch`). Si Git Credential Manager tiene otra cuenta guardada, `gh auth setup-git` puede no bastar y
darte el 403 de abajo: en ese caso usa el método recomendado.

### El error 403 al clonar o actualizar

Síntoma: `remote: Permission to guillequinterot/gui-skills.git denied to <otra-cuenta>` y
`The requested URL returned error: 403` (o `Repository not found`), aunque el token sea correcto.

Causa: Git Credential Manager guarda **una credencial por sitio** (`github.com`). Si ya tiene guardada otra
cuenta tuya de GitHub, la envía también a este repo, y esa cuenta no tiene acceso. El token nuevo ni siquiera se usa.

Arreglo: el método recomendado de arriba (los dos `git config` hacen que la credencial de este repo se guarde
y se busque aparte, sin tocar la de tus otros repos). No hace falta borrar la otra cuenta. Para ver qué se manda:
`GIT_TRACE=1 GIT_CURL_VERBOSE=1 git ls-remote https://github.com/guillequinterot/gui-skills.git`
(no compartas esa salida: contiene encabezados de autenticación).

### Cuando el token vence (cada 90 días) o se renueva

```
printf 'protocol=https\nhost=github.com\npath=guillequinterot/gui-skills.git\nusername=<alias>\n\n' | git credential reject
```

(en PowerShell: `"protocol=https`nhost=github.com`npath=guillequinterot/gui-skills.git`nusername=<alias>`n" | git credential reject`)
y repite el paso 2 con el token nuevo. El aviso de actualización dice `SIN_CREDENCIAL` cuando GitHub rechaza la credencial.

## Cómo se mantienen al día

- **Al abrir cada sesión**, un hook `SessionStart` corre `python <repo>/tools/check_update.py --hook --pull`:
  compara tu clon con GitHub (en cada sesión, con 8 segundos de espera como tope) y, si estás atrasado y el clon
  está limpio, **se actualiza solo** (`git pull --ff-only`). Deja una línea que Claude lee. Nunca rompe la
  sesión: sin red, sigue con tu copia local.
- **Paso 0 en cada skill, cada vez que se usa:** Claude corre `check_update.py --quiet --pull`, vuelve a leer el
  `SKILL.md` si hubo cambios (`ACTUALIZADA n`) y lee el `HANDSHAKE.md` y el registro de trabajos.
- Resultados posibles de `check_update.py`: `AL_DIA`, `ACTUALIZADA <n>` (se descargaron n cambios), `ATRASADA <n>`
  (hay n cambios nuevos pero no se pudieron bajar solos, o no se pidió `--pull`), `CAMBIOS_LOCALES` (tu clon tiene
  cambios sin subir: nunca hace pull), `SIN_RED`, `SIN_CREDENCIAL`. Solo se actualiza un clon limpio, en `main`
  y sin commits sin subir. Si hay ramas `aporte/*` sin publicar, agrega un `AVISO` (se resuelve con
  `publish_job.py --reintentar`).
- Para actualizar a mano: `git -C ~/gui-skills pull --ff-only`. Como las skills son enlaces al clon, no hay que copiar nada.

## Cómo se publica lo aprendido (automático)

Al **terminar un trabajo que el usuario aprueba**, Claude hace sin pedir permiso el "Paso final" del protocolo:
registra la entrada con `log_job.py` en el HANDOFF de cada skill que intervino, actualiza el HANDSHAKE si hizo
falta y corre `python <repo>/tools/publish_job.py --tema <caso-o-tema>`, que crea la rama
`aporte/<alias>/<fecha>-<tema>`, hace commit (pasa el escáner de privacidad), la sube y abre un Pull Request hacia
`main`. Los amigos obtienen un PR que revisa el mantenedor. Si eres el mantenedor (`"mantenedor": true` en `~/.gui-skills/config.json`), tu aporte se integra solo: el PR se fusiona en el acto (`PUBLICADO <url>`); `--no-merge` lo evita. Si no hay red, la rama queda guardada en tu clon (`PENDIENTE`) y el Paso 0 te avisa hasta que se suba
con `publish_job.py --reintentar`. El PR se abre con `gh` si está autenticado, si no con la API de GitHub usando el
token de tu credencial de git (nunca se imprime ni se guarda) y, si tampoco, te da el enlace para abrirlo a mano.

## Herramientas (`tools/`)

| Herramienta | Qué hace |
|---|---|
| `check_update.py` | Compara tu clon con GitHub y lo actualiza si es seguro (`--quiet`, `--pull`, `--hook`, `--repo`). |
| `privacy_scan.py` | Escáner de privacidad; lo usan el hook `pre-commit`, GitHub Actions y `log_job.py`. |
| `log_job.py` | Agrega al HANDOFF de una skill la entrada de un trabajo terminado, ya revisada por el escáner. |
| `publish_job.py` | Publica lo que dejó un trabajo: rama `aporte/...`, commit, push y Pull Request (`--tema`, `--merge`, `--reintentar`, `--dry-run`). |
| `install.ps1` / `install.sh` | Instaladores para Windows / Mac. |
| `settings_hook.py` | Agrega, actualiza o quita el hook `SessionStart` (`check_update.py --hook --pull`) en `~/.claude/settings.json` (lo usan los instaladores). |
| `build_hosted.py` | Regenera `seo-content-system-web-hosted` desde `seo-content-system`. |
| `tests/` | Pruebas de las herramientas (repo y remoto temporales, nunca el real): `python -m unittest discover -s tests`. |

## Desinstalar

1. Quita los enlaces (no borran el clon):

   ```powershell
   # Windows
   Get-ChildItem "$HOME\gui-skills\skills" -Directory | ForEach-Object {
     $l = Join-Path "$HOME\.claude\skills" $_.Name
     $i = Get-Item $l -Force -ErrorAction SilentlyContinue
     if ($i -and ($i.Attributes -band 'ReparsePoint')) { [System.IO.Directory]::Delete($l) }
   }
   ```

   ```bash
   # Mac / Linux
   for d in ~/gui-skills/skills/*/; do n=$(basename "$d"); [ -L ~/.claude/skills/"$n" ] && rm ~/.claude/skills/"$n"; done
   ```

2. Quita el hook: `python ~/gui-skills/tools/settings_hook.py --settings ~/.claude/settings.json --remove`
   (en Windows, con la ruta completa de tu carpeta de usuario).
3. Borra de `~/.claude/CLAUDE.md` el bloque "gui-skills (skills compartidas)".
4. Si quieres recuperar lo que tenías antes, copia de vuelta las carpetas de `~/.gui-skills/backup-<fecha>/`
   a `~/.claude/skills/`.
5. Opcional: quita las credenciales (`git credential reject`, como arriba, y las dos líneas `credential.https://github.com/...`
   de `git config --global --edit`), y borra `~/gui-skills` y `~/.gui-skills`.

## Más

- [CONTRIBUTING.md](CONTRIBUTING.md): cómo registrar un trabajo, ramas y revisión.
- [PRIVACY.md](PRIVACY.md): qué nunca se sube y cómo funciona el escáner.
- [`shared/protocolo-skill.md`](shared/protocolo-skill.md): el protocolo común de las 9 skills (Paso 0, privacidad, Paso final).
