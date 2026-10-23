<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella 39bc61e14024). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# GEO: citación en IA, entidades y densidad de señales

Visibilidad ante LLMs, construcción de entidad y grafo de conocimiento, la Metodología de Densidad de Señales de Los Creativos, y diversificación de canales (YouTube, comunidades).

---

## Fuente original: `ai-citation-and-geo-playbook.md`

# Citación en IA, agrupadores y lenguaje natural vs. optimizado

## Índice

- Principio
- Estado de la evidencia
- El experimento de 90 días
- Hallazgo 1: el lenguaje forzado pierde
- Hallazgo 2: las páginas agrupadoras concentran la citación
- Entrenamiento y recuperación no son lo mismo
- Qué confirma y qué corrige la Densidad de Señales
- Playbook táctico de ejecución
- Errores frecuentes
- Lista de revisión
- Límites y preguntas abiertas

## Principio

La visibilidad ante sistemas de inteligencia artificial no se gana escribiendo para un validador robótico. Se gana con **autenticidad humana verificable** respaldada por un **ecosistema digital interconectado**. Optimizar la superficie lingüística de un texto para que parezca "semánticamente denso" es, con la evidencia disponible, contraproducente.

## Estado de la evidencia

Clasificación honesta de lo que aquí se afirma:

| Afirmación | Estado | Origen |
|---|---|---|
| El lenguaje natural supera al lenguaje forzado en citaciones de IA | **Experimento propio** (n=2 sitios, 90 días, un sector, un idioma) | Los Creativos, 2026 |
| Las páginas agrupadoras concentran la mayoría de citaciones | **Experimento propio + caso de escala** | Los Creativos / BIU |
| Umbral de ~250 documentos coherentes para alterar comportamiento del modelo | **Investigación de terceros**, aplica a *entrenamiento*, no a recuperación | Anthropic + Alan Turing Institute + UK AI Security Institute |
| Reddit, Wikipedia y YouTube dominan la citación en IA | **Estudios de terceros**, correlacional, sujeto a cambio | Semrush, Profound, índices públicos 2026 |

Ninguna de estas afirmaciones es una ley universal. Son evidencia direccional. Al aplicarlas, decirlo.

## El experimento de 90 días

Diseño (Los Creativos, dirigido por David Martínez Mata):

- **Sujetos:** dos sitios web gemelos de escuelas de idiomas en Francia.
- **Duración:** 90 días, con datos reales de Google Search Console y Bing Webmaster Tools.
- **Variables de control (idénticas):** mismas empresas locales, reseñas reales de Google My Business, idéntica estructura H1–H3.
- **Variable independiente (lo único distinto):** el tratamiento lingüístico del texto.

Los dos corpus:

- **Corpus A — Optimizado (Protocolo PES).** Explicitación Semántica bajo cinco reglas: campo léxico con hiperónimos e hipónimos, sinonimia controlada, anáforas nominales obligatorias (prohibidos los pronombres simples), marcadores discursivos inyectados y densidad léxica forzada al 45–55 %. Validado por un script de Python (`pes_validator.py`) con spaCy.
- **Corpus B — Natural.** Narrativa libre, tono conversacional experto, sin reglas matemáticas ni validación robótica. Escrito para ser leído por una persona.

## Hallazgo 1: el lenguaje forzado pierde

Resultados a tres meses:

| Métrica | Sitio optimizado (PES) | Sitio natural |
|---|---|---|
| Impresiones (GSC) | 106 | **205** |
| Posición promedio | 61,9 | **51,2** |
| Citaciones en IA (Bing/Copilot) | 9 | **118** |

En Google la diferencia fue moderada: el sitio natural obtuvo casi el doble de exposición y mejor posición inicial, aunque ambos seguían en sandbox. **En la IA la diferencia fue de aproximadamente 13×.**

Explicación propuesta: para un modelo entrenado con volúmenes enormes de lenguaje natural, el texto artificialmente estructurado **suena anómalo**. Forzar sinónimos y conectores inyectados rompe la fluidez, y un sistema de recuperación busca fluidez y respaldo verificable (autores reales, perfiles validados). La autenticidad humana se reconoce de forma implícita.

