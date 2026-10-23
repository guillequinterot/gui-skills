# Libros de trabajo en Google Sheets [Sheets]

Estructura reconstruida a partir de **18 hojas reales del equipo** (auditorías, migraciones, KWR, arquitectura, plan de trabajo, enlazado, 404, matrices de insumos), leídas en solo lectura en 2026-10. Solo se conserva la estructura y la metodología; no hay dominios, URLs, cifras ni nombres de clientes. Las plantillas vacías están en `assets/templates/*.csv` (importables en Sheets: Archivo → Importar).

## 1. Libro de auditoría por hallazgo (patrón dominante, 8 de 18 hojas)
Nombre: `<Cliente> | Auditoría <tipo> <mes>`. Orden de pestañas:

1. **Resumen**: título, fuente ("rastreo con Screaming Frog del dd/mm/aaaa"), tabla *Métrica | Valor* (total URLs rastreadas, HTML, indexables, no indexables, 4xx, 3xx, sin meta description, sin H2, tiempo de respuesta medio) y *Hallazgos por prioridad* (Alta/Media/Baja con conteo).
2. **Matriz de entendimiento**: texto que explica el objetivo (estructura de carpetas, total de URLs, porcentaje que entra en el alcance) y las páginas de alto impacto según tráfico GSC. Ver `assets/templates/audit-understanding-matrix.md`.
3. **Entendimiento gráfico**: bloques lado a lado para graficar.
   - *Código de respuesta | N.º URLs* (200 / 301 / 404).
   - *Categoría por contenido* (HTML, CSS-JS, Imagen-vídeo, PDF).
   - *Segmentación* por idioma, subcarpeta o submarca, con el total de URLs sin repetir.
   - *URLs con tráfico relevante | N.º | Clics | %*.
   - *Oportunidades de optimización | N.º URLs* (metatítulos, metadescripciones, headings, imágenes, body/head, noindex/nofollow).
4. **Incidencias / Hallazgos**: la matriz maestra. Ver `assets/templates/audit-findings-matrix.csv`.
   - Columnas reales: *Nombre del problema · Tipo · Prioridad · Área responsable · Status · N.º URLs · % del total · Descripción · Cómo solucionar · Documento/pestaña con hallazgos · Insumo · Validación de optimización · Observaciones/Pendiente*.
   - El nombre usa la taxonomía de Screaming Frog `Categoría: Problema`, por ejemplo `H1: Duplicado`, `Meta description: Más de 155 caracteres` o `Directivas: Noindex`.
   - Hallazgos propios del equipo se añaden en lenguaje natural, por ejemplo "Discrepancia de dominio: URLs duplicadas" o "Fichas de producto duplicadas venta/preventa".
5. **Todas las URLs / Rastreo completo**: export completo del rastreo con columnas de GSC (Clics, Impresiones, CTR, Posición) unidas por URL. Las hojas nuevas llevan una celda `⬅ Volver a Hallazgos` y un subtítulo con el conteo.
6. **Categorización por sección**: *Sección (segmento de URL) | Total | Indexables | No indexables | Promedio de palabras | Tiempo de respuesta*. Variante: una pestaña de URLs y otra de categorización por submarca o carpeta.
7. **Una pestaña por hallazgo**, con nombre corto (`H1 Duplicado`, `Imágenes +100 kb`, `Metatítulos -30 caracteres`, `URLs 404`, `Hreflang - Sin vuelta`, `Directivas fuera del head`, `No indexables con datos de GA`, `URLs sin datos de SC`, `URLs con mayúsculas`, `URLs con guiones bajos`, `Recursos +2 MB`). Ver `assets/templates/audit-finding-tab.csv`.
   - Columnas: URL, valor actual, longitud `=LEN()`, **propuesta nueva**, longitud de la propuesta, **Implementado (casilla)** y nota.
   - La pestaña de 404 añade *URL de llegada* e *Implementación*.
8. Pestañas de análisis cuando aplican:
   - *Rendimiento de URLs* (PSI: performance, FCP, SI, LCP, TTI, TBT, CLS).
   - *Tráfico GSC 12 meses*.
   - *Segmento + tráfico*, con modelo de escenarios de leads. Ver `assets/templates/traffic-opportunity-model.csv`.

