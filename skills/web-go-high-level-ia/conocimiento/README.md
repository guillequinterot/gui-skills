# Conocimiento (GHL AI Studio)

Material de apoyo que no es proceso ni incidencia. Añadir aquí notas sobre la plataforma (límites, cambios de interfaz, funciones nuevas del constructor) con fecha y fuente. Hoy:

- 2026-10-13 · Límites observados: chat ≤ 50 000 caracteres y ≤ 5 imágenes; sin subida de archivos al proyecto; «Descargar base de código» disponible; «Insertar enlaces» en Medios; CDN `assets.cdn.filesafe.space/<location>/media/`.
- Estructura del proyecto: plantilla `tanstack_start_ts` (`.vibe/project.json`) y `@leadconnector/vite-tanstack-config` (ya incluye tanstackStart, react, tailwind, tsconfig paths y nitro): no duplicar plugins.
- Integración `form_tracking`: POST al endpoint de seguimiento externo de LeadConnector con los IDs de campos personalizados de la cuenta. Esos IDs son de cada cuenta: nunca se copian entre proyectos ni se guardan en notas o en la skill.
