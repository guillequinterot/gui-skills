#!/usr/bin/env python3
"""Recopila cambios de las fuentes SEO configuradas y escribe un informe fechado.

Sin bóveda de Obsidian el informe va a ``memoria/novedades/`` de la skill; con bóveda, a su
``02_Investigacion/Novedades/``. El estado (hashes) se guarda fuera del repo cuando no hay bóveda.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any

from paths import resolve_memory, skill_root


USER_AGENT = "SEOContentSystem/1.0 (+local research collector)"
MAX_BYTES = 4_000_000


def fetch(url: str, timeout: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/xml,text/xml,text/html,*/*"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_BYTES:
            raise ValueError(f"Respuesta demasiado grande: {length} bytes")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Respuesta supera el límite permitido")
        return data


def clean_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def node_text(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def first_node(*nodes: ET.Element | None) -> ET.Element | None:
    for node in nodes:
        if node is not None:
            return node
    return None


def parse_feed(data: bytes, limit: int) -> list[dict[str, str]]:
    root = ET.fromstring(data)
    items: list[dict[str, str]] = []
    if root.tag.endswith("rss") or root.find("channel") is not None:
        for item in root.findall(".//item")[:limit]:
            items.append(
                {
                    "title": node_text(item.find("title")),
                    "url": node_text(item.find("link")),
                    "date": node_text(item.find("pubDate")),
                    "summary": clean_html(node_text(item.find("description")))[:500],
                }
            )
    else:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall(".//atom:entry", ns)
        if not entries:
            entries = root.findall(".//entry")
        for entry in entries[:limit]:
            link = first_node(entry.find("atom:link", ns), entry.find("link"))
            href = link.attrib.get("href", "") if link is not None else ""
            summary = first_node(entry.find("atom:summary", ns), entry.find("summary"))
            if summary is None:
                summary = first_node(entry.find("atom:content", ns), entry.find("content"))
            items.append(
                {
                    "title": node_text(first_node(entry.find("atom:title", ns), entry.find("title"))),
                    "url": href,
                    "date": node_text(first_node(entry.find("atom:updated", ns), entry.find("updated"))),
                    "summary": clean_html(node_text(summary))[:500],
                }
            )
    return items


def parse_page(data: bytes, url: str) -> list[dict[str, str]]:
    text = data.decode("utf-8", errors="replace")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    description_match = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return [
        {
            "title": clean_html(title_match.group(1)) if title_match else url,
            "url": url,
            "date": "",
            "summary": clean_html(description_match.group(1))[:500] if description_match else "La página cambió; requiere revisión manual.",
        }
    ]


def digest(items: list[dict[str, str]]) -> str:
    payload = json.dumps(items, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def render_report(now: datetime, changes: list[dict[str, Any]], errors: list[dict[str, str]], in_vault: bool = False) -> str:
    lines = [
        "---",
        "type: research-update",
        "status: candidate",
        f"created: {now.date().isoformat()}",
        f"updated: {now.date().isoformat()}",
        "confidence: low",
        "topics:",
        "  - seo",
        "  - novedades",
        "---",
        "",
        f"# Actualización SEO — {now.date().isoformat()}",
        "",
        "> Recopilación automática. Verificar las fuentes completas antes de cambiar una regla o una página.",
        "",
        "## Fuentes con cambios",
        "",
    ]
    if not changes:
        lines.append("No se detectaron cambios respecto al estado anterior.")
    for source in changes:
        lines.extend([f"### {source['name']}", "", f"Fuente: {source['url']}", ""])
        for item in source["items"]:
            title = item.get("title") or "Sin título"
            url = item.get("url") or source["url"]
            date_text = f" — {item['date']}" if item.get("date") else ""
            lines.append(f"- [{title}]({url}){date_text}")
            if item.get("summary"):
                lines.append(f"  - {item['summary']}")
        lines.extend(["", "**Revisión requerida**", "", "- ¿Qué cambió realmente?", "- ¿A qué sitios o funciones aplica?", "- ¿Modifica una regla existente o solo añade contexto?", ""])
    if errors:
        lines.extend(["## Errores de recopilación", ""])
        for error in errors:
            lines.append(f"- {error['name']}: {error['error']}")
    relaciones = (["- [[Protocolo de actualización]]", "- [[Registro maestro de fuentes]]"] if in_vault
                  else ["- `references/update-governance-and-research.md` (protocolo de actualización)",
                        "- `references/official-source-register.md` (registro de fuentes)"])
    lines.extend(["", "## Decisión", "", "- Estado: pendiente", "- Responsable:", "- Fecha de revisión:", "", "## Relaciones", "", *relaciones, ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", help="ruta de la bóveda de Obsidian (opcional)")
    parser.add_argument("--sources", type=Path)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--force-report", action="store_true")
    args = parser.parse_args()

    memory = resolve_memory(args.vault)
    sources_path = args.sources or (skill_root() / "assets" / "official-sources.json")
    sources = load_json(sources_path, [])
    if not isinstance(sources, list) or not sources:
        raise SystemExit(f"No hay fuentes válidas en {sources_path}")

    state_path = memory.state_file
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state = load_json(state_path, {})
    changes: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for source in sources:
        name = source["name"]
        url = source["url"]
        try:
            data = fetch(url, args.timeout)
            items = parse_feed(data, args.limit) if source.get("format", "feed") == "feed" else parse_page(data, url)
            current = digest(items)
            if args.force_report or state.get(url) != current:
                changes.append({"name": name, "url": url, "items": items})
            state[url] = current
        except (OSError, ValueError, ET.ParseError, urllib.error.URLError) as exc:
            errors.append({"name": name, "error": str(exc)})

    now = datetime.now(timezone.utc)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not changes and not errors and not args.force_report:
        print("Sin cambios detectados.")
        return 0

    folder = memory.news
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now.date().isoformat()}-actualizacion-seo.md"
    if path.exists():
        path = folder / f"{now.strftime('%Y-%m-%d-%H%M%S')}-actualizacion-seo.md"
    path.write_text(render_report(now, changes, errors, memory.is_vault), encoding="utf-8")
    print(path)
    print(f"({memory.describe()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
