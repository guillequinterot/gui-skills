#!/usr/bin/env python3
"""Publish the repo changes left by a finished job (rama + commit + push + Pull Request).

Normally those changes are the HANDOFF/HANDSHAKE edits written by log_job.py. Start from `main` with the
changes uncommitted in the working tree:

  python tools/publish_job.py --tema caso-web-universidad-01
  python tools/publish_job.py --tema caso-web-universidad-01 --merge   # maintainer: merge the PR right away
  python tools/publish_job.py --reintentar                             # push + PR for pending aporte/* branches

First word of the output is the status token:
PR_CREADO <url> | PUBLICADO <url> | PR_MANUAL <url> | PENDIENTE <rama> | BLOQUEADO | SIN_CAMBIOS | DRY_RUN | ERROR
Exit code: 0 for everything except BLOQUEADO / ERROR (1) and usage errors (2).

Never force-pushes, never pushes to main, never prints or stores a token.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_update  # noqa: E402
import gui_common  # noqa: E402
import privacy_scan  # noqa: E402

FETCH_TIMEOUT = 20
PUSH_TIMEOUT = 60
PULL_TIMEOUT = 30
COMMIT_TIMEOUT = 120
GH_TIMEOUT = 45
HTTP_TIMEOUT = 25
TEMA_RE = re.compile(r"^[a-z0-9-]{1,60}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PR_URL_RE = re.compile(r"https://[^\s]+/pull/(\d+)")
EXTRA_DIRS = ("shared/", "templates/", "tools/", "tests/")  # allowed outside skills/ with --incluir-todo


class Abort(Exception):
    def __init__(self, token: str, message: str, code: int = 1, detail: str = ""):
        super().__init__(message)
        self.token, self.message, self.code, self.detail = token, message, code, detail


NOTES: list = []  # secondary remarks; printed after the status line so the first word is always the token


def say(text: str = "") -> None:
    print(text)


def note(text: str) -> None:
    NOTES.append(text)


def git(repo: Path, *args: str, timeout: float = 30):
    return check_update.run_git(repo, list(args), timeout=timeout)


def git_ok(repo: Path, *args: str) -> bool:
    return git(repo, *args)[0] == 0


def git_out(repo: Path, *args: str, timeout: float = 30) -> str:
    rc, out, _ = git(repo, *args, timeout=timeout)
    return out.strip() if rc == 0 else ""


def short_err(err: str, out: str = "") -> str:
    return check_update.first_line(err) or check_update.first_line(out) or "sin detalle"


def push_failure_reason(rc, err: str) -> str:
    if rc is None:
        return f"sin respuesta de GitHub en {PUSH_TIMEOUT} s"
    if check_update.AUTH_RE.search(err):
        return "GitHub rechazó la credencial (revisa la sección Credenciales del README)"
    return short_err(err)


# ---------------------------------------------------------------- remote / GitHub helpers

def parse_github_remote(url: str):
    """(owner, repo) for GitHub https/ssh URLs; None for anything else (file remotes, other hosts)."""
    url = (url or "").strip()
    m = re.match(r"^(?:https?://(?:[^@/]+@)?|ssh://(?:[^@/]+@)?|git@)github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", url)
    return (m.group(1), m.group(2)) if m else None


def origin_url(repo: Path) -> str:
    return git_out(repo, "config", "--get", "remote.origin.url")  # raw URL (get-url applies insteadOf)


def compare_url(owner_repo, branch: str) -> str:
    owner, name = owner_repo
    return f"https://github.com/{owner}/{name}/compare/main...{branch}?expand=1"


def run_cmd(cmd: list, timeout: float, cwd=None, stdin_text=None, env=None):
    """Never raises: (rc|None on timeout, stdout, stderr)."""
    return check_update.run_proc(cmd, timeout, env=env, cwd=cwd, stdin_text=stdin_text)


def gh_available() -> bool:
    if os.environ.get("GUI_SKILLS_NO_GH") or not shutil.which("gh"):
        return False
    rc, _, _ = run_cmd(["gh", "auth", "status", "--hostname", "github.com"], 15, env=_gh_env())
    return rc == 0


def _gh_env() -> dict:
    env = dict(os.environ)
    env["GH_PROMPT_DISABLED"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["NO_COLOR"] = "1"
    return env


def api_base() -> str:
    return (os.environ.get("GUI_SKILLS_API_URL") or "https://api.github.com").rstrip("/")


def get_token(repo: Path, owner_repo):
    """Token from GH_TOKEN/GITHUB_TOKEN or git's credential helper (non-interactive). Never printed or stored."""
    for key in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(key):
            return os.environ[key].strip()
    owner, name = owner_repo
    env = check_update.git_env()
    env["GCM_INTERACTIVE"] = "never"
    request = f"protocol=https\nhost=github.com\npath={owner}/{name}.git\n\n"
    rc, out, _ = run_cmd(["git", "-C", str(repo), "credential", "fill"], 15, stdin_text=request, env=env)
    if rc == 0:
        for line in out.splitlines():
            if line.startswith("password="):
                return line[len("password="):].strip() or None
    return None


