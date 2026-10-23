# Investigación: metodología SEO en ClickUp (solo lectura)

Fecha: 2026-10-23 (hora Bogotá). Fuente: workspace de ClickUp de la empresa, leído con el conector, **sin escribir nada**.
Anonimizado: no aparecen clientes, dominios, personas, enlaces ni datos. Los ejemplos están generalizados.

## 1. Alcance de la revisión
- Se revisó la jerarquía completa: 28 espacios de cliente, las plantillas de metodología (GDD y GDD Light) y el Área de Diseño.
- **Paginación completa** de 37 listas SEO, incluidas las cerradas: 49 páginas de 100 tareas, en total **unas 4.849 tareas** (de mediados de 2022 a octubre de 2026). La página 49 vino vacía, con `has_more: false`.
- **59 tareas leídas a fondo** (descripción, checklists, custom fields, adjuntos y subtareas). Cubren auditorías (inicial, 2.0, post-migración, WordPress + servidor, rendimiento), redirecciones y 404, desindexación, FAQs, enlazado interno, anchor text, schema, game plans, KWR, PR para backlinks, GBP, programático (canonical e indexación), landings (humanización y tono conversacional), informes Q1, capacitación y validación de implementaciones.
- **Docs de ClickUp:** se encontraron 15 únicos y se leyeron los 3 con valor SEO: *Onboarding SEO*, *Diseñando sitios web SEO / GDD* y *Cómo usamos ClickUp* (con *Resumen y alcance*). También se leyó *Planeación* del evento propio, que tiene poco valor SEO.
- Los adjuntos de las tareas son casi todos capturas PNG y no contienen texto metodológico.

## 2. Estructura de servicio
- Por cliente se crea una lista "<cliente> - SEO <año>", más "Reuniones" y canales.
- Los contratos más maduros se dividen en listas: **01 Fase inicial · 02 Operación mensual · 03 Bolsa de expansión/mercados · 04 Dependencias del cliente · 05 Solicitudes y control de alcance**.
- Plantilla de crecimiento (GDD): **Entendimiento del negocio → Estrategia → Launchpad → Dashboard → Mejoras continuas → Handoff de operaciones**.
- Los proyectos puntuales tienen su propia lista con pasos numerados (por ejemplo, la desindexación de PDFs en 10 pasos).
- Los nombres de tarea siguen el formato `SIGLA | Tipo: detalle`, y a veces `[Proyecto] N. paso`.

## 3. Estados
nuevo → en proceso → en revisión → completado/finalizada, más **estancado**. Cada tarea lleva prioridad, estimación de tiempo, fechas de inicio y entrega, y uno o más responsables.

## 4. Formato de tarea (patrón observado en las mejor redactadas)
Cliente/Origen (hallazgo, fecha de la auditoría, prioridad, número de URLs) · Hoja/insumo · **Qué se espera** · Qué NO hacer · **Criterio de hecho** · Cómo entregar (link al entregable y paso a "en revisión") · Qué necesitamos del cliente · Esfuerzo/Impacto · Responsable o "por definir".

## 5. Checklist técnica (una tarea por tipo de hallazgo y mercado/idioma, con prioridad Alta/Media/Baja)
- **Titles:** menos de 30 o más de 60 caracteres, duplicados, múltiples, fuera del head.
- **Meta description:** duplicada, ausente o múltiple.
- **H1:** ausente, múltiple o duplicado. **H2:** vacío o ausente.
- **Imágenes:** más de 100 kB, sin WebP o sin alt.
- **Directivas:** noindex/nofollow. Las páginas de login, carrito y reset de contraseña van con noindex. Verificar que las plantillas no bloqueen el blog.
- **Respuestas:** 4xx, 302 que deberían ser 301 (sobre todo si la URL tiene clics o impresiones en GSC), redirecciones y enlaces rotos.
- **Hreflang:** destino que no responde 200, sin enlace de vuelta, sin autorreferencia (no apuntar siempre al home).
- **Sitemap:** URLs que redirigen, entradas duplicadas, páginas publicadas que faltan, regeneración por cron.
- **Otros:** canonical autorreferente, lang del HTML, slugs duplicados, anchor text, scripts sin defer/async.
- **Auditoría de rutas:** cruzar sitemaps con las páginas clave (HTTP, redirección, canonical, hreflang, presencia en sitemap). Reportar primero lo que está bien y luego los pendientes numerados con "👉 Qué revisar".
- **Herramientas:** Screaming Frog (licencia), Search Console, GA4, Clarity, Python/cURL, URL Inspection API.
- **Regla de priorización:** primero los hallazgos que se corrigen sin crear páginas nuevas (ganancias tempranas).

