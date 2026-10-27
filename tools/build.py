"""Build ai.hiina.space from content/ into dist/.

Content kinds:
  content/reports/<slug>.md  versioned reports
  content/pages/<slug>.md    site pages served at the root (/about.md)

Every published Markdown file gets an HTML twin (`<path>/index.html`, no JS).
Reports longer than SPLIT_BYTES are split at their H2 headings: the report URL
becomes a short overview (metadata, lede, contents, first section) and each
section gets its own page, because fetch tools pass only the first ~40K
characters through verbatim. The whole report stays available as one file at
`/reports/<slug>/full.md` and immutably at `/reports/<slug>/v<N>.md` (frozen into
the committed versions/ directory on first build).

Derived files: index.md (= llms.txt), recent.md, feed.xml, topics/*.md,
robots.txt, sitemap.xml, corpus.tar.gz, manifest.json. `--lint` runs
publish_lint after building.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
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
# Claude Code's WebFetch passed ~39.4K characters verbatim in the phase 0 test.
SPLIT_BYTES = 30_000

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
    "pages": ["title"],
}


@dataclass
class Source:
    src: Path
    meta: dict
    body: str
    kind: str
    slug: str

    @property
    def path(self) -> str:
        return self.slug if self.kind == "pages" else f"{self.kind}/{self.slug}"

    @property
    def md_url(self) -> str:
        return f"{BASE}/{self.path}.md"

    @property
    def title(self) -> str:
        return str(self.meta["title"])

    @property
    def updated(self) -> str:
        return fmt(self.meta.get("updated", ""))


@dataclass
class Section:
    number: int
    heading: str  # without the leading "## "
    slug: str
    body: str  # including its own "## " heading line

    def path(self, report: Source) -> str:
        return f"{report.path}/{self.slug}"


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.index("\n---\n", 4)
    meta = yaml.safe_load(text[4:end]) or {}
    return meta, text[end + 5 :].lstrip("\n")


def load_sources() -> list[Source]:
    out = []
    for src in sorted(CONTENT.glob("*/*.md")):
        meta, body = split_frontmatter(src.read_text(encoding="utf-8"))
        kind = src.parent.name
        missing = [k for k in REQUIRED.get(kind, ["title"]) if k not in meta]
        if missing:
            raise ValueError(f"{src}: missing frontmatter {missing}")
        out.append(Source(src=src, meta=meta, body=body, kind=kind, slug=src.stem))
    return out


def fmt(v: object) -> str:
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def slugify(text: str, words: int = 7) -> str:
    text = re.sub(r"^\d+\.\s*", "", text)
    parts = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(parts[:words]) or "section"


def strip_leading_h1(body: str) -> str:
    """The metadata header supplies the H1; drop the source's own if present."""
    first, _, rest = body.partition("\n")
    return rest.lstrip("\n") if first.startswith("# ") else body


def split_sections(body: str) -> tuple[str, list[Section]]:
    """Split at H2 headings outside code fences; returns (lede, sections)."""
    chunks: list[list[str]] = [[]]
    fence = False
    for line in body.splitlines(keepends=True):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and line.startswith("## "):
            chunks.append([])
        chunks[-1].append(line)
    lede = "".join(chunks[0]).strip() + "\n"
    sections = []
    for i, chunk in enumerate(chunks[1:], 1):
        heading = chunk[0][3:].strip()
        num = re.match(r"(\d+)\.", heading)
        slug = (f"{int(num[1]):02d}-" if num else "") + slugify(heading)
        sections.append(Section(i, heading, slug, "".join(chunk).strip() + "\n"))
    return lede, sections


def frontmatter(meta: dict) -> str:
    clean = {k: fmt(v) if isinstance(v, date) else v for k, v in meta.items()}
    return "---\n" + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True) + "---\n\n"


FOOTER = f"\n---\n\n{LICENSE_LINE} Source: {REPO_URL}\n"


