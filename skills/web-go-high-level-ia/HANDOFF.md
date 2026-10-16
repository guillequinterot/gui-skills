# HANDOFF — web-go-high-level-ia

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.

## 1. Qué es y cuándo se usa

Sub-skill propia de `direct-visual-design` (diseño y QA visual) y de `seo-content-system` (title, meta, H1, alt,
schema, `noindex`, enlazado), por decisión del mantenedor del 2026-10-13, para construir y mantener webs dentro del
constructor de IA de GoHighLevel (AI Studio / «Vibe»). Contiene el proceso completo, el registro de incidencias
(`references/07`), scripts, plantillas (`AGENTS.md`, `README.md`), ejemplos sanitizados de un caso resuelto y
fichas de proyecto. Se usa en cuanto el usuario trabaja una web en ese constructor o nombra la skill; su proceso es
obligatorio y completo. Llama a `direct-visual-design` (dirección visual) y a `seo-content-system` (qué se escribe
y se indexa); `canva-design` y `design-illustrator` no intervienen.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano. Ya no existe un
  `install.py` propio de la skill ni una «copia instalada» que pueda desfasarse: se instala por enlace.
- Dependencias externas: cuenta de GoHighLevel con AI Studio; **Chrome** + la extensión Claude in Chrome (no
  funciona en Arc); Node 20+ y npm (chequeo de tipos y servidor local; `npm install` tarda ~5 min); PowerShell
  (`Set-Clipboard`) para la receta de pegado en Windows; Python 3.9+ (scripts); Pillow solo para `qa_visual.py`.
- La receta de pegado y las coordenadas del editor están verificadas **solo en Windows** y en una ventana de
  1568 × 726 de captura; en macOS el equivalente de `Set-Clipboard` es `pbcopy` (sin probar).

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-13 | La skill es sub-skill propia de `direct-visual-design` y de `seo-content-system`; su proceso es obligatorio y completo | guille | Que lo aprendido en el primer sitio no se pierda y las dos skills principales lo invoquen |
| 2026-10-13 | Editar todo **primero en local** y luego pasarlo a mano al editor del constructor (portapapeles + «Guardar») | guille | El constructor no deja subir archivos al proyecto |
| 2026-10-13 | El proyecto del constructor lleva su propio `README.md` como handoff + handshake y el `AGENTS.md` ordena a la IA mantenerlo | guille | Que la IA del constructor no pierda el hilo entre tareas |
| 2026-10-13 | Una carpeta de imágenes por entrega, subida a Medios; «Insertar enlaces» para dar las URL a la IA; contrastar por SHA-256 | guille | El CDN renombra los archivos y no se puede cambiar |
| 2026-10-13 | Nunca pulsar «Publicar» ni cambiar ajustes de la cuenta o del proyecto sin pedido expreso; no reescribir historial publicado | guille | El historial git está conectado al constructor y «Publicar» comparte la esquina del botón «Guardar» |
| 2026-10-14 | El constructor se puede operar de punta a punta con Claude in Chrome (solo Chrome; coordenadas dentro de su iframe de otro origen) | guille | Verificado en la entrega 2 del caso `caso-web-universidad-01` (07 §L) |
| 2026-10-16 | Los ejemplos del caso se conservan solo anonimizados (`ejemplos/caso-web-universidad-01/`); los generadores específicos de cada entrega se sustituyen por `scripts/make_partes.py` genérico | guille | Compartir la skill sin datos del cliente |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-13 · caso-web-universidad-01 · guille

- **Qué se hizo:** Primera Home de una web de campaña en el constructor, de punta a punta: UI kit y Home en HTML aprobados → entrega en 5 partes ≤ 50 000 caracteres → construcción por la IA → auditoría del código descargado (hallazgos C1–C10) → mejoras locales con tipos estrictos y servidor local → pegado manual de 22 archivos por portapapeles → 32 imágenes por Medios emparejadas por SHA-256 → `AGENTS.md` y `README.md` vivos. De ahí salió la skill (v1.0.0).
- **Salió bien:** La Home quedó con las alturas del HTML; el chequeo de tipos en copia aparte; verificar pestaña y primera línea antes de «Guardar»; emparejar 32/32 imágenes por hash.
- **Salió mal / incidencia:** `.container` de Tailwind pisaba el del kit (B1); `AGENTS.md` casi vacío (C1) y metadatos con afirmaciones inventadas (C3); `Ctrl+S` escribió una «s» (E2); el portapapeles se pisó dos veces y se pegó una ruta de archivo dentro de un archivo (E5, E9); `msedge --headless` no capturaba con Edge abierto (F8).
- **Regla candidata:** Escribir `AGENTS.md` + `README.md` vivos antes de pedirle más a la IA del constructor; shell común en `__root.tsx` desde la primera construcción; pegar y guardar en llamadas separadas.
- **Herramientas:** GoHighLevel AI Studio, Claude in Chrome, PowerShell `Set-Clipboard`, Chrome headless, `tsc` estricto, Node/Vite

### 2026-10-13 · caso-web-universidad-01 · guille

