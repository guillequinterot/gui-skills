# Video handoff — {{BRAND}}
Creado: {{DATE}} · Carpeta: `{{PROJECT}}` · Motor: {{ENGINE}}

> Léelo al empezar, actualízalo al terminar cada tramo. Skill: `video-editing-ai-agent`.

## Objetivo
(1–2 frases: qué piezas, formato, plataforma, fecha límite)

## Fuente de copy (handshake de contenido)
{{COPY_SOURCE}} — fila/versión usada: (…)
Copy en pantalla, teléfonos/CTA y reglas de marca: (…)

## Entorno (de handshake.json)
Motor recomendado: (…) · Filtros ffmpeg clave: (…) · Advertencias: (…)

## Archivos
| Rol | Ruta |
|---|---|
| Metraje fuente | |
| Proyecto editable (.mlt) | |
| Assets (logo, audio, imágenes) | |
| Exportaciones | |
| Entrega final (Drive, etc.) | |

## Decisiones (con motivo)
- (fecha) decisión — motivo

## Estado por pieza
| Pieza | Estado (pendiente / en edición / exportado / entregado) | Último archivo | Notas |
|---|---|---|---|

## Verificado vs no verificado
- Verificado (medición/preview): 
- No verificado (oído/movimiento/sincronía): 

## Aprobación del usuario
- Cita textual con la que aprobó: «…»  (vacío = aún no aprobada)
- Aprobado explícitamente: (…)
- **Sin decidir** (no es preferencia): (…)

## Lo bueno / lo malo (para la biblioteca)
- Bueno (repetir): (…)
- Malo (evitar, con costo): (…)
- Si fue aprobada: `python {{SKILL_DIR}}\scripts\save_approved.py add …`  ·  lecciones generales → `references/errores-conocidos-y-aciertos.md`

## Pendientes
- [ ] 

## Próxima acción
(una sola, concreta)

## Cómo retomar
1. `python {{SKILL_DIR}}\scripts\handshake.py --project {{PROJECT}}` y leer `references/errores-conocidos-y-aciertos.md`
2. Abrir proyecto: `inspect_project` → revisión actual.
3. (comandos específicos del trabajo)

## Historial de sesiones
### Sesión 1 — {{DATE}}
**Estrategia:** (un párrafo)
**Decisiones:** (tomas, cortes, color, animaciones y por qué)
**Registro de razonamiento:** (una línea por decisión no obvia)
**Pendiente:** (lo aplazado)
- Creado por export_agent.py.
