# Cómo conectar la puerta anti-slop

## 1. Con otras skills (quién la llama y cuándo)

| Skill que produce | Momento | Qué se aplica |
|---|---|---|
| `seo-content-system` | Modos `write`, `brief`, `on-page`, `programmatic`, `update`, justo antes de «Entregar el paquete SEO» | Pasos 1 a 3 de la puerta; el detector sobre el texto final. En `programmatic`, la puerta es **por plantilla y por página**: cada página debe tener datos propios (ver «unicidad» de esa skill) |
| `direct-visual-design`, `canva-design` | Antes de entregar imágenes y piezas para redes o blog | Sección «Imagen» y «Redes» de `03-…` |
| `video-editing-ai-agent`, `video-aprender` | Antes de publicar un video o un resumen hecho con IA | Sección «Video» de `03-…`; guion revisado contra las fuentes |
| Cualquier flujo automático | Antes de **cada** publicación | La puerta completa y la decisión «publicar / reescribir / descartar» |

La skill que llama sigue mandando en su propio formato; esta solo agrega la puerta y puede decir **«no pasa»**.

## 2. En un flujo de publicación programada (calendario, agentes sin supervisión)

Un flujo sin revisión semanal es donde más se cuela el slop. Condiciones mínimas:

1. **La puerta es un paso del manual del flujo** (RUNBOOK) y bloquea la publicación si falla.
2. **Hay un banco de experiencia aprobado** (casos, cifras y opiniones que la persona firmante autorizó una vez) y un archivo de voz; el agente solo cita de ahí en las partes de experiencia propia.
3. **Registro de revisión humana:** quién revisó, cuándo y qué cambió. Para el primer mes, revisión de todas las piezas; luego, muestreo.
4. **Validación automática de lo objetivo**: enlaces vivos, fuentes citadas, cifras con fuente, restos de chatbot, marcadores de posición, `utm_*`. Se corre `scripts/slop_lint.py` y se trata como **fallo** lo objetivo y como **aviso** lo demás.
5. **Interruptor de pausa** y **límite de volumen** (como máximo una pieza por unidad de tiempo definida).
6. **Descartar es un resultado normal:** si una semana no hay nada propio que decir, no se publica y se avisa; no se rellena.

Ejemplo de conexión en un validador de artículos:

```python
import subprocess, sys
r = subprocess.run([sys.executable, "-I", "<skill>/scripts/slop_lint.py", articulo, "--idioma", "es", "--json"],
                   capture_output=True, text=True, encoding="utf-8")
# r.returncode == 1  -> restos objetivos: bloquear
# r.stdout (JSON)    -> avisos por familia y nivel: mostrar al revisor, no bloquear por sí solos
```

## 3. Registro de revisión humana (plantilla)

```
Pieza: <título o archivo>
Fecha: <AAAA-MM-DD>
Firma/revisión: <persona real>
Propósito para el lector: <una frase>
Sustancia propia añadida: <caso, dato, criterio> (de dónde sale)
Fuentes abiertas y verificadas: <n>  (enlaces comprobados el <fecha>)
Uso de IA: <qué hizo la IA, qué hizo la persona>
Divulgación: <dónde se explica, o «no corresponde»>
Detector: <n restos objetivos, n síntomas por familia> → <qué se corrigió y por qué causa>
Decisión: publicar | reescribir | descartar
```

## 4. Qué registrar para aprender

En el HANDOFF de la skill que produjo la pieza, anotar: qué falló en la puerta, de qué prompt o fuente vino, qué
se añadió y cuántas piezas se descartaron. Una **regla candidata** solo pasa a regla cuando se repite en dos o más
casos o la aprueba la persona responsable (protocolo gui-skills).
