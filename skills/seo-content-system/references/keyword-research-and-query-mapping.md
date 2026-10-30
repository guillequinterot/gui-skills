---
tags:
  - seo
---

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


## Formato de hoja del equipo [Sheets]
- Calendario editorial (una fila por pieza, con la aprobación del cliente en la misma fila): `assets/templates/keyword-content-calendar.csv`.
- Términos por pieza (dificultad, volumen, CPC, CPS, objetivo SEO/IA): `assets/templates/keyword-research-terms.csv`.
- Mapeo de keywords a la arquitectura (niveles 1–4, tipología, metadatos con caracteres restantes): `assets/templates/content-architecture-map.csv`.


## KWR por programa y gameplan E-E-A-T [Drive]
Usa una pestaña por programa con bloques *Keyword · VOL/M · Dificultad* y una pestaña Resumen (`assets/templates/kwr-program-clusters.csv`). El gameplan trimestral con preguntas al experto va en `assets/templates/eeat-gameplan.csv`. Ver `references/drive-deliverables-and-guidelines.md` §7–8.



## Mapa de clústeres frente al sitio: cobertura y acción por clúster (SEO Skills, 2026-10-30)

Origen: skill `keyword-cluster` de `seo-skills.com` (Jorge Jaramillo), reformulada; el repositorio no declara licencia. Cruza una lista de keywords con las páginas existentes y deja una acción por clúster. No sirve para optimizar el title de una sola página ([title-and-description-generation.md](title-and-description-generation.md)) ni para una auditoría completa ([audit-scoring-and-weights.md](audit-scoring-and-weights.md)).

### Qué fuente de keywords hay
- **Lista del usuario** (Search Console, Semrush, Ahrefs, Keyword Planner o manual): lo ideal, porque trae volumen y dificultad.
- **Sin lista:** construirla con términos de títulos y H1 del sitio y con ideas de un modelo de lenguaje (sinónimos, preguntas, comparaciones, términos transaccionales, variantes por público o uso).
- **Regla:** las keywords generadas por un modelo **no tienen volumen ni dificultad**. Rotularlas "generadas por IA, sin volumen", no inventar cifras y sugerir validarlas con Keyword Planner o Search Console.
- **Sin sitio o sin la keyword en el sitio** no es un error: todos los clústeres salen como "hueco" y el entregable es la arquitectura de páginas por crear.

### Agrupar y corregir
Un agrupamiento léxico automático (normalizar minúsculas, tildes, palabras vacías y plurales; fusionar por tokens contenidos o por similitud de Jaccard, umbral inicial 0,5; pilar = la keyword de mayor volumen) **no entiende significado**. La persona corrige:

1. Fusionar sinónimos y variantes que se separaron.
2. Separar falsos amigos y clústeres con **intenciones mezcladas**: una consulta transaccional y una informativa no comparten página.
3. Confirmar la intención de cada clúster (informacional, comercial, transaccional, navegacional). Los clústeres "genéricos" son términos amplios: decidir con el contexto del negocio.
4. Pilar y apoyo: el término más amplio y de mayor volumen es el pilar; el resto son subtemas o secciones. **Una página por intención, no por keyword.**
5. Si hay duda entre fusionar y separar, **separar** y anotarlo.
6. Si el usuario aporta los 10 primeros resultados por keyword, fusionar los clústeres que comparten 3 o 4 URLs o más. Sin esos datos, no simularlos.

### Acción por clúster
| Estado | Significado | Acción |
|---|---|---|
| Cubierto | Hay una página adecuada | Optimizar la existente (title, H1, secciones para términos de apoyo) |
| Parcial | Hay algo cercano | Ampliar el contenido o rehacer la página más próxima |
| Hueco | No hay página | Crear (tipo: categoría, producto, guía, comparación o landing; slug propuesto) |
| Canibalización | Varias páginas compiten por el pilar | Elegir una canónica, consolidar o diferenciar por intención (ver "Canibalización" arriba) |

Orden de acciones: **crear, consolidar, optimizar**, según volumen × intención × esfuerzo.

### Prioridad, solo con datos reales
Alto volumen + baja dificultad + intención alineada + posición actual entre 8 y 20 (ganancia rápida). Sin volumen ni dificultad, ordenar por intención y cobertura y decirlo.

### Puntuación (solo si hay cruce con el sitio y volumen; si no, sin nota)
| Criterio | Peso | Medida |
|---|---|---|
| Cobertura | 50 % | Parte del volumen total en clústeres cubiertos (parcial cuenta 0,5) |
| Canibalización | 25 % | 100 menos 25 por clúster con páginas que compiten (mínimo 0), ponderado por volumen |
| Alineación de intención | 25 % | Parte del volumen cuya página existente coincide con la intención del clúster (revisión manual) |

Hallazgos típicos: clúster de alto volumen sin página; página transaccional que atiende una consulta informativa; dos URLs que compiten por un pilar; clústeres de una sola keyword sin potencial (descartar o fusionar).

### Entregable y límites
- Tabla del mapa: clúster (pilar), intención, acción, URL actual o propuesta, keywords de apoyo.
- Tope de unos **50 clústeres**; el resto, "cola larga" con una nota.
- Al volver a ejecutar el agrupamiento con otros parámetros se **regeneran** los clústeres: copiar antes las correcciones manuales a la tabla del mapa.
