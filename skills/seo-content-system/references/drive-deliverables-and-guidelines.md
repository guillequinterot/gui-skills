# Entregables, lineamientos y presentaciones del equipo [Drive]

Este documento reconstruye la estructura y la metodología de los Docs, Slides y .xlsx del Drive del equipo. Se leyeron en modo de solo lectura el 2026-10-23. No incluye datos de clientes: los nombres, dominios, cifras, personas y montos se sustituyeron por marcadores `{…}`.

## 1. Informe mensual de rendimiento SEO (deck)
Plantilla: `assets/templates/seo-performance-report-deck.md`.

**Orden de las diapositivas.** Se repite por cada propiedad o país, con una portada de sección para cada uno:
1. **Portada.** Título del informe, mes, propiedades analizadas, fuentes y periodos comparados (GSC mes vs. mes anterior; GA4 trimestre vs. mismo trimestre del año anterior y mes vs. mes) y "preparado por / fecha".
2. **Resumen GSC.** Cuatro KPI grandes: Clics, Impresiones, CTR promedio y Posición promedio.
3. **GA4, canal Organic Search.** Ocho tarjetas: Sesiones, Usuarios, Usuarios nuevos, Interacción %, Páginas vistas, Sesiones con interacción, Eventos clave y Peso orgánico (sesiones orgánicas sobre totales). Cada tarjeta muestra el valor, la variación % o pp y el valor del mes anterior. El pie lleva las definiciones de cada métrica.
4. **Evolución mensual** (4 meses) de las cuatro métricas GSC. Los meses incompletos llevan asterisco.
5. **Mes vs. mes anterior.** Los KPI con su variación y 3 viñetas que *explican la causa*: qué URL o consulta movió el total, marca frente a sin marca, y contenido nuevo.
6. **Top 10 páginas de alto impacto.** Columnas: # · Página · Clics act/ant · Var. · Impr. act/ant · CTR act/ant · Pos. act/ant. Las páginas nuevas se etiquetan "Nuevo". Debajo va una frase de lectura, por ejemplo "las 10 suman X % de los clics".
7. **Top 10 consultas sin marca** y **Top 10 consultas de marca**, con las mismas columnas. Al pie se ponen los totales de marca y de sin marca y la advertencia "Google oculta consultas poco frecuentes".
8. **Consultas de marca, serie de 6 meses.** Una tabla de clics e impresiones y otra de CTR y posición.
9. **Top 10 contenidos del blog** y la lección editorial del mes. Un ejemplo típico: los títulos con el año anterior caen y los que llevan el año vigente entran al top.
10. **Conclusiones generales.** Entre 4 y 5 viñetas por propiedad, con números y causa.
11. **Cierre.**

**Reglas:**
- Cada diapositiva lleva un *titular-conclusión* (por ejemplo "La Home crece X % y suma Y % de los clics"), no un título genérico.
- Separar siempre marca de sin marca.
- Explicar las caídas de impresiones de bajo valor antes de alarmar: si los clics se mantienen y el CTR sube, es ruido.
- Las variaciones de tasas se expresan en pp, no en %.
- La posición se interpreta como "menor es mejor".
- Pie de página uniforme con agencia, cliente e informe.

**Variante post-migración** (deck "Rendimiento orgánico"):
- Mostrar el desplome del dominio antiguo como *confirmación* de que Google procesó los 301, no como penalización.
- Identificar las URL que concentran el tráfico, porque su redirección es crítica.
- Detectar "gigantes dormidos": muchas impresiones, posición 8–10 y CTR bajo. Se priorizan para reescribir el title y la meta.
- Mover el seguimiento a la nueva propiedad de GSC.

## 2. Acta de revisión de auditoría
Plantilla: `assets/templates/audit-review-minutes.md`.
- Contenido: tema y fecha, hallazgos agrupados (técnicos on-page · duplicados y URL · indexación · game plan y contenidos), acciones por parte con responsable y "observación para próximas reuniones".
- Expectativa que se comunica al cliente: los resultados se ven en 2–3 meses.

**Memoria de sprint semanal:**
- Encabezado: reunión, fecha y hora con zona horaria, participantes por parte.
- Secciones numeradas:
  1. Accesos y pendientes del cliente.
  2. Contenido SEO (game plan nuevo, artículos listos para revisión, entrevista con experto, páginas nuevas a priorizar Alta/Media/Baja).
  3. Otros frentes, como email o CRO.
  4. Métricas del mes (Leads · Oportunidades · Cerradas · Lead-to-sale · MRR).
  5. Mejoras de conversión.
- Cada punto termina en *quién hace qué y cuándo*. Un bloqueo del cliente ("sin el documento, la página queda en espera") se escribe de forma explícita.

