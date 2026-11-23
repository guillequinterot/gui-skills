# Modelo
1. Conserva en AGENTS.md las reglas y guardrails acordados para este proyecto.
2. Usa HANDSHAKE.md como única fuente documental del estado vivo: objetivo, estado fechado y firmado, próximo paso, cola, decisiones, límites e índice. El tope es 150 líneas por defecto; cambia el marcador `<!-- handshake-tope: N -->` o usa `--tope N`.
3. Usa HANDOFF.md como ficha breve de la tarea y su evidencia; archiva decisiones anteriores en `historial/`.
4. Ante un conflicto, contrasta con la realidad comprobable y registra la evidencia. Si no puedes, escribe NO CONSTA y pregunta.

Ejemplo mínimo: HANDSHAKE dice «Estado: en curso» y la ficha enlaza el resultado parcial sin duplicar el estado.

Ejemplo de ficha ficticia:
```text
De: agente A
Para: agente B
Objetivo: preparar una entrega de prueba
Hecho y rutas de evidencia: borrador en entregables/borrador.md
Último trabajo real: agente A, 2026-01-01, borrador inicial
Falta: revisar el borrador
No consta: fecha de entrega
Skills a cargar: NO CONSTA
QA cumplimiento: pendiente
QA calidad: pendiente
Acuse del receptor: pendiente
```

Ejemplo de historial ficticio:
| Fecha | Quién | Decisión | Evidencia |
|---|---|---|---|
| 2026-01-01 | Agente A | Trabajar en copia | acta inicial |
| 2026-01-02 | Agente B | Separar la ficha | borrador de ficha |
| 2026-01-03 | Agente A | Pedir QA | registro de entrega |

Errores típicos: mantener dos estados vivos, borrar antecedentes o decidir una contradicción sin evidencia.
