"""The cue carrier (unattended-cue-carrier-2026-09-12; change-reconciliation.md
→ The Cue Persists).

`candidates` asks the cue question at the commit boundary; `cues` reads the
same question back off the commit stream and holds it until a human answers
it with a `type: cue` thing. These tests pin the two halves (unanswered open
cues; unraised modifications), the coverage rule (a cue covers its subject at
and before its `raised_at` commit), the receipt's shape (answered ⇒ verdict +
reason), and the session-start line.

Run: python -m pytest tools/tests/test_cues.py -q
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import _sync_git, all_findings, messages, thing_text, write  # noqa: E402


def _head(root: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          capture_output=True, text=True).stdout.strip()


def _seed(tmp_path: Path) -> Path:
    """A spine with three inbound edges (reasoned-from by fan-in) and one leaf,
    committed once."""
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/spine.md",
          "---\nid: spine\ntype: note\nstatus: active\ncreated: 2026-08-01\n---\n# S\n")
    for i in range(3):
        write(root, f"things/leaf{i}.md",
              "---\nid: leaf%d\ntype: note\nstatus: active\ncreated: 2026-08-01\n"
              "linked_things:\n  - id: spine\n    relation: references\n---\n# L\n" % i)
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "seed")
    return root


def _modify(root: Path, rel: str, msg: str) -> str:
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8") + f"\n{msg}\n", encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", msg)
    return _head(root)


def _cue(subject: str, sha: str, status: str = "open", verdict: str | None = None,
         reason: str | None = None, created: str = "2026-09-12") -> str:
    fm = (f"id: cue-{subject}\ntype: cue\nstatus: {status}\ncreated: {created}\n"
          f"subject: {subject}\nraised_at: {sha}\nraised_by: test")
    if verdict is not None:
        fm += f"\nverdict: {verdict}"
    if reason is not None:
        fm += f"\nverdict_reason: {reason}"
    return thing_text(fm, "# Cue\n\nbody\n")


def _run_cues(root: Path, capsys, since: str | None = None):
    from markdownllm.touchpoints import cmd_cues
    rc = cmd_cues(argparse.Namespace(path=str(root), since=since))
    return rc, capsys.readouterr().out


# ------------------------------------------------------------ the two halves

def test_unraised_modification_of_reasoned_from_thing_is_listed(tmp_path, capsys):
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    rc, out = _run_cues(root, capsys)
    assert rc == 0
    assert "Unraised (1)" in out and "`spine`" in out and "3 inbound" in out
    assert sha[:7] in out
    assert "Unanswered" not in out


def test_leaf_modification_raises_nothing(tmp_path, capsys):
    root = _seed(tmp_path)
    _modify(root, "things/leaf0.md", "tweak leaf")
    rc, out = _run_cues(root, capsys)
    assert rc == 0 and "- none" in out


def test_raised_cue_covers_the_change_and_is_listed_as_unanswered(tmp_path, capsys):
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    write(root, "things/cue-spine.md", _cue("spine", sha))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "raise cue")
    rc, out = _run_cues(root, capsys)
    assert rc == 0
    assert "Unanswered (1)" in out and "`cue-spine` on `spine`" in out and "by test" in out
    assert "Unraised" not in out  # the cue covers the modification it was raised for


def test_answered_cue_is_quiet_until_the_subject_moves_again(tmp_path, capsys):
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    write(root, "things/cue-spine.md",
          _cue("spine", sha, status="answered", verdict="not-inflection",
               reason="wording only; dependants hold"))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "answer cue")
    rc, out = _run_cues(root, capsys)
    assert rc == 0 and "- none" in out

    # A later modification is a new question: the old answer does not cover it.
    _modify(root, "things/spine.md", "revise spine again")
    rc, out = _run_cues(root, capsys)
    assert "Unraised (1)" in out and "`spine`" in out and "1 commit(s)" in out


def test_since_override_narrows_the_walk(tmp_path, capsys):
    import datetime as dt
    root = _seed(tmp_path)
    _modify(root, "things/spine.md", "revise spine")
    # Tomorrow, not a far-future year: git's approxidate overflows on the
    # latter and silently returns the whole history.
    tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    rc, out = _run_cues(root, capsys, since=tomorrow)
    assert rc == 0 and "- none" in out and "(--since)" in out


def test_since_must_be_a_date(tmp_path, capsys):
    root = _seed(tmp_path)
    rc, out = _run_cues(root, capsys, since="yesterday")
    assert rc == 2 and "YYYY-MM-DD" in out


# --------------------------------------------------------- the receipt's shape

def test_answered_cue_needs_verdict_and_reason(tmp_path):
    write(tmp_path, "things/spine.md", thing_text(
        "id: spine\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(tmp_path, "things/cue-spine.md",
          _cue("spine", "0" * 40, status="answered"))
    errs = messages(all_findings(tmp_path), "Error")
    assert any("answered cue needs `verdict: inflection | not-inflection`" in e for e in errs)
    assert any("no `verdict_reason`" in e for e in errs)


def test_answered_cue_with_verdict_and_reason_is_clean(tmp_path):
    write(tmp_path, "things/spine.md", thing_text(
        "id: spine\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(tmp_path, "things/cue-spine.md",
          _cue("spine", "0" * 40, status="answered", verdict="inflection",
               reason="walked and sealed"))
    assert not [m for m in messages(all_findings(tmp_path), "Error") if "cue" in m]


def test_open_cue_with_a_verdict_warns(tmp_path):
    write(tmp_path, "things/spine.md", thing_text(
        "id: spine\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(tmp_path, "things/cue-spine.md",
          _cue("spine", "0" * 40, status="open", verdict="inflection"))
    warns = messages(all_findings(tmp_path), "Warning")
    assert any("open cue already carries `verdict: inflection`" in w for w in warns)


def test_cue_subject_must_resolve_and_must_exist(tmp_path):
    write(tmp_path, "things/cue-ghost.md", _cue("ghost", "0" * 40))
    errs = messages(all_findings(tmp_path), "Error")
    assert any("`subject` references unknown id `ghost`" in e for e in errs)
    write(tmp_path, "things/cue-none.md", thing_text(
        "id: cue-none\ntype: cue\nstatus: open\ncreated: 2026-09-12"))
    errs = messages(all_findings(tmp_path), "Error")
    assert any("cue has no `subject`" in e for e in errs)


def test_cue_status_vocabulary_is_reserved(tmp_path):
    write(tmp_path, "things/spine.md", thing_text(
        "id: spine\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(tmp_path, "things/cue-spine.md", _cue("spine", "0" * 40, status="pending"))
    errs = messages(all_findings(tmp_path), "Error")
    assert any("status `pending` not in" in e and "`cue`" in e for e in errs)


def test_cue_does_not_count_toward_its_subjects_fan_in(tmp_path):
    # A cue's `subject` edge is reverse-indexed but not cue-relevant: raising
    # one must not make the next modification more likely to raise another.
    from markdownllm.touchpoints import _inbound_counts
    from markdownllm.model import scan
    write(tmp_path, "things/spine.md", thing_text(
        "id: spine\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(tmp_path, "things/cue-spine.md", _cue("spine", "0" * 40))
    corpus, _ = scan(tmp_path)
    assert _inbound_counts(corpus).get("spine", 0) == 0


# ------------------------------------------------------------ the loud half

def test_session_start_names_open_and_unraised_cues(tmp_path, capsys):
    from markdownllm.session import cmd_session_start
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    write(root, "things/leaf0.md",  # a second reasoned-from thing, by type
          "---\nid: leaf0\ntype: skill\nstatus: draft\ncreated: 2026-08-01\n"
          "linked_things:\n  - id: spine\n    relation: references\n---\n# L\n")
    write(root, "things/cue-spine.md", _cue("spine", sha))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "raise cue; leaf0 becomes a skill")
    _modify(root, "things/leaf0.md", "revise the skill")
    cmd_session_start(argparse.Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert "Reconciliation cues (2)" in out
    assert "1 raised and unanswered, 1 modified-and-unraised" in out
    assert "`cue-spine` — open on `spine`" in out
    assert "`leaf0` — modified 2× since" in out and "definition surface" in out
    # An open cue is a question, not a loop: it must not also appear there.
    assert "`cue-spine` (cue, open)" not in out


def test_session_start_is_quiet_when_every_cue_is_answered(tmp_path, capsys):
    from markdownllm.session import cmd_session_start
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    write(root, "things/cue-spine.md",
          _cue("spine", sha, status="answered", verdict="not-inflection",
               reason="wording only"))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "answer cue")
    cmd_session_start(argparse.Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert "Reconciliation cues" not in out
