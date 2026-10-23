---
tags:
  - seo
  - educacion
  - programas
  - rediseño
---

# SEO para oferta académica: programas como unidad de trabajo [ClickUp 2]

Origen: tres años de listas de SEO de dos universidades (una con 98 programas), su rediseño web y sus landings de pauta (anonimizado). **Cobertura parcial:** quedaron sin leer las listas de otras universidades; las secuencias de rediseño salen en parte de títulos de tarea. Complementa [programmatic-and-local-seo.md](programmatic-and-local-seo.md), [editorial-pattern-long-form.md](editorial-pattern-long-form.md) y [migration-redirects-and-validation.md](migration-redirects-and-validation.md).

## Índice

- Principios
- Priorización por dato comercial
- Ficha de acción del plan por programa
- Keyword, metadatos y schema por programa
- Programas hermanos y canibalización
- Modelo de página de programa
- Gate de QA de páginas de programa
- Contenido: entrevistas, artículos y ciclos propedéuticos
- Landings geolocalizadas por país
- Matriz maestra de oferta académica
- Rediseño con foco SEO
- Operación con CMS ajeno

## Principios

1. **El programa académico es la unidad de optimización**, no la página suelta ni la keyword.
2. El catálogo oficial vigente es la fuente de verdad para nombres, planes de estudio y créditos. Validar el catálogo **antes** de asignar tareas (apareció en una lista priorizada un programa que no existía).
3. Quitar las promesas no sostenibles (p. ej. salariales) y mantener coherentes los avisos de acreditación, licencia y convocatoria; ver [editorial-quality-gates.md](editorial-quality-gates.md).
4. Consistencia de tratamiento (tuteo o usted) en todos los textos: el cliente lo reclamó.

## Priorización por dato comercial

Ordenar los programas por **el dato del negocio, no solo por tráfico**: primero los que **cayeron a cero matrículas orgánicas** en el mes (pregrados y tecnologías), después los posgrados sin matrículas en dos meses. Los programas que **no se van a pautar** reciben un plan de acciones aparte para impulso orgánico, rendimiento y conversión. Un «KWR de programas que han caído» sirve de disparador de optimización. En una oferta con varias escuelas o países, rebalancear el game plan según dónde está la captación (p. ej. más negocios y doctorados si ahí están más programas y matrículas) y dejar una fila de comentarios del cliente dentro del game plan.

## Ficha de acción del plan por programa

Plantilla de tarea para un sprint de acciones (se crean varias el mismo día tras la reunión de seguimiento):

```text
Acción: [verbo + qué + cómo]
Programas: [lista numerada; tachar los inexistentes]
Entregable: [artefacto + criterio, p. ej. «N propuestas aprobadas y publicadas»]
Carpeta: [enlace]
Esfuerzo: [Bajo|Medio|Alto] | Impacto: [Bajo|Medio|Alto]
Qué necesitamos del cliente: [insumo]
```

Orden implícito del sprint: (1) mapa de keywords por programa (insumo de todo) → (2) title/meta/H1 por lotes → (3) schema en plantilla → (4) FAQs desde consultas reales → (5) diferenciación de programas que compiten → (6) enlazado interno hacia programas con pocos enlaces → (7) game plan multiformato de entrevistas. **Registrar la fecha de publicación** de cada lote para medir en Search Console.

## Keyword, metadatos y schema por programa

- **Keyword por programa:** principal + 2-4 secundarias = nivel + disciplina + modalidad + ciudad, con volumen y posición actual. Hoja: programa · URL · principal · secundarias · volumen · posición. KWR separado por nivel (pregrado, posgrado, virtual) y por marca/especialidades. **Release de keywords por convocatoria**: tanda 1 con la matriz táctica; tanda 2 con el resto de programas de la convocatoria.
- **Metadatos:** reglas del cliente (en un caso: título 58 caracteres, metadescripción 140) en vez de un rango universal; ver [on-page-metadata-and-urls.md](on-page-metadata-and-urls.md). No tocar el nombre oficial del programa; un H1 duplicado se corrige en la plantilla.
- **Schema:** `EducationalOccupationalProgram` (nombre, nivel, duración, modalidad, ciudad) en la **plantilla**, una sola vez, y `CollegeOrUniversity` en la home; validar todas las URLs **en lote** en el validador de schema.org. Ver [schema-markup-for-ai-citation.md](schema-markup-for-ai-citation.md).
- **FAQs:** 4-6 preguntas por programa a partir de **consultas de Search Console con impresiones que la página no responde**.

