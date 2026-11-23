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

[visto] En 02 la v0.2 corrigió los dos parciales (qué manda y último trabajo real). En 04 la pregunta fallada fue la contradicción del total: el proyecto traía una regla que decidía y el migrador escribió «pendiente»; el paso 4 de la migración se ajustó y **no se ha re-probado**. [inferido] 6 contra 7 con una lectura por celda es compatible con un empate. Estado: **validación parcial; umbral de uso provisional**.

## Conclusiones del informe
1. [medido] El nuevo ganó en los dos casos grandes o caóticos (01 y 03).
2. [medido] El viejo ganó en los casos cortos y limpios (02 y 04); el nuevo no ahorró lectura de forma consistente.
3. [medido] En tres de cinco casos (02, 04 y 05), la firma de migración tapó el último trabajo real. Un resultado hipotético sin ese defecto no es una medición.
4. [visto] En 02 se enumeró una contradicción sin aclarar qué manda; en 04 faltó una frase citable sobre el estado.
5. [medido] No hubo respuestas inventadas en ninguno de los dos formatos; eso no demuestra una reducción de alucinaciones.

## Protocolo de medición
Una IA prepara ocho preguntas y una clave con evidencia; otra IA migra una copia. Una IA sin historia lee en frío el formato viejo y, en otra sesión, el nuevo, usando la misma cuenta para ambos. Un evaluador independiente puntúa a ciegas contra la clave con etiquetas CORRECTA, PARCIAL, INCORRECTA, NO CONSTA-OK, NO CONSTA-FALSO e INVENTADA. Hay n = 1 lectura por celda: son indicios, no estadística. Registra posibles contaminaciones; en 04 el lector viejo consultó previamente memoria personal, aunque no usó lo encontrado.

Registra archivos y rangos efectivamente leídos, líneas físicas incluyendo vacías y comentarios, y bytes de los rangos leídos; anota búsquedas, salidas truncadas, relecturas y archivos ausentes. Para lecturas parciales cuenta solo rangos realmente recibidos, distingue lectura real del paquete recomendado y no extrapoles contenido no leído. Si hay un archivo combinado cuéntalo una sola vez. Presenta límites y métricas de ambos formatos por separado.

En un piloto de solo lectura respeta el alcance: no actualices la skill ni publiques, conserva las fuentes y trabaja solo en la copia o salida autorizada. Si ni siquiera se permite escribir una copia, documenta la limitación en el lugar autorizado y no afirmes una migración completada. La re-prueba de 02 y 04 se hizo (cuadro anterior). El criterio fijado, que el nuevo igualara o superara al viejo en ambos, **no se cumplió por una respuesta en 04**; se publicó como validación parcial por decisión del orquestador, sujeta a revisión del mantenedor.

Límites de la medición: [medido] las mejoras de la v0.2 se calculan contra la v0.1.1 y contra el formato anterior, con una lectura por celda; [visto] los cambios de la v0.2 se diseñaron viendo fallar los casos 02 y 04, que son los mismos en que se re-probó, así que esa re-prueba no es independiente de su diseño; [no sé] si mejora en 01, 03 y 05 o en proyectos nuevos.
