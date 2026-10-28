# HANDSHAKE — buffer-social-post

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 0.1.0 (borrador local, **sin publicar en GitHub**) |
| Última actualización | 2026-10-28 por guille |
| Skill principal / padre | ninguna (herramienta de publicación) |
| Llama a | ninguna (cliente propio sin dependencias) |
| La llaman | `seo-content-system` y `video-editing-ai-agent` (cuando preparan el post de redes de un artículo o un video); y cualquier flujo de blog |

## Herramientas y su estado verificado

| Herramienta | Estado | Verificado el | Notas |
|---|---|---|---|
| `scripts/buffer_api.py canales` | verificado | 2026-10-28 | Cuenta real: organización y 3 canales (YouTube, LinkedIn, Instagram), todos conectados |
| `buffer_api.py borrador` (texto, LinkedIn) | verificado | 2026-10-28 | Estado devuelto `draft`; no se publica |
| `buffer_api.py listar` | verificado | 2026-10-28 | Devuelve estado y texto |
| `buffer_api.py eliminar` | verificado | 2026-10-28 | `DeletePostSuccess` |
| `scripts/test_buffer_api.py` | verificado | 2026-10-28 | 16 comprobaciones sin red: conteo UTF-16, URL=24 en LinkedIn, `--confirmo`, tope de largo, medios públicos |
| `ahora` (shareNow) con una imagen en LinkedIn | **verificado** | 2026-10-28 | Publicado a pedido del dueño: estado `sending` → `sent` en ~10 s; Buffer devolvió el activo con URN de LinkedIn (`image/jpeg`). Imagen JPG de 1280×720 (114 KB) alojada en el hosting del dueño en `assets/social/<slug>/` |
| `ahora` con **carrusel de 4 imágenes en Instagram** (`--servicio instagram`, 4 × `--imagen`) | **verificado** | 2026-10-28 | Publicado a pedido del dueño: `metadata.instagram = {type: post, shouldShareToFeed: true}` y 4 JPG de 1080×1350 (150–220 KB) por URL pública; `sending` → `sent` en ≤ 20 s. El enum `PostType` también trae `carousel`, pero `post` con varias imágenes bastó |
| `--primer-comentario` (LinkedIn/Instagram) y `--ig-tipo` | implementados, **sin publicar** | 2026-10-28 | Verificados solo en simulación (pruebas sin red); falta una publicación real con primer comentario |
| `buffer_api.py limpiar` (borrar medios del hosting tras `sent`) | **verificado** | 2026-10-28 | Prueba en vivo con una carpeta de prueba: con un post en borrador **se niega** (`NO_ENVIADO`, la carpeta sigue); con un post `sent` **borra** y la URL da 404. Solo borra `assets/social/<slug>/`; el slug se valida. Antes se había limpiado a mano `assets/social/` (5 archivos, ≈ 900 KB). Regla del dueño |
| Comprobación de URL pública (HEAD) | verificado | 2026-10-28 | 200, `image/jpeg`, sin redirección, también con un User-Agent de robot |
| `programar`, `cola` | **sin probar** | — | Documentados; solo con orden explícita del dueño |
| Video, documento (PDF) | **sin probar** | — | Tipos de entrada confirmados por introspección (`VideoAssetInput`, `DocumentAssetInput`), no publicados |
| Metadatos de YouTube y `annotations`/`linkAttachment` de LinkedIn | **tipos confirmados, sin implementar** | 2026-10-28 | Por introspección: LinkedIn `annotations`, `linkAttachment`; YouTube `title`, `privacy` (`private`/`public`/`unlisted`), `categoryId`… |
| Explorador web (`developers.buffer.com/explorer.html`) | **no usado** | 2026-10-28 | Pide teclear la clave en un formulario de la página; no se hace. El mismo esquema se obtiene por introspección con `buffer_api.py`/consulta directa |
| Cuota | observado | 2026-10-28 | Cuenta con 3.000 solicitudes cada 30 días; las pruebas gastaron ~13 |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas
- Leer la clave de un archivo fuera del repo sin imprimirla; listar canales; crear, listar y eliminar borradores de texto.
- Contar caracteres como Buffer y rechazar textos que pasan el límite antes de gastar cuota.
- Rechazar medios no públicos (Drive/Dropbox/firmados/redirecciones).

## Pendientes
1. Probar, con publicaciones autorizadas por el dueño: documento PDF (carrusel de LinkedIn), video y programar para una hora futura (la imagen ya está probada).
2. Implementar en el script los metadatos por red (`--primer-comentario` de LinkedIn, tipo de Instagram, opciones de YouTube): los tipos ya están confirmados.
3. Decidir si el post de LinkedIn de cada artículo queda en borrador o se programa con orden permanente (decisión del dueño).
4. Publicar la skill en GitHub (`publish_job.py`) cuando el usuario la apruebe.
