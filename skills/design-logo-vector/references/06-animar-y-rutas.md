# 06 — Animar y rutas hacia otras herramientas

## 1. Logo animado (traspaso, no se hace aquí)

Esta skill **no anima**. Prepara el insumo y traspasa:

1. El SVG estático ya pasó *vectorizar*/*crear* (suave, estructurado, verificado). **Minimal suave = animable**: un logo de 3 partes semánticas se coreografía limpio; uno de 400 nodos por píxel no.
2. Estructura para movimiento: una parte por elemento o `<g>` con id estable (`#simbolo`, `#punto`, `#wordmark`, letras sueltas si se van a mover por separado). Ancla las animaciones a esos ids.
3. Escribe el **brief de movimiento** antes de tocar geometría: 3 palabras de personalidad derivadas del propio lenguaje visual (geométrico → movimiento de ingeniería, orgánico → fluido, redondeado → suave/rebote) y el contexto de uso: *splash/intro* ~1200–2000 ms, *revelado en cabecera* ~300–800 ms, *carga* en bucle, *hover* ~150–300 ms (órdenes de magnitud de partida, no reglas).
4. **Contrato del fotograma final:** la animación debe aterrizar **exactamente** en el SVG estático verificado.
5. Entrega a **`video-editing-ai-agent`** (HyperFrames: HTML → MP4 / web) o a un HTML con JS propio. Los 12 principios de animación de Disney (anticipación, solapamiento, curvas de aceleración…) son el marco de elección de tiempos y *easings*.

Fuente de inspiración: `pixel2motion` (MIT, Nolan Lai). Sus scripts de animación **no** se incluyeron; si hace falta, clona el repo upstream y úsalo como referencia (ver `CREDITOS.md`).

## 2. Rutas para obtener la forma inicial

| Ruta | Úsala cuando | Qué pasa después |
|---|---|---|
| **Dibujo directo en SVG** (esta skill) | Marcas geométricas y simples: lo normal | Probar y entregar |
| **Vectorizar un original** (`03`) | Hay un raster del logo propio | Escalera + compuerta + verificación |
| **Concepto con IA como imagen** (`freepik-imagegen`, `ckm:design`, `brandkit`) | Explorar direcciones visuales rápido | El raster **no** es entregable: se redibuja o se vectoriza con `03` y pasa todas las pruebas. Revisa créditos antes de generar. No prometas pixel a pixel. |
| **Autovectorizado con servicio** (p. ej. `images_to_svg` / `images_generate_svg` del conector Freepik/Magnific, si la sesión lo tiene) | Conveniencia en siluetas irregulares | **No probado en esta skill.** Su salida es nivel 5 (trazo automático): debe pasar `verificar_vectorizado.py` y suavizarse o reajustarse igual. Revisa créditos y verifica que la herramienta exista antes de prometerla. |
| **Potrace / vtracer / Inkscape** (si están instalados) | Trazo automático local de siluetas | Mismo trato: medida, no arte final |

## 3. Hacia Illustrator, Canva, Figma, web

| Destino | Skill | Insumo desde esta skill |
|---|---|---|
| `.ai`, EPS, PDF editable | `design-illustrator` | SVG maestro limpio (sin texto vivo, sin máscaras ni filtros); avisa que los textos del logo ya son contornos |
| Canva (plantillas, posts, avatar) | `canva-design` | PNG transparente a tamaño suficiente + SVG; *los activos subidos a Canva no admiten SVG en `update_fill`* (límite del conector, ver esa skill) |
| Figma (símbolos, librería, variables de color) | `figma:figma-use` (+ `figma:figma-generate-library` si es una librería) | SVG maestro y variantes; usar estilos/variables existentes, crear solo las que falten con aprobación |
| Sitio web | `direct-visual-design` (método HTML→Figma), `skill-web-astro`, `web-go-high-level-ia` según el caso | `favicon.svg`, `favicon.ico`, set web y `head-snippet.html` de `export_variants.py --web-icons` |
| Sistema de diseño | `design-system-ia` | Tokens de color y reglas de uso del logo |

## 4. Entorno y límites

- **Windows:** usa `python`, no `python3`. Sin `cairosvg` (falta `libcairo`): el render de SVG/HTML se hace con **Chrome headless** (suficiente para todo lo de esta skill). `render_overlay.py` y `render_png.py` necesitan un navegador; exporta `CHROME_BIN` si no lo detectan.
- Dependencias: Pillow y numpy (obligatorias para vectorizar); OpenCV, potrace, vtracer, Inkscape son opcionales y no se usan por defecto.
- La **biblioteca de logos** del repo upstream `logo-design-skill` (1.400+ SVG de marcas reales) **no** se incluyó: son marcas registradas de terceros. Sirve para estudiar construcción y convenciones de una categoría, nunca para copiar. Si la necesitas, clona el repo upstream aparte; `search_library.py` y `preview_sheet.py --refs-industry` dependen de ella.
- El navegador integrado del panel **no** sirve para renderizar archivos locales con estos scripts.
