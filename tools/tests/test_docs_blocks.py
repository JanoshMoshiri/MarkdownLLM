"""docs_blocks — the derived blocks in the human-facing docs, and the checks
over their authored halves (public-docs-face-build Phase 1).

Two kinds of test. Unit tests build a throwaway framework root so each check
is exercised against a surface it can be made to fail on. One dogfood test
runs the live check over this repository's own docs — the same call the
pre-commit coherence leg makes — because a generator whose own output is
allowed to drift proves nothing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import _ns  # noqa: E402
from markdownllm import docs_blocks as db  # noqa: E402
from markdownllm.model import SEV_ERROR, SEV_WARNING  # noqa: E402

FW_ROOT = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------- the CLI inventory


def test_subcommand_rows_cover_the_parser_alphabetically_without_help_flags():
    from markdownllm.cli import build_cli
    parser = build_cli()
    subs = next(a for a in parser._actions
                if a.__class__.__name__ == "_SubParsersAction")
    rows = db.subcommand_rows()
    assert [r.name for r in rows] == sorted(subs.choices), (
        "every registered subcommand, alphabetical — registration order is a "
        "code-layout fact a derived surface must not drift on")
    for r in rows:
        assert r.usage.startswith(f"mdllm {r.name}"), r
        assert "[-h]" not in r.usage, r
        assert "\n" not in r.usage and "\n" not in r.help, r


def test_toolbox_block_is_deterministic_and_table_safe():
    one = db._db_toolbox(FW_ROOT, None)
    two = db._db_toolbox(FW_ROOT, None)
    assert one == two
    lines = one.splitlines()
    assert lines[0] == "| Subcommand | Usage | The tool's own description |"
    assert len(lines) == 2 + len(db.subcommand_rows())
    for line in lines[2:]:
        # a raw pipe inside a cell would split the row; the builder escapes it
        assert line.count("|") - line.count("\\|") == 4, line


# --------------------------------------------------------------- the spec layer


def _spec(root: Path, rel: str, *, id_: str, typ: str, status: str,
          links: list[tuple[str, str]] = ()) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    lt = "".join(f"  - id: {t}\n    relation: {r}\n" for r, t in links)
    p.write_text(
        f"---\nid: {id_}\ntype: {typ}\nstatus: {status}\ncreated: 2026-09-22\n"
        + (f"linked_things:\n{lt}" if lt else "")
        + f"---\n\n# {id_}\n\nBody.\n", encoding="utf-8")


def _tiny_root(tmp_path: Path) -> Path:
    root = tmp_path / "fw"
    root.mkdir()
    (root / ".markdownllm").write_text(
        "framework: T\nversion: 0.0.1\nrole: canonical-version-sentinel\n",
        encoding="utf-8")
    _spec(root, "thing.md", id_="thing-specification", typ="specification",
          status="evolving")
    _spec(root, "trigger-specification.md", id_="trigger-specification",
          typ="specification", status="stable",
          links=[("extends", "thing-specification"),
                 ("references", "some-insight")])
    _spec(root, "docs/first-hour.md", id_="first-hour-guide", typ="guide",
          status="draft", links=[("complements", "thing-specification")])
    _spec(root, "things-are-not-specs.md", id_="plan-x", typ="plan",
          status="not-started")
    return root


def test_spec_set_reads_frontmatter_type_not_filename_or_location(tmp_path):
    root = _tiny_root(tmp_path)
    specs = db.spec_set(root)
    assert [s.rel for s in specs] == [
        "docs/first-hour.md", "thing.md", "trigger-specification.md"]
    by_rel = {s.rel: s for s in specs}
    assert by_rel["thing.md"].id == "thing-specification"
    assert by_rel["docs/first-hour.md"].type == "guide"
    assert by_rel["trigger-specification.md"].edges == (
        ("extends", "thing-specification"), ("references", "some-insight"))
    assert "the manifesto" not in by_rel["thing.md"].label_keys
    assert {"thing.md", "thing"} <= by_rel["thing.md"].label_keys


def test_spec_edges_block_names_spec_targets_and_counts_the_rest(tmp_path):
    root = _tiny_root(tmp_path)
    body = db._db_spec_edges(root, None)
    lines = body.splitlines()
    assert lines[0].startswith("- **`docs/first-hour.md`** (`guide`, `draft`): complements → `thing.md`")
    assert "- **`thing.md`** (`specification`, `evolving`): no edges to other specs" in lines
    trig = next(l for l in lines if l.startswith("- **`trigger-specification.md`**"))
    assert "extends → `thing.md`" in trig
    assert "+1 edge(s) outside the spec layer" in trig
    assert "some-insight" not in trig, "non-spec targets are counted, never named"


# --------------------------------------------------------------- the authored halves


def _when(names: list[str]) -> str:
    return db.WHEN_HEADING + "\n\n" + "".join(
        f"- **`{n}`** — when you'd type {n}.\n" for n in names) + "\n### Next\n"


def test_when_bullets_are_checked_both_ways():
    names = {"validate", "kernel", "docs"}
    assert db._toolbox_findings(_when(["validate", "kernel", "docs"]), names) == []

    missing = db._toolbox_findings(_when(["validate", "kernel"]), names)
    assert [f.severity for f in missing] == [SEV_ERROR]
    assert "`docs` has no authored line" in missing[0].message

    ghost = db._toolbox_findings(_when(["validate", "kernel", "docs", "orient"]), names)
    assert [f.severity for f in ghost] == [SEV_ERROR]
    assert "`orient`, which is not an mdllm subcommand" in ghost[0].message


def test_when_bullets_absent_heading_is_could_not_look_not_all_clear():
    out = db._toolbox_findings("# A guide with no toolbox section\n", {"validate"})
    assert [f.severity for f in out] == [SEV_WARNING]


def _map(view2_nodes: list[str], view3_nodes: list[str]) -> str:
    v2 = "\n".join(f'    N{i}["{label}"]' for i, label in enumerate(view2_nodes))
    v3 = "\n".join(f'        C{i}["{label}"]' for i, label in enumerate(view3_nodes))
    return (
        "# Map\n\n## View 2 — specs\n\n```mermaid\nflowchart TD\n"
        f"{v2}\n```\n\n## View 3 — floor\n\n```mermaid\nflowchart LR\n"
        f"    subgraph cli [\"mdllm subcommand\"]\n{v3}\n    end\n"
        "    subgraph target [\"what it serves\"]\n        T1[\"x.md\"]\n    end\n"
        "```\n")


def test_view3_subcommand_nodes_are_checked_both_ways():
    names = {"validate", "docs"}
    ok = _map([], ["validate", "docs"])
    assert db._view3_findings(ok, names) == []

    missing = db._view3_findings(_map([], ["validate"]), names)
    assert [f.severity for f in missing] == [SEV_ERROR]
    assert "no node for subcommand `docs`" in missing[0].message

    ghost = db._view3_findings(_map([], ["validate", "docs", "orient"]), names)
    assert "draws `orient`, which is not an mdllm subcommand" in ghost[0].message

    # a <br/> annotation on the label is display, not identity
    annotated = _map([], ['validate', 'docs<br/>(internal)'])
    assert db._view3_findings(annotated, names) == []


def test_view2_every_spec_has_a_node_and_status_tags_must_match(tmp_path):
    root = _tiny_root(tmp_path)
    specs = db.spec_set(root)

    complete = _map(["thing.md", "trigger-specification (stable)",
                     "first-hour"], [])
    assert db._view2_findings(complete, specs) == []

    missing = db._view2_findings(_map(["thing.md", "first-hour"], []), specs)
    assert [f.severity for f in missing] == [SEV_ERROR]
    assert "no node for `trigger-specification.md`" in missing[0].message

    wrong = db._view2_findings(
        _map(["thing.md", "trigger-specification (draft)", "first-hour"], []),
        specs)
    assert [f.severity for f in wrong] == [SEV_ERROR]
    assert "tags `trigger-specification` as `(draft)`" in wrong[0].message
    assert "is `stable`" in wrong[0].message

    # absence of a tag is not a claim; an unrecognised node is not an error
    loose = _map(["thing.md<br/>the atom", "trigger-specification",
                  "first-hour", "the manifesto"], [])
    assert db._view2_findings(loose, specs) == []


# --------------------------------------------------------------- drift, end to end


def _docs_pair(root: Path) -> None:
    names = [r.name for r in db.subcommand_rows()]
    (root / "docs").mkdir(exist_ok=True)
    (root / db.OPERATOR_GUIDE).write_text(
        "---\nid: operator-guide\ntype: guide\nstatus: draft\ncreated: 2026-09-22\n---\n\n"
        "# Guide\n\n<!-- generated:toolbox -->\n\n<!-- /generated:toolbox -->\n\n"
        + _when(names), encoding="utf-8")
    # The pair are guides themselves, so they join the spec layer the moment
    # they exist — the map must draw them too (the guide is on disk by now;
    # the map cannot list itself before it is written, so name it).
    v2 = sorted({s.basename for s in db.spec_set(root)} | {"framework-map.md"})
    (root / db.FRAMEWORK_MAP).write_text(
        "---\nid: framework-map\ntype: guide\nstatus: draft\ncreated: 2026-09-22\n---\n\n"
        + _map(v2, names)
        + "\n### Edges\n\n<!-- generated:spec-edges -->\n\n<!-- /generated:spec-edges -->\n",
        encoding="utf-8")


def test_generation_clears_drift_and_a_hand_edit_inside_a_block_restores_it(
        tmp_path, capsys):
    root = _tiny_root(tmp_path)
    _docs_pair(root)

    # Empty blocks: missing bodies are drift.
    before = [f for f in db.docs_block_findings(root) if f.severity == SEV_ERROR]
    assert before and all("drifted" in f.message for f in before), before

    assert db.cmd_docs(_ns(path=str(root), check=False)) == 0
    capsys.readouterr()
    assert db.docs_block_findings(root) == []
    assert db.cmd_docs(_ns(path=str(root), check=True)) == 0
    out = capsys.readouterr().out
    assert "in sync" in out and "2 block(s)" in out

    # Someone "fixes" a row by hand inside the block.
    guide = root / db.OPERATOR_GUIDE
    guide.write_text(guide.read_text(encoding="utf-8").replace(
        "| `validate` |", "| `validate` (please run me) |", 1), encoding="utf-8")
    drift = [f for f in db.docs_block_findings(root) if f.severity == SEV_ERROR]
    assert len(drift) == 1 and "`toolbox` drifted" in drift[0].message
    assert db.cmd_docs(_ns(path=str(root), check=True)) == 1
    capsys.readouterr()


def test_a_missing_block_marker_is_named_not_skipped(tmp_path, capsys):
    root = _tiny_root(tmp_path)
    _docs_pair(root)
    fmap = root / db.FRAMEWORK_MAP
    fmap.write_text(fmap.read_text(encoding="utf-8").replace(
        "<!-- generated:spec-edges -->\n\n<!-- /generated:spec-edges -->\n", ""),
        encoding="utf-8")
    db.cmd_docs(_ns(path=str(root), check=False))
    capsys.readouterr()
    findings = [f for f in db.docs_block_findings(root) if f.severity == SEV_ERROR]
    assert any("managed block `spec-edges` is missing" in f.message for f in findings)


# --------------------------------------------------------------- dogfood


def test_this_repositorys_own_docs_are_in_sync():
    """The same call the pre-commit coherence leg makes, over the live docs.
    A generator whose own output may drift proves nothing."""
    errors = [f for f in db.docs_block_findings(FW_ROOT) if f.severity == SEV_ERROR]
    assert errors == [], "\n".join(f"{f.thing}: {f.message}" for f in errors)
