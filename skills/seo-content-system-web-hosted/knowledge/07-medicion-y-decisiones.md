<!-- GENERADO por tools/build_hosted.py desde skills/seo-content-system (v1.5.0, huella 87cfc8e82991). NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->

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



## Informe mensual [Drive]
Estructura de deck y reglas de lectura (marca vs. sin marca, pp para tasas, impresiones de bajo valor, gigantes dormidos tras una migración): `assets/templates/seo-performance-report-deck.md` y `references/drive-deliverables-and-guidelines.md` §1.


## Ampliación [ClickUp 2]: línea base, scorecard y dashboard

Las trampas de medición (`page` frente a `query` en Search Console, rompecachés, distribución del enlazado, diagnóstico de caídas) están en [measurement-traps-and-diagnosis.md](measurement-traps-and-diagnosis.md).

- **Línea base explícita** («marcar las métricas actuales») antes de cada ciclo de mejora y **scorecard** al cierre. En mejoras continuas: línea base de métricas → cinco tareas de implementación por rol → scorecard → reporte. Core Web Vitals forman parte del dashboard y de dos auditorías.
- **Dashboard (Looker Studio), especificación observada:** tráfico orgánico global; clics; impresiones; crecimiento con **línea base = fecha de publicación** de lo optimizado; comportamiento por programa o página (posiciones en la SERP); rendimiento de keywords y mejores posiciones. Feedback del cliente que conviene prever: filtro de fechas libre (no solo trimestre), filtro por programa, fuentes de tráfico, páginas más visitadas, rebote y tiempo en página, usuarios del blog, sesiones por país conectadas al filtro de fecha. **Validación obligatoria:** «métricas muy altas para ser solo tráfico orgánico» indica un error de configuración.
- **Fugas de impresiones y clics por URL** frente al **mismo mes del año anterior** (la comparación interanual evita la estacionalidad); y tráfico mes contra mes de lo optimizado, en una pestaña nueva de la matriz.
- **Informe de acciones**, secciones fijas: mejoras en CTA · acciones de enlazado interno · backlinks comprados (tabla) · banners · otras tareas, y el comportamiento por carpeta o por programa. Borrador revisado antes de enviar, con tiempos reales.
- **Informe de SEO + CRO**: mapas de calor, CTAs por tipo de página, medición de conversión con página de gracias.
- **Plan de medición de un sitio nuevo** (tabla evento · disparador · parámetros · `dataLayer.push`, sin datos personales, UTM hasta el formulario): [launch-checklist-new-site.md](launch-checklist-new-site.md).

---

## Fuente original: `measurement-traps-and-diagnosis.md`

# Trampas de medición, diagnóstico de caídas y priorización

Origen: auditorías reales de WordPress documentadas en la bóveda del mantenedor (anonimizadas) y los marcos de `03_Estrategia`, `04_Produccion` y `05_Medicion`. Complementa [analytics-search-console-and-decisions.md](analytics-search-console-and-decisions.md); no lo sustituye.

## Índice

- Principios de trabajo en una auditoría
- Trampas de Search Console y medición
- Enlazado interno: distribución, no media
- Diagnóstico de caídas
- Modelo de priorización
- Regla de bloqueo antes de publicar
- Antes de dar algo por bueno

## Principios de trabajo en una auditoría

1. **Mide, no estimes.** Si el dato no está en el rastreo, la API o el HTML en vivo, se dice «no lo sé». Nunca rellenar con cifras plausibles.
2. **Separar siempre** hecho medido · inferencia · hipótesis · recomendación. Una correlación se escribe como correlación.
3. **Respaldo antes de cada cambio** y verificación en vivo después: una API puede devolver 200 sin persistir el cambio.
4. **Registrar las no-acciones**: si se decide no tocar algo, se anota por qué.
5. **Rectificar en el propio informe**, con la cifra correcta junto a la errónea.
6. Mantener un `HANDOFF` vivo desde el primer minuto, con una fila numerada por hallazgo o cambio: nº · fecha · objetivo · qué se encontró · qué se hizo o decidió · ¿respaldo?. Los respaldos van en una carpeta de evidencia del proyecto, nunca dentro del repo de la skill.
7. Fase 0 siempre es **inventario y accesos**: confirmar qué herramientas responden de verdad (rastreador, Search Console, GA4, acceso al CMS) antes de prometer nada, y congelar un inventario de URLs desde el sitemap como fuente de verdad.

