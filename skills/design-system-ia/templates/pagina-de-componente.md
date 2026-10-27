<!--
PLANTILLA · pagina-de-componente
Para qué: documentar un componente en cuatro secciones más accesibilidad y contacto, con el mismo propósito que el contrato y los nombres exactos del código.
Modo: documentar · Perfil: todos (en `website` basta una versión breve; en `app` y `sistema compartido` añade hacer/no hacer, lista de control y guía de contribución) · Referencia: references/04-documentacion-y-entrega.md (secciones 4, 9, 10 y 11)
Cómo se usa: UNA página por componente. La primera es la plantilla: pide opinión a diseño y a desarrollo y solo entonces replica las demás.
Reglas: muestra el componente REAL (instancias en Figma; el propio componente en HTML), no capturas · el componente aparece una sola vez (matriz única); las propiedades booleanas se activan, no se despliegan en columnas · propósito único: el del contrato, no un segundo texto · no copies cifras que se desactualicen · enlaza lo que se pueda generar (cambios, tokens, estado).
Si se publica: pregunta el destino (hosting, Drive o Figma). Una página pública de documentación lleva `<meta name="robots" content="noindex">`; no la bloquees en robots.txt. noindex no protege el acceso.
-->

# <Componente>   · estado: <borrador | beta | estable | obsoleto> · [código](<ruta>) · [Figma](<enlace>) · [referencia](<enlace>)

> <Propósito en una frase — el mismo del contrato>

**Versión:** <x.y.z> · **Actualizado:** <AAAA-MM-DD> · [Cambios](<enlace al registro de cambios>) · **Contrato:** [<archivo>](<ruta>)

## Propiedades

*Matriz variante × tamaño × estado. Las etiquetas son los nombres exactos del código.*

| Propiedad | Valores | Por defecto | Notas |
|---|---|---|---|
| `<prop>` | `<a · b · c>` | `<valor>` | <…> |

**Estados que se entregan:** normal · hover · foco · deshabilitado · <otros>.
**Valores por defecto iguales en código y en Figma:** ☐ comparados el <AAAA-MM-DD>.

## Anatomía

*Partes con el mismo nombre en código y en Figma.*

| Parte | Elemento | Opcional | Márgenes · relleno · dimensiones |
|---|---|---|---|
| `<parte>` | <etiqueta HTML o hueco> | <sí / no> | <valores en tokens> |

## Comportamiento

**✔ Hacer**
- <caso concreto en el que sí>

**✘ No hacer**
- <caso concreto en el que no> (usa <alternativa>)

**? Dudoso**
- <caso que depende del contexto y qué criterio aplicar>

**Contenido:** <textos cortos; verbos de acción; texto permitido para acciones, si existe una lista>.

## Aplicación

*Dónde se coloca en pantalla, con ejemplos reales (el componente en uso, no capturas).*

- <ejemplo 1: dónde va y por qué>
- <ejemplo 2>

## Accesibilidad

Rol: <…> · Teclas: <…> · Criterios WCAG: <nombre oficial y nivel>
Lista de control: [<enlace a la lista de control de este componente>]
Última revisión humana: <AAAA-MM-DD · persona · tecnología usada>

## Entrega a desarrollo

☐ Contrato (mínimo o completo) · ☐ Esta página · ☐ Tabla de nombres Figma ↔ código · ☐ Valores por defecto y estados comparados · ☐ Versión y fecha · ☐ Canal de consulta
**Formato en que desarrollo prefiere recibir los cambios:** <preguntado el AAAA-MM-DD → respuesta>

## Contacto

<Canal o persona para dudas>. Para proponer cambios: <cómo contribuir; ver gobierno del proyecto>.
