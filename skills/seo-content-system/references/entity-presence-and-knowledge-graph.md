---
tags:
  - seo
  - geo
  - entidades
---

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
