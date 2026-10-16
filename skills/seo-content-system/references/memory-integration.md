---
tags:
  - seo
---

# Memoria de la skill: repo primero, Obsidian opcional

## Índice

- Función de la memoria
- Fuente canónica de la skill
- Dónde se guarda cada cosa
- Resolución de ruta (con o sin bóveda)
- Paso 0: qué leer y dónde
- Tipos de notas
- Frontmatter
- Flujo de aprendizaje
- Lectura selectiva
- Conflictos
- Estructura sugerida para la bóveda (opcional)

## Función de la memoria

La memoria conserva investigación, decisiones, proyectos y aprendizajes extensos. La skill conserva el procedimiento estable y referencias compactas. No duplicar toda la memoria dentro de `SKILL.md`.

La memoria es la versión actual del conocimiento; el modelo entrenado es la versión vieja. Cuando ambos difieran, gana la memoria, salvo instrucción explícita del usuario, brief activo o fuente primaria.

## Fuente canónica de la skill

La fuente canónica de esta skill es **el repo gui-skills** (`<repo>/skills/seo-content-system/`). Se instala por enlaces (`tools/install.ps1` / `tools/install.sh`), así que no existe una "copia instalada" que pueda quedar desfasada: lo que edites en el repo es lo que usa el agente. Los cambios se proponen con una rama `aporte/<alias>/<tema>` y un PR (ver `CONTRIBUTING.md` del repo).

La versión para entornos sin sistema de archivos (`skills/seo-content-system-web-hosted/`) se **genera** desde esta skill con `tools/build_hosted.py`; nunca se edita a mano.

## Dónde se guarda cada cosa

| Qué | Dentro del repo (siempre disponible) | En la bóveda de Obsidian (solo si está configurada) |
|---|---|---|
| Estado vivo, herramientas, pendientes | `HANDSHAKE.md` | — |
| Decisiones vigentes y registro de casos | `HANDOFF.md` §3 y §4 | `06_Aprendizaje/Decisiones/`, `09_Proyectos/` |
| Aprendizajes sin validar | `memoria/aprendizaje/inbox/` | `06_Aprendizaje/Inbox/` |
| Decisiones aprobadas (con evidencia y fecha de revisión) | `memoria/decisiones/` | `06_Aprendizaje/Decisiones/` |
| Reportes de novedades de buscadores | `memoria/novedades/` | `02_Investigacion/Novedades/` |
| Fichas de fuentes | `memoria/fuentes/` | `08_Fuentes/` |

Los casos de clientes nunca se nombran en el repo: solo con código `caso-<tipo>-<NN>`. La equivalencia código → cliente vive en `~/.gui-skills/equivalencias.md` (fuera del repo). En la bóveda propia sí pueden usarse nombres reales, porque es privada.

## Resolución de ruta (con o sin bóveda)

Los scripts (`capture_learning.py`, `research_update.py`, `scheduler.py`, `validate_vault.py`) deciden dónde escribir así:

1. Argumento `--vault` (si se pasa).
2. Variable de entorno `SEO_OBSIDIAN_VAULT`.
3. Clave `obsidian_vault` de `~/.gui-skills/config.json` (y, opcional, `obsidian_seo_folder` para indicar la carpeta de la skill dentro de la bóveda).
4. Clave heredada `vault` de `~/.seo-content-system.json` (configuración anterior al repo).

Si ninguna apunta a una carpeta existente, **no hay bóveda y los scripts escriben en `memoria/` dentro de la skill**, creando las carpetas que falten. Nunca fallan por no tener Obsidian.

Cuando hay bóveda y su ruta es la raíz de la bóveda (no la carpeta de la skill), la carpeta de trabajo se busca en este orden: la que indique `obsidian_seo_folder`; una subcarpeta que ya tenga la estructura `06_Aprendizaje/`; `SEO Content System/` en cualquier nivel conocido; y, si no existe nada, se crea `SEO Content System/` en la raíz.

Si ninguna memoria persiste, informarlo: el aprendizaje no se guardó. Nunca simular que se consultó.

## Paso 0: qué leer y dónde

Antes de producir cualquier salida, consultar en este orden:

1. `HANDSHAKE.md` y el registro de trabajos de `HANDOFF.md` (siempre).
2. `memoria/decisiones/` y `memoria/aprendizaje/inbox/` por el tema concreto.
3. `memoria/fuentes/` antes de afirmar datos o reglas SEO.
4. Si hay bóveda: su carpeta de la skill (misma estructura) y la nota madre del proyecto.
5. El brief o la nota del proyecto del usuario, en su carpeta de proyecto.

Leer primero mapas de contenido y notas enlazadas. No cargar toda la memoria: buscar por tema y leer solo notas pertinentes.

## Tipos de notas

- `learning`: observación de trabajo.
- `research-update`: novedad recopilada.
- `source`: ficha de evidencia.
- `decision`: cambio aprobado.
- `project`: contexto y resultados.
- `experiment`: hipótesis, cambio y medición.
- `content`: brief y paquete SEO.

## Frontmatter

```yaml
---
type: learning
status: candidate
created: 2026-07-23
updated: 2026-07-23
topics:
  - seo
sources: []
projects: []
confidence: low
review_after: 2026-08-23
---
```

## Flujo de aprendizaje

1. Capturar con `scripts/capture_learning.py` en `memoria/aprendizaje/inbox/` (o `06_Aprendizaje/Inbox/`).
2. Relacionar con caso (código) y fuente.
3. Revisar evidencia.
4. Mover a experimentación o descartar.
5. Promover a conocimiento estable solo con decisión registrada en `memoria/decisiones/` (y anotada en HANDOFF §3). Una observación de un solo trabajo nunca es regla.
6. Sincronizar la referencia de la skill si corresponde, mediante un PR.

## Lectura selectiva

Buscar por:

- Título.
- Alias.
- Etiqueta.
- Enlace.
- Caso.
- Fuente.

## Conflictos

Ante versiones distintas:

- Conservar ambas.
- Comparar fechas y fuentes.
- Crear una nota de decisión.
- Marcar la nota obsoleta con `status: superseded`.
- Enlazar la versión vigente.

## Estructura sugerida para la bóveda (opcional)

Para quien usa Obsidian, la carpeta de la skill dentro de su bóveda puede organizarse así (`scripts/validate_vault.py` la comprueba):

```
SEO Content System/
├── 00_Inicio/                      ← Punto de entrada, mapas generales
├── 01_Conocimiento/                ← Notas de conocimiento estable (SEO, GEO, redacción…)
├── 02_Investigacion/
│   └── Novedades/                  ← Reportes de actualización fechados
├── 03_Estrategia/                  ← Frameworks, mapas de keywords, priorización
├── 04_Produccion/                  ← Checklists de publicación y flujo editorial
├── 05_Medicion/                    ← GA4, Search Console, experimentos
├── 06_Aprendizaje/
│   ├── Inbox/                      ← Aprendizajes candidatos, sin validar
│   └── Decisiones/                 ← Cambios aprobados con evidencia y fecha de revisión
├── 07_Plantillas/                  ← Plantillas de proyecto, decisión, brief, experimento, fuente
├── 08_Fuentes/                     ← Fichas de fuentes, registro maestro, evaluación
└── 09_Proyectos/                   ← Contexto y resultados por cliente
```

Las notas de bóveda pueden usar enlaces `[[...]]`; los archivos del repo usan enlaces Markdown relativos.