Consecuencia operativa: **escribir para el validador robótico está muerto; escribir para el experto humano es el estándar.** No fijar densidades objetivo, no inyectar conectores por cuota, no prohibir pronombres.

## Hallazgo 2: las páginas agrupadoras concentran la citación

En el sitio natural, la URL agrupadora `/ecoles-de-langues/` —el directorio que reúne la información de todas las ciudades— acumuló **65 citaciones**, más del 50 % del total. Las páginas ultraespecíficas por ciudad casi no fueron citadas (Toulouse 1, Rennes 1, Strasbourg 1, Lille 1).

Validación a escala (caso Broward International University, dominio con autoridad histórica): las URLs más citadas fueron artículos agrupadores por **tipología de contenido**, no por keyword aislada:

- `/mba-online-vs-presencial-roi-latinoamerica-2026` → 1,3 K citaciones
- `/diferencia-entre-educacion-remota-y-virtual` → 1,1 K citaciones
- `/calidad-academica-biu` → 860 citaciones

**La lógica evolucionada:** agrupar no es solo reunir ciudades. Es crear tipologías de contenido —comparativas, guías técnicas, rankings—. A mayor agrupación de valor resolutivo en una sola URL, mayor volumen de citaciones.

**Por qué ocurre (eficiencia energética).** La memoria y el procesamiento del grafo de conocimiento son costosos. Saltar entre decenas de páginas dispersas gasta recursos computacionales; citar un nodo agrupador consolidado resuelve múltiples sub-consultas en un solo lugar. Un bot prefiere la página que responde más con menos saltos. La analogía: la esfera encierra más volumen con menos superficie.

### Cómo diseñar un agrupador

1. Elegir una **tipología**, no una keyword: comparativa, ranking, guía técnica, directorio, glosario, "X vs Y", "cómo elegir".
2. Que resuelva **varias sub-consultas plausibles** en la misma URL, cada una bajo su propio encabezado.
3. Enlazar desde el agrupador hacia las páginas específicas y **de vuelta** desde ellas (ecosistema de enlaces cruzados).
4. Embeber diversidad de formatos dentro del agrupador: video, audio, resumen en PDF, tablas.
5. Jerarquía impecable H1–H6 y datos estructurados (Schema, FAQ) para facilitar la recuperación.
6. No fragmentar en microURLs lo que la IA prefiere citar unido.

## Entrenamiento y recuperación no son lo mismo

Distinción crítica que evita prometer resultados imposibles:

**Mecanismo de entrenamiento.** Absorbe datos masivos para construir los pesos del modelo a lo largo de meses. Aquí aplica el umbral de los ~250 documentos coherentes para alterar un comportamiento base. Es lento y no se controla desde una campaña.

**Mecanismo de recuperación (RAG / búsqueda).** Consulta fuentes en tiempo real para responder a un usuario (Copilot, Perplexity, Gemini). Requiere máxima eficiencia en milisegundos.

**Las citaciones medidas en este experimento son de recuperación.** El bot no está aprendiendo: está buscando la respuesta más completa al instante. Casi todo el SEO accionable hoy opera sobre recuperación. No vender efectos de entrenamiento como si fueran alcanzables en un trimestre.

## Qué confirma y qué corrige la Densidad de Señales

**Confirmado (el ecosistema macro).** La Densidad de Señales **entre** plataformas es crítica. Las páginas agrupadoras respaldadas por un ecosistema de enlaces cruzados y diversidad de formatos son el imán de citaciones para la IA.

**Corregido (el texto micro).** La Densidad de Señales forzada **dentro** de un texto individual —optimización matemática explícita— ya no aporta valor: penaliza.

La metodología sigue siendo válida a nivel de entidad y ecosistema. Deja de serlo a nivel de párrafo.

## Playbook táctico de ejecución

1. **Partir del experto.** Anclar la autoridad (EEAT) desde el primer párrafo, con nombre, credenciales y enlaces a perfiles validados de LinkedIn.
2. **Agrupación temática.** Construir URLs por tipología de contenido (guías, rankings, comparativas), no por palabra clave aislada.
3. **Diversidad multimedia.** Embeber videos, audios y resúmenes en PDF dentro del agrupador para enriquecer la retención.
4. **Esquemas ricos.** Jerarquías impecables H1–H6 y marcado de datos estructurados (Schema, FAQ) para facilitar la eficiencia de recuperación.

