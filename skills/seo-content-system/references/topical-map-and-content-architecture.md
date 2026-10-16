---
tags:
  - seo
---

# Mapa temático: arquitectura de contenido a nivel de sitio

## Índice

- Principio
- Estado de la evidencia
- Los tres niveles
- Definir el alcance antes de listar temas
- Dónde investigar subtemas
- El filtro de cuatro dimensiones
- Cómo armar el mapa paso a paso
- Priorización de ejecución
- Errores frecuentes
- Lista de revisión

## Principio

El mapa temático es la capa de planificación **por encima** del brief de una página individual (ver [content-brief-and-architecture.md](content-brief-and-architecture.md)) y del clustering de keywords (ver [keyword-research-and-query-mapping.md](keyword-research-and-query-mapping.md)): responde qué temas cubre el sitio completo, cómo se relacionan entre sí y en qué orden se abordan, antes de que exista un calendario editorial o un brief puntual. Sin este documento, el clustering de keywords tiene insumos pero no un techo que le dé forma de conjunto.

## Estado de la evidencia

Framework editorial de un consultor SEO (Julián Durango, +10 años en SEO para ecommerce), consistente con la práctica extendida de "topical authority" / "topical maps" en la industria SEO. No es un estudio con datos controlados — es metodología de consultoría aplicada, presentada como tal.

## Los tres niveles

1. **Tema principal (pilar).** El paraguas que define el sitio o una sección relevante. Debe ser amplio para generar múltiples subtemas, pero específico para tener sentido con el negocio ("posicionamiento web para empresas", no simplemente "SEO").
2. **Temas de apoyo (clusters).** Las grandes categorías que cubren distintas facetas del tema principal. Cada uno se convierte en una página pilar que agrupa artículos relacionados.
3. **Subtemas (artículos individuales).** Piezas específicas que profundizan un aspecto concreto dentro de un cluster, cada una apuntando a una keyword o grupo de keywords con intención clara.

Referencia de tamaño orientativa (no regla rígida): 3 a 7 temas de apoyo, cada uno con 5 a 20 subtemas. Empezar con 30-50 subtemas bien filtrados es más manejable que partir con 300.

## Definir el alcance antes de listar temas

El error más común: listar subtemas sin haber fijado con precisión el tema central y sus límites. Preguntas para fijar el alcance:

- ¿Cuál es el enfoque del sitio, lo más específico posible?
- ¿En qué se quiere ser reconocido como experto?
- ¿Qué productos o servicios limitan el alcance temático?
- ¿Qué temas, aunque relacionados, **no** debería cubrir el sitio? (tan valioso como definir lo que sí)

Cada tema candidato pasa dos filtros antes de entrar al mapa:

- **Relevancia de marca:** ¿refuerza el posicionamiento como experto? ¿tiene sentido que el sitio hable de esto?
- **Potencial comercial:** ¿las personas que buscan esto podrían convertirse en clientes o leads?

## Dónde investigar subtemas

Ningún origen por sí solo es suficiente — cada uno tiene sesgos propios:

- **Herramientas de keywords** (Ahrefs, Semrush, etc.): datos duros de volumen, dificultad, potencial de tráfico.
- **IA generativa** (ChatGPT, Claude, Gemini): generación rápida de ideas masivas — usar para *brainstorming*, nunca como fuente de verdad sobre demanda real.
- **La propia búsqueda de Google:** autocompletar, "otras preguntas de los usuarios" (PAA), búsquedas relacionadas, panel de conocimiento — cada uno revela cómo Google ya entiende la estructura del tema.
- **Wikipedia y fuentes editoriales de referencia:** el índice de un artículo enciclopédico sobre el tema principal ayuda a ver cómo se estructura ese conocimiento.
- **Análisis de competidores:** qué publican y qué tráfico les genera — los huecos frente a ellos son oportunidad.

Esto es coherente con el orden de fuentes ya establecido en `keyword-research-and-query-mapping.md`; aplicarlo aquí a nivel de mapa completo, no solo de un clúster puntual.

## El filtro de cuatro dimensiones

Cada subtema candidato se evalúa en:

1. **Relevancia de marca** — ¿refuerza lo que el sitio representa?
2. **Potencial de negocio** — ¿la persona que busca esto está en algún punto del embudo de compra?
3. **Volumen de búsqueda** — sin necesidad de miles de búsquedas: cola larga con 50-200 búsquedas/mes puede ser muy rentable con alta intención comercial.
4. **Potencial de tráfico real** — cuánto tráfico se captaría realmente en el top 3 para ese clúster.

Regla práctica: si un subtema puntúa bajo en al menos dos de las cuatro dimensiones, se elimina del mapa. El volumen de búsqueda es solo una de las cuatro métricas — nunca el único criterio de inclusión.

## Cómo armar el mapa paso a paso

1. Agrupar los subtemas filtrados en 3-7 clusters. Si un subtema no encaja de forma natural en ninguno, probablemente no pertenece al mapa.
2. Si el sitio ya existe, revisar el sitemap y mapear cada URL existente al subtema correspondiente — muestra de inmediato qué está cubierto y qué huecos hay. Si tienes la skill `screaming-frog-seo` (opcional; no viene en gui-skills) con el MCP local de Screaming Frog, úsala para obtener el inventario real de URLs (indexabilidad, título, profundidad) en vez de trabajar solo del sitemap declarado.
3. Para cada subtema sin URL asignada, definir un slug propuesto — queda un inventario completo de lo que falta producir.

## Priorización de ejecución

Un mapa que se queda en documento es inútil. Tipos de tarea que resultan: crear páginas pilar faltantes, crear artículos nuevos, actualizar contenido existente con más profundidad, consolidar contenido redundante, implementar enlazado interno dentro de cada cluster (ver [internal-linking-and-conversion-paths.md](internal-linking-and-conversion-paths.md)).

Orden de prioridad sugerido:

1. Alta relevancia de marca **y** alto potencial comercial.
2. Alto potencial de tráfico que fortalece autoridad temática.
3. Subtemas informativos que completan cobertura.
4. Actualizaciones de contenido existente.

Revisar el mapa cada 3-6 meses — no es un documento de una sola vez.

## Errores frecuentes

- Incluir todo lo que tiene volumen sin pasar el filtro de cuatro dimensiones.
- Ignorar la intención de búsqueda al agrupar keywords parecidas pero con intención distinta.
- Construir un mapa de 300 subtemas inmanejable en vez de empezar acotado.
- Crear todo el contenido sin conectar con enlazado interno.
- Crear el mapa una vez y no revisarlo nunca más.
- Confundir mapa temático (documento estratégico completo) con cluster de contenido (un grupo de artículos alrededor de una pilar) — el mapa planifica todos los clusters, no es sinónimo de uno solo.

## Lista de revisión

- ¿El tema principal está definido con precisión, incluyendo qué **no** cubre el sitio?
- ¿Cada subtema pasó los dos filtros de alcance (relevancia de marca, potencial comercial)?
- ¿Se consultaron al menos tres fuentes distintas de investigación de subtemas?
- ¿Cada subtema puntuó en las cuatro dimensiones antes de entrar al mapa?
- ¿Las URLs existentes ya están mapeadas a su subtema correspondiente?
- ¿Existe un orden de prioridad de ejecución, no solo una lista?
- ¿Hay fecha de próxima revisión del mapa (3-6 meses)?

Fuente primaria: [Mapa Temático SEO: cómo crearlo desde cero](https://juliandurango.com/blog/mapa-tematico-seo/) — Julián Durango, 1 de marzo de 2026.
