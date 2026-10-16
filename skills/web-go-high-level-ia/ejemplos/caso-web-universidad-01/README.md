# Ejemplo · caso-web-universidad-01 (versión sanitizada)

Caso real que dio origen a la skill: sitio de una campaña de inscripciones de una universidad, construido en el
constructor de IA de GoHighLevel (TanStack Start + React + Tailwind v4 + CSS propio de la marca) a partir de un
diseño aprobado en HTML. Aquí solo quedan **los patrones reutilizables**, con datos inventados. El código, los
textos, las fotos, los datos de contacto y los identificadores del proyecto del cliente viven únicamente en el
equipo del mantenedor y no se publican.

## Qué contiene esta carpeta

| Archivo | Qué enseña | Incidencias / referencias |
|---|---|---|
| `datos-modulo.ejemplo.ts` | Un solo módulo de datos: configuración, `img()` con base única, `siteUrl()`, enlace de mensajería con respaldo, listado tipado, `initTracking()` con un listener global para `data-track` | C2, C7, `references/05` |
| `img-map.ejemplo.ts` | `IMG_MAP`: la única relación «nombre original → URL del CDN» (el CDN renombra los archivos) | D1, `references/05` |
| `ruta-con-filtros.ejemplo.tsx` | Listado con filtros en la URL (`validateSearch`), estado vacío específico y respaldo de imagen con `onError` | J3, J4, K7 |
| `gen_datos_desde_csv.ejemplo.py` + `datos.ejemplo.csv` | Un generador CSV → módulo TypeScript que aplica las reglas de datos del cliente al generar | J2, K1 |
| `partes.ejemplo.json` | Configuración de ejemplo para `scripts/make_partes.py` (archivos nuevos, «reemplaza todo», «añade al final») | `references/02`, K9, H |

## Qué se hizo en el caso (línea de tiempo, 2026-10-13 a 2026-10-15)

1. **Preparación:** carpeta del proyecto organizada, fuentes del cliente leídas, fotografías reales verificadas,
   resumen de marca y handoff/handshake.
2. **Diseño:** UI kit y Home en HTML (1920 de lienzo, 240 de márgenes, 80 por sección, múltiplos de 4),
   revisión visual con Chrome headless y cambios del usuario (menú a páginas internas).
3. **Entrega al constructor** en «partes» de ≤ 50 000 caracteres con capturas de referencia.
4. **El constructor generó la Home** con las alturas del HTML; se corrigió el choque de `.container` con Tailwind.
5. **Auditoría del código descargado** (hallazgos C1–C10 de `references/07`).
6. **Mejoras locales** con respaldo previo: módulo de datos único, shell común en `__root.tsx`, 404 y error en
   español, metadatos sin afirmaciones inventadas, `<Link>`, corrección del carrusel, medición real con
   `data-track`, formulario único reexportado, rutas provisionales con `noindex`, `AGENTS.md` y `README.md` vivos.
7. **Pegado manual de 22 archivos** por portapapeles y verificación en la vista previa real.
8. **Imágenes por Medios:** carpeta por entrega, CDN que renombra, 32/32 URL emparejadas por SHA-256.
9. **Rondas posteriores:** QA de contenido y de CSS responsive (tablet/móvil), listado con filtros en la URL y
   ficha dinámica, contenido largo desde fuentes oficiales (≤ 50 000 caracteres por parte), operación del
   constructor con Claude in Chrome (46/46 comprobaciones en la vista previa pública).
10. **Giro del cliente (2026-10-15):** se descartaron las fichas internas y se resumió cada elemento en un
    módulo del listado; la skill documenta que una estructura aprobada puede cambiar y que no se ejecutan
    cambios de estructura hasta que el responsable los autorice.

## Qué se descartó al anonimizar (y dónde queda la lección)

| Archivo original | Por qué no se copia | Dónde queda la lección |
|---|---|---|
| `AGENTS.md` y `README.md` rellenados del proyecto | Contienen contenido, decisiones y pendientes del cliente | `templates/AGENTS.template.md` y `templates/README.template.md`; `references/03` |
| Módulos de datos, de textos largos y de oferta del cliente (`*-data.ts`, `*-programas*.ts`, `*-oferta.ts`) | Datos y textos del cliente | `datos-modulo.ejemplo.ts`, `gen_datos_desde_csv.ejemplo.py`, `references/07` J y K |
| Componentes de marca (cabecera, pie, secciones, listado) | Texto, marca y estructura del cliente | `references/03` (qué va en cada capa) y `ruta-con-filtros.ejemplo.tsx` |
| Generadores de partes específicos de cada entrega (3 scripts) | Rutas, textos y comprobaciones del cliente | `scripts/make_partes.py` genérico + `partes.ejemplo.json` |
| `extraer_contenido_programas.py`, `textos-elaborados.json`, `gen_qa_home_*.py` | Extractor y datos de las páginas oficiales del cliente | Regla en `references/07` K2–K5: textos literales de la fuente oficial, rotulados, con fuente y fecha |
| `gen_oferta.py` (oferta completa de 150 filas con enlaces rastreados a mano) | Datos y enlaces del cliente | Mismo patrón que `gen_datos_desde_csv.ejemplo.py` |
| Fotografías, logos y capturas | Material del cliente | `references/05` (flujo de imágenes) |
