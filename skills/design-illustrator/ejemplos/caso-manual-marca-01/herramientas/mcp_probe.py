import json, sys, urllib.request

URL = "http://localhost:18412/v1/mcp"
import os
# El token NUNCA va en el repo ni en la skill: variable de entorno o archivo local fuera del repo (panel «MCP y herramientas» de Illustrator).
TOKEN = os.environ.get("ILLUSTRATOR_MCP_TOKEN") or open(os.path.expanduser("~/.gui-skills/illustrator-mcp-token.txt")).read().strip()
HEAD = {
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
session = None


def rpc(method, params=None, id_=1, notify=False):
    global session
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if not notify:
        body["id"] = id_
    h = dict(HEAD)
    if session:
        h["Mcp-Session-Id"] = session
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=40) as r:
        sid = r.headers.get("Mcp-Session-Id")
        if sid:
            session = sid
        ctype = r.headers.get("Content-Type", "")
        if notify:
            return None
        if "event-stream" in ctype:
            for line in r:
                line = line.decode("utf-8", "replace").strip()
                if line.startswith("data:"):
                    return json.loads(line[5:].strip())
            return None
        raw = r.read().decode("utf-8", "replace")
    if not raw.strip():
        return None
    return json.loads(raw)


if __name__ == "__main__":
    init = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "claude-code", "version": "1"}})
    print(json.dumps(init, ensure_ascii=False)[:600])
    rpc("notifications/initialized", notify=True)
    tl = rpc("tools/list", {}, id_=2)
    tools = tl["result"]["tools"]
    print(len(tools), "tools")
    for t in tools:
        print("-", t["name"], ":", (t.get("description") or "")[:160].replace("\n", " "))
