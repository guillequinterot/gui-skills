<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella e8b1207b9830). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->
# Memoria y continuidad sin acceso al repo ni a una bóveda de Obsidian

Adaptación de `references/memory-integration.md` (versión con sistema de archivos) para el entorno alojado, donde no hay MCP de Obsidian ni acceso al clon del repo gui-skills. La memoria de largo plazo real vive en el `HANDOFF.md` y la carpeta `memoria/` de la skill (y, si el usuario la usa, en su bóveda de Obsidian). Este archivo define cómo trabajar sin acceso directo a ellas: **el usuario sube manualmente las notas relevantes cuando hacen falta**, sin sincronización automática.

## Principio

Esta sesión (Claude.ai Project o ChatGPT Custom GPT) no tiene memoria persistente propia entre conversaciones distintas, salvo lo que la propia plataforma retenga como "memoria" nativa (si esa función está activa) y lo que el usuario vuelva a aportar. No simular que se consultó una memoria que no fue subida a esta conversación.

## Paso 0 en este entorno

Antes de producir cualquier salida relevante para un proyecto recurrente:

1. Preguntar si el usuario tiene una nota del proyecto, decisiones previas o fuentes ya evaluadas.
2. Si las sube (como `.md`, texto pegado, o PDF), leerlas y tratarlas como la versión vigente del conocimiento — gana sobre el conocimiento entrenado del modelo, salvo que la instrucción presente, el brief activo o una fuente primaria digan otra cosa.
3. Si no las aporta, decirlo explícitamente: la salida queda marcada como *no contrastada con memoria de largo plazo*.

## Qué pedir subir, y cuándo

No pedir "toda la memoria" — pedir solo lo pertinente al tema concreto:

| Tarea | Qué pedir |
|---|---|
| Retomar un proyecto existente | Nota del proyecto (objetivo, brief, decisiones, entregables previos) o sus entradas del registro de trabajos del `HANDOFF.md` |
| Verificar una regla o dato SEO | Registro de fuentes / decisiones relacionadas, si las tiene documentadas |
| Evitar repetir investigación de keywords | Matriz de keywords o mapa temático previos |
| Escribir en la voz de una marca ya definida | Nota de voz de marca / guía de estilo |

## Registrar un aprendizaje sin script

No existe `capture_learning.py` en este entorno. Cuando surja una observación reutilizable durante la sesión:

1. Redactarla en un bloque de texto con esta estructura (igual al frontmatter que usa la versión con sistema de archivos, en formato legible):

```text
Título:
Estado: candidate
Contexto:
Evidencia:
Resultado:
Límites:
Fecha:
Próxima revisión sugerida:
```

2. Entregar ese bloque al usuario al final de la sesión y pedirle explícitamente que lo guarde en su sistema de memoria (el `HANDOFF.md` de la skill en el repo, Obsidian u otro) si quiere conservarlo — esta sesión no lo persiste por sí sola.
3. Nunca tratarlo como regla validada solo por haberlo observado una vez en esta conversación.
4. Referirse a los clientes con un código de caso (`caso-<tipo>-<NN>`), no con su nombre, si el bloque va a acabar en un repo compartido.

## Puente opcional vía Google Sheets/Drive

Si Drive y Sheets están conectados en la plataforma, es válido usarlos como memoria intermedia cuando el usuario lo prefiera a subir archivos sueltos cada vez:

- Un Sheet o documento de Drive con el resumen del proyecto, decisiones y matriz de keywords, actualizado por el usuario o por un flujo local (ver `07-medicion-y-decisiones.md` y `09-keyword-research-hosted.md`).
- Esta sesión lee ese documento al inicio de cada tarea relevante en vez de partir de cero.
- Esto no reemplaza la memoria canónica de la skill (repo u Obsidian); es un puente práctico para este entorno.

## Qué no hacer

- No afirmar haber "consultado la memoria" cuando nada fue subido a la conversación.
- No inventar decisiones o aprendizajes previos que no fueron aportados.
- No guardar credenciales, tokens o datos personales en ningún bloque de "aprendizaje" que se le entregue al usuario.
- No asumir que la memoria nativa de la plataforma (si existe) equivale a la memoria de la skill — son sistemas distintos con distinta cobertura y confiabilidad.
