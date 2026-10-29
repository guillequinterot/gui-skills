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
- **YouTube por Buffer = solo Shorts (verificado en vivo 2026-10-28):** un MP4 horizontal de 3:10 se rechazó con «Video must be no longer than 3 minutes for YouTube Shorts» y «Video must be vertical (portrait orientation) for YouTube Shorts»; la ayuda de Buffer confirma: solo Shorts (1 video, ≤ 3 min, 9:16 o 1:1) y no admite video largo. Un video horizontal se sube a mano en YouTube Studio (o con la API de YouTube y un token con `youtube.upload`, que esta cuenta no tiene).
- **Miniatura propia: no.** `VideoAssetInput.thumbnailUrl` existe en el esquema, pero la API responde «Video thumbnailUrl is not supported: social networks do not accept custom video thumbnail images»; `thumbnailOffset` solo vale en Instagram, TikTok y Pinterest. La miniatura de YouTube se pone a mano.
- Campos de YouTube implementados en el script (`--yt-titulo`, `--yt-privacidad` private por defecto, `--yt-categoria` 27, `--yt-ia`): el payload se valida con `--simular`; la publicación real de un Short **no se ha probado**.
- Los tipos de entrada exactos (`PostInputMetaData` → `linkedin`, `instagram`, `youtube`…) existen en el esquema; la skill aún no los usa. Antes de implementarlos: introspección del tipo (`__type(name:"...")`), no suposición.

## Qué plataformas soporta Buffer por API
Instagram, Threads, LinkedIn, X, Facebook, Google Business Profile, Mastodon, YouTube, Pinterest, Bluesky (más TikTok y Substack en el esquema).

## Métricas
`Post.metrics` solo está disponible para flujos personales con clave personal.
