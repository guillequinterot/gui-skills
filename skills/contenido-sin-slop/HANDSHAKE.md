# HANDSHAKE — contenido-sin-slop

> Estado vivo. Se lee en el Paso 0 antes de actuar y se actualiza cuando algo cambia.
> Si este archivo contradice lo que "sabes" de una herramienta, manda este archivo.

| Campo | Valor |
|---|---|
| Versión | 1.2.0 |
| Última actualización | 2026-10-30 por guille (1.2.0: puntaje 1 a 100 por bloque y excepciones SEO) |
| Skill principal / padre | ninguna (skill de calidad transversal) |
| Llama a | ninguna (el detector es un script propio sin dependencias) |
| La llaman | `seo-content-system`, `direct-visual-design`, `canva-design`, `video-editing-ai-agent`, `video-aprender` y cualquier flujo de publicación automática |

## Herramientas y su estado verificado

| Herramienta / MCP | Estado | Verificado el | Notas |
|---|---|---|---|
| `scripts/slop_lint.py` | verificado | 2026-10-26 | Python 3.12 en Windows 11, solo biblioteca estándar. Probado con textos sintéticos (español e inglés) y con dos artículos reales en español. Detecta restos objetivos, síntomas con fuente y síntomas candidatos; exit 1 solo con restos objetivos |
| `scripts/slop_lint.py --semaforo` | verificado | 2026-10-26 | Luz provisional por párrafo (rojo/amarillo/verde) con evidencia, tipo sugerido y qué falta; semáforo del documento. Probado con textos sintéticos y con dos artículos reales en español (HTML). Ignora frases citadas entre «» (mención vs uso) y menús/pies de página en HTML. Sin la opción, la salida no cambia |
| `scripts/test_slop_lint.py` | verificado | 2026-10-26 | 38 comprobaciones, todas bien (incluye falsos positivos: «todo» en español y enlaces markdown, y las del semáforo) |
| Conexión con otras skills | sin probar | — | Documentada en `references/04-integracion.md`; el primer uso real fue un validador de blog propio del mantenedor (artículos en borrador) |

Estados: `verificado` · `falla` · `sin probar` · `no aplica en Mac/Windows`.

## Capacidades confirmadas

- Puerta de cinco pasos (propósito → sustancia → procedencia y revisión humana → síntomas → decisión) aplicada a un artículo real en borrador: el detector encontró un hallazgo de formato y uno de concreción, y se añadió un dato propio verificable.
- El detector no marca como marcador de posición la palabra «todo» ni los enlaces markdown `[tu web](url)` (falso positivo corregido y cubierto por pruebas).

- Modo revisión **semáforo por párrafo** (`references/06-semaforo-por-parrafo.md`): cinco preguntas (novedad, especificidad, respaldo, lo propio, función), exigencias por tipo de párrafo, reglas de rojo/amarillo/verde y plantilla de informe. Criterios sacados de ocho fuentes (siete páginas y un video).

## Pendientes abiertos

- [ ] (1.2.0) Probar el puntaje 1 a 100 (`references/07-puntaje-por-bloque-y-excepciones-seo.md`) en un artículo real y anotar si discrepa del semáforo; hasta entonces la equivalencia entre ambos es una propuesta.
- [ ] (1.2.0) `slop_lint.py` aún no busca las familias nuevas (adverbios de relleno, falsa agencia, narrador distante, absolutos, preguntas retóricas de relleno, consejo de salud genérico) ni respeta las excepciones SEO: decidir si se añaden como candidatas con pruebas.

- [ ] Afinar los umbrales del semáforo (60 palabras sin anclajes → amarillo, un cuarto de amarillos, un tercio de rojos) con casos reales de Guille: hoy son iniciales.
- [ ] Probar el semáforo en un contenido propio completo (con revisión humana comparando la luz provisional con la final) y anotar las diferencias.
- [ ] El punto 9 de la lista de fuentes del encargo llegó vacío: si había una novena fuente, falta añadirla.

- [ ] Verificar con más textos reales en español: los síntomas del idioma español son **candidatos** (no hay una fuente comparable a la guía de Wikipedia).
- [ ] Revisión de las fuentes y de las políticas de YouTube/Google cada 3 a 6 meses (`references/05-fuentes.md`).
- [ ] Probar la integración con `seo-content-system` en un caso real que no sea el blog propio.
- [ ] Ampliar el detector a imágenes y video (hoy solo texto; imagen y video están como reglas en `references/03-…`).

## Límites conocidos

- Es un detector de **síntomas**, no de IA: no calcula porcentajes y no decide. Un texto sin hallazgos puede ser slop si falta sustancia.
- Los patrones de lenguaje cambian con cada generación de modelos; las listas se desactualizan.
- No hay fuente primaria para los síntomas en español; se rotulan «candidato».
- La métrica de «baja concreción» es una heurística burda (cifras, ejemplos y enlaces por cada mil palabras).
