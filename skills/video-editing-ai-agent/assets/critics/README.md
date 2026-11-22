# Lentes de revisión (v1.6)

Plantillas para que **un revisor distinto del que construyó** mire la pieza con un solo criterio a la vez. Patrón y estructura de `cinetic` (Leonxlnx, MIT), reescritas en nuestras palabras y con nuestros scripts. Cómo y cuándo usarlas: `references/direccion-y-revision.md` §4.

- Rellena cada `{{CAMPO}}` y entrega el archivo entero a un subagente (o síguelo tú con la hoja abierta). El revisor **no recibe** el contexto de quien construyó, solo lo que la plantilla pide.
- Todas devuelven **solo JSON** con la forma del final de `director.md` (`issues[]` con `id`, `item`, `priority`, `frame`, `problem`, `fix`), así los resultados de varias lentes se pueden juntar.
- Orden: `director` (siempre) → `forense`, `sincronia-sonido`, `detalle` (solo si el usuario pide más profundidad o una compuerta sigue fallando en su área) → `refutador` sobre **todos los P0 y P1** antes de arreglar nada.
- **Prioridades:** P0 se ve en un momento clave o rompe la historia; P1 se nota viendo con normalidad; P2 solo al pausar. Cualquier cosa que el revisor cuente la apoya con **fotogramas** (número exacto o rango), nunca con «se ve mal».
- Que una plantilla diga «no propongas añadir texto» no es estilo: es la causa más común de piezas peores tras una revisión.
- Estado: **candidato**. Ninguna lente se ha corrido todavía con una pieza real; anota en el `HANDOFF.md` cuál sirvió y cuál sobró.
