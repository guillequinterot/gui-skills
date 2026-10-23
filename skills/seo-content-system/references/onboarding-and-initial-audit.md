# Onboarding SEO y auditoría inicial [ClickUp]

Origen: el Doc interno "Onboarding SEO" y unas 60 tareas de auditoría leídas a fondo, anonimizadas. Se usa en el modo `onboarding` y al empezar el modo `audit`.

## 1. Kickoff
- Se hace **después** de que el cliente llene el formulario de entrada. La reunión resuelve dudas del negocio, no recoge datos básicos.
- Participan las personas que asigna operaciones.
- Al salir hay que tener: accesos pedidos (GSC, GA4, GTM, CMS, hosting/CDN si aplica), competidores declarados por el cliente y objetivos de negocio.

## 2. Auditoría inicial en tres pasos
1. **Rastrear el sitio** (Screaming Frog con licencia y las API de GSC, GA4 y PSI conectadas). Se exporta a una hoja con **una pestaña por hallazgo**: encabezados (H1 ausentes o duplicados), metadatos sin optimizar, imágenes pesadas, códigos de respuesta (200/301/302/404/5xx), arquitectura y rendimiento por URL.
2. **Clasificar las URLs** por carpeta o tipo (servicio/producto, categoría, blog, legal, utilitaria). Cada grupo lleva un color, y se separan las **transaccionales** de las **evergreen**.
3. **Matriz de entendimiento**: una pestaña índice con las columnas `Hallazgo · Descripción · Link a la pestaña · Prioridad (Alta/Media/Baja) · Esfuerzo`. Esa matriz es el resumen para el cliente y sirve de backlog. Plantilla en `assets/templates/audit-understanding-matrix.md`.

Cada fila de la matriz pasa a ser una tarea con `assets/templates/task-brief.md` (ver `technical-audit-by-finding.md`).

## 3. Keyword research inicial
- Se parte de una semilla genérica más el país. Se sacan las relacionadas y las **preguntas**.
- Columnas mínimas: `KW · Volumen mensual · Dificultad`. Se colorean las que tienen buena relación volumen/dificultad.
- **Cuatro tipos de KWR** (cada uno va a una pestaña):
  1. Producto o servicio, transaccional (páginas de servicio).
  2. Categoría, que define las secciones del blog.
  3. Long tail informativa, que alimenta el game plan de contenidos.
  4. Long tail transaccional (landings específicas, local, programático).
- La herramienta (Semrush, Mangools, Keyword Planner) se declara siempre. **Nunca se inventan volúmenes**: si no hay acceso, se escribe "sin dato" (principio 4).
- En entornos con IA, la ruta la eligen `keyword-research-ia-local-desktop.md` y `keyword-research-ia-web-hosted.md`.

## 4. Análisis de competidores en 7 pasos
1. Mirar la SERP local de las keywords principales para saber quién compite de verdad en el buscador, que no siempre es quien el cliente cree.
2. Hacer un overview de dominio por competidor: keywords top, tráfico estimado, backlinks y dominios de referencia.
3. Limpiar la lista: quitar marketplaces, medios y directorios que no compiten por el mismo servicio.
4. **Keyword gap**: qué keywords tienen ellos y nosotros no.
5. Perfilar los sitios que enlazan a la competencia, que son la base de la prospección de link building.
6. Armar la matriz: índice, un dashboard por competidor y una carpeta de evidencias.
7. Para estudiar la estructura de páginas concretas, usar `rea-reverse-engineer`.

## 5. Siguientes pasos
- Pasar los objetivos de negocio a **OKR** (objetivo + 2–4 resultados medibles). Los KPI son **parámetros de gestión, no garantías**: se dice así en el entregable.
- Hacer el roadmap de la fase inicial: SEO técnico, contenidos, programático, local y posicionamiento en IA. Después, el cronograma de tareas (ver `agency-operating-methodology.md`).
- Priorizar las ganancias tempranas (principio 16).

## Matriz de insumos y plan [Sheets]
- La matriz de insumos tiene tres partes: índice de enlaces, accesos con casilla sí/no **sin credenciales** y matriz de productos con bloques por responsable. Ver `references/sheets-workbook-templates.md` §7.
- Plan y cronograma: `assets/templates/seo-work-plan.csv`; pendientes: `assets/templates/pending-tracker.csv`.
- Proyección de impacto (escenarios de leads 10/7/5/3 %): `assets/templates/traffic-opportunity-model.csv`.


## Ampliación [ClickUp 2]: handoff, insumos y variantes de KWR

- **Handoff de ventas a operaciones:** asistentes, qué se entrega, carpeta/cliente/canal, correo de bienvenida con un **cuestionario por servicio** (SEO, link building, pauta, GDD) y correo-resumen posterior.
- **Insumos en cuatro bloques:** entendimiento del negocio, diseño, SEO (con «palabras clave identificadas») y front; accesos concedidos a tres correos del equipo. Todo vive en **una matriz maestra** (pestañas: accesos, insumos/cuestionario, cronograma, resumen de entendimiento) y los entregables en **una carpeta** del cliente. Marcar el **plazo de entrega de insumos del cliente** como tarea para medir el retraso.
- **KWR de prospecto** pedido a veces en tres tipos (informativo / transaccional / mixto × geolocalización / categoría / producto), frente a los cuatro tipos del documento de onboarding: adoptar los que el contrato nombre.
- **Competidores:** variables a comparar = autoridad de dominio, palabras clave, nº de backlinks, dominios de referencia, tráfico mensual promedio; con varios países, 2-3 competidores por país.
- **Auditoría inicial:** añadir el ítem «revisar con Search Console las páginas clave para optimizar textos y keywords con consultas reales y rendimiento orgánico», y hacerla **por país** si hay varios mercados.
- **Benchmark y competencia de un sitio de oferta educativa:** extraer tipos de módulos, enlazado interno, uso de formularios y FAQs de los 3 mejores competidores por programa; el hallazgo alimenta a SEO y UX.
- **Auditoría comercial de un prospecto** y **exploración de un CMS ajeno**: ver [agency-operating-methodology.md](agency-operating-methodology.md).
