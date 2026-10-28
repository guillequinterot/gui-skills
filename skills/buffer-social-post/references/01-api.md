# API de Buffer — lo esencial (fuente: https://developers.buffer.com, leída el 2026-10-28)

## Conexión
- **Endpoint único:** `POST https://api.buffer.com` con `Content-Type: application/json` y cuerpo `{"query": "...", "variables": {...}}` (GraphQL).
- **Autenticación:** cabecera `Authorization: Bearer <clave>`. Sin clave válida: error `UNAUTHORIZED`. La clave se crea en Buffer > Settings > API; actúa en nombre de la cuenta, con acceso a **todas** las organizaciones y canales (no hay alcance por organización). No hay botón para borrar una clave: se rota creando otra. Las apps OAuth usan alcances (`posts:read/write`, `ideas:read/write`, `account:read/write`, `snippets:read/write`, `offline_access`).
- Documentación útil: guías `authentication`, `your-first-post`, `posts-and-scheduling`, `hosting-media`, `character-limits`, `error-handling`, `api-limits`; ejemplos `create-text-post`, `create-image-post`, `create-draft-post`, `create-scheduled-post`, `get-channels`; `reference.html`; estado en `status.buffer.com`.

## Orden de consultas
1. `query { account { organizations { id name } } }` → `OrganizationId`.
2. `query($o: OrganizationId!){ channels(input:{organizationId:$o}){ id name service isDisconnected isLocked isQueuePaused timezone } }` → `ChannelId`. Un canal **bloqueado** (`isLocked`) no permite publicar; uno **desconectado** falla al publicar.
3. `createPost` (abajo). Tipos de variable verificados: `OrganizationId!`, `ChannelId!`, `PostId!`.

## `createPost(input: CreatePostInput!)`
Campos de `CreatePostInput` (verificados por introspección): `text` (String), `channelId` (ChannelId!, obligatorio), `schedulingType` (obligatorio), `mode` (obligatorio), `needsApproval` (Boolean!, obligatorio en el esquema; el script envía `false`), `saveToDraft` (Boolean), `dueAt` (DateTime, ISO 8601 UTC), `assets` (lista), `metadata` (por red), `tagIds`, `ideaId`, `draftId`, `aiAssisted`, `source`.

| Enumeración | Valores |
|---|---|
| `SchedulingType` | `automatic` (la publica Buffer) · `notification` (recordatorio para publicar a mano) |
| `ShareMode` | `addToQueue` (siguiente hueco del horario) · `customScheduled` (hora exacta con `dueAt`) · `shareNext` · `shareNow` |

Respuesta (unión): `... on PostActionSuccess { post { id status text dueAt channelService assets { id mimeType } } }` y `... on MutationError { message }`. **Incluye siempre las dos.** Estados de un post: `draft`, `scheduled`, `sent`, `error`.

`assets` (lista ordenada; cada entrada, un solo tipo): `{image:{url}}`, `{video:{url, metadata:{thumbnailOffset}}}`, `{document:{url, thumbnailUrl, title}}`. Un enlace con tarjeta no es un asset: va en `metadata.<red>.linkAttachment` y no se combina con `assets`.

## Otras operaciones
- **Listar:** `posts(first:N, input:{organizationId, filter:{channelIds:[...]}}){ edges{ node{ id status text dueAt channelService } } }` (paginación por cursor: `first` + `after`).
- **Eliminar:** `mutation($i: PostId!){ deletePost(input:{id:$i}){ __typename ... on MutationError { message } } }` → `DeletePostSuccess` (verificado).
- **Mutaciones existentes (introspección):** `createPost`, `deletePost`, `editPost`, `movePostInQueue`, `createIdea`, `createTag`, `deleteTag`, `updateTag`, `createSnippet`/`updateSnippet`/`deleteSnippet`, `createPostTemplate`…, `createContentItem`… (experimental). Las ideas (`createIdea`) guardan borradores de ideas sin canal.
- Cabeceras de límite en cada respuesta: `RateLimit: "<ventana>"; r=<restantes>; t=<segundos hasta el reinicio>`.

## Errores
- **HTTP 200 siempre**, incluso con error: hay que leer el cuerpo.
- **Errores tipados** (usuario puede corregir: validación, límite de texto, medios inaccesibles): `data.createPost.message` (`MutationError`, `InvalidInputError`, `LimitReachedError`).
- **Errores no recuperables:** `data: null` y `errors[].extensions.code`: `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `UNEXPECTED` (reintentar tras una pausa), `RATE_LIMIT_EXCEEDED` (HTTP 429 con `Retry-After`).
- Ejemplos de mensajes: «LinkedIn posts cannot exceed 3000 characters», «Failed to fetch image dimensions: Not Found» (una miniatura que no se puede descargar hace fallar toda la mutación).

## Límites de la API (por cuenta; todas las claves comparten cuota)
| Plan | Claves | 15 min | 24 h | 30 días |
|---|---|---|---|---|
| Free | 1 | 150 | 600 | 1.000 por canal (máx. 3.000) |
| Essentials | 3 | 450 | 1.800 | 3.000 por canal (máx. 30.000) |
| Team | 5 | 1.500 | 6.000 | 10.000 por canal (máx. 100.000) |

Complejidad de consulta: máx. 175.000 puntos, 25 niveles, 30 alias. Los límites de publicaciones diarias son aparte (consulta `dailyPostingLimits`). **Backoff:** vigilar `r`; ante 429, esperar `Retry-After` + algo de azar, tope de intentos; un agente debe parar y avisar en vez de reintentar sin fin.
