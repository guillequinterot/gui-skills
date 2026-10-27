# CHANGELOG — design-system-ia

## 0.2.0 — 2026-10-27

Primera prueba real (`caso-ds-01`, sitio Astro propio) y biblioteca de módulos.

- **Nuevo:** `scripts/generar_biblioteca.py` (página única de documentación: menú lateral con el logo y los colores del cliente, botón para volver al home, referente visual por módulo, botones Copiar HTML/CSS/JSON/prompt, Ver código y Ver CSS del módulo, `noindex`), `scripts/extraer_modulo.py` (HTML y CSS reales de un componente) y `templates/biblioteca-manifiesto.json`. Referencia 04, sección 13.
- **Corregido durante la prueba:** `contraste.py` admite un sitio de un solo tema; el verificador de contratos de otro sistema no valida el esquema completo (referencia 01); el esquema propio admite campos extra en objetos anidados.
- **Entrega estándar = carpeta con capa para IA:** `generar_biblioteca.py` escribe además `sistema.json`, `llms.txt`, `AGENTS.md`, `modulos/<id>.json` y `logo.svg`; el **logo de la marca es obligatorio**; las vistas previas existen en el HTML estático (Shadow DOM declarativo); la página trae «Copiar prompt maestro» con la URL.
- Pruebas: de 25 a 55.

## 0.1.0 — 2026-10-27

Primera versión (borrador), construida a partir de la investigación de un sistema de diseño de código abierto y contrastada con fuentes primarias.

- `SKILL.md`: 3 perfiles de proyecto, 2 de gobierno, regla de salto, 7 modos de trabajo, 14 reglas duras (cada una declara si es blanda o dura), publicación que siempre pregunta el destino.
- `references/` (9): contrato · tokens y nombres · vocabulario de props · documentación y entrega · Figma · listo para IA · medición · gobierno, accesibilidad y estabilidad · arranque y operación.
- `templates/` (16 + índice): plan de arranque, decisión, contrato mínimo y completo, vocabulario, página de componente, lista de control, nota para agentes, índice `llms.txt`, solicitud, ficha de auditoría, tabla de métricas, tabla «antes → después», patrón, tarea y encuesta corta.
- `scripts/`: `validar_contrato.py` (+ `contrato.schema.json`), `contraste.py`, `vocabulario_check.py`, `comparar_figma_contrato.py`, `handshake.py`, `install.py` y 25 pruebas.
- `conocimiento/`, `memoria/`, `proyectos/`, `ejemplos/` y `CREDITOS.md`.
- Hallazgo corregido durante la construcción: el verificador de contratos del sistema de referencia no valida el esquema completo; se aclaró en la referencia 01.
