<!--
PLANTILLA · contrato-minimo
Para qué: decir qué ES un componente y cómo se usa, antes de construirlo. Lo lee una persona para decidir, una IA para no inventar y un verificador para comprobar.
Modo: contrato · Perfil: website (también vale para empezar en app o sistema compartido) · Referencia: references/01-contrato.md (secciones 3, 5, 6, 7 y 14)
Cómo se usa: un archivo por componente, con el nombre del componente. Se escribe ANTES que el código: diseño lo define y desarrollo completa la anatomía.
Reglas: propósito en UNA frase desde quien lo usa · «Nunca usar para» con la alternativa nombrada · los nombres de las partes son los mismos en código y en Figma · no copies cifras que se desactualicen (cuéntalas con un script).
`scripts/validar_contrato.py` comprueba la forma de este contrato. Si no se ejecutó, no se escribe «válido»: se escribe «revisado a mano» con la fecha.
-->

# <Nombre del componente>

**Propósito:** <una frase, desde quien lo usa>.
**Nunca usar para:** <uso que no corresponde> (usa <alternativa>) · <otro uso> (usa <alternativa>).
**Justificación:** <la decisión y su motivo, en una o dos frases>.
**Se adapta en el proyecto:** <cambios permitidos sin pedir permiso, p. ej. añadir un icono, pasar una etiqueta accesible>.
**Se escala al sistema:** <cambios que alteran lo compartido, p. ej. una variante nueva, cambiar relleno o altura>.
**Anatomía:** `<parte-raiz>` (raíz, <elemento HTML>) · `<parte>` (<elemento o hueco>, opcional) · `<parte>` (<elemento>).
**Estados que se entregan:** normal · hover · foco · deshabilitado · <otros: cargando, error…>.

## Opcional pero recomendado

**Origen:** <sistema propio / librería abierta (cuál) / tercero> · **Código:** <ruta o repositorio> · **Figma:** <archivo y nombre exacto de la capa o el componente>.
**Regla para la IA:** usa este componente, no el equivalente de la librería base.
**Fuente de verdad:** <contrato/código | Figma> *(la registrada en el plan de arranque)*.

## Estado de la revisión

☐ Revisado a mano contra la lista de revisión de la referencia 01 (sección 14) · **Fecha:** <AAAA-MM-DD> · **Por:** <persona>
☐ Validado por un verificador *(solo cuando exista; indicar cuál)*
**Lo que no se comprobó:** <…>
