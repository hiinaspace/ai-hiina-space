"""Fail-closed publication lint for ai.hiina.space.

Checks content/, dist/ and top-level docs for private terms (an external
denylist), stray email addresses, local paths, private IP addresses, private
claude.ai links and oversized pages, and checks that every commit is authored
and committed as Hiina. Second-person references to private circumstances are
reported as warnings for the reviewer, not failures.

The denylist is not in this repo (it would itself be a leak). Lookup order:
$AIHS_DENYLIST, lint/denylist.txt (git-ignored), then the private tracker copy.
Format: one term per line, `#` comments, `re:` prefix for a raw regex; plain
terms match case-insensitively on word boundaries.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DENYLIST_CANDIDATES = [Path(p) for p in [os.environ.get("AIHS_DENYLIST", "")] if p] + [
    ROOT / "lint" / "denylist.txt",
    Path.home() / "org" / "projects" / "ai-hiina-space" / "denylist.txt",
]
SCAN_DIRS = ["content", "dist", "worker", "versions"]
SCAN_TOP = ["README.md", "AGENTS.md", "LICENSE", "wrangler.jsonc"]
TEXT_SUFFIXES = {".md", ".html", ".txt", ".xml", ".json", ".js", ".jsonc", ""}
# Fetch tools pass ~40K characters verbatim; whole-report files are exempt by name.
MAX_PAGE_BYTES = 35_000
BULK_FILE_RE = re.compile(r"(?:^|/)(?:full|v\d+)\.md$")
ALLOWED_EMAILS = {"hiina@hiina.space"}
ALLOWED_IDENTITY = "Hiina <hiina@hiina.space>"

EMAIL_RE = re.compile(r"(?<![\w/@.])[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
FIXED_PATTERNS: dict[str, re.Pattern[str]] = {
    "home path": re.compile(r"(?<![\w.])~/|/home/\w|/mnt/\w|/run/user/|/Users/\w"),
    "private claude.ai link": re.compile(
        r"claude\.ai/(?:artifact|chat|project|code|messages|share)\b"
    ),
    "private IPv4": re.compile(
        r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01])|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))"
        r"\.\d{1,3}\.\d{1,3}\b"
    ),
}
SECOND_PERSON_RE = re.compile(
    r"\byour\s+(?:own\s+)?(?:\w+\s+){0,2}?"
    r"(?:cluster|server|homelab|lan|network|machine|box|host|vault|notes|schedule|"
    r"health|doctor|money|finances|income|budget|house|home|family|friend|partner|"
    r"job|employer|quota|subscription|agents?)\b",
    re.IGNORECASE,
)


@dataclass
class Finding:
    level: str  # "error" | "warn"
    where: str
    rule: str
    text: str

    def __str__(self) -> str:
        return f"{self.level.upper():5} {self.where}: [{self.rule}] {self.text}"


def load_denylist(path: Path) -> list[tuple[str, re.Pattern[str]]]:
    rules = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            rules.append((line, re.compile(line[3:], re.IGNORECASE)))
        else:
            rules.append((line, re.compile(rf"(?<!\w){re.escape(line)}(?!\w)", re.IGNORECASE)))
    return rules


def find_denylist() -> Path | None:
    return next((p for p in DENYLIST_CANDIDATES if p.is_file()), None)


def scan_files(root: Path) -> list[Path]:
    files = []
    for d in SCAN_DIRS:
        base = root / d
        if base.is_dir():
            files += [p for p in base.rglob("*") if p.is_file()]
    files += [root / f for f in SCAN_TOP if (root / f).is_file()]
    return sorted(p for p in files if p.suffix in TEXT_SUFFIXES)


def lint_text(
    where: str, text: str, denylist: list[tuple[str, re.Pattern[str]]]
) -> list[Finding]:
    out: list[Finding] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        loc = f"{where}:{lineno}"
        for _term, pat in denylist:
            if m := pat.search(line):
                # Never echo the term's definition; the match is already in the file.
                out.append(Finding("error", loc, "denylist", m.group(0)))
        for name, pat in FIXED_PATTERNS.items():
            if m := pat.search(line):
                out.append(Finding("error", loc, name, m.group(0)))
        for m in EMAIL_RE.finditer(line):
            if m.group(0).lower() not in ALLOWED_EMAILS:
                out.append(Finding("error", loc, "email", m.group(0)))
        for m in SECOND_PERSON_RE.finditer(line):
            out.append(Finding("warn", loc, "second-person", m.group(0)))
    return out


def lint_sizes(root: Path) -> list[Finding]:
    dist = root / "dist"
    if not dist.is_dir():
        return [Finding("error", "dist", "build", "dist/ missing; run tools/build.py")]
    return [
        Finding("error", str(p.relative_to(root)), "size", f"{p.stat().st_size} bytes")
        for p in dist.rglob("*.md")
        if p.stat().st_size > MAX_PAGE_BYTES and not BULK_FILE_RE.search(p.name)
    ]


def lint_git_identity(root: Path) -> list[Finding]:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
        ).stdout.strip()

    out = []
    # The commit about to be made uses the configured identity.
    who = f"{git('config', 'user.name')} <{git('config', 'user.email')}>"
    if who != ALLOWED_IDENTITY:
        out.append(Finding("error", "git config", "identity", who))
    log = git("log", "--format=%h%x09%an <%ae>%x09%cn <%ce>")
    for row in filter(None, log.splitlines()):
        sha, author, committer = row.split("\t")
        for role, ident in (("author", author), ("committer", committer)):
            if ident != ALLOWED_IDENTITY:
                out.append(Finding("error", f"commit {sha}", f"{role} identity", ident))
    return out


def run(root: Path = ROOT, check_git: bool = True) -> list[Finding]:
    dl_path = find_denylist()
    if dl_path is None:
        return [Finding("error", "denylist", "config", "no denylist found; failing closed")]
    denylist = load_denylist(dl_path)
    findings: list[Finding] = []
    for p in scan_files(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        findings += lint_text(str(p.relative_to(root)), text, denylist)
    findings += lint_sizes(root)
    if check_git:
        findings += lint_git_identity(root)
    return findings


def main(argv: list[str]) -> int:
    findings = run(check_git="--no-git" not in argv)
    for f in findings:
        print(f, file=sys.stderr)
    errors = sum(f.level == "error" for f in findings)
    warns = len(findings) - errors
    print(f"publish-lint: {errors} errors, {warns} warnings", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
