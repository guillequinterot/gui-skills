---
tags:
  - seo
  - geo
  - entidades
---

# Metodología de Densidad de Señales: taxonomía, KPI y roadmap 30-60-90

## Índice

- Principio
- Estado de la evidencia
- Entidad y Señal (relación con el resto de la skill)
- Los cinco tipos de señal
- El Trigger: la señal de alta relación señal-ruido
- KPI de Densidad de Señales: fórmula y cálculo
- Cómo estimar el "universo temático"
- Roadmap operativo 30-60-90
- Qué confirma y qué no debe confundirse
- Errores frecuentes
- Lista de revisión
- Límites y preguntas abiertas

## Principio

La Metodología de Densidad de Señales (Los Creativos) es un **framework propio de agencia** para operacionalizar la construcción de entidad ante LLMs: convierte el principio ya validado en [entity-presence-and-knowledge-graph.md](entity-presence-and-knowledge-graph.md) (la entidad, no la página, es la unidad de trabajo) en una taxonomía de señales, un KPI de seguimiento y un plan de ejecución por fases. No sustituye a [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md) ni a `entity-presence-and-knowledge-graph.md`: los complementa con el "cómo ejecutar y medir".

Analogía central del propio framework (bingo): cada señal verificable de una entidad es un cartón adicional en juego. Más cartones (señales) distribuidos en más tableros (plataformas) no cambian las reglas del sorteo, pero sí aumentan la probabilidad de coincidencia cuando un usuario formula una consulta. Es la misma lógica que ya recoge `entity-presence-and-knowledge-graph.md` como "cartón de bingo"; este archivo aporta la taxonomía y la fórmula que faltaban.

## Estado de la evidencia

| Afirmación | Estado | Origen |
|---|---|---|
| La entidad (no la página) es la unidad de posicionamiento ante LLMs | Confirmado en la skill, con respaldo cruzado | Los Creativos + `entity-presence-and-knowledge-graph.md` |
| Los LLMs pueden alterar comportamiento con ~250 documentos coherentes | Investigación de terceros, aplica a *entrenamiento*, no a recuperación | Alan Turing Institute + Anthropic (ya registrado en `ai-citation-and-geo-playbook.md`) |
| Las "250 señales" como objetivo operativo de una marca | **Hipótesis/framework propio**, extrapolación deliberada del hallazgo anterior a un contexto distinto (recuperación, no entrenamiento) | Los Creativos, marco de trabajo, no regla |
| La taxonomía de 5 tipos de señal (estructurales, semánticas, relacionales, de autoridad, de distribución) | Framework propio de agencia, sin validación externa independiente | Los Creativos |
| La fórmula de KPI `(Señales × Plataformas / Universo del tema) × 100` | **Explícitamente Beta según el propio autor**: "complejo de medir, aunque paradójicamente comprobado en resultados de visibilidad" (afirmación sin datos publicados que la respalden) | Los Creativos |
| El roadmap 30-60-90 días | Adaptación de un modelo de gestión del cambio (Michael D. Watkins, *The First 90 Days*) a construcción de presencia digital | Los Creativos, aplicación propia de un marco de otra disciplina |

**Lectura obligatoria antes de usar este archivo con un cliente:** todo lo anterior salvo la fila 1 y 2 es marco de trabajo y opinión experta de Los Creativos, no un hallazgo académico independiente ni un benchmark medido con datos publicados. Presentarlo como tal —"metodología propia, en desarrollo"— nunca como "está comprobado que...".

## Entidad y Señal (relación con el resto de la skill)

Antes de aplicar esta taxonomía, completar la ficha de entidad de `entity-presence-and-knowledge-graph.md`. Sin entidad clara (nombre estable, biografías, descripciones coherentes, identificadores), las señales no tienen ancla y pierden fuerza — es el mismo principio de consistencia carácter-por-carácter ya documentado ahí.

Una **Señal**, en este framework, es cualquier aparición verificable de la entidad dentro de un contexto temático, procesable por un sistema de información: un artículo, un perfil, una entrevista, un directorio, una mención en podcast, una cita académica. El valor de una señal no depende del tráfico que genera, sino de si permite responder: ¿quién aparece?, ¿en qué contexto?, ¿con qué temas se relaciona?, ¿en qué plataformas tiene presencia? Una señal débil (contenido duplicado) aporta poco contexto nuevo; una señal fuerte (perfil de autor bien estructurado, mención en medio, cita académica) aporta identidad, relación externa o legitimidad temática.

## Los cinco tipos de señal

Útil como checklist de auditoría de ecosistema antes de planificar un trimestre de contenido:

