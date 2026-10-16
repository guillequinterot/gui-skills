# 02 · «Partes» para el constructor (texto ≤ 50 000 caracteres + ≤ 5 imágenes)

## Por qué
El chat solo admite texto (≤ 50 000 caracteres por mensaje) e imágenes (≤ 5). El diseño aprobado (CSS + HTML + kit + instrucciones) no cabe en un mensaje, así que se parte en **PARTE 1 … PARTE 5**.

## Estructura de la carpeta de entrega
```
entrega-N-<pagina>/
  A-IMAGENES-subir-a-Medios/        solo las imágenes NUEVAS de esa entrega (JPG/SVG/PNG con nombre final)
  B-REFERENCIA-adjuntar-en-Parte-1/ ≤ 5 capturas del diseño aprobado (desktop y móvil)
  C-COPIAR-Y-PEGAR/PARTE-1-de-5.txt … PARTE-5-de-5.txt
  D-AJUSTES-despues/AJUSTE-0..n.txt un prompt corto por archivo (cabecera, carrusel, formulario, mensajería, medición, revisión, publicar)
  E-solo-para-mirar/                UI kit visual (no se envía)
  LEEME-PRIMERO.txt                 pasos
  MANIFIESTO-IMAGENES.md            archivo → qué se ve (generado con scripts/manifest_imagenes.py)
```

## Reglas de las partes
1. **PARTE 1** lleva el encargo (qué se construye, reglas, tono) y se envía con las capturas de referencia. Responde «Parte 1 de 5 recibida.»
2. **PARTES 2-4** llevan, en orden, el contexto del proyecto/UI kit y el CSS+JS del kit; **no construye todavía**.
3. **PARTE 5** lleva el HTML de la página y la orden **«construir ahora»**.
4. El código se corta en puntos **estrictamente contiguos** y se **verifica que las partes recomponen exactamente el original** (hash). Cada parte ≤ 50 000 caracteres.
5. Si el constructor empieza antes de la PARTE 5: «Detente. Aún no he terminado de enviarte el material. Espera la PARTE 5 DE 5 antes de construir.»
6. **El CSS del kit no debe pisar Tailwind:** `.container` lleva `max-width:none; width:100%; margin-inline:0` (ver [07](07-incidencias-y-soluciones.md)). Evitar nombres de clase de Tailwind.
7. Antes de enviar los ajustes de mensajería (WhatsApp u otro) y de medición, **reemplazar los marcadores** (número, IDs) por los reales del cliente.
8. El texto del cliente va **literal**; lo pendiente va con `<span class="placeholder">`.

## Generación
`python scripts/make_partes.py <config.json>` arma las partes a partir de los archivos reales del proyecto (ver `scripts/make_partes.py` y el ejemplo `ejemplos/caso-web-universidad-01/partes.ejemplo.json`). Cualquier cambio de kit/CSS → regenerar. En el caso `caso-web-universidad-01` el primer lote (Home) lo generaba un script propio del proyecto a partir del HTML aprobado.

## Prompts de ajuste útiles
- AJUSTE-0: comparar con las capturas de referencia y corregir diferencias sin rediseñar.
- «Qué hiciste y qué falta» al terminar (la IA responde con su lista; contrastar con el código).
- Para conectar imágenes: ver [05](05-imagenes-medios-cdn.md).