## Programas hermanos y canibalización

Para pares o tríos que compiten (especialización frente a maestría del mismo campo, áreas vecinas): revisar las consultas compartidas, definir el ángulo de cada uno y añadir un bloque corto **«¿Cuál elegir?»** con enlaces cruzados, **validado por la facultad**. Entregable: informe de consultas compartidas por par.

## Modelo de página de programa

Módulos de referencia: descripción y por qué estudiarlo · conocimientos que adquirirá · salidas profesionales (en qué puede desempeñarse) · perfil ideal · convenios · docentes (perfiles) · plan de estudios (módulo propio) · tabla de créditos · programas relacionados · países y ciudades desde donde se puede cursar · FAQs · formulario con prueba por programa · bloque de «convocatoria cerrada» si aplica · banner con el idioma de la oferta · versión ES/EN.

- **Orden de H2:** primero el valor para el usuario (qué aprenderá, salidas, convenios) y después «desde dónde estudiar».
- H2 internos **más cortos** que los H2 de SEO cuando los títulos largos se ven mal (compromiso SEO/UX).
- Cuando la estructura de URLs del sitio es deficiente, definir una **plantilla mínima de contenido** (contenido + metadatos + 5-6 módulos + FAQs), optimizar un programa de referencia y replicar por programa en documentos.
- Datos concretos y diferenciadores, no objetivos y beneficios genéricos repetidos entre programas.
- Banners CTA: 2 por artículo (tras un H2 relevante y al final); archivos con el nombre exacto del programa; el CTA enlaza al formulario del programa o abre el modal.

## Gate de QA de páginas de programa

Tras un montaje masivo (decenas de concentraciones en pocas semanas) una auditoría abrió ~54 tickets de reproceso (23 % de las tareas del año). Los errores se repiten, así que **ninguna página pasa a «en revisión» sin esta lista, con una captura como evidencia por punto**:

- plan de estudios correcto (no el de otra concentración; módulos compartidos entre páginas no son error);
- idioma de cada bloque (nada en español en la página en inglés: notas al pie, encabezados, FAQ);
- H1/H2 únicos;
- 301 de la ruta vieja y entrada en el sitemap;
- menú: sin ítems muertos ni que apunten a la versión del otro idioma; programa en la escuela correcta;
- estado de convocatoria correcto (hubo avisos de «admisiones cerradas» en programas activos);
- PDF vigente, sin duplicados ni nombre antiguo;
- logos y textos de plantilla retirados (placeholders); sin promesas residuales;
- nombres consistentes; enlaces rotos.

## Contenido: entrevistas, artículos y ciclos propedéuticos

- **Entrevista a un decano o experto = motor de contenido** con cinco salidas (blogpost, presentación, resumen ejecutivo, tabla de datos, infografía); ver [sme-interview-guide.md](../assets/templates/sme-interview-guide.md). **SEO revisa las preguntas antes de entregarlas** para sacar keywords naturales, dudas frecuentes y datos duros.
- **Ciclos propedéuticos** (técnico → tecnólogo → profesional, con homologación): añadir 2-3 rutas de formación al contenido. Bloque por ciclo: nombre de la salida · lo que sabrás hacer (3) · dónde podrás trabajar. Se puede explicar el valor de cada ciclo **sin mostrar el plan de estudios**. En una landing, el titular vende **al profesional**, no al técnico; nombrar los tres niveles; módulo bajo el pliegue; ocultar testimonios genéricos repetidos.
- **Artículos de pregrado**: ángulo campo laboral, salario y perspectivas en el país + año (los pregrados no tienen especializaciones).
- **Pipeline podcast → artículo** (una tarea por paso): ficha del episodio → imágenes de encabezado (web y LinkedIn) → ficha con botón de descarga de PDF → recursos del podcast (PDF) → versión artículo en el CMS → versión LinkedIn → programas relacionados.
- **Artículo + versión LinkedIn** como entregable estándar de contenido propio: versión reducida que enlaza a los programas y al home.
- Criterios editoriales que el cliente aplicó (convertir en gate): ortografía y puntuación; repetición de la keyword exacta (una aparecía ~30 veces en un documento); redundancia; claridad; cifras con cita; consistencia tuteo/usted. Mantener un documento vivo **«Ajustes genéricos»** con las reglas surgidas del feedback y referenciarlo en cada tarea de ajuste; resaltar en verde lo cambiado para que lo siga quien maqueta.

## Landings geolocalizadas por país

Para programas replicados por país en un CMS donde la plantilla no se puede cambiar (**solo contenido, sin módulos nuevos**):

