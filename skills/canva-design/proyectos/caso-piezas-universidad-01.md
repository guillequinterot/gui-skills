# caso-piezas-universidad-01 — ficha Canva (actualizada 2026-10-09)

Centro de educación continua de una universidad pública. Agencia: Los Creativos. Campaña de anuncios en Meta (24 ago – 10 dic 2026). Proyecto local y su HANDOFF/HANDSHAKE: en la PC del usuario, fuera del repo (son la fuente de verdad del estado). Nota de Obsidian: en el vault del usuario, si lo usa.

## Alcance y nomenclatura
36 programas (hoja de cálculo del cliente, pestaña de anuncios; col. B programa, E/F = copy 1/2) × 2 diseños × 3 formatos: **Post 1080×1080 (P) · Historia 1080×1920 (H) · Banner 1200×628 (B)**. Página = `N-F-slug-<marca>-cX` (N = orden de la hoja, c1/c2 = copy 1/2). **Contenido de la pieza = solo las columnas E/F** (literal); fijos de marca: barra de sede + lockup del centro y la universidad.

## Marca (la guía de identidad del cliente)
- Verde institucional (CTA) y rojo alterno; complementarios en tonos neutros. **Cada programa tiene su propia paleta/línea** (familias definidas en el documento de línea gráfica del proyecto).
- Tipografía: **una fuente institucional del cliente** (TTF en el kit de marca del proyecto). Está en el Brand Kit de Canva del cliente, **pero el importador de HTML no la aplica** (ver `references/08` §4); el usuario cambia la fuente en Canva **en bloque** (Canva reconoce la fuente de reemplazo y la cambia en todo el diseño) → **una sola familia y solo Regular/Bold/Italic en todas las piezas**.
- Logos SVG del lockup (blanco y negro) en el kit de marca del proyecto. Reglas del cliente: sin sombras/texturas/distorsión; área de protección ¼ del escudo; aval de comunicaciones previo a publicar; el hashtag institucional va en el copy de salida (no en la pieza).

## Canva
- Diseño de trabajo del usuario: un diseño con 63 páginas de tamaños mixtos = 9 programas × 7 páginas (portada negra 1080² + [P,H,B] c1 + [P,H,B] c2). Las partes 2/4…4/4 serán otros diseños. Las páginas actuales eran andamios sin título.
- **Copia de prueba** con el programa 1 montado; el original NO se modificó.
- **Diseños intermedios que la API no puede borrar** (4 en la prueba): borrar a mano.
- Assets subidos a la biblioteca de Canva (reutilizables): logo lockup blanco SVG, una persona recortada (PNG) y los fondos del programa 1 por formato y variante. Faltaba subir el logo negro y las fotos de los demás programas. Los ids de Canva no se guardan en el repo.
- La fuente de marca tiene en esa cuenta un `fontRef` propio (se conserva al editar cuadros que ya la usan; no asignable por API).

## Decisiones del usuario (2026-10-09)
Programa 1 aprobado como modelo · sin WhatsApp/correo ni etiquetas añadidas · cada programa con su línea · HTML de todos primero, luego fase de imágenes (Magnific, en otra cuenta/sesión), luego montaje en Canva · cambia la tipografía manualmente en Canva · quiere todo en el menor número de diseños de Canva posible (si no, lista de URLs).

## Autorización de montaje (2026-10-09, tarde)
El resultado final debe quedar **en el Canva de trabajo del usuario** (63 págs = 9 programas × 7: portada + P,H,B × c1,c2). El usuario **autoriza borrar las páginas andamio que él creó** (solo texto) a medida que se monta cada programa; las portadas se conservan salvo indicación contraria. Cada diseño se mantiene en 63 páginas → no hay problema de límite de páginas. Aun así: hosting temporal con autorización por tanda, `merge-designs` una operación por llamada y verificación por exportación antes de seguir.

## Pendientes
Aprobar los HTML 2–36 · fase de imágenes · montaje por tandas (partes 1/4…4/4) · limpiar diseños intermedios · corregir/registrar lo aprendido en `references/08`.
