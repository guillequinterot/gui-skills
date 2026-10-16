# Patrones web destilados de ejemplos aprobados

Patrones **transferibles** extraídos de dos sitios que Guille y su equipo valoraron como muy logrados (2026-10-09). Son heurísticas profesionales con evidencia propia, no reglas absolutas ni plantillas para copiar: no reutilizar marcas, textos, fotos ni paletas de los ejemplos. El análisis con valores medidos está en `conocimiento/02-analisis-ejemplos.md` y las capturas en `ejemplos/`.

- **Ejemplo A** — Landing agrupadora de servicios B2B (educación). Densa en pruebas, una familia tipográfica, un acento.
- **Ejemplo B** — Sitio de marca de producto agrícola premium (Astro). Sistema de tokens estricto, serif editorial + sans, fotografía protagonista.

Siempre que un patrón choque con el método HTML→Figma (`html-to-figma-method.md`), gana el método: p. ej. ambos ejemplos usan ritmos verticales 72/76/120 y el método exige 80.

## Contenido

1. Lo que los hace buenos
2. Estructura de página
3. Ritmo y espaciado
4. Tipografía
5. Color
6. Cards, bordes, radios y sombras
7. CTAs
8. Componentes recurrentes
9. Movimiento e interacción
10. Errores que no hay que heredar

## 1. Lo que los hace buenos (criterio profesional)

- **Un acento, usado con disciplina.** A: rojo solo en CTA, eyebrows, cifras y bloques de énfasis; el resto blanco, gris niebla y azul noche. B: amarillo como único color de acción sobre crema/azul.
- **Jerarquía por contraste de peso/familia, no por cantidad de estilos.** A: una sans en 800 para titulares y 400 para cuerpo. B: serif media en titulares grandes con tracking negativo + sans neutra en cuerpo.
- **Prueba antes de la petición.** Datos, casos, equipo, recursos y FAQ preceden al CTA final; el CTA se repite en hero, módulos y cierre.
- **Ritmo de fondos alternos** (blanco → niebla → banda de color → oscuro) que separa secciones sin divisores.
- **Variedad de módulos con un sistema común** (eyebrow → H2 → bajada → contenido): cada sección cambia de forma pero no de lenguaje.
- **Datos visualizados** (gauges, barras, cifras gigantes) en vez de párrafos con números.
- **Accesibilidad trabajada (B):** estados hover/focus/disabled/active, contraste AA documentado por token, `prefers-reduced-motion`.
- **Decisiones documentadas (B):** cada excepción marcada como "excepción autorizada" con su motivo.

## 2. Estructura de página (secuencia que funcionó)

Landing agrupadora (A): hero con propuesta + 2 CTA → "por qué" con estadísticas → diferenciador/metodología (carrusel) → casos con pestañas → recursos descargables → newsletter/contenido → equipo (carrusel) → a quién ayudamos (acordeón + chips) → videos → FAQ con pestañas → CTA final con imagen → cobertura geográfica → footer.

Home de marca (B): hero foto a sangre con titular abajo-izquierda → cifras (foto + panel de filas) → producto (banda de color a sangre) → cadena/proceso (carrusel de etapas) → audiencias (2 caminos con foto) → blog (3 cards) → FAQ (título 4 col + acordeón 7 col) → footer con frase grande.

Patrón común: **hero → prueba cuantitativa → diferenciador → prueba cualitativa → caminos/CTA → contenido → FAQ → cierre**.

## 3. Ritmo y espaciado

- Encabezado de sección como bloque: eyebrow (12–14 px) → 8–16 → H2 → 16–24 → bajada → 32–64 → contenido.
- Separación título→contenido mayor que la interna del título (B usa 40–64; A usa 32).
- Grids de cards con gap 16–24; columnas con gap 64 (gutter) en layouts editoriales.
- Traducción al método: usar 8/16/24/32/40 dentro de secciones y **80** entre secciones; 120 solo como espacio interno excepcional aprobado.

## 4. Tipografía