def report_header(rep: Source, full_bytes: int | None) -> str:
    m = rep.meta
    lines = [
        f"# {rep.title}",
        "",
        f"- Author: {m['author']} (hiina@hiina.space)",
        f"- Produced by: {m['produced-by']}",
        f"- Version: {m['version']} · published {fmt(m['published'])} · "
        f"updated {fmt(m['updated'])} · status: {m['status']}",
        f"- Canonical: {rep.md_url} (this version as one file: "
        f"{BASE}/{rep.path}/v{m['version']}.md)",
        f"- Takeaway: {m['takeaway']}",
        f"- Topics: {', '.join(topic_link(t) for t in m['topics'])}",
    ]
    # Optional provenance (report Section 8): model id, run id, evidence date.
    for key, label in (
        ("model", "Model"),
        ("run", "Run"),
        ("sources-through", "Sources through"),
    ):
        if key in m:
            lines.append(f"- {label}: {fmt(m[key])}")
    if full_bytes is not None:
        lines.append(
            f"- Whole report as one file ({full_bytes // 1000} KB; fetch tools may truncate "
            f"it, so prefer the section pages below or download with curl): "
            f"{BASE}/{rep.path}/full.md"
        )
    return "\n".join(lines) + "\n"


# Topics get a page only once two reports share them; until then a link is a wasted hop.
TOPIC_PAGES: set[str] = set()


def topic_link(topic: str) -> str:
    return f"[{topic}]({BASE}/topics/{topic}.md)" if topic in TOPIC_PAGES else topic


def render_report_full(rep: Source) -> str:
    body = strip_leading_h1(rep.body).rstrip() + "\n"
    return frontmatter(rep.meta) + f"{POINTER}\n\n{report_header(rep, None)}\n{body}{FOOTER}"


def render_report_overview(
    rep: Source, lede: str, sections: list[Section], full_bytes: int
) -> str:
    contents = ["## Contents", ""]
    for i, s in enumerate(sections):
        size = len(s.body.encode()) // 1000 or 1
        where = "included below" if i == 0 else f"{size} KB"
        contents.append(f"- [{s.heading}]({BASE}/{s.path(rep)}.md) ({where})")
    first = sections[0].body if sections else ""
    nxt = f"\nNext section: {BASE}/{sections[1].path(rep)}.md\n" if len(sections) > 1 else ""
    return (
        frontmatter(rep.meta | {"sections": len(sections)})
        + f"{POINTER}\n\n{report_header(rep, full_bytes)}\n{lede}\n"
        + "\n".join(contents)
        + f"\n\n{first}{nxt}{FOOTER}"
    )


def render_section(rep: Source, sections: list[Section], i: int) -> str:
    s = sections[i]
    m = rep.meta
    nav = [
        f"- Section {s.number} of {len(sections)} of the report "
        f'"{rep.title}" by {m["author"]} (v{m["version"]}, updated {fmt(m["updated"])})',
        f"- Report overview and contents: {rep.md_url}",
    ]
    if i > 0:
        nav.append(f"- Previous: {BASE}/{sections[i - 1].path(rep)}.md")
    if i + 1 < len(sections):
        nav.append(f"- Next: {BASE}/{sections[i + 1].path(rep)}.md")
    fm = {
        "id": f"{m['id']}/{s.slug}",
        "title": f"{rep.title}: {s.heading}",
        "report": rep.md_url,
        "section": s.number,
        "version": m["version"],
        "updated": m["updated"],
        "author": m["author"],
    }
    return (
        frontmatter(fm)
        + f"{POINTER}\n\n# {rep.title}: {s.heading}\n\n"
        + "\n".join(nav)
        + f"\n\n{s.body}{FOOTER}"
    )


def render_page(page: Source) -> str:
    body = strip_leading_h1(page.body).rstrip() + "\n"
    return frontmatter(page.meta) + f"{POINTER}\n\n# {page.title}\n\n{body}{FOOTER}"


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
        f'<link rel=alternate type="application/atom+xml" href="{BASE}/feed.xml">'
        f"<style>{CSS}</style></head><body>\n"
        f'<p class=meta>Markdown version: <a href="{u}">{u}</a> · '
        f'<a href="{BASE}/">index</a></p>\n'
        f"{frag}\n</body></html>\n"
    )


