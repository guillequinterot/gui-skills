# Plan de planos (tabla) — se valida con `python scripts/storyboard_lint.py plan.md [--script guion.txt] [--expected-duration S]`

> **Bloqueo de estilo (3 líneas, antes de la tabla; una sola vez por pieza)**
> - **Estilo:** una frase (un solo estilo; nombrado por una referencia real, no por adjetivos)
> - **Paleta:** nombre o 3–6 hex con rol (fondo / texto / UN acento) — los hex que teclea el usuario ganan a los muestreados
> - **Personajes:** ninguno | solo manos y espalda | banco de fotogramas del usuario
>
> **Hechos** (lista aprobada): todo nombre, fecha y cifra que salga en pantalla está aquí con su fuente. Lo ilustrativo se etiqueta como tal.

Reglas que el lint comprueba (ROJO = corregir antes de escribir código; AMARILLO = mirar):
**objeto** = un sustantivo concreto (no «título», «tarjeta», «fondo»); **acción** = un verbo que HACE algo (no «aparece»/«muestra»); texto en pantalla corto (≤ 6 palabras por defecto) y que no repita la locución; planos de ~2–6 s (> 8 s = ROJO); primer y último plano no dominados por texto; texto dominante ≤ 30 % de los planos; no 3 planos seguidos con la misma cámara ni 3 empujes hacia dentro; acentos de cámara ≤ 1/3 de los planos; huecos o solapes en el tiempo; cada cifra en pantalla aparece en el guion (`--script`).
Umbrales de partida de las fuentes, **sin calibrar con nuestro material**.

| tiempo | objeto (sustantivo) | acción (verbo) | cámara | texto en pantalla | cómo se hace |
|---|---|---|---|---|---|
| 0-3 | una mano | rasga la bolsa y saca el pan | parada | pan con moho | clip de mano + sonido de bolsa |
| 3-6 | una rebanada | se llena de motas verdes | empuje lento | | 3 capas, motas con semilla fija |
| 6-9 | un frasco | se cierra con su tapa | paneo | | |
| 9-12 | el congelador | recibe la bolsa | parada | guárdalo frío | cierre con acción, no con eslogan |

**Variante `timeline.json`** (fuente única de verdad si la pieza se genera por código; el lint acepta este formato):
```json
{"meta": {"w": 1080, "h": 1920, "fps": 30, "dur": 12},
 "scenes": [{"id": "gancho", "start": 0, "end": 3, "object": "una mano", "action": "rasga la bolsa", "camera": "parada", "text": "pan con moho"}],
 "texts": [{"role": "hook", "from": 0.2, "to": 3, "px": 96}, {"role": "cta", "from": 10, "to": 12, "px": 56}]}
```
Los componentes referencian **beats con nombre** (nunca números de fotograma); los SFX y subtítulos se derivan de las líneas de voz o de los beats (nunca tiempos escritos a mano). Gancho: texto con rol `hook` visible antes de 3 s; suelos orientativos a 1080 px de lado corto: gancho ≥ 84 px, CTA y términos ≥ 48 px.
