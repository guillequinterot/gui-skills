---
tags:
  - seo
  - lanzamiento
  - tecnico
---

# Lanzamiento de un sitio nuevo: checklist, medición y secuencia [ClickUp 2]

Origen: el plan de lanzamiento de un sitio de donaciones en React (proyecto vivo, 7 días), el SEO mínimo de un sitio estático para un hito, y las plantillas GDD (anonimizado). La checklist de 12 secciones es la más completa del conjunto; el resto es evidencia de tareas reales. Complementa [migration-redirects-and-validation.md](migration-redirects-and-validation.md) (que cubre migrar un sitio existente) y [growth-driven-design-gdd.md](growth-driven-design-gdd.md).

## Índice

- Decisión de render antes del prototipo
- Reparto de roles y secuencia fechada
- Checklist de 12 secciones
- Plan de medición
- MVP estático para un hito
- Auditoría en stage antes del lanzamiento
- Contenido de recaudación y YMYL ligero

## Decisión de render antes del prototipo

Un sitio React sin renderizado en servidor indexa mal. Antes de avanzar el prototipo, **validar con desarrollo cómo llega el HTML al buscador**: prerender o exportación estática, URLs reales sin `#`, title, meta, canonical y Open Graph por página, generación de robots y sitemap. Si el cliente pide una home por perfiles **sin menú ni pie**, exigir páginas agrupadoras y enlaces en el cuerpo: sin ellos se pierde enlazado interno y rastreo (inferencia, no documentada en las tareas).

## Reparto de roles y secuencia fechada

Separar y declarar en cada tarea quién lleva qué: **SEO de contenido** (keywords, textos, metas, alt) ≠ **SEO técnico y analítica** (especificación, medición, QA).

Secuencia de referencia, con dependencias:

1. Referentes (4-5 sitios comparables) y arquitectura (mapa, secciones del home en orden, flujo, wireframe de baja fidelidad).
2. Keyword research.
3. Textos por sección. **El texto bloquea al diseño**: con plazo fijo antes del mediodía, el diseño arranca esa tarde.
4. Metas, Open Graph y alt.
5. Prototipo → revisión interna → entrega al cliente → ajustes de texto → QA → salida.
6. Revisión a los 7 días.

Línea técnica en paralelo: validar el render (arriba) → especificación de URLs y SEO técnico → crear GTM/GA4/GSC (idealmente en una cuenta del **cliente**, con administración para la agencia; confirmar antes de crear en una propia) → plan de medición → implementar y validar en el build de producción → probar eventos → rendimiento, móvil y cookies → checklist integrador alineado con diseño, desarrollo y quien despliega → GSC (verificar por DNS, enviar sitemap, solicitar indexación) → QA del día de salida → revisión a 7 días.

Plantilla de tarea para un proyecto nuevo: `## Contexto` (marco, fechas clave, reparto) · `## Qué hacer` · `## Entregable` (qué, dónde y a quién se etiqueta) · `## Importante` (restricciones, p. ej. sin datos personales a analítica) · `## Dudas` (ruta de escalamiento).

## Checklist de 12 secciones

Marcar cada punto ✔ listo / ✖ falta / N/A, con **responsable y fecha** para cada pendiente.

