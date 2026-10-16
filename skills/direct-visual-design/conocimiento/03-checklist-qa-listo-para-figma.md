# Checklist QA "listo para Figma"

Usar antes de pedir la aprobación del HTML y otra vez antes de construir en Figma. Marcar cada punto; si alguno falla, corregir o documentar la excepción aprobada.

## A. Proceso

- [ ] Se leyó el Figma del proyecto (Styles, Variables, componentes) antes de diseñar.
- [ ] Todo color, fuente, tamaño, radio y efecto usado existe en ese Figma, o se preguntó y quedó aprobado.
- [ ] El HTML fue **aprobado por el usuario** antes de pasar a Figma.

## B. Lienzo y retícula

- [ ] Ancho de diseño 1920 px; alto Hug (sin `height` fija en la página).
- [ ] Sin scroll horizontal a 1920 (`scrollWidth == 1920`).
- [ ] Contenido de cada sección empieza en **x = 240** y termina en x = 1680 (ancho útil 1440).
- [ ] Fondos a sangre solo como fondo; el contenido respeta los 240.

## C. Espaciado

- [ ] Cada sección de contenido: **80 px arriba y 80 px abajo**.
- [ ] Menú/header, hero y footer: exentos del 80/80, pero todos sus paddings/gaps/margins en múltiplos de 4.
- [ ] Todos los padding, gap y margin son **múltiplos de 4** (escala 8, 16, 24, 32, 40, 80, 120).
- [ ] Sin `rem` fraccionarios; tipografía y line-height en px enteros.
- [ ] `button` con padding reseteado (el navegador añade 1 px / 6 px).

## D. Estructura Auto Layout

- [ ] Cada sección es un contenedor flex/grid que equivale a un frame **Fill × Hug**.
- [ ] Separaciones con `gap` / `padding` del padre, no con `margin` de los hijos.
- [ ] Jerarquía de anidación = jerarquía de frames prevista (sección → contenedor → grupo → elemento).
- [ ] Sin alturas fijas salvo medios con proporción (`aspect-ratio`) o carruseles.
- [ ] `position:absolute` solo para decoraciones/insignias (en Figma: "absolute position").
- [ ] Clases semánticas para nombrar capas.

## E. Clip y desbordes

- [ ] `overflow:hidden`/`clip` solo en carruseles, máscaras de imagen o sangrados realmente necesarios, y cada uno justificado.

## F. Estilos y componentes

- [ ] Un solo bloque/archivo de tokens; nombres que mapean 1:1 con los estilos/variables de Figma.
- [ ] Sin hex ni tamaños sueltos en componentes.
- [ ] Header/menú, footer, botones y demás componentes existentes replicados fielmente (medidas, estados) para usarlos como instancias.
- [ ] Interacciones no representables en Figma marcadas como "solo web".

## G. Imágenes

- [ ] Imágenes exportadas del Figma cuando provienen de allí; nombres descriptivos; sin base64 innecesario.
- [ ] `object-fit` / `object-position` anotados para replicar el recorte en Figma (Fill/Crop).
- [ ] Herramienta para colocar imágenes en Figma verificada en la sesión (o limitación declarada).

## H. Calidad base (skill)

- [ ] Contraste AA del texto, `focus-visible`, estados hover/active/disabled.
- [ ] `prefers-reduced-motion` respetado.
- [ ] Elementos clicables como `<a>` o `<button>`.

## Validación automática

```text
python -I "<repo>/skills/direct-visual-design/scripts/validate_figma_ready.py" pagina.html
python -I "<repo>/skills/direct-visual-design/scripts/validate_figma_ready.py" pagina.html --render
python -I "<repo>/skills/direct-visual-design/scripts/validate_figma_ready.py" tokens.css componentes/ 
```

- Modo estático (solo librería estándar): múltiplos de 4 en `<style>`, `style=""` y `.css`/`.astro`/`.vue`; resuelve `var()`; marca `calc/clamp/em/%` para revisar a mano; lista overflow hidden/clip.
- Modo `--render` (Playwright + Chrome): valores computados a 1920, padding vertical de cada sección de contenido (esperado 80; header/nav/menú, hero y footer marcados "exento 80/80"), x del contenido (esperado 240), scroll horizontal y contenedores con clip. Los múltiplos de 4 se exigen en todo, incluidos los exentos.
- Código de salida 1 si hay errores de múltiplos de 4 (o scroll horizontal en render); los avisos de 80/240/clip no cambian el código: se revisan con criterio.
- Probado el 2026-10-09 con los dos ejemplos de `ejemplos/` (resultados en `02-analisis-ejemplos.md`).
