"""Repository-view and provenance regression tests."""

from __future__ import annotations

import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.mcp_server import (  # noqa: E402
    mcp_build_manifest,
    mcp_get_deliverable,
    mcp_query_things,
    mcp_read_resource,
)
from markdownllm.model import scan  # noqa: E402
from markdownllm.provenance import cmd_provenance  # noqa: E402
from markdownllm.repository_view import (  # noqa: E402
    RepositoryHeadMoved,
    RepositoryView,
    RepositoryViewMode,
)
from markdownllm.session import cmd_session_start  # noqa: E402
from markdownllm.touchpoints import cmd_candidates  # noqa: E402
from markdownllm.validation import cmd_validate  # noqa: E402


for _key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_key, "repository-view-tests")
for _key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_key, "repository-view-tests@local")


def _run(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True,
    ).stdout.strip()


def _write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def _thing(body: str) -> str:
    return (
        "---\n"
        "id: exposed-record\n"
        "type: record\n"
        "status: active\n"
        "created: 2026-08-20\n"
        "exposed: true\n"
        "---\n\n"
        f"# Exposed Record\n\n{body}\n"
    )


def _validation_thing(body: str = "valid") -> str:
    return (
        "---\n"
        "id: validation-target\n"
        "type: note\n"
        "status: in-progress\n"
        "created: 2026-08-20\n"
        "---\n\n"
        f"# Validation Target\n\n{body}\n"
    )


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _run(root, "init", "-q")


def _commit_all(root: Path, message: str) -> str:
    _run(root, "add", "-A")
    _run(root, "commit", "-q", "-m", message)
    return _run(root, "rev-parse", "HEAD")


def test_worktree_index_and_commit_are_distinct_logical_views(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "_schema.yaml", "marker: committed\n")
    _write(root, "things/exposed.md", _thing("committed bytes"))
    head = _commit_all(root, "base")

    _write(root, "_schema.yaml", "marker: candidate\n")
    _write(root, "things/exposed.md", _thing("candidate bytes"))
    _write(root, "things/candidate-only.md", "# Candidate-only file\n")
    _run(root, "add", "_schema.yaml", "things/exposed.md",
         "things/candidate-only.md")
    candidate = RepositoryView.index(root)

    _write(root, "_schema.yaml", "marker: draft\n")
    _write(root, "things/exposed.md", _thing("draft bytes"))
    worktree = RepositoryView.worktree(root)
    committed = RepositoryView.commit(root, "HEAD")

    assert worktree.mode is RepositoryViewMode.WORKTREE
    assert candidate.mode is RepositoryViewMode.INDEX and candidate.immutable
    assert committed.mode is RepositoryViewMode.COMMIT and committed.immutable
    assert committed.commit_sha == head
    assert len(committed.commit_sha) in (40, 64)

    logical = "things/exposed.md"
    assert logical in {p.as_posix() for p in worktree.list_paths(".md")}
    assert "things/candidate-only.md" in {
        p.as_posix() for p in candidate.list_paths(".md")
    }
    assert "things/candidate-only.md" not in {
        p.as_posix() for p in committed.list_paths(".md")
    }
    assert b"draft bytes" in worktree.read_bytes(logical)
    assert b"candidate bytes" in candidate.read_bytes(logical)
    assert b"committed bytes" in committed.read_bytes(logical)

    draft_corpus, _ = scan(root, worktree)
    candidate_corpus, _ = scan(root, candidate)
    committed_corpus, _ = scan(root, committed)
    assert draft_corpus.schema["marker"] == "draft"
    assert candidate_corpus.schema["marker"] == "candidate"
    assert committed_corpus.schema["marker"] == "committed"
    assert "draft bytes" in draft_corpus.things[0].body
    assert "candidate bytes" in candidate_corpus.things[0].body
    assert "committed bytes" in committed_corpus.things[0].body

    # The candidate is a frozen write-tree, not a live alias for the index.
    _run(root, "add", "_schema.yaml", "things/exposed.md")
    assert b"candidate bytes" in candidate.read_bytes(logical)


