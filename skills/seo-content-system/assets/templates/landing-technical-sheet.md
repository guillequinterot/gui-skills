# Ficha técnica de landing (por equipo)

> Checklist de cuatro bloques que Account diligencia completo antes de entregarlo a SEO, UX y pauta. Cada campo lleva su **objetivo** y su **instrucción**. Estructura observada en una ficha interna; el ejemplo relleno de la ficha original era ficticio y aquí no se copia.

**Landing:** {nombre} · **Oferta única:** {una sola} · **Responsable de Account:** {rol}

## Account
- [ ] Ficha completa antes de entregarla a los demás equipos.

## SEO · contenido
| Campo | Objetivo / instrucción |
|---|---|
| Objetivo de la landing | {una frase} |
| Buyer journey | Una etapa del embudo + justificación en una frase |
| KW research de SEO y de pauta | 5-10 keywords transaccionales por canal |
| Texto introductorio | 2-3 líneas: beneficio, propuesta de valor y keyword principal |
| Meta title / meta description | Dentro del límite del cliente; un solo beneficio |
| Estructura H1-H3 | Un H1; secundarias en H2/H3 |
| CTA primario / secundario | Verbo de acción + beneficio; el secundario va tras los beneficios; contraste alto |
| Beneficios | 3-5, concretos y medibles, cerca del CTA |
| FAQ | 3-5 relevantes para la conversión |
| Prueba social | Arriba o junto al formulario; solo real y verificable |
| Legitimidad | Footer con privacidad, términos, aviso legal, datos legales y dirección |
| Requisitos técnicos | Metadatos completos, schema del tipo de negocio, enlaces internos, Open Graph, canonical |
| Canales de contacto | Cada botón apunta al canal correcto |

## UX
- [ ] Coherencia visual: la imagen del anuncio refuerza el mensaje de la landing.
- [ ] Diseño de escritorio (enlace al prototipo marcado «Aprobado por el cliente»).
- [ ] Responsive mobile-first validado en los anchos acordados.
- [ ] Fotografías reales y de buena calidad.
- [ ] Accesibilidad: contraste AA, texto mínimo 16 px, alt, botones grandes, puntaje de la herramienta de accesibilidad por encima del umbral acordado (adjuntar puntaje y acciones).
- [ ] Menú fijo con logo, anclas y CTA; footer.
- [ ] Orden de secciones: Hero → Beneficios → Producto / servicio → Experiencias → Testimonios → FAQ → CTA final → Footer.

## Pauta (SEM)
- [ ] Objetivo de medición: conversiones, clics en WhatsApp, clics en CTA, scroll.
- [ ] Formulario con fricción mínima (3-5 campos).

## Front
- [ ] LCP dentro de la meta acordada (compresión, lazy load, WebP).
- [ ] Píxeles (Meta, GA4, GTM) con eventos nombrados.
- [ ] URL amigable, corta y con la keyword.

## Prototipo (opcional, con IA)
Una celda concatena todos los campos (`=TEXTJOIN(CHAR(10)&CHAR(10);TRUE;…)`) en un prompt para generar el prototipo; el resultado se captura y se importa al diseñador. Guardar el prompt para regenerar la fórmula cuando se añadan campos. **El prototipo no se publica ni se envía al cliente sin la compuerta de aprobación visual.**

## Etapa de revisión
- [ ] QA por área (Account, SEO, UX, pauta, front): CTA, formularios, enlaces, enlaces de seguimiento, velocidad, estructura, diseño y copy.
- [ ] Correcciones adjuntas **antes** del lanzamiento.
