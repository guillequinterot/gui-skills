# HANDOFF — handoff-handshake-ia

> Traspaso entre sesiones y personas: qué es la skill, qué se decidió y qué se aprendió en cada trabajo. Estado vivo (versión, pendientes, límites) → `HANDSHAKE.md`.

## 1. Qué es y cuándo se usa

Skill **propia** del mantenedor para que los agentes de IA traspasen proyectos y tareas sin perder el hilo: `HANDSHAKE.md` corto con el estado vivo, ficha `HANDOFF.md`, `historial/` archivado, `AGENTS.md` con los guardrails que el dueño decide por proyecto, lectura de arranque de cinco líneas, `NO CONSTA` en vez de inventar, un verificador (`scripts/verificar.py`) y un modo `repartir` para varios encargos. Se usa al arrancar, retomar, traspasar y cerrar proyectos o tareas y al partir un HANDOFF extenso. **Validación parcial** (ver `references/08-pilotos.md`).

## 3. Decisiones vigentes

| Fecha | Decisión | Quién la aprobó | Por qué |
|---|---|---|---|
| 2026-11-22 | Estructura: HANDSHAKE vivo con tope de 150 líneas por defecto (configurable), ficha HANDOFF, historial archivado, AGENTS.md, readback, `NO CONSTA`, verificador y paso de reparto | el mantenedor | Las IA alucinan cuando el proyecto crece y el contexto se compacta; el traspaso debe ser lo mínimo para ejecutar sin inventar |
| 2026-11-22 | Los guardrails se preguntan al dueño en cada proyecto; no se heredan | el mantenedor | Cada proyecto tiene riesgos distintos |
| 2026-11-22 | Los proyectos existentes se migran solo cuando se retoman, en copia y sin borrar | el mantenedor | Evitar tocar lo que no se usa |
| 2026-11-22 | Se publica la v0.2 como «validación parcial» aunque quedó a una respuesta del criterio en un caso | Desktop (orquestador), por instrucción de el mantenedor de aprobar y subir si los pilotos lo justificaban | Mejoras medidas en dos casos; el repo es privado y se revisa. **El criterio escrito de la skill (igualar o superar al formato anterior en los dos casos re-probados) quedó incumplido por una respuesta; publicar como parcial fue decisión de una IA y el mantenedor debe revisarla** |

## 4. Registro de trabajos
<!-- registro:inicio -->
### 2026-11-22 22:05 (Bogotá) · re-prueba y decisión de publicar · Desktop
- [medido] Re-prueba a ciegas de la v0.2: caso-handoff-02 7 contra 7 del formato anterior (la v0.1.1 había sacado 5); caso-handoff-04 6 contra 7 (la v0.1.1, 5). Lectura en frío ≈ 188 líneas en 02 (antes ≈ 249) y ≈ 157 en 04 (antes ≈ 447).
- [visto] La firma de migración ya no tapa el último trabajo real (pregunta 7 acertada en ambos). La pregunta fallada en 04 fue la contradicción del total: el proyecto traía la regla y el migrador escribió «pendiente». Se ajustó el paso 4 de `references/06-migracion.md` (buscar primero una regla del propio proyecto); **sin re-probar**.
- [inferido] 6 contra 7 con n = 1 por celda es compatible con empate. No se cumplió por una respuesta el criterio «iguala o supera en los dos»; se decide publicar como **validación parcial** con la etiqueta escrita en la skill.
- [no sé] Eficacia contra alucinaciones: ninguna IA inventó datos con ningún formato, por lo que no se puede atribuir mejora. Ejemplos anonimizados de casos reales: no hechos.

### 2026-11-22 21:32 (Bogotá) · v0.2 en re-prueba · Codex
- [visto] Cambios en `templates/`, `references/06-migracion.md`, `references/07-evidencia-y-limites.md`, `references/08-pilotos.md`, `SKILL.md` y `scripts/`: último trabajo real, precedencia de contradicciones, estado citable, umbral provisional, resultados y verificador.
- [visto] La v0.1.1 empató 30/40 contra 30/40. La v0.2 requiere QA independiente y re-migración con lectura a ciegas de caso-handoff-02 y caso-handoff-04 antes de publicar.
- [no sé] Resultado de la re-prueba y eficacia contra alucinaciones: NO CONSTA. Los detalles y comprobaciones de esta tarea constan en `04-trabajo/2026-11-22-skill-v0.2/NOTAS-codex.md` fuera del repositorio.

