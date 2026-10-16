# CHANGELOG — web-go-high-level-ia

## 2026-10-16 — v1.3.0 (migración al repo gui-skills)
- El repo gui-skills pasa a ser la fuente canónica; ya no hay `install.py` propio ni copia instalada que desfasar (instalación por enlace con `tools/install.ps1` / `tools/install.sh`).
- Anonimizado el caso de origen: queda como `caso-web-universidad-01` (`references/08-caso-web-universidad-01.md`, `proyectos/caso-web-universidad-01.md`); ids de cuenta y proyecto, correos, dominios y rutas personales fuera de todos los archivos.
- `ejemplos/caso-web-universidad-01/` ahora son patrones sanitizados con datos inventados (módulo de datos, mapa de imágenes, ruta con filtros, generador CSV → TypeScript, configuración de partes); el código y los textos del cliente no se publican.
- `scripts/make_partes.py` genérico (configuración en JSON) sustituye a los generadores de partes específicos de cada entrega (`make_entrega2_partes.py`, `make_cambios2_partes.py`, `make_qa_partes.py`); `cshot.sh` y `qa_visual.py` dejan de usar rutas del equipo (variables `CHROME` y `GUI_QA_DIR`); `handshake.py` avisa (no falla) fuera de Windows.
- Protocolo gui-skills en `SKILL.md`; `HANDOFF.md` con registro de trabajos y `HANDSHAKE.md` con herramientas verificadas; Obsidian pasa a ser opcional en todas las referencias.
- No migrados: `_respaldo/`, `gen_oferta.py` y el resto del código del cliente.

## 2026-10-14 — v1.2.0 (primera operación real del builder con Claude in Chrome)
- `references/07` sección **L** (L1–L9): conexión de la extensión, iframe de otro origen, patrón fiable de pegado en el chat, pestaña única, la IA que reestructura (y cómo re-sincronizar el local), descarga de la base de código, subida a Medios con `file_upload`, URL del CDN desde el DOM + SHA-256, QA en la vista previa pública con iframes del mismo origen.
- Caso `caso-web-universidad-01`: entrega 2 aplicada en el builder (4 partes), 17 fotos subidas y conectadas, 46/46 comprobaciones en la vista previa real; ejemplos actualizados con la estructura real del builder (mapa de imágenes en un módulo aparte).

## 2026-10-13 (noche) — v1.1.0 (contenido largo desde fuentes oficiales y entrega sin acceso al builder)
### Añadido
- `references/07` sección **K** (K1–K9): límite de 50 000 caracteres y archivos generados, 403 por cabeceras, hipervínculos de la hoja de cálculo que el conector no expone, PDF equivocados en la hoja del cliente, erratas de la fuente, capturas móviles con `--headless`, respaldo de fotos no subidas, qué hacer si no hay acceso al builder, no pisar archivos «completos».
- Ejemplos: módulo de textos largos, extractor literal de páginas oficiales → JSON → generador, y partes con archivos nuevos «CREA», «REEMPLAZA», «AÑADE AL FINAL».
- Un script de partes como plantilla, con parte final de memoria (AGENTS + README).
- Patrón: **textos de fichas = literales de la fuente oficial**, rotulados por tipo, con fuente y fecha de consulta visibles; lo que la fuente no trae queda con marcador y en el README.

## 2026-10-13 — v1.0.0 (creación, caso `caso-web-universidad-01`)
Origen: petición del mantenedor durante la Home del caso: «hagamos una skill web-go-high-level-IA donde tengamos todo este proceso y las incidencias y que tenga su handoff y handshake; agrégala como sub skill de /direct-visual-design y de /seo-content-system».

### Añadido
- `SKILL.md` (criterio de aceptación, flujo, 12 reglas duras) y `references/01…08` (proceso, partes, AGENTS/README vivos, transferencia por portapapeles, imágenes/CDN, SEO, **incidencias**, caso).
- `scripts/`: `handshake.py` (preflight), `manifest_imagenes.py`, `match_cdn.py` (SHA-256, probado 32/32), `install.py` (retirado el 2026-10-16).
- `templates/`: `AGENTS.template.md`, `README.template.md`.
- Ejemplos del caso (estado 2026-10-13), `HANDOFF.md`, `HANDSHAKE.md`, `memoria/`, `proyectos/` y `conocimiento/`.
- Integración en `direct-visual-design`, `seo-content-system` y la configuración global del mantenedor.
