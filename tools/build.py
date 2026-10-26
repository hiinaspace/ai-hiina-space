"""Build ai.hiina.space from content/ into dist/.

Every content page becomes:
  dist/<path>.md          Markdown with frontmatter, pointer line and metadata header
  dist/<path>/index.html  minimal no-JS HTML view (pandoc)
  dist/<path>/v<N>.md     immutable copy for versioned content (reports)

Plus derived files: index.md (= llms.txt), index.html, robots.txt, sitemap.xml,
corpus.tar.gz and manifest.json. `--lint` runs publish_lint after building.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import io
import json
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
BASE = "https://ai.hiina.space"
INDEX_URL = f"{BASE}/index.md"
POINTER = f"Index of everything on this site: {INDEX_URL}"
REPO_URL = "https://github.com/hiinaspace/ai-hiina-space"
CONTENT_SIGNAL = "search=yes, ai-input=yes, ai-train=yes"
LICENSE_LINE = "Text licensed CC BY 4.0 (attribution: Hiina, ai.hiina.space)."

SITE_BLURB = (
    "ai.hiina.space publishes agent-written research reports and project status from "
    "Hiina (hiina@hiina.space) as small Markdown files meant to be read by AI agents. "
    "Every page is available as Markdown at a `.md` URL, and the whole corpus is "
    "downloadable as a tarball or clonable as a git repository."
)

CSS = """
body{max-width:46rem;margin:2rem auto;padding:0 1rem;font:16px/1.55 system-ui,sans-serif;
color:#1d1d1f;background:#fff}
@media (prefers-color-scheme:dark){body{color:#e6e6e6;background:#151515}a{color:#8ab4ff}}
pre,code{font-size:.9em}pre{overflow-x:auto}table{border-collapse:collapse;display:block;
overflow-x:auto}td,th{border:1px solid #8884;padding:.25rem .5rem;vertical-align:top}
.meta{font-size:.9em;opacity:.8}
""".strip()


@dataclass
class Page:
    src: Path
    meta: dict
    body: str
    kind: str  # "reports" | "projects" | ...
    slug: str
    extra_files: list[str] = field(default_factory=list)

    @property
    def path(self) -> str:
        return f"{self.kind}/{self.slug}"

    @property
    def md_url(self) -> str:
        return f"{BASE}/{self.path}.md"

    @property
    def html_url(self) -> str:
        return f"{BASE}/{self.path}/"

    @property
    def title(self) -> str:
        return str(self.meta["title"])


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.index("\n---\n", 4)
    meta = yaml.safe_load(text[4:end]) or {}
    return meta, text[end + 5 :].lstrip("\n")


REQUIRED = {
    "reports": [
        "id",
        "title",
        "version",
        "published",
        "updated",
        "author",
        "produced-by",
        "status",
        "takeaway",
        "topics",
    ],
}


def load_pages() -> list[Page]:
    pages = []
    for src in sorted(CONTENT.glob("*/*.md")):
        meta, body = split_frontmatter(src.read_text(encoding="utf-8"))
        kind = src.parent.name
        missing = [k for k in REQUIRED.get(kind, ["title"]) if k not in meta]
        if missing:
            raise ValueError(f"{src}: missing frontmatter {missing}")
        pages.append(Page(src=src, meta=meta, body=body, kind=kind, slug=src.stem))
    return pages


def fmt(v: object) -> str:
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def metadata_header(page: Page) -> str:
    """In-body metadata: fetch tools strip HTTP headers and frontmatter may not survive."""
    m = page.meta
    lines = [f"# {page.title}", ""]
    if page.kind == "reports":
        lines += [
            f"- Author: {m['author']} (hiina@hiina.space)",
            f"- Produced by: {m['produced-by']}",
            f"- Version: {m['version']} · published {fmt(m['published'])} · "
            f"updated {fmt(m['updated'])} · status: {m['status']}",
            f"- Canonical: {page.md_url} (this version: {BASE}/{page.path}/v{m['version']}.md)",
            f"- Takeaway: {m['takeaway']}",
            f"- Topics: {fmt(m['topics'])}",
        ]
    lines.append("")
    return "\n".join(lines)


def strip_leading_h1(body: str) -> str:
    """The metadata header supplies the H1; drop the source's own if present."""
    first, _, rest = body.partition("\n")
    return rest.lstrip("\n") if first.startswith("# ") else body


def render_md(page: Page) -> str:
    fm = yaml.safe_dump(
        {k: fmt(v) if isinstance(v, date) else v for k, v in page.meta.items()},
        sort_keys=False,
        allow_unicode=True,
    )
    body = strip_leading_h1(page.body).rstrip() + "\n"
    footer = f"\n---\n\n{LICENSE_LINE} Source: {REPO_URL}\n"
    return f"---\n{fm}---\n\n{POINTER}\n\n{metadata_header(page)}\n{body}{footer}"


def pandoc_html(markdown: str, title: str, md_url: str) -> str:
    frag = subprocess.run(
        ["pandoc", "--from=gfm-raw_html+yaml_metadata_block", "--to=html5"],
        input=markdown,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return html_shell(title, frag, md_url)


def html_shell(title: str, frag: str, md_url: str) -> str:
    t = html.escape(title)
    u = html.escape(md_url)
    return (
        "<!doctype html>\n<html lang=en><head><meta charset=utf-8>"
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        f"<title>{t}</title>"
        f'<link rel=alternate type="text/markdown" href="{u}">'
        f"<style>{CSS}</style></head><body>\n"
        f'<p class=meta>Markdown version: <a href="{u}">{u}</a> · '
        f'<a href="{BASE}/">index</a></p>\n'
        f"{frag}\n</body></html>\n"
    )


def build_index(pages: list[Page]) -> str:
    reports = sorted(
        (p for p in pages if p.kind == "reports"),
        key=lambda p: fmt(p.meta["updated"]),
        reverse=True,
    )
    out = ["# ai.hiina.space", "", SITE_BLURB, ""]
    out += ["## Reports", ""]
    for p in reports:
        out.append(
            f"- [{p.title}]({p.md_url}) — {p.meta['takeaway']} "
            f"(v{p.meta['version']}, {fmt(p.meta['updated'])})"
        )
    out += [
        "",
        "## Bulk access",
        "",
        f"- Tarball of all Markdown: {BASE}/corpus.tar.gz",
        f"- Manifest (path to sha256, build time): {BASE}/manifest.json",
        f"- Git repository: {REPO_URL}",
        "",
        "## Conventions",
        "",
        "- Append `.md` to any page path for Markdown, or send `Accept: text/markdown`.",
        "- Report URLs without a version track the latest version; "
        "`/reports/<slug>/v<N>.md` never changes.",
        f"- Content signals: {CONTENT_SIGNAL}.",
        f"- {LICENSE_LINE}",
        "",
    ]
    return "\n".join(out)


def robots() -> str:
    return (
        "User-agent: *\nAllow: /\n\n"
        f"Content-Signal: {CONTENT_SIGNAL}\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n"
    )


def sitemap(urls: list[str]) -> str:
    items = "".join(f"<url><loc>{html.escape(u)}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'
    )


def write(rel: str, data: str | bytes) -> None:
    p = DIST / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        p.write_text(data, encoding="utf-8")
    else:
        p.write_bytes(data)


def deterministic_tarball(md_files: list[str]) -> bytes:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for rel in sorted(md_files):
            data = (DIST / rel).read_bytes()
            info = tarfile.TarInfo(f"ai-hiina-space/{rel}")
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))
    gz = io.BytesIO()
    with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0) as f:
        f.write(raw.getvalue())
    return gz.getvalue()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> list[Page]:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    pages = load_pages()
    md_files: list[str] = []
    urls = [f"{BASE}/", INDEX_URL]

    for page in pages:
        md = render_md(page)
        write(f"{page.path}.md", md)
        md_files.append(f"{page.path}.md")
        if page.kind == "reports":
            versioned = f"{page.path}/v{page.meta['version']}.md"
            write(versioned, md)
            md_files.append(versioned)
        write(f"{page.path}/index.html", pandoc_html(md, page.title, page.md_url))
        urls += [page.html_url, page.md_url]

    index_md = build_index(pages)
    write("index.md", index_md)
    write("llms.txt", index_md)
    md_files.append("index.md")
    write("index.html", pandoc_html(index_md, "ai.hiina.space", INDEX_URL))
    write(
        "404.html",
        html_shell(
            "Not found",
            f"<h1>Not found</h1><p>Index: <a href='{INDEX_URL}'>{INDEX_URL}</a></p>",
            INDEX_URL,
        ),
    )
    write("robots.txt", robots())
    write("sitemap.xml", sitemap(urls))
    write("corpus.tar.gz", deterministic_tarball(md_files))

    files = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file())
    manifest = {
        "site": BASE,
        "built": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": {f: sha256(DIST / f) for f in files},
    }
    write("manifest.json", json.dumps(manifest, indent=2) + "\n")
    return pages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lint", action="store_true", help="run publish_lint after building")
    args = ap.parse_args()
    pages = build()
    print(f"built {len(pages)} pages into {DIST}")
    if args.lint:
        sys.path.insert(0, str(Path(__file__).parent))
        import publish_lint

        return publish_lint.main([])
    return 0


if __name__ == "__main__":
    sys.exit(main())