### Vocabularios controlados (listas desplegables observadas)
- **Tipo**: `Problema` (rompe algo) · `Aviso` (revisar) · `Oportunidad` (mejora).
- **Prioridad**: `Alta` · `Media` · `Baja`. Una página con tráfico eleva la prioridad.
- **Área responsable**: `SEO` · `Front` · `Cliente` · `QA` · `UX`, más `SEO - Técnico` / `SEO - Contenido`.
- **Status**: `Pendiente` → `En implementación` → `Realizado`. `Cliente` significa bloqueado esperando una decisión del cliente.
- **Implementado / Validado**: casilla TRUE/FALSE por fila. Es la fuente para "validar implementaciones" (ver `migration-redirects-and-validation.md`).
- **% del total** = URLs afectadas ÷ URLs HTML (o imágenes) del rastreo.

### Fórmulas observadas
- `=LEN(B2)` junto a títulos, H1 y descripciones, para la longitud actual y la propuesta.
- `=54-LEN(G2)` / `=60-LEN(..)` / `=155-LEN(..)`: caracteres restantes; un valor negativo indica que el texto se pasa.
- Una columna con fórmula que extrae el H1 de la URL para comparar la propuesta con lo implementado.
- Escenarios de conversión al 10/7/5/3 % sobre el tráfico de cada segmento, multiplicados por el costo por lead.

**Nota:** el conector solo expone valores y fórmulas. No expone colores, formato condicional ni reglas de validación. Los vocabularios de arriba se infieren de los valores repetidos. La codificación por color de URLs (ver `onboarding-and-initial-audit.md`) no se pudo verificar en las hojas.

## 2. Migración (3 hojas)
- **Check list**: *Etapa (Prelanzamiento / Migración / Post migración) · Ítem · Responsable · Validación · Insumo · Nota*. Ver `assets/templates/migration-checklist.csv`.
- **Rastreo fechado** (`rastreo - dd/mm/aaaa`): export completo de Screaming Frog del sitio viejo, que sirve de línea base.
- **URLs viejas vs URLs nuevas**: *URL actual · URL nueva · Nota*. Las URLs que desaparecen se marcan explícitamente como "¿Desaparece del sitio?" y se le pregunta al cliente.
- **Mapa de redirecciones**: *URL actual · Código actual · URL nueva*. Ver `assets/templates/redirect-map.csv`.
- **Check migración** dentro del plan estratégico, con hreflang, robots, sitemap y mapa de redirecciones → GSC + envío del sitemap, GA y GTM → auditoría post-migración, medición, renderizado y QA.

## 3. Tratamiento de 404 y URLs duplicadas
Ver `assets/templates/404-triage.csv`. El libro se organiza en tres pestañas:
- *URL a redireccionar* (URL, error, respuesta, decisión).
- *URLs redireccionadas* (`Source URL`, `Target URL`, `HTTP Code 301/302/410`, el formato que piden los plugins de redirección).
- *URLs que no se pueden redireccionar*: externas, PDFs de terceros, enlaces de reunión; decisión: **desindexar**.

Las decisiones posibles son: `Arreglada` · URL destino (301) · `desindexar` · 410. Para duplicados de prueba (`-prueba`, `-2`), basta con *URL | Código*, donde la oficial va en 200 y la de prueba en 301.

## 4. Keyword research y calendario editorial
- **Calendario de contenidos**: ver `assets/templates/keyword-content-calendar.csv`.
  - Columnas: *País · Ciudad · Buyer persona · Proyecto · Nivel · H1 · Comentario idea (aprobado) · Keyword · Volumen · Intención · Palabras semánticas · Documento · Portada · Link · Status · Meta title · Meta description · Enlaces a proyecto*.
  - Una fila es una pieza. La aprobación del cliente se registra en la misma fila.
- **Términos** (oculta): export de la herramienta (*Keyword · País · Dificultad · Volumen · CPC · CPS*), agrupado por pieza.
  - Añade un **objetivo SEO/RAG** y un **diferencial para citación IA**: una tabla o dato extraíble que el modelo pueda citar. Conecta con `ai-citation-and-geo-playbook.md`.

