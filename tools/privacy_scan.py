#!/usr/bin/env python3
"""Privacy scanner for gui-skills.

Blocks emails, phones, tokens/keys, personal absolute paths and the private terms
of each person (~/.gui-skills/private-terms.txt). Exit 0 = clean, 1 = hits, 2 = usage error.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gui_common  # noqa: E402

IGNORE_MARK = "privacy-scan: ignore"
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
BINARY_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".ico", ".avif", ".heic",
    ".psd", ".ai", ".eps", ".indd", ".fig", ".sketch", ".svgz",
    ".pdf", ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2", ".xz",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".pages", ".numbers",
    ".mp4", ".mov", ".avi", ".mkv", ".webm", ".mp3", ".wav", ".m4a", ".flac", ".ogg",
    ".ttf", ".otf", ".woff", ".woff2", ".exe", ".dll", ".so", ".dylib", ".sqlite", ".db",
}
IGNORED_EXTS = {".pyc", ".pyo"}
FILE_TLDS = {"png", "jpg", "jpeg", "gif", "svg", "webp", "avif", "ico", "bmp", "css", "js",
             "json", "woff", "woff2", "ttf", "otf", "map"}
PLACEHOLDERS = {
    "usuario", "tu-usuario", "tu_usuario", "tuusuario", "user", "username", "nombre", "name",
    "tu-nombre", "tunombre", "ejemplo", "example", "runner", "public", "default", "all", "amigo",
    "yo", "me", "xxx", "x", "ruta", "path", "carpeta", "folder", "dir", "proyecto", "project",
    "tu-carpeta", "tu-proyecto",
}
SAFE_DRIVE_SEGMENTS = {"windows", "program", "programdata", "temp", "tmp"}

Finding = namedtuple("Finding", "file line category detail blocking")

EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![\w-])")
PHONE_RES = [
    (re.compile(r"(?<![\w.+-])\+\d{1,3}[\s.-]?\(?\d{1,4}\)?(?:[\s.-]?\d{2,4}){2,4}(?![\w-])"), True),
    (re.compile(r"(?<![\w.+-])(?:\(?\+?57\)?[\s.-]?)?3[0-5]\d[\s.-]?\d{3}[\s.-]?\d{4}(?![\w-])"), False),
    (re.compile(r"(?<![\w.+-])\(?60[1-8]\)?[\s.-]?\d{3}[\s.-]?\d{4}(?![\w-])"), False),
    (re.compile(r"(?<![\w.+-])\(\d{3}\)\s?\d{3}[\s.-]\d{4}(?![\w-])"), False),
    (re.compile(r"(?<![\w.+-])\d{3}[\s.-]\d{3}[\s.-]\d{4}(?![\w-])"), False),
]
# (category, regex, group holding the secret tail or 0, needs_digit)
SECRET_RES = [
    ("token-github", re.compile(r"\b(?:github_pat_|gh[pousr]_)([A-Za-z0-9_]{16,})"), 1, False),
    ("clave-api", re.compile(r"(?<![A-Za-z0-9])sk-(?:ant-|proj-|live-|test-)?([A-Za-z0-9_-]{20,})"), 1, True),
    ("clave-aws", re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA)([0-9A-Z]{16})\b"), 1, False),
    ("clave-aws", re.compile(r"aws_secret_access_key\s*[=:]\s*[\"']?([A-Za-z0-9/+=]{30,})", re.I), 1, False),
    ("clave-google", re.compile(r"\bAIza([0-9A-Za-z_-]{35})\b"), 1, False),
    ("bearer", re.compile(r"\bBearer\s+([A-Za-z0-9._~+/=-]{20,})"), 1, True),
    ("clave-privada", re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY(?: BLOCK)?-----"), 0, False),
    ("token-slack", re.compile(r"\bxox[abprs]-([A-Za-z0-9-]{10,})"), 1, False),
]
WIN_USER_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]+Users[\\/]+([^\\/\s\"'`]+)", re.I)
NIX_USER_RE = re.compile(r"(?<![\w.~:/\\-])/(?:Users|home)/([^/\s\"'`]+)")
DRIVE_RE = re.compile(r"(?<![A-Za-z0-9])([A-Za-z]):[\\/]+([^\\/\s\"'`<>|*?:;,()\[\]{}]+)")


def is_placeholder(seg: str) -> bool:
    s = seg.strip().strip("\"'`").lower()
    return (not s) or s[0] in "<[{$%~*." or s in PLACEHOLDERS or s[-1] in ">}]"


def looks_real_secret(tail: str, needs_digit: bool) -> bool:
    if len(set(tail)) < 6:
        return False
    return (not needs_digit) or any(c.isdigit() for c in tail)


def mask(value: str) -> str:
    return value[:4] + "..." if len(value) > 6 else "***"


def generic_matches(line: str):
    """Yield (start, end, category, detail) for generic patterns."""
    for m in EMAIL_RE.finditer(line):
        if m.group(1).rsplit(".", 1)[-1].lower() in FILE_TLDS:
            continue
        yield m.start(), m.end(), "correo", m.group(0)
    seen = []
    for rx, check_digits in PHONE_RES:
        for m in rx.finditer(line):
            if any(m.start() < e and m.end() > s for s, e in seen):
                continue
            digits = sum(c.isdigit() for c in m.group(0))
            if check_digits and not 9 <= digits <= 15:
                continue
            seen.append((m.start(), m.end()))
            yield m.start(), m.end(), "telefono", m.group(0).strip()
    for category, rx, grp, needs_digit in SECRET_RES:
        for m in rx.finditer(line):
            tail = m.group(grp) if grp else m.group(0)
            if grp and not looks_real_secret(tail, needs_digit):
                continue
            yield m.start(), m.end(), category, mask(m.group(0))
    for m in WIN_USER_RE.finditer(line):
        if not is_placeholder(m.group(1)):
            yield m.start(), m.end(), "ruta-personal", "carpeta de usuario de Windows"
    for m in NIX_USER_RE.finditer(line):
        if not is_placeholder(m.group(1)):
            yield m.start(), m.end(), "ruta-personal", "carpeta de usuario de macOS/Linux"
    for m in DRIVE_RE.finditer(line):
        seg = m.group(2)
        low = seg.lower()
        if low == "users" or low in SAFE_DRIVE_SEGMENTS or is_placeholder(seg):
            continue
        yield m.start(), m.end(), "ruta-personal", f"ruta absoluta de disco ({m.group(1).upper()}:\\{seg}...)"


def load_terms(path: Path):
    """Parse a private-terms file into [(display, compiled_regex)]. Raises ValueError on bad regex."""
    out = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return out
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            pat = line[3:].strip()
            try:
                out.append((f"re:{pat}", re.compile(pat)))
            except re.error as exc:
                raise ValueError(f"{path}:{n}: expresion regular invalida ({exc})")
        else:
            out.append((line, re.compile(r"(?<!\w)" + re.escape(line) + r"(?!\w)", re.I)))
    return out


def load_allowlist(path: Path):
    out = []
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return out
    for n, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            out.append(re.compile(line))
        except re.error as exc:
            raise ValueError(f"{path}:{n}: expresion regular invalida ({exc})")
    return out


class Scanner:
    def __init__(self, terms=None, allow=None, generic=True):
        self.terms = terms or []
        self.allow = allow or []
        self.generic = generic

    def _allowed(self, line: str, start: int, end: int) -> bool:
        for rx in self.allow:
            for m in rx.finditer(line):
                if m.start() < end and m.end() > start:
                    return True
        return False

    def scan_line(self, line: str):
        """Return [(category, detail)] for one line."""
        if IGNORE_MARK in line:
            return []
        hits = []
        if self.generic:
            for s, e, cat, detail in generic_matches(line):
                if not self._allowed(line, s, e):
                    hits.append((cat, detail))
        for display, rx in self.terms:
            for m in rx.finditer(line):
                if not self._allowed(line, m.start(), m.end()):
                    hits.append(("termino-privado", display))
                    break
        return hits

    def scan_text(self, text: str, label: str):
        found = []
        for n, line in enumerate(text.splitlines(), 1):
            for cat, detail in self.scan_line(line):
                found.append(Finding(label, n, cat, detail, True))
        return found

    def scan_name(self, label: str):
        """Private terms in a file name/path (a name can leak a client too)."""
        found = []
        for display, rx in self.terms:
            if rx.search(label):
                found.append(Finding(label, 0, "termino-privado", f"{display} (en el nombre del archivo)", True))
        return found


def build_scanner(use_terms=True, extra_terms=(), extra_allow=(), repo: Path | None = None) -> Scanner:
    here = Path(__file__).resolve().parent
    allow_files = [here / "privacy-allowlist.txt"]
    if repo is not None and (repo / "tools" / "privacy-allowlist.txt") not in allow_files:
        allow_files.append(repo / "tools" / "privacy-allowlist.txt")
    allow_files.extend(Path(p) for p in extra_allow)
    allow = []
    for f in allow_files:
        allow.extend(load_allowlist(f))
    terms = []
    if use_terms:
        terms.extend(load_terms(gui_common.gui_home() / "private-terms.txt"))
        for t in extra_terms:
            p = Path(t)
            if not p.is_file():
                raise ValueError(f"no existe el archivo de terminos: {t}")
            terms.extend(load_terms(p))
    return Scanner(terms, allow, generic=True)


def is_binary_bytes(data: bytes) -> bool:
    return b"\x00" in data[:8192]


def decode(data: bytes) -> str:
    return data.decode("utf-8-sig", errors="replace")


def git(repo: Path, *args: str) -> bytes:
    res = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode("utf-8", "replace").strip() or "git fallo")
    return res.stdout


def scan_blob(scanner: Scanner, label: str, data: bytes, ext: str, strict_bin: bool):
    out = scanner.scan_name(label)
    if ext in IGNORED_EXTS:
        return out
    if ext in BINARY_EXTS or is_binary_bytes(data):
        out.append(Finding(label, 0, "binario-revisar",
                           "archivo binario no escaneado (imagen, PDF, comprimido u oficina): revisalo a mano",
                           strict_bin))
        return out
    out.extend(scanner.scan_text(decode(data), label))
    return out


def walk(path: Path):
    if path.is_file():
        yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            yield Path(root) / f


def display_name(p: Path, repo: Path) -> str:
    try:
        return p.resolve().relative_to(repo).as_posix()
    except ValueError:
        return str(p)


def main(argv=None) -> int:
    gui_common.setup_stdio()
    ap = argparse.ArgumentParser(description="Escaner de privacidad de gui-skills.")
    ap.add_argument("paths", nargs="*", help="archivos o carpetas a revisar (por defecto, todo el repo)")
    ap.add_argument("--staged", action="store_true", help="revisa lo que esta en el area de preparacion de git")
    ap.add_argument("--ci", action="store_true", help="solo patrones genericos (sin terminos privados)")
    ap.add_argument("--terms", action="append", default=[], help="archivo extra de terminos privados")
    ap.add_argument("--allowlist", action="append", default=[], help="archivo extra de excepciones")
    ap.add_argument("--strict-binaries", action="store_true", help="los binarios tambien bloquean")
    ap.add_argument("--repo", help="ruta del repo (por defecto, el de este script)")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else gui_common.script_repo_root(__file__)
    try:
        scanner = build_scanner(not args.ci, args.terms, args.allowlist, repo)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    findings = []
    try:
        if args.staged:
            names = git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split(b"\0")
            for raw in names:
                if not raw:
                    continue
                name = raw.decode("utf-8", "replace")
                data = git(repo, "show", f":{name}")
                findings += scan_blob(scanner, name, data, Path(name).suffix.lower(), args.strict_binaries)
        else:
            if args.paths:
                files = [f for p in args.paths for f in walk(Path(p))]
            else:
                try:
                    listed = git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
                    files = [repo / n.decode("utf-8", "replace") for n in listed.split(b"\0") if n]
                except (RuntimeError, OSError):
                    files = list(walk(repo))
            for f in files:
                if not f.is_file():
                    continue
                if any(part in SKIP_DIRS for part in f.parts):
                    continue
                findings += scan_blob(scanner, display_name(f, repo), f.read_bytes(),
                                      f.suffix.lower(), args.strict_binaries)
    except (RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    blocking = [f for f in findings if f.blocking]
    warnings = [f for f in findings if not f.blocking]
    for f in warnings:
        print(f"AVISO {f.file}: [{f.category}] {f.detail}")
    for f in blocking:
        loc = f"{f.file}:{f.line}" if f.line else f.file
        print(f"{loc}: [{f.category}] {f.detail}")
    if blocking:
        print(f"\nBLOQUEADO: {len(blocking)} hallazgo(s) de privacidad, {len(warnings)} aviso(s).")
        return 1
    print(f"OK: sin hallazgos de privacidad ({len(warnings)} aviso(s) de binarios).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
