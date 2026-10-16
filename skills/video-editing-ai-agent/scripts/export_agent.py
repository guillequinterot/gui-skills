#!/usr/bin/env python
"""Exporta el agente editor de video a un proyecto para que arranque ya instruido.

Uso: python export_agent.py --project D:/ruta/Proyecto [--engine shotcut|ffmpeg|hyperframes] [--brand "Marca"] [--copy-source URL_O_RUTA] [--force]
Crea en el proyecto:
  .claude/agents/video-editor.md   subagente (usa la skill video-editing-ai-agent)
  video-handoff.md                 traspaso (si no existe)
  handshake.json                   capacidades del entorno
No sobrescribe archivos existentes salvo --force. Los agentes nuevos pueden requerir reiniciar la sesión.
"""
import argparse, datetime, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fill(text, mapping):
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def write(path, content, force):
    if os.path.exists(path) and not force:
        print("existe, no se sobrescribe:", path)
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("creado:", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--engine", default="shotcut", choices=["shotcut", "ffmpeg", "hyperframes"])
    ap.add_argument("--brand", default="")
    ap.add_argument("--copy-source", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    proj = os.path.abspath(a.project)
    m = {"PROJECT": proj, "ENGINE": a.engine, "BRAND": a.brand or "(definir)", "COPY_SOURCE": a.copy_source or "(definir)",
         "SKILL_DIR": ROOT, "DATE": datetime.date.today().isoformat()}
    tpl = open(os.path.join(ROOT, "assets", "agent-template.md"), encoding="utf-8").read()
    write(os.path.join(proj, ".claude", "agents", "video-editor.md"), fill(tpl, m), a.force)
    ho = open(os.path.join(ROOT, "assets", "handoff-template.md"), encoding="utf-8").read()
    write(os.path.join(proj, "video-handoff.md"), fill(ho, m), a.force)
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "handshake.py"), "--project", proj], stdout=subprocess.DEVNULL)
    print("handshake.json:", os.path.join(proj, "handshake.json"))


if __name__ == "__main__":
    main()