## 5. Arquitectura de contenido SEO
Ver `assets/templates/content-architecture-map.csv`.
- Una pestaña por submarca o sección.
- Columnas: *Dominio · Nivel 1…4 · URL nueva · Tipología (Home / Agrupadora / Categoría / Producto / Informativa) · Metatítulo · Longitud restante · Metadescripción · Longitud restante · Nota*.
- Pestaña auxiliar *URL planeada vs URL nativa del CMS*, por ejemplo cuando una plataforma impone `/pages/` o `/products/`.
- Es el insumo directo del menú (UX) y de la columna "Metadatos y contenido" del checklist de migración.

## 6. Plan de trabajo, cronograma y pendientes
- **Plan de trabajo SEO**: ver `assets/templates/seo-work-plan.csv`.
  - Columnas: *Fase · Acción · Descripción · Insumos · Responsable · Estado · Fecha de entrega · Link de entregable*.
  - Fases: Planteamiento estratégico → Indexación y rastreabilidad → Estrategia de contenidos.
- **Cronograma de rediseño** (unos 4 meses): Etapa I (entendimiento y arquitectura; kickoff, benchmark, auditorías, KWR) → II prototipos UI/UX → III maquetación y configuración técnica multi-idioma → redacción on-page → capacitaciones → QA, migración y go-live. Se integra con GDD (ver `growth-driven-design-gdd.md`).
- **Pendientes / sprint**: ver `assets/templates/pending-tracker.csv`.
  - Columnas: *Fecha · Actividad · Responsable · Status · Prioridad · Insumo · Observaciones · Encargado*.
  - Separa lo que debe entregar el cliente (accesos, listado de ciudades para programático, manual de marca, buyer personas) de lo que entrega el equipo.

## 7. Matriz de insumos del cliente
- **Pestaña de índice** con enlaces a plan, rediseño, productos, pendientes y notebook.
- **Pestaña de accesos** (GSC, GA, GTM, CMS, YouTube, GBP, dominio/hosting) con una casilla por acceso.
- **Matriz de productos/fichas** con bloques de columnas por responsable: *información que suministra el cliente* (nombre, imagen, marca/línea, categoría, subcategoría, país, descripción corta, precio, variantes, especificaciones técnicas), *lo que diligencia SEO* y *lo que diligencia Front*.
- Hallazgo de seguridad genérico: nunca guardar credenciales en tareas, documentos ni hojas; usar un gestor de contraseñas, rotar ante cualquier exposición y nunca copiarlas a entregables.

## 8. Enlazado interno, FAQs y on-page por URL
Ver `assets/templates/implementation-tracker.csv`.
- Columnas: *URL destino/a optimizar · Documento con la propuesta · Comentarios · Implementado (?)*.
- El documento de propuesta es un Google Doc **con una pestaña por URL**. La hoja solo hace el seguimiento.
- Se usa igual para estrategia de enlazado interno, optimización de FAQs y matrices de implementación on-page.

## 9. Seguimiento de URLs por carpeta
- Pestaña *Todas las URLs* con GSC + rastreo y **una pestaña por carpeta** (`/pregrados/`, `/blog/`, `/profesores/`…) con las mismas 7 columnas.
- Las carpetas que requieren revisión de contenido añaden *Nota · Dato faltante · Descripción nueva*.
- Sirve para priorizar por clics dentro de cada sección y para repartir el trabajo.

## 10. [Sheets 2] Libros nuevos de la segunda pasada
Segunda lectura (2026-10-23) de unos 25 libros y hojas más. Solo estructura; sin dominios, URLs, cifras ni nombres. Algunas lecturas quedaron cortadas por el tope del conector, y lo derivado solo de títulos de pestaña es **evidencia parcial**.

### 10.1 Libro vivo de una cuenta de SEO programático (≈ 30 pestañas)
- **Cronograma por semanas** (Gantt): *Actividad (objetivo + lista numerada de lo que se revisa) · Entregable · Status/Responsable* y bloques `mes → semana 1..4` con una marca. Cabeceras de fase en filas propias: Auditoría y estrategia → SEO on-page → Creación de landings → Sitemap a indexación. Status: `Realizado` / `En proceso` / `Pendiente` / `Cliente`.
- **Inventarios de landings** (una pestaña por familia: por servicio y ciudad, por ciudad de evento, por ruta origen-destino, por industria, hiperespecializadas, de carriers). Todas llevan la casilla **Indexada en GSC**. Plantilla: `assets/templates/programmatic-landing-inventory.csv`.
  - Ruta del contenido: *Doc con una pestaña por ciudad → doc de barrios → prototipo → URL → metas → fecha de entrega*.
  - La URL de las variantes (marketplace, pool) se deriva de la de la variante directa.
  - **QA hallado:** una fila con el title de otra ciudad que la del slug. Validar siempre que ciudad del slug = ciudad del title, meta y H1.
