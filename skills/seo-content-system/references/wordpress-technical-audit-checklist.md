# Checklist de auditoría técnica WordPress + servidor [ClickUp]

Origen: una tarea interna de auditoría técnica (generalizada). Úsala cuando el sitio esté en WordPress y la auditoría abarque plugins, seguridad y carga, no solo el SEO on-page. Los hallazgos se priorizan como Crítico, Medio o Bajo.

1. **Infraestructura y hosting**:
   - tipo de hosting (shared, VPS, cloud o dedicado) acorde al tráfico;
   - PHP ≥ 8.1;
   - recursos suficientes;
   - servidor optimizado (Apache, Nginx o LiteSpeed);
   - CDN;
   - SSL sin contenido mixto;
   - caché de servidor;
   - backups automáticos verificados.
2. **Core**:
   - WordPress actualizado;
   - `WP_DEBUG` desactivado en producción;
   - prefijo de base de datos personalizado;
   - `wp-config.php` bien configurado;
   - revisiones de posts limitadas;
   - transients limpios;
   - WP-Cron sustituido por un cron real si hace falta.
3. **Plugins**:
   - número justificado y todos actualizados;
   - sin plugins abandonados ni con funciones duplicadas;
   - plugins pesados detectados e impacto en el rendimiento evaluado;
   - críticos identificados (SEO, caché, seguridad);
   - sin conflictos.
4. **Tema**:
   - con soporte;
   - child theme si hay personalización;
   - HTML semántico;
   - CSS y JS optimizados;
   - page builder con mesura;
   - scripts cargados solo donde se usan.
5. **Rendimiento / CWV**:
   - TTFB, LCP, CLS e INP;
   - imágenes en WebP o AVIF con lazy load (tope de 100 KB por imagen, ver `image-seo-and-accessibility.md`);
   - minificación;
   - sin recursos que bloqueen el render;
   - caché de navegador;
   - precarga de fuentes y recursos críticos.
6. **SEO técnico**:
   - meta robots;
   - robots.txt;
   - sitemap XML;
   - URLs limpias;
   - canonical;
   - 301 bien configuradas;
   - páginas huérfanas;
   - 404 y 5xx;
   - schema;
   - hreflang.
7. **Seguridad**:
   - protección contra fuerza bruta;
   - roles y permisos (cuántos usuarios hay y con qué rol);
   - usuarios inactivos por más de 6 meses señalados para eliminarlos;
   - wp-admin protegido;
   - WAF;
   - escaneo de malware;
   - archivos críticos protegidos;
   - sin vulnerabilidades conocidas.
8. **Base de datos**:
   - tamaño;
   - tablas huérfanas;
   - revisiones;
   - transients;
   - logs;
   - índices.
9. **UX técnica y accesibilidad**:
   - navegación;
   - formularios;
   - mensajes de error;
   - mobile;
   - WCAG A/AA.
10. **Integraciones y tracking**:
    - GTM y GA4 con eventos y conversiones;
    - formularios conectados al CRM;
    - scripts de terceros controlados;
    - APIs y webhooks estables.
11. **Escalabilidad y riesgos**:
    - hosting escalable;
    - dependencias documentadas;
    - puntos únicos de falla;
    - plan de contingencia.
12. **Entregables**:
    - resumen ejecutivo;
    - hallazgos priorizados;
    - impacto en SEO, rendimiento y negocio;
    - quick wins;
    - roadmap técnico.

La auditoría no pide ni guarda contraseñas. Los accesos los gestiona una persona (ver `AGENTS.md` del proyecto).

## Trampas de WordPress con Elementor Pro [Obsidian]

Origen: una auditoría real con rastreador y API, traducida de otro constructor a Elementor. Las trampas 1-8 son específicas de Elementor; las de medición (rompecachés, `page` frente a `query`, distribución del enlazado) son agnósticas y viven en [measurement-traps-and-diagnosis.md](measurement-traps-and-diagnosis.md).

| Otro constructor | Elementor Pro |
|---|---|
| Plantillas de contenido | Theme Builder (Single, Archive, Header, Footer, Loop Item, Popup) + `elementor_library` |
| Elementos en meta serializado | `_elementor_data` (JSON en postmeta), **no** `post_content` |
| Estilos por clase | CSS cacheado por post en `uploads/elementor/css/`: hay que regenerarlo |
| `heading` con su etiqueta | Widget Heading con su propia etiqueta HTML |
| Bloque con bucle y consulta | Widget Posts / Loop Grid con su consulta |

1. El contenido **no está en `post_content`**: Elementor lo guarda como JSON en `_elementor_data`. Añadir HTML a `content.raw` por REST no aparece en el frontend. Para leer la estructura hay que parsear ese JSON.
2. El Theme Builder equivale a las plantillas: un arreglo hecho solo en la página **se revierte** si el elemento viene de una plantilla (Single, Archive, Header, Footer, Loop Item, Popup). Buscar también en `elementor_library`, en plantillas guardadas y en contenedores globales.
3. Elementor cachea el CSS por post. Tras cambios estructurales, regenerar CSS y datos, o se verá el sitio viejo y se concluirá, mal, que el cambio falló.
4. El widget Heading tiene su propia etiqueta: un nombre de persona, un precio o un banner puede estar marcado como H2. Auditar **qué texto** lleva cada nivel, no solo cuántos hay.
5. Antes de bajar un encabezado a `div`, mirar si tiene hijos: si cuelgan H3, quedan huérfanos y se crea un salto de nivel.
6. Al editar un texto, conservar el HTML interno: reemplazar un `<span>` con estilo por texto plano destruye el tratamiento tipográfico.
7. El widget Posts / Loop Grid tiene una consulta configurable. Sin taxonomía ni orden es donde nace el sumidero de enlazado interno.
8. Elementor genera muchos wrappers: no confundir la profundidad del DOM con jerarquía semántica; mirar los encabezados, no los `div`.
9. Comprobar si hay más de una fuente emitiendo Open Graph (plugin SEO, tema y complementos a la vez).
10. Revisar si el plugin SEO transforma lo servido: opciones como «capitalizar títulos» cambian el frontend aunque la base de datos esté bien.
