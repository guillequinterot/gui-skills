<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.2.0, huella 14023d946911). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# Estrategia, arquitectura y keyword research

Cómo investigar demanda, construir el mapa temático del sitio, redactar briefs y diseñar enlazado interno. Consolidado a partir de varios archivos de referencia de la skill `seo-content-system` — cada sección conserva el archivo de origen para trazabilidad.

---

## Fuente original: `search-intent-and-customer-journey.md`

# Intención de búsqueda y customer journey

## Índice

- Diferencia central
- Taxonomía de intención
- Etapas del recorrido
- Método de clasificación
- Matriz de decisiones
- Consultas mixtas
- Errores frecuentes

## Diferencia central

La intención describe lo que la persona intenta resolver en la búsqueda actual. El journey representa su relación con una decisión o con la marca.

No fusionar ambos campos.

## Taxonomía de intención

- **Informativa:** aprender, comprender o resolver una duda.
- **Investigación comercial:** comparar enfoques, proveedores, características, precios o riesgos.
- **Transaccional:** comprar, contratar, reservar, registrarse o solicitar.
- **Navegacional:** llegar a una marca, producto, cuenta o página concreta.
- **Mixta:** dos intenciones tienen peso real y la página puede resolver ambas sin dispersarse.

Registrar por separado:

- Intención principal.
- Intención secundaria.
- Componente local: sí/no.
- Necesidad de actualidad: baja/media/alta.

## Etapas del recorrido

- **Atracción:** reconoce un tema, problema u oportunidad.
- **Consideración:** evalúa soluciones y criterios.
- **Decisión:** reduce riesgo y busca actuar.
- **Fidelización:** necesita soporte, adopción, renovación o ampliación.

Una consulta informativa puede pertenecer a cualquier etapa:

| Consulta | Intención | Journey |
|---|---|---|
| Qué es identidad visual | Informativa | Atracción |
| Qué incluye un servicio de identidad visual | Informativa | Consideración |
| Qué archivos debo entregar para iniciar el branding | Informativa | Decisión |
| Cómo aplicar el manual de marca | Informativa | Fidelización |

## Método de clasificación

1. Leer la formulación literal.
2. Identificar verbo, objeto, modificadores, ubicación y marca.
3. Revisar resultados actuales cuando sea posible.
4. Reconocer formatos predominantes sin copiarlos automáticamente.
5. Determinar qué respuesta cerraría satisfactoriamente la búsqueda.
6. Estimar el nivel de conocimiento.
7. Identificar la objeción que impide avanzar.
8. Seleccionar CTA y página siguiente.

## Matriz de decisiones

| Intención y etapa | Prioridad editorial | Evidencia | CTA |
|---|---|---|---|
| Informativa + atracción | Claridad y contexto | Definiciones, fuentes, ejemplos | Explorar guía relacionada |
| Comercial + consideración | Criterios y comparación | Casos, metodología, límites | Conocer servicio o caso |
| Transaccional + decisión | Alcance y reducción de riesgo | Precio, proceso, prueba, condiciones | Solicitar, reservar o comprar |
| Informativa + fidelización | Aplicación práctica | Pasos, soporte, recursos | Usar recurso o contactar soporte |

## Consultas mixtas

No etiquetar “mixta” para evitar decidir. Registrar:

```text
Intención principal:
Intención secundaria:
Porcentaje o peso aproximado:
Secciones que resuelven cada una:
CTA compatible:
```

Separar en páginas distintas cuando:

- Las audiencias son diferentes.
- Las acciones esperadas se contradicen.
- La profundidad necesaria hace que una intención quede enterrada.
- El contenido existente muestra canibalización.

## Errores frecuentes

- Asociar automáticamente “qué es” con atracción.
- Tratar toda consulta local como transaccional.
- Elegir formato solo por volumen.
- Insertar un CTA de venta agresivo en una consulta temprana.
- Copiar la SERP sin evaluar diferenciación.
- Crear una página por cada variante lingüística sin necesidad propia.

---

## Fuente original: `keyword-research-and-query-mapping.md`

# Investigación de keywords y mapeo de consultas

## Índice

- Orden de fuentes
- Campos de la matriz
- Clustering
- Priorización
- Canibalización
- Query fan-out
- Entregable