- **Fórmula de la landing hiperespecializada:** Servicio + Ubicación + Producto + Buyer persona + Industria; 6 productos por categoría; un módulo de «otros productos de esta categoría» con enlazado industria → industria, industria → sus productos y producto → productos de su categoría.
- **Matriz de insumos del programático** (producto cartesiano industria × servicio × ciudad × persona × reto): `assets/templates/programmatic-input-matrix.csv`. Alimenta los módulos de dolores, personas y retos. Esqueleto de la landing: 1 about the fold · 2 dolores · 3 «pensados para ayudar a» (cargos) · 4 retos de la industria · 5 servicios específicos · 6 casos de éxito · 7 equipo + CTA.
- **Pestaña «Formularios»:** *Landing · Casilla · Acción (revisar que cada botón lleve al formulario o CTA correcto) · Formulario en el CRM*. Insumo de CRO.
- **«Proyección»:** *Tipo de términos · N.º de keywords · Tráfico potencial · % a ganar · Leads orgánicos mínimo / esperado / óptimo* + comparativo mes a mes de contactos. **«Resultados por ruta»:** *¿A qué página llegaron? · Leads potenciales · Cierres* por ruta (home, cada servicio, programático por familia, blog) para medir la contribución de cada ruta.
- **Pestañas KW:** export de la herramienta con *Keyword · Dificultad · País · Volumen · CPC · Keyword padre · Funciones de SERP · Tráfico potencial · Intención* (informativa / comercial / navegacional + de marca / sin marca + local / no local).
- **Optimización de metadatos:** *3 banderas (título muy corto / duplicado / descripción larga o duplicada) · URL · actual · longitud · propuesta de H1 · nuevo título + longitud · nueva meta + longitud*. Límites de trabajo del cliente: 59 y 140 (otro cliente trabaja con 60 y 155: **declarar el límite por cliente**, ver `on-page-metadata-and-urls.md`).
- **Implementación de encabezados:** *URL · nomenclatura actual (árbol H1-H6 en una celda) · propuesta anotada*.

### 10.2 Auditoría de URLs con clasificación por impacto
Pestañas: Clasificación de URLs · Rendimiento · Fuentes de tráfico (móvil / escritorio) · Sesión por fuente (export de GA4 con su cabecera) · Todas las URLs (export de rastreo de ~43 columnas) · Top países · Top ciudades año contra año · Blog por categoría · metadatos cortos / duplicados · imágenes pesadas.
- **Tabla «Clasificación de URLs»:** *Categoría (Alto / Mediano / Bajo impacto / Otras) · N.º de URLs · % de URLs · Tráfico anual · % del tráfico* + dos gráficos (distribución de URLs frente a la de tráfico). Define a quién optimizar primero. Es habitual que un porcentaje muy pequeño de las URLs concentre la mayor parte del tráfico: **medirlo en cada sitio, no suponerlo**.
- Segmentar siempre en **Toda la web / URLs TOP / Programas (o la oferta)** con *Total de URLs · % de URLs · Visitas · % de visitas*.

### 10.3 Matriz de entendimiento e insumos del cliente
`assets/templates/client-intake-matrix.csv`. Pestañas **Entendimiento · Accesos · Insumos** (+ cronograma y resumen).
- *Entendimiento:* «Qué es el cliente» (un párrafo: modelo y promesa de valor); *línea de negocio · qué ofrece (qué gestiona el cliente y qué el usuario) · ideal para (tipo de comprador, tamaño, cargos) · **palabras clave sugeridas por línea***; comparativo de dos productos o plataformas; beneficios por público.
- *Accesos:* plataforma, usuario, enlace. **Las contraseñas no van aquí** (nunca registrar credenciales; gestor de contraseñas y rotación).
- *Insumos:* *Nombre · Responsable (Cliente / SEO / UX) · Link* + un bloque *Fecha de reunión · Sobre (kick off / brief / estrategia / demo) · Grabación*. Los hitos de contrato y de publicación se anotan como filas, no como notas sueltas.
- Bloque **«Para el contrato»** (documentos legales y de facturación): lo gestiona Account y no se guarda en la matriz.