## 6. Desindexación de documentos (procedimiento de 10 pasos)
1. Accesos.
2. Inventario de URLs en CSV, sin duplicados y comprobando que abren.
3. Confirmar la infraestructura y las cabeceras.
4. `X-Robots-Tag: noindex` solo en los documentos a retirar, que siguen públicos y responden 200. **No usar robots.txt**, porque así Google no podría leer la orden.
5. Piloto con 10 documentos, validado con Python/cURL.
6. No apareció en el listado.
7. Despliegue y auditoría automatizada.
8. Retiradas temporales en GSC.
9. Monitoreo con la URL Inspection API.
10. Reporte final con evidencias y un **protocolo de encarpetado** (`/documentos/<tipo>/<año>/` con noindex por ruta) para que el problema no se repita, más las decisiones pendientes del cliente sobre retención.

## 7. Contenido
- **Game plan:** lista de N artículos con objetivo, programas o servicios, **Esfuerzo/Impacto** y "qué necesitamos del cliente".
- **EEAT por entrevistas:** preguntas al experto → entrevista → multiformato (blogpost, presentación, resumen ejecutivo, tabla de datos, infografía). Las preguntas se ajustan para que sirvan también al SEO.
- **Flujo:** KWR → redacción → imagen de portada → publicación en el CMS → enlazado (módulo de relacionados). Fuentes de contenido: podcast, video o conferencia convertidos en artículo, y calendarios basados en YouTube.
- **Keyword mapping por página:** keyword principal y 2–4 secundarias (nivel + disciplina + modalidad + ciudad), con volumen y posición actual. Entregable: hoja con página · URL · principal · secundarias · volumen · posición.
- **Release de keywords para pauta:** universo de keywords generales y long tail por programa, con volumen y dificultad por país, cuando las campañas tienen pocas keywords o cero impresiones.
- **FAQs** a partir de consultas reales de GSC. Diferenciar las páginas que canibalizan.
- **Compliance:** quitar promesas no sostenibles (por ejemplo, salariales) y mantener los catálogos al día.

## 8. On-page y schema
Title, meta y H1 por tandas. Schema de programa/servicio, FAQPage, BreadcrumbList y og:image.

## 9. Link building / PR
- **Artículo resumen de prensa** (600–800 palabras, estilo periodístico): nombra el medio, explica por qué habla de la marca y qué impacto tiene, y enlaza al home, a la nota original y a 1–2 servicios.
- **Versión newsletter de LinkedIn** (400–500 palabras) que enlaza al artículo y a la nota original.
- **Actualización en GBP** por cada post.
- Se lleva una matriz de notas en medios.

## 10. Local
Optimización de la ficha GBP por país (fotos de interiores y exteriores, portada, video) y publicaciones por servicio. Se registra lo que falta del cliente.

## 11. Programático
Hubs o landings por categoría, módulo de programas relacionados, carrusel de clientes por industria y casos. **Queda en STOP hasta que el cliente aprueba la visual.**

## 12. Migración
- QA por prioridad (Crítico/Alto/Medio/Bajo/Neutral).
- Al lanzar: GA, GSC, GTM, HTTPS/SSL y cabeceras, nomenclatura de URLs y redirecciones.
- Chequeos post-migración.

## 13. Informes
- **Mensual de resultados SEO**, semestral y de rendimiento.
- **El informe de impacto compara antes y después de cada implementación** (clics, posiciones, tráfico en GSC/GA4) e incluye cuántos artículos están publicados, cuántos en el sitemap y cuántos indexados.
- Se avisa de que la indexación puede tardar de 2 a 3 meses, para manejar expectativas.
- Informe UX con Clarity.

## 14. Cadencia y gobierno
- Reuniones semanales o quincenales con acta, que generan tareas.
- Sprint quincenal interno y con el cliente.
- Control de alcance: cada solicitud se vincula a una cláusula del contrato y se indica si entra en el fee.
- Lista de dependencias del cliente.

