---
tags:
  - seo
---

# Datos estructurados y funciones de búsqueda

## Índice

- Principio
- Selección
- Limitaciones
- Validación
- Cambios
- Lista de control

## Principio

El schema describe entidades y contenido visibles. No crea por sí solo autoridad, calidad ni derecho a un resultado enriquecido.

## Selección

Secuencia:

```text
Contenido visible
→ tipo real de entidad
→ documentación actual
→ propiedades aplicables
→ marcado
→ validación
→ seguimiento
```

Usar Schema.org para vocabulario y la documentación del buscador para compatibilidad de funciones.

## Limitaciones

- No existe un schema especial obligatorio para AI Overviews o AI Mode.
- `Article` describe autoría, fechas y publicación; no certifica E-E-A-T.
- `FAQPage` puede ser semánticamente válido aunque Google limite su rich result — **retirado por completo el 7 de mayo de 2026**, incluida la excepción que quedaba para sitios de gobierno y salud (verificado externamente, ver fuentes en [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md)). El vocabulario sigue siendo válido; lo que desaparece es el despliegue visual en Google, no la utilidad para otros sistemas.
- `HowTo` no debe prometer un rich result que ya no existe (descontinuado desde septiembre de 2023).
- `Speakable` tiene disponibilidad limitada.
- `DefinedTerm` describe conceptos; no garantiza visibilidad especial.

Verificar siempre el estado actual antes de recomendar una implementación. Para priorización de tipos orientada a GEO/citación en LLMs (Organization, Article, FAQPage, HowTo, Service, Person y la técnica `@graph`), ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).

## Validación

Comprobar:

- JSON válido.
- Tipo correcto.
- Propiedades requeridas y recomendadas.
- Coincidencia con contenido visible.
- URLs absolutas y canónicas.
- Fechas y zonas horarias.
- Identificadores consistentes.
- Ausencia de reseñas, precios o disponibilidad inventados (sin precio público: nada de `Offer` vacío ni `price` 0).
- Ningún marcador (`[PENDIENTE]`, `TBD`, `XXX`) dentro de un valor: si falta el dato, se omite el campo.
- Sin nodos duplicados con los que ya genera el plugin SEO (Rank Math: `#organization`, `#website`, `#webpage`); ver `schema-markup-for-ai-citation.md`.

Usar validadores pertinentes y revisar Search Console después del despliegue.

## Cambios

Registrar:

```text
Tipo:
Página:
Motivo:
Documentación consultada:
Fecha:
Resultado esperado:
Resultado observado:
```

No retirar marcado útil solo porque no produce una función visual, si sigue describiendo correctamente la entidad y no causa problemas.

## Lista de control

- ¿Existe contenido visible equivalente?
- ¿El tipo representa la entidad real?
- ¿La función sigue vigente?
- ¿El marcado valida?
- ¿La expectativa se comunicó sin garantías?
- ¿Se medirá el resultado?