### 10.4 KWR de prospecto y por programa
- **Un libro por país**; una pestaña por tema o ciudad. Tres bloques horizontales: *Keyword · VOL/M · Dificultad · CPC* (la primera fila es el **head term**; debajo las variantes de cola larga) · *Palabras tipo pregunta* (20-60, de «También preguntan» y de Google) · *Top 10 de la SERP* de la keyword principal + una celda «Comportamiento KW» para el gráfico de tendencia.
- **De lo general a lo específico** (negocio de dos líneas): pestaña **Matriz general** *(entendimiento · categoría · subcategoría · temas semánticos · preguntas en Google)* con un texto de método que declara fecha, herramientas y **cuatro insumos** (reunión con el cliente, benchmark, competidores en Google, intenciones del sitemap); luego **una pestaña por subcategoría** con *Keyword · Intención · Volumen · Dificultad · CPC · Funciones de SERP*. Se conservan las filas con volumen 0 (cola larga muy específica, incluidas las de ciudad).
- Nombre de la pestaña = keyword principal con intención. Una pestaña de producto nuevo puede ser una sola celda con la lista de semillas, **sin volúmenes**: marcarla como semilla antes de medir.
- Plantilla ampliada: `assets/templates/kwr-program-clusters.csv` (añadir las columnas de preguntas y del top 10 de la SERP).

### 10.5 Libros de oferta académica (universidad)
- **Matriz de programas** (ciclo: proponer → revisar internamente → aprobar el cliente → publicar → QA final con comentario): `assets/templates/program-approval-matrix.csv`. Más: matriz de ajustes (índice de Docs), matriz de tráfico antes/después (sesiones y vistas de dos meses consecutivos), matriz de redirecciones, **paridad de idiomas** (ES/EN con estado y «no existe en inglés»), landings geolocalizadas por programa × país con **lead de prueba por landing** (alias único) y la casilla «Prueba ingresada en el CRM».
- **Matriz maestra de oferta para el rediseño:** una hoja por nivel, con **tres URLs por programa** (actual → de prueba → final), imágenes, datos del programa, metatítulo y metadescripción; se reutiliza para redirecciones, metadatos e imágenes. Hoja «Matriz general» con `=COUNTA()` por nivel como control de cobertura y vocabularios en listas desplegables cerradas (nivel, facultad, especialidad madre) para evitar variantes de escritura. Hoja de **videos / nodos sin plantilla** con *URL a redireccionar*.
- **Ficha de datos del programa** (la fuente única de landing, FAQ, schema y copys): `assets/templates/program-data-sheet.csv`. Los datos oficiales (código, registro, costo) vienen solo del cliente.
- **Game plan** por periodo: *País · Intención · Journey (Atracción / Consideración / Decisión, o TOFU / MOFU / BOFU) · Título · Keywords · V/M · Dificultad · Formato principal y secundario · enlazado a programas y a artículos · anchor sugerido · metatítulo + longitud · metadescripción + longitud · artículo de blog · artículo de LinkedIn · comentarios del cliente*. Una **fila de ayuda** explica cada columna (útil para formar a redactores). Un artículo viaja por dos canales (blog y newsletter) con aprobación propia.
- **Calendario por programa priorizado:** checklist de *qué se le hace a cada artículo por canal* (blog: 6 preguntas frecuentes, banners, enlazado hacia y desde otros, versión infográfica; LinkedIn: enlazar el newsletter al original, banners, home, programas).
- **E-E-A-T con expertos:** mapa letra → formato (Expertise + Authority → artículo con citas expertas; Experience → guía basada en experiencia; Trust → metodología) con *Fuente a consultar · Rol · Objetivo E-E-A-T · Objetivo de negocio · 5 preguntas al experto*.
- **Pipeline podcast → artículo → YouTube → LinkedIn:** *Estado · Autor (experto) · enlaces · copy de YouTube (gancho + 3 conceptos + hashtags) · nombre de YouTube con patrón `<Título> | <Experto> | <Serie>` · artículo de LinkedIn · estado de grabación*.
- **YouTube como motor de SEO:** exportar el canal → clasificar por temática → enlazar a programas → medir caracteres de la descripción → clasificar cada descripción (*recomendable / recomendable con complemento / no recomendable*) → reescribirlas para que resuman y respondan dudas, y enlacen a programas, artículos y guías, no solo al home.
- **Datos estructurados por tipo de página:** home (`CollegeOrUniversity`/`EducationalOrganization` con `sameAs`, dirección y acreditaciones), programas (`EducationalOccupationalProgram`), admisiones (`FAQPage`), eventos (`Event` con modalidad, lugar, organizador). Ver `education-program-seo.md`.
- **Nuevas concentraciones o programas:** *imagen principal · Doc ES · slug ES · title ES · description ES · Doc EN · title EN · description EN · slug EN*. El inglés es una adaptación con su propio slug, no una traducción literal.
- **Consolidación de subpáginas** (rediseño con plantilla de pestañas): `assets/templates/consolidation-canonical-redirect.csv`. Regla observada: la subpágina que responde 200 con contenido propio se **canonicaliza** a la página principal del programa; las que dan 403/404 se **redirigen con 301**.
- **Pauta alineada con SEO:** `assets/templates/ad-copy-by-angle.csv`. Cuatro ángulos por programa (flexibilidad, ubicación, campos de acción, reconocimiento), una **línea legal única** repetida en todas las piezas, un dato verificable distinto por ángulo, y una campaña paraguas para ofertas de muchas especialidades. Una hoja «hub» une por programa: KWR, anuncios, landing y ajustes.