## 15. Roles (genéricos)
Account/PM (brief, envío y aprobación), contenido (copy), diseño UI, front/maquetación, **SEO técnico (formularios y eventos GA4/Meta Pixel, auditoría)**, QA. Flujo de una landing: brief → copy → UI → maquetación → medición → QA interno → ajustes → envío al cliente → ronda 1 de ajustes. **Nada se publica sin aprobación escrita del cliente.**

## 16. KPIs que se usan
Clics, impresiones, CTR y posición (GSC); tráfico y conversiones (GA4); páginas indexadas o en el sitemap; número de URLs por hallazgo; keywords activas e impresiones por campaña; eventos de formulario.

## 17. Docs internos (resumen)
- **Onboarding SEO:**
  - kickoff después del formulario;
  - auditoría en 3 pasos (rastreo con una pestaña por hallazgo, clasificación de URLs por color y transaccional/evergreen, matriz de entendimiento con prioridad y esfuerzo);
  - 4 tipos de KWR;
  - competidores en 7 pasos;
  - OKR y cronograma.
  - Ahora está en `references/onboarding-and-initial-audit.md`.
- **GDD:**
  - Entendimiento → Estrategia (KWR, persona, IA por intención) → Launchpad de PAI con dashboard (adquisición, visibilidad, salud) → Mejoras continuas (PMI y PBI).
  - Ahora está en `references/growth-driven-design-gdd.md`.
- **Cómo usamos ClickUp:**
  - 5 carpetas, nombre con prefijo y cláusula, 8 estados, campos, niveles de servicio, tarea madre/subtareas, 11 frentes mensuales y los KPI como parámetros.
  - Ahora está en `references/clickup-task-operating-model.md`.

## 18. Obsidian (solo lectura, sin secretos)
- La bóveda tiene 803 notas `.md`.
- La carpeta *SEO Content System* replica la skill (`98_Skill_Source`) y añade la estructura `00_Inicio · 01_Conocimiento · 02_Investigacion · 03_Estrategia · 04_Produccion · 05_Medicion · 06_Aprendizaje · 08_Fuentes · 09_Proyectos`.
- **Nota puente SEO ↔ diseño:** dice cuándo cargar `seo-content-system` y `direct-visual-design` a la vez (landings, UI copy, imágenes, piezas sociales, conversión).
- **Ficha de fuente** del checklist de rastreo por bots de IA. Tiene jerarquía de evidencia (nivel 1 confirmado frente a nivel 5–6 editorial de agencia) y cubre bots de entrenamiento frente a bots de recuperación, la postura según el modelo de negocio, robots.txt en 5 pasos y llms.txt. Ya estaba cubierta por `ai-crawler-access-and-llms-txt.md`.
- Decisión registrada el 2026-07-23: "SEO content system obligatorio", más un protocolo obligatorio de SEO y Obsidian.
- **No se leyeron** las notas *Checklist de publicación*, *Modelo de priorización*, *Flujo editorial*, *Diagnóstico de caídas* ni *Prompt - Auditoría SEO con Screaming Frog (WP + Elementor)*. La lectura se interrumpió y no se reintentó para no cargar el PC. Solo se conocen los títulos.

## 19. Recursos que requieren sesión (no se intentó acceder)
Recuento de enlaces únicos en los Docs y las 59 tareas leídas:

| Servicio | Enlaces | Qué aportaría |
|---|---|---|
| Google Sheets | 45 | Ejemplos reales de matriz de auditoría, KWR, mapas de redirecciones, keyword mapping, matriz de competidores e incidencias. Es lo más valioso. |
| Google Drive (carpetas) | 38 | Entregables (informes, auditorías y game plans en PDF o Slides) |
| Google Docs | 6 | Lineamientos SEO, checklist SEO, propuestas de FAQs y on-page |
| Google Slides | 5 | Formatos de informe y presentación de resultados |
| Looker Studio | 2 | Estructura real del dashboard GDD y de los informes |
| Brevo/Sendinblue | 1 | Poco valor SEO |
| Reportei | 1 | Formato de informe automatizado |

