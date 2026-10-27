<!--
PLANTILLA · tabla-antes-despues
Para qué: sincronizar nombres entre Figma y código (o migrar nombres) cuando NO hay un gestor de tokens que haga de puente. Se adjunta a una incidencia o tarea de desarrollo.
Modo: construir, documentar · Perfil: app y sistema compartido (en `website`, úsala al renombrar clases o variables) · Referencia: references/09-arranque-y-operacion.md (sección 7), 02 y 03
Cómo se usa: 1) captura lo de Figma junto a lo del código; 2) rellena la tabla; 3) pregunta a desarrollo en qué formato prefiere recibirla; 4) marca el estado según avance.
Reglas: renombrar es un cambio MAYOR si el sistema ya está publicado: añade periodo de alias, aviso de obsolescencia y guía de migración (propuesta de la skill, sin probar) · si hay gestor de tokens, renombra en el gestor, no dentro de las variables de Figma · el nombre «después» sale del vocabulario aprobado, no de esta tabla · decide la persona responsable.
-->

# Tabla de nombres · antes → después · <proyecto>

**Fecha:** <AAAA-MM-DD> · **Decide:** <persona> · **Formato acordado con desarrollo:** <tabla en la tarea / captura lado a lado / otro> *(preguntado el <AAAA-MM-DD>)*
**Incidencia o tarea:** <enlace> · **Decisión asociada:** <enlace a decision-NNN.md, si la hay>

| Elemento | Nombre en Figma (antes) | Nombre en código (antes) | Nombre acordado (después) | Alias hasta (si está publicado) | Estado |
|---|---|---|---|---|---|
| <token o propiedad o componente> | <…> | <…> | <…> | <AAAA-MM-DD o —> | ☐ pendiente ☐ en curso ☐ hecho |

## Captura lado a lado

<Imagen o enlace: lo de Figma junto a lo del código.>

## Notas para desarrollo

- <Qué cambia, qué no, y en qué orden conviene aplicarlo.>
- **¿Rompe algo ya publicado?** <no / sí: versión nueva y guía de migración>

## Verificación

☐ Revisado a mano · ☐ Comprobado con <script> · **Lo que no se comprobó:** <…>
