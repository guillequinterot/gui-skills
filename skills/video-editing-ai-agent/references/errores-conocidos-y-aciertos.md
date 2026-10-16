# Errores conocidos y aciertos (léelo antes de construir una pieza)

Lista de verificación viva, sacada de **piezas reales aprobadas** (cada línea cita su evidencia y, si lo hubo, su costo). Una pieza aprobada se guarda además con `scripts/save_approved.py` (biblioteca `memoria/videos-aprobados.md`). Si esta lista y la realidad chocan, manda la realidad: corrige la línea y registra el cambio con `scripts/log_update.py`.

Piezas de origen: **V001** Reel «caso-reel-01» (2026-10-16; HyperFrames; música al compás; 29.9 s).

## 0. Antes de tocar nada (preguntas y medidas que ahorran un re-render)
| Hacer | Por qué / evidencia (V001) |
|---|---|
| **Pedir de una vez todo lo que falta**: CTA y datos de contacto (correo, teléfono, web), idioma, si se muestra la dirección. Si la marca ya tiene una pieza de cierre, pedir **su captura** | Los datos de contacto llegaron al final: hubo que rehacer la escena de cierre y volver a renderizar (+5 min). La captura del Instagram de la marca dio el diseño exacto del cierre en un mensaje |
| **Medir la música antes del primer render**: `python scripts/beat_grid.py musica.mp3 --end 31` | La rejilla por autocorrelación gruesa (123 BPM) dejó los cortes hasta 0.2 s antes del golpe; se detectó tras un render completo y hubo que repetirlo (el render en curso se canceló: ~6 min perdidos) |
| **Revisar medidas de los medios** (`ffprobe`) y decidir la forma de uso | Fotos de 1600×747 en lienzo 1080×1920: recortar a vertical = ampliación 2.6× (pixelada). Solución aprobada: tarjeta + fondo desenfocado de la misma foto, y solo la foto de 4080×3060 a sangre completa |
| **Usar el copy literal y avisar lo propuesto**: si no hay texto del cliente, proponer textos descriptivos (lo que se ve), sin promesas ni cifras, y marcarlos «propuestos» en el brief | V001: textos en inglés propuestos, aprobados sin cambios («está bien así en inglés y está perfecto») |
| **Ver el video de origen** antes de usarlo (un fotograma por tramo) | El video de 848×478 solo servía en tarjeta (4× de ampliación a sangre completa) |
| Si hay una línea gráfica de marca, **leer su handoff completo** (paleta, zona segura, logo) aunque el motor sea otro | Se respetó identidad, no herramienta: el handoff de la marca (caso-reel-01) pedía su propio script de armado, pero el pedido (motion graphics) exigía HyperFrames |

## 1. Construcción en HyperFrames
| Hacer | Evitar (error real) |
|---|---|
| **Declarar el estado inicial de cada elemento una sola vez** | Dos `tl.set` sobre el mismo elemento en t = 0: una escena quedó **fuera de cuadro** y `check` pasó en verde; solo lo mostró `snapshot` |
| **Mirar una hoja de contacto (`snapshot --at …`) antes del primer render**, con un instante en cada escena y en cada corte | `check` no ve contenido ausente ni composiciones vacías |
| Guardar las versiones **fuera** de la carpeta del proyecto (`../versiones/`) | `index_v1.html` dentro del proyecto → `multiple_root_compositions` |
| `<video>` como **hermano en la raíz** (no dentro de una escena con `data-start`), movido con su propio tween de `x` sincronizado con el push | Anidarlo da `video_nested_in_timed_element` |
| Texto decorativo grande con **relleno de baja opacidad** (9 %) | Texto con contorno (`color: transparent` + `-webkit-text-stroke`) = error `text_not_painted` |
| `render --batch filas.json -o "x_row{index}.mp4" --strict-variables` para variantes A/B | Sin `{index}`: «Batch output collision» |
| **Fondos pre-horneados** (foto desenfocada + tinte de marca + ruido fino, semilla fija) | Degradados lineales de pantalla completa sobre oscuro: bandas en H.264 |
| **Centro de masa del contenido a y ≈ 800–900** (zona segura 250–1500; la interfaz tapa 1500+) | Primer diseño: el tercio inferior quedaba vacío en 4 escenas |
| Texto en **máscara de línea** (`overflow:hidden` + `yPercent` 115 → 0) y palabras que cambian con **cortar la curva** (salida `power4.in` 0.3 s, entrada `power4.out` 0.4 s) | Entradas con rebote o todo a la vez |
| Push entre páginas de 0.6 s `power3.inOut` **centrado en el tiempo de compás** | Cortes a sangre completa con opacidad: hueco oscuro (ver `motion-doctrine.md` §7) |
| Poner **una señal en cada pausa ≥ 1 s** (subrayado que barre en el tiempo 2 del grupo, deriva lenta de un número gráfico, pulso de escala ≤ 1.04, empuje de foto ≤ 8 %) | Una escena con todo entrando en el primer segundo y luego quieta: 189 fotogramas casi inmóviles de 881 (bajó a 71 tras añadir señales; solo queda el CTA final) |

