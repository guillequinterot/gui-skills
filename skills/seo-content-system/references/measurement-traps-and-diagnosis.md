---
tags:
  - seo
  - medicion
  - diagnostico
---

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