### 10.6 Linkbuilding, enlazado interno y competencia
- **Linkbuilding:** matriz de entendimiento (dominios por competidor, categorías de enlaces propios, país, follow / nofollow) → plan por dominio *(DA · costo · tráfico · dominios de referencia · enlaces)* con total en moneda → una pestaña por categoría y por competidor (export de la herramienta). Método: clasificar el perfil de enlaces por categoría de medio y pedir o comprar en la categoría de medios masivos con mínimos de DA y tráfico. Registrar siempre la política de enlaces (do-follow a terceros, UTM) y el presupuesto aprobado.
- **Enlazado interno del blog:** `assets/templates/internal-linking-matrix.csv`. Inventario por categoría con sesiones y vistas; **una pestaña por combinación de categorías** (el enlace se asigna dentro de la misma categoría); pestaña **«sin match»** para decidir con el cliente. **Enlazado a programas:** una pestaña por programa con *ruta · home · categoría del artículo · URL · anchor · listo · destino · usuarios · vistas*, y un *Dashboard* con el número de URLs que enlazan a cada grupo de programas como meta de cobertura.
- **Competencia:** `assets/templates/competitor-matrix.csv`. Pestaña de entendimiento con cinco objetivos numerados (autoridad, mejores palabras clave, tráfico, keywords orgánicas, dominios de referencia), la finalidad («qué replicar, qué desechar, qué keywords atacar»), la herramienta y **fecha de ejecución y de actualización**; un dashboard con ~10 competidores por columnas, la **definición de cada métrica en la columna A**, la autoridad como par *dominio / prefijo analizado* y enlaces a su pestaña de detalle. Clasificar cada competidor: **directo, indirecto, sustituto o revendedor-proveedor**, con un bloque de «contexto del mercado» antes de la tabla.
- **Libro maestro de URLs por tipología** (agencia propia): pestañas Todas las URLs → 404 por carpeta → landings por servicio × ciudad × responsable → casos de éxito (resumen de reto, enfoque y resultado) → industrias → plataformas → errores de slugs heredados (`__trashed` se redirige al padre) → blog con checklist por pieza (módulos, enlazado, videos, enviado a indexar) → biblioteca de módulos HTML con estilos con alcance propio y un banner CTA obligatorio. Es el insumo de los módulos dinámicos de «relacionados».