## 3. Lineamientos de SEO técnico (documento marco)
Plantilla: `assets/templates/technical-seo-guidelines.md`. Complementa `technical-seo-lineamientos-generales.md`.

Es un documento genérico que se entrega al equipo de desarrollo de cualquier sitio. Contiene 7 bloques:
1. **URL y arquitectura:**
   - Solo `a-z 0-9 -`. Sin mayúsculas, `_`, espacios, tildes, ñ ni símbolos.
   - Longitud de 75–80 caracteres o menos y sin stop words.
   - Enlaces con `<a href>` real (nunca `onclick` ni `javascript:void(0)`).
   - Pirámide de 3–4 niveles. Tabla "estándar vs. mala práctica".
2. **Canonical y servidor:**
   - Canonical absoluta con HTTPS.
   - 301 de HTTP a HTTPS y de no-www a www (una versión maestra), y 301 cuando una ruta cambia.
   - Sin contenido mixto.
   - Parámetros de filtros y búsqueda bajo control con robots o canonical, para no gastar crawl budget.
3. **hreflang:** recíproco, ISO 639-1 más ISO 3166-1, `x-default`, en el `<head>` o en el sitemap.
4. **Home:**
   - Title de 50–60 caracteres (marca y propuesta de valor). Meta de 140–155 caracteres.
   - `robots index,follow,max-image-preview:large`.
   - HTML5 semántico (`header/nav/main/section/article/footer`), menú en `<nav><ul><li><a>` y un solo H1.
   - Open Graph y Twitter Cards.
   - JSON-LD `@graph` Organization más WebSite con SearchAction.
5. **Ficha o PDP:**
   - Title con el patrón `Producto - Variante | Marca`. El H1 es igual al nombre oficial.
   - Imágenes: hero de 100 KB o menos (tope unificado en la v1.3.0), contenido de 70–100 KB o menos, miniaturas de 30 KB o menos.
   - Formato WebP o AVIF, alt descriptivo y `width`/`height` explícitos.
   - Hero con `loading="eager" fetchpriority="high"`; el resto con `loading="lazy" decoding="async"`.
   - JSON-LD Product (Brand, Offer, AggregateRating). `Offer` solo con precio real publicado y `AggregateRating` solo con reseñas reales visibles; sin precio público, no usar `Offer` (para software, solo `SoftwareApplication`). Si el plugin SEO ya genera Organization/WebSite, no duplicarlos a mano.
6. **Rendimiento:**
   - SSR o SSG en frameworks de JavaScript.
   - Metas de Core Web Vitals: LCP < 2,5 s, INP < 200 ms, CLS < 0,1.
   - Minificar y usar `defer`/`async`.
   - Cache-Control y CDN.
   - Sin interstitials intrusivos en móvil.
7. **Rich results y checklist final:**
   - Schemas: FAQPage, BreadcrumbList, Article/BlogPosting y VideoObject.
   - Matriz de auditoría con columnas *Categoría · Ítem · Requisito aceptable*. Categorías: Indexabilidad y servidor, Meta y contenido, Seguimiento (GSC/GA4/GTM), Rendimiento, HTML5 y Datos estructurados.

> Nota: los rich results de FAQPage están restringidos por Google. Se mantiene el marcado por su valor semántico y para IA (ver `schema-markup-for-ai-citation.md`).

**Matriz de insumos de producto para e-commerce o migración:**
- Columnas: Marca · Categoría · Tipo · SKU · Nombre · Tamaño/talla · Color · Ingredientes/atributos · Beneficios · Necesidad · Claim (clínico/dermatológico) · Etiquetas · Descripción · Carpeta de imágenes (mínimo 4 por producto) · Formato de foto · Productos relacionados.
- Regla de fotos: mismo tamaño, 100 KB o menos, WebP, nombre en minúsculas con guiones y sin caracteres especiales.

## 4. Propuesta de optimización de FAQs
Plantilla: `assets/templates/faq-optimization-proposal.md`.
- Un documento con un bloque por URL (encabezado de página más URL) y las preguntas numeradas en H2 con su respuesta.
- La Home lleva las preguntas de decisión: costo de inscripción, ventajas, becas, financiación, reconocimiento, calidad, investigación, alianzas, docentes, empleabilidad, internacionalización e impacto regional.
- Las preguntas operativas (inducción, pagos, horarios) se reubican en su página de servicio.
- Las respuestas se escriben en 2–4 frases y empiezan con "Sí/No" cuando aplica.
- La entidad se nombra completa en la primera mención.
- No se prometen cifras que no estén verificadas.

