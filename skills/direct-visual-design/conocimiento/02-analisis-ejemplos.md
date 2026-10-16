# Análisis de los ejemplos aprobados (valores medidos)

- **Fecha:** 2026-10-09
- **Contexto:** el usuario dijo "nos gustó mucho cómo quedaron". Se estudian para extraer patrones transferibles, no para copiarlos.
- **Método de medición:** lectura completa del CSS/marcado (data URIs recortados con Python) + render con Playwright y Chrome instalado a **1920 × 1080**, scroll completo para disparar animaciones de entrada, medición de valores **computados** con JavaScript y captura de página completa. El ejemplo B se sirvió desde su `dist/` con un servidor estático local (127.0.0.1, solo lectura) y se apagó al terminar.
- **Capturas:** no están en el repo por privacidad (ver `ejemplos/README.md`).
- **Destilado reutilizable:** `references/web-patterns-from-examples.md`.

---

## Ejemplo A — Landing agrupadora de servicios (Los Creativos · educación superior)

**Origen:** HTML de referencia aportado en la carpeta del proyecto `caso-landing-industrial-01` (solo lectura; el archivo no se sube al repo).
**Formato:** export de "Design Component" (runtime React incrustado + bloque `<x-dc>` con plantillas `sc-for`/`sc-if`). 8,6 MB; 51 data URIs (10 pesos de Satoshi OTF en base64 + fotos). Sin el base64 el HTML pesa 315 KB.

### Estructura (13 bloques, alto total 10.049 px a 1920)

| # | Sección | y | alto | padding vert. | fondo |
|---|---|---|---|---|---|
| 1 | Header + hero (bloque rojo redondeado con "notch" blanco para el logo) | 0 | 624 | 14 / 0 | blanco + bloque `#FF2D46` |
| 2 | Por qué educación: texto + 4 stat tiles (gauges y barras SVG) | 624 | 1005 | 72 / 72 | blanco |
| 3 | Diferenciador: carrusel de metodologías (panel + bento de medios) | 1629 | 877 | 72 / 0 | blanco |
| 4 | Casos de éxito: pestañas pill + card split 0.82fr / 1.18fr | 2506 | 1043 | 76 / 76 | `#F9FAFB` |
| 5 | Recursos descargables: grid 2 col de cards con efecto linterna | 3549 | 1022 | 76 / 76 | blanco |
| 6 | Newsletter: card blanca con panel rojo + lista 2 col | 4570 | 569 | 76 / 76 | `#FFDFE6` |
| 7 | Expertos: carrusel horizontal de cards 300 × 470 | 5140 | 779 | 76 / 76 | `#0B1628` |
| 8 | A quién ayudamos: acordeón con miniaturas + chips | 5919 | 1472 | 76 / 76 | blanco |
| 9 | Videos: grid 4 col, portada 16:9 con botón play | 7391 | 822 | 76 / 76 | `#F9FAFB` |
| 10 | FAQ: pestañas pill + acordeón dentro de card | 8213 | 729 | 76 / 76 | blanco |
| 11 | CTA final: banda con imagen y velo degradado | 8941 | 470 | 104 / 104 | `#F9FAFB` + imagen |
| 12 | Ciudades: grid 4 col de cards | 9411 | 557 | 76 / 76 | blanco |
| 13 | Footer mínimo | 9968 | 81 | 32 / 32 | `#0B1628` |

### Retícula

- `.wrap { max-width:1160px; padding:0 40px }` → caja en x = 380, **texto en x = 420**, ancho útil 1080 px a 1920.
- Hero: margen exterior 14 px, radio 32 px; gutter interno calculado `max(28px, (100% − 1052px)/2 − 14px)`.

### Tipografía (computada)

| Rol | Valor |
|---|---|
| Familia | Satoshi (única), pesos 300–900 |
| H1 | 3.4rem = **54.4 px**, 800, lh 1.08, tracking −0.01em, `text-wrap:balance` |
| H2 | 1.9rem = **30.4 px**, 800, lh 1.2 (variantes 2.1–2.15rem) |
| H3 | 1.5–1.55rem ≈ 24.8 px, 800, lh 1.3 |
| Cuerpo | 15.5 px lh 1.75 (sección), 14.5 px lh 1.7 (cards), 18 px en hero |
| Eyebrow | 12.5 px, 700, mayúsculas, tracking 0.12em, rojo |
| Botón | 14.5 px, 700 |

### Color

