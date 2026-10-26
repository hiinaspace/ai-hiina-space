import re

import publish_lint as pl

DENY = [("natto", re.compile(r"(?<!\w)natto(?!\w)", re.IGNORECASE))]


def rules(text: str) -> list[str]:
    return [f.rule for f in pl.lint_text("x", text, DENY) if f.level == "error"]


def test_denylist_word_boundary():
    assert rules("ran on Natto last night") == ["denylist"]
    assert rules("nattokinase supplement") == []


def test_email_allowlist():
    assert rules("mail hiina@hiina.space") == []
    assert rules("mail someone@example.org") == ["email"]
    assert rules("see https://medium.com/@author/post") == []


def test_paths_ips_and_private_links():
    assert rules("in ~/code/foo") == ["home path"]
    assert rules("host 192.168.1.20 and 10.0.0.5") == ["private IPv4"]
    assert rules("public 8.8.8.8") == []
    assert rules("https://claude.ai/artifact/abc") == ["private claude.ai link"]


def test_second_person_is_warning_only():
    found = pl.lint_text("x", "runs on your homelab", DENY)
    assert [f.level for f in found] == ["warn"]
