# Aprendizaje y memoria de diseño

## Contenido

1. Capas
2. Promoción de aprendizajes
3. Registro
4. Resolución de conflictos

## 1. Capas

| Capa | Ejemplo | Persistencia |
|---|---|---|
| Fundamento | WCAG 4.5:1 para texto normal AA | Hasta cambio de estándar |
| Preferencia general | Favorecer imágenes base sin texto para diseñar después | Reutilizable, con excepciones |
| Marca | caso-marca-belleza-01 usa lujo editorial cálido | Solo esa marca |
| Proyecto | Esta campaña usa Burgundy | Solo campaña indicada |
| Experimento | Probar composición cenital | No promover sin validación |

## 2. Promoción de aprendizajes

Registrar como **aprobado** si ocurre una de estas condiciones:

- el usuario dice explícitamente “recuerda”, “siempre para esta marca” o equivalente;
- la misma corrección aparece de forma consistente en varios trabajos;
- una guía de marca o documento fuente lo establece;
- el usuario confirma una propuesta de regla reutilizable.

Registrar como **candidato** una tendencia aún no confirmada. No guardar como preferencia una orden puntual, una limitación de herramienta o una variación experimental.

## 3. Registro

Usar `scripts/update_design_memory.py` para añadir registros JSONL cuando exista autorización para persistirlos. Incluir:

- fecha;
- alcance: `global`, `brand` o `project`;
- contexto/nombre;
- aprendizaje;
- evidencia o feedback;
- estado: `candidate`, `approved` o `deprecated`;
- origen.

No guardar datos sensibles, rostros, archivos privados ni credenciales en la memoria textual.

## 4. Resolución de conflictos

Aplicar esta precedencia:

1. instrucción explícita actual;
2. guía o brief actual del proyecto;
3. memoria de marca aprobada;
4. preferencia general aprobada;
5. heurística profesional;
6. estilo propuesto por la IA.

Si una nueva decisión contradice una regla anterior, no borrar silenciosamente. Marcar la anterior como obsoleta o limitar su alcance, y registrar la razón.
## 5. Base de conocimiento y Obsidian (opcional)

La memoria de diseño de la skill vive en su base de conocimiento `<repo>/skills/direct-visual-design/` (repo gui-skills). Obsidian, si el usuario lo tiene configurado (`obsidian_vault` en `~/.gui-skills/config.json`), es una capa extra de proyectos y decisiones; sin Obsidian, esta sección se aplica solo a las rutas del repo.

- Proyecto: registrar decisiones y pendientes en la nota del proyecto (carpeta `obsidian_projects_folder` del vault, si hay) y, si son de diseño/marca, en `proyectos/<caso-código>.md`.
- Marca: registrar reglas confirmadas en `proyectos/<caso-código>.md`. Si la marca conserva una nota extra en el vault del usuario, es de solo lectura desde la skill hasta migrarla.
- Preferencia general aprobada: `memoria/preferencias-generales-aprobadas.md`.
- Candidato: `memoria/inbox-aprendizajes.md`.
- Decisión formal: registrar en la carpeta de decisiones del vault (si hay) y anotarla en el HANDOFF (sección 3, Decisiones vigentes).
- Trabajo terminado: entrada en el Registro de trabajos del `HANDOFF.md` (`tools/log_job.py`).
- Registro JSONL opcional con `scripts/update_design_memory.py --file "<carpeta-del-proyecto>/design-memory.jsonl"`.

Actualizar la skill solo cuando una regla sea estable, aprobada y reusable. No convertir un comentario aislado o una preferencia de un proyecto en regla global.
