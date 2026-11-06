# HANDOFF — contenido-sin-slop

> Traspaso entre sesiones y personas: qué es la skill, cómo se instala, qué se decidió y qué se aprendió
> en cada trabajo. Estado vivo (versión, herramientas, pendientes) → `HANDSHAKE.md`.

## 1. Qué es y cuándo se usa

Puerta de calidad contra el **slop** (contenido de baja calidad hecho con IA, en cantidad y sin revisión). Se usa antes de
publicar o entregar texto, imágenes, video, carruseles o PDFs hechos o asistidos con IA, y en cualquier flujo de
publicación automática. Es transversal: la llaman `seo-content-system`, `direct-visual-design`, `canva-design`,
`video-editing-ai-agent` y `video-aprender`.

## 2. Instalación y dependencias

- Viene con el repo gui-skills (`tools/install.ps1` / `tools/install.sh`); no se copia a mano.
- Dependencias externas: ninguna (el detector usa solo la biblioteca estándar de Python 3).

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-10-26 | La skill evalúa **valor para el lector y procedencia**, no apariencia; los patrones de lenguaje son síntomas y el detector es solo ayuda | el mantenedor (pidió la skill tras investigar el tema) | Las políticas de Google y YouTube hablan de propósito y valor, no de método; la guía de Wikipedia advierte que los síntomas no prueban nada y que corregir solo la superficie oculta el problema |
| 2026-10-26 | Nada de «humanizadores», errores a propósito, cuotas de palabras ni porcentajes de detectores | el mantenedor | Es slop de otro tipo y empeora el texto; coincide con la regla de `seo-content-system` contra la ingeniería lingüística forzada |

| 2026-10-26 | Se añade un **semáforo por párrafo** (modo revisión) con cinco preguntas y reglas por tipo de párrafo; el detector da la luz provisional y quien revisa fija la final | el mantenedor (lo pidió, aportó las fuentes) | Las ocho fuentes coinciden en que el slop es falta de novedad, especificidad, respaldo y voz propia, no una apariencia; un criterio por párrafo permite decir qué falta en cada uno |
| 2026-10-26 | Se rechaza el consejo de reescribir un blog ajeno con IA «para que se parezca menos al original» (video de YouTube, fuente 6): se marca rojo (spinning) | el mantenedor (pidió analizar las fuentes; decisión tomada al diseñar la rúbrica, pendiente de su visto bueno final) | Es contenido ajeno disimulado, sin nada propio |

## 4. Registro de trabajos

> Una entrada por trabajo terminado o implementado y aprobado. Solo se agregan entradas al final; las
> correcciones van como entrada nueva. Casos solo con código `caso-<tipo>-<NN>`. Formato:
> `templates/entrada-de-trabajo.md`. Se escribe con `tools/log_job.py`.

<!-- registro:inicio -->

### 2026-10-26 · banco-pruebas-semaforo-parrafo · guille

- **Qué se hizo:** Se añadió un semáforo por párrafo (rojo/amarillo/verde) con cinco preguntas (novedad, especificidad, respaldo, lo propio, función) sacadas de ocho fuentes (siete páginas y un video); rúbrica en references/06, opción --semaforo en slop_lint.py y 12 pruebas nuevas
- **Salió bien:** El detector dio luz provisional útil en dos artículos reales en español; corregidos mención vs uso (frases entre comillas), menús y pies de página en HTML; 38 pruebas en verde
- **Salió mal / incidencia:** Las fuentes son blogs y glosarios casi todos de vendors: los umbrales numéricos son iniciales; quedan falsos amarillos (definiciones largas sin cifras) y falsos verdes (párrafo vacío sin síntomas) Incidencia: El punto 9 de la lista de fuentes llegó vacío; el video recomienda reescribir blogs ajenos con IA (spinning), se rechazó y se marca rojo
- **Regla candidata:** Frases entre comillas no cuentan como síntomas (mención vs uso); umbral de 60 palabras sin anclajes = amarillo
- **Herramientas:** slop_lint.py --semaforo, WebFetch, yt-dlp (subtítulos)

### 2026-10-30 · banco-pruebas-seo-skills-terceros · guille

- **Qué se hizo:** Anadida la referencia 07: puntaje 1 a 100 por bloque, excepciones SEO, dieciseis familias de senales, cinco dimensiones y salida JSON, desde la skill no-slop de seo-skills.com
- **Salió bien:** Complementa el semaforo sin sustituirlo; resuelve que repetir la keyword en titulos, FAQ e introduccion no es relleno; las 38 pruebas existentes siguen en verde
- **Salió mal / incidencia:** La equivalencia puntaje-semaforo y los puntos de corte son propuestas sin probar; slop_lint.py no detecta aun las familias nuevas
- **Regla candidata:** Repetir la keyword en titulos, encabezados, introduccion y FAQ no es slop; el relleno de keywords dentro de una oracion si
- **Herramientas:** no indicadas

### 2026-11-06 · caso-migracion-01 · guille

- **Qué se hizo:** Revisión del contenido publicado de un sitio YMYL de trading: detector con semáforo sobre las 35 entradas y lectura humana de una muestra con las cinco preguntas, cruzada con repeticiones literales de párrafos entre artículos y con las fuentes externas enlazadas.
- **Salió bien:** El cruce entre piezas encontró lo que el detector no ve: 8 artículos con el mismo aviso final y 8 con la misma referencia, y una fuente oficial enlazada en 25 sitios que ya daba 404.
- **Salió mal / incidencia:** El detector dio 34 de 35 documentos en verde (0 párrafos rojos) para una serie de artículos que falla en novedad y en lo propio: sus ejemplos son ficticios y no nombran a la marca. Un semáforo en verde no equivale a pasar la puerta. Incidencia: nada relevante
- **Regla candidata:** El detector solo ve síntomas dentro de un texto: añadir al informe un chequeo de párrafos repetidos entre piezas, de menciones de la marca y de enlaces externos rotos antes de dar un verde.
- **Herramientas:** slop_lint.py --semaforo, Python (comparación de fragmentos de 8 palabras)

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Los síntomas de lenguaje en español de `references/02-…` (marcados «candidato») solo pasan a «fuente» cuando haya una fuente verificable o se repitan en varios casos | — | candidata |
| Frases entre comillas no cuentan como síntomas (mención vs uso); umbral de 60 palabras sin anclajes = amarillo | banco-pruebas-semaforo-parrafo | candidata |
| Repetir la keyword en titulos, encabezados, introduccion y FAQ no es slop; el relleno de keywords dentro de una oracion si | banco-pruebas-seo-skills-terceros | candidata |
| El detector solo ve síntomas dentro de un texto: añadir al informe un chequeo de párrafos repetidos entre piezas, de menciones de la marca y de enlaces externos rotos antes de dar un verde. | caso-migracion-01 | candidata |