Para la planificación de arquitectura a nivel de sitio completo (antes de llegar al clustering de una sección puntual), ver [topical-map-and-content-architecture.md](topical-map-and-content-architecture.md). Para el flujo asistido por IA en entornos con acceso local o alojados, ver [keyword-research-ia-local-desktop.md](keyword-research-ia-local-desktop.md) y [keyword-research-ia-web-hosted.md](keyword-research-ia-web-hosted.md). Para cada cuánto repetir esta investigación, ver [keyword-research-cadence-and-triggers.md](keyword-research-cadence-and-triggers.md).

## Orden de fuentes

Priorizar:

1. Consultas reales de Search Console.
2. Búsqueda interna, ventas, soporte, CRM y entrevistas.
3. Datos del sitio y contenido existente.
4. Resultados de búsqueda actuales.
5. Google Trends y herramientas de demanda.
6. Competidores y publicaciones sectoriales.
7. Foros y comunidades como evidencia de lenguaje, no como autoridad factual.

Registrar fuente y fecha. No presentar estimaciones de volumen o dificultad como datos exactos.

## Campos de la matriz

```text
Keyword principal
Consulta real
Variaciones naturales
Intención principal
Intención secundaria
Componente local
Journey
Entidad principal
Problema o pregunta
Formato sugerido
URL asignada
Prioridad comercial
Demanda
Dificultad o competencia
Riesgo de canibalización
Fuente
Fecha
Estado
```

## Clustering

Agrupar por necesidad y respuesta, no solo por coincidencia de palabras.

Dos consultas pertenecen al mismo clúster cuando:

- Esperan una respuesta sustancialmente similar.
- Comparten intención y etapa.
- Una página puede resolverlas con claridad.
- Los resultados actuales muestran solapamiento razonable.

Separarlas cuando exigen un formato, entidad, ubicación, profundidad o acción diferente.

## Priorización

Usar una puntuación explicable, por ejemplo:

```text
Prioridad = valor de negocio + evidencia de demanda + ajuste estratégico
          + oportunidad orgánica - esfuerzo - riesgo
```

No convertir umbrales como KD < 40 o volumen > 100 en reglas universales. Ajustar al mercado, autoridad, ticket, margen y madurez del sitio.

## Canibalización

Investigar:

- Varias URLs reciben impresiones por la misma consulta.
- El ranking alterna entre páginas.
- Anchors internos apuntan a destinos distintos para la misma necesidad.
- Los títulos prometen lo mismo.
- Una página informativa compite con una transaccional.

Opciones:

- Diferenciar intención.
- Consolidar.
- Redirigir.
- Cambiar enlazado.
- Reorientar el contenido.
- Mantener ambas si cumplen funciones distintas y los datos lo respaldan.

## Query fan-out

Generar subpreguntas plausibles para cubrir relaciones útiles:

- Definición.
- Causas.
- Comparaciones.
- Pasos.
- Costos.
- Riesgos.
- Excepciones.
- Aplicación local o sectorial.

No afirmar que estas subpreguntas son exactamente las consultas internas de Google, ChatGPT u otro sistema.

## Entregable

Cada clúster debe terminar con:

- Página objetivo.
- Intención y journey.
- Promesa central.
- Subtemas.
- Fuentes requeridas.
- Enlaces entrantes y salientes.
- CTA.
- KPI.
- Fecha de revisión.

---

## Fuente original: `keyword-research-cadence-and-triggers.md`

# Cada cuánto hacer keyword research: cadencia y disparadores

## Índice

- Principio
- Estado de la evidencia
- Tres tipos de keyword research, tres cadencias distintas
- Cadencia orientativa por tipo de sitio
- Disparadores que fuerzan una revisión fuera de calendario
- Cómo decidir el alcance de cada revisión
- Registro de cadencia por proyecto
- Errores frecuentes
- Lista de revisión

## Principio

"Hacer keyword research" no es un evento único ni una tarea de calendario fijo idéntica para todos los proyectos: la frecuencia correcta depende de qué tipo de investigación es, de la velocidad de publicación del sitio, de la volatilidad del sector y de señales concretas de rendimiento — no de un número universal de meses. Este archivo cierra ese hueco: aplica tanto en la ruta local ([keyword-research-ia-local-desktop.md](keyword-research-ia-local-desktop.md)) como en la ruta alojada ([keyword-research-ia-web-hosted.md](keyword-research-ia-web-hosted.md)).

