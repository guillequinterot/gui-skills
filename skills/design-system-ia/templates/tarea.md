<!--
PLANTILLA · tarea (opcional)
Para qué: una plantilla de tarea por tipo de trabajo del sistema (crear un componente, cambiar un token, retirar algo, auditar), para que el proceso quede escrito y no dependa de la memoria de nadie.
Modo: documentar, definir · Perfil: equipo (en `individual` se usa como lista de pasos propia) · Referencia: references/09-arranque-y-operacion.md (sección 11)
Cómo se usa: copia el bloque del tipo que toque. Actualízalas cuando el proceso cambie; una plantilla desactualizada se vuelve un obstáculo.
Reglas: no prometas fechas que no puedas cumplir · en `equipo`, los cambios no se hacen «al momento»: pasan por propuesta y revisión · la IA propone, decide la persona responsable.
-->

## Tarea: crear un componente — <nombre>

- **Tipo:** crear componente · **Quién decide:** <persona> · **Fecha límite acordada:** <AAAA-MM-DD o «sin fecha»>
- **Pasos:**
  1. Reunión con desarrollo: qué piden los equipos y qué límites impone el framework.
  2. Contrato (mínimo o completo) y vocabulario de sus props.
  3. Primera propuesta (código y, si aplica, Figma con previsualización aprobada).
  4. Revisión conjunta de diseño y desarrollo.
  5. Lista de control y página de componente.
  6. Publicación y aviso de cambios.
- **Verificación:** <qué se comprueba y con qué>
- **Aviso a:** <canal o personas>

## Tarea: cambiar un token o el vocabulario — <nombre>

- **Tipo:** cambiar token/vocabulario · **Quién decide:** <persona responsable>
- **Pasos:** 1) escribir la decisión con 2–3 opciones y contraste AA claro/oscuro; 2) aprobación; 3) aplicar y actualizar contratos, documentación y Figma; 4) tabla antes → después; 5) versión y aviso (si rompe lo publicado: alias y guía de migración).
- **Verificación:** <…> · **Aviso a:** <…>

## Tarea: retirar un componente — <nombre>

- **Tipo:** retirar · **Quién decide:** <persona responsable>
- **Pasos:** 1) comprobar usos; 2) marcarlo `deprecated` (versión menor con aviso); 3) guía de migración; 4) retirarlo en la versión mayor siguiente.
- **Verificación:** <…> · **Aviso a:** <…>

## Tarea: auditoría periódica — <fecha>

- **Tipo:** auditar · **Frecuencia sugerida:** trimestral (propuesta, sin probar)
- **Pasos:** rellenar la ficha de auditoría; revisar componentes sin uso y deuda `[CUSTOM]`; registrar mejoras.
- **Verificación:** <…> · **Aviso a:** <…>