`--red #FF2D46` (acción/acento), `--red-dark #E0233A` (hover), `--navy #1E2939` (titulares), `--night #0B1628` (secciones oscuras/footer), `--ink #363636` (cuerpo), `--muted #6A7282`, `--line #E7E9EC`, `--mist #F9FAFB`, rojo suave `rgba(255,45,70,.08/.14)`, banda rosa `#FFDFE6`.

### Superficies

- Radios (conteo computado): 50 % ×33, 999px ×25, 16px ×20, 10px ×14, 18px ×13, 14px ×12, 20px ×11, 12/24/11/9/32 px — **12 radios distintos**.
- Sombras: prácticamente ninguna (solo el botón play: `0 6px 18px rgba(11,22,40,.28)`). Profundidad por color y borde 1 px `#E7E9EC`.

### CTA e interacción

- Primario pill rojo (radio 24, padding 14/26) + secundario outline navy 1.5 px; en hero se invierten (blanco + ghost blanco).
- Hover: `translateY(-1px)`, transiciones 0.15 s; carrusel 0.55 s `cubic-bezier(.65,.05,.36,1)`; zoom 1.04 en portadas de video; "linterna" con gradiente radial que sigue el cursor (`--mx/--my`) en cards de recursos.
- Móvil: reglas dedicadas (lateral único 20 px, verticales 40/32/24, textos que nunca bajan de tamaño, objetivos táctiles 48 px).

### Medición "listo para Figma" (validador)

- Estático: **128 de 355** declaraciones de espaciado no son múltiplo de 4 (más frecuentes 14, 10, 22, 18, 26 px).
- Render: **437 de 835** valores computados (52 %) fuera de múltiplos de 4; 16 contenedores con overflow hidden (cards, fotos, hero, carruseles).
- Secciones a 72/76/104 px, no 80. Contenido en x = 420, no 240.

### Lectura profesional

**Funciona:** un solo acento con disciplina; jerarquía por peso 800 con una sola familia; secuencia de prueba (datos → método → casos → recursos → equipo → FAQ) antes del CTA; datos visualizados; fondos alternos que dan ritmo sin divisores; módulos variados con un lenguaje común (eyebrow → H2 → contenido); densidad alta pero escaneable.
**No heredar:** estilos inline y overrides de móvil por selector de atributo con `!important`; rem fraccionarios; espaciados fuera de 4; contenedor 1160; demasiados radios; `div` clicables sin rol; fuentes en base64.

---

## Ejemplo B — Sitio `caso-home-01` (grupo agroalimentario, producto premium)

**Origen:** proyecto Astro del cliente (`caso-grupo-agro-01`; bilingüe ES/EN; solo lectura; no se sube al repo). Fuente de verdad visual: `src/styles/tokens.css` ("único archivo con valores crudos") + `global.css` + componentes `.astro`.

### Estructura del Home (alto total 7.746 px a 1920)

| # | Sección | y | alto | padding vert. | fondo |
|---|---|---|---|---|---|
| 0 | Header sticky 80 px (logo, nav, idioma, CTA pill) | 0 | 81 | 0 | crema `#FFF3C7` |
| 1 | Hero overlay: foto a sangre, velo degradado azul, titular abajo-izq., borde inferior curvo (máscara radial) | 81 | 1000 | 0 (texto 80) | azul `#002D74` + foto |
| 2 | Cifras: foto 50 % + panel con filas valor/etiqueta y hairlines | 1001 | 861 | 0 (panel 120+curva) | crema / amarillo 12 % |
| 3 | Producto: banda de foto cobalto a sangre, texto a la izquierda | 1862 | 1080 | 0 (contenido 80) | `#0156BF` |
| 4 | Cadena "del campo al puerto": carrusel de 5 cards 380 × 500 con stickers y línea que se dibuja | 2942 | 1081 | 80 / 80 | amarillo 24 % |
| 5 | Audiencias: 2 paneles con foto 3:2 (radio 24) + texto + CTA | 4023 | 1082 | 120 / 120 | crema |
| 6 | Blog: encabezado con CTA a la derecha + 3 cards | 5105 | 1021 | 120 / 120 | amarillo 12 % |
| 7 | FAQ: título cols 1–4, acordeón cols 6–12 + enlaces relacionados | 6125 | 680 | 80 / 80 | crema |
| 8 | Footer: frase grande, 3 columnas, franja ilustrada, legal | 6805 | 941 | 96 / 48 | azul `#002D74` |

### Retícula y espaciado (tokens)