## Estado de la evidencia

Los rangos de cadencia de este archivo son **heurística de consultoría razonable**, no una cifra medida ni una regla de Google. Se construyen sobre dos piezas ya presentes en la skill que sí tienen justificación propia: la recomendación de revisar el mapa temático cada 3-6 meses (`topical-map-and-content-architecture.md`) y la revisión mensual de logs/consultas ya sugerida para flujos de IA (`ai-assisted-search-console-workflow.md`, `ai-crawler-access-and-llms-txt.md`). Tratar como candidata a ajustar con evidencia propia del proyecto, no como calendario fijo.

## Tres tipos de keyword research, tres cadencias distintas

No es lo mismo investigar desde cero que dar mantenimiento a lo que ya existe. Distinguir:

### 1. Investigación fundacional (mapa temático completo)

Construir o reconstruir el mapa temático completo del sitio (`topical-map-and-content-architecture.md`): tema principal, clusters, universo de subtemas.

- **Cuándo:** al arrancar un proyecto nuevo, o cuando el negocio cambia de forma material (nueva línea de producto, nuevo mercado/país, rebranding, fusión de sitios).
- **No tiene cadencia de calendario fija** — es event-driven, no periódica. Repetirla completa sin que el negocio haya cambiado es desperdiciar el trabajo ya hecho.

### 2. Revisión y expansión del mapa existente

Revisar el mapa ya construido para detectar huecos nuevos, consolidar duplicados y ajustar prioridades — no reconstruirlo desde cero.

- **Cadencia orientativa:** cada 3-6 meses (ya establecida en `topical-map-and-content-architecture.md`). Sitios con publicación intensa o sectores volátiles, hacia el extremo de 3 meses; sitios estables con publicación baja, hacia 6 meses.

### 3. Minería de keywords de oportunidad (mantenimiento continuo)

Detectar keywords de oportunidad sobre contenido ya publicado usando datos reales de Search Console (`analytics-search-console-and-decisions.md`, `ai-assisted-search-console-workflow.md`): posición 5-20, impresiones altas con CTR bajo, gaps de contenido.

- **Cadencia orientativa:** mensual para sitios con volumen alto de tráfico/páginas donde hay suficientes datos nuevos cada mes para que el análisis sea confiable; trimestral para sitios pequeños o de bajo tráfico, donde un mes no acumula señal suficiente en Search Console.
- Esta es la cadencia que más se beneficia de automatización (ver `ai-assisted-search-console-workflow.md`), precisamente porque se repite con frecuencia sobre las mismas URLs.

## Cadencia orientativa por tipo de sitio

| Tipo de sitio / sector | Revisión de mapa | Minería de oportunidad |
|---|---|---|
| Ecommerce o sector de alta competencia y cambio rápido (moda, tecnología, finanzas) | 3 meses | Mensual |
| Servicios B2B o profesionales con catálogo estable | 4-6 meses | Mensual a trimestral |
| Sitio local o de nicho con baja competencia | 6 meses | Trimestral |
| Contenido evergreen de bajo volumen de publicación | 6-12 meses | Trimestral a semestral |

Ajustar siempre con datos propios del proyecto (velocidad real de cambio de la SERP, volumen de tráfico, capacidad del equipo) en vez de aplicar la tabla de forma mecánica.

## Disparadores que fuerzan una revisión fuera de calendario

Cualquiera de estos eventos justifica adelantar la revisión sin esperar al ciclo programado:

- **Core update o spam update de Google** confirmado (ver cadencia "por evento" ya establecida en `update-governance-and-research.md`).
- **Caída o subida sostenida** de impresiones, clics o posición media en un clúster completo, no solo una URL.
- **Aparición de una nueva feature de SERP** relevante para el sector (por ejemplo, AI Overviews empieza a aparecer en consultas transaccionales del nicho).
- **Un competidor gana visibilidad** notable en el mismo campo temático.
- **Lanzamiento de un producto, servicio o línea de negocio nueva.**
- **Canibalización detectada** entre dos o más URLs propias.
- **Cambio de plataforma, CMS o migración** que pueda haber alterado arquitectura o URLs.
- **Anomalía puntual** en Search Console (caída repentina de una página que antes tenía tráfico estable).

