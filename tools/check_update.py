#!/usr/bin/env python3
"""Compare the local gui-skills clone with GitHub.

First word of the output is the status token:
AL_DIA | ATRASADA <n> | CAMBIOS_LOCALES | SIN_RED | SIN_CREDENCIAL
Exit code is 0 for every status (usage errors: 2). With --hook it never fails.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gui_common  # noqa: E402

FETCH_TIMEOUT = 8
HOOK_INTERVAL = 6 * 3600
AUTH_RE = re.compile(
    r"\b40[13]\b|authentication failed|could not read (username|password)|terminal prompts disabled|"
    r"permission denied|invalid username or password|repository not found|access denied|"
    r"bad credentials|requested url returned error: 40[13]", re.I)


def git_env() -> dict:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GCM_INTERACTIVE"] = "never"
    env.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o ConnectTimeout=8")
    env["LC_ALL"] = "C"
    return env


def run_git(repo: Path, args: list, timeout: float = 20):
    """Return (returncode, stdout, stderr); returncode None on timeout. Kills the whole process tree."""
    cmd = ["git", "-C", str(repo), *args]
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = 0x00000200  # CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.DEVNULL, env=git_env(), **kwargs)
    except OSError as exc:
        return 127, "", str(exc)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        else:
            try:
                import signal
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                proc.kill()
        for pipe in (proc.stdout, proc.stderr):
            try:
                pipe.close()
            except Exception:
                pass
        try:
            proc.wait(timeout=2)
        except Exception:
            pass
        return None, "", "timeout"
    return proc.returncode, out.decode("utf-8", "replace"), err.decode("utf-8", "replace")


def last_check_path() -> Path:
    return gui_common.gui_home() / "last_check.json"


def read_last_check(repo: Path):
    try:
        data = json.loads(last_check_path().read_text(encoding="utf-8-sig"))
        if data.get("repo") == str(repo):
            return float(data["epoch"])
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def write_last_check(repo: Path, status: str) -> None:
    try:
        path = last_check_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "repo": str(repo), "epoch": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "estado": status,
        }, indent=2), encoding="utf-8")
    except OSError:
        pass


def upstream_ref(repo: Path):
    rc, out, _ = run_git(repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    if rc == 0 and out.strip():
        return out.strip()
    rc, branch, _ = run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    for cand in (f"origin/{branch.strip()}" if rc == 0 else None, "origin/main"):
        if cand and run_git(repo, ["rev-parse", "--verify", "--quiet", cand])[0] == 0:
            return cand
    return None


def classify_fetch_error(err: str) -> str:
    return "SIN_CREDENCIAL" if AUTH_RE.search(err) else "SIN_RED"


def first_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line[:160]
    return ""


def compute(repo: Path, do_fetch: bool):
    """Return (token, n, detail dict)."""
    detail = {"fetched": False, "age_h": None}
    rc, _, err = run_git(repo, ["rev-parse", "--git-dir"])
    if rc != 0:
        return "SIN_RED", 0, {"reason": "la ruta no es un clon de git", **detail}

    rc, out, _ = run_git(repo, ["status", "--porcelain"])
    dirty = len([l for l in out.splitlines() if l.strip()]) if rc == 0 else 0

    fetch_status = None
    fetch_err = ""
    if do_fetch:
        ref = upstream_ref(repo)
        remote = ref.split("/", 1)[0] if ref else "origin"
        rc, _, err = run_git(repo, ["fetch", "--quiet", "--no-tags", remote], timeout=FETCH_TIMEOUT)
        if rc == 0:
            detail["fetched"] = True
        elif rc is None:
            fetch_status, fetch_err = "SIN_RED", f"sin respuesta de GitHub en {FETCH_TIMEOUT} s"
        else:
            fetch_status, fetch_err = classify_fetch_error(err), first_line(err)

    ref = upstream_ref(repo)
    ahead = behind = 0
    if ref:
        rc, out, _ = run_git(repo, ["rev-list", "--left-right", "--count", f"HEAD...{ref}"])
        if rc == 0 and out.split():
            ahead, behind = (int(x) for x in out.split()[:2])
    detail.update(dirty=dirty, ahead=ahead, behind=behind, fetch_err=fetch_err, fetch_status=fetch_status)

    if dirty or ahead:
        return "CAMBIOS_LOCALES", 0, detail
    if fetch_status:
        return fetch_status, 0, detail
    if not ref:
        detail["reason"] = "no hay rama remota de referencia"
        return "SIN_RED", 0, detail
    if behind:
        return "ATRASADA", behind, detail
    return "AL_DIA", 0, detail


def plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def describe(token: str, n: int, d: dict, repo: Path) -> str:
    if token == "AL_DIA":
        return "Las skills están al día con GitHub."
    if token == "ATRASADA":
        return (f"Hay {plural(n, 'cambio nuevo', 'cambios nuevos')} en GitHub. "
                f"Para actualizar: git -C \"{repo}\" pull --ff-only")
    if token == "CAMBIOS_LOCALES":
        parts = []
        if d.get("dirty"):
            parts.append(plural(d["dirty"], "archivo con cambios sin guardar en git", "archivos con cambios sin guardar en git"))
        if d.get("ahead"):
            parts.append(plural(d["ahead"], "commit sin subir", "commits sin subir"))
        msg = "El clon tiene " + " y ".join(parts) + ". No hagas pull hasta decidir si se suben (PR) o se descartan."
        if d.get("behind"):
            msg += f" Además GitHub tiene {plural(d['behind'], 'cambio nuevo', 'cambios nuevos')}."
        if d.get("fetch_status"):
            msg += " (No se pudo consultar GitHub.)"
        return msg
    if token == "SIN_CREDENCIAL":
        return ("GitHub rechazó la credencial (401/403). Se usa la copia local. "
                "Revisa la sección Credenciales del README.")
    reason = d.get("reason") or d.get("fetch_err") or "sin conexión"
    return f"No se pudo consultar GitHub ({reason}). Se usa la copia local."


def hook_line(token: str, n: int, d: dict, repo: Path, skipped_age) -> str:
    age = f" (última comprobación hace {skipped_age:.0f} h)" if skipped_age is not None else ""
    if token == "AL_DIA":
        return f"gui-skills: skills al día{age}."
    if token == "ATRASADA":
        return (f"gui-skills: hay {plural(n, 'cambio nuevo', 'cambios nuevos')} de las skills en GitHub{age}. "
                f"Avísale al usuario al empezar y ofrécele actualizar con: git -C \"{repo}\" pull --ff-only "
                "(hazlo antes de leer la skill).")
    if token == "CAMBIOS_LOCALES":
        return "gui-skills: " + describe(token, n, d, repo) + " Avísale al usuario."
    if token == "SIN_CREDENCIAL":
        return ("gui-skills: GitHub rechazó la credencial; se usa la copia local. "
                "Avísale al usuario (README, sección Credenciales).")
    if d.get("reason"):
        return f"gui-skills: no se pudo comprobar actualizaciones ({d['reason']}: {repo})."
    return "gui-skills: sin conexión con GitHub; se usa la copia local."


def main(argv=None) -> int:
    gui_common.setup_stdio()
    ap = argparse.ArgumentParser(description="Compara el clon local de gui-skills con GitHub.")
    ap.add_argument("--repo", help="ruta del clon (por defecto, repo_path de config.json o este repo)")
    ap.add_argument("--quiet", action="store_true", help="solo el token de estado")
    ap.add_argument("--hook", action="store_true", help="una linea para un hook SessionStart; nunca falla")
    args = ap.parse_args(argv)

    if args.hook:
        try:
            return run_hook(args)
        except BaseException:  # the hook must never break a session
            print("gui-skills: no se pudo comprobar si hay actualizaciones; se usa la copia local.")
            return 0

    repo = gui_common.resolve_repo(args.repo, __file__)
    token, n, d = compute(repo, do_fetch=True)
    if d.get("fetched"):
        write_last_check(repo, token)
    label = f"{token} {n}" if token == "ATRASADA" else token
    print(label if args.quiet else f"{label} - {describe(token, n, d, repo)}")
    return 0


def run_hook(args) -> int:
    repo = gui_common.resolve_repo(args.repo, __file__)
    last = read_last_check(repo)
    age = (time.time() - last) if last is not None else None
    skip = age is not None and 0 <= age < HOOK_INTERVAL
    token, n, d = compute(repo, do_fetch=not skip)
    if d.get("fetched"):
        write_last_check(repo, token)
    print(hook_line(token, n, d, repo, (age / 3600) if skip else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