Complementar con [entity-presence-and-knowledge-graph.md](entity-presence-and-knowledge-graph.md), [channel-diversification-and-youtube-seo.md](channel-diversification-and-youtube-seo.md), [community-search-reddit-quora.md](community-search-reddit-quora.md) y [signal-density-methodology-and-kpi.md](signal-density-methodology-and-kpi.md) (taxonomía de señales, KPI Beta y roadmap 30-60-90 para ejecutar esto por fases).

## Errores frecuentes

- Fijar una densidad léxica objetivo y editar el texto hasta cumplirla.
- Sustituir pronombres por sustantivos repetidos "para que la IA entienda mejor".
- Inyectar conectores discursivos que la lógica del párrafo no pedía.
- Crear una URL por cada variación de keyword y dispersar el valor resolutivo.
- Publicar el agrupador sin enlaces de vuelta desde las páginas hijas.
- Presentar el umbral de 250 documentos como si aplicara a la recuperación.
- Extrapolar estos resultados a todos los modelos: los datos actuales reflejan Copilot (Bing).

## Lista de revisión

- ¿El texto se sostiene leído en voz alta por una persona experta?
- ¿Hay alguna regla lingüística aplicada por cuota y no por sentido?
- ¿Existe una URL agrupadora que resuelva varias sub-consultas?
- ¿El agrupador enlaza a las hijas y las hijas de vuelta al agrupador?
- ¿La autoría es real, nombrada y verificable desde el primer párrafo?
- ¿Hay diversidad de formatos dentro del agrupador?
- ¿Se distinguió en el entregable qué es recuperación y qué es entrenamiento?
- ¿Se etiquetó el estado de la evidencia de cada afirmación?

## Límites y preguntas abiertas

- Los datos de citación provienen de **Copilot (Bing)**. El comportamiento en Claude, ChatGPT, Perplexity y Deepseek aún no está medido en este experimento.
- La muestra es de dos sitios, un sector (escuelas de idiomas), un idioma (francés) y un país.
- Ambos sitios eran nuevos y permanecían en sandbox de Google; los resultados de Google no son concluyentes.
- El caso BIU aporta magnitud pero parte de un dominio con autoridad histórica, lo que no es replicable de inmediato.
- No se ha aislado cuánto del efecto proviene del lenguaje y cuánto de la estructura agrupadora.

