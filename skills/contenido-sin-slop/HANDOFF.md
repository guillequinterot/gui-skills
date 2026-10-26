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

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Los síntomas de lenguaje en español de `references/02-…` (marcados «candidato») solo pasan a «fuente» cuando haya una fuente verificable o se repitan en varios casos | — | candidata |
| Frases entre comillas no cuentan como síntomas (mención vs uso); umbral de 60 palabras sin anclajes = amarillo | banco-pruebas-semaforo-parrafo | candidata |
