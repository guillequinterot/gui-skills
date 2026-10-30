---
tags:
  - seo
  - audit
---

# Auditoría SEO con puntuación: categorías, pesos y hallazgos

## Índice

- Para qué sirve y cuándo se usa
- Estado de la evidencia
- Flujo de una auditoría general
- Categorías y pesos
- Cómo se puntúa
- Cómo se escribe un hallazgo
- Acciones: cuatro niveles
- Reglas que no se saltan
- Lista de revisión

## Para qué sirve y cuándo se usa

Una auditoría general de dominio o de un grupo de páginas ("auditoría SEO", "por qué no posiciono", "chequeo de salud") necesita dos cosas que [technical-audit-by-finding.md](technical-audit-by-finding.md) no define: **una puntuación comparable entre auditorías** y **un orden de prioridades**. Este archivo aporta ese modelo. Diagnostica y prioriza; no implementa cambios salvo que se pida (entonces se pasa a modo prescriptivo: pasos concretos, no consejos generales).

La puntuación es una herramienta de comunicación, no un resultado de Google. Un 82 no significa que Google puntúe 82: significa "en las categorías que revisamos, con esta evidencia, perdimos 18 puntos por estos hallazgos".

## Estado de la evidencia

Modelo tomado de la skill `basic-audit` de SEO Skills (Jorge Jaramillo, `github.com/jorgejaramillo/seoskills`) y de las páginas de `seo-skills.com`, consultadas el 2026-10-30. El repositorio no declara licencia: aquí **se reformula la metodología con palabras propias** y no se copian sus textos. Los pesos y las deducciones son criterio de su autor, no un estándar de la industria: tratarlos como **valores iniciales** y ajustarlos con casos reales. La regla del cliente manda sobre estos valores.

## Flujo de una auditoría general

1. **Datos.** Sitio con mucho JavaScript → HTML renderizado (ver [rendered-html-crawl.md](rendered-html-crawl.md)). Sitio estático o WordPress → extracción por HTTP. Muestra: la home más 3 a 5 páginas por plantilla (categoría, producto, artículo, servicio). Si la muestra es pequeña, decirlo ("30 de 1.200 URLs").
2. **Métricas con script o con herramienta de rastreo** (títulos, descripciones, H1, canonical, noindex, enlaces, imágenes). robots.txt y sitemap se revisan con [robots-txt-audit-and-generation.md](robots-txt-audit-and-generation.md).
3. **Análisis humano de lo que ningún script juzga:** intención de búsqueda, calidad del contenido, E-E-A-T, coherencia entre title, H1 y contenido.
4. **Core Web Vitals:** solo si hay datos (PageSpeed Insights o datos de campo) o el sitio es lento; si no, marcar "no evaluado".
5. **Títulos fuera de rango o duplicados, descripciones ausentes, cortas, largas o repetidas:** se reescriben con el procedimiento de [title-and-description-generation.md](title-and-description-generation.md), no a mano y a ojo.
6. **Informe completo:** sumar enlazado interno ([internal-linking-and-conversion-paths.md](internal-linking-and-conversion-paths.md)) e imágenes ([image-seo-and-accessibility.md](image-seo-and-accessibility.md)) sobre los mismos datos.

**Regla de herramienta:** un lector de páginas que convierte HTML a texto o Markdown pierde `title`, `meta`, `canonical`, Open Graph, `hreflang`, `alt`, `loading` y `srcset`. Para auditar el `<head>` y los atributos se usa el HTML real (extractor, rastreador o "ver código fuente"), nunca un resumen de la página.

## Categorías y pesos

| Categoría | Peso | Qué mira |
|---|---|---|
| Rastreo e indexación | 30 % | robots.txt, sitemap, canonicals que apuntan a sí mismas, noindex, cadenas de redirección, profundidad de clic |
| Técnico | 25 % | HTTPS, viewport, `lang`, TTFB, Core Web Vitals (si hay datos), JSON-LD válido, HTML inicial frente a HTML renderizado |
| On-page | 20 % | title único (30 a 60 caracteres como rango de auditoría), descripción (70 a 160), un solo H1, jerarquía H2/H3, Open Graph, `alt`, enlaces internos |
| Contenido y E-E-A-T | 15 % | contenido delgado (menos de 300 palabras en páginas clave), intención, credenciales del autor (crítico en YMYL), páginas "quiénes somos" y contacto, fechas |
| Autoridad | 10 % | solo con datos de Search Console, Ahrefs o Semrush; sin ellos, fuera de alcance |

