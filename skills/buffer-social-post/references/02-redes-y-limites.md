# Redes: límites de texto, medios y metadatos (fuente: documentación de Buffer, 2026-10-28)

## Límites de texto (el script valida con `--servicio`)
| Red | Texto del post | Primer comentario |
|---|---|---|
| LinkedIn (páginas y perfiles) | 3.000 | 1.250 |
| Instagram | 2.196 | 2.200 |
| Facebook | 5.000 | 5.000 |
| X (gratis) | 280 | — |
| X (Basic/Premium) | 25.000 | — |
| YouTube (descripción) | 5.000 (título: 100) | — |

**Cómo cuenta Buffer:** unidades UTF-16 (un emoji o una letra «negrita» Unicode cuenta 2); **LinkedIn: cada URL cuenta 24** sin importar su largo; **Instagram: cada salto de línea cuenta 2**; X usa su conteo ponderado (URL = 23). Superar el límite devuelve HTTP 200 con el mensaje en `message`. Los medios no consumen caracteres. Instagram: no hay cifra documentada de imágenes por carrusel ni de requisitos de PDF en LinkedIn (documento sin verificar).

## Medios
- Sin subida de archivos: URL **pública, https, directa y estable** (no Drive/Dropbox, no firmadas, no redirecciones). Alojar en el propio sitio web del usuario o en un servicio de archivos con URL directa (Cloudinary, R2 con acceso público…). Probar la URL en una ventana privada; algunos hosts con protección contra robots bloquean la descarga automática.
- Documento (PDF) = **dos archivos alojados**: el PDF y su miniatura (`thumbnailUrl`), más `title`. LinkedIn lo muestra como carrusel de láminas.
- Video: `video.url`; en Instagram, TikTok y Pinterest se puede fijar el cuadro de portada con `metadata.thumbnailOffset` (milisegundos).
- No se documentan límites de peso ni formatos: no asumirlos; confirmar con una prueba.

## Tipos de entrada confirmados por introspección (2026-10-28)
- `ImageAssetInput`: `url` (String!, obligatorio), `thumbnailUrl`, `metadata`. `VideoAssetInput`: `url!`, `thumbnailUrl`, `metadata`. `DocumentAssetInput`: `url!`, `thumbnailUrl!`, `title!` (los tres obligatorios).
- `LinkAttachmentInput`: `url!`, `title`, `description`, `thumbnail`.
- `metadata.linkedin` (`LinkedInPostMetadataInput`): `annotations`, `firstComment`, `linkAttachment`.
- `metadata.instagram` (`InstagramPostMetadataInput`): **`type` (PostType!) y `shouldShareToFeed` (Boolean!) obligatorios**, además de `firstComment`, `geolocation`, `isAiGenerated`, `link`, `stickerFields`.
- `metadata.youtube` (`YoutubePostMetadataInput`): `title`, `categoryId`, `privacy`, `license`, `embeddable`, `madeForKids`, `notifySubscribers`, `isAiGenerated`.
- **Formato de imagen:** LinkedIn → JPG o PNG (no WebP). Verificado: JPG de 1280×720 y 114 KB aceptado.

## Metadatos por red (`metadata`, solo la red del canal)
- Hilos (X, Bluesky, Threads, Mastodon); **primer comentario** (LinkedIn, Facebook, Instagram); tipo de post `post`/`story`/`reel` (Instagram); tablero (Pinterest); etiquetas de usuario por imagen (`image.metadata.userTags`, Instagram); tarjeta de enlace `linkAttachment` (Bluesky, Facebook, LinkedIn, Substack, Threads; no se combina con `assets`).
- Opciones de YouTube (privacidad, título, categoría…) existen en `YoutubePostMetadata`; sus campos de entrada **no se han probado**.
- Los tipos de entrada exactos (`PostInputMetaData` → `linkedin`, `instagram`, `youtube`…) existen en el esquema; la skill aún no los usa. Antes de implementarlos: introspección del tipo (`__type(name:"...")`), no suposición.

## Qué plataformas soporta Buffer por API
Instagram, Threads, LinkedIn, X, Facebook, Google Business Profile, Mastodon, YouTube, Pinterest, Bluesky (más TikTok y Substack en el esquema).

## Métricas
`Post.metrics` solo está disponible para flujos personales con clave personal.
