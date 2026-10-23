# Auditoría técnica por hallazgo [ClickUp]
Se abre una tarea por cada tipo de hallazgo y mercado. Cada una indica origen (fecha de la auditoría), prioridad, número de URLs, hoja o pestaña, qué se espera y responsable.

| Hallazgo | Corrección esperada | Prioridad típica |
|---|---|---|
| 302 en URLs con clics o impresiones en GSC | Cambiar a 301 | Alta |
| 4xx, redirecciones o enlaces rotos | Redirigir o corregir el enlace | Alta |
| noindex/nofollow mal puesto (por ejemplo, el blog bloqueado por la plantilla) | index,follow en la plantilla; noindex en login, carrito y reset | Alta |
| Title con menos de 30 o más de 60 caracteres, duplicado, múltiple o fuera del head | Reescribir por tandas | Media |
| Meta description duplicada, ausente o múltiple | Reescribir | Media |
| H1 ausente, múltiple o duplicado; H2 vacío | Corregir la plantilla o el contenido | Media |
| Hreflang a un destino que no da 200, sin vuelta o sin autorreferencia | Cada página declara su par por idioma y se referencia a sí misma | Media |
| Sitemap con URLs que redirigen, entradas duplicadas o páginas que faltan | Revisar el generador o el cron | Media/Baja |
| Imágenes de más de 100 kB, sin WebP o sin alt | Comprimir y documentar | Baja |
| Scripts sin defer/async; slugs duplicados; anchors genéricos | Ajustar | Baja |

**Auditoría de rutas:** cruzar los sitemaps con las páginas clave (HTTP, redirección, canonical, hreflang, lang, presencia en sitemap). Reportar primero lo que está bien y luego los pendientes numerados con "Qué revisar".

**Herramientas:** Screaming Frog (licencia activa), GSC, Python/cURL.

Para la pestaña índice usar `assets/templates/audit-understanding-matrix.md`. Para WordPress, `wordpress-technical-audit-checklist.md`. Para validar las correcciones, `migration-redirects-and-validation.md` (sección "Validar las implementaciones").

## Riesgo y ámbito

Cada hallazgo declara riesgo y ámbito, además de prioridad:

- **Bajo:** una URL, reversible en minutos.
- **Medio:** una plantilla o un grupo de URLs, o reversible solo con respaldo.
- **Alto:** ajuste global (plugin SEO, schema del sitio, robots, sitemap, redirecciones por regla, `sameAs`, cabeceras) o difícil de revertir.

Un cambio de schema que toca ajustes globales del plugin o el filtro `rank_math/json_ld` **nunca es Bajo**: como mínimo Medio, y Alto si cambia la identidad (`@id`, `@type`, nombre, `sameAs`).

## Entrega completa

Toda auditoría se entrega con la matriz completa (`assets/templates/audit-findings-matrix.csv`, sin celdas vacías: `n/a` o `por definir`) y **un brief por hallazgo** (`assets/templates/task-brief.md`) enlazado en la columna «Brief (link)». Un hallazgo sin brief no está entregado.

## Formato de entrega en hoja [Sheets]
Ver `references/sheets-workbook-templates.md` §1 y las plantillas `assets/templates/audit-findings-matrix.csv` y `assets/templates/audit-finding-tab.csv`.
- Orden de pestañas: Resumen → Matriz de entendimiento → Entendimiento gráfico → Hallazgos → Todas las URLs → Categorización por sección → una pestaña por hallazgo.
- Cada pestaña de hallazgo empieza con `⬅ Volver a Hallazgos`.


## Ampliación [ClickUp 2]: criterio de hecho, calibración y casos de plataforma

Origen: 15 tareas de una auditoría de tienda en línea y varias auditorías previas (anonimizado). Hueco encontrado: **ninguna de las tareas por hallazgo declaraba criterio de hecho**; solo «qué se espera».

### Criterio de hecho por tipo de hallazgo
| Hallazgo | Criterio de hecho verificable |
|---|---|
| 302 que debería ser 301 | Un re-rastreo muestra 301 en las N URLs y el destino responde 200 |
| Redirección rota | La ruta antigua llega en un salto a una URL 200; 0 cadenas |
| Título fuera de rango o duplicado | Re-rastreo sin títulos fuera de rango ni duplicados; los nuevos son únicos |
| Meta description ausente o duplicada | 0 ausentes y 0 duplicados en el re-rastreo; la plantilla ya no repite |
| H1 ausente/múltiple, H2 ausente/vacío | N páginas con un solo H1 y al menos un H2 con texto en el re-rastreo |
| hreflang | Cada URL se autorreferencia y tiene retorno; todos los destinos responden 200 (una sola tarea con los tres hallazgos) |
| Sitemap | Solo URLs 200 finales, 0 redirecciones; enviado y sin errores en Search Console |
| Fichas duplicadas | Una URL viva por producto según el stock real; la otra con 301 |
| Enlaces internos rotos | 0 enlaces a 404 desde las plantillas; revisado en rastreo |

Cerrar siempre con una **re-auditoría** que muestre el avance (ejemplos reales: H1 faltante de 6 a 2 páginas; títulos largos de 12 a 5) y con la pestaña del libro actualizada.

### Esqueleto y reparto
`Cliente` → `Origen` (hallazgo, fecha de la auditoría, herramienta, prioridad, nº de URLs) → `Hoja` (pestaña «Hallazgos» y la propia del hallazgo) → `Qué pasa` (solo en los complejos) → `Qué se espera` (por rol) → `Responsable según la hoja` (o «la hoja no nombra a nadie, asignación propuesta, por confirmar»). **SEO técnico propone** (títulos y metas, plan de redirecciones, decisión de URL viva) y **desarrollo implementa** (plantilla, tema, redirecciones, sitemap).

### Calibración
Alta 0,5-2 h; Media 1-2 h; Baja 1-2 h. Escalonar fechas con las Alta primero. **No silenciar inconsistencias de la hoja** (una columna mal nombrada, un hallazgo sin responsable): resolver con criterio y dejar la nota escrita.

### Casos de plataforma
Hallazgos propios de una tienda en Shopify (errores de Liquid, sitemap raíz con 302 por mercados, fichas de venta frente a preventa, slug «-copia», `pages/` frente a `collections/`): ver [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md). Auditoría de rendimiento y seguridad (cabeceras CSP/HSTS, `lang` y `hreflang`, librerías con vulnerabilidades): entrega con un **resumen explícito en comentarios y capturas antes y después**; los datos de campo tardan ~28 días en reflejarse.

### Tarea de Page Speed (plantilla)
Metas TTFB/LCP/FCP → diagnóstico **servidor primero** → plan de 8 pasos con minutos y **respaldo previo** → «qué NO tocar» → entrega antes/después por URL. Detalle del orden de ataque en [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md#plan-de-rendimiento-y-seguridad-en-20-tareas).
