# 05 · Imágenes: Medios de GHL, CDN que renombra y mapa verificado

## Hechos (2026-10-13)
- El proyecto **no admite subir archivos**. Las imágenes van a **Medios** (biblioteca de GHL; botón «Subir» acepta **carpetas**).
- Al subir, el **CDN cambia el nombre del archivo automáticamente** (`<id-de-24-caracteres>.jpg`) y **no se puede modificar**: la URL (`https://assets.cdn.filesafe.space/<location>/media/<id>.<ext>`) nunca contiene el nombre original.
- En el selector de Medios hay un botón **«Insertar enlaces»** que pega **todas las URL** de las imágenes seleccionadas en el chat de la IA (sin nombres).
- El archivo subido es **idéntico byte a byte** al original (no recomprime): se puede emparejar por **SHA-256**.
- La IA, si no ve los archivos, pedirá «sube tú los archivos a `public/imagenes/`»: **no puede** (no ve Medios). Hay que darle las URL.

## Flujo por entrega
1. Cada entrega tiene su carpeta `A-IMAGENES-subir-a-Medios/` con **solo las imágenes nuevas** de esa entrega. Así se sabe qué subir y qué seleccionar.
2. Generar `MANIFIESTO-IMAGENES.md` (archivo → qué se ve): `python -I scripts/manifest_imagenes.py <carpeta-entrega> <N> <Nombre> <ruta-src>` (usa el `alt` del código).
3. Subir la carpeta a Medios → seleccionar esas imágenes → **«Insertar enlaces»** → la IA del constructor conecta en `IMG_URLS` (en `src/lib/*-data.ts`): `img(file)` devuelve `IMG_URLS[file]` y, si no existe, `<P>_CONFIG.imgBase + file`. **Añadir** al objeto sin borrar lo anterior.
4. **Contrastar** lo que escribió la IA: `scripts/match_cdn.py` (`urls.txt` → descarga → SHA-256 contra la carpeta `A-IMAGENES` → `cdn_match.json`). Debe dar N de N exactos. Generar `MAPA-URL-IMAGENES.md` y `IMG_URLS-listo-para-*.ts.txt`.
5. Si la IA se equivoca o falla «Insertar enlaces»: **plan B** = la IA descarga las URL a `/tmp`, las mira y las empareja por contenido con el manifiesto (SVG por su `fill`, PNG por ser único, fotos por el alt); o se pega el `IMG_URLS` verificado.
6. Verificar en la vista previa: imágenes rotas = 0.

## Reglas de código
- **Siempre `img("nombre-original.jpg")`**; nunca rutas sueltas (`imagenes/…` relativo se rompe en rutas anidadas; `/imagenes/…` solo sirve si están en `public/`).
- `<P>_CONFIG.imgBase` (hoy `/imagenes/`) es el respaldo; si todo pasa a Medios, `IMG_URLS` manda.
- Cada `<img>`: `width`/`height`, `alt` descriptivo en español, `loading="lazy"` salvo la foto principal (`fetchPriority="high"`).
- Formato web: JPG ≤ 250 KB; logos SVG.

## SEO de imágenes con CDN que renombra
El nombre del archivo servido ya no aporta señal; compensar con: `alt` descriptivo, `width/height`, texto cercano relevante, `title`/pie cuando aplique, `og:image` absoluta, y **no** depender del nombre. Sitemap de imágenes: solo si hay dominio propio definitivo.
