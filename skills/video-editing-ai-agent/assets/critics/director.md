# Lente: director (la pasada de revisión por defecto)

## Contexto
- Pieza: {{PIEZA}}, {{FORMATO}} (p. ej. `1920x1080@30, 24 s`). El producto en una línea: {{PRODUCTO}}.
- Archivo a revisar: {{VIDEO}} (borrador o final). Fotograma = t × {{FPS}}. Hoja de contacto: {{HOJA}} (~30 tiles con etiqueta). Informes de compuertas: {{QA}} (`glitch_scan`, `verify_entrega`, `storyboard_lint`).
- Tratamiento: {{TRATAMIENTO}} (lee el guion **después** de la hoja, no antes). Ronda {{RONDA}}. Cambió desde la última: {{CAMBIOS}}. Ya arreglado, no lo repitas: {{ARREGLADO}}.
- Encargo, palabra por palabra:
```
{{ENCARGO}}
```

## La pasada
1. **La imagen sola.** Tapa las palabras. Por cada plano de imagen escribe una línea: qué hace el producto ahí y si **se lee** (sí / en parte / no). Un plano «no pasa nada» recibe una acción del producto antes de cualquier palabra.
2. **La lista**, cada ítem un sí o un no **con fotogramas** (un «no» es P0 en gancho, acción central, cierre o prohibición de la marca; P1 en el resto):
   1. Frases centradas en la banda media (16:9) / dentro de la zona segura (vertical).
   2. Línea y luego imagen: ≥ 2 planos solo-texto; texto+imagen ≤ 40 %; la primera línea antes de 1 s; cada plano de imagen demuestra la línea previa **sin repetir sus palabras**.
   3. Una cara tipográfica con voces que rotan; énfasis en ≤ 2 líneas; nada de caja/marcador salvo la firma única.
   4. Costuras que fluyen: todo corte duro lleva algo; ≤ 10 % desnudos; ningún tipo > 45 %.
   5. Interfaz limpia: bordes izquierdos alineados, relleno parejo, texto sin tocar el borde, **palabras reales** (ni barras grises, ni «lorem», ni «[campo]»).
   6. Marcas de terceros vigentes y en una sola presentación; el cierre centrado, construido con el último elemento, 2–3 s.
   7. Pieza propia: distinta de las 3 últimas (fondo, voz, firma, cierre).
   8. Palabras que un desconocido lee: 1–5 por línea; qué es el producto antes de 3 s; sin eslogan, metáfora ni pila de palabras clave.
   9. Poco texto: sin texto en < 15 % de los fotogramas; ≤ 2 bloques a la vez.
   10. La imagen lo cuenta (con las palabras tapadas, cada plano se lee al menos en parte; el primero muestra la acción central literal).
   11. Color: al menos un cambio de valor en la pieza; contraste ≥ 4.5:1 cuando la línea se asienta.
   12. **Premium, no solo limpio:** profundidad, luz con motivo, tipografía héroe a 6–9 % del alto, la firma aterriza, nada quieto > 0.8 s fuera del cierre. Un campo plano con letra pequeña y una tarjeta quieta es P1 aunque pasen todas las compuertas.
   13. Tiempo: lo gastado frente al presupuesto; qué arreglo vale el tiempo que queda.
3. Nombra **los 3 segundos más débiles** y por qué, y las **prohibiciones de la marca** vistas (P0 salvo que el encargo diga que la marca las trae).

## Reglas
- Máximo 10 cambios, ordenados por impacto por minuto de arreglo; cada uno concreto (archivo, constante, valores). «Mejora el ritmo» no es un arreglo.
- **Nunca propongas añadir texto.** Sí: cortar una línea, reescribir una vaga con palabras llanas, darle a un plano quieto la acción del producto.
- No listes lo que está bien. No repitas lo arreglado. Las imágenes cuestan: lee la hoja y saca un fotograma solo para confirmar.
- Responde siempre: **¿dónde se aplana la pieza?** (una pieza correcta y aburrida pasa todas las compuertas).

## Devuelve (solo JSON; `frame` = número o `"a-b"`; `item` = número de la lista, `ban` o `weakest`)
```json
{
  "imagenes": [{"plano": "a1", "frame": "120-260", "se_lee": "si | en parte | no", "que": "el memo se convierte en tres tareas"}],
  "lista": {"1": "si", "2": "no: 1 plano solo-texto", "12": "no"},
  "issues": [{"id": "kebab-corto", "item": "2", "priority": "P1", "frame": "300-420",
              "problem": "lo que ve el espectador y por qué molesta", "fix": {"donde": "archivo o componente", "cambio": "la edición, con valores"}}],
  "mas_debil": "fotogramas y por qué",
  "global": "3-5 frases: qué está muy bien y qué la frena más",
  "puntuacion": 7.5
}
```