## Cómo decidir el alcance de cada revisión

No cada disparador exige repetir la investigación fundacional completa:

```text
¿Cambió el negocio (producto, mercado, marca)?      → investigación fundacional
¿Cambió el algoritmo o la SERP de forma amplia?      → revisión del mapa + validación SERP de clusters afectados
¿Hay una anomalía en una URL o clúster puntual?      → minería de oportunidad focalizada en esa URL/clúster
¿Pasó el tiempo del ciclo normal sin eventos?        → revisión de mapa según la cadencia de la tabla
```

## Registro de cadencia por proyecto

Guardar en la nota del proyecto del usuario (en Obsidian, si lo usa) o en `00_PROYECTO` de la matriz:

```text
Proyecto:
Cadencia de revisión de mapa: (meses)
Cadencia de minería de oportunidad: (meses)
Última investigación fundacional: (fecha)
Última revisión de mapa: (fecha)
Última minería de oportunidad: (fecha)
Próxima revisión programada: (fecha)
Disparadores activados desde la última revisión:
```

## Errores frecuentes

- Tratar "hacer keyword research" como una sola tarea con una sola cadencia, sin distinguir fundacional / revisión de mapa / minería de oportunidad.
- Reconstruir el mapa temático completo cada vez que se detecta una keyword de oportunidad puntual.
- Dejar pasar un core update sin revisar si algún clúster necesita atención antes del ciclo programado.
- Aplicar la misma cadencia a un ecommerce de alta rotación y a un sitio de servicios profesionales estable.
- No registrar la fecha de la última revisión, perdiendo trazabilidad de cuándo tocaría la siguiente.

## Lista de revisión

- ¿Se distinguió qué tipo de keyword research corresponde (fundacional, revisión de mapa, minería de oportunidad)?
- ¿La cadencia elegida está justificada por el tipo de sitio y sector, no aplicada por defecto?
- ¿Se revisó si algún disparador de la lista ocurrió desde la última revisión?
- ¿Quedó registrada la fecha de la última revisión y la próxima programada?
- ¿Una anomalía puntual se atendió de forma focalizada, sin disparar una investigación fundacional innecesaria?

---

## Fuente original: `topical-map-and-content-architecture.md`

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

---

## Fuente original: `content-brief-and-architecture.md`

# Brief y arquitectura de contenidos

## Índice

- Brief obligatorio
- Diseño de la respuesta
- Encabezados
- Profundidad
- Evidencia
- Conversión
- Criterios de aprobación

## Brief obligatorio

```text
Proyecto:
URL o tipo de página:
Objetivo del negocio:
Audiencia:
País/idioma:
Consulta principal:
Intención principal/secundaria:
Journey:
Necesidad:
Nivel de conocimiento:
Objeción:
Respuesta central:
Diferenciador:
Entidades:
Preguntas secundarias:
Fuentes:
Contenido existente:
Competidores de referencia:
CTA:
Página siguiente:
KPI:
Fecha de revisión:
```

## Diseño de la respuesta

Orden recomendado, adaptable:

1. Resolver o enmarcar la pregunta.
2. Aclarar alcance y condiciones.
3. Desarrollar criterios o proceso.
4. Presentar evidencia y ejemplos.
5. Resolver objeciones.
6. Conectar con la siguiente acción.

No agregar secciones por costumbre. Cada bloque debe responder una pregunta o cumplir una función.

## Encabezados

Los encabezados deben:

- Describir el contenido que sigue.
- Mantener jerarquía.
- Ayudar a escanear.
- Usar lenguaje natural.
- Evitar variantes casi idénticas de la keyword.

Un H2 no necesita contener siempre la keyword exacta. No saltar niveles para lograr un estilo visual.

## Profundidad

Definir profundidad por:

- Complejidad de la decisión.
- Conocimiento de la audiencia.
- Riesgo del tema.
- Competencia y cobertura existente.
- Evidencia disponible.
- Formato.

No usar mínimos de palabras como sinónimo de calidad. Eliminar lo que no cambia comprensión o decisión.

## Evidencia

Asignar afirmaciones a fuentes antes de redactar:

| Afirmación | Evidencia | Fuente | Fecha | Limitación |
|---|---|---|---|---|
| Dato de mercado | Estadística | Primaria | AAAA-MM-DD | Muestra/país |
| Resultado del servicio | Caso verificable | Interna | AAAA-MM-DD | Contexto |
| Requisito | Norma/documentación | Oficial | AAAA-MM-DD | Vigencia |

