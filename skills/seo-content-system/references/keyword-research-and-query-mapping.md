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

