# 02 · Escalera de profundidad y sondas

Regla: **el nivel más bajo que responda la pregunta**. Subir se justifica por escrito («el DOM no explica cómo se anima X»).

## N0 · Mirar
- Imagen/captura: `Read` sobre el PNG. Describir composición, jerarquía, tipografía, color, ritmo.
- Página abierta: navegador integrado del panel (`mcp__Claude_Browser__*`) o `WebFetch` para texto. **El navegador del panel no sirve para archivos locales** (abre una instantánea `data:` sin imágenes ni fuentes): para HTML local usar Chrome headless.
- Bloqueado/login: **no insistir**. Pedir al usuario captura o acceso propio.

## N1 · Sonda web propia (`scripts/web_probe.py`)
```powershell
python -I "<repo>/skills/rea-reverse-engineer/scripts/web_probe.py" https://ejemplo.com --out <carpeta-del-proyecto>/referencias/ejemplo-2026-10-15 --widths 1440,390 --scroll
```
Requiere Python con Playwright y Chrome o Edge (verificado solo en el Windows del mantenedor: Playwright 1.59, Chrome y Edge presentes). Entrega: `probe.md` (resumen), `probe.json` (todo), `rendered.html` (DOM final), `shot-<ancho>.png`.

Qué mide: título/meta/canonical/hreflang/JSON-LD, titulares, enlaces, imágenes (alt, lazy, formatos, sobredimensionadas), **escala tipográfica real**, fuentes cargadas, colores y fondos más usados, radios, gaps, sombras, variables CSS de `:root`, `@keyframes`, librerías de movimiento (GSAP, Lenis, AOS, Swiper, Lottie…), sticky/scroll-snap/backdrop-filter, secciones con alto y fondo, huellas de tecnología, peticiones por tipo y **terceros**, errores de consola, accesibilidad rápida y **HTML crudo vs renderizado** (¿depende de JS el contenido?).

Cómo usarla bien:
1. Leer `probe.md`, luego **mirar `shot-1440.png` y `shot-390.png`**.
2. `--scroll` si hay carga diferida; `--wait 3000` si hay intro o animación inicial.
3. Una URL por llamada. Para un benchmark de varias referencias, una carpeta por referencia y una **tabla comparativa** en la ficha (no ocho fichas sueltas).
4. Si `hojasCss.inaccesibles > 0`, hojas de otro origen: las variables CSS no se leen (inferir de computados).
5. Interacciones (hover, menú, modal, carrusel): la sonda no las prueba. Con el navegador del panel o Chrome in-browser: hacer la acción y capturar, o N2 (`capture_browser_scenario`).

Límites honestos: estado inicial sin sesión; un solo viewport por captura; tokens = valores computados, no el sistema original; huellas = indicios.

### Capturas a escala de diseño
Para comparar con un diseño propio a 1920 (método HTML→Figma): `--widths 1920,1440,390`.

## N2 · REA ligero (cuando el DOM no basta)

Necesita REA conectado (ver [04](04-rea-upstream.md)). Preguntas típicas y herramienta:

| Pregunta | Herramienta REA |
|---|---|
| ¿Qué scripts, módulos, rutas e imports tiene la app web? | `export_web_scripts` → `analyze_javascript_application` |
| ¿Qué pide la página, a qué APIs llama, qué ejecuta? | `inspect_web_page`, `observe_web_session`, `inspect_web_network_capture` (HAR/SAZ), vista `api-surface` |
| ¿Cómo se logra esta interacción/animación? | `capture_browser_scenario` (acciones declaradas), `inspect_web_event_listeners`, `observe_web_execution` (cobertura) |
| ¿Qué cambió entre dos versiones/capturas? | `compare_web_captures`, `compare_artifacts` |
| App Electron (p. ej. editor de escritorio) | `analyze_javascript_application` sobre ASAR/carpeta, `list_electron_targets`, `inspect_electron_fuses` |
| Plugin/extensión empaquetada | `open_binary` / `inspect_artifact` sobre el paquete |

Reglas N2: observación **pasiva** por defecto; `capture_browser_scenario` **ejecuta acciones** sobre la página (decirlo: «REA realizó estas acciones»); conectar solo a páginas/instancias del usuario o públicas; no usar sesiones con datos personales; las capturas omiten valores de cabeceras de credenciales y cuerpos privados.

Resultados grandes: pedir `detail: "summary"` y paginar con `inspect_analysis_view`; no volcar todo al chat.

## N3 · REA nativo
Solo con pregunta que lo justifique y motor disponible (Ghidra/IDA/Hopper, JADX+JDK…). Para diseño/SEO/video casi nunca. Ver [04](04-rea-upstream.md). Pedir confirmación antes de instalar motores externos: REA no los instala.

## Cuándo NO subir
- La ficha ya responde la pregunta del consumidor.
- Subir exigiría saltar un login, un CAPTCHA o un bloqueo (prohibido).
- El objetivo es copiar activos o código propietario (no es entender; ver [05](05-limites-y-etica.md)).
