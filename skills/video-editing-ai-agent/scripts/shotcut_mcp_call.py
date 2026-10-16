#!/usr/bin/env python
"""Cliente mínimo stdio para shotcut-mcp (para lotes grandes sin pegar JSON en el chat).

Uso como librería:
    from shotcut_mcp_call import Shotcut
    sc = Shotcut()
    info = sc.call("inspect_project", {"path": PROJ})
    sc.call("edit_project", {"project_path": PROJ, "expected_revision": info["revision"], "operations": [...]})
    sc.close()
Variables: SHOTCUT_MCP_SERVER (ruta de shotcut_mcp_server.py) y SHOTCUT_*_PATH (por defecto rutas de Shotcut en %LOCALAPPDATA%).
Reglas: nunca usar force; no llamar start_render sin petición explícita del usuario.
"""
import json, os, subprocess, sys

DEFAULT_SERVER = os.path.join(os.path.expanduser("~"), ".claude", "mcp-servers", "shotcut-mcp", "scripts", "shotcut_mcp_server.py")
SC = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Shotcut")


class Shotcut:
    def __init__(self, server=None):
        env = dict(os.environ)
        env.setdefault("SHOTCUT_PATH", os.path.join(SC, "shotcut.exe"))
        env.setdefault("SHOTCUT_MELT_PATH", os.path.join(SC, "melt.exe"))
        env.setdefault("SHOTCUT_FFMPEG_PATH", os.path.join(SC, "ffmpeg.exe"))
        env.setdefault("SHOTCUT_FFPROBE_PATH", os.path.join(SC, "ffprobe.exe"))
        self.p = subprocess.Popen([sys.executable, server or os.environ.get("SHOTCUT_MCP_SERVER", DEFAULT_SERVER)],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=env)
        self._id = 0
        self._rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "video-editing-ai-agent", "version": "1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def _rpc(self, method, params=None):
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError("shotcut-mcp cerró la conexión")
            r = json.loads(line)
            if r.get("id") == self._id:
                return r

    def call(self, name, args):
        r = self._rpc("tools/call", {"name": name, "arguments": args})
        if "error" in r:
            raise RuntimeError(json.dumps(r["error"]))
        res = r["result"]
        text = res["content"][0]["text"] if res.get("content") else "{}"
        if res.get("isError"):
            raise RuntimeError("TOOL ERROR: " + text[:1500])
        try:
            return json.loads(text)
        except Exception:
            return {"raw": text}

    def close(self):
        try:
            self.p.terminate()
        except Exception:
            pass