Fuente primaria: [¿La IA premia el lenguaje optimizado o el lenguaje natural?](https://loscreativos.co/blog/seo-en-ia-premia-lenguaje-natural-optimizado/) — Los Creativos, 24 de agosto de 2026. Investigación de David Martínez Mata, interpretación de Juan David Uribe Taquez.

---

## Fuente original: `entity-presence-and-knowledge-graph.md`

# Entidad, grafo de conocimiento, Wikidata y tripletas semánticas

## Índice

- Principio
- La entidad como unidad de trabajo
- Tripletas semánticas
- Wikidata y Wikipedia
- Presencia en consultas y grafos
- Schema y `sameAs`
- Errores frecuentes
- Lista de revisión

## Principio

Los sistemas de recuperación no razonan sobre páginas: razonan sobre **entidades y relaciones**. Una marca invisible como entidad puede tener buen contenido y aun así no ser citada, porque el modelo no sabe qué es, a qué categoría pertenece ni con qué otras entidades se relaciona.

El trabajo consiste en volver la entidad **inequívoca, consistente y verificable** en todas partes donde aparezca.

## La entidad como unidad de trabajo

Antes de escribir, definir la ficha de entidad:

```text
Nombre canónico:
Variantes y alias (cómo la nombran de verdad):
Tipo (organización, persona, producto, lugar, concepto):
Categoría temática principal:
Entidades relacionadas (personas, marcas, lugares, tecnologías):
Atributos verificables (fundación, sede, tamaño, sector, certificaciones):
Identificadores externos (Wikidata QID, LinkedIn, GBP, registro mercantil):
Fuentes públicas que respaldan cada atributo:
```

Regla de consistencia: el nombre, la descripción y los atributos deben coincidir **carácter por carácter** entre el sitio, Schema, Google Business Profile, LinkedIn, directorios y perfiles sociales. La incoherencia es lo que impide que el sistema fusione todas las menciones en una sola entidad.

Ver también el umbral de coherencia y la lógica de agrupadores en [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md).

## Tripletas semánticas

Una tripleta es la unidad mínima de conocimiento estructurado: **sujeto → predicado → objeto**. Es la forma en que Wikidata, los grafos de conocimiento y el marcado RDF representan hechos.

```text
[Los Creativos] —(es una)→ [agencia de marketing digital]
[Los Creativos] —(tiene sede en)→ [Medellín, Colombia]
[David Martínez Mata] —(es director de SEO en)→ [Los Creativos]
```

**Cómo se usa al redactar.** No se trata de escribir robóticamente en sujeto-verbo-predicado. Se trata de asegurar que cada afirmación importante del texto **pueda extraerse como tripleta**: que tenga sujeto explícito, relación clara y objeto identificable.

Ambiguo (no extraíble):

> Llevamos más de una década ayudando a que las marcas crezcan en la región.

Extraíble (sin sonar artificial):

> Los Creativos es una agencia de marketing digital con sede en Medellín que desde 2013 acompaña a marcas en Colombia, Ecuador, España, Estados Unidos y Australia.

De la segunda frase salen cinco tripletas limpias. Sigue siendo prosa natural.

**Prueba práctica:** tomar los diez enunciados centrales de la pieza y verificar que cada uno responde *quién / qué relación / con qué*. Si el sujeto es "esto", "ello" o está elidido, la tripleta se rompe. Esto es coherencia referencial, no ingeniería lingüística: la diferencia está en que se corrige el enunciado que realmente es ambiguo, no en aplicar una regla a todos por cuota.

## Wikidata y Wikipedia

Wikidata es la capa de datos estructurados bajo Wikipedia. Alimenta el grafo de conocimiento de Google y forma parte de los datos de entrenamiento de los principales modelos de lenguaje. Las entidades con ficha en Wikidata tienden a ser reconocidas, atribuidas correctamente y citadas con más confianza.

**Advertencia de notabilidad.** Wikidata y Wikipedia tienen criterios propios y comunidades activas de edición. No toda marca califica. Crear entradas promocionales para una entidad sin notabilidad demostrable **es contraproducente**: se revierte, y deja historial. No prometer al cliente una página de Wikipedia como entregable.

Camino realista, en orden:

1. **Construir la evidencia externa primero.** Cobertura de medios independientes, publicaciones académicas, registros oficiales, bases de datos sectoriales. La notabilidad se demuestra, no se declara.
2. **Verificar si ya existe la entidad** en Wikidata antes de crear nada (duplicados dañan).
3. **Empezar por entidades más fáciles de sostener:** personas con obra publicada, productos con cobertura, eventos documentados.
4. **Cada declaración debe llevar cita** a una fuente pública, fiable y verificable. Es requisito, no buena práctica.
5. **Nunca editar con conflicto de interés no declarado.** Las comunidades lo detectan y penalizan.

Si la entidad no es notable, el esfuerzo rinde más en identificadores sectoriales, perfiles verificados y `sameAs` (abajo) que en forzar una entrada enciclopédica.

## Presencia en consultas y grafos

Además de Wikidata, la entidad debe existir donde los sistemas la puedan resolver:

- **Google Business Profile** completo y consistente (si hay componente local).
- **Perfiles verificados** de la organización y de sus personas clave, especialmente LinkedIn — el playbook de citación lo usa como anclaje de EEAT.
- **Registros e identificadores sectoriales** propios del rubro (cámaras, asociaciones, catálogos, ORCID para autores académicos).
- **Menciones coherentes en plataformas de terceros**, incluidas comunidades — ver [community-search-reddit-quora.md](community-search-reddit-quora.md).
- **Formatos diversos** que hablen de la misma entidad — ver [channel-diversification-and-youtube-seo.md](channel-diversification-and-youtube-seo.md).

Cada presencia coherente es una señal adicional. La lógica del "cartón de bingo": más superficies consistentes, mayor probabilidad de coincidir cuando alguien pregunta por el tema. Para la taxonomía de tipos de señal, el KPI de seguimiento (Beta) y el roadmap de ejecución por fases, ver [signal-density-methodology-and-kpi.md](signal-density-methodology-and-kpi.md).

## Schema y `sameAs`

El puente entre el sitio y el grafo externo:

- `Organization` o `LocalBusiness` con `name`, `description`, `logo`, `url`, `address`, `founder`.
- `Person` para autores y directivos, con `jobTitle` y `worksFor`.
- **`sameAs`** apuntando a Wikidata (si existe), LinkedIn, perfiles oficiales y registros. Es la declaración explícita de "estas identidades son la misma entidad".
- `author` real en cada artículo, enlazado a la ficha `Person`.
- Coherencia entre lo que dice el Schema y lo que dice el texto visible. Si difieren, gana el texto visible y el marcado pierde credibilidad.

Mantener visible y útil todo contenido descrito por datos estructurados. Ver [structured-data-and-search-features.md](structured-data-and-search-features.md) y, para la priorización de tipos y la técnica `@graph` orientadas a GEO, [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).

## Errores frecuentes

- Nombrar la marca de cinco formas distintas entre el sitio, LinkedIn y GBP.
- Crear una entrada de Wikipedia promocional sin notabilidad y sin declarar el conflicto de interés.
- Añadir declaraciones a Wikidata sin cita verificable.
- Escribir en sujeto-verbo-predicado telegráfico creyendo que eso son "tripletas semánticas".
- Marcar `sameAs` hacia perfiles abandonados o con datos contradictorios.
- Firmar artículos con autores genéricos ("Equipo editorial") y esperar señales de EEAT.
- Duplicar entidades en Wikidata por no buscar antes.

## Lista de revisión

- ¿Existe una ficha de entidad escrita antes de redactar?
- ¿El nombre y la descripción son idénticos en todas las plataformas?
- ¿Los diez enunciados centrales se pueden extraer como tripletas sin ambigüedad?
- ¿Cada atributo afirmado tiene una fuente pública que lo respalde?
- ¿Se verificó si la entidad ya existe en Wikidata?
- ¿La notabilidad está demostrada antes de intentar cualquier entrada enciclopédica?
- ¿`sameAs` apunta a perfiles vivos y coherentes?
- ¿Los autores son personas reales con perfil verificable?


## Ampliación [ClickUp 2]: perfiles de equipo y cajas de autor

- **Perfiles de equipo como páginas de autor:** una URL por persona con cargo, módulos de servicio o industria y enlaces a sus apariciones (conferencias, artículos). Es una señal de experiencia y autoría (E-E-A-T) y alimenta el grafo de entidades (`Person` con `sameAs`).
- **Ficha o caja de autor en los artículos**, enlazada al perfil.
- En sitios de educación, la misma lógica aplica a **docentes e investigadores**: página agrupadora + una interna por persona, solo con perfiles aprobados; ver [education-program-seo.md](education-program-seo.md).
- Schema por tipo de entidad (programa, organización, persona) en la **plantilla**, una sola vez, y validado en lote; ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).

