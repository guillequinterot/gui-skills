# Videos aprobados por el usuario

> Vista generada por `scripts/save_approved.py` (fuente de verdad: `videos-aprobados.jsonl`). Cada entrada lleva la **cita textual** con la que el usuario aprobó. Una receta es una **recomendación que nombra su origen**, no una orden; lo «sin decidir» no es una preferencia. No editar a mano.

## V001 · Reel caso-reel-01 · 2026-10-16

- **Pieza:** Reel Instagram 9:16: obra de rotulacion de una gasolinera de un cliente de caso-reel-01 (8 fotos + 1 video + musica, sin voz) · 1080x1920 · 29.9 s · ruta `musica-al-compas` · motor hyperframes 0.8.162 (+ ffmpeg de Shotcut) · proyecto `<carpeta-del-proyecto>/caso-reel-01`
- **Mensaje:** Una empresa de rotulacion instala la rotulacion completa de una gasolinera, de las letras con LED a la marquesina terminada.
- **Aprobado por usuario:** «Está excelente está bien así en inglés y está perfecto sólo nos falta al final este cta con esta info // Genial el video no hagamos más nada esto fue un test (Guille, 2026-10-16; el CTA pedido se añadió después y la v3 quedó verificada)»
- **Aprobado explícitamente:** textos en ingles, descriptivos y sin promesas (propuestos por la IA, aprobados sin cambios); estructura resultado > proceso > alcance > tension > drop > funcion > CTA; diseno: tarjetas con foto y fondo desenfocado teñido de marca, push entre paginas, texto en mascara, muro de fotos en el drop; cierre con el CTA tomado de la captura de su Instagram: logo, barra de color de marca, llamado a pedir presupuesto, correo, telefono y web en mayusculas
- **Sin decidir (no usar como preferencia):** con o sin empuje de camara en las fotos: aprobo la pieza sin elegir entre reel_v3_row0 (con) y reel_v3_row1 (sin); la sincronia con la musica solo esta medida (122.0 BPM), no confirmada a oido; derechos de uso de la pista de musica usada y permiso del cliente para mostrar la marca de la gasolinera si se publica
- **Estructura:** S1 hero de la marca a sangre completa (0-4 s) > S2 video de letras LED en tarjeta (4-7.9) > S3 tres palabras con tarjeta (alcance: marquesina / surtidores / todo el sitio) (7.9-13.8) > persianas que cierran en el valle de la musica (13.8-15.8) > S5 drop: muro de 3 filas de fotos + titular de branding (15.8-21.7) > S6 titular «visto desde la carretera» (21.7-25.6) > S7 CTA con datos de contacto (25.6-29.9)
- **Receta:** Rejilla B(n)=q(t0+T*n) con T=0.4918 y t0=0.05 (beat_grid.py, 122 BPM); push de 0.6 s power3.inOut centrado en el tiempo; palabras con cortar-la-curva (salida power4.in 0.3 s, entrada power4.out 0.4 s); lineas con mascara yPercent 115>0; drop = corte duro con destello de 2 fotogramas; persianas scaleY 0>1 en 1.95 s power3.in; filas que entran con power4/expo/power3 y derivan lineales en direcciones alternas; pulso de escala 1.035 de una fila por tiempo; fondos pre-horneados (make_bgs.py); video como hermano en la raiz; render --batch con variable push 1/0; audio data-volume 0.85 + data-fade-out 1.5
- **Medido:** 29.90 s; -15.3 LUFS, pico -1.3 dBFS; hueco 0 % en los 4 push (cut_dip); fotogramas casi inmoviles 71 de 896; render 2m20s-2m40s por version; 24-36 MB a CRF 16; selftest 27/27

**Lo bueno (repetir)**
- Guille lo aprobo sin cambios de diseno ni de textos; el cierre salio de una captura de su Instagram en un solo mensaje
- Fotos horizontales en tarjeta + fondo desenfocado de marca: ninguna foto pixelada; solo la de 4080x3060 a sangre completa
- Verificacion en orden check > snapshot > render > ebur128 > cut_dip > self_eval > motion_energy: cada fallo se vio a tiempo
- Senales ancladas al compas en cada pausa >= 1 s: fotogramas casi inmoviles 189 > 71 de 896 (solo queda el CTA final)
- Render --batch con variables permitio dos variantes comparables con una sola orden (2 m 20 s - 2 m 40 s cada una)

**Lo malo (evitar)**
- Los datos de contacto del CTA se pidieron al final: rehacer la escena y re-renderizar (+5 min). Pedirlos en el brief
- Rejilla de compas por autocorrelacion gruesa (123 BPM) desplazo los cortes hasta 0.2 s: render completo repetido y otro cancelado (~6 min). Medir con beat_grid.py antes del primer render
- Dos tl.set sobre el mismo elemento dejaron una escena fuera de cuadro y check salio en verde: mirar la hoja de contacto de snapshot antes de renderizar
- Un index_v1.html dentro del proyecto dio multiple_root_compositions: guardar versiones fuera de la carpeta de HyperFrames
- Primer diseno con el tercio inferior vacio en 4 escenas (la interfaz tapa 1500+): centrar el contenido a y 800-900
- Un archivo de 36 MB no cabia en el envio (30 MB): hacer una copia ligera con crf 24 y marcarla como vista previa

**Archivos:** `<carpeta-del-proyecto>/hyperframes/index.html`; `<carpeta-del-proyecto>/hyperframes/renders/reel_v3_row0.mp4`; `<carpeta-del-proyecto>/hyperframes/renders/reel_v3_row1.mp4`; `<carpeta-del-proyecto>/storyboard/storyboard_board_v3.jpg`; `<carpeta-del-proyecto>/video-handoff.md`

Etiquetas: reel, instagram, vertical, musica, fotos, sin-voz, gasolinera, hyperframes, cta, motion-graphics