Los rangos de title y descripción de esta tabla son **rangos de auditoría** (para detectar lo que está claramente mal). Los rangos de **redacción** son otros y están en [title-and-description-generation.md](title-and-description-generation.md).

Si una categoría queda fuera de alcance (por ejemplo, Autoridad sin datos), se **redistribuye su peso proporcionalmente** entre las demás y se dice en el resumen.

## Cómo se puntúa

1. Cada categoría empieza en 100 y pierde puntos por hallazgo según su gravedad:

| Gravedad | Deducción |
|---|---|
| Crítica | 15 a 30 |
| Alta | 8 a 12 |
| Media | 4 a 6 |
| Baja | 1 a 3 |

2. La deducción se **multiplica por la confianza** en el hallazgo: alta ×1, media ×0,5, baja ×0,25. Un hallazgo que se sospecha pero no se pudo comprobar pesa poco; uno medido en todas las URLs pesa completo.
3. La puntuación global es la suma ponderada de las categorías.
4. **Un puntaje alto con un hallazgo crítico abierto no es válido:** el crítico se menciona siempre en el resumen, aunque la nota sea 90.
5. Bandas: 90 o más, excelente · 75 a 89, buena · 60 a 74, mejorable · 40 a 59, deficiente · menos de 40, crítica.

Cuando una auditoría se repite, comparar siempre con la misma tabla de pesos; si se cambian, dejar escrito qué se cambió y por qué.

## Cómo se escribe un hallazgo

Cada hallazgo lleva cinco cosas:

1. **Gravedad** (crítica, alta, media, baja).
2. **Título de una frase.**
3. **Evidencia concreta:** URL más el dato observado ("`/servicios/x` devuelve 302 a `/servicios/x/`", no "hay redirecciones raras").
4. **Por qué importa.**
5. **Recomendación** accionable ("quitar el `noindex` de la plantilla del blog"), no vaga ("mejorar el SEO").

No se declara que falta un elemento (title, canonical, alt…) sin haberlo verificado en los datos extraídos. No se inventan métricas de tráfico, posiciones ni Core Web Vitals: si no hay dato, se escribe "no evaluado".

## Acciones: cuatro niveles

| Nivel | Qué entra |
|---|---|
| Bloqueos críticos | Lo que impide rastrear, indexar o que la página funcione |
| Alto impacto | Cambios que mueven la puntuación o el tráfico con esfuerzo razonable |
| Ganancias rápidas | Impacto medio con esfuerzo bajo (plantillas, metadatos, alt) |
| Largo plazo | Contenido nuevo, arquitectura, autoridad |

Cada acción lleva **impacto** y **esfuerzo** (alto, medio o bajo). Para convertirlas en tareas con criterio de hecho y responsable, usar [technical-audit-by-finding.md](technical-audit-by-finding.md); aquel archivo trata la gestión de cada hallazgo, este trata cómo se descubre, se puntúa y se prioriza.

## Reglas que no se saltan

- Verificar antes de afirmar que algo falta.
- Sin datos no hay métrica: "no evaluado" es una respuesta válida.
- Si el usuario pide implementar, cambiar a pasos concretos ("corregir X en Y"), no a recomendaciones generales.
- La regla del cliente (longitudes, escalas de prioridad) manda sobre los valores por defecto.

## Lista de revisión

- ¿La muestra incluye todas las plantillas y se dijo su tamaño?
- ¿Cada hallazgo tiene URL, dato observado, motivo y recomendación?
- ¿Las deducciones llevan el multiplicador de confianza?
- ¿Se redistribuyó el peso de las categorías sin datos y se avisó?
- ¿Algún crítico abierto quedó fuera del resumen?
- ¿Las acciones están en los cuatro niveles con impacto y esfuerzo?

Fuente: SEO Skills, skill `basic-audit` (Jorge Jaramillo), https://github.com/jorgejaramillo/seoskills, consultada el 2026-10-30.
