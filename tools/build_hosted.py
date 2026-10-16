#!/usr/bin/env python3
"""Regenera skills/seo-content-system-web-hosted/ desde skills/seo-content-system/.

La versión "hosted" es un port de la skill para entornos sin sistema de archivos ni MCP (un Project de
Claude.ai o un Custom GPT / Project de ChatGPT). Se GENERA; nunca se edita a mano.

  python tools/build_hosted.py            # regenera la carpeta
  python tools/build_hosted.py --check    # no escribe; sale con 1 si lo guardado está desfasado

Cómo se deriva (determinista: misma entrada, misma salida; sin fechas ni rutas del equipo):
  * knowledge/NN-*.md  = consolidación de archivos de la skill según
    skills/seo-content-system/hosted-src/knowledge-map.json (sin frontmatter, una sección
    "Fuente original" por archivo).
  * 00-instrucciones-del-proyecto.md, 10-memoria-sin-obsidian.md y README-INSTALACION.md salen de las
    plantillas escritas a mano en hosted-src/ (se rellenan los marcadores {{...}}).
  * Cada archivo generado lleva una cabecera que lo declara generado y la huella (SHA-256) de SUS entradas,
    de modo que un cambio en la skill solo toca los archivos que dependen de él.
  * HANDOFF.md y HANDSHAKE.md de la carpeta de salida SÍ son manuales y no se tocan ni se borran.

Solo biblioteca estándar (Python >= 3.9). Salida siempre UTF-8 con saltos de línea LF.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

SKILL_NAME = "seo-content-system"
HOSTED_NAME = "seo-content-system-web-hosted"
MANUAL_FILES = {"HANDOFF.md", "HANDSHAKE.md"}  # escritos a mano; fuera de la regeneración
TEMPLATES = {
    # nombre en hosted-src/  ->  ruta de salida
    "00-instrucciones-del-proyecto.md": "00-instrucciones-del-proyecto.md",
    "10-memoria-sin-obsidian.md": "10-memoria-sin-obsidian.md",
    "README-INSTALACION.md": "README-INSTALACION.md",
}
FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*\r?\n", re.DOTALL)
PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


class BuildError(Exception):
    pass


def read_text(path: Path) -> str:
    """Lee UTF-8 y normaliza CRLF -> LF y BOM."""
    text = path.read_text(encoding="utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def body_of(path: Path) -> str:
    return strip_frontmatter(read_text(path)).strip("\n")


def source_hash(skill_dir: Path, inputs: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(set(inputs), key=lambda p: p.relative_to(skill_dir).as_posix()):
        digest.update(path.relative_to(skill_dir).as_posix().encode("utf-8") + b"\0")
        digest.update(read_text(path).encode("utf-8") + b"\0")
    return digest.hexdigest()[:12]


def digest_of(*chunks: str) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk.encode("utf-8") + b"\0")
    return digest.hexdigest()[:12]


def make_header(version: str, file_hash: str) -> str:
    return (
        f"<!-- GENERADO por tools/build_hosted.py desde skills/{SKILL_NAME} (v{version}, huella {file_hash}). "
        f"NO EDITAR A MANO: cambia la skill o hosted-src/ y regenera con `python tools/build_hosted.py`. -->"
    )


def fill(template: str, values: dict[str, str], where: str) -> str:
    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise BuildError(f"{where}: marcador desconocido {{{{{key}}}}}")
        return values[key]

    return PLACEHOLDER.sub(repl, template)


def classify_references(skill_dir: Path, knowledge: list[dict], excluded: list[dict]) -> None:
    """Toda referencia/plantilla de la skill debe estar incluida o excluida a propósito."""
    declared = {s for k in knowledge for s in k["sources"]} | {e["source"] for e in excluded}
    existing = {
        p.relative_to(skill_dir).as_posix()
        for pattern in ("references/*.md", "assets/templates/*.md")
        for p in skill_dir.glob(pattern)
    }
    missing = sorted(declared - existing)
    if missing:
        raise BuildError("knowledge-map.json cita archivos que no existen: " + ", ".join(missing))
    unclassified = sorted(existing - declared)
    if unclassified:
        raise BuildError(
            "archivos de la skill sin clasificar en hosted-src/knowledge-map.json (añádelos a un documento "
            "de 'knowledge' o a 'excluidos'): " + ", ".join(unclassified)
        )


def build(repo: Path) -> dict[str, str]:
    skill_dir = repo / "skills" / SKILL_NAME
    src_dir = skill_dir / "hosted-src"
    if not skill_dir.is_dir() or not src_dir.is_dir():
        raise BuildError(f"no encuentro {skill_dir} o su carpeta hosted-src/")

    mapping = json.loads(read_text(src_dir / "knowledge-map.json"))
    knowledge = mapping["knowledge"]
    excluded = mapping.get("excluidos", [])
    classify_references(skill_dir, knowledge, excluded)

    manifest = json.loads(read_text(skill_dir / "assets" / "system-manifest.json"))
    version = str(manifest.get("version", "0"))

    inputs: list[Path] = [src_dir / "knowledge-map.json", skill_dir / "assets" / "system-manifest.json"]
    inputs += [src_dir / name for name in TEMPLATES]
    for entry in knowledge:
        inputs += [skill_dir / s for s in entry["sources"]]
    short_hash = source_hash(skill_dir, inputs)

    outputs: dict[str, str] = {}

    # --- knowledge/ (consolidación mecánica)
    knowledge_lines: list[str] = []
    for entry in knowledge:
        entry_hash = digest_of(
            entry["title"], entry.get("intro", ""), entry["layout"],
            *[f"{s}\n{read_text(skill_dir / s)}" for s in entry["sources"]],
        )
        parts = [make_header(version, entry_hash), "", f"# {entry['title']}", ""]
        if entry["layout"] == "single":
            if len(entry["sources"]) != 1:
                raise BuildError(f"{entry['name']}: layout 'single' admite una sola fuente")
            parts.append(body_of(skill_dir / entry["sources"][0]))
        elif entry["layout"] == "sections":
            if entry.get("intro"):
                parts += [entry["intro"], ""]
            for source in entry["sources"]:
                parts += ["---", "", f"## Fuente original: `{Path(source).name}`", "", body_of(skill_dir / source), ""]
        else:
            raise BuildError(f"{entry['name']}: layout desconocido {entry['layout']!r}")
        outputs[f"knowledge/{entry['name']}"] = "\n".join(parts).rstrip("\n") + "\n"
        knowledge_lines.append(f"  - `knowledge/{entry['name']}` — {entry['title']}")

    # --- plantillas escritas a mano
    values = {
        "SKILL_VERSION": version,
        "SOURCE_HASH": short_hash,
        "N_KNOWLEDGE": str(len(knowledge)),
        "N_SOURCES": str(sum(len(k["sources"]) for k in knowledge)),
        "KNOWLEDGE_LIST": "\n".join(knowledge_lines),
    }
    for template_name, out_name in TEMPLATES.items():
        template = read_text(src_dir / template_name)
        file_hash = digest_of(template, *[f"{k}={v}" for k, v in sorted(values.items())])
        filled = fill(template, {**values, "GENERATED_HEADER": make_header(version, file_hash)},
                      f"hosted-src/{template_name}")
        outputs[out_name] = filled.rstrip("\n") + "\n"

    # --- coherencia: todo `NN-nombre.md` citado en los textos debe existir en la salida
    known = {Path(p).name for p in outputs}
    for out_name, text in outputs.items():
        if out_name.startswith("knowledge/"):
            continue
        for ref in sorted(set(re.findall(r"`(\d\d-[a-z0-9-]+\.md)`", text))):
            if ref not in known:
                raise BuildError(f"{out_name} cita `{ref}`, que no se genera")
    return outputs


def current_files(out_dir: Path) -> dict[str, bytes]:
    found: dict[str, bytes] = {}
    if out_dir.is_dir():
        for path in sorted(out_dir.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                rel = path.relative_to(out_dir).as_posix()
                if rel in MANUAL_FILES:
                    continue
                # a Windows checkout may have turned LF into CRLF (core.autocrlf): compare by content
                found[rel] = path.read_bytes().replace(b"\r\n", b"\n")
    return found


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        description=f"Regenera skills/{HOSTED_NAME}/ desde skills/{SKILL_NAME}/ (determinista)."
    )
    parser.add_argument("--check", action="store_true", help="no escribe: sale con 1 si la salida guardada está desfasada")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="raíz del repo (por defecto, la de este script)")
    parser.add_argument("--out", type=Path, help="carpeta de salida (por defecto skills/%s)" % HOSTED_NAME)
    args = parser.parse_args()

    repo = args.repo.resolve()
    out_dir = (args.out or (repo / "skills" / HOSTED_NAME)).resolve()
    try:
        outputs = build(repo)
    except (BuildError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    expected = {rel: text.encode("utf-8") for rel, text in outputs.items()}
    present = current_files(out_dir)
    missing = sorted(set(expected) - set(present))
    extra = sorted(set(present) - set(expected))
    changed = sorted(rel for rel in expected if rel in present and present[rel] != expected[rel])

    if args.check:
        if not (missing or extra or changed):
            print(f"AL DIA: {len(expected)} archivos de {out_dir.name} coinciden con la skill.")
            return 0
        print(f"DESFASADA: {out_dir} no coincide con la skill. Regenera con `python tools/build_hosted.py`.")
        for label, items in (("faltan", missing), ("distintos", changed), ("sobran", extra)):
            for rel in items:
                print(f"  {label}: {rel}")
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    for rel, data in expected.items():
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if present.get(rel) != data:
            target.write_bytes(data)
    for rel in extra:
        (out_dir / rel).unlink()
    # carpetas vacías tras borrar
    for path in sorted(out_dir.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    print(f"Generado {out_dir} — {len(expected)} archivos ({len(changed) + len(missing)} escritos, {len(extra)} borrados).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
