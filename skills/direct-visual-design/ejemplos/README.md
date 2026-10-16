# Ejemplos aprobados — ficha (sin capturas)

Dos sitios que el mantenedor y su equipo valoraron como muy logrados (2026-10-09) se renderizaron con Playwright + Google Chrome instalado (headless), viewport **1920 × 1080**, con scroll completo previo para disparar animaciones de entrada y captura de página completa. Las fuentes originales no se modificaron.

| Ejemplo | Qué es | Alto de la captura original |
|---|---|---|
| **A** | Landing agrupadora de servicios B2B para educación superior (HTML autocontenido, export de "Design Component") | 1920 × 10049 |
| **B** | Home de un sitio de marca de producto agroalimentario premium, código `caso-home-01` (Astro, bilingüe ES/EN) | 1920 × 7746 |

**Las capturas no están en este repo.** Contienen marcas, fotos y textos de clientes y terceros (además pesan ~10 MB), así que quedaron fuera por la regla de privacidad de gui-skills (`PRIVACY.md`). Quien las necesite puede regenerarlas con el mismo método sobre sus propios ejemplos:

1. Servir el sitio por HTTP local si usa fuentes o rutas absolutas (abierto como archivo, las rutas absolutas no cargan); un HTML autocontenido renderiza igual por `file://`.
2. Playwright + Chrome headless a 1920 × 1080, hacer scroll completo para disparar las animaciones, medir valores **computados** con JavaScript y capturar la página completa.
3. Guardar capturas y medidas **fuera del repo** (carpeta del proyecto del usuario) y dejar aquí solo el análisis anonimizado.

Análisis medido: `../conocimiento/02-analisis-ejemplos.md`. Patrones destilados: `../references/web-patterns-from-examples.md`.
