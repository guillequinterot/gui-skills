---
tags:
  - seo
---

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