def reports_by_date(sources: list[Source]) -> list[Source]:
    return sorted(
        (s for s in sources if s.kind == "reports"), key=lambda s: s.updated, reverse=True
    )


def all_topics(sources: list[Source]) -> dict[str, list[Source]]:
    topics: dict[str, list[Source]] = {}
    for rep in reports_by_date(sources):
        for t in rep.meta["topics"]:
            topics.setdefault(str(t), []).append(rep)
    return dict(sorted(topics.items()))


def report_line(rep: Source) -> str:
    return (
        f"- [{rep.title}]({rep.md_url}) — {rep.meta['takeaway']} "
        f"(v{rep.meta['version']}, {rep.updated})"
    )


def build_index(sources: list[Source]) -> str:
    out = ["# ai.hiina.space", "", SITE_BLURB, "", "## Reports", ""]
    out += [report_line(r) for r in reports_by_date(sources)]
    out += ["", "## Navigate", ""]
    out += [
        f"- Recently added or updated: {BASE}/recent.md (Atom: {BASE}/feed.xml)",
        f"- How this site is produced and what it leaves out: {BASE}/about.md",
    ]
    if TOPIC_PAGES:
        out.append("- Topics: " + ", ".join(topic_link(t) for t in sorted(TOPIC_PAGES)))
    out += [
        "",
        "## Bulk access",
        "",
        f"- Tarball of all Markdown: {BASE}/corpus.tar.gz",
        f"- Manifest (path to sha256, build time): {BASE}/manifest.json",
        f"- Git repository: {REPO_URL} (`git clone --depth 1`; sources are in "
        "`content/`, unsplit; the served tree with section pages is the tarball)",
        "- Verify: `sha256sum` each file against manifest.json; the tarball and git tags "
        "are not signed.",
        "",
        "## Conventions",
        "",
        "- Append `.md` to any page path for Markdown, or send `Accept: text/markdown`.",
        "- Long reports are split into section pages; each report's `.md` URL is an "
        "overview with absolute links to its sections.",
        "- Report URLs without a version track the latest version; "
        "`/reports/<slug>/v<N>.md` never changes.",
        f"- Content signals: {CONTENT_SIGNAL}.",
        f"- {LICENSE_LINE}",
        "",
    ]
    return "\n".join(out)


def build_recent(sources: list[Source]) -> str:
    out = [f"{POINTER}", "", "# Recently added or updated", ""]
    out += [report_line(r) for r in reports_by_date(sources)]
    return "\n".join(out) + "\n"


def build_topic(topic: str, reports: list[Source]) -> str:
    out = [f"{POINTER}", "", f"# Topic: {topic}", ""]
    out += [report_line(r) for r in reports]
    return "\n".join(out) + "\n"


def build_feed(sources: list[Source], built: str) -> str:
    entries = []
    for rep in reports_by_date(sources):
        entries.append(
            "<entry>"
            f"<title>{html.escape(rep.title)}</title>"
            f'<link href="{html.escape(rep.md_url)}"/>'
            f"<id>{html.escape(rep.md_url)}#v{rep.meta['version']}</id>"
            f"<updated>{rep.updated}T00:00:00Z</updated>"
            f"<summary>{html.escape(str(rep.meta['takeaway']))}</summary>"
            "</entry>"
        )
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        f"<title>ai.hiina.space</title><id>{BASE}/</id>"
        f'<link href="{BASE}/"/><link rel="self" href="{BASE}/feed.xml"/>'
        f"<updated>{built}</updated><author><name>Hiina</name>"
        "<email>hiina@hiina.space</email></author>" + "".join(entries) + "</feed>\n"
    )


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


VERSIONS = ROOT / "versions"


