# Reparto y ejecutores
1. Descompón el trabajo en encargos verificables; identifica dependencias y rutas que cada uno puede tocar. Evita solapamientos y usa sellos (un sello es una marca en el encargo con ejecutor, estado ASIGNADO, EN CURSO o TERMINADO, fecha y hora; solo quien tiene el sello trabaja ese encargo).
2. Completa la tabla y justifica el reparto según disponibilidad y restricciones de la sesión. Avisa si todos los encargos recaen en un solo ejecutor.
3. Reparto base aprobado: Claude Code para trabajo general y orquestación; Codex para código e imágenes/Magnific; Antigravity para investigación; OpenCode para tareas pequeñas y verificables con QA siempre.
4. Para OpenCode, entrega instrucciones cortas, numeradas y explícitas; fija un modelo `opencode/*-free`, nunca `openrouter/free`. Exige NO CONSTA ante ausencias y comprueba existencia y contenido del entregable, no solo el código de salida.

| Encargo | Ejecutor | Motivo | Archivos que toca |
|---|---|---|---|
| Crear comprobación | Codex | Código | `scripts/` |
| Revisar fuentes | Antigravity | Investigación | `referencias/` |

Evidencia de pruebas propias (una tarea acotada y verificable por script, una corrida por celda): con `opencode/deepseek-v4.1-flash-free` y `opencode/mimo-v2.6-flash-free` fijos, 5 de 6 corridas perfectas y una con 12/13; con el enrutador `openrouter/free` y con `gemma-4-31b` hubo fallos y vencimientos de tiempo (900 s sin entregar). Por eso: modelo fijo, tope de tiempo por encargo (un vencimiento es un fallo, no una espera) y comprobar el entregable. No prueba que OpenCode no invente en tareas abiertas ni que un HANDOFF estructurado le ayude más que uno informal [no sé].

Errores típicos: asignar rutas solapadas, omitir QA de OpenCode o confundir éxito del proceso con entrega existente.
