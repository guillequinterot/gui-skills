# Arranque y cierre
**Arrancar un proyecto nuevo:** crea `AGENTS.md`, `HANDSHAKE.md` y `HANDOFF.md` copiando las plantillas de `templates/` (más `historial/` con su índice), pregunta los guardrails con [guardrails](03-guardrails-por-proyecto.md), rellena Objetivo, Estado, Fecha, Firma y Próximo paso y ejecuta `python <ruta de la skill>/scripts/verificar.py PROYECTO`. Un `OK` solo confirma el formato, no que el contenido sea cierto. Código de salida 1 = hay un BLOQUEA: corrígelo antes de seguir.

1. Lee AGENTS.md, HANDSHAKE.md y la ficha de la tarea; consulta únicamente el plan y los archivos pertinentes. No leas todo el historial ni handoffs antiguos por defecto.
2. Antes de actuar, comunica el readback de cinco líneas y distingue lo que NO CONSTA. Si una ausencia bloquea, pregunta antes de continuar con esa parte.
3. En la frontera de tarea, actualiza en el mismo paso el estado vivo con fecha, firma y próximo paso. Pasa el detalle histórico al archivo correspondiente.
4. Completa la ficha con rutas de evidencia, pendientes y destinatario; solicita acuse y ejecuta el verificador. Anota fallos y límites.

Ejemplo de readback:
Objetivo: preparar una entrega de prueba.
Estado: borrador en curso, según HANDSHAKE.
Próximo paso: revisar la ficha.
NO CONSTA: fecha de entrega.
Guardrails: no publicar sin autorización.

Errores típicos: inventar datos, leer todos los archivos por defecto o cerrar sin actualizar el estado vivo.