Herramientas SEO citadas que requieren licencia: Screaming Frog, Semrush, Mangools, Clarity, GSC, GA4 y Bing Webmaster Tools.

## 20. No leído
- Unas 4.790 tareas solo por título (sirvieron para los patrones del §17 y de `clickup-task-operating-model.md`).
- Docs de diseño: UX *Mide y vencerás*, *UX ¿Por qué?*, UI, Design PM playbook, Estatus/Tráfico de diseño, Branding y Motion.
- Docs del evento propio: sitio web, pauta y email.
- La página *Equipo*, que se omitió a propósito porque contiene datos personales.
- Las 5 notas de Obsidian del §18.
- En Gmail, la búsqueda de documentos de metodología SEO no dio resultados.

## 21. Google Sheets enlazadas desde ClickUp [Sheets]
Lectura en 2026-10-23 con el conector de Sheets, **solo lectura**: se usaron `get_spreadsheet` y `read_range`, sin ninguna escritura.
- **Inventario:** 45 enlaces que corresponden a **30 IDs únicos**.
  - 18 hojas leídas (estructura, encabezados y fórmulas).
  - 8 hojas no encontradas o sin permiso.
  - 4 archivos Office (.xlsx), que el API de Sheets no puede abrir.
- **Patrones extraídos** (estructura y metodología, sin datos de clientes): ver `seo-content-system-v2/references/sheets-workbook-templates.md`.
  - Libro de auditoría por hallazgo, con vocabularios Tipo, Prioridad, Área y Status.
  - Checklist de migración por etapa y responsable.
  - Mapa de redirecciones y triage de 404 en tres pestañas.
  - Calendario editorial con objetivo SEO/IA.
  - Arquitectura de contenido por niveles.
  - Plan de trabajo, cronograma de rediseño y sprint de pendientes.
  - Matriz de insumos (accesos y productos por responsable).
  - Seguimiento de implementación con un Doc que tiene una pestaña por URL.
  - Modelo de escenarios de leads.
- **Límites:** el conector no expone colores, formato condicional ni reglas de validación de datos. Los vocabularios se infirieron de los valores. No apareció ninguna hoja de competidores legible.
- Hallazgo de seguridad genérico: nunca guardar credenciales en tareas, documentos ni hojas; usar un gestor de contraseñas, rotar ante cualquier exposición y nunca copiarlas a entregables.
- **Drive, Docs y Slides:** leídos después; ver §22.

## 22. Drive, Docs y Slides [Drive]
Lectura del 2026-10-23 con `user-Google-drive`, **solo lectura**. Se usaron `list_folder`, `get_file_metadata`, `read_file` y `download_file`, y los binarios se analizaron localmente con python-pptx y openpyxl. No hubo escrituras, comentarios ni comparticiones.
- **Leídos (solo estructura):**
  - Docs: lineamientos de SEO técnico, acta de revisión de auditoría, memoria de sprint, resumen de hallazgos, optimización de FAQs, guía de entrevista a experto, doc de enlazado interno, artículo E-E-A-T y matriz de insumos.
  - Slides: informe mensual de rendimiento SEO, rendimiento orgánico post-migración y propuesta de desindexación de PDFs (.pptx).
  - .xlsx: gameplan E-E-A-T, calendario de contenidos, estrategia SEO de cuenta, análisis de GBP y KWR por programa.
  - Se listaron también las carpetas del cliente para inventariar los tipos de entregable.
- **Sin acceso (404):**
  - 2 Docs y 3 Slides, uno de ellos con un ID probablemente truncado en ClickUp.
  - 5 IDs de 33 caracteres.
  - 4 carpetas vacías o sin permiso.
  - Las 8 hojas que fallaron con el conector de Sheets no se pudieron identificar una a una porque sus IDs no quedaron registrados. Las pruebas por Drive con los candidatos dieron 404 o duplicaban archivos ya leídos.
- **No leído por irrelevante:** carpetas de fotos y videos.
- **Novedad frente a Sheets:** openpyxl sí expone las validaciones de datos. Las listas reales de Intención, Journey, Formato y Status se incorporaron a las plantillas.
- **Privacidad:**
  - Los documentos contienen métricas, leads y MRR de clientes, nombres de personas, teléfonos, direcciones y un correo de la agencia. Nada de eso se copió.
  - Las memorias de reunión mezclan datos comerciales del cliente. Se recomienda no compartirlas fuera de la cuenta.