## 5. Propuesta técnica comercial (deck)
Plantilla: `assets/templates/technical-proposal-deck.md`. El caso de referencia es la desindexación de PDFs; ver `deindexing-procedure.md`.

**Secuencia:**
Portada → Contexto con KPI → Por qué importa (legal, fraude, marca) → Cómo funciona Google (rastrea, indexa, muestra) → Solución, con una tabla de herramientas oficiales (*Herramienta · Para qué sirve · Alcance y límites*) → Objetivo → Plan en pasos → Cronograma → Protocolo de prevención → Entregables → Insumos requeridos → Inversión y forma de pago → Siguiente paso.

**Plan técnico de desindexación en 7 pasos:**
1. Inventario.
2. Infraestructura.
3. Configuración de `X-Robots-Tag: noindex` en la cabecera HTTP. No se usa robots.txt, porque bloquear impide que Google vea el noindex.
4. Piloto con una muestra pequeña.
5. Implementación.
6. Retiradas temporales en GSC.
7. Monitoreo con la URL Inspection API.

**Prevención:** archivar los documentos en carpetas `/documentos/{tipo}/{año}/` con noindex heredado por carpeta.

## 6. Guía de entrevista a experto y gameplan por programa
Plantilla: `assets/templates/sme-interview-guide.md`.
- Por cada programa o servicio, una entrevista de unos 90 minutos alimenta **5 salidas**: blogpost, presentación, resumen ejecutivo, tabla de datos e infografía.
- Bloques de la entrevista:
  - Datos de la entrevista.
  - El profesional y su día a día.
  - Campo laboral y empleabilidad.
  - Proyección salarial (siempre con fuente).
  - Diferencias con disciplinas similares.
  - Por qué estudiar o contratar aquí.
  - Testimonios.
  - Notas de uso, que indican qué cita se puede publicar con nombre.
- Cadencia: cada 4–6 semanas, rotando entre perfiles de dirección, operaciones y comercial.

## 7. Gameplan E-E-A-T y calendario de contenidos (.xlsx)
Plantilla: `assets/templates/eeat-gameplan.csv`. Es una extensión de `keyword-content-calendar.csv` [Sheets].

**Columnas:**
- Intención: `Informativo/Transaccional/Mixto`.
- Journey: `Atracción/Consideración/Decisión`.
- Título (headings), Keywords, V/M y Dificultad.
- Formato principal y Formato secundario. Lista de validación: Imágenes, Lista, Check list, Blog post tradicional, Paso a paso, How to, Pillar Page, Entrevista, Comparativo…
- Link de enlazado y Anchor text.
- Metatítulo y Longitud (`=59-LEN()`, caracteres restantes).
- Metadescripción y Longitud (`=140-LEN()`).
- Preguntas para el experto.
- Nombre del experto, Cargo, LinkedIn y registro académico (el cliente suministra estos datos).
- Enlace al Doc, Enlace publicado y Comentarios del cliente.

**Organización del libro:**
- Una pestaña por trimestre: "Publicados", "Gameplan Qn" y "Artículos a optimizar Qn".
- La pestaña "Artículos a optimizar" lleva las columnas *URL · tráfico último año · imagen destacada · preguntas · experto*.

**Patrón de artículo E-E-A-T** (Doc por artículo):
- Cabecera: Metatítulo · Metadescripción · Keyword · Propuesta de URL.
- H1 con una afirmación cuantificada ("X veces…", "N %").
- Introducción con contexto y la tesis.
- H2 con el sustento científico: estudio con la revista, el título y una cita textual, y luego la explicación del cálculo.
- H2 con las dimensiones de beneficio y H3 numerados.
- Enlaces internos a categorías o productos y un enlace externo a la fuente primaria.

## 8. Investigación de keywords por programa (.xlsx)
Plantilla: `assets/templates/kwr-program-clusters.csv`.
- Una pestaña por programa más una pestaña "Resumen".
- Dentro de cada pestaña, bloques horizontales repetidos de *Keyword · VOL/M · Dificultad*: el primero para la keyword principal y los siguientes para las variantes o subclusters.
- La pestaña Resumen consolida la keyword principal, el volumen total y la dificultad media por programa.

