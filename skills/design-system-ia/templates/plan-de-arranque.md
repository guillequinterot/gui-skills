<!--
PLANTILLA · plan-de-arranque
Para qué: dejar por escrito las decisiones del modo `definir` (¿hace falta un sistema?, perfiles, qué hay, MVP, fases) y la revisión de la regla de salto.
Modo: definir (y auditar, para la sección 11) · Perfil: todos · Referencia: references/09-arranque-y-operacion.md
Cómo se usa: copia este archivo a la carpeta del proyecto, rellena los <marcadores>, borra los comentarios y las secciones que tu perfil marca como «no aplica».
Reglas: decide el usuario, no la skill · lo que no se sepa se escribe «no se sabe» · no pongas contraseñas ni claves aquí.
En `individual` + `website` bastan las secciones 1, 2, 4, 5, 8, 9 y 11.
-->

# Plan de arranque · <proyecto o código de caso>

**Fecha:** <AAAA-MM-DD> · **Decide:** <persona> · **Última revisión:** <AAAA-MM-DD>

## 1. ¿Hace falta un sistema?

| Pregunta | Respuesta | Consecuencia |
|---|---|---|
| ¿Cuántas pantallas, páginas o productos comparten piezas? | <…> | <ninguna / hay caso> |
| ¿Se repite trabajo o se duplican componentes? | <…> | |
| ¿Cuántas personas cambian el diseño o el código? | <…> | <individual / equipo> |
| ¿Quién lo mantendrá dentro de 6 meses? | <…> | <si nadie: avisar> |
| ¿Hay ya una librería abierta o un tema que cumpla? | <…> | <adoptar y documentar qué se cambia> |
| ¿Tiene implementación, documentación y gobierno (tres pilares)? | <…> | <si no: es un UI kit, no un sistema> |

**Resultado:** ☐ No hace falta sistema ☐ Hace falta uno mínimo (`website`) ☐ Hace falta uno completo (`app` / `sistema compartido`)
**Razón:** <una o dos frases> · **Decidido por:** <persona> el <fecha>

## 2. Perfiles y fuente de verdad

- **Perfil de proyecto:** ☐ `website` ☐ `app` ☐ `sistema compartido`
- **Perfil de gobierno:** ☐ `individual` (por defecto) ☐ `equipo`
- **Fuente de verdad:** ☐ contrato/código primero (por defecto) ☐ Figma primero · **Motivo si no es la de por defecto:** <…>
- **Stack:** <WordPress / HTML+CSS / Astro / React / Next.js / otro>

## 3. Prerrequisitos *(no aplica en `individual` + `website` si ya se conocen)*

| Qué | Disponible y permitido | Notas |
|---|---|---|
| Repositorio / carpeta de código | <sí / no / no se sabe> | |
| Archivo de Figma | | |
| Herramienta de IA y servidores MCP | | <¿permisos bloqueados?> |
| Hosting, Drive o Figma para publicar la documentación | | <se pregunta siempre el destino> |
| Entorno de código (Git, terminal) | | <si falta, la skill lo explica en una línea> |

## 4. Inventario de recursos

| Recurso | Dónde vive | Quién lo mantiene | ¿Está al día? |
|---|---|---|---|
| <hoja de estilos / tema / Figma / páginas / documentación> | <ruta o enlace> | <persona> | <sí / no / no se sabe> |

## 5. Preguntas

**Al usuario (siempre):**
1. ¿Qué es lo que más repites o te duele? → <…>
2. ¿Qué tienes ya? → <ver inventario>
3. ¿Qué no se puede cambiar (marca, tema, plugin, nombres de colores)? → <…>
4. ¿Quién más tocará esto? → <…>
5. ¿Dónde se mostrará la documentación? → <…>

**A desarrollo** *(`app`, `sistema compartido`)*: ¿qué framework y qué nomenclatura impone? ¿en qué formato prefiere recibir los nombres? → <…>
**A equipos y líderes** *(`equipo`)*: ¿qué esperan del sistema? ¿quién bloquea las revisiones? ¿qué están construyendo sin terminar? → <…>

## 6. Cuatro bloques de contexto

1. **Requisitos visuales:** <…>
2. **Estructura:** <…>
3. **Límites de desarrollo:** <…>
4. **Límites de diseño:** <…>

## 7. Conflictos de nombres detectados

| Palabra o par | Dónde choca | Propuesta (2–3 opciones) | Decisión |
|---|---|---|---|
| <p. ej. un mismo nombre para tamaño y peso> | | | |

## 8. Librería de partida

- **¿Usa ya una librería o un tema?** <cuál / ninguna>
- **¿Qué quiere poder cambiar?** <…>
- **Origen que se anotará en cada contrato:** <sistema propio / librería abierta (cuál) / tercero>
- **Regla para la IA:** <«usa el nuestro, no el de la librería base» u otra>

## 9. MVP y fases

- **Entra:** <…>
- **No entra todavía:** <…>
- **Puerta de entrada:** ☐ sistema nuevo con código → contrato primero ☐ sistema existente sin contrato → MVP de documentación y luego contrato mínimo

| Fase | Qué se hace | Estado |
|---|---|---|
| 0 | Descubrimiento (secciones 3–7) | <hecho / pendiente> |
| 1 | MVP y priorización | |
| 2 | Propiedades y valores en tabla | |
| 3 | Nomenclatura y taller de vocabulario | |
| 4 | Primera versión | |
| 5 | Accesibilidad | |
| 6 | Verificación | |
| 7 | Segunda versión | |

## 10. Medida de éxito

- **Qué tiene que dejar de doler:** <…>
- **Cómo se medirá:** <…> · **Fecha de revisión:** <AAAA-MM-DD>

## 11. Regla de salto: señales vistas

Se revisa al arrancar y en cada auditoría. **La skill avisa; el cambio de perfil lo decide el usuario.**

| Salto | Señal | ¿Se cumple? | Anotación |
|---|---|---|---|
| `website` → `app` | Área de clientes o inicio de sesión | ☐ | |
| | Paneles o tablas con filtros | ☐ | |
| | Formularios con validación y estados de error | ☐ | |
| | Más de unos 5 componentes interactivos con estados | ☐ | |
| | Modo oscuro o responsive complejo con datos dinámicos | ☐ | |
| `app` → `sistema compartido` | Un segundo producto o marca reutiliza componentes | ☐ | |
| | Más de una persona o equipo cambia el sistema | ☐ | |
| | Piden versiones y avisos de cambio | ☐ | |
| | Se duplican componentes entre proyectos | ☐ | |
| | Temas por cliente | ☐ | |

- **0–1 señal:** se anota, sin avisar. **2 o más:** se avisa con las señales, qué cambiaría y qué costaría.
- **Respuesta del usuario:** ☐ cambiar de perfil ☐ quedarse ☐ decidir más adelante · **Fecha:** <…>
  *Si dice que no, no se insiste hasta que cambie una señal.*

## 12. Qué no se verificó

<Lista de lo que no se pudo comprobar y por qué. Si no hay nada, escribe «nada pendiente» solo si es cierto.>