---

## Fuente original: `signal-density-methodology-and-kpi.md`

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

---

## Fuente original: `channel-diversification-and-youtube-seo.md`

# Diversificación de canales y SEO en YouTube

## Índice

- Principio
- El agrupador como centro, los canales como radios
- Matriz de canales
- SEO en YouTube
- Reaprovechamiento sin duplicación
- Qué medir
- Errores frecuentes
- Lista de revisión

## Principio

Una entidad citada por sistemas de IA rara vez vive en un solo sitio. La evidencia del experimento de 90 días apunta a que **la diversidad de formatos y plataformas alrededor de un mismo tema** es lo que convierte una URL en imán de citaciones. Diversificar no es estar en todas partes: es sostener presencia **coherente** en las superficies donde el público y los sistemas de recuperación efectivamente buscan.

## El agrupador como centro, los canales como radios

El modelo operativo es un cubo con radios:

```text
                    PDF / resumen descargable
                             │
        Podcast ─────── AGRUPADOR TEMÁTICO ─────── YouTube
                             │
                      LinkedIn / comunidades
```

- El **agrupador** en el sitio propio es el nodo canónico y el destino de la citación.
- Cada canal aloja una **versión nativa** del mismo conocimiento, no un recorte automático.
- Todos apuntan al agrupador; el agrupador embebe o enlaza a todos.
- Se refuerza la misma entidad y los mismos hechos en cada superficie.

