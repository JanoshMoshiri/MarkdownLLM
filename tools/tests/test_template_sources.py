"""Framework birth-source checks: defects should fail before scaffolding."""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.coherence import template_source_findings  # noqa: E402
from markdownllm.model import SEV_ERROR  # noqa: E402


def _schema(root: Path) -> None:
    p = root / "templates" / "_schema.yaml.template"
    p.parent.mkdir(parents=True)
    p.write_text("schema_version: 1\ndomain: sample\nrelations: [informs]\n",
                 encoding="utf-8")


def test_comments_before_frontmatter_and_invalid_reserved_status_are_errors(tmp_path):
    _schema(tmp_path)
    p = tmp_path / "evidence" / "record.md.template"
    p.parent.mkdir()
    p.write_text("# comment\n---\nid: x\ntype: artifact\nstatus: draft\n"
                 "created: 2026-01-01\n---\n\n# X\n", encoding="utf-8")
    found = template_source_findings(tmp_path)
    assert sum(f.severity == SEV_ERROR for f in found) == 2
    assert any("content before" in f.message for f in found)
    assert any("reserved type" in f.message for f in found)


def test_relation_choices_must_exist_in_the_scaffold_schema(tmp_path):
    _schema(tmp_path)
    p = tmp_path / "templates" / "insight.md.template"
    p.write_text("---\nid: x\ntype: insight\nstatus: active\n"
                 "created: 2026-01-01\nlinked_things:\n  - id: y\n"
                 "    relation: informs|supports\n---\n\n# X\n", encoding="utf-8")
    found = template_source_findings(tmp_path)
    assert any("supports" in f.message for f in found)


def test_current_framework_birth_sources_are_clean():
    root = Path(__file__).resolve().parents[2]
    assert template_source_findings(root) == []


def test_birth_sources_have_checkout_stable_lf_bytes():
    root = Path(__file__).resolve().parents[2]
    paths = sorted(
        path.relative_to(root).as_posix()
        for holder in (root / "templates", root / "tools" / "tests" / "fixtures")
        for path in holder.rglob("*")
        if path.is_file()
    )
    checked = subprocess.run(
        ["git", "-C", str(root), "check-attr", "eol", "--", *paths],
        capture_output=True,
        text=True,
    )
    assert checked.returncode == 0, checked.stderr
    rows = checked.stdout.splitlines()
    assert len(rows) == len(paths)
    assert all(row.endswith(": eol: lf") for row in rows), rows