def frozen_version(rep: Source, full: str) -> str:
    """Return the immutable `v<N>.md` text, freezing it into versions/ on first build.

    A frozen file records the sha256 of the source it was built from. If the source
    changes while the version number stays the same, the build fails: bump `version`.
    """
    path = VERSIONS / rep.path / f"v{rep.meta['version']}.md"
    src_sha = sha256(rep.src)
    if path.exists():
        meta, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if meta.get("source-sha256") != src_sha:
            raise SystemExit(
                f"{rep.src.relative_to(ROOT)} changed but version {rep.meta['version']} is "
                f"already frozen in {path.relative_to(ROOT)}; bump `version` (and `updated`)"
            )
        return path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(full)
    text = frontmatter(meta | {"source-sha256": src_sha}) + body
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


class Site:
    def __init__(self) -> None:
        self.md_files: list[str] = []
        self.urls: list[str] = [f"{BASE}/", INDEX_URL]

    def page(self, path: str, md: str, title: str, html_too: bool = True) -> None:
        """Write `<path>.md` and, unless suppressed, its HTML twin `<path>/index.html`."""
        write(f"{path}.md", md)
        self.md_files.append(f"{path}.md")
        self.urls.append(f"{BASE}/{path}.md")
        if html_too:
            write(f"{path}/index.html", pandoc_html(md, title, f"{BASE}/{path}.md"))
            self.urls.append(f"{BASE}/{path}/")


def build() -> list[Source]:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    built = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    sources = load_sources()
    TOPIC_PAGES.clear()
    TOPIC_PAGES.update(t for t, reps in all_topics(sources).items() if len(reps) >= 2)
    site = Site()

    for src in sources:
        if src.kind == "pages":
            site.page(src.path, render_page(src), src.title)
            continue
        full = render_report_full(src)
        full_bytes = len(full.encode())
        site.page(
            f"{src.path}/v{src.meta['version']}",
            frozen_version(src, full),
            src.title,
            html_too=False,
        )
        lede, sections = split_sections(strip_leading_h1(src.body))
        if full_bytes <= SPLIT_BYTES or len(sections) < 2:
            site.page(src.path, full, src.title)
            continue
        site.page(f"{src.path}/full", full, src.title, html_too=False)
        site.page(src.path, render_report_overview(src, lede, sections, full_bytes), src.title)
        for i, s in enumerate(sections):
            site.page(
                s.path(src), render_section(src, sections, i), f"{src.title}: {s.heading}"
            )

    site.page("recent", build_recent(sources), "Recently added or updated")
    for topic, reps in all_topics(sources).items():
        if topic in TOPIC_PAGES:
            site.page(f"topics/{topic}", build_topic(topic, reps), f"Topic: {topic}")

    index_md = build_index(sources)
    write("index.md", index_md)
    write("llms.txt", index_md)
    site.md_files.append("index.md")
    write("index.html", pandoc_html(index_md, "ai.hiina.space", INDEX_URL))
    write(
        "404.html",
        html_shell(
            "Not found",
            f"<h1>Not found</h1><p>Index: <a href='{INDEX_URL}'>{INDEX_URL}</a></p>",
            INDEX_URL,
        ),
    )
    write("feed.xml", build_feed(sources, built))
    write("robots.txt", robots())
    write("sitemap.xml", sitemap(site.urls))
    write("corpus.tar.gz", deterministic_tarball(site.md_files))

    files = sorted(str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file())
    manifest = {
        "site": BASE,
        "built": built,
        "files": {f: sha256(DIST / f) for f in files},
    }
    write("manifest.json", json.dumps(manifest, indent=2) + "\n")
    return sources


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lint", action="store_true", help="run publish_lint after building")
    args = ap.parse_args()
    sources = build()
    print(f"built {len(sources)} sources into {DIST}")
    if args.lint:
        sys.path.insert(0, str(Path(__file__).parent))
        import publish_lint

        return publish_lint.main([])
    return 0


if __name__ == "__main__":
    sys.exit(main())
