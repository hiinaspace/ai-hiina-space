from types import SimpleNamespace

import build


def test_strip_leading_h1():
    assert build.strip_leading_h1("# T\n\nbody") == "body"
    assert build.strip_leading_h1("body\n# T") == "body\n# T"


def test_split_frontmatter():
    meta, body = build.split_frontmatter("---\ntitle: X\n---\n\nhello\n")
    assert meta == {"title": "X"}
    assert body == "hello\n"


def test_split_sections_ignores_fenced_headings():
    body = "lede\n\n## 1. One\na\n```\n## not a heading\n```\n## 2. Two words here\nb\n"
    lede, sections = build.split_sections(body)
    assert lede == "lede\n"
    assert [s.slug for s in sections] == ["01-one", "02-two-words-here"]
    assert "## not a heading" in sections[0].body


def test_older_versions_lists_superseded_frozen_files(tmp_path, monkeypatch):
    monkeypatch.setattr(build, "VERSIONS", tmp_path)
    d = tmp_path / "reports" / "x"
    d.mkdir(parents=True)
    for name in ("v1.md", "v2.md", "v3.md", "notes.md"):
        (d / name).write_text("x")
    rep = SimpleNamespace(path="reports/x", meta={"version": 3})
    assert build.older_versions(rep) == [1, 2]  # ty: ignore[invalid-argument-type]