### 2026-11-22 19:34 (Bogotá) · revisión 1 · Codex
- Hecho: corrección UTF-8, referencias y plantillas ampliadas, patrón de orden y pruebas nuevas.
- Evidencia: `scripts/test_verificar.py`: 11 pruebas pasan; búsqueda de corrupción y escaneo de privacidad sin hallazgos.
- Pendiente: QA independiente, cinco pilotos y resultado de la ronda 3 de OpenCode; eficacia contra alucinaciones no probada.

### 2026-11-22 19:30 (Bogotá) · construcción inicial · Codex
- Hecho: skill 0.1 en piloto, referencias, plantillas y comprobador.
- Evidencia: cuatro pruebas mínimas del script y escaneo de privacidad sin hallazgos informados en esa sesión.

### 2026-11-22 · banco-pruebas-handoff-handshake · guille

- **Qué se hizo:** Skill nueva handoff-handshake-ia v0.2: estado vivo corto, ficha, historial, verificador y umbral de uso; cinco pilotos (caso-handoff-01 a 05) con lectura en frío a ciegas contra el formato anterior y re-prueba de la v0.2 en dos casos.
- **Salió bien:** Cero respuestas inventadas con ambos formatos; la v0.2 corrigió la firma de migración que tapaba el último trabajo real (02: 5 a 7; 04: 5 a 6 de 8) y redujo la lectura (04: unas 157 líneas contra unas 447); mejor resultado en dos proyectos grandes o caóticos (01 y 03) con una lectura por celda.
- **Salió mal / incidencia:** La v0.1.1 empató 30 contra 30 de 40; la v0.2 quedó 6 contra 7 en caso-handoff-04 por una respuesta (criterio de aprobación no cumplido); una lectura por celda, solo indicios; sin ejemplos anonimizados; el ajuste del paso 4 de la migración no se re-probó. Incidencia: Un lector de Codex quedó 1,4 horas esperando entrada por teclado hasta lanzarlo con la entrada cerrada; un sello vencido de otra cuenta bloqueó encargos que declaraban la misma carpeta de trabajo; una lectura de Figma salió con archivos faltantes por mi montaje y se repitió.
- **Regla candidata:** Umbral provisional: migrar solo si HANDOFF y HANDSHAKE superan unas 400 líneas, hay varios archivos de estado o contradicciones; si el proyecto es corto y limpio, solo AGENTS.md, Último trabajo real y Estado en una frase. Cinco casos, sin validar.
- **Herramientas:** Claude Pro CLI, Codex, subagentes de Desktop, verificar.py, privacy_scan.py

### 2026-11-22 · banco-pruebas-handoff-handshake · guille

- **Qué se hizo:** Re-prueba ciega de la v0.2 en los casos 01, 03 y 05 (total v0.2: 30 contra 32 del formato anterior en cinco casos); ajuste del umbral de uso a unas 1.000 líneas, nuevo paso de migración que comprueba que objetivo y rutinas sobreviven y aviso de ruido de puntuación.
- **Salió bien:** El formato anterior cayó otra vez en la trampa del caso 01 y el nuevo no; la firma de migración ya no tapa el último trabajo real en ningún caso; cero respuestas inventadas; se detectó el ruido de puntuación comparando el mismo texto puntuado dos veces.
- **Salió mal / incidencia:** No se demostró ventaja de la v0.2: el post bajó de 7 a 5 porque el migrador perdió el objetivo y la rutina de las 21:30; el mismo texto se puntuó 5 y 7 según el evaluador, así que diferencias de 1 o 2 puntos no son distinguibles del ruido; la única ventaja repetida es con un HANDOFF de unas 1.200 líneas (un caso).
- **Regla candidata:** ninguna
- **Herramientas:** Codex, Claude Pro CLI, subagentes de Desktop

<!-- registro:fin -->

## 5. Reglas candidatas (sin aprobar)

| Regla | Visto en (casos) | Estado |
|---|---|---|
| Umbral provisional: migrar solo si el HANDOFF no cabe en una lectura (unas 1.000 líneas o más) o hay un estado desactualizado conocido; entre 150 y 1.000 líneas sin evidencia en ningún sentido; si es corto y limpio, solo AGENTS.md, Último trabajo real y Estado en una frase. | caso-handoff-01, caso-handoff-02, caso-handoff-03, caso-handoff-04, caso-handoff-05 | candidata |

