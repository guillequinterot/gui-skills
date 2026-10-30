---
tags:
  - seo
---

# Controles de calidad editorial y SEO

## Índice

- Puertas
- Semántica
- Evidencia
- Lenguaje
- SEO
- Conversión
- Medición
- Higiene de archivos y retiro de datos
- Roadmap
- Temas YMYL
- Resultado

## Puertas

No publicar hasta superar las puertas aplicables.

## 1. Semántica

- Responde la intención.
- La tesis es clara.
- Las entidades conservan significado.
- No hay contradicciones.
- Las excepciones están indicadas.

## 2. Evidencia

- Las cifras tienen fuente.
- Las fuentes sostienen la afirmación.
- Fechas y alcance están vigentes.
- Hechos e inferencias están separados.
- No existen testimonios o resultados inventados.

## 3. Lenguaje

- Voz y variante correctas.
- Pronombres claros.
- Ritmo natural.
- Mayúsculas y puntuación consistentes.
- Keywords integradas sin forzar.
- Patrones robóticos revisados.

## 4. SEO on-page

- Title, descripción y H1 representan la página.
- Encabezados tienen jerarquía.
- URL y canonical son coherentes.
- Imágenes tienen tratamiento adecuado.
- Enlaces son rastreables y descriptivos.
- Schema coincide con contenido visible.

## 5. Técnico

- Código HTTP correcto.
- Rastreo e indexación según objetivo.
- Contenido principal disponible.
- Responsive y accesible.
- Rendimiento suficiente.
- Sitemap y hreflang correctos cuando aplican.

## 6. Conversión

- CTA corresponde al journey.
- Promesa y destino coinciden.
- Fricción crítica resuelta.
- Evento medible configurado.

## 7. Medición

- Línea base.
- KPI primario.
- Fecha de revisión.
- Responsable.
- Registro del cambio.

## 8. Higiene de archivos y retiro de datos

- En Windows no generar Markdown, HTML ni JSON con cadenas o here-strings de comillas dobles (`"…"`, `@"…"@`): PowerShell expande `$variables` y backticks y corrompe el texto (`$schema`, precios con `$`). Usar here-strings literales `@'…'@`, `[IO.File]::WriteAllText` con UTF-8 sin BOM, la herramienta de archivos del agente o Python (`Path.write_text(texto, encoding="utf-8")`).
- Antes de entregar, validar: sin bytes NUL (síntoma de UTF-16 accidental con `>` u `Out-File` en PowerShell 5.1), UTF-8 sin BOM y tildes legibles.
- Al retirar un dato (precios, una plataforma, un producto, una sede, una cifra), buscarlo en todos los entregables y en el sitio: textos, titles, metas, schema, alt, FAQs, `llms.txt`, plantillas, CSV y briefs. Registrar término, alcance y resultado (0 coincidencias).

## 9. Roadmap

- Los productos o funciones del roadmap solo aparecen como «próximamente»: sin fecha salvo aprobación escrita, sin precio, sin CTA de compra, sin schema de producto u oferta y sin FAQs que los den por disponibles.

## 10. Temas YMYL (finanzas, trading, salud)

- No prometer ni insinuar ganancias, rentabilidad, «ingresos pasivos», tasas de acierto ni resultados de clientes como esperables; tampoco en titles, metas, FAQs ni schema.
- Aviso de riesgo visible junto al CTA y en el pie. Ejemplo para trading: «Operar con instrumentos financieros implica un alto riesgo de pérdida de capital. Los resultados pasados no garantizan resultados futuros. Este contenido es educativo y no constituye asesoría financiera.» El texto final se adapta con el cliente a la regulación del país; la skill no da asesoría legal.
- Autoría con credenciales verificables; testimonios de resultados solo con aviso y evidencia.

## Resultado

Clasificar:

- `approved`
- `approved-with-notes`
- `blocked`

Un linter puede detectar señales; la aprobación requiere juicio contextual.



## 11. Gates añadidos [ClickUp 2]

Origen: feedback real de clientes sobre contenido y una ola de reproceso tras un montaje masivo (anonimizado).

**Reglas editoriales que un cliente aplicó (convertirlas en gate previo a enviar):** ortografía y puntuación · repetición de palabras clave dentro de un párrafo · redundancia entre párrafos · claridad · **cifras con cita** · consistencia de tratamiento (tuteo o usted) · información **diferenciadora**, no genérica entre URLs · datos concretos en lugar de objetivos y beneficios repetidos. Mantener un documento vivo **«Ajustes genéricos»** con las reglas que salgan del feedback y referenciarlo en cada tarea de ajuste. En una revisión, **resaltar en verde lo cambiado** para quien maqueta.

**Cuatro criterios de revisión de contenido del cliente** (taller de revisión): encabezados · caracteres por módulo · keywords · narrativa frente al objetivo del módulo. Orden de entrega: **contenido → metadatos → wireframe**. En plantillas de e-commerce, resaltar en otro color los cambios SEO para pasarlos a producción.

**Chequeos de QA antes de publicar:**
- Texto de relleno («lorem ipsum») o logos de plantilla en páginas publicadas.
- URLs repetidas en las listas de «páginas a optimizar».
- Residuos de contexto: contenido de otro país, programa o producto pegado por error.
- Idioma de cada bloque (nada en español en la versión en inglés).
- Avisos de estado (convocatoria cerrada, agotado, próximamente) coherentes con la realidad.
- Promesas residuales retiradas (salarios, resultados) en todas las páginas, no solo en las revisadas.
- Una **captura de evidencia por punto** al devolver una corrección.

Gate de QA completo para páginas de programa: [education-program-seo.md](education-program-seo.md#gate-de-qa-de-páginas-de-programa).

**Contenido de recaudación y causas sociales (YMYL ligero):** no inventar cifras, testimonios ni beneficios tributarios; `[PENDIENTE]` solo en el borrador, nunca en producción; cifras oficiales «por validar»; pie de foto que aclare que son proyectos anteriores. Ver [launch-checklist-new-site.md](launch-checklist-new-site.md).

**Seguridad en tareas y hojas:** no pegar credenciales ni direcciones IP de infraestructura del cliente en tareas, comentarios ni hojas; usar un gestor de contraseñas y registrar solo «acceso concedido sí/no».


## Puntaje por bloque y excepciones SEO (2026-10-30)
La skill `contenido-sin-slop` tiene una escala 1 a 100 por bloque y una lista de **excepciones SEO** (repetir la keyword en títulos, encabezados, introducción y preguntas frecuentes no es relleno; sí lo es el relleno de keywords dentro de una oración): `contenido-sin-slop/references/07-puntaje-por-bloque-y-excepciones-seo.md`.