### 10.7 Plan editorial de autoridad (SEO + GEO + AEO)
- **Plan de N piezas** (una fila = una pieza): *Macrocluster · Objetivo · Buyer persona dominante · Tipo de intención · Formatos que deben dominar · Frente competitivo · Quiénes destacan · Qué hacen bien · Hueco que puede tomar el cliente · Capa semántica · Ejemplos prioritarios · Título SEO · URL sugerida · Description · Carpeta · Artículo · Enlace publicado · Autores en LinkedIn*. Los cuatro campos de frente competitivo son un **mini-benchmark por macrocluster** dentro del plan.
- **Leyenda** (diccionario de campos), **Resumen** (piezas por macrocluster y personas dominantes), **Categorías** (lista real del blog para detectar brechas).
- **Página agrupadora por industria:** above the fold · intro (~500 palabras: por qué esa industria, 3-4 datos) · casos de éxito del sector · proyectos y experimentos propios · recursos descargables · newsletter · expertos (ficha por persona con `Person`) · clientes del sector (clasificados) · conferencias · ~30 FAQs hiperespecializadas.
- **Taxonomía reutilizable del sector educativo** para FAQs y segmentación: por nivel académico, por modalidad y por tipo de institución, cada nodo con una definición de una línea.

### 10.8 E-commerce multiidioma (tienda de plataforma cerrada)
- **Auditoría por hallazgo:** misma estructura del §1, con la variante más reciente: columna final **quién propone y quién implementa** (p. ej. «SEO propone, Front implementa») y la **decisión de no actuar con su razón** («se resuelve en el rediseño», «no aplica»); un **hallazgo positivo** registrado como tipo Aviso y prioridad Baja («se revisaron N URLs: ninguna con noindex»); y pestañas pequeñas con título y conteo («Títulos – Longitud – 14 URLs»), una línea de verificación en vivo con fecha y una columna final **Motivo**. La pestaña de redirecciones 302 con tráfico real lleva impresiones y clics: la prueba numérica de por qué sube de prioridad.
- **Reglas de redacción de la descripción de un hallazgo:** cuenta exacta y porcentaje, un ejemplo con patrón de URL, consecuencia para Google y para el usuario, **marca explícita de lo inferido frente a lo verificado** y petición de confirmación humana cuando el hallazgo se deduce por coincidencia (p. ej. pares de fichas detectados por slug).
- **Todas las URLs** con ~30 columnas, entre ellas *Nivel de profundidad · Enlaces entrantes únicos · Recuento de palabras · Impresiones, clics y posición de GSC · Tipo de redirección · **Hash de contenido*** (detecta duplicados exactos). **Categorización por sección:** en plataformas donde los recursos del CDN dominan el rastreo, separar activos de páginas HTML antes de calcular porcentajes.
- **Matriz de productos** (32 columnas en tres bandas con responsable): `assets/templates/product-input-matrix.csv`. **Matriz de implementación:** *URL · Doc de implementación · Implementado*. **Listado de productos** simplificado para el cliente con preguntas guía; sirve para validar categorías contra la intención de búsqueda y para detectar productos que aún no están en la web.
- **Cronograma de un rediseño de ~4 meses** y **cronograma de oferta de 12 meses con acta de supervisión**: *Etapa · Descripción · Mes · Inicio · Entrega · Fecha límite · % avance · Status · Entregables*, con una fila final `=AVERAGE()` de avance global; el status de etapa es texto libre con el conteo de talleres; los entregables escriben **obligaciones por parte**. El acta repite las etapas con **dos fechas** (entrega y verificación del supervisor) y añade premigración, migración, posmigración, entrega de administración y soporte. Un plan de rediseño también cuenta **páginas por tipo** y exige un **acta de entrega** que formalice la conformidad.
- **Check de migración:** *Fase · Acción · Descripción · Validado (FALSE por defecto) · Fecha · Insumos · Responsable · Estado · Link*. Ver `migration-redirects-and-validation.md`.

