<!--
PLANTILLA · nota-para-agentes (se guarda como AGENTS.md en la raíz del proyecto, o como CLAUDE.md u otro nombre según la herramienta)
Para qué: decirle a un agente que USA el sistema cómo debe trabajar, para que lea el contrato real y no invente. Es la capa de INSTRUCCIÓN; el índice (indice-llms.txt) es la de DESCUBRIMIENTO.
Modo: documentar · Perfil: todos · Referencia: references/06-listo-para-ia.md (secciones 2–5, 7 y 12)
Cuánto llevar según el perfil:
  · website → la regla clave de arriba y los apartados 1, 3, 4, 5, 7, 8 y 9 (nota raíz corta + vocabulario + errores frecuentes).
  · app → todos; en el 9 borra la consulta por CLI o MCP si no existe.
  · sistema compartido → todos.
Reglas: sin campos ni encabezados obligatorios (AGENTS.md es un Markdown libre) · si el repositorio tiene subproyectos, cada uno puede tener la suya y el agente lee la más cercana al archivo que edita · el mensaje explícito del usuario manda sobre esta nota · NO pongas contraseñas, claves ni tokens · lo que sea generable (inventario, tablas) se genera, no se copia a mano · revisa que la nota no contradiga el contrato (una guía copiada se desactualiza).
Dos audiencias: esta nota es para quien USA el sistema. Las reglas de quien lo MANTIENE van en otro archivo (CLAUDE.md o una carpeta de contribución).
Cada regla declara si es BLANDA (una instrucción) o DURA (un permiso más un verificador). Una instrucción en este archivo es blanda. No instales hooks ni servidores sin permiso expreso del usuario.
-->

# <Nombre del sistema> · nota para agentes

> **Antes de escribir código con este sistema, lee el contrato real de cada componente que vayas a usar. Nunca adivines una prop.** *(blanda)*

## 1. Qué es

<Una frase: qué es el sistema, para qué proyecto y dónde vive el código (<ruta>) y el diseño (<enlace a Figma>).>

## 2. Inventario de componentes

<!-- inicio: inventario generado — no editar a mano -->
<Lo escribe un script a partir del índice de contratos: nombre · estado · propósito.>
<!-- fin: inventario generado -->

## 3. Jerarquía

1. **Usa primero el sistema.** Si existe el componente, úsalo; no uses el equivalente de la librería base (<nombre de la librería, si la hay>).
2. **Si no existe,** crea un componente propio marcado con `// [CUSTOM] <motivo>` y parte del andamio del sistema, no de cero.
3. **Si no puedes resolverlo con lo que hay,** no inventes: deja una solicitud (<ruta de solicitudes>) o pide el componente a <persona>.

## 4. Tokens

- Usa **solo tokens semánticos** (<prefijos permitidos>). Nunca colores, medidas ni sombras sueltos.
- Prohibidos: <prefijos de primitivos>.
- Claro y oscuro salen de los mismos tokens; no escribas un valor para cada tema.

## 5. Vocabulario canónico

*(La tabla completa está en <ruta al vocabulario>; estas son las filas que más se rompen.)*

| Usa | No uses |
|---|---|
| `<nombre>` | `<sinónimo prohibido>`, `<sinónimo prohibido>` |

## 6. ¿Puedes? ¿Deberías? ¿Se te permite?

| Pregunta | Qué significa | Qué hacer si falla |
|---|---|---|
| **¿Puedes?** | Es mecánicamente correcto: compila, usa tokens y props válidos | Corrígelo; el verificador te dirá cómo (<comando>) |
| **¿Deberías?** | Respeta el juicio de diseño: el «nunca usar para» del contrato y la accesibilidad | Cambia de componente o consulta el contrato |
| **¿Se te permite?** | Tienes autoridad: lo que el contrato permite adaptar localmente | Si el contrato lo lista en «se escala al sistema», **no lo hagas: pregunta** |

## 7. Registro de errores frecuentes

*(Sale de pruebas reales o de auditorías; cada línea con su fecha. Si no hay, escribe «sin registro todavía».)*

- <AAAA-MM-DD> · <error que se repite> → <qué hacer en su lugar>

## 8. Qué NO hacer

- No inventes props, valores, variantes ni rutas de importación.
- No cambies tokens, contratos, vocabulario ni el estándar de conversión de Figma sin que la persona responsable lo apruebe: presenta **2–3 opciones** con su efecto y espera.
- No uses los nombres de Figma si no coinciden con los del código: manda <fuente de verdad registrada>.
- No edites las partes marcadas como generadas.
- <Otro que el proyecto haya aprendido>

## 9. Cómo consultar y a quién escalar

- **Contratos:** <ruta>. **Vocabulario:** <ruta>. **Página de cada componente:** <ruta o enlace>.
- **Consulta por CLI o MCP:** <comando o «no hay»>. *(Solo de lectura. No registres un servidor MCP ni toques la configuración del usuario sin su permiso expreso.)*
- **Escalar a:** <persona o canal>.

## 10. Contexto de producto

<Qué es la empresa o el proyecto, visión, quién lo usa, principios de diseño y **cosas que evitar**.>

## 11. Flexibilidad

<Elige una y bórrala si no aplica:>
- «Usa siempre el sistema.»
- «90 % sistema, 10 % nuevo solo si nada lo cubre.»
- «No crees layouts nuevos sin preguntarme.»

## 12. Orden de lectura para construir una pantalla

1. Layout → 2. Componentes (sus contratos) → 3. Tokens → 4. Accesibilidad → 5. Idiomas y textos.
