---
tags:
  - seo
---

# SEO on-page, metadatos y URLs

## Índice

- Paquete por página
- Title
- Metadescripción
- H1 y encabezados
- Slugs
- Cambios de URL
- QA

## Paquete por página

Entregar cuando aplique:

```text
URL:
Keyword e intención:
Title:
Metadescripción:
H1:
Slug:
H2/H3:
Canonical:
Robots:
Enlaces:
Imágenes:
Schema:
CTA:
KPI:
```

## Title

Crear un title:

- Único.
- Descriptivo.
- Coherente con la página.
- Diferenciado de otras URLs.
- Natural.
- Con marca cuando aporte reconocimiento.

Usar 50–60 caracteres como referencia editorial, no como garantía. Los buscadores pueden construir otro title link.

Evitar:

- Repetición de keywords.
- Titles idénticos en muchas páginas.
- Promesas ausentes del contenido.
- Plantillas que ocultan el tema.

## Metadescripción

Resumir el valor real de la página. Incluir detalles concretos, intención y diferenciador. Un rango de 140–160 caracteres puede ayudar a editar, pero no garantiza el fragmento mostrado.

No:

- Duplicar descripciones.
- Rellenar con listas de keywords.
- Inventar precios, ubicaciones o beneficios.
- Repetir el title sin ampliar.

## H1 y encabezados

Usar un H1 principal que describa la página. No es obligatorio que sea idéntico al title. Mantener una jerarquía semántica y no elegir niveles por tamaño visual.

## Slugs

Preferir:

- Minúsculas.
- Guiones.
- Brevedad suficiente.
- Palabras descriptivas.
- Estabilidad.

Evitar fechas innecesarias, parámetros indexables sin control, stopwords acumuladas y keyword stuffing.

## Cambios de URL

Antes de cambiar una URL existente:

1. Verificar tráfico, enlaces, rankings y uso externo.
2. Definir destino equivalente.
3. Crear redirección 301.
4. Actualizar enlaces internos, canonical, hreflang y sitemap.
5. Probar códigos y cadenas.
6. Supervisar Search Console y logs.

No redirigir muchas páginas diferentes a una home genérica.

## QA

- Title y H1 representan el contenido.
- Metadescripción no promete de más.
- Slug coincide con la arquitectura.
- Canonical es correcto.
- La página puede indexarse si debe.
- No existe duplicación evitable.



## Ampliación [ClickUp 2]: reglas por cliente y sobre-optimización

- **Longitudes: regla por cliente.** Los rangos de otros documentos (title ≈ 30-60, meta ≈ 120-160) son valores por defecto. Cuando el cliente fije los suyos, manda su regla: un caso real trabajó con **58 caracteres para el title y 140 para la meta description** («más que optimizar, ajustar a la extensión»). Registrar la regla del cliente en el HANDOFF del proyecto.
- **Sobre-optimización.** Fijar un máximo de repeticiones de la keyword exacta por documento y tratar como alarma casos como una keyword repetida ~30 veces. Variar con naturalidad (ver principios 6, 7 y 11 de `SKILL.md`).
- **H2 en páginas de programa o de servicio:** el valor para el usuario (qué aprenderá, resultados, convenios) va antes que «desde dónde estudiar» o «dónde estamos». Los H2 internos pueden ser más cortos que los H2 de SEO cuando los títulos largos se ven mal (compromiso SEO/UX).
- No tocar el nombre oficial de un producto o programa; revisar la nomenclatura con el cliente. Un H1 duplicado se corrige **a nivel de plantilla**, no página a página.
- **H2 en forma de pregunta** para landings de servicio, ciudad o industria (lista de 21 variantes usada como plantilla) más los módulos a añadir (instituciones, ciudades). «Humanizar» una landing: texto natural en el idioma de la audiencia, sin rebuscar, con enlaces, módulos y FAQs hiperpersonalizadas.
- **Taxonomías y categorías del blog:** plantilla única de archivo administrable, tarjetas, paginación y mensaje de vacío estándar. Si se dejan indexables categorías vacías, marcarlo como **riesgo de contenido delgado** y documentar el motivo y la alternativa (`noindex` hasta tener entradas). Verificar en el código fuente, no en el inspector.
- **SEO + CRO en on-page:** CTA claro por tipo de página, banners de conversión, página de gracias para medir y mapas de calor sobre las transaccionales prioritarias.


## Procedimiento de redacción (SEO Skills, 2026-10-30)
Para producir title y metadescripción de forma repetible (tres opciones, conteo de caracteres, reglas de puntuación, límites por tanda y salida estructurada), ver [title-and-description-generation.md](title-and-description-generation.md). Ojo con los rangos: uno es el de **auditoría** (title 30 a 60, descripción 70 a 160) y otro el de **redacción** (title 45 a 55, descripción 150 a 160, nunca más de 165). La regla del cliente manda sobre ambos.