| Tipo | Responde a | Ejemplos |
|---|---|---|
| **Estructurales** | ¿Qué o quién es la entidad? | Página "Nosotros", Schema de organización/persona, estructura de autor, biografías |
| **Semánticas** | ¿En qué temas participa? | Artículos, investigaciones, whitepapers, casos de estudio, contenido educativo |
| **Relacionales** | ¿Con quién se relaciona? | Enlaces, citaciones, menciones externas (linkbuilding), entrevistas, colaboraciones |
| **De autoridad** | ¿Por qué tiene legitimidad? | PR en medios, participación académica, directorios profesionales, premios, certificaciones |
| **De distribución** | ¿Dónde aparece? | Publicación multiplataforma, diversidad de formatos, presencia multicanal |

Nota táctica del artículo fuente: la página `/nosotros/` o "about", que en SEO clásico a veces se desindexaba para no gastar crawl budget, hoy es señal estructural de alto valor y merece el mismo nivel de optimización que una página transaccional.

La distribución importa tanto como el volumen: diez menciones en un mismo dominio generan contexto limitado; diez menciones en diez plataformas distintas generan contexto diverso, porque los modelos aprenden de distribuciones del lenguaje, no de repetición aislada.

## El Trigger: la señal de alta relación señal-ruido

Un **Trigger** es la señal narrativa central —equivalente conceptual de una pillar page— que organiza y da coherencia a un clúster de señales alrededor de una idea concreta que conecta dos entidades (p. ej. `[Marca] + [tema de especialización]`). No todas las señales pesan igual: un Trigger bien diseñado puede tener más impacto que un volumen grande de contenido ambiguo, porque concentra una asociación clara y repetible entre entidad y tema.

Estructura de un Trigger:

```text
Entidad 1: [la marca]
Entidad 2: [el tema/categoría a poseer]
Trigger: [la afirmación central, ej. "mejor agencia SEO para universidades"]
Señales satélite: caso de éxito, podcasts, comparativas, posts en LinkedIn de las personas de la marca
Canales primarios: blog, YouTube, LinkedIn, etc.
Canales secundarios: perfiles personales de los voceros de la entidad
```

Al planificar un clúster de contenido, definir primero el Trigger y derivar las señales satélite desde ahí — no al revés.

## KPI de Densidad de Señales: fórmula y cálculo

```text
DS = [ (Nº señales totales emitidas) × (Nº plataformas únicas) / (Total de contenidos del tema) ] × 100
```

- **Señales totales:** todo lo verificable de la entidad en el tema — contenido propio, menciones externas, perfiles, entrevistas, citaciones.
- **Plataformas únicas:** dominios/canales distintos donde aparecen esas señales. Corrige el sesgo de inflar el número solo publicando mucho en un mismo sitio.
- **Universo temático (denominador):** el total de contenidos indexados relevantes sobre el tema — no "todo internet", sino el conjunto contra el que compite la entidad.

Pasos: (1) contar señales verificables, (2) contar plataformas únicas, (3) estimar el universo temático, (4) aplicar la fórmula.

**Trátese como indicador direccional de seguimiento propio en el tiempo, no como cifra comparable entre agencias o clientes** — el propio marco lo declara Beta y sin método de cálculo estandarizado.

## Cómo estimar el "universo temático"

Tres métodos, de más simple a más riguroso:

1. **Proxy de resultados de Google.** Buscar la keyword principal, tomar el número de resultados indexados que reporta Google como aproximación. Rápido, poco preciso.
2. **Clúster de keywords.** Buscar varias keywords relacionadas del mismo campo y promediar sus resultados. Da un universo más realista que una sola consulta.
3. **Universo competitivo.** Analizar el top 50 de resultados relevantes, filtrar duplicados, clasificar por entidad y construir un dataset propio. Es el método recomendado para research serio, papers internos o benchmarking de cliente — pero exige tiempo de análisis manual.

## Roadmap operativo 30-60-90

Adaptado del modelo de transición organizacional de Michael D. Watkins (*The First 90 Days*): los cambios estructurales requieren secuencia, no acciones aisladas. Aplica solo después de tener la ficha de entidad de `entity-presence-and-knowledge-graph.md` resuelta.

**Días 0–30 · Construcción de base semántica (claridad interna antes que visibilidad externa)**
- Auditoría y SEO técnico impecable.
- Optimización on-page de activos principales.
- Reestructuración de la arquitectura semántica.
- Definición estricta de entidades corporativas.
- Estructuración verificable de perfiles de autor.