- Estructura: validadores de números (estudiantes, ciudades) · ciudades del país · testimonios y reseñas · industrias del país que más demandan el programa · FAQs geolocalizadas · mapa o tarjetas por país.
- Guía de contenido por país: oportunidades comerciales, industrias y sectores con mayor impacto, quién cursa el programa, para qué sirve en el año actual.
- Hoja de personalización: país · programa · responsable · fecha · documento · URL de la versión por país. Competidores: 2-3 por país.
- **Publicación escalonada**: subdirectorio por país con hreflang (`es-XX` + `x-default`), **noindex hasta que el redactor edite** (evita residuos de contexto de otro país), tarea «Colocar INDEX» y luego «Indexar en GSC»; QA de residuos de contexto entre países. Detalle en [programmatic-and-local-seo.md](programmatic-and-local-seo.md).
- Si el proveedor del CMS rompe traducciones (bloques huérfanos), abrir ticket y registrar el bloqueo con fecha.

## Matriz maestra de oferta académica

Hoja con **una pestaña por nivel**; columnas: programa · URL actual · **URL de pruebas** (nuevo slug) · metatítulo · meta descripción · imagen. **Nuevas columnas siempre a la izquierda** (no rompe fórmulas). Una sola matriz sirve para redirecciones, metadatos e imágenes, y para el seguimiento de aprobación por color: **verde** aprobado · **azul** comentarios del cliente por atender · **naranja** ajustado y listo para reenviar · **amarillo/rojo/rosado** pendientes; más una columna «implementado». Las tareas apuntan a la pestaña, no copian datos.

Reglas de imagen destacada: `.webp`, menos de 100 kB, nombre en minúscula sin tildes, `ñ`, símbolos ni espacios, palabras separadas por guion medio y **nombre = nombre del artículo**; enlace en una columna de la hoja para que SEO la implemente. Ver [image-seo-and-accessibility.md](image-seo-and-accessibility.md).

## Rediseño con foco SEO

Secuencia observada: **auditoría base** (hoja) → talleres internos y con el cliente por sección y por perfil (la institución, estudiantes, docentes, egresados) → **documento único de arquitectura** → tres propuestas visuales (el cliente elige «opción N» por módulo y el equipo responde por escrito con el criterio de UX) → UI kit → sprint con el cliente quincenal → WordPress + constructor visual en **subdominio de pruebas** → matriz de programas con nuevos slugs → maquetar plantillas → **QA por plantilla** con capturas marcadas → ajustes → metadatos de todos los programas → imágenes por programa.

- Tipos de plantilla definidos **antes** de maquetar: agrupadora (pregrado, facultad), interna (programa, facultad) y perfil (estudiantes, docentes, egresados).
- **Congelar y firmar el árbol del menú** en el documento de arquitectura antes de maquetar, y fijar el criterio de hecho de «ajustes de menú» como «estructura = documento de arquitectura». Sin eso la tarea se repitió cinco veces.
- Módulos del home institucional: banner editable (desktop/móvil), buscador por oferta formal y no formal, accesos rápidos (calendario de admisiones, pagos, apoyo financiero, inscripción), unidades de negocio, vinculaciones (internacionalización, proyección social, bienestar, investigación, biblioteca), noticias con categorías, eventos, alianzas (logos con enlace), pie con sedes y PQRS.
- Plugins y funciones de sitio universitario (accesibilidad, íconos flotantes de contacto, traductor): tabla plugin · vista previa · gratis/pago · alternativa · comprobado.
- Decisiones de diseño razonadas por escrito (tamaño de párrafo 16 pt como óptimo web, 14 pt solo en tarjetas; íconos de tamaño único y visible; tipografía institucional verificada contra el manual de marca).

## Operación con CMS ajeno

- **Riesgo de migración por falta de acceso al CMS** (administrado por un proveedor): registrarlo como dependencia del cliente y **escalar por correo antes** de que avance la migración. Sin acceso no hay redirecciones.
- Captura de formularios en un CMS cerrado: JavaScript que captura los campos (incluido el acudiente en menores) y los envía a un automatizador; **piloto con un programa**; campos desplegables por especialidad, ciudad y modalidad.
- Entornos PRE y PRO sin fusión: crear directamente en producción con «publicado» desmarcado para que quede oculto; probar el formulario con el código del programa y reportar correo y hora.
- Informes: el semestral lleva una diapositiva de tráfico de pregrados y otra de posgrados; el mensual compara con el mes anterior y con el objetivo del semestre.
