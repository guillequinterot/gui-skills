---
tags:
  - seo
---

# Cada cuánto hacer keyword research: cadencia y disparadores

## Índice

- Principio
- Estado de la evidencia
- Tres tipos de keyword research, tres cadencias distintas
- Cadencia orientativa por tipo de sitio
- Disparadores que fuerzan una revisión fuera de calendario
- Cómo decidir el alcance de cada revisión
- Registro de cadencia por proyecto
- Errores frecuentes
- Lista de revisión

## Principio

"Hacer keyword research" no es un evento único ni una tarea de calendario fijo idéntica para todos los proyectos: la frecuencia correcta depende de qué tipo de investigación es, de la velocidad de publicación del sitio, de la volatilidad del sector y de señales concretas de rendimiento — no de un número universal de meses. Este archivo cierra ese hueco: aplica tanto en la ruta local ([keyword-research-ia-local-desktop.md](keyword-research-ia-local-desktop.md)) como en la ruta alojada ([keyword-research-ia-web-hosted.md](keyword-research-ia-web-hosted.md)).

## Estado de la evidencia

Los rangos de cadencia de este archivo son **heurística de consultoría razonable**, no una cifra medida ni una regla de Google. Se construyen sobre dos piezas ya presentes en la skill que sí tienen justificación propia: la recomendación de revisar el mapa temático cada 3-6 meses (`topical-map-and-content-architecture.md`) y la revisión mensual de logs/consultas ya sugerida para flujos de IA (`ai-assisted-search-console-workflow.md`, `ai-crawler-access-and-llms-txt.md`). Tratar como candidata a ajustar con evidencia propia del proyecto, no como calendario fijo.

## Tres tipos de keyword research, tres cadencias distintas

No es lo mismo investigar desde cero que dar mantenimiento a lo que ya existe. Distinguir:

### 1. Investigación fundacional (mapa temático completo)

Construir o reconstruir el mapa temático completo del sitio (`topical-map-and-content-architecture.md`): tema principal, clusters, universo de subtemas.

- **Cuándo:** al arrancar un proyecto nuevo, o cuando el negocio cambia de forma material (nueva línea de producto, nuevo mercado/país, rebranding, fusión de sitios).
- **No tiene cadencia de calendario fija** — es event-driven, no periódica. Repetirla completa sin que el negocio haya cambiado es desperdiciar el trabajo ya hecho.

### 2. Revisión y expansión del mapa existente

Revisar el mapa ya construido para detectar huecos nuevos, consolidar duplicados y ajustar prioridades — no reconstruirlo desde cero.

- **Cadencia orientativa:** cada 3-6 meses (ya establecida en `topical-map-and-content-architecture.md`). Sitios con publicación intensa o sectores volátiles, hacia el extremo de 3 meses; sitios estables con publicación baja, hacia 6 meses.

### 3. Minería de keywords de oportunidad (mantenimiento continuo)

Detectar keywords de oportunidad sobre contenido ya publicado usando datos reales de Search Console (`analytics-search-console-and-decisions.md`, `ai-assisted-search-console-workflow.md`): posición 5-20, impresiones altas con CTR bajo, gaps de contenido.

- **Cadencia orientativa:** mensual para sitios con volumen alto de tráfico/páginas donde hay suficientes datos nuevos cada mes para que el análisis sea confiable; trimestral para sitios pequeños o de bajo tráfico, donde un mes no acumula señal suficiente en Search Console.
- Esta es la cadencia que más se beneficia de automatización (ver `ai-assisted-search-console-workflow.md`), precisamente porque se repite con frecuencia sobre las mismas URLs.

## Cadencia orientativa por tipo de sitio

| Tipo de sitio / sector | Revisión de mapa | Minería de oportunidad |
|---|---|---|
| Ecommerce o sector de alta competencia y cambio rápido (moda, tecnología, finanzas) | 3 meses | Mensual |
| Servicios B2B o profesionales con catálogo estable | 4-6 meses | Mensual a trimestral |
| Sitio local o de nicho con baja competencia | 6 meses | Trimestral |
| Contenido evergreen de bajo volumen de publicación | 6-12 meses | Trimestral a semestral |

Ajustar siempre con datos propios del proyecto (velocidad real de cambio de la SERP, volumen de tráfico, capacidad del equipo) en vez de aplicar la tabla de forma mecánica.

## Disparadores que fuerzan una revisión fuera de calendario

Cualquiera de estos eventos justifica adelantar la revisión sin esperar al ciclo programado:

- **Core update o spam update de Google** confirmado (ver cadencia "por evento" ya establecida en `update-governance-and-research.md`).
- **Caída o subida sostenida** de impresiones, clics o posición media en un clúster completo, no solo una URL.
- **Aparición de una nueva feature de SERP** relevante para el sector (por ejemplo, AI Overviews empieza a aparecer en consultas transaccionales del nicho).
- **Un competidor gana visibilidad** notable en el mismo campo temático.
- **Lanzamiento de un producto, servicio o línea de negocio nueva.**
- **Canibalización detectada** entre dos o más URLs propias.
- **Cambio de plataforma, CMS o migración** que pueda haber alterado arquitectura o URLs.
- **Anomalía puntual** en Search Console (caída repentina de una página que antes tenía tráfico estable).

## Cómo decidir el alcance de cada revisión

No cada disparador exige repetir la investigación fundacional completa:

```text
¿Cambió el negocio (producto, mercado, marca)?      → investigación fundacional
¿Cambió el algoritmo o la SERP de forma amplia?      → revisión del mapa + validación SERP de clusters afectados
¿Hay una anomalía en una URL o clúster puntual?      → minería de oportunidad focalizada en esa URL/clúster
¿Pasó el tiempo del ciclo normal sin eventos?        → revisión de mapa según la cadencia de la tabla
```

## Registro de cadencia por proyecto

Guardar en la nota del proyecto del usuario (en Obsidian, si lo usa) o en `00_PROYECTO` de la matriz:

```text
Proyecto:
Cadencia de revisión de mapa: (meses)
Cadencia de minería de oportunidad: (meses)
Última investigación fundacional: (fecha)
Última revisión de mapa: (fecha)
Última minería de oportunidad: (fecha)
Próxima revisión programada: (fecha)
Disparadores activados desde la última revisión:
```

## Errores frecuentes

- Tratar "hacer keyword research" como una sola tarea con una sola cadencia, sin distinguir fundacional / revisión de mapa / minería de oportunidad.
- Reconstruir el mapa temático completo cada vez que se detecta una keyword de oportunidad puntual.
- Dejar pasar un core update sin revisar si algún clúster necesita atención antes del ciclo programado.
- Aplicar la misma cadencia a un ecommerce de alta rotación y a un sitio de servicios profesionales estable.
- No registrar la fecha de la última revisión, perdiendo trazabilidad de cuándo tocaría la siguiente.

## Lista de revisión

- ¿Se distinguió qué tipo de keyword research corresponde (fundacional, revisión de mapa, minería de oportunidad)?
- ¿La cadencia elegida está justificada por el tipo de sitio y sector, no aplicada por defecto?
- ¿Se revisó si algún disparador de la lista ocurrió desde la última revisión?
- ¿Quedó registrada la fecha de la última revisión y la próxima programada?
- ¿Una anomalía puntual se atendió de forma focalizada, sin disparar una investigación fundacional innecesaria?