## 23. Segunda pasada: ClickUp, Obsidian, Drive y Sheets [ClickUp 2] [Sheets 2]
Lectura del 2026-10-23, **solo lectura** y anonimizada. Se hizo sobre la v1.4.0 con el fin de cubrir lo que la primera pasada no alcanzó. Resultado en la v1.5.0.

**Qué se hizo**
- **ClickUp:** seis agentes de lectura por bloques de listas (agencia propia; clientes recurrentes; B2B y logística; educación; contrato por fases y e-commerce; plantillas GDD y Docs). La primera pasada había cubierto unas 4.850 tareas por título y 59 a fondo; esta leyó más a fondo las de mayor valor metodológico.
- **Obsidian:** cinco notas que habían quedado pendientes (modelo de priorización, checklist de publicación, flujo editorial, diagnóstico de caídas, prompt de auditoría con rastreador para WordPress + Elementor). Aportaron lo que la skill no tenía: *page* frente a *query* en Search Console, la distribución del enlazado interno, las trampas de Elementor y el diagnóstico de caídas.
- **Drive y Sheets:** dos agentes leyeron los libros enlazados desde las tareas (estructura, columnas, vocabularios, fórmulas). Quedaron como notas de estructura; ninguno cerró con conclusiones propias, y las conclusiones se redactaron después en `sheets-workbook-templates.md` §10 y `drive-deliverables-and-guidelines.md` §12.

**Qué aportó**
- Cinco referencias nuevas: contrato por fases y control de alcance; lanzamiento de un sitio nuevo; e-commerce multipaís; SEO de oferta académica; trampas de medición y diagnóstico de caídas.
- Dieciocho referencias ampliadas con una sección `[ClickUp 2]` y dos principios nuevos en `SKILL.md` (medir en lugar de estimar; criterio de hecho y horas reales).
- Dieciséis plantillas nuevas (checklists de revisión y de auditoría previa al lanzamiento, brief GDD, ficha técnica de landing, inventarios y matrices de programático, oferta académica, producto, enlazado, competencia, insumos, solicitudes mensuales, pauta y estimaciones GDD).
- Patrones de gestión que se repiten entre cuentas: la tarea que apunta a una pestaña de la hoja en vez de copiar datos; la columna de bloqueo explícito; el estado «Verificación» entre «hecho» y «realizado»; la decisión de no actuar escrita con su razón; el lead de prueba por landing.

**Límites (importantes)**
1. **El conector de ClickUp tiene un tope de 1.000 llamadas al día para todo el workspace** y los seis agentes lo agotaron a mitad de la lectura (se repone unas 15 horas después). Todos los digests quedaron **parciales**. Las listas sin leer están registradas con su método en un archivo de pendientes fuera del repo (lleva IDs).
2. Lo derivado **solo de títulos de tarea** está marcado como evidencia parcial en las referencias.
3. Los dos agentes de Drive/Sheets fueron **detenidos antes de terminar**: algunos libros solo tienen notas incrementales; los enlaces de los grupos G4-G6 no abiertos hay que repetirlos. El conector solo expone valores y fórmulas, no colores ni reglas de validación, salvo cuando el binario se analiza con una librería de hojas.
4. Los adjuntos (capturas, PDFs) y los Docs de ClickUp de diseño y del evento propio no se leyeron; tampoco la mayoría de los comentarios.
5. Las estimaciones de horas de la plantilla GDD son de 2022: orden de magnitud, no resultado medido. No se replicó ninguna instrucción de inflar horas; la skill exige **horas reales**.

**Hallazgos de seguridad (no copiados)**
- Hallazgo de seguridad genérico: nunca guardar credenciales en tareas, documentos ni hojas; usar un gestor de contraseñas, rotar ante cualquier exposición y nunca copiarlas a entregables.
- Una tarea de informe pedía «exagerar» las horas. La skill lo trata como mala práctica: reportar horas reales.

**Privacidad:** todo el material de esta sección está anonimizado (sin nombres de cliente, dominios, personas, correos, teléfonos, IDs de tarea ni credenciales). Los digests con identificadores viven fuera del repo.
