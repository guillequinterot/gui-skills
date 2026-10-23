---
tags:
  - seo
  - ecommerce
  - shopify
  - multipais
---

# SEO de e-commerce multipaís (Shopify, programático y rendimiento) [ClickUp 2]

Origen: un proyecto de e-commerce de dos o más países con cambio de dominio (auditoría por hallazgo, arquitectura, programático, migración) y un plan técnico de rendimiento y seguridad de 20 tareas (anonimizado). Complementa [technical-audit-by-finding.md](technical-audit-by-finding.md), [programmatic-and-local-seo.md](programmatic-and-local-seo.md) y [migration-redirects-and-validation.md](migration-redirects-and-validation.md).

## Índice

- Hallazgos típicos de Shopify
- Esqueleto de tarea por hallazgo y calibración
- Arquitectura multipaís
- Plantillas y módulos de contenido
- Programático de e-commerce
- Plan de rendimiento y seguridad en 20 tareas
- Secuencia de un proyecto multipaís
- Migración de e-commerce

## Hallazgos típicos de Shopify

Observados en una auditoría real (con prioridad y nº de URLs en la hoja de auditoría):

| Hallazgo | Prioridad | Corrección esperada |
|---|---|---|
| 302 en URLs con impresiones y clics en GSC, y en cualquier URL de la estructura antigua sin prefijo de idioma | Alta | Cambiar a 301 para transferir historial |
| Redirección rota: ruta antigua que lleva (302) a una ruta con prefijo de idioma que da 404 | Alta | Crear la página si debe existir o apuntar a una URL válida (p. ej. la colección principal) |
| Enlaces internos rotos por **errores de Liquid** en secciones del tema (404 con el error visible) | Alta | Revisar las secciones del tema que generan los enlaces |
| Fichas duplicadas de **venta directa frente a preventa/reserva** | Alta | **Una sola URL viva por producto** según el stock real: si ya hay stock, la de reserva redirige 301 a la de venta; si sigue en preventa, al revés. Depende de una decisión del cliente (estado real de stock) |
| Sitemap índice cuyas versiones «raíz» listan URLs antiguas que redirigen | Alta | Configurar mercados/generador para listar las URLs finales, o eliminar el sitemap raíz si el mercado por defecto ya es el idioma principal |
| Slug con «-copia» y contenido de otro producto | Media | Reorganizar la URL, redirigir la duplicada y completar el contenido (requiere información correcta del cliente) |
| hreflang: destino sin 200, sin enlace de vuelta, sin autorreferencia | Media | **Una sola tarea con tres hallazgos**: cada página declara hreflang hacia su propia URL en cada idioma, no siempre al home; verificar con rastreo directo |
| Meta description duplicada entre fichas / ausente en páginas indexables | Media | Corregir desde la plantilla por qué se repite; proponer e implementar |
| Títulos de más de 60 caracteres | Media | Proponer e implementar (y anotar si la hoja nombra mal la columna) |
| H2 ausente en páginas indexables | Media | Añadir al menos un H2 en la plantilla de producto («Características», «Especificaciones») |
| H2 vacío, más de un H1, páginas no indexables, directivas noindex/nofollow | Baja | Dejar un H1 y pasar el segundo a H2; confirmar fila por fila que cada exclusión es intencional |

Diferencias propias de la plataforma: `pages/` para páginas agrupadoras frente a `collections/` para grupos de productos; un sitio por país frente a mercados (verificar la capacidad real de la plataforma antes de prometer). **Ocultar menús por IP no sustituye a hreflang** y se parece a servir contenido distinto al rastreador: comprobar antes de proponerlo.

## Esqueleto de tarea por hallazgo y calibración

`Cliente` → `Origen` (hallazgo, fecha de la auditoría, herramienta, prioridad, nº de URLs) → `Hoja` (libro, pestaña «Hallazgos» y la pestaña propia) → `Qué pasa` (solo en los complejos) → `Qué se espera` (acción concreta, separada por rol) → `Responsable según la hoja` (o «la hoja no nombra a nadie, asignación propuesta, por confirmar»).