1. **Render e indexación.** HTML renderizado por prerender o generación estática, validado con «ver código fuente» y **no con el inspector**. La inspección de URL de Search Console o la prueba de resultados enriquecidos muestra el contenido completo. Entorno de pruebas bloqueado (noindex o contraseña). **Quitar el noindex de producción el día de salida** (el error más común: verificar dos veces). Nada importante depende de clic o scroll.
2. **URLs, estados y redirecciones.** Slugs en minúscula con guiones, sin `#` ni parámetros; una sola versión del dominio (http→https, www ↔ no www, 301); barra final consistente; **404 real y no soft-404** (en una SPA todo suele responder 200); sin cadenas ni bucles; enlaces internos a la URL final.
3. **robots.txt, sitemap y canonical.** robots en la raíz que permite rastrear y declara el sitemap, sin bloquear CSS/JS del render; sitemap solo con URLs indexables 200, canónicas y https; canonical autorreferenciado; `lang` correcto y UTF-8.
4. **Metadatos y encabezados.** Title único de 50-60 caracteres con keyword; meta description única de 140-160; un H1; jerarquía sin saltos; Open Graph (`og:image` 1200×630) y Twitter Cards con prueba de enlace compartido en WhatsApp, LinkedIn y Facebook; favicon y apple-touch-icon. (Los rangos son por defecto: el cliente puede fijar los suyos; ver [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md).)
5. **Datos estructurados JSON-LD.** Organización, WebSite y FAQPage solo si las preguntas son visibles; validados en la prueba de resultados enriquecidos y en el validador de schema.org. Sin marcadores en campos (ver principio 20 de `SKILL.md`).
6. **Rendimiento.** PageSpeed móvil ≥ 80, LCP < 2,5 s, CLS < 0,1, INP < 200 ms; WebP/AVIF con `width`/`height` y carga diferida salvo el hero; video del hero con póster, carga diferida y sin audio automático; `font-display: swap` y fuentes precargadas; build minificado con división de código; gzip/brotli y caché de estáticos.
7. **Móvil, accesibilidad e imágenes.** Formulario usable en móvil (teclados correctos, botones ≥ 44 px); `alt` en todas las imágenes, con aclaración cuando son fotos de proyectos anteriores; contraste según el manual de marca; nombres de archivo descriptivos.
8. **Seguridad y servidor.** SSL válido sin contenido mixto; HSTS, `X-Content-Type-Options`, `Referrer-Policy`; formulario por https sin datos personales en la URL; las rutas funcionan al entrar directo o recargar; copia de seguridad o plan de reversión.
9. **Analítica.** GTM en `head` y `body` con contenedor publicado; **`page_view` en cada cambio de ruta** (disparador por cambio de historial); eventos probados en DebugView; conversiones marcadas; **ningún dato personal a analítica**; tráfico interno excluido; retención de datos 14 meses; **UTM conservados hasta el formulario** para el CRM; píxeles del cliente; modo de consentimiento conectado al aviso de cookies; accesos (administración para agencia y cliente, edición para pauta).
10. **Legal y confianza.** Aviso de cookies enlazado a la política de datos del titular; documentos legales del titular enlazados en formulario y pie (verificar que no se enlace a una organización ajena que un correo de referencia mencione); casilla obligatoria de aceptación.
11. **Día de salida.** Quitar noindex y revisar robots en producción; verificar GSC por DNS, enviar sitemap, solicitar indexación de la home y las páginas clave; vincular GSC con GA4; probar el formulario de punta a punta y que el evento llegue a GA4; revisar enlaces rotos con un rastreador; avisar en el canal.
12. **A los 7 días.** Cobertura de indexación y errores en GSC; los eventos y conversiones siguen llegando; Core Web Vitals con datos de campo (tardan unos 28 días en reflejar cambios: comparar también con laboratorio y TTFB); reporte corto.

## Plan de medición

Tabla **evento · disparador · parámetros · ejemplo de `dataLayer.push`**. Ejemplo de eventos para un sitio de donaciones: `page_view` por ruta; `clic_donar` (con sección); `inicio_formulario`; `envio_formulario` (con campo «requiere certificado», **sin datos personales**); `donacion_completada` (cuando exista la pasarela); `descarga_documento_legal`; `clic_whatsapp`; `scroll_etapas`. Conversiones = envío y donación. Conservar UTM y preguntar al cliente qué píxeles y scripts de CRM necesita.

## MVP estático para un hito

Cuando el SEO «no es prioridad todavía» pero hay una fecha dura (p. ej. una feria), el mínimo del lanzamiento es: sitemap generado por la integración del framework con el **dominio final** en la configuración; robots permisivo con puntero al sitemap; **entorno de pruebas bloqueado**; medición lista (GA4, GTM, GSC por DNS TXT, en cuenta del cliente); consentimiento de cookies (Consent Mode) si habrá tráfico europeo. Al estar arriba, enviar el sitemap en Search Console. Lo demás se pospone. Arquitectura de las páginas del MVP con módulos definidos **antes** del prototipo («desbloquea el montaje de módulos y después la redacción»).

## Auditoría en stage antes del lanzamiento

Cuando el sitio se construye por etapas (GDD) o se rediseña, auditar el entorno de pruebas **en tres frentes** antes de lanzar: SEO (metadatos, encabezados, URLs, redirecciones, sitemap, schema), UX (navegación, formularios, móvil, accesibilidad) y Front (rendimiento, errores de consola, responsive). Incluir la verificación de que **las herramientas de analítica están conectadas**. Preparar el prototipo para desarrollo con imágenes **nombradas con keywords desde el diseño** y exportadas por página.

## Contenido de recaudación y YMYL ligero

- No inventar cifras, testimonios ni beneficios tributarios. Dejar `[PENDIENTE: …]` en el borrador (nunca en producción ni en schema) y marcar las cifras oficiales como «por validar».
- Textos por sección: hero, contador de meta e hitos, **qué pasa después de donar** (4 etapas: qué pasa, quién lo hace, qué desbloquea el dinero), nosotros, microcopy del formulario, FAQ, pie.
- Fotos de proyectos anteriores con pie de foto que lo aclare, también en el `alt`.
- Keywords de ejemplo por intención: «donar + lugar», «reconstrucción + lugar», «ayuda + evento».