## 2. Música y audio
| Hacer | Evidencia |
|---|---|
| Sin voz: **sin carve ni duck**; `<audio data-volume="0.85" data-fade-out="1.5">` | −15.3 LUFS, pico −1.3 dBFS sin `loudnorm` |
| Anclar todo a `B(n) = q(t0 + T·n)` con `T, t0` de `beat_grid.py` (cuantizado a 1/fps); hit visual del «drop» con un destello de 2 fotogramas | v1 (123 BPM): saltos de amplitud en los cortes ×0.4–0.8 (cortes fuera de golpe); v2: ×3–5 (en el golpe) |
| Anticipar el efecto visual ~0.1 s | `motion-doctrine.md` §10 |
| **No interpretar «posible clic» de `self_eval.py` en una pieza al compás como fallo**: es el bombo en el corte; confirmar que la fuente es un solo archivo continuo | Falsa alarma en 3 de 4 empujes |
| **Confirmar la sincronía a oído** (o con un golpe visual) | `beat_grid.py` mide, no oye |

## 3. Verificación (orden que funcionó)
1. `check` (0 errores; los avisos de contraste de numerales decorativos son esperables). 2. `snapshot --at …` + hoja de contacto: **mirarla**. 3. Render. 4. `ffprobe` (resolución, duración, códecs). 5. `ebur128` (−16…−14 LUFS, TP ≤ −1). 6. `cut_dip.py --cuts …` (hueco 0 % en los push). 7. `self_eval.py --boundaries … --expected-duration …`. 8. `motion_energy.py A.mp4 [B.mp4]` (tramos quietos y diferencia A/B). 9. Tablero con fotogramas reales (`storyboard/make_board.py` del proyecto V001 como modelo). 10. Reportar **medido / visto / no verificado**.

## 4. Con el usuario
- **Aprobado ≠ elegido**: el usuario aprobó la pieza y el inglés pero **no eligió** entre con y sin empuje de cámara; se guarda como «sin decidir», no como preferencia. Si hace falta decidirlo, se pregunta una vez con las dos versiones a la vista.
- Para enviar un video de más de 30 MB por el canal de archivos: copia ligera con `ffmpeg -crf 24 -c:a copy -movflags +faststart` (8 MB), claramente marcada como vista previa; el original no cambia.
- **No exportar ni entregar fuera del proyecto sin petición explícita** (se cumplió: `salida/` quedó vacía hasta que se pida).
- Lo que el usuario dice de una pieza aprobada se guarda con su **cita textual**; es la evidencia más fuerte que hay de su gusto (más que cualquier regla escrita), pero sigue siendo una recomendación con origen, no una orden.

