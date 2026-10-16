---
tags:
  - seo
---

# Enlazado interno y rutas de conversión

## Índice

- Funciones
- Modelo de registro
- Anchor text
- Arquitectura
- Auditoría
- Conversión

## Funciones

Un enlace interno puede:

- Facilitar descubrimiento y rastreo.
- Explicar relaciones temáticas.
- Distribuir autoridad interna.
- Ayudar a completar una tarea.
- Guiar hacia consideración o conversión.

No agregar enlaces solo para alcanzar una cuota.

### Por qué distribuir autoridad interna importa (lógica de fondo)

Google ya no publica un valor público de PageRank, pero sigue usando indicadores de autoridad equivalentes: un enlace entrante es, en esencia, una recomendación, y esa autoridad se reparte entre los enlaces salientes de una página — más enlaces en una página, menor autoridad relativa transmitida por cada uno. Esto explica por qué la arquitectura pilar↔clúster de este archivo y del mapa temático (ver [topical-map-and-content-architecture.md](topical-map-and-content-architecture.md)) importa: concentrar enlaces relevantes hacia las páginas que sí deben posicionar, en vez de enlazar todo hacia todo, es lo que hace efectiva la distribución.

**Advertencia — técnica obsoleta a evitar:** ocultar o "enmascarar" enlaces con JavaScript como alternativa a `rel="nofollow"` (técnica de "PageRank sculpting" de la era 2008-2012) **no** es una práctica recomendada actualmente. Google rastrea y ejecuta JavaScript de forma rutinaria, por lo que no oculta nada del análisis del motor, y la intención de manipular artificialmente el reparto de autoridad por esa vía es contraria al espíritu de las directrices de enlaces de Google — puede leerse como un intento de manipulación de PageRank. Usar en su lugar los atributos que Google sí documenta oficialmente: `rel="nofollow"`, `rel="sponsored"` (enlaces pagados/afiliados) y `rel="ugc"` (contenido generado por usuarios).

## Modelo de registro

```text
URL de origen:
URL de destino:
Anchor:
Ubicación:
Relación:
Intención:
Journey:
Prioridad:
Estado:
```

## Anchor text

Describir el destino con naturalidad.

Preferir:

- conoce el proceso de diseño de marca
- guía para auditar el enlazado interno
- comparar planes de consultoría SEO

Evitar anchors genéricos cuando pierden contexto:

- haz clic aquí
- ver más
- enlace

Variar cuando el contexto lo permita, sin cambiar la promesa del destino. No repetir la keyword exacta artificialmente.

El atributo `title` del enlace es opcional; omitirlo si solo repite el anchor.

## Arquitectura

Diseñar relaciones:

- Pilar ↔ clúster.
- Servicio ↔ caso.
- Artículo ↔ servicio pertinente.
- Guía ↔ recurso práctico.
- Localización ↔ servicio disponible.
- Contenido nuevo ↔ páginas históricas.

Evitar páginas huérfanas y profundidades innecesarias.

## Auditoría

Revisar:

- Enlaces rotos.
- Redirecciones internas.
- Anchors ambiguos.
- Exceso de enlaces repetidos.
- Enlaces a páginas no indexables.
- Huérfanas.
- Canibalización de anchors.
- Enlaces que distraen del CTA principal.

## Conversión

El enlace siguiente debe corresponder al journey. Una guía temprana puede enlazar a una comparación antes del contacto. Una página de decisión debe ofrecer evidencia y una acción directa.

Medir no solo clics, sino calidad del paso:

- Continuación de sesión.
- Evento clave.
- Lead.
- Venta.
- Uso del recurso.