## Conversión

El CTA debe ser la continuación lógica de la respuesta. Definir:

- Acción.
- Beneficio.
- Riesgo percibido.
- Información que necesita antes de actuar.
- Página o canal de destino.
- Evento medible.

## Criterios de aprobación

- Responde la intención.
- Tiene una promesa distinta.
- No contradice otras páginas.
- Las fuentes sostienen las afirmaciones.
- La estructura guía sin inflar.
- El CTA corresponde al journey.
- Existe un plan de enlazado y medición.

---

## Fuente original: `internal-linking-and-conversion-paths.md`

# Enlazado interno y rutas de conversión

## Índice

- Funciones
- Modelo de registro
- Anchor text
- Arquitectura
- Auditoría
- Conversión

## Funciones

Un enlace interno puede:

- Facilitar descubrimiento y rastreo.
- Explicar relaciones temáticas.
- Distribuir autoridad interna.
- Ayudar a completar una tarea.
- Guiar hacia consideración o conversión.

No agregar enlaces solo para alcanzar una cuota.

### Por qué distribuir autoridad interna importa (lógica de fondo)

Google ya no publica un valor público de PageRank, pero sigue usando indicadores de autoridad equivalentes: un enlace entrante es, en esencia, una recomendación, y esa autoridad se reparte entre los enlaces salientes de una página — más enlaces en una página, menor autoridad relativa transmitida por cada uno. Esto explica por qué la arquitectura pilar↔clúster de este archivo y del mapa temático (ver [topical-map-and-content-architecture.md](topical-map-and-content-architecture.md)) importa: concentrar enlaces relevantes hacia las páginas que sí deben posicionar, en vez de enlazar todo hacia todo, es lo que hace efectiva la distribución.

**Advertencia — técnica obsoleta a evitar:** ocultar o "enmascarar" enlaces con JavaScript como alternativa a `rel="nofollow"` (técnica de "PageRank sculpting" de la era 2008-2012) **no** es una práctica recomendada actualmente. Google rastrea y ejecuta JavaScript de forma rutinaria, por lo que no oculta nada del análisis del motor, y la intención de manipular artificialmente el reparto de autoridad por esa vía es contraria al espíritu de las directrices de enlaces de Google — puede leerse como un intento de manipulación de PageRank. Usar en su lugar los atributos que Google sí documenta oficialmente: `rel="nofollow"`, `rel="sponsored"` (enlaces pagados/afiliados) y `rel="ugc"` (contenido generado por usuarios).

## Modelo de registro

```text
URL de origen:
URL de destino:
Anchor:
Ubicación:
Relación:
Intención:
Journey:
Prioridad:
Estado:
```

## Anchor text

Describir el destino con naturalidad.

Preferir:

- conoce el proceso de diseño de marca
- guía para auditar el enlazado interno
- comparar planes de consultoría SEO

Evitar anchors genéricos cuando pierden contexto:

- haz clic aquí
- ver más
- enlace

Variar cuando el contexto lo permita, sin cambiar la promesa del destino. No repetir la keyword exacta artificialmente.

El atributo `title` del enlace es opcional; omitirlo si solo repite el anchor.

## Arquitectura

Diseñar relaciones:

- Pilar ↔ clúster.
- Servicio ↔ caso.
- Artículo ↔ servicio pertinente.
- Guía ↔ recurso práctico.
- Localización ↔ servicio disponible.
- Contenido nuevo ↔ páginas históricas.

Evitar páginas huérfanas y profundidades innecesarias.

## Auditoría

Revisar:

- Enlaces rotos.
- Redirecciones internas.
- Anchors ambiguos.
- Exceso de enlaces repetidos.
- Enlaces a páginas no indexables.
- Huérfanas.
- Canibalización de anchors.
- Enlaces que distraen del CTA principal.

## Conversión

El enlace siguiente debe corresponder al journey. Una guía temprana puede enlazar a una comparación antes del contacto. Una página de decisión debe ofrecer evidencia y una acción directa.

Medir no solo clics, sino calidad del paso:

- Continuación de sesión.
- Evento clave.
- Lead.
- Venta.
- Uso del recurso.