- **División de trabajo:** SEO técnico **propone** (títulos y metas nuevos, plan de redirecciones, decisión de URL viva, listado de URLs afectadas); desarrollo **implementa** (plantilla, tema, redirecciones, configuración del sitemap).
- **Criterio de hecho — hueco observado:** ninguna de las 15 tareas leídas lo declaraba. Añadirlo siempre: URL corregida **y revalidada con rastreo**, pestaña del libro actualizada, y re-auditoría que muestre el avance (ejemplos reales: H1 faltante de 6 a 2 páginas; títulos largos de 12 a 5).
- **Calibración orientativa:** Alta 0,5-2 h; Media 1-2 h; Baja 1-2 h.
- **No silenciar inconsistencias de la hoja** (una columna que dice «metadescripciones» en un hallazgo de títulos, un hallazgo sin responsable): resolver con criterio y **dejar la nota escrita**.
- Escalonar fechas con un criterio visible (las Alta primero), no al revés.

## Arquitectura multipaís

- **Marca sombrilla** con líneas de producto como submenús y home propio; qué va en cada país (p. ej. un país con todo, otro con una sola línea, otro con un solo producto y landing propia).
- **Módulos globales frente a variables por país** (copys, precios, medios de pago, FAQ).
- **Venta consultiva** (máquinas: formulario, WhatsApp, ficha técnica, beneficios, retorno) **frente a venta masiva** (productos): dos fichas distintas.
- En producto masivo, **una sola URL con selector de tamaño y color** para evitar canibalización (no una URL por variante).
- **Validar las categorías contra la intención de búsqueda** en vez de copiar el listado del cliente; entregable: estructura de categorías recomendada.
- Auditoría, KWR, metadatos, redirecciones, píxel y pasarelas **por país**.
- Insumos comestibles o accesorios cuelgan de la marca principal; garantías en el pie solo para equipos; repuestos dentro de la línea.

## Plantillas y módulos de contenido

- **Plantillas de contenido de e-commerce:** producto, categoría, agrupadora, nosotros e instructivos. Regla: los cambios SEO se **resaltan en otro color** para pasar a producción.
- **Matriz de fichas de producto** (hoja): keyword principal, nombre, descripción corta y larga y demás campos; **fuente única** para maquetación. Las tareas apuntan a una pestaña, no copian los datos.
- **Módulo de FAQ de producto «en bloque»** (no acordeón) de 8-10 preguntas con términos locales (país, ciudades, envíos), más 4-5 módulos nuevos (garantía, gestión, quién la usa, para qué es ideal, calidad).
- **Biblioteca de diez intenciones de FAQ de producto** (cada una con una nota interna del porqué): para quién es y qué experiencia necesito · qué puedo hacer que no pueda a mano · cuánto tiempo y dinero ahorra (retorno percibido) · compatibilidad con los materiales que ya uso · qué revisar antes de comprar (potencia, capacidad, voltaje, garantía) · calidad profesional frente a doméstica · espacio necesario · si vale la pena empezando el negocio · qué dicen otros usuarios (prueba social) · mantenimiento a largo plazo (poscompra).
- **Biblioteca de módulos** para páginas informativas rápidas: equipo, banners transaccionales, sucursales, galería de videos, descarga de guía (checklist o PDF), carrusel de blog.
- **Módulos de confianza:** reseñas (red social, LinkedIn, Google), testimonios en video, fotos de clientes, validadores; tono que reduzca el miedo a invertir en una máquina.
- Error a evitar: listas de «páginas a optimizar» con **URLs repetidas**; texto de relleno («lorem ipsum») en páginas publicadas. Verificar ambos en el QA.

## Programático de e-commerce

- Prototipo en **HTML plano** desde la plantilla de producto: título, párrafo, botón y módulos por bloque; **sin** desplegables, acordeones ni imágenes con efectos; módulo de **barrios por ciudad** para SEO local; primero móvil.
- **Fuente única:** la matriz de fichas. Ajustes por perfil de comprador y por manual de marca.
- Decisión «landing o programático» antes de construir.
- **Compuerta: STOP hasta que el cliente apruebe la visual.** Sin esa aprobación el trabajo queda detenido, no «estancado».