## 4b. Cuando el trabajo es APRENDER de videos (sub-skill `video-aprender`)
Errores y recetas medidas con 11 reels de Instagram (2026-10-16): `skills/video-aprender/references/procedimiento.md` §7b y `references/handoff-handshake.md` §3b. Lo esencial: `-o <proyecto>` siempre; lote en segundo plano (`aprender_lote.py`); `--glosario <dominio>`; si la pantalla es una cámara filmando un monitor, leer primero `hoja.jpg` del muestreo; recalcular todo lo recalculable (una afirmación del reel resultó falsa); clasificar la fuente (captación = pistas, no evidencia); leer la plantilla del proyecto de destino antes de volcar ideas.

## 5. Dónde registrar lo aprendido (siempre al cerrar)
`video-handoff.md` del proyecto (medido/visto/no verificado) → `scripts/save_approved.py add` (si el usuario aprobó, con su cita) → `scripts/log_update.py` (fallos y verificaciones) → entrada en el «Registro de trabajos» del `HANDOFF.md` (con `tools/log_job.py`; si el usuario usa Obsidian, también su nota del proyecto y el registro de skills) → si es una lección general nueva, **una línea aquí** con su evidencia.

## 6. Rehacer una pieza rechazada por el usuario (caso-reel-02, 2026-10-16)
Origen: video entregado a medias por otra IA; el usuario dijo «la verdad el video no me gusta nada». Auditoría y rehacer medidos.
| Hacer | Evidencia |
|---|---|
| **Comparar voz y video antes de mirar el diseño**: `ffprobe` de la voz, `transcribe_words.py`, y cruzar con las escenas | La voz duraba 10.8 s en un video de 30 s: 18 s mudos, sin CTA hablado, y decía «verifica la plataforma» mientras se veía la escena 1 |
| **Una hoja de contacto del estado heredado** (`snapshot --at`) | Escenas que solo se mostraban (`autoAlpha:1`) y nunca se ocultaban: texto encimado en 4 de 6 fotogramas; fotograma en blanco en 1.5 s |
| **Cada escena entra Y sale** (`push()`) y **su contenido llega dentro de la página** (títulos revelándose desde −0.2 s del centro del push) | `cut_dip.py`: hueco 26 % en 16 fotogramas con títulos tardíos → ≤ 6 % al adelantarlos |
| **Subtítulos de frase: ocultar la anterior antes de entrar la siguiente** (`min(fin+0.45, siguiente−0.30)`, salida 0.14 s) | Frases solapadas en la hoja a 17.9 s |
| **Medir `motion_energy.py` tras mover tiempos**: adelantar entradas deja tramos quietos nuevos (191 → 244 fotogramas) | Solución: empuje de cámara 1.0→1.028 por escena + barrido lima en las pausas |
| **Recortes locales de objetos neón**: fondo negro → alfa por luminancia (`color=rgb/alfa`); fondo gris → máscara de píldora con plumas; recolor de naranja a lima por HSV | Escudo+candado de stock con candado naranja quedó en la paleta de marca sin pagar recortes |
| **Tipografía: la marca manda, no el UI kit viejo** — leer el paquete de logo vigente | El logo de la marca cambió (Montserrat); los diseños aprobados antiguos llevan el logo anterior y Poppins |
| **Presentar el guion antes de gastar créditos de voz** y reutilizar la voz aprobada (ids y ajustes en el handoff del proyecto) | Voz completa 74 créditos; la muestra rechazada ya se había cobrado |
| `.ln{overflow:hidden}` con `padding-bottom/margin-bottom` de 20 px | Con 8 px se recortaban los descendentes (`check`: `container_overflow`) |
| Montserrat es más ancha que Poppins: bajar el nombre del producto de 150 a 128 px | Se salía del cuadro en la hoja de contacto |

**Plantilla de marca reutilizable:** cuando una marca ya tiene una pieza aprobada, guarda en la carpeta de su proyecto una plantilla (HTML aprobado + `captions_from_transcript.py` + `render_and_verify.sh`) y una receta corta de la pieza; en la siguiente, imitar la pieza aprobada (p. ej. V002 de la biblioteca) antes que inventar un estilo. La ruta concreta va en la nota del proyecto, nunca aquí.
