# CHANGELOG — design-logo-vector

## 1.0.0 — 2026-10-31 — Creación

- Skill nueva, sub-skill de `direct-visual-design`, a petición del mantenedor, a partir de cinco repos de referencia (ver `CREDITOS.md`).
- Método reexpresado en seis referencias (`01` contrato · `02` crear · `03` vectorizar · `04` pruebas y QA · `05` entrega y kit · `06` animar y rutas).
- Scripts MIT de `pixel2svg-html` y `logo-design-skill` vendorizados sin modificar (`scripts/vendor/`, con `UPSTREAM.md` y licencias). Propios: `handshake.py` y `verificar_vectorizado.py` (semáforo ROJO/AMARILLO/VERDE).
- Verificado en Windows 11 / Python 3.12 / Chrome headless con un logo sintético de dos colores; **sin caso real todavía** (ver `HANDSHAKE.md`).
- Hallazgo de la prueba: `svg_path_audit.py` aproxima los arcos SVG con rectas y avisa de uniones falsas; `verificar_vectorizado.py` omite esos avisos cuando el trazado usa arcos.
- Integración: fila en la tabla de enrutamiento de `direct-visual-design/SKILL.md`, fila en el `README.md` del repo y `HANDSHAKE.md` del padre.