Ver [ai-citation-and-geo-playbook.md](ai-citation-and-geo-playbook.md) para el diseño del agrupador y [entity-presence-and-knowledge-graph.md](entity-presence-and-knowledge-graph.md) para la coherencia de entidad.

## Matriz de canales

Decidir por criterio, no por inercia:

| Canal | Aporta | Cuándo tiene sentido |
|---|---|---|
| YouTube | Motor de búsqueda propio + alta citación en IA | Hay demanda demostrable de video en el tema |
| LinkedIn | Señal de EEAT, perfiles de autores | B2B, servicios profesionales, educación |
| Comunidades | Conversación real y citación | Ver [community-search-reddit-quora.md](community-search-reddit-quora.md) |
| PDF / resumen | Formato descargable citable, embebible | Contenido de investigación o guía extensa |
| Podcast | Retención y alcance en audio | Existe capacidad real de sostener cadencia |
| TikTok / Reels | Descubrimiento en audiencias jóvenes | El tema admite formato corto sin distorsionarse |

Regla de honestidad operativa: **no abrir un canal que no se pueda sostener**. Un canal abandonado es una señal de entidad incoherente, no una señal adicional.

## SEO en YouTube

YouTube funciona como buscador con su propia lógica de recomendación, y además es una de las superficies más citadas por sistemas de IA.

**Antes de grabar**

- Investigar la demanda dentro de YouTube (autocompletado, videos existentes, comentarios que revelan preguntas sin responder).
- Definir la consulta principal y la promesa concreta del video.
- Decidir si el tema realmente gana en video o solo se está duplicando el artículo.

**Metadatos**

- **Título:** la consulta real del usuario, con la promesa clara al inicio. Sin acumulación de keywords.
- **Descripción:** primeras dos líneas son las visibles y las que más pesan; resumen real del contenido. Después, contexto ampliado, marcas de tiempo y **enlace al agrupador**.
- **Etiquetas:** apoyo menor; no compensan un título ambiguo.
- **Miniatura:** determina el clic más que ningún otro elemento. Legible en tamaño pequeño, coherente con el título, sin prometer lo que el video no entrega.
- **Capítulos:** marcas de tiempo reales. Ayudan a la retención y hacen el contenido más recuperable por segmentos.

**Contenido**

- Resolver pronto la promesa del título; la retención temprana condiciona la distribución.
- Estructura declarada al inicio para que el espectador sepa qué viene.
- Hablar como experto humano — el mismo criterio de naturalidad del resto de esta skill aplica al guion.

**Accesibilidad y recuperación**

- **Subtítulos revisados a mano.** Los automáticos en español cometen errores en términos técnicos y nombres de marca, justo lo que necesita ser reconocido.
- La transcripción es texto indexable: publicar una versión editada dentro del agrupador.
- Nombres de archivo y descripciones coherentes con la entidad.

**Sobre las métricas**

Las señales que YouTube pondera (retención, clic, satisfacción) están documentadas de forma general por la propia plataforma, pero **el peso exacto del algoritmo no es público**. No presentar reglas de ponderación como hechos verificados.

## Reaprovechamiento sin duplicación

- Adaptar, no cortar y pegar: cada plataforma tiene formato y expectativa propios.
- El mismo hecho puede repetirse en todas partes; el mismo párrafo, no.
- La transcripción publicada debe editarse para leerse como texto, no como habla transcrita.
- Evitar contenido duplicado indexable entre el agrupador y las versiones externas: canonical claro y valor diferenciado en cada superficie.

