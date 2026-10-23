# Lineamientos de SEO técnico, indexación y resultados enriquecidos · {sitio} [Drive]
1. **URL y arquitectura:** `a-z 0-9 -` · 80 caracteres o menos · sin stop words ni IDs dinámicos · `<a href>` real · 3–4 niveles (Home › Categoría › Subcategoría › Ficha) · tabla estándar vs. mala práctica
2. **Canonical y servidor:** canonical absoluta HTTPS · 301 HTTP→HTTPS y no-www→www · 301 ante cambios de ruta · sin contenido mixto · parámetros bajo control
3. **hreflang:** recíproco · ISO 639-1(-ISO 3166-1) · `x-default` · en el head o en el sitemap
4. **Home:** title de 50–60 · meta de 140–155 · `index,follow,max-image-preview:large` · HTML5 semántico · un H1 · OG/Twitter · JSON-LD `@graph` Organization + WebSite (si Rank Math o Yoast ya los generan, completar por ajustes o el filtro `rank_math/json_ld`, no con bloques manuales; son ajustes globales)
5. **Ficha/PDP:** `Producto - Variante | Marca` · H1 = nombre oficial · imágenes: hero de 150 KB o menos, contenido de 100 KB o menos, miniatura de 30 KB o menos · WebP/AVIF · alt · width/height · hero eager + fetchpriority high, resto lazy · JSON-LD Product (sin precio público: solo `SoftwareApplication` para software, nunca `Offer` vacío ni `price` 0; sin marcadores dentro de campos)
6. **Rendimiento:** SSR/SSG · LCP < 2,5 s · INP < 200 ms · CLS < 0,1 · defer/async · caché + CDN · sin interstitials
7. **Rich results:** FAQPage, BreadcrumbList, Article/BlogPosting, VideoObject
8. **Checklist final**

| Categoría | Ítem | Requisito aceptable | Estado | Responsable |
|---|---|---|---|---|
| Indexabilidad y servidor | robots.txt | Bloquea QA y URL dinámicas, no bloquea CSS/JS | | |
| Indexabilidad y servidor | Sitemap XML | Solo URL 200 canónicas | | |
| Meta y contenido | Title/meta | Únicos y dentro del límite | | |
| Seguimiento | GSC/GA4/GTM | Instalados sin conflicto | | |
| Rendimiento | CWV | En verde | | |
| HTML5 | Encabezados/nav | Un H1, `<nav>` | | |
| Datos estructurados | JSON-LD | Sin advertencias | | |
