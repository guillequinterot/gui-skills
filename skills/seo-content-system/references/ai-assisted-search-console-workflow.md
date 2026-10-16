---
tags:
  - seo
  - automation
---

# Automatizar la detección de keywords de oportunidad con IA, GSC y CMS

## Índice

- Principio
- Estado de la evidencia
- Qué es una keyword de oportunidad
- Arquitectura del flujo
- Los 9 pasos
- Seguridad y manejo de credenciales
- Cuándo tiene sentido automatizar esto
- Errores frecuentes
- Lista de revisión

## Principio

Este archivo documenta un **patrón de automatización**, no una herramienta que la skill ejecute por sí sola. Sirve para cuando el usuario ya tiene (o va a configurar) acceso real a Google Search Console y a un CMS, y quiere usar un asistente de código (Claude Code u otro) para conectar datos de rendimiento real con generación de contenido — sin fingir ese acceso cuando no existe (principio 4 de esta skill).

La lógica de "keyword de oportunidad" ya está en `analytics-search-console-and-decisions.md` (impresiones altas + CTR bajo, posiciones ~4-20); este archivo aporta el **cómo automatizarla con datos reales vía API**, no un concepto nuevo.

## Estado de la evidencia

Caso propio de un consultor SEO (Julián Durango) documentado con código real y una cifra de ejemplo verificable dentro de su propio artículo ("que es un led": 2.755 impresiones, posición 6.8, CTR 0.2%). Es un flujo reproducible y técnicamente correcto (usa las APIs oficiales de Google y WordPress), pero es un caso de un solo operador, no un benchmark con muestra.

## Qué es una keyword de oportunidad

Consulta donde el sitio ya tiene visibilidad en Google pero no aprovecha su potencial completo:

- Posición aproximada entre 5 y 20.
- Impresiones altas con CTR bajo respecto al estándar esperado para esa posición.
- La query genera impresiones pero no tiene sección dedicada en el contenido actual (gap de contenido).

Ventaja de esta técnica: genera incrementos de tráfico sin crear contenido desde cero, aprovechando autoridad que la URL ya tiene con Google — alto ROI relativo frente a producir una página nueva.

## Arquitectura del flujo

Tres componentes conectados:

1. **Google Search Console API** — extrae datos reales de clics, impresiones, CTR y posición por URL y consulta. Fuente oficial, no estimaciones de terceros (Ahrefs/Semrush).
2. **Asistente de código** (Claude Code u otro con capacidad de ejecutar scripts) — aplica el framework de priorización sobre esos datos y redacta propuestas de contenido.
3. **API REST del CMS** (WordPress en el caso documentado) — lee el contenido actual y publica las secciones nuevas una vez aprobadas por una persona.

## Los 9 pasos

1. **Configuración inicial:** archivo de credenciales de la cuenta de servicio de GSC (JSON) + archivo `.env` con credenciales del CMS.
2. **Conexión a GSC:** autenticación y listado de sitios disponibles para confirmar acceso.
3. **Análisis de URLs:** extraer las páginas con más clics/impresiones en un rango reciente (p. ej. últimos 4 meses).
4. **Análisis de keywords por URL:** para la URL seleccionada, extraer las consultas específicas que generan impresiones.
5. **Detección de oportunidades:** aplicar el framework — posición 5-20, alto volumen de impresiones con bajo CTR, gaps de contenido (queries sin sección dedicada).
6. **Conexión al CMS:** verificar credenciales y obtener el contenido actual del artículo objetivo.
7. **Análisis de contenido:** extraer encabezados (H2/H3) existentes y contrastarlos contra las keywords de oportunidad para ver qué falta.
8. **Generación de contenido:** proponer nuevas secciones que respondan las queries detectadas, amplíen cobertura semántica sin canibalizar la keyword principal, e incluyan FAQs.
9. **Aprobación humana y publicación:** mostrar la propuesta para revisión antes de publicar vía API — nunca publicar de forma automática sin ese punto de control.

El paso 9 no es opcional: es la salvaguarda editorial que evita que un flujo automatizado publique contenido sin supervisión.

## Seguridad y manejo de credenciales

Aplican los mismos principios que `update-governance-and-research.md` ya fija para investigación automatizada, extendidos aquí a un flujo con capacidad de publicar:

- La cuenta de servicio de Google debe tener el **scope mínimo necesario** (lectura de Search Console, no permisos amplios de la cuenta de Google Cloud).
- Las credenciales (JSON de la cuenta de servicio, Application Password de WordPress) van en archivos fuera de control de versiones (`.gitignore`) — nunca en el repositorio, nunca en un documento del vault, nunca pegadas en el chat.
- Application Passwords de WordPress deben crearse con un nombre descriptivo y alcance identificable, para poder revocarlas de forma aislada si es necesario.
- Nunca automatizar el paso de publicación sin aprobación humana intermedia (paso 9).
- Si el usuario no tiene ya configurado este acceso, no simular que existe — ofrecer el patrón como algo a implementar, no como algo ya operativo.

## Cuándo tiene sentido automatizar esto

- El sitio tiene volumen suficiente de URLs y consultas en Search Console para que la revisión manual sea el cuello de botella (no tiene sentido para sitios con muy poco tráfico).
- Existe ya acceso de API a GSC y al CMS, o el cliente está dispuesto a configurarlo.
- El equipo mantiene el paso de aprobación humana como parte real del flujo editorial, no como formalidad que se salta.
- Se repite el mismo análisis para muchas URLs — el valor crece con la escala.

No sustituye investigación de intención, arquitectura de mapa temático (ver `topical-map-and-content-architecture.md`) ni criterio editorial: opera sobre contenido que ya existe, ampliándolo, no reemplaza la planificación previa.

## Errores frecuentes

- Publicar directamente sin revisión humana del contenido generado.
- Usar credenciales con permisos más amplios de los necesarios.
- Tratar la cifra de ejemplo de un caso propio como benchmark generalizable.
- Ampliar una sección con keywords de oportunidad sin verificar que no canibaliza la keyword principal del artículo.
- Ejecutar el flujo sobre URLs sin suficiente volumen de datos en Search Console para que el análisis sea confiable.

## Lista de revisión

- ¿Las credenciales están fuera de control de versiones y con scope mínimo?
- ¿Existe un paso de aprobación humana antes de publicar?
- ¿Se verificó que las nuevas secciones no canibalizan la keyword principal?
- ¿El análisis se basa en datos reales de Search Console, no en estimaciones de terceros?
- ¿Se documentó qué URLs y qué periodo se analizaron?

Fuentes primarias: [Palabras clave de oportunidad con IA y GSC](https://juliandurango.com/blog/palabras-clave-oportunidad/) (14 de octubre de 2025) y [Automatizar SEO con Claude Code y Search Console](https://juliandurango.com/blog/automatizar-seo-claude-code/) (6 de febrero de 2026) — Julián Durango.
