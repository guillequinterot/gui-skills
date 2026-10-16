# Motores futuros (stubs, NO verificados)

Estado de todos: **`not_configured`**. No prometas capacidades. Para activar uno: (1) cumplir su checklist, (2) probarlo en un proyecto real, (3) registrar `engine-verify` con evidencia en el log y cambiar su estado aquí y en `scripts/handshake.py`.

Contrato común: todo motor recibe el **EDL neutro** (`assets/edl-schema.json`) y devuelve artefactos + `RESULT`. Traducir el EDL → formato del motor; nunca perder el copy oficial ni las reglas de marca.

## CapCut
- Vía conocida: `pyJianYingDraft` genera borradores (visto en video-shotcraft, `jianying-export.md`): pistas de video por plano, BGM/SFX separados y pistas de texto; exporta una "plate" sin subtítulos/SFX y monta tablas de planos/subtítulos/SFX.
- Limitaciones documentadas: verificado solo en **Mac + CapCut 11.2**, Windows sin verificar; CapCut cifra el borrador de forma irreversible; cerrar CapCut antes de instalar el borrador; los movimientos internos quedan "horneados". Regla de microsegundos: redondear cada borde por separado antes de restar.
- Checklist de activación: versión de CapCut instalada, ruta de drafts, probar un borrador de 1 clip + 1 texto, abrirlo en la app, registrar resultado.

## Canva
- En el entorno del usuario hay un conector Canva (tools `mcp__...canva` como generate/edit/export/resize design, upload asset). Aún no probado para video con esta skill.
- Checklist: conector autenticado, confirmar si edita video/animación o solo diseño estático; probar subida de asset + export de un Reel corto; registrar límites (duración, animaciones).

## Premiere Pro
- Rutas candidatas: exportar EDL CMX3600 / FCPXML desde el EDL neutro (importable), o scripting ExtendScript/UXP (ver skill `adobe-suite` del usuario).
- Checklist: versión de Premiere, método de importación, probar una secuencia de 3 clips con 1 texto y 1 transición; verificar que el color/velocidad se conservan.

## After Effects
- Ruta candidata: JSX (ExtendScript) para crear composiciones, capas de texto, keyframes y exportar por Media Encoder/aerender (skill `adobe-suite`, MCP Illustrator/Adobe si aplica).
- Checklist: aerender disponible, plantilla de comp, mapeo de easing cúbico a keyframes de influencia/velocidad, probar una comp de 5 s.

## Cómo añadir un motor (procedimiento)
1. Crear `references/engine-<nombre>.md` (instalación, flujo, trampas, render/export).
2. Añadir sonda en `scripts/handshake.py` (`future_engines.<nombre>`).
3. Extender `scripts/export_agent.py` (`--engine <nombre>`) y `assets/agent-template.md`.
4. Probar con un proyecto real → `log_update.py --kind engine-add`, luego `engine-verify`.
5. Actualizar la tabla de motores en `SKILL.md` y el `HANDSHAKE.md` de la skill (si el usuario usa Obsidian, también su matriz multiplataforma).