## 9. Libro de estrategia SEO de cuenta (.xlsx)
- **Entendimiento:** árbol de navegación del sitio por columnas y niveles.
- **Estrategia SEO:** Actividad · Asignado a · Entregable · Status, con un cronograma por semanas de cada mes. Status: `Realizado/Cliente revisión/En proceso/No asignado`. Asignado: rol o área, como Cliente, Account, UX/UI, Front o SEO.
- **Insumos landing:** Tipo · Diseño · Contenido · URL · Metatítulo · Metadescripción · Indexada.
- **Pendientes (sprint):** Fecha · Actividad · Responsable · Status (`Realizado/Pendiente/En proceso/No asignado/Estancado/Listo`) · Prioridad (`Alta/Media/Baja`) · Insumo · Observaciones.
- **Landings geolocalizadas, por industria y de accesorios:** País · Ciudad/Industria · URL · Redirección · ID de formulario · Contenido · Above the fold · Diseño · Priorización · Indexada.
- **Resultados por landing:** leads por mes.

## 10. Análisis de Google Business Profile (.xlsx)
Plantilla: `assets/templates/gbp-audit.csv`.
- **Ficha de validación:** una fila por ficha y una columna por variable: nombre, categoría, descripción, fecha de apertura, teléfono, chat, web, redes, ubicación y áreas de servicio, horario, horario especial, accesibilidad, público, servicios, fotos interiores y exteriores, ciudades de cobertura y logotipo.
- **Preguntas de atributos:** SÍ/NO por grupo (Accesibilidad, Estacionamiento, Opciones de servicio, Pagos, Planificación, Público, Qué ofrece, Servicios).
- **Productos a publicar:** Categoría · URL · Descripción · Texto de portada · Portada · Status code · Ya existe en GBP · Continúa · Observación.

## 11. Otros patrones
- **Enlazado interno:** un Doc con un H1 por artículo, el enlace, el cambio aplicado (por ejemplo "agregamos video" o "enlace a programa") y una captura como evidencia.
- **Resumen de hallazgos de auditoría:**
  - Herramienta usada, problemas con su conteo de URL (metadatos truncados, duplicados por variantes de producto…) y recomendaciones por mercado.
  - En sitios internacionales, subcarpetas por mercado y contenido local, nunca traducción literal.

## 12. [Drive 2] Convenciones de entrega observadas en la segunda pasada
Lectura del 2026-10-23, solo de estructura. Los libros de Sheets están en `sheets-workbook-templates.md` §10; aquí quedan las reglas de **cómo se entrega** en Drive.
- **Nombre estándar del Doc por URL:** `<Programa o página> – módulos a implementar` (o `Optimización`). Un Doc por entregable, con una pestaña por URL, y la hoja solo lleva el seguimiento (*URL · Doc · Implementado*). El cronograma enlaza a la pestaña que contiene el resultado de cada tarea.
- **Hoja «hub» por programa:** une KWR, anuncios, landing y ajustes de ese programa; el equipo de SEO y el de pauta trabajan sobre la misma fila.
- **Fila de ayuda** en los game plans (la fila 1 o 3 explica cada columna, p. ej. «lugar al que va dirigido el contenido», «cuántas veces se busca la palabra al mes») y glosario lateral de columnas; sirve para formar a redactores nuevos.
- **Dos fechas en el acta de un contrato** (entrega y verificación del supervisor del cliente) y entregables que escriben **obligaciones por parte**: «Equipo: … / Cliente: revisión en 2-3 días hábiles». Las dependencias del cliente quedan escritas, no implícitas.
- **Matriz de insumos** con *Responsable (Cliente / SEO / UX)* y grabación de cada reunión de kick off y de socialización. Sin contraseñas en la matriz: acceso concedido a los correos del equipo y credenciales en un gestor.
- **Biblioteca de módulos HTML** (Doc u hoja): un módulo autocontenido con estilos con alcance bajo un identificador propio, reinicio local, fuente propia con `preconnect` y sin heredar estilos externos, más un **banner CTA obligatorio** reutilizable. Evita que un módulo pise los estilos del tema.
- **Informe semestral con una diapositiva de tráfico de pregrados y otra de posgrados** (o de la oferta equivalente); el mensual compara contra el objetivo del semestre.
- **Plantillas nuevas de esta pasada** (en `assets/templates/`): `gdd-task-brief.md`, `client-content-review-checklist.md`, `pre-launch-audit-checklist.md`, `landing-technical-sheet.md` y los CSV `programmatic-landing-inventory`, `programmatic-input-matrix`, `program-approval-matrix`, `program-data-sheet`, `product-input-matrix`, `monthly-request-log`, `internal-linking-matrix`, `consolidation-canonical-redirect`, `competitor-matrix`, `client-intake-matrix`, `ad-copy-by-angle` y `gdd-time-estimates`.
- **Privacidad al leer Drive:** los documentos de clientes pueden contener datos sensibles (métricas, leads, datos personales). Nada de eso se copia; se resume la estructura y se marca lo derivado solo de títulos como evidencia parcial. Si aparece una credencial: avisar, recomendar rotarla y moverla a un gestor, y no repetirla.