## Qué medir

- YouTube Studio: impresiones, CTR de miniatura, retención media, fuentes de tráfico.
- GA4: tráfico de referencia desde cada canal hacia el agrupador.
- Search Console: si el tema del video mueve consultas de marca o de la entidad.
- Comprobación manual periódica: ¿aparece el video o el agrupador citado en respuestas de IA?

Comparar periodos equivalentes y considerar estacionalidad antes de concluir.

## Errores frecuentes

- Abrir cinco canales y sostener ninguno.
- Subir el artículo leído en voz alta y llamarlo video.
- Rellenar la descripción con keywords en vez de un resumen real.
- Dejar los subtítulos automáticos sin revisar.
- Publicar la transcripción cruda como si fuera un artículo.
- Prometer que un canal nuevo generará citaciones en IA a corto plazo.
- Afirmar pesos concretos del algoritmo de YouTube como si fueran públicos.

## Lista de revisión

- ¿Cada canal abierto se puede sostener con la capacidad real del equipo?
- ¿Existe un agrupador que actúe como nodo canónico?
- ¿Todos los canales apuntan a él y él los recoge?
- ¿El título del video es la consulta real y no una acumulación de keywords?
- ¿La miniatura es legible en pequeño y honesta?
- ¿Los subtítulos fueron revisados a mano?
- ¿La transcripción publicada está editada para lectura?
- ¿Se distinguió lo documentado por la plataforma de lo inferido?

---

## Fuente original: `community-search-reddit-quora.md`

# Búsqueda en comunidades: Reddit y Quora, con enfoque LATAM

## Índice

- Principio
- Por qué pesan las comunidades
- Realidad LATAM y en español
- Regla de participación legítima
- Método de trabajo
- Reddit
- Quora y equivalentes
- Qué medir
- Errores frecuentes
- Lista de revisión

## Principio

El contenido generado por usuarios ocupa una parte desproporcionada de lo que los sistemas de IA citan. Trabajar comunidades no es "poner enlaces en foros": es **participar donde la conversación real ocurre**, con identidad declarada y aporte verificable, para que la entidad exista en las superficies que los modelos consultan.

## Por qué pesan las comunidades

Estudios públicos de 2026 (Semrush, Profound e índices de citación) coinciden en un patrón: la citación en IA está mucho más concentrada que la búsqueda orgánica, y el contenido de comunidad domina.

Cifras reportadas por esos estudios, **con estado de evidencia "terceros / correlacional"**:

- Reddit ronda el 46 % de las citaciones de Perplexity y cerca del 21 % de las de Google AI Overviews.
- Wikipedia es la fuente más citada por ChatGPT (~7,8 % del total).
- Los 15 dominios más citados capturan alrededor del 68 % de la citación consolidada, frente a ~20 % en búsqueda orgánica de Google para consultas comparables.
- Reddit, YouTube, LinkedIn, Quora, Stack Overflow y Facebook, sumados, superan la citación conjunta de los 20 grandes medios periodísticos.

**Cómo usar estos números.** Son direccionales y cambian rápido. Sirven para justificar *dónde invertir esfuerzo*, no para prometer resultados. Al citarlos en un entregable, nombrar la fuente, la fecha y su condición de estudio de terceros. Ver [source-verification-and-evidence.md](source-verification-and-evidence.md).

## Realidad LATAM y en español

Antes de copiar tácticas anglosajonas, verificar la realidad del mercado hispanohablante:

- **Reddit en español tiene masa crítica desigual.** Comunidades como r/MedellinColombia, r/Colombia, r/mexico, r/argentina, r/chile, r/uruguay o r/PERU son activas; verticales profesionales en español lo son mucho menos que sus equivalentes en inglés.
- **Quora en español está en declive** frente a su versión en inglés. No asumir que replica el peso que tiene en índices anglosajones.
- **El hueco lo llenan otras superficies:** grupos y páginas de Facebook (todavía muy vivos en LATAM), WhatsApp y Telegram (no rastreables, no sirven para citación), LinkedIn en español, TikTok y YouTube como motores de respuesta, y foros verticales locales.

