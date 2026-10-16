# 08 · Caso de referencia: caso-web-universidad-01 (campaña de inscripciones)

Proyecto de una agencia para una universidad: sitio de campaña en el constructor de IA de GoHighLevel. La
carpeta del proyecto y las notas del caso viven en el equipo del mantenedor, fuera de este repo (la
equivalencia código → cliente está en `~/.gui-skills/equivalencias.md`). Aquí queda solo lo aprendido.
Ejemplos sanitizados del código: [`../ejemplos/caso-web-universidad-01/`](../ejemplos/caso-web-universidad-01/README.md).

## Línea de tiempo (2026-10-13 a 2026-10-15)
1. Preparación: carpeta organizada, fuentes del cliente leídas, fotos reales verificadas, marca resumida, handoff/handshake.
2. Diseño: UI kit y **Home v1** en HTML, revisión visual con navegador headless. Cambios del usuario: menú a páginas internas; un bloque de ubicaciones en carrusel.
3. Entrega al constructor: sistema de **partes** (script propio del proyecto; hoy genérico en `scripts/make_partes.py`) → carpeta `entrega-1-home/`.
4. El constructor generó la Home (alturas idénticas a las del HTML). Se corrigió `.container`.
5. **Auditoría** del código descargado: ver hallazgos en [07](07-incidencias-y-soluciones.md) C1-C10.
6. **Mejoras locales** (con respaldo `_backup-original`): módulo de datos único (`img()`, `siteUrl()`, enlace de mensajería, `initTracking()`), shell a `__root.tsx`, 404/error en español, metadatos neutros, `<Link>`, bug del carrusel, formulario reexportado, 5 rutas provisionales con `noindex`, `AGENTS.md` y `README.md` vivos.
7. **Pegado manual** de 22 archivos con portapapeles ([04](04-transferencia-editor-portapapeles.md)); verificación en la vista previa (12 secciones, un `h1`, un header/footer, rutas 200, 404 en español).
8. **Imágenes:** carpeta de la entrega → Medios; el CDN renombra; 32/32 URL verificadas por SHA-256.
9. **QA de contenido y responsive** (sección nueva, FAQ completa, desbordes en móvil/tablet): [07](07-incidencias-y-soluciones.md) H e I.
10. **Listado con filtros en la URL y ficha dinámica**, contenido largo desde fuentes oficiales ([07](07-incidencias-y-soluciones.md) J y K) y primera operación del constructor con Claude in Chrome ([07](07-incidencias-y-soluciones.md) L).
11. **Giro del cliente (2026-10-15):** se descartaron las fichas internas y cada elemento se resumió en un módulo del listado. Lección: una estructura aprobada puede cambiar; las ideas «en espera de luz verde» no se ejecutan hasta que el responsable las autorice.

## Decisiones del caso que sirven de patrón
- Identidad visual con tipografías y color propios en un CSS único; solo fotografía real de la marca (sin stock ni filtros).
- El menú principal lleva a **páginas internas**, no a anclas.
- Datos con contradicciones entre fuentes del cliente (códigos oficiales, cifras de cupos): **no se muestran** hasta confirmarlos; los cupos nunca se suman.
- Lenguaje claro, trato de «tú», sin promesas (admisión, gratuidad, empleo).
- Pendientes del cliente siempre como marcador visible `.placeholder` y anotados en el README del proyecto: contacto de mensajería, testimonios, redes, CRM definitivo, medición (Clarity/GA4), dominio.

## Qué reutilizar en otro proyecto de GHL AI Studio
1. `templates/AGENTS.template.md` y `templates/README.template.md`.
2. `scripts/make_partes.py`, `scripts/manifest_imagenes.py` y `scripts/match_cdn.py`.
3. Receta de transferencia ([04](04-transferencia-editor-portapapeles.md)) y tabla de incidencias ([07](07-incidencias-y-soluciones.md)).
4. Los patrones de código de `ejemplos/caso-web-universidad-01/`.