def api_request(method: str, path: str, token: str, payload=None):
    """(status|None, parsed json|None, reason). The token only goes in the Authorization header."""
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(api_base() + path, data=data, method=method, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "gui-skills-publish-job",
        **({"Content-Type": "application/json"} if data is not None else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status, (json.loads(body) if body.strip() else {}), ""
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8", "replace") or "{}")
        except ValueError:
            body = {}
        return exc.code, body if isinstance(body, dict) else {}, f"HTTP {exc.code}"
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return None, None, f"sin conexión con la API de GitHub ({type(exc).__name__})"


def _rest_error(status, reason: str, body) -> str:
    if status in (401, 403):
        return f"GitHub rechazó la credencial (HTTP {status})"
    msg = (body or {}).get("message") if isinstance(body, dict) else ""
    return f"{reason}{': ' + str(msg)[:120] if msg else ''}"


def create_pr(repo: Path, owner_repo, branch: str, title: str, body: str):
    """Try gh, then the REST API. Returns dict(url, number, via, notes) with url=None when both fail."""
    result = {"url": None, "number": None, "via": None, "notes": []}
    if not owner_repo:
        result["notes"].append("el remoto origin no es de GitHub")
        return result
    owner, name = owner_repo
    slug = f"{owner}/{name}"

    if gh_available():
        with tempfile.TemporaryDirectory() as tmp:
            body_file = Path(tmp) / "body.md"
            body_file.write_text(body, encoding="utf-8")
            rc, out, err = run_cmd(["gh", "pr", "create", "--repo", slug, "--base", "main", "--head", branch,
                                    "--title", title, "--body-file", str(body_file)], GH_TIMEOUT, cwd=str(repo), env=_gh_env())
        m = PR_URL_RE.search(out + "\n" + err)
        if m and (rc == 0 or "already exists" in (out + err)):
            result.update(url=m.group(0), number=int(m.group(1)), via="gh")
            return result
        result["notes"].append(f"gh no pudo crear el PR ({short_err(err, out)})")

    token = get_token(repo, owner_repo)
    if token:
        status, data, reason = api_request("POST", f"/repos/{slug}/pulls", token,
                                           {"title": title, "head": branch, "base": "main", "body": body})
        if status == 201 and isinstance(data, dict) and data.get("html_url"):
            result.update(url=data["html_url"], number=data.get("number"), via="api")
            return result
        if status == 422:  # probably "a pull request already exists"
            st2, lst, _ = api_request("GET", f"/repos/{slug}/pulls?head={owner}:{branch}&state=open", token)
            if st2 == 200 and isinstance(lst, list) and lst:
                result.update(url=lst[0].get("html_url"), number=lst[0].get("number"), via="api")
                return result
        result["notes"].append(f"la API de GitHub no creó el PR ({_rest_error(status, reason, data)})")
    else:
        result["notes"].append("no hay gh autenticado ni token en GH_TOKEN/GITHUB_TOKEN/credencial de git")
    return result


def merge_pr(repo: Path, owner_repo, pr: dict, branch: str):
    """Merge (merge commit) and delete the remote branch. Returns (ok, note)."""
    slug = "{}/{}".format(*owner_repo)
    order = ["gh", "api"] if pr.get("via") == "gh" else ["api", "gh"]
    notes = []
    for how in order:
        if how == "gh" and gh_available():
            rc, out, err = run_cmd(["gh", "pr", "merge", str(pr["number"]), "--repo", slug, "--merge", "--delete-branch"],
                                   GH_TIMEOUT, cwd=str(repo), env=_gh_env())
            if rc == 0:
                return True, ""
            notes.append(f"gh: {short_err(err, out)}")
        elif how == "api":
            token = get_token(repo, owner_repo)
            if not token:
                notes.append("sin token para la API")
                continue
            status, data, reason = api_request("PUT", f"/repos/{slug}/pulls/{pr['number']}/merge", token,
                                               {"merge_method": "merge"})
            if status == 200:
                api_request("DELETE", f"/repos/{slug}/git/refs/heads/{branch}", token)  # best effort
                return True, ""
            notes.append(f"API: {_rest_error(status, reason, data)}")
    return False, "; ".join(notes) or "sin método disponible"


# ---------------------------------------------------------------- repo state helpers

def parse_status(repo: Path):
    """[(xy, path)] from porcelain -z (renames/copies also list the original path)."""
    rc, out, err = git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if rc != 0:
        raise Abort("ERROR", f"git status falló: {short_err(err)}")
    entries = out.split("\0")
    items, i = [], 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if len(entry) < 4:
            continue
        xy, path = entry[:2], entry[3:]
        items.append((xy, path))
        if "R" in xy or "C" in xy:
            if i < len(entries) and entries[i]:
                items.append((xy, entries[i]))
            i += 1
    return items


def allowed_outside_skills(path: str) -> bool:
    return path.startswith(EXTRA_DIRS) or ("/" not in path and path.lower().endswith(".md"))


def check_scope(paths: list, incluir_todo: bool) -> None:
    bad = [p for p in paths if not p.startswith("skills/") and not (incluir_todo and allowed_outside_skills(p))]
    if bad:
        shown = "\n".join(f"  - {p}" for p in bad[:15]) + ("\n  ..." if len(bad) > 15 else "")
        extra = ("" if not incluir_todo else
                 "\nAun con --incluir-todo no se publican .githooks/, .github/ ni otras rutas sensibles: eso se hace con git a mano.")
        raise Abort("ERROR", "hay cambios fuera de skills/, que este comando no publica por defecto:\n" + shown +
                    "\nUsa --incluir-todo si de verdad cambiaste shared/, templates/, tools/ o la documentación; "
                    "si no, descarta esos cambios." + extra)


def commit_count(repo: Path, rev_range: str) -> int:
    cnt = git_out(repo, "rev-list", "--count", rev_range)
    return int(cnt) if cnt.isdigit() else 0


def branch_exists(repo: Path, name: str) -> bool:
    return git_ok(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{name}") or \
        git_ok(repo, "rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}")


def pick_branch(repo: Path, alias: str, fecha: str, tema: str) -> str:
    base = f"aporte/{alias}/{fecha}-{tema}"
    name, n = base, 1
    while branch_exists(repo, name):
        n += 1
        name = f"{base}-{n}"
    return name


def sync_main(repo: Path, untracked: list) -> str:
    """git fetch; when main is behind, stash -> pull --ff-only -> stash pop. Returns a note (may be empty)."""
    rc, _, err = git(repo, "fetch", "--quiet", "--no-tags", "origin", timeout=FETCH_TIMEOUT)
    if rc != 0:
        return f"no se pudo consultar GitHub ({push_failure_reason(rc, err)}); se sigue con la copia local"
    behind = commit_count(repo, "HEAD..origin/main")
    if not behind:
        return ""
    old_head = git_out(repo, "rev-parse", "HEAD")
    rc, _, err = git(repo, "stash", "push", "--include-untracked", "-m", "gui-skills-publish")
    if rc != 0:
        raise Abort("ERROR", f"no pude guardar tus cambios para actualizar main ({short_err(err)}); no se tocó nada.")
    rc, _, err = git(repo, "pull", "--ff-only", "--quiet", "origin", "main", timeout=PULL_TIMEOUT)
    pull_err = short_err(err) if rc != 0 else ""
    if rc == 0:
        rc, _, err = git(repo, "stash", "pop", "--quiet")
        if rc == 0:
            return f"main estaba {behind} commit(s) atrás: se actualizó antes de publicar"
        pull_err = "los cambios de GitHub chocan con los tuyos (mismos archivos)"
        for path in untracked:  # partly restored by the failed pop; the stash still holds them
            try:
                (repo / path).unlink()
            except OSError:
                pass
        git(repo, "reset", "--hard", "--quiet", old_head)
    rc, _, err = git(repo, "stash", "pop", "--quiet")
    if rc != 0:
        raise Abort("ERROR", "no pude devolver tus cambios al clon; siguen guardados en `git stash list` "
                             f"(stash 'gui-skills-publish'). Recupéralos con `git -C \"{repo}\" stash pop`. Motivo: {pull_err}")
    raise Abort("ERROR", f"no se publicó nada: {pull_err}. Tus cambios siguen en el clon, como estaban. "
                         f"Actualiza main (python \"{repo.as_posix()}/tools/check_update.py\" --pull) con los cambios "
                         "guardados aparte, o reconcilia el HANDOFF a mano y vuelve a correr publish_job.py.")


def build_pr_body(repo: Path, base: str, branch: str, alias: str) -> str:
    rc, out, _ = git(repo, "diff", "--name-status", f"{base}..{branch}")
    labels = {"A": "nuevo", "M": "modificado", "D": "borrado", "R": "renombrado", "C": "copiado"}
    files, handoffs = [], []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            files.append((labels.get(parts[0][:1], parts[0]), parts[-1]))
            if parts[-1].endswith("HANDOFF.md") and parts[0][:1] != "D":
                handoffs.append(parts[-1])
    lines = [f"## Aporte de {alias} vía gui-skills", "",
             "Publicado automáticamente al terminar un trabajo con `tools/publish_job.py`. Lo revisa el mantenedor "
             "(contenido y privacidad) antes de fusionarlo.", "", "### Archivos cambiados", ""]
    lines += [f"- `{path}` ({label})" for label, path in files] or ["- (sin lista)"]
    entries = []
    for path in handoffs:
        rc, diff, _ = git(repo, "diff", "--unified=0", f"{base}..{branch}", "--", path)
        added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")
                 and (l.startswith("+### ") or l.startswith("+- **"))]
        if added:
            entries.append((path, added))
    if entries:
        lines += ["", "### Registro de trabajos: entradas nuevas", ""]
        for path, added in entries:
            lines.append(f"**{path}**")
            lines.append("")
            lines += [f"> {l}" for l in added]
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_message(path: Path, subject: str, alias: str) -> None:
    path.write_text(f"{subject}\n\nAporte de {alias} vía gui-skills\n", encoding="utf-8")


# ---------------------------------------------------------------- flows

def finish_pr(repo: Path, owner_repo, branch: str, title: str, body: str, want_merge: bool) -> None:
    """Create the PR (and merge it when asked) for a branch already on GitHub; print the result token."""
    pr = create_pr(repo, owner_repo, branch, title, body)
    if not pr["url"]:
        if owner_repo:
            say(f"PR_MANUAL {compare_url(owner_repo, branch)}")
            say(f"La rama {branch} ya está en GitHub. Abre el Pull Request en ese enlace.")
        else:
            say(f"PR_MANUAL (sin URL: el remoto origin no es de GitHub) rama {branch}")
        for note in pr["notes"]:
            say(f"  - {note}")
        if want_merge:
            say("  - --merge no se pudo aplicar porque el PR no se creó automáticamente; fusiónalo a mano.")
        return
    if not want_merge:
        say(f"PR_CREADO {pr['url']}")
        say(f"Rama {branch}. Lo revisa el mantenedor.")
        return
    ok, note = merge_pr(repo, owner_repo, pr, branch)
    if not ok:
        say(f"PR_CREADO {pr['url']}")
        say(f"AVISO: no se pudo fusionar automáticamente ({note}); queda para revisión del mantenedor.")
        return
    cleanup_after_merge(repo, branch)
    say(f"PUBLICADO {pr['url']}")
    say(f"Fusionado en main y rama {branch} borrada.")


def cleanup_after_merge(repo: Path, branch: str) -> None:
    git(repo, "fetch", "--quiet", "--prune", "--no-tags", "origin", timeout=FETCH_TIMEOUT)
    if git_out(repo, "rev-parse", "--abbrev-ref", "HEAD") == "main" and not git_out(repo, "status", "--porcelain"):
        git(repo, "pull", "--ff-only", "--quiet", "origin", "main", timeout=PULL_TIMEOUT)
    if git_out(repo, "rev-parse", "--abbrev-ref", "HEAD") != branch:
        git(repo, "branch", "-D", branch)


def publish(a, repo: Path, alias: str) -> int:
    if git_out(repo, "rev-parse", "--abbrev-ref", "HEAD") != "main":
        raise Abort("ERROR", "publish_job.py debe empezar en la rama main con los cambios sin commitear "
                             f"(estás en '{git_out(repo, 'rev-parse', '--abbrev-ref', 'HEAD') or '?'}'). "
                             "Si ya trabajaste en una rama aporte/..., súbela con git a mano o con --reintentar.")
    items = parse_status(repo)
    if any("U" in xy or xy in ("AA", "DD") for xy, _ in items):
        raise Abort("ERROR", "hay conflictos sin resolver en el clon; resuélvelos antes de publicar.")
    paths = list(dict.fromkeys(p for _, p in items))
    if not paths:
        say("SIN_CAMBIOS - no hay nada que publicar (el clon no tiene cambios).")
        return 0
    if commit_count(repo, "origin/main..HEAD") > 0:
        raise Abort("ERROR", "main tiene commits locales sin subir; no se publica desde ahí. Revísalos con git.")
    check_scope(paths, a.incluir_todo)

    subject = a.mensaje or f"Registro de trabajo: {a.tema}"
    scanner = privacy_scan.build_scanner(use_terms=True, repo=repo)
    hits = scanner.scan_text(subject, "--mensaje") + scanner.scan_text(a.tema, "--tema")
    if hits:
        raise Abort("BLOQUEADO", "el escáner de privacidad rechazó el mensaje o el tema (no se hizo nada)",
                    detail="\n".join(f"  {h.file}: [{h.category}] {h.detail}" for h in hits))

    owner_repo = parse_github_remote(origin_url(repo))

    if a.dry_run:
        branch = pick_branch(repo, alias, a.fecha, a.tema)
        say("[dry-run] no se cambia nada. Pasos que se harían:")
        say(f"[dry-run] 1. git fetch; si main está atrás, stash -> pull --ff-only -> stash pop")
        say(f"[dry-run] 2. rama nueva {branch} desde main")
        say(f"[dry-run] 3. git add -A y commit «{subject}» (el hook pre-commit corre el escáner de privacidad)")
        for p in paths[:20]:
            say(f"[dry-run]      - {p}")
        if len(paths) > 20:
            say(f"[dry-run]      ... y {len(paths) - 20} más")
        say(f"[dry-run] 4. git push -u origin {branch} (sin force, nunca a main)")
        if owner_repo:
            say(f"[dry-run] 5. PR hacia main en {owner_repo[0]}/{owner_repo[1]}: gh si está autenticado, si no la API "
                "con GH_TOKEN/GITHUB_TOKEN o la credencial de git, si no el enlace de comparación:")
            say(f"[dry-run]      {compare_url(owner_repo, branch)}")
        else:
            say("[dry-run] 5. el remoto origin no es de GitHub: no se puede abrir el PR automáticamente (PR_MANUAL)")
        if a.merge:
            say("[dry-run] 6. --merge: gh pr merge --merge --delete-branch (o PUT /pulls/{n}/merge y borrar la rama remota), "
                "luego git checkout main, git pull --ff-only y borrar la rama local")
        say(f"[dry-run] {'7' if a.merge else '6'}. volver a main con el clon limpio y avisar: "
            f"{'PUBLICADO <url>' if a.merge else 'PR_CREADO <url>'}")
        say("DRY_RUN - no se cambió nada.")
        return 0

    sync_note = sync_main(repo, [p for xy, p in items if xy == "??"])
    if sync_note:
        note(f"Nota: {sync_note}.")

    branch = pick_branch(repo, alias, a.fecha, a.tema)
    rc, _, err = git(repo, "checkout", "-b", branch)
    if rc != 0:
        raise Abort("ERROR", f"no pude crear la rama {branch}: {short_err(err)}")
    rc, _, err = git(repo, "add", "-A")
    if rc != 0:
        restore_main(repo, branch)
        raise Abort("ERROR", f"git add falló: {short_err(err)}")
    with tempfile.TemporaryDirectory() as tmp:
        msg_file = Path(tmp) / "mensaje.txt"
        write_message(msg_file, subject, alias)
        rc, out, err = git(repo, "commit", "-q", "-F", str(msg_file), timeout=COMMIT_TIMEOUT)
    if rc != 0:
        output = (out + "\n" + err).strip()
        restore_main(repo, branch)
        if re.search(r"privacidad|privacy", output, re.I):
            raise Abort("BLOQUEADO", "el escáner de privacidad bloqueó el commit; tus cambios siguen en el clon, "
                                     "sin publicar. Corrige el texto señalado y vuelve a correr publish_job.py "
                                     "(nunca se salta el hook).", detail=output)
        raise Abort("ERROR", f"el commit falló: {short_err(err, out)}", detail=output)

    title = subject
    body = build_pr_body(repo, "main", branch, alias)
    rc, _, err = git(repo, "push", "-u", "origin", branch, timeout=PUSH_TIMEOUT)
    git(repo, "checkout", "-q", "main")
    if rc != 0:
        say(f"PENDIENTE {branch} - no se pudo subir: {push_failure_reason(rc, err)}.")
        say("El trabajo quedó guardado en esa rama local (el clon está en main y limpio); "
            "se reintentará con --reintentar (el Paso 0 lo avisará).")
        return 0
    finish_pr(repo, owner_repo, branch, title, body, a.merge)
    return 0


def restore_main(repo: Path, branch: str) -> None:
    """After a failed commit: unstage, go back to main (changes stay in the working tree), drop the empty branch."""
    git(repo, "reset", "-q")
    git(repo, "checkout", "-q", "main")
    git(repo, "branch", "-D", branch)


def reintentar(a, repo: Path) -> int:
    rc, _, _ = git(repo, "fetch", "--quiet", "--no-tags", "origin", timeout=FETCH_TIMEOUT)
    branches = check_update.pending_branches(repo)
    if not branches:
        say("SIN_CAMBIOS - no hay aportes pendientes de publicar.")
        return 0
    owner_repo = parse_github_remote(origin_url(repo))
    alias = (a.alias or gui_common.load_config().get("alias") or "").strip()
    for branch in branches:
        if a.dry_run:
            say(f"[dry-run] push -u origin {branch} y PR hacia main"
                + (f" ({compare_url(owner_repo, branch)})" if owner_repo else ""))
            continue
        rc, _, err = git(repo, "push", "-u", "origin", branch, timeout=PUSH_TIMEOUT)
        if rc != 0:
            say(f"PENDIENTE {branch} - no se pudo subir: {push_failure_reason(rc, err)}.")
            continue
        title = git_out(repo, "log", "-1", "--format=%s", f"refs/heads/{branch}") or branch
        body = build_pr_body(repo, "origin/main", branch, alias or "alguien")
        finish_pr(repo, owner_repo, branch, title, body, a.merge)
    if a.dry_run:
        say("DRY_RUN - no se cambió nada.")
    return 0


def main(argv=None) -> int:
    gui_common.setup_stdio()
    ap = argparse.ArgumentParser(description="Publica (rama + commit + push + PR) los cambios de un trabajo terminado.")
    ap.add_argument("--tema", help="identificador de la rama: caso-o-tema en minúsculas, números y guiones")
    ap.add_argument("--mensaje", help='resumen del commit y título del PR (por defecto "Registro de trabajo: <tema>")')
    ap.add_argument("--merge", action="store_true", help="fusiona el PR de inmediato (pensado para el mantenedor)")
    ap.add_argument("--reintentar", action="store_true", help="sube y abre PR de las ramas aporte/* pendientes")
    ap.add_argument("--incluir-todo", action="store_true", help="permite cambios en shared/, templates/, tools/ y documentación")
    ap.add_argument("--dry-run", action="store_true", help="muestra los pasos sin cambiar nada")
    ap.add_argument("--repo", help="ruta del clon (por defecto, repo_path de config.json o este repo)")
    ap.add_argument("--alias")
    ap.add_argument("--fecha", default=time.strftime("%Y-%m-%d"), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    if not a.reintentar:
        if not a.tema:
            ap.error("falta --tema <slug> (o usa --reintentar)")
        if not TEMA_RE.match(a.tema):
            ap.error("--tema solo admite minúsculas, números y guiones (máx. 60)")
    if not DATE_RE.match(a.fecha):
        ap.error("--fecha debe ser AAAA-MM-DD")
    repo = gui_common.resolve_repo(a.repo, __file__)
    try:
        if git(repo, "rev-parse", "--git-dir")[0] != 0:
            raise Abort("ERROR", f"{repo} no es un clon de git")
        if a.reintentar:
            code = reintentar(a, repo)
        else:
            alias = (a.alias or gui_common.load_config().get("alias") or "").strip()
            if not re.match(gui_common.ALIAS_RE, alias):
                raise Abort("ERROR", "falta un alias válido: define 'alias' en ~/.gui-skills/config.json o usa --alias")
            code = publish(a, repo, alias)
    except Abort as exc:
        say(f"{exc.token} - {exc.message}")
        if exc.detail:
            say(exc.detail)
        code = exc.code
    for text in NOTES:
        say(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