Consecuencia: para LATAM, **no dar por hecho que Reddit y Quora son el canal principal**. Investigar dónde ocurre la conversación real del sector y del país antes de asignar presupuesto. Documentar el hallazgo en el vault.

## Regla de participación legítima

Innegociable, y previa a cualquier táctica:

1. **Identidad declarada.** Si se participa en nombre de una marca o como su empleado, decirlo. El astroturfing es detectable, viola las normas de las plataformas y, cuando se descubre, destruye la señal de entidad que se buscaba construir.
2. **Aportar antes de pedir.** Responder preguntas sin enlace, de forma útil, durante un tiempo real.
3. **Respetar las reglas de cada comunidad.** Muchos subreddits prohíben enlaces de marca por completo. Leerlas antes de publicar.
4. **No incentivar reseñas ni respuestas falsas.**
5. **No borrar el rastro cuando algo sale mal.** Corregir públicamente construye más autoridad que desaparecer.

Si el cliente pide participación encubierta, explicar el riesgo y proponer la alternativa declarada. No ejecutarla.

## Método de trabajo

1. **Escuchar.** Buscar las consultas reales del negocio en cada plataforma y registrar qué se pregunta, con qué palabras y qué respuestas ganan tracción.
2. **Mapear superficies.** Listar comunidades por país, sector e idioma, con volumen y reglas de cada una.
3. **Priorizar** por conversación real, no por tamaño bruto.
4. **Participar** con una persona identificada de la organización — idealmente la misma que firma el contenido del sitio, para reforzar la entidad.
5. **Conectar** las respuestas con el agrupador del sitio cuando la comunidad lo permita y **solo** cuando aporte a quien pregunta.
6. **Registrar** en la memoria (`memoria/aprendizaje/inbox/`, o la bóveda si se usa Obsidian) qué funcionó, en qué comunidad y con qué evidencia.

## Reddit

- Leer las reglas del subreddit antes de cualquier publicación; la mayoría de los baneos ocurren por ignorarlas.
- Construir historial de cuenta con aportes ajenos al negocio.
- Las respuestas largas y específicas rinden más que las promocionales breves.
- Los hilos de tipo "X vs Y", "¿cuál recomiendan?" y "mi experiencia con…" son los que más aparecen citados por sistemas de IA.
- Un AMA solo funciona con experticia real y aprobación de moderadores.

## Quora y equivalentes

- Verificar primero si el volumen en español justifica el esfuerzo para ese sector.
- Perfil completo con credenciales reales; la biografía es parte de la señal de entidad.
- Responder preguntas donde exista experiencia genuina, no todas las del tema.
- Las respuestas con datos propios y estructura clara envejecen mejor.
- Considerar equivalentes locales del sector antes de asumir que Quora es la opción.

## Qué medir

- Menciones de marca y de personas clave por plataforma, con fecha.
- Apariciones de esas URLs o hilos dentro de respuestas de IA (comprobación manual periódica).
- Tráfico de referencia en GA4 desde comunidades.
- Consultas de marca en Search Console como proxy de reconocimiento de entidad.

No atribuir causalidad de una sola coincidencia temporal. Comparar periodos equivalentes.

## Errores frecuentes

- Publicar el mismo texto en varias comunidades a la vez.
- Crear cuentas de marca encubiertas.
- Asumir que las cifras anglosajonas aplican a LATAM sin verificar.
- Enlazar en cada respuesta hasta que la comunidad expulse la cuenta.
- Tratar WhatsApp o Telegram como superficie de citación (no son rastreables).
- Presentar los porcentajes de citación de terceros como dato propio.

## Lista de revisión

- ¿Se verificó dónde ocurre la conversación real en el país y sector, en lugar de asumirlo?
- ¿La participación va con identidad declarada?
- ¿Se leyeron las reglas de cada comunidad?
- ¿La persona que participa es la misma que firma el contenido del sitio?
- ¿Cada aporte es útil aunque se le quite el enlace?
- ¿Las cifras de terceros están etiquetadas como tales, con fuente y fecha?
- ¿Se registró el aprendizaje en la memoria como candidato, no como regla?
