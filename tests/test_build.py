import build


def test_strip_leading_h1():
    assert build.strip_leading_h1("# T\n\nbody") == "body"
    assert build.strip_leading_h1("body\n# T") == "body\n# T"


def test_split_frontmatter():
    meta, body = build.split_frontmatter("---\ntitle: X\n---\n\nhello\n")
    assert meta == {"title": "X"}
    assert body == "hello\n"
