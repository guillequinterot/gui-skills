# Sistemas de diseño, componentes y tokens

## Contenido

1. Propósito
2. Atomic Design
3. Design tokens
4. Componentes
5. Gobernanza
6. QA

## 1. Propósito

Construir un sistema para mejorar coherencia, velocidad, accesibilidad y colaboración. No confundir sistema de diseño con archivo de Figma, catálogo visual o guía de marca.

Definir alcance, consumidores, plataformas, responsables, contribución, versiones y métricas antes de multiplicar componentes.

## 2. Atomic Design

Usar átomos, moléculas, organismos, plantillas y páginas como modelo mental útil. No convertir la nomenclatura química en requisito. Diseñar simultáneamente desde componentes y páginas reales para comprobar contexto y resiliencia.

- Átomo: unidad básica con función clara.
- Molécula: combinación pequeña con responsabilidad concreta.
- Organismo: sección compleja y reconocible.
- Plantilla: estructura de página sin contenido definitivo.
- Página: instancia con contenido real y casos extremos.

Permitir taxonomías semánticas alternativas cuando mejoren comunicación.

## 3. Design tokens

Seguir el estándar DTCG cuando la interoperabilidad sea importante. Separar cuando convenga:

- **tokens base/primitive:** valores de escala o marca;
- **tokens semánticos:** propósito como `color.text.default`;
- **tokens de componente:** decisión específica como `button.primary.background`.

No asumir que los primitives son universalmente inmutables ni que toda arquitectura necesita exactamente dos niveles. Documentar alias, temas, modos, deprecación y salida por plataforma.

Categorías frecuentes: color, tipografía, espacio, tamaño, radio, borde, sombra, opacidad, duración, easing y z-index.

## 4. Componentes

Documentar:

- propósito y cuándo no usar;
- anatomía;
- variantes y propiedades;
- estados y comportamiento;
- contenido permitido y límites;
- responsive;
- accesibilidad, teclado y nombres;
- tokens utilizados;
- ejemplos con contenido real;
- casos vacíos, loading, error y overflow;
- equivalencia entre diseño y código.

Evitar variantes combinatorias innecesarias. Separar configuración, contenido y estado.

## 5. Gobernanza

Definir:

- propietario y modelo federado/centralizado;
- proceso de propuesta, revisión y aceptación;
- criterios para añadir en lugar de reutilizar;
- versionado y cambios incompatibles;
- deprecación y migración;
- documentación y soporte;
- sincronización diseño-código;
- métricas: adopción, cobertura, defectos, tiempo y satisfacción.

## 6. QA del sistema

Probar componentes aislados y en páginas reales:

- contenido mínimo/máximo y localización;
- temas y contraste;
- teclado, foco y lector de pantalla;
- breakpoints y zoom;
- estados asíncronos;
- snapshots o regresión visual;
- compatibilidad de tokens;
- consistencia entre Figma y producción;
- migración y deprecación.

No prometer consistencia del 100% ni rendimiento de negocio sin medición.