## Trampas de Search Console y medición

1. **`page` y `query` no son comparables.** Google anonimiza las consultas poco frecuentes: aparecen en la dimensión página y desaparecen al cruzar con consulta. Calcular siempre:

   ```text
   anonimizado % = 1 − (impresiones de query+page ÷ impresiones de page)
   ```

   En un caso real el hueco fue del 68 % (1.252 impresiones por página frente a 404 sumando consultas). Por encima de ~30 %, «esta página funciona por esta keyword» no es defendible. Cruzar siempre consulta + página, nunca una sola dimensión.
2. **Search Console ordena por clics** aunque se pida ordenar por impresiones. Si se limitan las filas se pierden URLs con muchas impresiones y cero clics. Comprobar que las sumas cuadran con el total.
3. **Dos diagnósticos que se confunden**:
   - *Problema de descubrimiento*: buena posición, buen engagement, pocos clics → el fragmento (title, meta, rich result).
   - *Problema de contenido*: entran y se van en segundos → el título no lo arregla.
4. **Rompecachés**: usar `?cb=<timestamp>`. Nunca `?s=` ni `?m=` en WordPress (búsqueda y archivo por mes): producen falsos 404.
5. **PageSpeed**: una sola pasada no es concluyente; mínimo tres por URL.
6. Si la keyword ya está en slug, title y H1 y la consulta sigue en la página 3, el cuello de botella no es léxico. No presentar como demostrado lo que solo es plausible.
7. **Competidores reales**: no elegirlos a priori. Sacarlos de las consultas que el sitio ya comparte y de SERP reales, y verificar en vivo que existen (a menudo el «competidor» está caído). Extraer su estructura real (title, H1, H2) y compararla.
8. **Auditoría de afirmaciones**: buscar superlativos sin sustento, promesas de resultado y datos legales incorrectos en titles, metas y copy. Comprobar que cada metadescripción corresponde al artículo que describe: el copiado-pegado entre plantillas pasa desapercibido.

## Enlazado interno: distribución, no media

- Construir el grafo **sin nav, header ni footer**, que si no lo tapan todo.
- Una media de «3 enlaces por post» puede esconder un reparto 23/23/1/0/0.
- Calcular: entrantes por URL, huérfanas, concentración máxima y cuántas URLs son alcanzables desde la home solo por enlaces de contenido.
- Si hay un bloque de «entradas relacionadas», **auditar su consulta**: sin taxonomía ni orden no relaciona nada, recicla las últimas N y concentra el enlazado en un puñado de URLs. Comprobar también si los posts tienen categorías y etiquetas reales o una sola genérica.
- Estructura de encabezados por URL: cuántos H1, saltos de nivel y cuántos H2 son de plantilla y no del contenido (el dato que casi nunca se mira y suele ser el más sucio).

## Diagnóstico de caídas

Orden de trabajo:

1. Confirmar la medición (¿cambió el tracking?).
2. Definir fecha y alcance.
3. Segmentar por canal, país, dispositivo, página y consulta.
4. Revisar cambios técnicos y editoriales en esas fechas.
5. Consultar el estado de los buscadores.
6. Evaluar estacionalidad y demanda.
7. Revisar competencia y SERP.
8. Formular hipótesis.
9. Probar correcciones.

Tipos de caída: rastreo · indexación · ranking · CTR · demanda · conversión · tracking. **No atribuir automáticamente una caída a una actualización de Google.**

## Modelo de priorización

Variables: valor de negocio, demanda o necesidad demostrable, ajuste con la propuesta, oportunidad orgánica, capacidad de diferenciación, confianza de la evidencia, esfuerzo, riesgo y mantenimiento.

```text
(valor + demanda + ajuste + oportunidad + confianza)
----------------------------------------------------
(esfuerzo + riesgo + mantenimiento)
```

Las escalas se definen por proyecto. No convertir volumen o dificultad en una decisión automática. Categorías: **Ahora** (impacto alto y base suficiente) · **Después** (útil, pero necesita datos o recursos) · **Prueba** (hipótesis con alcance controlado) · **No hacer** (utilidad o evidencia insuficiente).

