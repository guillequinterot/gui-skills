# Metodología operativa de agencia [ClickUp]
Origen: patrones de unas 4.850 tareas (paginación completa, 2022–2026) y 59 leídas a fondo en ClickUp, anonimizados.

## Fases y listas por contrato
1. **Fase inicial:** accesos (GSC, GA4, GTM, CMS, Screaming Frog), entendimiento del negocio, auditoría técnica, estrategia, game plan y keyword mapping.
2. **Operación mensual:** sprint quincenal, correcciones por hallazgo, contenido, informe mensual.
3. **Bolsa de expansión y mercados:** nuevos países o idiomas (hreflang), programático.
4. **Dependencias del cliente:** insumos, aprobaciones, entrevistados, fotos. Se registran como tareas bloqueantes.
5. **Solicitudes y control de alcance:** cada pedido se asocia a una cláusula y se indica si entra en el fee.

Ciclo de crecimiento (variante GDD): Entendimiento → Estrategia → Launchpad → Dashboard → Mejoras continuas → Handoff de operaciones.

## Cadencia
- Reunión semanal o quincenal con acta. Cada acuerdo se convierte en tarea.
- Sprint quincenal.
- Informes: mensual, de rendimiento después de las implementaciones, y semestral.

## Contenido
- **Flujo:** game plan → KWR → redacción → portada → CMS → enlazado interno o módulo de relacionados.
- **Fuentes:** entrevistas con expertos (EEAT), podcast, video y conferencias.
- **Multiformato:** blogpost, presentación, resumen ejecutivo, tabla de datos e infografía.

## Link building
1. Matriz de notas en medios.
2. Resumen de prensa con enlaces al home, a la nota original y a 1–2 servicios.
3. Newsletter de LinkedIn.
4. Publicación en GBP.

## Roles y flujo de una landing
- **Roles:** account (brief, aprobación), contenido, diseño UI, front, SEO técnico (formularios, GA4 y eventos de píxel), QA.
- **Flujo:** brief → copy → UI → maquetación → medición → QA interno → ajustes → envío al cliente → ronda 1 de ajustes.
- **Criterio de hecho:** publicada, formulario probado con el evento registrado, QA cerrado y aprobación escrita del cliente.

## Migración
- QA por prioridad (Crítico/Alto/Medio/Bajo/Neutral).
- En el lanzamiento: redirecciones, GA4, GSC, GTM, HTTPS y cabeceras, nomenclatura de URLs.
- Chequeos post-migración.

## Ver también
- `onboarding-and-initial-audit.md` · `growth-driven-design-gdd.md` · `clickup-task-operating-model.md` · `migration-redirects-and-validation.md` · `wordpress-technical-audit-checklist.md`


## Ampliación [ClickUp 2]

Origen: lectura de listas de tres años, de un contrato por fases y de plantillas GDD (anonimizado; cobertura parcial, ver `docs/INVESTIGACION-CLICKUP-SEO.md` §23). Detalle en [contract-phases-and-scope-control.md](contract-phases-and-scope-control.md), [launch-checklist-new-site.md](launch-checklist-new-site.md), [ecommerce-seo-multicountry.md](ecommerce-seo-multicountry.md) y [education-program-seo.md](education-program-seo.md).

### Fases de un contrato (variante observada)
Accesos y entendimiento → investigación en paralelo (~2 semanas: KWR, benchmark, competidores, auditoría UX, dashboard, GSC/GA4 en subdominios) → cronograma de estrategia y OKR → socialización → optimización de lo existente (metadatos, encabezados, rendimiento, 404, sitemap, enlazado, CTA, mapas de calor) → producción de landings (geolocalizadas, por industria, por evento) → gobernanza (reunión semanal, SEO quincenal, informes) → capacitación al equipo que despliega. Una reunión de revisión interna **antes** de mostrar entregables al cliente.

### Reparto y secuencia de un sprint de lanzamiento
SEO de contenido (keywords, textos, metas, alt) separado de SEO técnico + analítica (especificación, medición, QA); el texto bloquea al diseño; validar el render con desarrollo antes del prototipo; entrega al cliente y revisión a los 7 días. Ver [launch-checklist-new-site.md](launch-checklist-new-site.md).

### Contenido y venta
- **Artículo + versión LinkedIn** como entregable estándar por artículo propio; **pipeline podcast/episodio → artículo → imágenes → LinkedIn → PDF de recursos → programas relacionados**.
- **Gestión por matriz de colores** de aprobación (verde aprobado · azul comentarios por atender · naranja ajustado y listo para reenviar · amarillo/rojo/rosado pendientes) y columna «implementado».
- Rutina de cambios del cliente: el cliente envía ajustes por correo, PDF o grabación → la PM crea tareas → quien ejecuta devuelve una **captura por punto**.
- **Auditoría comercial a un prospecto:** hoja completa + presentación resumida sin marca; **exploración de un CMS ajeno en 8 puntos** (solo explorar, nunca modificar) con entregable de 4 secciones y lista de dudas para el contacto. Los accesos de un CMS ajeno nunca viajan por mensajería ni en la tarea.
- **SEO + CRO:** mapas de calor, CTAs por tipo de página, banners de conversión y enlazado, página de gracias para medir conversión, pruebas A/B sobre las páginas transaccionales prioritarias; refresco de casos de éxito (filtro por industria, tarjetas con métrica, testimonios con retrato).
- **Biblioteca de módulos** (equipo, banners, sucursales, galería de videos, descarga de guía, carrusel de blog) como activo de diseño y SEO.

### Link building: variantes
- Artículo de nota de prensa en variante larga (1.400-1.700 palabras) con enlaces obligatorios y opcionales.
- **Cadena de publirreportajes:** plan de compra → plan de redacción → redacción → revisión → compra → registro, con presupuesto por enlace y plataforma. Estimar con holgura: el esfuerzo se subestimó varias veces.
- **Alerta de política de enlaces:** un ranking propio con enlace *do-follow* con UTM hacia terceros, o un enlace pagado, puede ser esquema de enlaces; usar `rel="sponsored"` o `nofollow` y documentarlo.
- Plan de medios de bajo costo por país (ver [contract-phases-and-scope-control.md](contract-phases-and-scope-control.md)); antes de comprar enlaces, consolidar el mercado piloto.

### Estimaciones (orden de magnitud, no compromiso)
Título/meta de un lote 1-2 h; KWR 2,5-3 h; benchmark 2 h; competidores 0,5-3 h; auditoría UX 6 h; mapas de calor 4 h; optimización de contenido por URL 1 h; artículo + versión LinkedIn ~2,3 h; optimización semántica ≥ 2 h por artículo; montar un programa en el CMS ~40 min; dashboard 15 h + 2 ajustes de 1 h. Las tareas de «ajustes» se reabren: dar holgura.
