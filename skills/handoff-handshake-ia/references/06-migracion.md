# Migración en copia

**Umbral provisional, 5 casos, sin validar:** al retomar, migra si HANDOFF + HANDSHAKE superan aproximadamente 400 líneas, si hay varios archivos de estado, contradicciones o estados desactualizados conocidos. Si el proyecto es corto y limpio, no migres: añade solo `AGENTS.md` y los campos `Último trabajo real` y `Estado` en una frase. Es una hipótesis, no un resultado demostrado: ver [pilotos](08-pilotos.md).

1. Si corresponde migrar, copia los documentos a un espacio de trabajo; conserva los originales intactos. Registra rutas y lectura real antes del cambio.
2. Identifica el estado vivo con evidencia. Escribe `Estado:` como una sola frase citable que diga qué se hace hoy y en qué punto; si no consta, dilo. Extrae objetivo, fecha, firma, próximo paso, cola, decisiones y guardrails.
3. Copia `Último trabajo real:` de la entrada más reciente del original que no sea migración: quién, fecha y ruta o línea de evidencia. Si falta algún dato, indica NO CONSTA. La firma corresponde a quien escribe la versión del estado; registra al migrador y la fecha aparte en `Migrado por:` de la ficha.
4. Por cada contradicción escribe fuentes, `Qué manda` y evidencia. **Antes de escribir «pendiente», busca en el propio proyecto una regla que decida** (por ejemplo «el total es la suma de las duraciones»); si existe, aplícala y cítala con su línea. Solo si no existe, escribe `pendiente de confirmar`. No decidas a ciegas. [visto] En la re-prueba de video, un migrador dejó «pendiente» aunque el proyecto traía la regla y el lector siguió esa nota; el ajuste no se ha re-probado.
5. Crea una ficha para la tarea con destinatario, evidencia, pendientes y QA. En la copia archiva el detalle histórico y enlázalo; no elimines originales.
6. Ejecuta `python scripts/verificar.py PROYECTO`, revisa avisos, coteja conservación y registra resultados. Para un archivo combinado usa `--combinado ARCHIVO`. Compara lectura real antes y después como indica [pilotos](08-pilotos.md).
7. Presenta la copia, contradicciones y comparación a la persona responsable antes de cambiar referencias operativas.

Si el encargo impone solo lectura o prohíbe actualizar o publicar, prevalece ese límite: no ejecutes pull, actualización ni publicación; usa la copia local permitida y registra la limitación. No alteres originales ni otros proyectos.
