# AGENTS.md — instrucciones para IAs que trabajan con este repo (gui-skills)

> Si eres Codex, Grokbot, Gemini, Cursor, Claude Code u otra IA: lee esto primero. Detalle largo: sección «Instalar y actualizar con otra IA» de `README.md`.

## Qué es
Repositorio privado con las skills de Guille (carpetas `skills/<nombre>/` con `SKILL.md`). Hay una sola copia de cada skill: este repo.

## Instalarlas en tu carpeta de skills
1. Necesitas `git` y Python 3.9+. Pide a la persona el token del repo (archivo `github-token.txt` de la carpeta `Github-access-token-skill`) y guárdalo SOLO en el gestor de credenciales (README, sección Credenciales). **Nunca lo imprimas, lo escribas en un archivo ni lo pegues en un chat.**
2. Clona: `git clone https://github.com/guillequinterot/gui-skills.git ~/gui-skills`
3. Instala (elige una):
   - Codex: `python ~/gui-skills/tools/install_agente.py --agente codex`
   - Otra IA: `python ~/gui-skills/tools/install_agente.py --destino <carpeta de skills de esa IA>`
   - Claude Code: `tools/install.ps1` (Windows) o `bash tools/install.sh` (Mac/Linux)
   - Si no admite enlaces: añade `--copiar`. Para solo mirar: `--dry-run`.
4. Verifica: el mismo comando con `--check` (0 = bien, 1 = falta algo o está desactualizado).

## Mantenerlas al día
Antes de usar CUALQUIER skill de este repo (cada vez, no solo al empezar): `python ~/gui-skills/tools/check_update.py --quiet --pull`.
`AL_DIA` → sigue · `ACTUALIZADA n` → relee el `SKILL.md` · `CAMBIOS_LOCALES` → no actualices y avisa · `SIN_RED`/`SIN_CREDENCIAL` → sigue con la copia local y dilo.
Luego lee `HANDSHAKE.md` y las últimas entradas del «Registro de trabajos» de `HANDOFF.md` de la skill.

## Reglas
- Privacidad: clientes solo con código `caso-<tipo>-<NN>`; nada de nombres, dominios, correos, rutas personales ni credenciales.
- No edites las skills dentro de tu carpeta de skills (son enlaces al repo): los cambios van en una rama `aporte/<alias>/<tema>` con Pull Request (`tools/log_job.py` y `tools/publish_job.py`).
- Al terminar un trabajo aprobado: registra con `log_job.py` y publica con `publish_job.py` (ver `shared/protocolo-skill.md`).
- Lo que no verificaste, dilo; no escribas «verificado» sin haberlo comprobado.
