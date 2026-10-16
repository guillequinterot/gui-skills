# 03 · Recetas por consumidor

Cada receta: **pregunta por defecto** (si el consumidor no formula otra), **nivel**, **qué entregar** y **dónde cae**. La skill que llama sigue mandando sobre su propio proceso.

## direct-visual-design (diseño: webs, landings, apps, campañas)
- **Pregunta por defecto:** ¿qué hace bien esta referencia, qué principios de composición/tipografía/color/ritmo/movimiento aplica y qué de eso conviene mantener, adaptar o evitar para **nuestro** brief?
- **Nivel:** N0 si hay imágenes; N1 para webs. N2 solo si el efecto clave (scroll, transición, 3D) no se explica con el DOM.
- **Entrega:** ficha con: estructura de secciones (orden, alto, fondos), escala tipográfica real, paleta funcional (texto/fondo/acento), radios/gaps/sombras, grilla y ancho de contenedor, patrón de componentes, movimiento (librerías + tipo), comportamiento móvil (captura 390), y la tabla **mantener / adaptar / evitar**.
- **Benchmark de varias webs:** una sonda por web + tabla comparativa (secciones, tipografía, densidad, CTA, movimiento, peso, tecnología) + **patrones comunes** y **diferenciadores**; recomendar un camino propio, no un promedio.
- **Lo construye:** `direct-visual-design` (método HTML→Figma 1920/240/80 si aplica, múltiplos de 4). Esta skill no construye.
- Los valores medidos son **aproximaciones**; el diseño final usa la escala y los estilos del proyecto/marca.

## seo-content-system (SEO, AEO, GEO)
- **Pregunta por defecto:** ¿cómo está construida la página que posiciona, qué señales on-page y técnicas muestra, y qué entiende un rastreador **sin JS**?
- **Nivel:** N1 (la sonda ya trae lo necesario). Con Screaming Frog (`screaming-frog-seo`) para rastreo de sitio completo: esa skill hace el crawl; esta solo desmonta una página.
- **Entrega:** title/meta/canonical/hreflang/robots, **outline H1–H3**, tipos de JSON-LD, enlaces internos/externos/nofollow, imágenes (alt, lazy, formatos, sobredimensionadas), **crudo vs renderizado** (¿contenido solo con JS?), peso y terceros, tecnología/CMS, accesibilidad rápida. Etiquetar qué es hecho y qué hipótesis de posicionamiento.
- **Prohibido inferir** causas de ranking como hechos: una correlación con una página no es una regla. Cualquier aprendizaje → `06_Aprendizaje/Inbox/` del vault, no a regla.
- No simular datos de GA4/Search Console/SERP que no estén conectados.

## video-editing-ai-agent (video, motion)
- **El video en sí** lo entiende su propio flujo (`video_understand.py`, `frame_probe.py`, `fetch_reference.py`). No duplicarlo aquí.
- **Aporta esta skill:** webs/apps de referencia cuyo **movimiento** interesa (transiciones, scroll, easings, secuencias, microinteracciones) y herramientas de video/diseño de escritorio o web cuyo comportamiento se quiere entender.
- **Nivel:** N1 (`movimiento` de la sonda: librerías, `@keyframes`, transiciones; capturas) → N2 (`capture_browser_scenario`, `observe_web_execution`) para ver qué se ejecuta.
- **Entrega:** lista de movimientos con duración/easing aproximado (medible en DOM/CSS), orden y disparador; **qué se puede reproducir con HyperFrames/ffmpeg** y qué no. Detalle de doctrina de movimiento: `video-editing-ai-agent/references/motion-doctrine.md`.

## web-go-high-level-ia (AI Studio / «Vibe»)
- Para analizar una web existente del cliente o referencia **antes** de pasar las «partes» al builder: N1, énfasis en estructura de secciones, textos H1/H2 (como hechos, sin reescribir), imágenes y rendimiento.
- Para **auditar la web que ya generó el builder** (qué entiende un rastreador, qué huellas deja): N1 sobre la URL pública de vista previa; `tecnologia` debe mostrar TanStack/Vite.
- No toca ni publica nada en el builder: eso es de esa skill.

## canva-design · design-illustrator
- Referencia de plantilla, manual o pieza ajena: N0 sobre imagen/PDF (`canva-design/scripts/pdf_pages.py` para PDF/`.ai`); N1 si la referencia es una página web.
- Entrega: dimensiones, retícula, jerarquía, tipografías aparentes (sin asumir licencias), paleta. La fuente de marca propietaria se **sustituye y se avisa** (regla de esas skills).

## odoo-* · skill-web-astro · desarrollo de plugins/apps
- **Qué hace esta app/plugin y cómo:** sitio de referencia → N1; app Electron o paquete → N2; APK → N2/N3.
- Entrega: arquitectura observada (módulos, rutas, llamadas de red), comportamiento, dependencias; «cómo lo resolveríamos nosotros» como diseño propio.
- Aplican los límites de [05](05-limites-y-etica.md): interoperabilidad y aprendizaje, no clonación de software protegido.

## Cualquier otra skill o tarea
Misma ficha. Decir en una línea quién pregunta, qué se quiere entender y por qué; elegir el nivel mínimo; entregar resumen + ficha.

## Frases del usuario que activan esta skill directamente
«analiza esta web / app», «cómo hace X», «desmonta», «benchmark de…», «qué tecnología usa», «ingeniería inversa», «entiende esta referencia», «REA».