- 2 niveles fuertes de display (H1 ~54–80 px, H2 ~30–56 px) y un cuerpo cómodo (18 px, interlineado 1.6; medida ≤ 64ch).
- Tracking negativo en titulares grandes (−0.01 a −0.03 em); positivo y mayúsculas en eyebrows (+0.08 a +0.12 em).
- Cifras como protagonistas: tamaño display, unidad o etiqueta pequeña al lado/abajo.
- `text-wrap: balance` en titulares para evitar viudas.
- Para Figma: tamaños en px enteros y line-height explícito.

## 5. Color

- Estructura de roles: **fondo base**, **superficie alterna** (niebla/crema), **texto principal oscuro** (no negro puro), **texto secundario** (gris o alfa del texto), **acento de acción**, **oscuro de contraste** para secciones de autoridad.
- Escalones de opacidad del acento y del texto (12/24/40/64/80 %) para fondos suaves, divisores y estados — documentando cuáles pasan AA como texto.
- Velo de color plano o degradado direccional sobre fotos para legibilidad, nunca oscurecer toda la imagen sin necesidad.

## 6. Cards, bordes, radios y sombras

- **Sin sombras** (o casi): ambos ejemplos son planos; la profundidad sale de color de superficie y borde 1 px.
- Radios: pill para botones/tabs/chips; 16–24 para cards e imágenes; 32 para bloques grandes (hero). Mantener una escala corta (B: 4/8/12/16/24/32). A usa 12 radios distintos: evitarlo.
- Divisores hairline (1 px, texto al 16 % o gris línea) en listas, filas de cifras y acordeones.
- Cards de recurso: miniatura + título + pie con formato y flecha circular.

## 7. CTAs

- Primario pill de alto contraste + secundario outline del mismo tamaño, lado a lado (gap 12–16); en móvil, apilados a ancho completo.
- Flecha (→) que se desplaza 2–4 px en hover; cambio de color de fondo con contraste ≥ 4.5:1; `focus-visible` con outline 2 px y offset 4.
- Variantes por contexto (sobre claro, sobre oscuro, sobre foto) definidas, no improvisadas.
- CTA en header (pill) + hero + módulos + cierre.

## 8. Componentes recurrentes

- **Eyebrow/kicker** antes de cada H2.
- **Stat tile / fila de cifra** (valor grande + etiqueta + fuente).
- **Carrusel** con flechas circulares 40–48 px y puntos; tarjetas de ancho fijo con scroll-snap (único lugar donde se acepta clip).
- **Pestañas pill** que filtran casos o FAQ.
- **Acordeón** con +/− y animación de altura (`grid-template-rows: 0fr → 1fr`).
- **Split media/texto** (0.82fr/1.18fr o 50/50) para casos y cifras.
- **Banda CTA** con imagen a un lado y velo degradado hacia el texto.
- **Header** sticky con borde que aparece al hacer scroll; subrayado animado en el enlace activo.
- **Footer** oscuro con frase de marca grande, columnas y franja ilustrada.

## 9. Movimiento e interacción

- Revelado al entrar en viewport: opacidad 0→1 + translateY 16–24 px, 400 ms, `cubic-bezier(.22,1,.36,1)`, escalonado 40–90 ms entre hijos.
- Hovers rápidos (150–200 ms): cambio de color, translateY(−1 px), zoom de imagen 1.04 en cards de video.
- Efecto "linterna" (gradiente radial que sigue al cursor) en cards: recurso de web, **no representable en Figma** → documentarlo como interacción.
- Siempre `prefers-reduced-motion: reduce`.

## 10. Errores que no hay que heredar

- Estilos inline + overrides por selector de atributo con `!important` para móvil (A): imposible de mapear a estilos de Figma.
- rem fraccionarios y espaciados fuera de múltiplos de 4 (A: 52 % de los valores computados).
- Contenedor de 1160 px (A) o de 1440 con padding interno (B → texto en x = 304) en vez de contenido en x = 240.
- Un bloque desalineado con el resto (B: encabezado de carrusel en x = 160).
- Botón sin reset de padding del navegador (B: 1 px / 6 px heredados).
- Elementos clicables como `div` sin rol de botón/enlace (A).
- Fuentes incrustadas en base64 que llevan el HTML a 8,6 MB (A).
