"""Shared fixtures for the gui-skills tool tests (stdlib only).

Everything runs in a temp dir: a bare "remote", clones of it, and an isolated GUI_SKILLS_HOME. The real
clone, the real GitHub and the real credential helpers are never touched.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS = REPO_ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import check_update  # noqa: E402  (run_proc: temp-file output + process-tree kill, so a hung git can never hang the suite)
PY = sys.executable
ALIAS = "tester"


def forward(p) -> str:
    return str(p).replace("\\", "/")


class Sandbox(unittest.TestCase):
    """Base class: temp dir, isolated environment, helpers to build remote + clones."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="gui-skills-test-")
        self.addCleanup(self._cleanup)
        self.tmp = Path(self._tmp.name)
        self.home = self.tmp / "home"
        self.home.mkdir()
        (self.home / "config.json").write_text(json.dumps({"alias": ALIAS}), encoding="utf-8")
        (self.home / "private-terms.txt").write_text("ClienteSecreto\n", encoding="utf-8")
        gitconfig = self.tmp / "gitconfig"
        gitconfig.write_text("", encoding="utf-8")
        self.env = dict(os.environ)
        for key in ("GH_TOKEN", "GITHUB_TOKEN", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(key, None)
        self.env.update(
            GUI_SKILLS_HOME=str(self.home),
            GIT_CONFIG_GLOBAL=str(gitconfig),
            GIT_CONFIG_NOSYSTEM="1",
            GIT_TERMINAL_PROMPT="0",
            GCM_INTERACTIVE="never",
            GUI_SKILLS_NO_GH="1",
            GUI_SKILLS_API_URL="http://127.0.0.1:9",  # nothing listens: no test can reach the real API
            LC_ALL="C",
        )
        self.remote = self.tmp / "remote.git"
        self._seed()

    def _cleanup(self):
        def onerror(func, path, _exc):
            try:
                os.chmod(path, 0o700)
                func(path)
            except OSError:
                pass
        shutil.rmtree(self.tmp, onerror=onerror)
        try:
            self._tmp.cleanup()
        except OSError:
            pass

    # ------------------------------------------------------------------ git helpers
    def git(self, cwd, *args, check=True, env=None):
        rc, out, err = check_update.run_proc(["git", "-C", str(cwd), *args], 120, env=env or self.env)
        if check and rc != 0:
            raise AssertionError(f"git {' '.join(args)} falló en {cwd}: {err or out}")
        return out.strip()

    def run_tool(self, script, *args, env=None, cwd=None):
        """Run tools/<script> from the real repo. Returns (returncode, stdout, stderr)."""
        rc, out, err = check_update.run_proc([PY, "-B", str(TOOLS / script), *args], 180, env=env or self.env,
                                             cwd=str(cwd or self.tmp))
        if rc is None:
            raise AssertionError(f"{script} {' '.join(args)} no terminó en 180 s")
        return rc, out, err

    def _seed(self):
        """Bare remote + one seed commit that carries the real tools, hook and a demo skill."""
        self.git(self.tmp, "init", "-q", "--bare", "-b", "main", forward(self.remote))
        seed = self.tmp / "seed"
        seed.mkdir()
        self.git(seed, "init", "-q", "-b", "main")
        self.git(seed, "config", "user.name", "seed")
        self.git(seed, "config", "user.email", "seed@gui-skills.local")
        self.git(seed, "config", "core.autocrlf", "false")
        shutil.copytree(TOOLS, seed / "tools", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(REPO_ROOT / ".githooks", seed / ".githooks")
        shutil.copytree(REPO_ROOT / "templates", seed / "templates")
        skill = seed / "skills" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# demo\n\ntexto base\n", encoding="utf-8")
        handoff = (REPO_ROOT / "templates" / "HANDOFF.md").read_text(encoding="utf-8").replace("\r\n", "\n")
        (skill / "HANDOFF.md").write_bytes(handoff.encode("utf-8"))  # LF, whatever the platform
        (seed / "README.md").write_text("# demo repo\n", encoding="utf-8")
        (seed / "shared").mkdir()
        (seed / "shared" / "nota.md").write_text("nota\n", encoding="utf-8")
        self.git(seed, "add", "-A")
        self.git(seed, "commit", "-q", "-m", "semilla")
        self.git(seed, "remote", "add", "origin", forward(self.remote))
        self.git(seed, "push", "-q", "origin", "main")

    def clone(self, name="clon") -> Path:
        dest = self.tmp / name
        self.git(self.tmp, "clone", "-q", forward(self.remote), forward(dest))
        self.git(dest, "config", "user.name", ALIAS)
        self.git(dest, "config", "user.email", f"{ALIAS}@gui-skills.local")
        self.git(dest, "config", "core.autocrlf", "false")
        self.git(dest, "config", "core.hooksPath", ".githooks")
        self.git(dest, "config", "credential.helper", "")
        return dest

    def push_from_other(self, rel="skills/demo/SKILL.md", text="\ncambio de otra persona\n", name="otra") -> str:
        """Commit + push to main from a second clone; returns the new commit id."""
        other = self.tmp / name
        if not other.exists():
            other = self.clone(name)
        else:
            self.git(other, "pull", "-q", "--ff-only")
        path = other / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        self.git(other, "add", "-A")
        self.git(other, "commit", "-q", "-m", "cambio remoto")
        self.git(other, "push", "-q", "origin", "main")
        return self.git(other, "rev-parse", "HEAD")

    def edit(self, clone: Path, rel="skills/demo/HANDOFF.md", text="\nlínea nueva\n") -> None:
        path = clone / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def remote_branches(self):
        out = self.git(self.remote, "for-each-ref", "--format=%(refname:short)", "refs/heads/")
        return [l for l in out.splitlines() if l]

    def head(self, repo):
        return self.git(repo, "rev-parse", "HEAD")

    def branch(self, repo):
        return self.git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    def status(self, repo):
        return self.git(repo, "status", "--porcelain")


class MockGitHub:
    """Tiny local stand-in for the GitHub REST API (only the endpoints publish_job.py uses)."""

    def __init__(self, bare: Path, owner="fake", name="repo", pr_status=201, merge_status=200, existing_pr=False):
        self.requests = []  # (method, path, headers, json body)
        self.bare, self.owner, self.name = bare, owner, name
        self.pr_status, self.merge_status, self.existing_pr = pr_status, merge_status, existing_pr
        self.branch = None
        mock = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _read(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length).decode("utf-8") if length else ""
                return json.loads(raw) if raw else None

            def _send(self, status, payload=None):
                data = json.dumps(payload if payload is not None else {}).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def _handle(self, method):
                body = self._read()
                mock.requests.append((method, self.path, dict(self.headers), body))
                base = f"/repos/{mock.owner}/{mock.name}"
                url = f"https://github.com/{mock.owner}/{mock.name}/pull/7"
                if method == "POST" and self.path == f"{base}/pulls":
                    mock.branch = body.get("head")
                    if mock.pr_status == 201:
                        return self._send(201, {"html_url": url, "number": 7})
                    if mock.pr_status == 422:
                        return self._send(422, {"message": "Validation Failed: A pull request already exists"})
                    return self._send(mock.pr_status, {"message": "nope"})
                if method == "GET" and self.path.startswith(f"{base}/pulls?"):
                    return self._send(200, [{"html_url": url, "number": 7}] if mock.existing_pr else [])
                if method == "PUT" and self.path == f"{base}/pulls/7/merge":
                    if mock.merge_status == 200:  # fast-forward main to the branch, like a merge would
                        subprocess.run(["git", "--git-dir", str(mock.bare), "update-ref", "refs/heads/main",
                                        f"refs/heads/{mock.branch}"], check=True)
                        return self._send(200, {"merged": True})
                    return self._send(mock.merge_status, {"message": "Not allowed"})
                if method == "DELETE" and self.path == f"{base}/git/refs/heads/{mock.branch}":
                    subprocess.run(["git", "--git-dir", str(mock.bare), "update-ref", "-d", f"refs/heads/{mock.branch}"])
                    return self._send(204)
                return self._send(404, {"message": "no mock"})

            def do_GET(self):
                self._handle("GET")

            def do_POST(self):
                self._handle("POST")

            def do_PUT(self):
                self._handle("PUT")

            def do_DELETE(self):
                self._handle("DELETE")

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        return False

    def calls(self, method):
        return [r for r in self.requests if r[0] == method]