- `--layout-container:1440px` con gutter 64 → a 1920 la caja empieza en **x = 240** (coincide con el método) pero el texto queda en **x = 304** por el padding interno.
- Escala `--space-*`: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 120 — **todo múltiplo de 4**.
- Ritmo de sección: desktop 120 (normal) / 80 (tight); tablet 80/64; móvil 40/32.
- Validador estático: **0 errores en 551** declaraciones (129 variables resueltas). Render: 16 valores fuera de 4, todos del **padding por defecto del navegador en `<button>`** (1 px / 6 px) en flechas de carrusel y disparadores del FAQ.
- Desalineación detectada: encabezado del carrusel de la cadena en **x = 160** (`--scale-start:160px` fijo) frente a x = 304 del resto.

### Tipografía (tokens; desktop)

| Rol | Valor |
|---|---|
| Titulares | Fraunces 500 (serif), tracking negativo |
| Display / H1 / H2 / H3 / H4 | 112 / 80 / 56 / 32 / 24 px; lh 1 / 1.04 / 1.08 / 1.2 / 1.3; tracking −0.03 / −0.03 / −0.02 / −0.01em |
| Cifras | 96 px (70 px en el módulo de cifras, excepción autorizada) |
| Cuerpo | DM Sans 18 px lh 1.6; cuerpo grande 22 px lh 1.5; small 16; caption/kicker 14 (500) |
| Medida | máx. 64ch |
| Fluidez | `clamp()` entre 768 y 1200 con pendiente documentada; fijo en móvil y en desktop |

### Color (tokens)

Primario UI amarillo `#FFD400` (+ 64/40/24/12 %), azul `#002D74` texto y secundario (+ 80/64/40/24/16 %, con nota de cuál pasa AA: azul 80 % = 6,8:1 sobre crema; 64 % solo deshabilitado), crema `#FFF3C7` fondo base, azul foto `#0156BF` solo en la banda de producto (excepción), amarillo Pantone del logo `#F3E85C` prohibido en UI.

### Superficies

- Radios: escala 4/8/12/16/24/32; computados 32 px ×16 (pills), 24 px ×5 (imágenes), 12 px ×5 (cards de carrusel), 8 px ×1. **Cero sombras.**
- Hairlines 1 px azul 16 % en filas de cifras, FAQ y footer.

### CTA e interacción

- Botón pill: altura 48 (compacto) / 56 (grande), padding 24 / 32, 16 px 500, flecha que se desplaza 4 px en hover; variantes por contexto (crema, azul, foto) con hover de alto contraste, `focus-visible` 2 px offset 4, active `scale(.98)`, estados deshabilitados.
- Header: subrayado amarillo que crece con `scaleX`; borde inferior aparece al hacer scroll; menú móvil con entrada escalonada (40 ms).
- Secciones: revelado fade + translateY 24 px, 400 ms `cubic-bezier(.22,1,.36,1)`, escalonado 80–90 ms; línea de la cadena que se dibuja (600 ms); acordeón con `grid-template-rows`. Todo con `prefers-reduced-motion`.
- Overflow hidden en hero (máscara curva), producto (foto), carrusel y franja del footer: **casos justificados** (máscara, sangrado, carrusel).

### Lectura profesional

**Funciona:** sistema de tokens único y auditable; serif editorial + sans neutra con contraste de escala fuerte; fotografía protagonista con velos planos y medidos; paleta corta con roles claros; estados y accesibilidad trabajados; excepciones documentadas con su motivo; carruseles y bandas a sangre que rompen la monotonía sin romper la retícula.
**Ajustar al método:** secciones a 120 (método: 80); texto en x = 304 (método: 240); bloque desalineado a x = 160; reset de padding de `button`.

---

## Comparación con el método HTML→Figma

| Criterio del método | A (landing) | B (caso-home-01) |
|---|---|---|
| 1920 × Hug, sin scroll horizontal | Sí (scrollWidth 1920) | Sí (scrollWidth 1920) |
| Contenido en x = 240 | No (420) | Caja sí (240), texto no (304) |
| 80 / 80 por sección | No (72/76/104) | Parcial (80 en 2 secciones; 120 en otras) |
| Múltiplos de 4 | No (52 % fuera) | Sí (salvo reset de botón) |
| Fill / Hug, sin alturas fijas | Parcial (cards con alto fijo 470) | Parcial (cards 380 × 500, hero min-height) |
| Sin clip innecesario | No (16 contenedores) | Sí (5, justificados) |
| Estilos como tokens mapeables | No (inline) | Sí (`tokens.css`) |

Conclusión: **A aporta el lenguaje visual y la secuencia persuasiva; B aporta la disciplina de sistema.** El método pide combinar ambos: la riqueza modular de A construida con el rigor de tokens de B, ajustada a 240/80.
