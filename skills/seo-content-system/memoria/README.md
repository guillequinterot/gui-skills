# Memoria de seo-content-system

Memoria de largo plazo de la skill **dentro del repo** (no hace falta Obsidian). Los scripts de `scripts/`
escriben aquí cuando no hay bóveda de Obsidian configurada.

| Carpeta | Qué va | Lo escribe |
|---|---|---|
| `aprendizaje/inbox/` | aprendizajes candidatos, sin validar | `scripts/capture_learning.py` |
| `decisiones/` | cambios aprobados, con evidencia y fecha de revisión (plantilla: `assets/templates/decision-record.md`) | a mano, tras repetición o aprobación del mantenedor |
| `novedades/` | informes fechados de cambios en las fuentes oficiales | `scripts/research_update.py` |
| `fuentes/` | fichas de fuentes evaluadas (plantilla: `assets/templates/source-record.md`) | a mano |

Reglas: los casos se nombran solo con código `caso-<tipo>-<NN>` (nunca cliente, marca, dominio, correo ni
ruta personal); un aprendizaje es `candidate` hasta que se repite o el mantenedor lo aprueba; el registro de
casos terminados va en `HANDOFF.md` §4 (con `tools/log_job.py`). Detalle: `references/memory-integration.md`.
