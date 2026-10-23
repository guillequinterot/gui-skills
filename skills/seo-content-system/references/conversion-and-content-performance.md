---
tags:
  - seo
---

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
