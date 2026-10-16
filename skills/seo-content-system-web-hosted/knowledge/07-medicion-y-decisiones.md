<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.2.0, huella 242e6ea43c15). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

# Medición, Search Console y decisiones

Cómo leer Search Console, GA4 y Clarity, diagnosticar señales, diseñar experimentos, y el patrón de automatización de keywords de oportunidad vía IA + GSC + CMS (para cuando exista un puente de Google Sheets).

---

## Fuente original: `analytics-search-console-and-decisions.md`

# Analytics, Search Console y decisiones

## Índice

- Roles
- Search Console
- GA4
- Clarity
- Diagnósticos
- Experimentos
- Informe

## Roles

- Search Console: cómo aparece el sitio en Google.
- GA4: qué ocurre después de la visita.
- Clarity o evidencia UX: cómo interactúan algunas personas.
- CRM/ventas: calidad y valor real.

No sustituir una fuente por otra.

## Search Console

Analizar:

- Clics.
- Impresiones.
- CTR.
- Posición media.
- Consultas.
- Páginas.
- País.
- Dispositivo.
- Apariencia.
- Indexación.
- Sitemaps.

Oportunidades:

- Impresiones altas y CTR bajo.
- Posiciones aproximadas 4–20.
- Nuevas consultas pertinentes.
- Pérdida sostenida.
- Canibalización.
- Páginas no indexadas.
- Diferencias por país o dispositivo.

Para automatizar la detección de estas oportunidades y su conexión con generación/publicación de contenido (con IA + API de GSC + CMS), ver [ai-assisted-search-console-workflow.md](ai-assisted-search-console-workflow.md) — incluye el punto de aprobación humana obligatorio antes de publicar. Para la frecuencia recomendada de esta minería de oportunidad frente a una investigación fundacional completa, ver [keyword-research-cadence-and-triggers.md](keyword-research-cadence-and-triggers.md).

## GA4

Revisar:

- Landing pages orgánicas.
- Sesiones y usuarios.
- Interacción.
- Tiempo de interacción.
- Eventos clave.
- Formularios, llamadas, ventas o registros.
- Rutas.
- Dispositivo y geografía.

Confirmar configuración antes de interpretar.

## Clarity

Usar mapas, grabaciones agregadas y señales de fricción como evidencia complementaria. No asumir intención psicológica a partir de un clic o scroll.

## Diagnósticos

| Señal | Hipótesis | Comprobación |
|---|---|---|
| Impresiones suben, clics no | SERP, CTR o intención | Consultas, titles, features |
| Tráfico estable, leads bajan | Conversión o calidad | GA4, CRM, formularios |
| Posición baja tras despliegue | Cambio técnico o contenido | Diff, logs, indexación |
| Caída general | Update, estacionalidad o sitio | Dashboard, periodos, segmentos |

## Experimentos

Registrar:

```text
Hipótesis:
Cambio:
URLs:
Fecha:
Métrica primaria:
Guardrails:
Periodo:
Resultado:
Decisión:
```

No atribuir causalidad a un antes/después sin controlar cambios relevantes.

## Informe

Separar:

- Hallazgo.
- Evidencia.
- Interpretación.
- Confianza.
- Acción.
- Responsable.
- Fecha de revisión.

---

## Fuente original: `conversion-and-content-performance.md`

# Conversión y rendimiento del contenido

## Índice

- Conversión por journey
- Microconversiones
- CTA
- Fricción
- Métricas
- Decisiones

## Conversión por journey

No exigir la misma conversión a todas las páginas.

| Journey | Resultado útil |
|---|---|
| Atracción | Comprensión, descubrimiento, siguiente lectura |
| Consideración | Comparación, caso, servicio, registro |
| Decisión | Lead, compra, reserva, contacto |
| Fidelización | Adopción, soporte, renovación, recomendación |

## Microconversiones

Definir solo si representan progreso:

- Ver un caso relevante.
- Usar una calculadora.
- Descargar un recurso.
- Iniciar formulario.
- Copiar contacto.
- Consultar disponibilidad.

No celebrar métricas de interacción desconectadas del objetivo.

## CTA

Un CTA debe indicar:

- Acción.
- Resultado.
- Nivel de compromiso.
- Destino.

Ejemplo:

> Compara los planes y elige el alcance que necesitas.

No usar urgencia o escasez sin fundamento.

## Fricción

Revisar:

- Promesa distinta entre SERP y página.
- Formularios excesivos.
- Información de precio o proceso ausente.
- CTA oculto.
- Pruebas poco creíbles.
- Navegación confusa.
- Rendimiento móvil.
- Accesibilidad.

## Métricas

Combinar:

- Visibilidad.
- Calidad de la visita.
- Acción.
- Calidad del lead.
- Resultado comercial.

Definir denominadores y ventanas. Una tasa sin volumen puede engañar.

## Decisiones

Priorizar cambios con:

```text
Impacto esperado × confianza × alcance
---------------------------------------
esfuerzo + riesgo
```

Documentar qué se cambió para no aprender de una versión inexistente.

---

## Fuente original: `ai-assisted-search-console-workflow.md`

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