- **Qué se hizo:** QA de la Home ya construida: sección nueva de convocatoria y FAQ completa (QA Home 1), ronda de CSS responsive en tablet y móvil, y listado con filtros en la URL + ficha dinámica de ~20 elementos, todo en local. Contenido largo tomado literal de fuentes oficiales con fuente y fecha visibles (v1.1.0).
- **Salió bien:** Cambios de CSS como bloque «AÑADE AL FINAL» con sobrescrituras; datos largos en un JSON fuente único; reglas de datos del cliente aplicadas al generar, no en el componente; medir el desborde con script, no a ojo.
- **Salió mal / incidencia:** Rejillas sin `minmax(0,1fr)` desbordaban 15 px en móvil (I1); `tsc` marcaba rutas nuevas como inexistentes por un `routeTree.gen.ts` desactualizado (J1); un módulo generado de 67 mil caracteres no cabía en una parte (K1); 403 en páginas oficiales por cabeceras (K2); el conector de Drive no expone hipervínculos de la hoja (K3); PDF equivocados en la hoja del cliente (K4); capturas «móviles» recortadas por el ancho mínimo de la ventana headless (K6).
- **Regla candidata:** Sobrescribir al final del CSS en vez de editar reglas anteriores; no pisar archivos que la IA del constructor también edita (los datos nuevos van «AÑADIDOS AL FINAL»); verificar cada PDF del cliente antes de citarlo.
- **Herramientas:** `scripts/make_partes.py` (antes, generadores propios del proyecto), `scripts/overflow.html`, Chrome headless, `curl`

### 2026-10-14 · caso-web-universidad-01 · guille

- **Qué se hizo:** Primera operación real del constructor con Claude in Chrome: se aplicaron las 4 partes de la entrega 2 desde el chat, se subieron 17 fotos a Medios con `file_upload` y se conectaron emparejándolas por SHA-256; 46/46 comprobaciones en la vista previa pública (v1.2.0, sección L de `references/07`).
- **Salió bien:** El patrón de pegado en el chat (clic → «x» → comprobar → `ctrl+a`/`ctrl+v`); sacar las URL del CDN directamente del DOM de Medios; abrir iframes del mismo origen para probar rutas y anchos.
- **Salió mal / incidencia:** La extensión no estaba emparejada al empezar (L1, K8); `ctrl+a` seleccionó la página entera (L3); capturas con «Script injection timed out» (L4); la IA del constructor reestructuró el código al aplicar las partes (dividió un componente grande, movió `IMG_URLS` a otro módulo, dejó carpetas temporales) y hubo que adoptar su versión como nueva base local (L5); «Descargar base de código» dejó un `.tmp` sin extensión (L6).
- **Regla candidata:** Tras aplicar partes, descargar la base de código y re-sincronizar el local con la versión del builder; mandar a la IA el mapa de imágenes ya verificado en vez de pedirle que adivine.
- **Herramientas:** Claude in Chrome (`file_upload`, `javascript_tool`), `scripts/match_cdn.py`

### 2026-10-15 · caso-web-universidad-01 · guille

- **Qué se hizo:** «Cambios 2» y cambios menores: menú reducido a dos entradas, pie simplificado, ubicaciones sin carrusel ni enlaces, listado con módulo de resumen por elemento y fin de las fichas internas por decisión del cliente; paquetes de partes con modos «reemplazar», «bloque», «anexar» y «texto».
- **Salió bien:** El patrón «ELIMINA estos archivos» como texto libre en una parte; regenerar `AGENTS.md` y `README.md` en la misma entrega para que la IA del constructor tenga el estado nuevo.
- **Salió mal / incidencia:** El cliente cambió la estructura aprobada (se eliminaron las fichas) y la reunión dejó ideas «en espera de luz verde»: ejecutarlas sin autorización habría sido retrabajo.
- **Regla candidata:** No ejecutar cambios de estructura propuestos en una reunión hasta que el responsable los autorice por escrito; anotar la nota «estructura en consulta» en la ficha del proyecto.
- **Herramientas:** `scripts/make_partes.py`, GoHighLevel AI Studio

### 2026-10-16 · caso-mantenimiento-08 · guille

- **Qué se hizo:** Migración de la skill al repo gui-skills: se anonimizó el caso (código `caso-web-universidad-01`, ids de cuenta y proyecto fuera, correos y rutas personales fuera), los tres generadores de partes de cada entrega se reemplazaron por `scripts/make_partes.py` genérico con `partes.ejemplo.json`, `cshot.sh` y `qa_visual.py` dejaron de usar rutas del equipo, y el código del cliente pasó a ejemplos sanitizados.
- **Salió bien:** No había desfase entre la fuente y la copia instalada (los 21 archivos de texto eran idénticos); `make_partes.py` se probó con un proyecto de muestra.
- **Salió mal / incidencia:** La fuente tenía una carpeta de respaldos con copias de otras skills y de la configuración global (`_respaldo/`), que no se migró.
- **Regla candidata:** Las carpetas `_respaldo/` no entran al repo; el respaldo es el propio historial de git.
- **Herramientas:** Python 3.12

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Escribir `AGENTS.md` + `README.md` vivos **antes** de pedirle más a la IA del constructor | caso-web-universidad-01 | candidata: un solo caso; ver `memoria/inbox-aprendizajes.md` |
| Una carpeta de imágenes por entrega + manifiesto, y contrastar las URL por SHA-256 | caso-web-universidad-01 | candidata (aprobada como práctica del caso; falta repetirla) |
| Mover el shell común a `__root.tsx` desde la primera construcción | caso-web-universidad-01 | candidata |
| Pegar y guardar en llamadas separadas; verificar pestaña y primera línea | caso-web-universidad-01 | candidata (la incidencia ocurrió dos veces) |
| Pedir `IMG_URLS` + `img()` en vez de rutas de imagen sueltas | caso-web-universidad-01 | candidata |
| No ejecutar cambios de estructura de una reunión sin autorización escrita del responsable | caso-web-universidad-01 | candidata |