def test_mcp_full_commit_or_explicit_uncommitted_provenance(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/exposed.md", _thing("committed v1"))
    first = _commit_all(root, "publish v1")
    historical_view = RepositoryView.commit(root, first)
    _write(root, "things/unrelated.md", "# Unrelated non-thing\n")
    current_head = _commit_all(root, "unrelated change")
    assert current_head != first

    clean, _ = scan(root)
    deliverable = mcp_get_deliverable(root, clean, "domain", "exposed-record")
    assert deliverable is not None
    assert deliverable["reference_triple"]["source_commit"] == first
    assert deliverable["source_state"]["state"] == "committed"
    assert len(deliverable["reference_triple"]["source_commit"]) in (40, 64)
    clean_manifest = mcp_build_manifest(root, clean, "domain")
    assert clean_manifest["head_commit"] == current_head
    assert clean_manifest["knows"][0]["source_commit"] == first

    # Windows may materialize CRLF for an LF Git blob.  The porch substitutes
    # the immutable blob before stamping it; line-ending transport is not a
    # dirty provenance claim.
    (root / "things" / "exposed.md").write_bytes(
        _thing("committed v1").replace("\n", "\r\n").encode("utf-8")
    )
    crlf_corpus, _ = scan(root)
    crlf = mcp_get_deliverable(root, crlf_corpus, "domain", "exposed-record")
    assert crlf is not None
    assert crlf["source_state"]["state"] == "committed"
    assert crlf["reference_triple"]["source_commit"] == first
    assert "\r" not in crlf["content"]

    _write(root, "things/exposed.md", _thing("uncommitted v2"))
    dirty, _ = scan(root)
    draft = mcp_get_deliverable(root, dirty, "domain", "exposed-record")
    assert draft is not None and "uncommitted v2" in draft["content"]
    assert draft["source_state"]["state"] == "uncommitted"
    assert draft["source_state"]["base_commit"] == current_head
    assert draft["reference_triple"]["source_commit"] == "uncommitted"

    manifest = mcp_build_manifest(root, dirty, "domain")
    assert manifest["head_commit"] == current_head
    assert manifest["knows"][0]["source_state"] == "uncommitted"
    assert manifest["knows"][0]["source_commit"] == "uncommitted"
    resource = mcp_read_resource(
        root, dirty, "domain", "thing://domain/exposed-record"
    )
    assert resource is not None
    assert resource["sourceState"] == "uncommitted"
    assert resource["sourceCommit"] == "uncommitted"

    # A historical corpus keeps serving the historical bytes and full pin even
    # while the ambient worktree contains a conflicting draft.
    historical, _ = scan(root, historical_view)
    pinned = mcp_get_deliverable(root, historical, "domain", "exposed-record")
    assert pinned is not None and "committed v1" in pinned["content"]
    assert "uncommitted v2" not in pinned["content"]
    assert pinned["source_state"]["state"] == "committed"
    assert pinned["reference_triple"]["source_commit"] == first


def test_mcp_index_candidate_never_claims_a_commit(tmp_path: Path) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/exposed.md", _thing("committed"))
    _commit_all(root, "publish")
    _write(root, "things/exposed.md", _thing("staged candidate"))
    _run(root, "add", "things/exposed.md")

    index_corpus, _ = scan(root, RepositoryView.index(root))
    deliverable = mcp_get_deliverable(
        root, index_corpus, "domain", "exposed-record"
    )
    assert deliverable is not None
    assert deliverable["source_state"]["state"] == "candidate"
    assert deliverable["reference_triple"]["source_commit"] == "uncommitted"


def test_mcp_query_rows_label_worktree_index_and_commit_bytes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/exposed.md", _thing("committed"))
    head = _commit_all(root, "publish")

    # A checkout-only CRLF materialisation is replaced by the committed blob
    # before the row is built and receives the full immutable reference.
    (root / "things" / "exposed.md").write_bytes(
        _thing("committed").replace("\n", "\r\n").encode("utf-8"))
    clean, _ = scan(root)
    clean_row = mcp_query_things(clean)[0]
    assert clean_row["_mcp_source"] == {
        "state": "committed",
        "source_commit": head,
        "view": f"commit:{head}",
    }

    candidate_text = _thing("candidate").replace(
        "status: active", "status: candidate")
    _write(root, "things/exposed.md", candidate_text)
    _run(root, "add", "things/exposed.md")
    candidate_view = RepositoryView.index(root)
    candidate, _ = scan(root, candidate_view)

    draft_text = _thing("draft").replace("status: active", "status: draft")
    _write(root, "things/exposed.md", draft_text)
    draft, _ = scan(root)

    candidate_row = mcp_query_things(candidate)[0]
    assert candidate_row["status"] == "candidate"
    assert candidate_row["_mcp_source"]["state"] == "candidate"
    assert candidate_row["_mcp_source"]["source_commit"] == "uncommitted"
    assert candidate_row["_mcp_source"]["view"] == candidate_view.identifier

    draft_row = mcp_query_things(draft)[0]
    assert draft_row["status"] == "draft"
    assert draft_row["_mcp_source"]["state"] == "uncommitted"
    assert draft_row["_mcp_source"]["source_commit"] == "uncommitted"
    assert draft_row["_mcp_source"]["view"] == "worktree"

    historical_view = RepositoryView.commit(root, head)
    historical, _ = scan(root, historical_view)
    historical_row = mcp_query_things(historical)[0]
    assert historical_row["status"] == "active"
    assert historical_row["_mcp_source"] == {
        "state": "committed",
        "source_commit": head,
        "view": f"commit:{head}",
    }


def _external_input(*, verified: bool, body: str = "source") -> str:
    return (
        "---\n"
        "id: external-input\n"
        "type: note\n"
        "status: active\n"
        "created: 2026-08-20\n"
        "origin: external\n"
        f"verified: {'true' if verified else 'false'}\n"
        "---\n\n"
        f"# External Input\n\n{body}\n"
    )


def _decision(pin: str) -> str:
    return (
        "---\n"
        "id: pinned-decision\n"
        "type: decision\n"
        "status: active\n"
        "created: 2026-08-20\n"
        "informed_by:\n"
        "  - id: external-input\n"
        f"    commit: {pin}\n"
        "---\n\n"
        "# Pinned Decision\n"
    )


def test_provenance_scans_exactly_one_selected_repository_view(
    tmp_path: Path, capsys,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/input.md", _external_input(verified=True))
    source_commit = _commit_all(root, "source")
    _write(root, "things/decision.md", _decision(source_commit))
    decision_commit = _commit_all(root, "decision")

    # The candidate is unverified, while the ambient draft is repaired.  Each
    # invocation must scan only the selected source instead of mixing them.
    _write(root, "things/input.md", _external_input(verified=False))
    _run(root, "add", "things/input.md")
    _write(root, "things/input.md", _external_input(verified=True))

    assert cmd_provenance(Namespace(path=str(root))) == 0
    worktree_output = capsys.readouterr().out
    assert "view: worktree" in worktree_output
    assert "UNVERIFIED" not in worktree_output

    assert cmd_provenance(
        Namespace(path=str(root), view="index", revision=None)) == 1
    index_output = capsys.readouterr().out
    assert "view: index:" in index_output
    assert "pins UNVERIFIED external thing `external-input`" in index_output

    assert cmd_provenance(Namespace(
        path=str(root), view="commit", revision="HEAD")) == 0
    commit_output = capsys.readouterr().out
    assert f"view: commit:{decision_commit}" in commit_output
    assert "UNVERIFIED" not in commit_output
    assert len(decision_commit) in (40, 64)


def test_provenance_commit_drift_stops_at_the_resolved_revision(
    tmp_path: Path, capsys,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/input.md", _external_input(verified=True))
    source_commit = _commit_all(root, "source")
    _write(root, "things/decision.md", _decision(source_commit))
    decision_commit = _commit_all(root, "decision")
    _write(root, "things/input.md", _external_input(
        verified=True, body="later committed revision"))
    later_commit = _commit_all(root, "source changed")

    assert cmd_provenance(Namespace(
        path=str(root), view="commit", revision=decision_commit)) == 0
    old_output = capsys.readouterr().out
    assert f"view: commit:{decision_commit}" in old_output
    assert "changed in" not in old_output

    assert cmd_provenance(Namespace(
        path=str(root), view="commit", revision=later_commit)) == 0
    later_output = capsys.readouterr().out
    assert f"view: commit:{later_commit}" in later_output
    assert "changed in 1 commit(s)" in later_output


def test_provenance_refuses_revision_on_a_mutable_view(
    tmp_path: Path, capsys,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    assert cmd_provenance(Namespace(
        path=str(root), view="worktree", revision="HEAD")) == 1
    assert "--revision is valid only with --view commit" in capsys.readouterr().out


def test_commit_view_scans_nested_corpus_and_detects_head_movement(
    tmp_path: Path,
) -> None:
    root = tmp_path / "framework"
    _init_repo(root)
    _write(root, "examples/sample/AGENTS.md", "# Sample\n")
    _write(root, "examples/sample/_schema.yaml", "marker: nested\n")
    _write(root, "examples/sample/things/record.md", _thing("nested committed"))
    base = _commit_all(root, "nested corpus")

    snapshot = RepositoryView.commit(root)
    nested, findings = scan(root / "examples" / "sample", snapshot)
    assert not findings
    assert nested.view_prefix.as_posix() == "examples/sample"
    assert nested.schema["marker"] == "nested"
    assert [t.id for t in nested.things] == ["exposed-record"]
    assert snapshot.assert_head_unchanged() == base

    _write(root, "unrelated.txt", "moves HEAD\n")
    moved = _commit_all(root, "move head")
    with pytest.raises(RepositoryHeadMoved) as exc:
        snapshot.assert_head_unchanged()
    assert exc.value.expected == base and exc.value.actual == moved


def test_session_long_read_names_full_view_and_refuses_moved_head(
    tmp_path: Path, capsys,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "AGENTS.md", "# Domain\n")
    base = _commit_all(root, "base")

    assert cmd_session_start(Namespace(
        path=str(root), contract=False, assert_head=None,
    )) == 0
    emitted = capsys.readouterr().out
    assert f"Significant-read base:** `commit:{base}`" in emitted
    assert f"--assert-head {base}" in emitted

    assert cmd_session_start(Namespace(
        path=str(root), contract=False, assert_head=base,
    )) == 0
    assert f"long-read view current: commit:{base}" in capsys.readouterr().out

    _write(root, "moved.txt", "concurrent state\n")
    moved = _commit_all(root, "move head")
    assert cmd_session_start(Namespace(
        path=str(root), contract=False, assert_head=base,
    )) == 1
    refused = capsys.readouterr().out
    assert f"expected commit:{base}" in refused
    assert f"current commit:{moved}" in refused

    assert cmd_session_start(Namespace(
        path=str(root), contract=False, assert_head=base[:12],
    )) == 2
    assert "requires one full" in capsys.readouterr().out


def test_index_validation_blocks_invalid_staged_even_if_worktree_repaired(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/target.md", _validation_thing("base"))
    _commit_all(root, "base")

    _write(root, "things/target.md", "---\nid: [unterminated\n---\n# Broken\n")
    _run(root, "add", "things/target.md")
    _write(root, "things/target.md", _validation_thing("repaired draft"))

    assert cmd_validate(Namespace(path=str(root), quiet=True, view="index")) == 1
    assert cmd_validate(Namespace(path=str(root), quiet=True, view="worktree")) == 0


def test_index_validation_accepts_valid_staged_despite_invalid_worktree(
    tmp_path: Path,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/target.md", _validation_thing("base"))
    _commit_all(root, "base")

    _write(root, "things/target.md", _validation_thing("valid candidate"))
    _run(root, "add", "things/target.md")
    _write(root, "things/target.md", "---\nid: [unterminated\n---\n# Broken draft\n")

    assert cmd_validate(Namespace(path=str(root), quiet=True, view="index")) == 0
    assert cmd_validate(Namespace(path=str(root), quiet=True, view="worktree")) == 1


def test_candidates_read_staged_metadata_not_conflicting_worktree(
    tmp_path: Path, capsys,
) -> None:
    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "things/target.md", _validation_thing("base"))
    _commit_all(root, "base")

    staged = _validation_thing("candidate").replace(
        "created: 2026-08-20\n", "created: 2026-08-20\nexposed: true\n"
    )
    _write(root, "things/target.md", staged)
    _run(root, "add", "things/target.md")
    _write(root, "things/target.md", _validation_thing("unexposed draft"))

    assert cmd_candidates(Namespace(path=str(root), view="index")) == 0
    index_output = capsys.readouterr().out
    assert "porch: `validation-target` is exposed" in index_output
    assert cmd_candidates(Namespace(path=str(root), view="worktree")) == 0
    assert capsys.readouterr().out == ""


def test_index_scan_git_spawn_count_is_bounded(tmp_path: Path, monkeypatch) -> None:
    # Structural anti-regression (consolidated-remedy Phase 0 residue): an
    # index-view corpus scan must cost a bounded constant number of git
    # spawns, never one-or-more per thing. The per-file shape (`ls-tree` +
    # `cat-file blob` per read) ran the framework root's pre-commit validate
    # for 302s and timed out the commits it was protecting (2026-08-21).
    import markdownllm.repository_view as rv

    root = tmp_path / "domain"
    _init_repo(root)
    _write(root, "_schema.yaml", "types:\n  note:\n    statuses: [open, done]\n")
    for i in range(30):
        _write(root, f"things/thing-{i:02}.md",
               "---\n"
               f"id: thing-{i:02}\n"
               "type: note\n"
               "status: open\n"
               "created: 2026-08-20\n"
               "---\n\n"
               f"# Thing {i}\n")
    _commit_all(root, "seed")

    calls: list[tuple[str, ...]] = []
    real_git = rv._git

    def counting_git(repo, *args, **kwargs):
        calls.append(args)
        return real_git(repo, *args, **kwargs)

    monkeypatch.setattr(rv, "_git", counting_git)
    view = RepositoryView.index(root)
    calls.clear()  # view construction (rev-parse/write-tree) is out of scope
    corpus, findings = scan(root, view)
    assert len(corpus.things) == 30
    assert not [f for f in findings if f.severity == "ERROR"]
    # One tree listing, one batch content fetch, plus a small fixed overhead
    # (schema read outside the batch). Thirty things must NOT mean thirty+
    # spawns — the bound is deliberately far below the corpus size and
    # deliberately above the exact count so incidental fixed calls do not
    # make the test brittle.
    assert len(calls) <= 6, [" ".join(c) for c in calls]
