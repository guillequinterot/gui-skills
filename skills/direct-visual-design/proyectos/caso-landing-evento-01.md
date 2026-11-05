# caso-landing-evento-01

**Tipo:** landing de evento (día familiar de entrada libre) de un proyecto inmobiliario campestre; entrega en HTML estático para montarse en WordPress. Objetivo: registros por formulario.

## Situación de partida
La landing venía construida con el **sistema azul corporativo genérico de la constructora** (azul marca frío). El **proyecto** dentro de esa constructora tiene identidad propia **cálida y campestre** (verde naturaleza + naranja «sol» + dorado + cremas), visible en su sitio real y en su logo (un sol). El azul frío remaba en contra del concepto del evento («un verano mágico»).

## Decisión de dirección
Re-skin a la identidad **del proyecto**, no la de la constructora madre, **conservando estructura, textos y nombres de clase** (el entregable se pega/sube a WordPress; no romper el handoff). Concepto: «un domingo de sol».

## Mapeo cromático (rol del sistema → color del proyecto)
- **Verde oscuro** → estructura: header, footer, títulos, texto.
- **Naranja «sol»** → CTAs y acentos (color de acción de la marca; es el color del logo).
- **Dorado** → badge y detalles cálidos.
- **Azul claro** → fondos suaves puntuales (no protagonista).
- **Crema cálida** → fondos de sección (reemplaza el gris frío; da el aire campestre).

## Decisión de contraste (reutilizable)
El naranja de marca **brillante** con texto blanco da ~2.5:1 → **insuficiente** para botones con texto. Solución aprobada por el dueño:
- **CTA con texto:** usar una variante **más profunda/terracota** del mismo naranja (reposo ≈ 4.67:1 AA, hover aún más oscuro ≈ 6:1).
- **Naranja brillante:** reservado a **acentos sin texto** (resplandor del hero, punto del badge, iconos, viñetas) para no perder el brillo «verano».
- Badge: fondo dorado + texto verde oscuro (≈ 5:1 AA).
- Eyebrows y enlaces legales: verde (no naranja), por contraste de texto pequeño.

## Verificado
Sin desbordes horizontales 360–1440, responsive (móvil/tablet/desktop), contrastes de texto 7–9:1 y CTA/badge AA. Entregable comprimido con **solo los archivos referenciados** por la página (se excluyen logos/imágenes del folder de trabajo que no se usan).

## Pendiente / no verificado
- El montaje real en WordPress y la conexión del formulario (spreadsheet/webhook) los hace el programador; no se probó en vivo.
- Enlaces de header/footer y de política de datos son marcadores a confirmar con el cliente.