## Plan de rendimiento y seguridad en 20 tareas

Una hoja de auditoría de rendimiento y seguridad se convierte en un plan de tareas numeradas («tarea N de 20») con un esqueleto uniforme:

`Contexto` (qué auditorías lo originan, nº de tareas, semanas) → `Qué se encontró` (hallazgo con métrica) → `Por qué importa` (impacto y severidad) → `Qué hacer` (a veces con la directiva exacta) → `Datos de referencia`: área · semana · fecha sugerida · fase · severidad · tiempo estimado · responsable sugerido **por rol** · depende de / precede a / complementa a → cierre: «dejar acá los soportes» y «la fecha real y el tiempo los define la cuenta».

- **Fases:** despliegue directo · preparación + despliegue · validación · cierre. **Severidad:** crítica · alta · media · baja-media.
- **Orden de ataque:** revisión de recursos del hosting → caché de servidor → base de datos → imágenes (WebP/AVIF, inventario por peso, primero lo visible sin scroll) → CLS (`width`/`height`, espacio fijo para banners, animaciones no compuestas) → fuentes y precarga del banner (LCP) → minificación y diferimiento de JS/CSS (`async`/`defer` en píxeles, mapas, chats) → accesibilidad y áreas táctiles → validación → documentación y cierre.
- **Seguridad del mismo plan:** ocultar versiones de PHP/servidor; restringir por IP con 2FA el acceso a un plugin que expone datos; CSP **primero en Report-Only** y luego en producción; HSTS persistente (directiva `always` para que viaje también en páginas de error); WAF perimetral con cambio de DNS (empezar temprano por la propagación); re-escaneo de validación.
- **Validación:** volver a ejecutar las **mismas herramientas** de la línea base y comparar antes/después, y comprobar que formularios, sliders, menús, GTM y píxeles siguen funcionando. Cierre con informe al cliente.
- **Línea base de ejemplo** (para calibrar prioridades): rendimiento móvil 43/100 y escritorio 33/100; TTFB hasta 5,5 s; LCP 27 s en móvil; CLS 0,29; ~2,1 MB de JS sin usar; ~2,7 MB ahorrables en imágenes.
- **Lección:** el plan se programó para 4 semanas y se fue a tres meses; dos cambios de 15-30 minutos quedaron estancados esperando acceso al servidor. Registrar los accesos como dependencia del cliente desde el día 1.

## Secuencia de un proyecto multipaís

1. Auditoría y su presentación.
2. Investigación de mercado SEO (competidores directos y sustitutos por país) y validación de categorías frente a intención.
3. Arquitectura de home y ficha; análisis de competidores; plan SEO a un año con cronograma (incluye redirecciones); KWR por país.
4. Socialización interna y presentación de entregables al cliente.
5. Kickoff formal (el diagnóstico y la estrategia pueden entregarse antes del arranque).
6. Prototipos, UI kit y matriz de fichas; programático (con su compuerta).
7. Metadatos y contenido on-page con re-auditoría; GBP; módulos y páginas informativas.
8. Si el proyecto se pausa y se reactiva: **nueva auditoría con ganancias tempranas** antes de seguir.
9. Sprint con el cliente (quincenal) y sprint interno.

## Migración de e-commerce

Entorno en el nuevo dominio con respaldo; espejo para el segundo país; validaciones técnicas en dos partes; **QA triple posmigración** con chequeos puntuales: cabeceras (headers), páginas sin H1, H1 no secuencial, imágenes de más de 100 KB, 404, sitemap + rastreo, caché del servidor y redirecciones por país. Checklist de migración de tienda con ítems previos y posteriores al lanzamiento (página personalizada, favicon, píxeles, pasarelas por país). Más en [migration-redirects-and-validation.md](migration-redirects-and-validation.md).