Todo plan priorizado incluye una sección «qué NO recomiendo hacer» y una tabla de medición a 30-60-90 días con las líneas base de hoy.

## Regla de bloqueo antes de publicar

No publicar si una afirmación importante carece de respaldo, la intención no está clara, la página compite innecesariamente con otra o no existe plan de medición.

Flujo editorial de referencia: intake → investigación → intención y journey → brief → evidencia → arquitectura → borrador → edición lingüística → SEO on-page → QA → publicación → medición → aprendizaje.

Checklist de publicación:

- **Contenido**: responde la intención · tesis clara · sin contradicciones · fuentes que respaldan · voz y variante correctas · patrones robóticos revisados.
- **On-page**: title y metadescripción · H1 y jerarquía · slug · canonical · enlaces internos · imágenes y alt · schema visible y válido.
- **Técnico**: HTTP · indexación · sitemap · responsive · accesibilidad · rendimiento.
- **Conversión y medición**: CTA · evento · línea base · KPI · fecha de revisión · cambio documentado.

## Antes de dar algo por bueno

- ¿Lo mediste o lo supusiste?
- ¿Lo verificaste en vivo con rompecachés?
- ¿Miraste la distribución o solo la media?
- ¿Qué porcentaje de impresiones está anonimizado en esa conclusión?
- ¿Está en una plantilla del CMS y, por tanto, se revertirá?
- ¿Qué decidiste no hacer, y por qué?

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


## Ampliación [ClickUp 2]: pauta y landing, SEO + CRO y cierre real de entregas

> Evidencia parcial: lo de pauta se reconstruyó de títulos y descripciones de tareas y de hojas de copys; no de resultados medidos. La skill no gestiona campañas: esto es el punto de contacto entre SEO y pauta.

### Pauta + landing como una sola secuencia
1. **Ficha técnica de la landing** diligenciada por equipo antes de maquetar (`assets/templates/landing-technical-sheet.md`): una sola oferta, una etapa del embudo, formulario corto.
2. **Medición antes de pagar tráfico:** GA4, GTM y píxeles con eventos nombrados; parámetros UTM que llegan hasta el CRM; una *thank-you page* distinta para medir la conversión; lead de prueba que se comprueba en el CRM.
3. **Pauta de prueba** (2-3 anuncios) con revisión cada pocos días y reporte semanal después de la primera semana; **bitácora de optimizaciones** (qué se cambió, cuándo, por qué) para no aprender de una versión que ya no existe.
4. **Coherencia anuncio ↔ landing:** el ángulo del anuncio es el titular de la landing; la concordancia exacta se usa para proteger la intención; un mensaje autodescalificador evita leads que no encajan.
5. **Copys por ángulo** con un dato verificable distinto por ángulo y una línea legal única (`assets/templates/ad-copy-by-angle.csv`).
6. Tras la semana 3 se **optimiza, no se rehace**: los cambios estructurales reevalúan el alcance.

### SEO + CRO en páginas transaccionales
- Mapas de calor y grabaciones sobre un conjunto pequeño de páginas transaccionales antes de cambiar nada; una prueba A/B solo con volumen suficiente (si no lo hay, comparar antes y después y decirlo).
- CTA por tipo de página y banners de conversión y de enlazado dentro de los artículos (el CTA aparece más de una vez, con banners genéricos reutilizables).
- **Refresh de casos de éxito:** filtro por industria, tarjeta con la métrica clave, testimonio con retrato, recursos relacionados y CTA. Una **biblioteca de módulos** reutilizables es un activo de diseño y de SEO.
- Las métricas de calidad (formularios enviados, leads calificados) pesan más que las de volumen; ver `measurement-traps-and-diagnosis.md`.

### Cierre real de una entrega externa
- «En revisión» no equivale a hecho. Registrar la **fecha en que el cliente implementó** y la **re-medición** posterior; sin ella, el resultado se pierde.
- Si una entrega quedó en estado de tipo «hecho» sin que nadie la cerrara, abrir una tarea de ajustes finales y cerrar con comentario de decisión.
- Un informe de impacto compara antes y después **desde la fecha de despliegue real**, no desde la de entrega.

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