### 10.9 Operación recurrente y proceso comercial
- **Matriz mensual de solicitudes** (una pestaña por mes): `assets/templates/monthly-request-log.csv`. Mide el tiempo real de cada solicitud y registra «por qué está estancado». Una alerta de ciberseguridad se registra como una solicitud más, con activo afectado, fecha y evidencia de la corrección. **Alimenta el informe y demuestra las horas: se reportan horas reales, nunca infladas.**
- **Seguimiento de tareas por sprint** (hoja): *Fecha · Actividad · Responsable · Status (Pendiente / Realizado / Estancado) · Prioridad · Insumo (enlace a la hoja de trabajo de esa fila) · Observaciones · Encargado*.
- **Proceso de clientes nuevos:** 10 entregables ordenados **con la justificación del orden** (reunión de entendimiento, landing de conversión, pauta de prueba, mensajes de respuesta, analítica, auditoría express de ventas de máximo 3 páginas, rediseño, SEO, contenido de soporte, optimización). Reglas escritas: la auditoría express dura como máximo 3 días y se centra en lo que impacta ventas; landing y pauta absorben la mayor parte de la energía de las primeras semanas; todo entregable lleva una métrica; los contenidos secundarios solo si hay un MVP activo; tras la semana 3 se optimiza, no se rehace.
- **Ficha técnica de landing por equipo:** `assets/templates/landing-technical-sheet.md`.
- **Tallas de rediseño** (solo orden de magnitud para estimar, no para cotizar sin medir): S (3-5 páginas), M (6-10), L (11-20), XL (aplicación, 15-40 pantallas), con horas por equipo (contenido, diseño UX/UI, maquetación) y siete excepciones que suman horas (e-commerce, animaciones, formularios avanzados, arquitectura multilingüe, personalización sin UI kit, audiovisual propio, revisión lenta del cliente). Acuerdos de servicio: el cliente responde en 24-48 h, versiones de escritorio y móvil obligatorias, los cambios estructurales reevalúan el alcance, y todos los equipos hacen QA.
- **Plantilla de estimaciones GDD** (con columna de tiempo real y desviación): `assets/templates/gdd-time-estimates.csv`.

### 10.10 Auditorías de la primera ronda y re-auditoría
- **Incidencias:** 9-10 columnas (*Nombre · Tipo · Prioridad · Status · URLs · % del total · Descripción · Cómo solucionar · Insumo*). Las descripciones y soluciones salen de la biblioteca de textos de la herramienta de rastreo, traducidas, y por eso son estables y reutilizables; los nombres usan `Categoría: Problema`.
- **Re-auditoría:** añade *Responsable (SEO / Front)* y un Status con **Verificación** (cambio hecho, falta comprobarlo) y **En redacción**, además de los ya conocidos. Sirve para medir avance entre rondas.
- **Pestañas por tipo de recurso, por tipología de plantilla y por versión de idioma** además de una por hallazgo. Una columna de **similitud semántica** (página más cercana y puntuación) detecta canibalización en blogs.
- **Hallazgos con vocabulario nuevo:** «Títulos: fuera del `<head>`», «Título / meta description: múltiple» (suele ser un conflicto de plugins), «H1: texto ALT en H1» (logotipo dentro del H1), «Enlaces salientes sin texto de anclaje», «Canonicals: falta», «Sitemap: URLs sin prefijo de idioma que redirigen», «Fichas duplicadas venta / reserva», «Slug con `-copia`», «H2 vacío» distinto de «H2 ausente».
- Reglas escritas en descripciones: cambiar URLs con mayúsculas o guiones bajos solo vale la pena con 301 y rara vez solo por SEO; el hreflang autorreferenciado dejó de ser requisito, pero sigue siendo la solución más simple.
- **Cuidado con el formato:** un porcentaje escrito como número puede salir con formato regional erróneo (4,550 en lugar de 4,55 %). Fijar el formato de celda.

**Límites de esta pasada:** las lecturas fueron de solo lectura y de estructura; no se vieron colores ni validaciones de datos en todos los libros. Dos agentes de lectura se detuvieron antes de cerrar, así que algunas hojas solo tienen notas incrementales; pueden quedar libros sin leer (ver el HANDOFF).

## Uso desde la skill
- En modo `audit`, `migration`, `keyword-research` o `report`, entrega los resultados en el formato de estas plantillas: mismas columnas y mismos vocabularios.
- Así el equipo puede pegarlos directamente en su libro.
- Si redactas propuestas (títulos, H1, metas), incluye siempre la columna de longitud y la casilla de Implementado en FALSE.
