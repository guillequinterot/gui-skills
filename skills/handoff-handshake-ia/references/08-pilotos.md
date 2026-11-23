# Pilotos de la v0.1.1 y re-prueba de la v0.2

[medido] Correctas sobre ocho preguntas por caso:

| Caso | Tipo | Viejo | Nuevo |
|---|---|---:|---:|
| caso-handoff-01 | Blog | 5 | 7 |
| caso-handoff-02 | Figma | 7 | 5 |
| caso-handoff-03 | Post | 5 | 7 |
| caso-handoff-04 | Video | 7 | 5 |
| caso-handoff-05 | SEO | 6 | 6 |
| **Total / 40** | | **30** | **30** |

[visto] La v0.1.1 no se aprobó como mejora general. La v0.2 se re-probó en dos casos (cuadro siguiente); en los otros tres no se re-probó.

[medido] Re-prueba de la v0.2 (migración por una IA, lectura en frío por otra, puntuación a ciegas):

| Caso | Viejo | Nuevo v0.1.1 | Nuevo v0.2 | Líneas leídas v0.2 (viejo) |
|---|---:|---:|---:|---|
| caso-handoff-02 | 7 | 5 | 7 | ≈ 188 (≈ 249) |
| caso-handoff-04 | 7 | 5 | 6 | ≈ 157 (≈ 447) |

[visto] En 02 la v0.2 corrigió los dos parciales (qué manda y último trabajo real). En 04 la pregunta fallada fue la contradicción del total: el proyecto traía una regla que decidía y el migrador escribió «pendiente»; el paso 4 de la migración se ajustó y **no se ha re-probado**. [inferido] 6 contra 7 con una lectura por celda es compatible con un empate.

[medido] Re-prueba de la v0.2 en 01, 03 y 05 (migró otra IA, lector en frío, puntuación ciega del par en una sesión):

| Caso | Viejo | Nuevo v0.2 |
|---|---:|---:|
| caso-handoff-01 | 5 | 6 |
| caso-handoff-03 | 7 | 5 |
| caso-handoff-05 | 6 | 6 |

[medido] **Con los cinco casos re-probados: v0.2 = 30, formato anterior = 32** (30 si el viejo de 03 se puntúa como en la primera ronda). [medido] El viejo cayó otra vez en la trampa de 01 («W48 sin publicar»); en 03 la v0.2 perdió el objetivo «repetible, seis redes, material real» y la rutina de las 21:30 que la v0.1.1 sí conservó.

[medido] **Ruido de puntuación:** el mismo texto del lector viejo de 03 sacó 5 correctas y 2 parciales con un evaluador y 7 correctas con otro. Diferencias de 1 o 2 puntos entre formatos no son distinguibles del ruido. [visto] Lo repetido y cualitativo: con un HANDOFF de unas 1.200 líneas (caso 01) el formato anterior no cabe en una lectura y la IA toma por vigente un estado desactualizado; con el nuevo no. Es un solo caso. [inferido] En proyectos de unas 136 a 500 líneas no hay ventaja medible; la calidad de la migración depende de la IA que migra.

Estado: **validación parcial; sin ventaja demostrada fuera de un HANDOFF muy grande; umbral de uso provisional (~1.000 líneas)**.

## Conclusiones del informe
1. [medido] Con la v0.1.1 el nuevo ganó en 01 y 03 y perdió en 02 y 04; con la v0.2 en los cinco casos no hubo ventaja demostrada (ver el cuadro de la re-prueba).
2. [visto] Solo el caso 01 (HANDOFF de unas 1.200 líneas) muestra una ventaja repetida y cualitativa; el nuevo no ahorró lectura de forma consistente en los demás.
3. [medido] En tres de cinco casos (02, 04 y 05), la firma de migración tapó el último trabajo real. Un resultado hipotético sin ese defecto no es una medición.
4. [visto] En 02 se enumeró una contradicción sin aclarar qué manda; en 04 faltó una frase citable sobre el estado.
5. [medido] No hubo respuestas inventadas en ninguno de los dos formatos; eso no demuestra una reducción de alucinaciones.

## Protocolo de medición
**Puntúa cada par viejo/nuevo en la misma sesión del evaluador** y, si puedes, con dos evaluadores: el mismo texto varió 2 puntos entre sesiones. Una IA prepara ocho preguntas y una clave con evidencia; otra IA migra una copia. Una IA sin historia lee en frío el formato viejo y, en otra sesión, el nuevo, usando la misma cuenta para ambos. Un evaluador independiente puntúa a ciegas contra la clave con etiquetas CORRECTA, PARCIAL, INCORRECTA, NO CONSTA-OK, NO CONSTA-FALSO e INVENTADA. Hay n = 1 lectura por celda: son indicios, no estadística. Registra posibles contaminaciones; en 04 el lector viejo consultó previamente memoria personal, aunque no usó lo encontrado.

Registra archivos y rangos efectivamente leídos, líneas físicas incluyendo vacías y comentarios, y bytes de los rangos leídos; anota búsquedas, salidas truncadas, relecturas y archivos ausentes. Para lecturas parciales cuenta solo rangos realmente recibidos, distingue lectura real del paquete recomendado y no extrapoles contenido no leído. Si hay un archivo combinado cuéntalo una sola vez. Presenta límites y métricas de ambos formatos por separado.

En un piloto de solo lectura respeta el alcance: no actualices la skill ni publiques, conserva las fuentes y trabaja solo en la copia o salida autorizada. Si ni siquiera se permite escribir una copia, documenta la limitación en el lugar autorizado y no afirmes una migración completada. La re-prueba de 02 y 04 se hizo (cuadro anterior). El criterio fijado, que el nuevo igualara o superara al viejo en ambos, **no se cumplió por una respuesta en 04**; se publicó como validación parcial por decisión del orquestador, sujeta a revisión del mantenedor.

Límites de la medición: [medido] las mejoras de la v0.2 se calculan contra la v0.1.1 y contra el formato anterior, con una lectura por celda; [visto] los cambios de la v0.2 se diseñaron viendo fallar los casos 02 y 04, que son los mismos en que se re-probó, así que esa re-prueba no es independiente de su diseño; [no sé] si mejora en 01, 03 y 05 o en proyectos nuevos.
