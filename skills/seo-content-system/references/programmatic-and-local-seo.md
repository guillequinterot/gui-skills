---
tags:
  - seo
---

# SEO programático y local

## Índice

- SEO programático
- Matriz
- Calidad
- Indexación
- SEO local
- Páginas de ubicación
- Reseñas

## SEO programático

Crear páginas escalables solo cuando cada combinación responda una necesidad diferenciada y disponga de datos confiables.

Modelo:

```text
Head term × modificador × entidad/dato
```

Ejemplos de modificadores:

- Ubicación.
- Categoría.
- Uso.
- Integración.
- Comparación.
- Industria.
- Atributo.

No asumir que toda combinación merece una URL.

## Matriz

Registrar:

| Plantilla | Entidades | Fuente de datos | Intención | Diferencia útil | Indexar |
|---|---|---|---|---|---|
| Servicio + ciudad | Ciudades atendidas | Operación real | Local/transaccional | Equipo, cobertura, casos | Según calidad |

## Calidad

Evaluar:

- Demanda o necesidad.
- Utilidad específica.
- Datos únicos.
- Contenido editorial.
- Experiencia funcional.
- Enlazado.
- Mantenimiento.
- Riesgo de páginas vacías o duplicadas.

No imponer mínimos de palabras, KD, volumen, número de datos o cantidad de páginas como reglas universales.

## Indexación

Definir estados:

- Generar e indexar.
- Generar con `noindex`.
- No generar.
- Consolidar.

Retirar o consolidar páginas sin utilidad persistente.

## SEO local

Trabajar:

- Relevancia.
- Distancia.
- Prominencia.
- Datos de negocio precisos.
- Categorías y servicios.
- Horarios.
- Ubicaciones reales.
- Reseñas auténticas.
- Enlaces y menciones locales.

No afirmar que un mapa embebido, coordenadas en schema o repetición de ciudad modifica la distancia real.

## Páginas de ubicación

Cada página debe reflejar:

- Dirección o área de servicio real.
- Horarios.
- Contacto.
- Servicios disponibles.
- Equipo o proceso local.
- Evidencia local.
- Cómo llegar cuando sea útil.
- Diferencias operativas.

Evitar reemplazar únicamente el nombre de la ciudad.

## Reseñas

Solicitar reseñas honestas sin dictar keywords. No fabricar ni marcar reseñas no visibles. Responder con información y tono coherentes.



## Auditoría de Google Business Profile [Drive]
Usa una ficha de validación por variable, los atributos SÍ/NO y los productos a publicar: `assets/templates/gbp-audit.csv`. Ver `references/drive-deliverables-and-guidelines.md` §9–10.


## Ampliación [ClickUp 2]: publicación escalonada, logística de landings y GBP

Origen: landings geolocalizadas por país y ciudad de dos cuentas y un programático de e-commerce (anonimizado). Referencias hermanas: [education-program-seo.md](education-program-seo.md) y [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md).

### Publicación escalonada por país o ciudad
1. Subdirectorio por país con **hreflang** (`es-XX` + `x-default`) y **noindex hasta que el redactor edite** la página (evita que salga contenido de otro contexto).
2. Tarea explícita «Colocar INDEX» cuando el contenido propio está listo, y luego «Indexar en GSC» (solicitud por lote).
3. Tarea correctiva de hreflang si hace falta.
4. **QA de residuos de contexto** entre países (nombres de ciudad, moneda, normativa o ejemplos de otro mercado).

### Logística de contenido por ciudad
Brief: servicio · referente (la primera ciudad ya hecha) · objetivo (conversión) · lista priorizada de ciudades **en grupos de 4** · carpeta · archivos nombrados «Servicio | Ciudad» · dos hitos de entrega (primer grupo y total). Una tarea por ciudad para producción, más: textos de barrios (diferenciador local), preguntas frecuentes geolocalizadas, página agrupadora (`/locations` con H1 con servicio y alcance geográfico, párrafo sobre el pliegue, title con marca, meta con beneficio y cobertura, módulos de ciudades), solicitud de indexación por lote, seguimiento semanal recurrente, informe del programático y tarea de «solucionar problema». Programático por modalidad de servicio cuando aplica.

### Landings por evento estacional, ruta y cruce de frontera
Pillar page + una landing por sede + plantilla única; contenido generado con un prompt acordado en reunión y depuración previa de keywords; fecha dura y prioridad alta. Las páginas de ruta (origen → destino) y de frontera comparten plantilla; cambiar el CTA o el pliegue **después** de desplegar generó muchos reprocesos: congelar plantilla y CTA antes de duplicar.

### Multimercado
Con varios países: auditoría, KWR, metadatos y redirecciones **por país**; píxel y pasarelas por país; hoja de personalización por programa y país; guía de contenido por país (oportunidades, industrias, para qué sirve en el año actual). Con una plantilla de CMS que el cliente no puede modificar: solo contenido, sin módulos nuevos. Si el proveedor rompe traducciones por bloques huérfanos, abrir ticket y registrar el bloqueo con fecha.

### Google Business Profile: paso previo
Antes de optimizar una ficha: **documento de variables de la ficha** (categorías, servicios o productos, atributos, fotos) y **lista de requerimientos al cliente** (qué falta). Auditar todas las fichas, definir la sede principal y dejar el listado de acciones e insumos. Crear «productos» en la ficha por categoría de oferta con una imagen por categoría.