**Días 30–60 · Expansión de señales externas (validación fuera del propio dominio)**
- Linkbuilding estratégico y temático.
- Gestión de PR y medios digitales.
- Inscripción en directorios especializados.
- SEO local, si aplica.
- Construcción de relaciones con otras entidades.

**Días 60–90 · Consolidación de masa crítica (la repetición se transforma en densidad)**
- Generación de citaciones cruzadas entre las propias piezas y plataformas.
- Refuerzo continuo de la autoridad de los autores.
- Publicación recurrente de contenido hiper-especializado (Triggers nuevos).
- Consolidación definitiva de clústeres temáticos.

No saltar la fase 1: construir autoridad externa (fase 2) sin haber fijado primero la identidad interna de la entidad es el error más común que señala el propio framework.

## Qué confirma y qué no debe confundirse

**Confirma y refuerza (ya presente en la skill):** la entidad como unidad de trabajo, la importancia de la distribución multiplataforma sobre el volumen aislado, y la lógica de "cartón de bingo" que ya recogía `entity-presence-and-knowledge-graph.md`.

**No debe confundirse:**
- El umbral de ~250 documentos del estudio Alan Turing Institute + Anthropic es sobre **entrenamiento de modelos** (ver distinción entrenamiento/recuperación en `ai-citation-and-geo-playbook.md`). Las "250 señales" de este framework son una **extrapolación operativa propia** a construcción de marca — útil como objetivo orientador, no como el mismo fenómeno técnico.
- El KPI de Densidad de Señales no es una métrica de plataforma (no lo reporta ninguna herramienta): es un cálculo manual, aproximado, para seguimiento interno.
- Nada de esto reemplaza el hallazgo ya validado en `ai-citation-and-geo-playbook.md` sobre lenguaje natural vs. forzado — la Densidad de Señales opera a nivel de ecosistema/entidad, no da licencia para forzar la escritura de un texto individual.

## Errores frecuentes

- Presentar el KPI de Densidad de Señales como una métrica estándar de la industria o como "comprobada" sin matizar que es Beta y de la propia agencia.
- Confundir el umbral de 250 documentos (entrenamiento, estudio de terceros) con las "250 señales" (objetivo operativo propio, recuperación).
- Publicar señales en muchas plataformas sin haber fijado antes una ficha de entidad consistente (fase 0 saltada).
- Contar señales sin contar plataformas únicas — infla el numerador sin ampliar presencia contextual real.
- Diseñar un clúster de contenido sin definir primero el Trigger que lo organiza.
- Tratar el roadmap 30-60-90 como calendario rígido en vez de secuencia lógica (claridad → distribución → repetición).

## Lista de revisión

- ¿Existe ficha de entidad resuelta antes de empezar a contar o planificar señales?
- ¿Se identificó el Trigger central del clúster antes de producir las señales satélite?
- ¿Las señales cubren los cinco tipos (estructurales, semánticas, relacionales, de autoridad, distribución) o se concentran en uno solo?
- ¿Se contaron plataformas únicas, no solo volumen de piezas?
- ¿El estado de evidencia de cada afirmación de este framework quedó explícito frente al cliente (framework propio vs. estudio de terceros)?
- ¿El roadmap respeta la secuencia 30-60-90 sin saltar la fase de claridad interna?

## Límites y preguntas abiertas

- El KPI no tiene metodología de cálculo estandarizada ni fuente de datos única y verificable para el denominador ("universo temático"); los tres métodos propuestos dan resultados distintos entre sí.
- No hay datos publicados por Los Creativos que muestren la correlación entre el valor del KPI y citaciones reales en LLMs — la afirmación de que "está comprobado en resultados de visibilidad" no viene acompañada de cifras en el artículo fuente.
- La cifra de "250 señales" es una extrapolación deliberada de un hallazgo de entrenamiento a un contexto de marca; el propio framework lo reconoce como referencia conceptual, no como regla rígida.
- El roadmap 30-60-90 no ha sido validado con casos publicados dentro de este mismo artículo (a diferencia del experimento de 90 días de `ai-citation-and-geo-playbook.md`, que sí trae datos de GSC/Bing).

Fuente primaria: [¿Qué es Densidad de Señales y cómo posicionar tu marca en LLMs o en agente de IA en 2026?](https://loscreativos.co/blog/densidad-senales-como-posicionarse-agente-llm-ia/) — Los Creativos, 25 de marzo de 2026. Autoría: David Martínez Mata (fundamento de investigación) y Juan David Uribe Taquez (redacción e interpretación estratégica). Incluye presentación PDF de 15 láminas.
