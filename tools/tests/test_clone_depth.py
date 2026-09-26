"""A clone that cannot see its whole history must say so — and be healed.

The lived instance (Claude Code cloud, 2026-09-24): a depth-50 harness clone
of a 938-commit repository made `validate` report 148 Errors (pins below the
shallow boundary "resolve to no commit"), 3 false born-verified Warnings, a
wrong velocity trend and no stall section at all — and nothing named the
cause. These tests pin the four answers: detect (clone_depth), stop minting
false findings (pins, born-verified, definition_commit), say it loudly
(validate/doctor/session-start), and heal it (estate-sync). They also pin the
sibling harness defect: a checked-out branch with no upstream configured
while the remote carries a branch of the same name.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.clone_depth import clone_depth  # noqa: E402
from markdownllm.model import SEV_ERROR, SEV_WARNING, scan  # noqa: E402
from markdownllm.structural_pins import structural_pin_findings  # noqa: E402
from markdownllm.sync import SyncState, sync_repo  # noqa: E402
from markdownllm.validation import validate_corpus  # noqa: E402

pytestmark = pytest.mark.gitfs


def _git(root: Path, *args: str) -> str:
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "clone-depth-tests",
        "GIT_COMMITTER_NAME": "clone-depth-tests",
        "GIT_AUTHOR_EMAIL": "clone-depth-tests@local",
        "GIT_COMMITTER_EMAIL": "clone-depth-tests@local",
    })
    return subprocess.run(["git", *args], cwd=root, check=True,
                          capture_output=True, text=True, env=env).stdout.strip()


def _thing(thing_id: str, thing_type: str = "task", status: str = "in-progress",
           extra: str = "") -> str:
    return ("---\n" f"id: {thing_id}\n" f"type: {thing_type}\n"
            f"status: {status}\n" "created: 2026-08-28\n" f"{extra}" "---\n\n"
            f"# {thing_id}\n\nClone-depth fixture.\n")


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")


def _source_with_old_pin(tmp_path: Path) -> tuple[Path, str]:
    """A source repo whose newest thing pins its OLDEST commit, plus padding
    commits so a depth-1 clone cannot see the pinned one."""
    src = tmp_path / "src"
    src.mkdir()
    _git(src, "init", "-q", "-b", "main")
    _write(src, "things/input.md", _thing("input"))
    _git(src, "add", "-A")
    _git(src, "commit", "-q", "-m", "record the input")
    old = _git(src, "rev-parse", "HEAD")
    for n in range(3):
        _write(src, f"things/pad-{n}.md", _thing(f"pad-{n}"))
        _git(src, "add", "-A")
        _git(src, "commit", "-q", "-m", f"pad {n}")
    _write(src, "things/d.md", _thing(
        "d", "decision", "made",
        f"informed_by:\n  - id: input\n    commit: {old}\n"))
    _git(src, "add", "-A")
    _git(src, "commit", "-q", "-m", "decide on the old input")
    return src, old


def _shallow_clone(src: Path, dest: Path, depth: int = 1) -> Path:
    subprocess.run(["git", "clone", "-q", "--depth", str(depth),
                    src.resolve().as_uri(), str(dest)],
                   check=True, capture_output=True)
    return dest


def test_full_clone_reports_full_history(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    depth = clone_depth(src)
    assert depth.shallow is False and not depth.truncated


def test_shallow_clone_is_detected_with_its_horizon(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = _shallow_clone(src, tmp_path / "clone")
    depth = clone_depth(clone)
    assert depth.truncated
    assert depth.boundaries and depth.oldest_visible is not None
    assert "history before" in depth.horizon()


def test_outside_any_repository_is_could_not_ask_not_full_history(tmp_path):
    lonely = tmp_path / "not-a-repo"
    lonely.mkdir()
    assert clone_depth(lonely).shallow is None


def test_a_valid_pin_below_the_boundary_is_not_an_error(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = _shallow_clone(src, tmp_path / "clone")
    corpus, _ = scan(clone)
    findings = structural_pin_findings(clone, corpus)
    assert not [f for f in findings if f.severity == SEV_ERROR]
    assert any("SHALLOW" in f.message and f.severity == SEV_WARNING
               for f in findings)


def test_the_same_pin_is_an_error_again_once_history_is_whole(tmp_path):
    # The downgrade must not become a hiding place: in a full clone an
    # unresolvable pin is still a transcription error, blocked at commit.
    src, _ = _source_with_old_pin(tmp_path)
    _write(src, "things/bad.md", _thing(
        "bad", "decision", "made",
        "informed_by:\n  - id: input\n    commit: "
        "bdb95714c3a7e2f08d61b95a2f4ee90c1d2a4f6b\n"))
    corpus, _ = scan(src)
    errors = [f for f in structural_pin_findings(src, corpus)
              if f.severity == SEV_ERROR]
    assert [f.thing for f in errors] == ["bad"]


def test_validate_names_the_shallow_clone_once_as_a_warning(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = _shallow_clone(src, tmp_path / "clone")
    _, findings = validate_corpus(clone)
    depth_findings = [f for f in findings if f.thing == "clone-depth"]
    assert len(depth_findings) == 1
    assert depth_findings[0].severity == SEV_WARNING
    assert not [f for f in findings if f.severity == SEV_ERROR]


def test_estate_sync_completes_shallow_history(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = _shallow_clone(src, tmp_path / "clone")
    res = sync_repo(clone)
    assert res.state is SyncState.UP_TO_DATE
    assert "history completed" in res.detail
    assert not clone_depth(clone).truncated


def test_estate_sync_says_shallow_loudly_when_it_cannot_heal(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = _shallow_clone(src, tmp_path / "clone")
    res = sync_repo(clone, fetch=False)  # the no-network form
    assert res.state is SyncState.SHALLOW
    assert "git fetch --unshallow" in res.detail


def test_harness_branch_without_upstream_compares_with_its_namesake(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    _git(src, "branch", "claude/session")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", src.resolve().as_uri(), str(clone)],
                   check=True, capture_output=True)
    _git(clone, "checkout", "-q", "--no-track", "-b", "claude/session",
         "origin/claude/session")
    # the remote moves on; the harness-created branch has no upstream
    _git(src, "checkout", "-q", "claude/session")
    _write(src, "things/later.md", _thing("later"))
    _git(src, "add", "-A")
    _git(src, "commit", "-q", "-m", "later")
    res = sync_repo(clone)
    assert res.state is SyncState.SYNCED and res.moved
    assert "origin/claude/session" in res.detail
    assert (clone / "things" / "later.md").is_file()
    unset = subprocess.run(
        ["git", "config", "--get", "branch.claude/session.merge"],
        cwd=clone, capture_output=True, text=True)
    assert unset.returncode != 0, "sync must not write upstream config"


def test_two_remotes_carrying_the_name_stay_no_upstream(tmp_path):
    src, _ = _source_with_old_pin(tmp_path)
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", src.resolve().as_uri(), str(clone)],
                   check=True, capture_output=True)
    _git(clone, "remote", "add", "mirror", src.resolve().as_uri())
    _git(clone, "fetch", "-q", "mirror")
    _git(clone, "checkout", "-q", "--no-track", "-b", "topic", "origin/main")
    _git(src, "branch", "topic")
    _git(clone, "fetch", "-q", "--all")
    assert sync_repo(clone).state is SyncState.NO_UPSTREAM
