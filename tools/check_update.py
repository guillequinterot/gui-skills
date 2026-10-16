#!/usr/bin/env python3
"""Compare the local gui-skills clone with GitHub.

First word of the output is the status token:
AL_DIA | ATRASADA <n> | ACTUALIZADA <n> | CAMBIOS_LOCALES | SIN_RED | SIN_CREDENCIAL
Exit code is 0 for every status (usage errors: 2). With --hook it never fails.

--pull: when the clone is behind, clean and on main (tracking origin/main), run `git pull --ff-only`
and report ACTUALIZADA <n>. Never pulls with local changes, unpushed commits, offline or on other branches.
Whatever the status, local `aporte/*` branches with unpublished commits add a warning after the status
(on its own line, or at the end of the hook line); the first token never changes because of it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gui_common  # noqa: E402

FETCH_TIMEOUT = 8
PULL_TIMEOUT = 10
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


def _kill_tree(proc) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        try:
            import signal
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        proc.kill()
    except OSError:
        pass


def run_proc(cmd: list, timeout: float, env=None, cwd=None, stdin_text=None):
    """Return (returncode, stdout, stderr); returncode None on timeout. Kills the whole process tree.

    Output goes through temp files, not pipes: a grandchild that keeps a handle open (a detached
    `git gc`, a credential helper) can never leave us waiting for EOF, and there are no reader threads
    to deadlock when the tree is killed.
    """
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = 0x00000200  # CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    with tempfile.TemporaryFile() as fout, tempfile.TemporaryFile() as ferr, tempfile.TemporaryFile() as fin:
        if stdin_text is not None:
            fin.write(stdin_text.encode("utf-8"))
            fin.seek(0)
        try:
            proc = subprocess.Popen(cmd, stdout=fout, stderr=ferr, stdin=fin if stdin_text is not None else subprocess.DEVNULL,
                                    env=env, cwd=cwd, **kwargs)
        except OSError as exc:
            return 127, "", str(exc)
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_tree(proc)
            try:
                proc.wait(timeout=5)
            except Exception:
                pass
            return None, "", "timeout"
        fout.seek(0)
        ferr.seek(0)
        return proc.returncode, fout.read().decode("utf-8", "replace"), ferr.read().decode("utf-8", "replace")


def run_git(repo: Path, args: list, timeout: float = 20):
    """Return (returncode, stdout, stderr); returncode None on timeout."""
    return run_proc(["git", "-C", str(repo), *args], timeout, env=git_env())


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


def current_branch(repo: Path) -> str:
    rc, out, _ = run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    return out.strip() if rc == 0 else ""


def _ok(repo: Path, args: list) -> bool:
    return run_git(repo, args)[0] == 0


def pending_branches(repo: Path) -> list:
    """Local `aporte/*` branches whose commits are not on GitHub yet.

    Pending = no remote counterpart (and its changes are not already in origin/main, which covers branches
    merged on GitHub and deleted there, also squash merges) or commits ahead of its remote counterpart.
    """
    rc, out, _ = run_git(repo, ["for-each-ref", "--format=%(refname:short)", "refs/heads/aporte/"])
    if rc != 0:
        return []
    pending = []
    main_ok = _ok(repo, ["rev-parse", "--verify", "--quiet", "origin/main"])
    for name in (l.strip() for l in out.splitlines()):
        if not name:
            continue
        remote = f"refs/remotes/origin/{name}"
        if _ok(repo, ["rev-parse", "--verify", "--quiet", remote]):
            rc, cnt, _ = run_git(repo, ["rev-list", "--count", f"{remote}..refs/heads/{name}"])
            if rc == 0 and cnt.strip().isdigit() and int(cnt) > 0:
                pending.append(name)
            continue
        if not main_ok:
            pending.append(name)
            continue
        rc, cnt, _ = run_git(repo, ["rev-list", "--count", f"origin/main..refs/heads/{name}"])
        if rc == 0 and cnt.strip() == "0":
            continue  # everything it has is already in main
        rc, base, _ = run_git(repo, ["merge-base", "origin/main", f"refs/heads/{name}"])
        if rc == 0 and base.strip():
            rc, files, _ = run_git(repo, ["diff", "--name-only", base.strip(), f"refs/heads/{name}"])
            paths = [f for f in files.splitlines() if f.strip()]
            if rc == 0 and paths and _ok(repo, ["diff", "--quiet", "origin/main", f"refs/heads/{name}", "--", *paths]):
                continue  # same content already in main (squash merge)
        pending.append(name)
    return pending


def pending_warning(repo: Path, branches: list) -> str:
    if not branches:
        return ""
    return (f"hay aportes sin publicar: {', '.join(branches)}; "
            f"corre `python \"{repo.as_posix()}/tools/publish_job.py\" --reintentar`")


def pull_now(repo: Path, ref: str, behind: int, detail: dict):
    """`git pull --ff-only` when it is safe. Returns (token, n)."""
    branch = current_branch(repo)
    if branch != "main" or ref != "origin/main":
        detail["pull_error"] = (f"la rama actual es {branch or 'desconocida'} (referencia {ref}); "
                                "solo se actualiza main con origin/main")
        return "ATRASADA", behind
    rc, _, err = run_git(repo, ["pull", "--ff-only", "--quiet", "origin", "main"], timeout=PULL_TIMEOUT)
    if rc is None:
        detail["pull_error"] = f"sin respuesta de GitHub en {PULL_TIMEOUT} s"
        return "ATRASADA", behind
    if rc != 0:
        detail["pull_error"] = ("GitHub rechazó la credencial" if AUTH_RE.search(err)
                                else first_line(err) or f"git pull terminó con código {rc}")
        return "ATRASADA", behind
    rc, cnt, _ = run_git(repo, ["rev-list", "--count", "HEAD..origin/main"])
    if rc == 0 and cnt.strip() not in ("", "0"):
        detail["pull_error"] = "el pull no dejó el clon al día"
        return "ATRASADA", behind
    detail["pulled"] = True
    return "ACTUALIZADA", behind


def compute(repo: Path, do_fetch: bool, do_pull: bool = False):
    """Return (token, n, detail dict)."""
    detail = {"fetched": False, "age_h": None, "pending": [], "pulled": False, "pull_error": ""}
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
    token, n = _status(repo, ref, dirty, ahead, behind, detail, do_pull)
    detail["pending"] = pending_branches(repo)
    return token, n, detail


def _status(repo: Path, ref, dirty: int, ahead: int, behind: int, detail: dict, do_pull: bool):
    fetch_status = detail["fetch_status"]

    if dirty or ahead:
        return "CAMBIOS_LOCALES", 0
    if fetch_status:
        return fetch_status, 0
    if not ref:
        detail["reason"] = "no hay rama remota de referencia"
        return "SIN_RED", 0
    if behind:
        if do_pull:
            return pull_now(repo, ref, behind, detail)
        return "ATRASADA", behind
    return "AL_DIA", 0


def plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def describe(token: str, n: int, d: dict, repo: Path) -> str:
    if token == "AL_DIA":
        return "Las skills están al día con GitHub."
    if token == "ACTUALIZADA":
        return (f"Se descargaron {plural(n, 'cambio', 'cambios')} de las skills; "
                "vuelve a leer el SKILL.md de la skill que estás usando.")
    if token == "ATRASADA":
        base = f"Hay {plural(n, 'cambio nuevo', 'cambios nuevos')} en GitHub"
        if d.get("pull_error"):
            return (f"{base} y no se pudieron descargar solos ({d['pull_error']}). "
                    f"Para actualizar: git -C \"{repo}\" pull --ff-only")
        return f"{base}. Para actualizar: git -C \"{repo}\" pull --ff-only"
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
    if token == "ACTUALIZADA":
        return (f"gui-skills: se descargaron {plural(n, 'cambio', 'cambios')} de las skills desde GitHub "
                "(actualización automática). Si ya leíste el SKILL.md de alguna, vuelve a leerlo.")
    if token == "ATRASADA" and d.get("pull_error"):
        return (f"gui-skills: hay {plural(n, 'cambio nuevo', 'cambios nuevos')} de las skills en GitHub y no se pudieron "
                f"descargar solos ({d['pull_error']}). Avísale al usuario y ofrécele: git -C \"{repo}\" pull --ff-only")
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
    ap.add_argument("--pull", action="store_true",
                    help="si esta atrasada y es seguro (clon limpio, rama main), hace git pull --ff-only")
    args = ap.parse_args(argv)

    if args.hook:
        try:
            return run_hook(args)
        except BaseException:  # the hook must never break a session
            print("gui-skills: no se pudo comprobar si hay actualizaciones; se usa la copia local.")
            return 0

    repo = gui_common.resolve_repo(args.repo, __file__)
    token, n, d = compute(repo, do_fetch=True, do_pull=args.pull)
    if d.get("fetched"):
        write_last_check(repo, token)
    label = f"{token} {n}" if token in ("ATRASADA", "ACTUALIZADA") else token
    print(label if args.quiet else f"{label} - {describe(token, n, d, repo)}")
    warn = pending_warning(repo, d.get("pending") or [])
    if warn:
        print(f"AVISO: {warn}")
    return 0


def run_hook(args) -> int:
    repo = gui_common.resolve_repo(args.repo, __file__)
    last = read_last_check(repo)
    age = (time.time() - last) if last is not None else None
    # with --pull every session start fetches (and updates); without it the old 6 h rate limit applies
    skip = (not args.pull) and age is not None and 0 <= age < HOOK_INTERVAL
    token, n, d = compute(repo, do_fetch=not skip, do_pull=args.pull)
    if d.get("fetched"):
        write_last_check(repo, token)
    line = hook_line(token, n, d, repo, (age / 3600) if skip else None)
    warn = pending_warning(repo, d.get("pending") or [])
    if warn:
        line += f" Aviso: {warn}."
    print(" ".join(line.split()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
