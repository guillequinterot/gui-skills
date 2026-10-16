# Biblioteca de movimiento (animación de video)

Destilada de: video-use, super-video-maker, video-shotcraft, promo-video-skill, VideoZero/animation-basics, más la edición real caso-video-02. Los valores marcados [~] vienen de resúmenes; verifícalos con una vista previa antes de fijarlos. Frames a 30 fps salvo indicación.

## 1. Principios
- **Nunca lineal**: easing cúbico. `ease_out_cubic = 1-(1-t)^3` (entradas/revelados); `ease_in_out_cubic = 4t^3 (t<.5) | 1-(-2t+2)^3/2` (movimientos continuos). Salidas: ease-in.
- Una técnica de movimiento por plano. Máx. 3 impactos de pantalla completa por video. Una transición por unión.
- Nunca un frame estático largo: "creep" de zoom lento (~+4 %/s, tope +9 %).
- Ver-luego-oír: el visual aparece 6–18 frames ANTES de la palabra; nunca más de 4 frames tarde (tolerancia ±3–4 f).
- Arco de tempo: lento → medio → rápido (clímax) → lento.

## 2. Tabla de timing
| Movimiento | Duración | Curva |
|---|---|---|
| Entrada de texto/objeto | 0.3–0.5 s (9–15 f) | ease-out (o pop 0.78→1.12→1.0 en 3+4 f) |
| Salida | 0.2–0.3 s (6–9 f) | ease-in; fade ≥3–4 f |
| Cambio en sitio | 0.3–0.8 s | ease-in-out |
| Énfasis / overshoot | 0.2–0.3 s | spring |
| Stagger palabras | 40–80 ms; elementos 100–150 ms | — |
| Transición dissolve/luma | 8–14 f (0.25–0.45 s) | — (usada: 10, 10, 14 f) |
| Flash-cut | 10 f, opacidad 0→0.85→0 | [~] |
| Whip-pan | 8 f de latigazo, blur solo ahí | [~] |
| Crash zoom | 6 f empuje 1x→2.6x, 5 f recuperación | bezier(.55,0,.7,1) [~] |
| Push-in lento | 1.0→1.14 en 4 s | ease-in(quad) [~] |
| Speed ramp | rápido ≥2×, lento ≈0.2×, contraste ≥10× | máx 2 por 30 s |

## 3. Reencuadre y zoom (lo aplicado en caso-video-02)
- Talking head vertical: zoom 1.00→1.12 (clip 1), 1.14→1.02 (clip 2), 1.02→1.14 (clip 3): alternar acercar/alejar entre clips.
- Anclaje arriba (`a=0.22`): `center_y = a + s(0.5−a)`. 5 keyframes con smoothstep: p=0,.25,.5,.75,1 → e=0,.156,.5,.844,1 (`scripts/ease_keyframes.py`).
- Fuente de baja resolución escalada ≥2× queda suave: `unsharp` leve y avisar.
- Cámara "handheld" (solo si el plano lo pide): `amp·(sin(0.31f)+0.6·sin(0.83f+1.7))` en X y `amp·(sin(0.47f+0.9)+0.5·sin(1.13f+3.1))` en Y, amp≈0.012; nunca en UI/producto.

## 4. Transiciones (una por unión)
- **Dissolve/luma** 8–14 f: seguro para talking head (caso-video-02).
- ffmpeg `xfade`: `smoothleft/smoothup/fade/dissolve` 0.25–0.35 s. Evitar `zoomin` (pixelado).
- Flash-cut, túnel oscuro (8–12 f entrar, 4–8 f oscuro, 10–14 f salir), traspaso de foco (crossfade 10–16 f con blur 0→8 px), tarjeta negra (6–10 f/lado, máx 2 por 30 s), whip-pan (20 f hold + 8 f). Mantener dirección: si sale por la derecha, entra por la derecha.
- Presupuestar frames: duración efectiva = suma de escenas − nº transiciones × duración.

## 5. Ritmo de cortes
- Beat visual nuevo cada 2.0–2.5 s; hold máx 3.5 s; sub-eventos 0.3–0.5 s; apertura ≥3 s; hold de marca ≥1 s.
- Cortes por audio: silencios ≥400 ms limpios; límites de frase 150–400 ms con verificación; <150 ms inseguro. Padding 30–200 ms (50 antes/80 después estándar). No cortar dentro de una palabra.
- Acelerando: intervalos 16→12→8→6→4 f con 1 f de brillo 1.05 [~].
- Solape de entrada del siguiente elemento 4–8 f antes de la salida del actual.

## 6. Texto animado
- Palabra por palabra (usado): un clip por palabra, pop 0.78→1.12 en 3 f → 1.0 en 7 f, opacidad 0→1 en 3 f, la última de cada frase con fade-out de 4 f; palabras clave en color de acento; tamaño 112 px (una palabra) / 84 px (frase) sobre banda `#a6000000`.
- Reglas: fuente ≥56 px (subtítulo narrativo, 1080p), ≥32 px secundaria; peso 900/700 (sin pesos finos); un solo acento; máx. 2 tipos de entrada de título por pieza.
- Otros: relleno karaoke (capa base gris + activa con recorte de izquierda a derecha), type-on (centrar sobre el ancho de la cadena COMPLETA), scramble-decode [~], letter-drop con rebotes 30 % y 9 % [~].
- Estilos de subtítulo animado nombrados (video-db): `box_highlight, color_highlight, reveal, karaoke, impact, supersize` — solo vocabulario.

## 7. Springs (motores con física; referencia numérica)
`{mass:1, damping:11, stiffness:210}` pop con leve rebote; cámara rígida `16/250`; lista `13/200`; word pop `10.5/230`. damping 8–12 rebote, 15–20 suave, 25+ seco. Micro-rebote: `exp(-t/7)·sin(t/1.9)·0.035`. En MLT/Shotcut no hay springs: precalcula la curva y vuélcala como keyframes (`ease_keyframes.py --spring`).

## 8. Motion blur
Sin blur bajo 3.5 px/frame; por encima `blur=min(8,(v−3.5)·0.28)`. Movimientos <9 f: 1–3 f de blur direccional. (Solo en motores que lo soporten.)

## 9. Lista anti-plantilla
No "AI slop": pills totalmente redondeadas con glow, gradientes morados, mismas mecánicas repetidas, más de 6 objetos a la vez, revelar dos cosas nuevas en paralelo.

## 7. Doctrina para piezas compuestas (v1.3)
Para animación de ilustraciones, motion graphics y tarjetas sobre un talking head, ver `references/motion-doctrine.md` (reglas de costura, recetas con números y tabla de compatibilidad con esta biblioteca).

