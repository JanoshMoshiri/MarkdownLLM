"""`mdllm precommit` — the concurrent hook coordinator (floor-sprint-1 F11).

The coordinator composes the four existing legs; these tests pin that the
composition changes scheduling only: same findings surface, same wrapper
messages, same exit severity, one frozen candidate.

Run: python -m pytest tools/tests/test_precommit.py -q
"""

from __future__ import annotations

import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.precommit import cmd_precommit  # noqa: E402


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def _repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@t")
    _git(root, "config", "user.name", "t")
    return root


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def _thing(front: str) -> str:
    return f"---\n{front}\n---\n\n# T\n"


def test_precommit_clean_candidate_exits_zero(tmp_path, capsys):
    root = _repo(tmp_path)
    _write(root, "things/a.md", _thing(
        "id: a\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    _git(root, "add", "-A")
    rc = cmd_precommit(Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert rc == 0
    assert "commit blocked" not in out


def test_precommit_blocks_on_staged_validation_error_with_hook_message(
        tmp_path, capsys):
    # The staged candidate is what counts (index view), and the failure
    # message is byte-identical to the sequential hook's wrapper line.
    root = _repo(tmp_path)
    _write(root, "things/bad.md", _thing(
        "id: bad\ntype: task\nstatus: in-progress"))  # missing created
    _git(root, "add", "-A")
    rc = cmd_precommit(Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert rc == 1
    assert ("mdllm: validation Errors — commit blocked. Fix or run with "
            "--no-verify (discouraged).") in out


def test_precommit_repaired_worktree_cannot_excuse_invalid_staged(
        tmp_path, capsys):
    # Freeze semantics preserved: the worktree repair after staging must not
    # rescue the invalid staged bytes.
    root = _repo(tmp_path)
    _write(root, "things/bad.md", _thing(
        "id: bad\ntype: task\nstatus: in-progress"))
    _git(root, "add", "-A")
    _write(root, "things/bad.md", _thing(
        "id: bad\ntype: task\nstatus: in-progress\ncreated: 2026-06-01"))
    rc = cmd_precommit(Namespace(path=str(root)))
    assert rc == 1


def test_precommit_boundary_block_carries_its_own_message(tmp_path, capsys):
    root = _repo(tmp_path)
    _write(root, ".gitignore", ".boundary-terms\n")
    _write(root, ".boundary-terms", "SECRETWORD\n")
    _write(root, "things/leak.md", _thing(
        "id: leak\ntype: task\nstatus: in-progress\ncreated: 2026-06-01")
        + "\nSECRETWORD appears here.\n")
    _git(root, "add", "-A")
    rc = cmd_precommit(Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert rc == 1
    assert ("mdllm: staged content crosses the disclosure boundary — "
            "commit blocked.") in out
