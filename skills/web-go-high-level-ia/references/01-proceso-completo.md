# 01 · Proceso completo (de diseño aprobado a sitio publicado en el constructor de GHL)

## Qué es el constructor y qué admite

- «AI Studio» / «Vibe» de GoHighLevel: proyecto **TanStack Start + TanStack Router (rutas por archivos) + React 19 + Tailwind v4 + shadcn/Radix + Supabase (plantilla)**. Vista previa pública `https://preview-<id>.vibepreview.app/`. Proyecto conectado a una rama git (bloque `VIBE` del `AGENTS.md`): los commits se sincronizan con el editor.
- El **chat** acepta solo **imágenes (máx. 5 por mensaje)** y **texto (≤ 50 000 caracteres por mensaje)**. No se suben archivos al proyecto.
- El **editor de código** (botón `</>`) permite abrir cada archivo, editarlo y «Guardar». No se pueden re-subir archivos; sí pegar contenido.
- **Medios**: biblioteca de GHL donde sí se suben carpetas/imágenes (ver [05](05-imagenes-medios-cdn.md)).
- La API de GHL **no crea páginas**: por eso el camino es HTML + kit + partes para el constructor.

## Fases

### 1. Diseño y contenido (con `direct-visual-design` + `seo-content-system`)
UI kit y páginas en HTML (1920 de lienzo, 240 de márgenes, 80 px por sección, múltiplos de 4, tokens en `:root`), textos del cliente literales, SEO por página. Aprobación del usuario.

### 2. Entrega al constructor («partes»)
Ver [02](02-partes-para-el-constructor.md). Resultado: carpeta `entrega-N-*/` con `A-IMAGENES` (a Medios), `B-REFERENCIA` (≤ 5 capturas), `C-COPIAR-Y-PEGAR` (PARTE-1..5), `D-AJUSTES` (prompts cortos), `E-solo-para-mirar`, `LEEME-PRIMERO.txt`, `MANIFIESTO-IMAGENES.md`.

### 3. Construcción por la IA
Pegar PARTE 1…4 (la IA responde «recibida», no construye), PARTE 5 (construye). Comparar la vista previa con las capturas de referencia. Ajustes uno por mensaje.

### 4. Auditoría del código que generó la IA
1. «Descargar base de código» (botón al pie del árbol de archivos) → carpeta del proyecto (`<proyecto>`).
2. Leer **todos los archivos propios** (no `components/ui/*`, `integrations/*`): `AGENTS.md`, `README.md`, `routes/*`, componentes de marca, `lib/*-data.ts`, CSS de marca, `styles.css`, `router.tsx`, `start.ts`.
3. Checklist de hallazgos típicos (todos ocurrieron en `caso-web-universidad-01`):
   - `AGENTS.md` casi vacío (solo el bloque VIBE) → la IA no sabe nada del proyecto.
   - Rutas de imagen **relativas** (`imagenes/x.jpg`) → se rompen en rutas anidadas.
   - Datos duplicados dentro de componentes; formularios duplicados en Tailwind con campos/IDs inventados.
   - Metadatos raíz con **afirmaciones inventadas** («la mejor institución de la región…», «más de N programas»).
   - 404/error en inglés con Tailwind; páginas provisionales sin header/footer.
   - Shell repetido en cada página; enlaces internos como `<a href>`.
   - `data-track` en el HTML pero **sin listener** (medición inerte).
   - Bugs de lógica (p. ej. `if (!track) return track.clientWidth` en el carrusel).
   - `aria-expanded="false"` fijo en el botón del menú.
4. Comparar el CSS del constructor con el CSS aprobado (el constructor suele reproducirlo fiel; verificar `.container`, ver [07](07-incidencias-y-soluciones.md)).

### 5. Edición local
- **Respaldo primero:** `cp -r src AGENTS.md ../_backup-original/`.
- Editar los archivos. Mantener el estilo del código (Prettier del proyecto: `printWidth 100`, comillas dobles, `trailingComma all`).
- **Chequeo de tipos** en una copia aparte (no ensuciar el proyecto): copiar sin `node_modules`, `npm install --ignore-scripts --legacy-peer-deps` (~5 min en Windows, salen avisos `TAR_ENTRY_ERROR` que no impiden que funcione), `node node_modules/typescript/lib/tsc.js --noEmit -p .`. El proyecto usa flags estrictos: `noPropertyAccessFromIndexSignature`, `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`. **Ignorar** errores de rutas (`"/" | "." | ".."`) si `routeTree.gen.ts` está desactualizado en local (el constructor lo regenera).
- **Servidor local:** `node node_modules/vite/bin/vite.js dev --port 5199 --host 127.0.0.1` en segundo plano (si el puerto está ocupado Vite usa el siguiente). Copiar las fotos a `public/imagenes/` de la copia para ver la página completa.
- **Capturas:** Chrome headless con perfil propio (`scripts/cshot.sh`; Edge falla si el usuario lo tiene abierto, ver 07 F8) a 1440 de ancho; para 390 usar `scripts/overflow.html` (iframe del ancho exacto, ver 07 K6). El panel del navegador integrado no captura si Claude está oculto.
- **Prettier** de la copia sobre los archivos tocados antes de pegarlos.

### 6. Transferencia al constructor
Ver [04](04-transferencia-editor-portapapeles.md). Orden recomendado para no dejar la vista previa rota entre guardados: **datos/utilidades primero** (`*-data.ts`), luego componentes que las usan, luego `__root.tsx`, luego `index.tsx` y rutas, y por último `AGENTS.md`/`README.md`.

### 7. Imágenes
Ver [05](05-imagenes-medios-cdn.md).

### 8. Verificación en la vista previa real
Abrir `https://preview-<id>.vibepreview.app/` en una pestaña propia y ejecutar un script que cuente: `h1`, `header.site-header`, `footer`, `main > section`, imágenes rotas, y haga `fetch` de cada ruta (200, `<title>`, `noindex`). Ver también consola (`read_console_messages`). Cerrar las pestañas que se abran.

### 9. Registro
README del proyecto (estado, pendientes, registro de cambios), HANDOFF/HANDSHAKE de la skill y de la carpeta del proyecto, entrada en el registro de trabajos del `HANDOFF.md` de la skill, `memoria/inbox-aprendizajes.md` y, si usas Obsidian, la nota del proyecto y el registro de skills.
