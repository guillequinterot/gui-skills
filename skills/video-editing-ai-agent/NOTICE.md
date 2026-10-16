# NOTICE — atribuciones

Esta skill incorpora ideas, reglas y patrones de diseño de otros proyectos. El código de esta carpeta está escrito para el stack propio (Shotcut/MLT + ffmpeg en Windows); se atribuyen las fuentes de inspiración.

## browser-use/video-use — MIT
Repositorio: https://github.com/browser-use/video-use (leído en crudo el 2026-09-21).
Adaptado en v1.1.0: proceso "preguntar → confirmar → ejecutar → iterar → persistir", las 12 reglas duras de corrección, oficio de cortes (padding 30–200 ms, silencios ≥400 ms), transcripción empaquetada por frases (`pack_transcripts.py`), vista de tira de fotogramas + forma de onda (`timeline_view.py`), autoexamen de la salida con tope de 3 pasadas (`self_eval.py`), presets de color y auto-grade acotado (`grade.py`), loudnorm en dos pasadas con `-c:v copy` (`loudnorm_audio.py`), formato EDL (`edl_to_shotcut.py`), briefs para subagentes y memoria por sesión.

```
MIT License
Copyright (c) 2026 Browser Use
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
```

## Otras fuentes analizadas (solo ideas; ver `references/fuentes-analizadas.md`)
Bomx/super-video-maker-skill (sin licencia declarada: no se copió código), video-db/skills, awesome-genmedia, GoogleCloudPlatform/vertex-ai-creative-studio, 6missedcalls/video-editing-skill, AKCodez/promo-video-skill, ZeroPointRepo/youtube-skills, Vincentwei1021/video-shotcraft, VideoZero/skills, bradautomates/claude-video, wilwaldon/Claude-Code-Video-Toolkit.

## shotcut-mcp — MIT
https://github.com/matrodrigs/shotcut-mcp — servidor MCP usado como motor de Shotcut (no se redistribuye aquí).

## HyperFrames (HeyGen) — Apache-2.0
https://github.com/heygen-com/hyperframes (leído en crudo el 2026-10-15). Se adaptaron **reglas y parámetros** (reescritos, sin copiar código ni texto) de sus skills `motion-doctrine`, `cut-the-curve`, `embedded-captions` y `talking-head-recut` en `references/motion-doctrine.md` y `references/captions-subtitles.md`. Copyright de HeyGen / colaboradores de HyperFrames. Si se redistribuye código de ese proyecto, hay que conservar su LICENSE y avisos (Apache-2.0, https://www.apache.org/licenses/LICENSE-2.0).

## Silero VAD — MIT
https://github.com/snakers4/silero-vad (Copyright (c) 2020-present Silero Team). `scripts/vad_segments.py` usa el modelo `silero_vad_v6.onnx` que **ya incluye faster-whisper** (MIT); no se redistribuye aquí. Valores por defecto de detección tomados de la documentación de LiveKit Agents (Apache-2.0) como referencia.

### Ampliación 2026-10-16 — otras skills de HyperFrames leídas (Apache-2.0, commit `490ecaf`)
Además de las cuatro skills citadas arriba, se leyeron y **reescribieron** (sin copiar código ni texto) ideas y parámetros de: `hyperframes` (router y `references/{brief-contract,intent-interview,pitch-round,production-loop,review-loop,storyboard-format,subagent-dispatch}`), `motion-graphics` (`agents/{director,builder,finalize}`, `references/{motion-vocabulary,shot-plan-ir,builder-contract}`), `general-video`, `faceless-explainer` (`references/{story-design,motion-language,cut-catalog}`), `hyperframes-core` (`SKILL.md`, `references/{creator-editing-recipes,determinism-rules,variables-and-media}`), `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-audio` y `hyperframes-creative` (`references/{motion-principles,story-spine,beat-direction,narration,video-composition}`), en `references/production-workflow.md`, `references/story-design.md`, `references/motion-doctrine.md` §8–§12, `references/engine-hyperframes.md`, `references/audio-mix.md` (carve), `references/captions-subtitles.md` y los scripts `scripts/carve_music.py` y `scripts/hf_captions.py` (implementaciones propias). Copyright de HeyGen / colaboradores de HyperFrames. No se instaló ninguna skill de HyperFrames en `~/.claude`. `media-use` depende de la CLI de HeyGen con inicio de sesión y créditos: **no se adopta**. Del resto de skills (`figma`, `pr-to-video`, `product-launch-video`, `slideshow`, `music-to-video`, `remotion-to-hyperframes`, `hyperframes-registry`, `hyperframes-studio`, `hyperframes-cli`) solo se conoce la descripción.
