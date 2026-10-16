# Brief para subagente de animación (uno por animación, en paralelo)

Cada subagente NO tiene el contexto del padre: el prompt debe ser autocontenido. Un subagente = un archivo (nombres únicos para que no se pisen). Adaptado de browser-use/video-use (MIT).

Incluir siempre:
1. **Objetivo en una frase**: "Construye UNA animación: [especificación]. Nada más."
2. **Ruta absoluta de salida**: `<proyecto>\edit\animations\slot_<id>\render.mp4` (o .webm si necesita alfa).
3. **Especificación técnica exacta**: resolución, fps, códec, pix_fmt, CRF, duración.
4. **Paleta como valores concretos**: tuplas RGB/hex o referencia a la guía de marca (caso-video-02: fondo #0A2A39, acento #FFD700, texto blanco).
5. **Ruta de la fuente con índice** (p. ej. `C:\Windows\Fonts\arialbd.ttf`).
6. **Línea de tiempo cuadro a cuadro** (qué ocurre cuándo, con easing: `ease_out_cubic` en entradas; ver `references/motion-library.md`).
7. **Lista de exclusiones**: "sin cromo, sin extras, sin títulos salvo que se pidan".
8. **Patrón de código de referencia**: copia los helpers en línea, no importes entre slots.
9. **Checklist de entregables**: script, render, verificar duración/dimensiones con `ffprobe`, informar.
10. **"No hagas preguntas. Si algo es ambiguo, elige la interpretación más obvia y avanza."**

Notas de nuestro stack: en Windows usa Pillow para tarjetas PNG y clips de texto de Shotcut para texto animado editable; HyperFrames/Remotion/Manim no están instalados (pedir aprobación antes de instalar, `npx --yes` ejecuta paquetes sin revisar).
