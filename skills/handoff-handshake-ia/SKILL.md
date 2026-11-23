---
name: handoff-handshake-ia
description: Usar para traspasos entre IA o sesiones, arrancar, retomar y cerrar proyectos o tareas, repartir encargos, partir un HANDOFF extenso y preguntar guardrails.
---
# Handoff y handshake entre IA

**Estado: v0.2, validación parcial** (cinco casos, una lectura por celda; sin ventaja demostrada salvo con un HANDOFF de unas 1.200 líneas; sin evidencia de que reduzca alucinaciones; umbral de uso provisional). Ver [pilotos](references/08-pilotos.md).

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
   (1) `python <repo>/tools/log_job.py --skill handoff-handshake-ia ...` por cada skill que intervino (qué se hizo, qué
   salió bien, qué salió mal, incidencias); (2) actualiza `HANDSHAKE.md` si cambió el estado vivo;
   (3) publica con `python <repo>/tools/publish_job.py --tema <caso-o-tema>` (rama + push + PR; si eres el
   mantenedor, tu aporte se integra solo); (4) dile al usuario el resultado (`PR_CREADO <url>` / `PUBLICADO <url>` /
   `PENDIENTE` / `BLOQUEADO`). Obsidian es opcional: si el usuario lo tiene, registra también allí.

`<repo>` = `repo_path` de `~/.gui-skills/config.json`, o dos carpetas arriba de esta skill.

## Modos
- **arrancar:** crear estructura y preguntar guardrails; sigue [arranque y cierre](references/02-arranque-y-cierre.md) y [guardrails](references/03-guardrails-por-proyecto.md).
- **retomar:** leer lo mínimo y hacer readback de cinco líneas; [procedimiento](references/02-arranque-y-cierre.md).
- **traspasar:** completar [ficha](templates/HANDOFF-ficha.md) y pedir acuse; [modelo](references/01-modelo.md).
- **cerrar:** actualizar estado en la frontera de tarea y archivar detalle; [cierre](references/02-arranque-y-cierre.md).
- **repartir:** tabla de encargos y ejecutores; [reparto](references/04-reparto-y-ejecutores.md).
- **migrar:** solo al retomar y según el umbral provisional; en copia y sin borrar; [migración](references/06-migracion.md).
- **verificar:** ejecutar `python scripts/verificar.py PROYECTO` desde esta skill; opciones `--tope N`, `--rutas`, `--json`, `--combinado ARCHIVO`. Revisar avisos manualmente.

QA: [dos pasadas](references/05-qa-dos-pasadas.md). Evidencia y límites: [fuentes](references/07-evidencia-y-limites.md). Resultados y re-prueba: [pilotos](references/08-pilotos.md).
