# 06 · SEO / AEO por página dentro del constructor (puente con `seo-content-system`)

`seo-content-system` decide **qué** se escribe (intención, keywords, copy, schema). Esta referencia fija **dónde y cómo** vive eso en TanStack Start.

## `head()` por ruta (plantilla)
```tsx
export const Route = createFileRoute("/pagina")({
  head: () => ({
    meta: [
      { title: "Título único ≤ 60 car. | Marca" },
      { name: "description", content: "120–155 caracteres, lenguaje claro, sin promesas." },
      { name: "robots", content: "noindex" },            // SOLO mientras la página sea provisional
      { property: "og:title", content: "…" },
      { property: "og:description", content: "…" },
      { property: "og:url", content: siteUrl("/pagina") },
    ],
    links: [{ rel: "canonical", href: siteUrl("/pagina") }],
    scripts: [{ type: "application/ld+json", children: JSON.stringify({ /* schema */ }) }],
  }),
  component: PaginaPage,
});
```
- `__root.tsx` solo trae lo común (charset, viewport, `theme-color`, `og:type/locale/site_name`, `twitter:card`) y **no afirma nada** que no esté aprobado. Cada ruta sobrescribe title/description.
- `siteUrl()` y el dominio viven en el módulo de datos (`<P>_CONFIG.siteUrl`); confirmar el dominio definitivo con el cliente antes de indexar.
- URLs **sin barra final** (`/pagina`).

## Qué exige cada tipo de página
| Página | `h1` | Schema | Notas |
|---|---|---|---|
| Home | 1 (promesa de la campaña) | `WebSite`, `Organization` (o el subtipo que corresponda al cliente), `FAQPage` (solo preguntas visibles) | `preload` de la imagen principal con `img()` |
| Agrupadora (listado) | 1 | `ItemList` / `CollectionPage` | filtros en la URL (`search`); estado vacío; enlaza a todas las fichas |
| Ficha | 1 con el nombre del elemento + su ubicación | `Course`, `Product` o el tipo que corresponda + `BreadcrumbList` | datos reales; enlaza al listado, a la ubicación y al trámite principal |
| FAQ | 1 | `FAQPage` | idéntica a lo visible |
| Provisional | 1 | — | `noindex`; quitarlo al publicar el diseño final |

## Reglas
1. **Un solo `h1`**, jerarquía sin saltos; las secciones reutilizadas en otra página no deben duplicar `h1`.
2. Enlaces internos con `<Link>`; texto de enlace descriptivo. Menú = páginas internas (no anclas).
3. **No indexar páginas a medias** (`noindex`). `public/robots.txt` permite rastreo; el sitemap se declara cuando haya dominio.
4. **AEO/GEO:** respuestas cortas y directas al inicio de cada bloque, datos citables (fechas, requisitos) con fuente oficial y aviso «confírmalo con la oficina responsable»; FAQ en lenguaje de las personas.
5. **Lenguaje claro** (guía de la marca) y sin promesas (resultados garantizados, gratuidad, cupos, empleo).
6. Medición: `data-track` + listener global → `dataLayer`/Clarity; GA4/GTM/Clarity se instalan en `RootShell` cuando el cliente entregue los códigos.
7. Imágenes: `alt`, `width/height`, `og:image` absoluta (ver [05](05-imagenes-medios-cdn.md)).
8. Registrar fuentes y aprendizajes en la memoria de `seo-content-system` (`memoria/` de esa skill, o su bóveda si usas Obsidian) según su protocolo; no convertir una sola observación en regla.
