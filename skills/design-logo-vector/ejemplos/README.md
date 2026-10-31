# Ejemplos

No hay material de clientes en esta carpeta (los logos de clientes no se suben al repo).

## Caso sintético de verificación (2026-10-31)

Para comprobar que las herramientas funcionan sin depender de un cliente:

1. Un logo geométrico generado con Pillow (anillo azul, hueco blanco, cuña naranja, 800 × 800 px).
2. `raster_logo_trace.py` → `logo.svg` con 207 nodos / 166 segmentos rectos / 0 curvas, IoU 0,9927. `verificar_vectorizado.py` lo marca **ROJO**: IoU alto, pero es un polígono por píxeles.
3. El mismo logo dibujado con dos arcos (`a.svg`, 190 bytes, 6 nodos) → **VERDE**.

Moraleja que ilustra el caso: el IoU no distingue un vector bien construido de un trazo por píxeles; la compuerta de suavidad y de complejidad sí.

Cuando exista un caso real aprobado, añade aquí un README anónimo (`caso-logo-<NN>`) con: insumo, nivel de la escalera usado, iteraciones, IoU, residuos y lecciones.
