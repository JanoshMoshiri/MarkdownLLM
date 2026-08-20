"""Coherence reads the same frozen candidate as validation at commit time."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.coherence import coherence_findings  # noqa: E402
from markdownllm.indexes import _anchor_notes, build_index_body  # noqa: E402
from markdownllm.model import SEV_ERROR, scan  # noqa: E402
from markdownllm.repository_view import RepositoryView  # noqa: E402


def _git(root: Path, *args: str) -> None:
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": "coherence-tests",
        "GIT_AUTHOR_EMAIL": "coherence@example.invalid",
        "GIT_COMMITTER_NAME": "coherence-tests",
        "GIT_COMMITTER_EMAIL": "coherence@example.invalid",
    })
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, env=env)


BASE_A = """---
id: a
type: note
status: in-progress
created: 2026-08-20
---

# A
"""

LINKED_A = """---
id: a
type: note
status: in-progress
created: 2026-08-20
linked_things:
  - id: b
    relation: related
---

# A
"""

B = """---
id: b
type: note
status: in-progress
created: 2026-08-20
linked_things:
  - id: a
    relation: related
---

# B
"""


def _write_index(root: Path) -> None:
    corpus, _ = scan(root)
    body, coverage = build_index_body(corpus, "relationships")
    path = root / "things" / "_index" / "relationships.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\nid: test-relationships-index\ntype: index\nstatus: live\n"
        "index_of: relationships\ncreated: 2026-08-20\n"
        "generated: 2026-08-20T00:00:00\ngenerated_from: HEAD@unknown\n"
        f"coverage: {coverage}\nframework_version: unknown\n---\n\n"
        f"# Relationships Index\n\n{body}\n",
        encoding="utf-8",
    )


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "domain"
    (root / "things").mkdir(parents=True)
    _git(root, "init", "-q")
    (root / "things" / "a.md").write_text(BASE_A, encoding="utf-8")
    (root / "things" / "b.md").write_text(B, encoding="utf-8")
    _write_index(root)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    return root


def _errors(root: Path, view: RepositoryView) -> list:
    return [f for f in coherence_findings(root, 15, view)
            if f.severity == SEV_ERROR]


def test_invalid_staged_index_candidate_cannot_be_hidden_by_repaired_worktree(tmp_path):
    root = _repo(tmp_path)
    a = root / "things" / "a.md"
    a.write_text(LINKED_A, encoding="utf-8")
    _git(root, "add", "things/a.md")
    a.write_text(BASE_A, encoding="utf-8")

    assert not _errors(root, RepositoryView.worktree(root))
    assert any("relationships-index" == f.thing
               for f in _errors(root, RepositoryView.index(root)))


def test_valid_staged_candidate_is_not_blocked_by_invalid_worktree(tmp_path):
    root = _repo(tmp_path)
    a = root / "things" / "a.md"
    a.write_text(LINKED_A, encoding="utf-8")
    _write_index(root)
    _git(root, "add", "things/a.md", "things/_index/relationships.md")
    a.write_text(BASE_A, encoding="utf-8")

    assert any("relationships-index" == f.thing
               for f in _errors(root, RepositoryView.worktree(root)))
    assert not _errors(root, RepositoryView.index(root))


def test_index_anchor_version_uses_candidate_sentinel_not_worktree(tmp_path):
    root = tmp_path / "framework"
    root.mkdir()
    _git(root, "init", "-q")
    sentinel = root / ".markdownllm"
    sentinel.write_text(
        "framework: MarkdownLLM\nversion: 3.32.0\nfoundational_specs: []\n",
        encoding="utf-8",
    )
    _git(root, "add", ".markdownllm")
    _git(root, "commit", "-q", "-m", "base")

    # Candidate remains 3.32 while the worktree advances. A candidate check
    # must not import that adjacent worktree version and invent drift.
    candidate = RepositoryView.index(root)
    sentinel.write_text(
        "framework: MarkdownLLM\nversion: 3.33.0\nfoundational_specs: []\n",
        encoding="utf-8",
    )
    assert not any("stamped at framework" in note for note in
                   _anchor_notes(root, {"framework_version": "3.32.0"},
                                 "relationships", candidate))
