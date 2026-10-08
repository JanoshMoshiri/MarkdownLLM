"""The cue carrier (unattended-cue-carrier-2026-09-12; change-reconciliation.md
→ The Cue Persists).

`candidates` asks the cue question at the commit boundary; `cues` reads the
same question back off the commit stream and holds it until its walk is recorded
on a `type: cue` thing. These tests pin the two halves (unanswered open
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


def test_cue_raised_in_the_same_commit_as_the_change_covers_it(tmp_path, capsys):
    # The dispatch rule: raise the cue IN the modifying commit. That commit's
    # sha does not exist yet, so the cue pins the parent — and the commit that
    # adds the cue file is covered by construction.
    root = _seed(tmp_path)
    parent = _head(root)
    p = root / "things" / "spine.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nrevised\n", encoding="utf-8")
    write(root, "things/cue-spine.md", _cue("spine", parent))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "revise spine and raise its cue together")
    rc, out = _run_cues(root, capsys)
    assert rc == 0
    assert "Unanswered (1)" in out and "Unraised" not in out


def test_since_override_narrows_the_walk(tmp_path, capsys):
    import datetime as dt
    root = _seed(tmp_path)
    _modify(root, "things/spine.md", "revise spine")
    # Tomorrow, not a far-future year: git's approxidate overflows on the
    # latter and silently returns the whole history.
    tomorrow = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    rc, out = _run_cues(root, capsys, since=tomorrow)
    assert rc == 0 and "- none" in out and "(--since)" in out


def test_a_baseline_of_today_still_sees_todays_modifications(tmp_path, capsys):
    # git reads a bare `--since=YYYY-MM-DD` as that date at the current time of
    # day; the walk must pass explicit midnight or the retrospective's own day
    # goes dark the moment the baseline moves to it.
    import datetime as dt
    root = _seed(tmp_path)
    _modify(root, "things/spine.md", "revise spine today")
    rc, out = _run_cues(root, capsys, since=dt.date.today().isoformat())
    assert rc == 0 and "Unraised (1)" in out and "`spine`" in out


def test_since_must_be_a_date(tmp_path, capsys):
    root = _seed(tmp_path)
    rc, out = _run_cues(root, capsys, since="yesterday")
    assert rc == 2 and "YYYY-MM-DD" in out


def test_candidates_asks_nothing_of_a_new_cue_thing(tmp_path, capsys):
    # A cue is the answer to a cue question; the boundary advisory must not
    # ask "is this new thing a duplicate?" of it, or every raise recurses.
    from markdownllm.touchpoints import cmd_candidates
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    write(root, "things/cue-spine.md", _cue("spine", sha))
    _sync_git(root, "add", "-A")
    rc = cmd_candidates(argparse.Namespace(path=str(root)))
    out = capsys.readouterr().out
    assert rc == 0 and "cue-spine" not in out


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


# ------------------------------------------------------------ the mechanical raise

def _run_raise(root: Path, capsys):
    from markdownllm.touchpoints import cmd_cues
    rc = cmd_cues(argparse.Namespace(path=str(root), since=None, raise_=True))
    return rc, capsys.readouterr().out


def test_raise_writes_an_open_cue_that_covers_the_change(tmp_path, capsys):
    """`mdllm cues --raise`: the raise is mechanical, the verdict is not. The
    written cue pins the modifying commit, carries no verdict, and the next
    read lists it as unanswered rather than the change as unraised."""
    import datetime as dt
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    rc, out = _run_raise(root, capsys)
    assert rc == 0 and "Raised (1)" in out
    path = root / "things" / "cues" / f"cue-spine-{dt.date.today().isoformat()}.md"
    assert path.exists() and path.as_posix().endswith(out.split("- things/")[-1].split("\n")[0])
    text = path.read_text(encoding="utf-8")
    assert "status: open" in text and "subject: spine" in text
    assert f"raised_at: {sha}" in text
    assert "raised_by: \"floor — mdllm cues --raise\"" in text
    assert "verdict:\n" in text and "verdict: inflection" not in text
    assert "3 inbound edge(s)" in text and sha[:7] in text

    rc, out = _run_cues(root, capsys)
    assert "Unanswered (1)" in out and "cue-spine-" in out
    assert "Unraised" not in out


def test_raise_leaves_a_cue_the_validator_accepts(tmp_path, capsys):
    root = _seed(tmp_path)
    _modify(root, "things/spine.md", "revise spine")
    _run_raise(root, capsys)
    errs = [m for m in messages(all_findings(root), "Error") if "cue" in m]
    assert errs == [], errs


def test_raise_never_overwrites_a_cue_already_on_disk_today(tmp_path, capsys):
    import datetime as dt
    root = _seed(tmp_path)
    sha = _modify(root, "things/spine.md", "revise spine")
    cues = root / "things" / "cues"
    cues.mkdir()
    hand = cues / f"cue-spine-{dt.date.today().isoformat()}.md"
    hand.write_text(_cue("spine", sha, created=dt.date.today().isoformat()),
                    encoding="utf-8")
    before = hand.read_text(encoding="utf-8")
    rc, out = _run_raise(root, capsys)
    assert rc == 0
    assert hand.read_text(encoding="utf-8") == before
    # The hand-raised cue already covers the change, so there is nothing
    # unraised to write: the raise respects a cover, whoever made it.
    assert "nothing to raise" in out


def test_raise_with_nothing_unraised_says_so(tmp_path, capsys):
    root = _seed(tmp_path)
    _modify(root, "things/leaf0.md", "tweak leaf")
    rc, out = _run_raise(root, capsys)
    assert rc == 0 and "nothing to raise" in out
    assert not (root / "things" / "cues").exists()


# ------------------------------------------------------------------ the gate
# `cues --staged` — the ask, where the change lands
# (the-verdict-is-asked-where-the-change-lands-2026-10-05): the question for
# the commit in hand, exit 1 while a definition surface changes with no cue on
# disk; `--staged --raise` writes the cue pinned to HEAD; one ask per subject
# per day; an unattended run is told to raise and file, never answer.

def _seed_surface(tmp_path: Path) -> Path:
    """A definition surface (`insight`) with two dependants, committed once."""
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/surface.md",
          "---\nid: surface\ntype: insight\nstatus: active\ncreated: 2026-08-01\n---\n# I\n")
    for i in range(2):
        write(root, f"things/leaf{i}.md",
              "---\nid: leaf%d\ntype: note\nstatus: active\ncreated: 2026-08-01\n"
              "linked_things:\n  - id: surface\n    relation: references\n---\n# L\n" % i)
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "seed")
    return root


def _touch(root: Path, rel: str, msg: str) -> None:
    """Modify without committing — the state a PreToolUse gate sees."""
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8") + f"\n{msg}\n", encoding="utf-8")


def _run_staged(root: Path, capsys, raise_: bool = False):
    from markdownllm.touchpoints import cmd_cues
    rc = cmd_cues(argparse.Namespace(path=str(root), since=None, raise_=raise_,
                                     staged=True))
    return rc, capsys.readouterr().out


def test_staged_owes_the_question_for_a_changed_definition_surface(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    _touch(root, "things/surface.md", "this is how it needs to be")
    rc, out = _run_staged(root, capsys)
    assert rc == 1
    assert "`surface`" in out and "definition surface (`insight`)" in out
    assert "2 dependant(s): `leaf0`, `leaf1`" in out
    assert "Walk it now" in out and "restatement level" in out
    assert "native choice prompt" in out and "defer to the seat" in out
    assert "cues . --staged --raise" in out


def test_staged_is_not_asked_for_a_fan_in_data_thing(tmp_path, capsys):
    # The gate's scope is the definition surfaces; a data thing reasoned from
    # by fan-in stays with `cues` and the retrospective's net.
    root = _seed(tmp_path)  # spine: type note, three inbound edges
    _touch(root, "things/spine.md", "revise spine")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out


def test_staged_is_quiet_when_nothing_reasoned_from_changed(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    _touch(root, "things/leaf0.md", "tweak a leaf")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out


def test_staged_raise_writes_the_cue_pinned_to_head_and_opens_the_gate(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    head = _head(root)
    _touch(root, "things/surface.md", "this is how it needs to be")
    rc, out = _run_staged(root, capsys, raise_=True)
    assert rc == 0 and "Raised (1)" in out
    today = __import__("datetime").date.today().isoformat()
    cue = root / "things" / "cues" / f"cue-surface-{today}.md"
    assert cue.exists()
    text = cue.read_text(encoding="utf-8")
    assert f"raised_at: {head}" in text and "status: open" in text
    assert "verdict:\n" in text  # the verdict is left empty — never the floor's
    # The cue on disk (untracked, in the delta) opens the gate.
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out
    # Committed together, the carrier reads it as raised and covered.
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "revise surface, cue rides along")
    rc, out = _run_cues(root, capsys)
    assert "Unanswered (1)" in out and "Unraised" not in out


def test_staged_raise_leaves_a_cue_the_validator_accepts(tmp_path):
    root = _seed_surface(tmp_path)
    _touch(root, "things/surface.md", "revise")
    from markdownllm.touchpoints import cmd_cues
    assert cmd_cues(argparse.Namespace(path=str(root), since=None, raise_=True,
                                       staged=True)) == 0
    assert messages(all_findings(root), "Error") == []


def test_a_cue_created_today_covers_the_days_later_edits(tmp_path, capsys):
    # One ask per subject per day: the fifth refinement in one sitting is not
    # a fifth dialog, and the carrier agrees after the commit.
    root = _seed_surface(tmp_path)
    today = __import__("datetime").date.today().isoformat()
    sha = _head(root)
    _touch(root, "things/surface.md", "first edit")
    write(root, "things/cue-surface.md",
          _cue("surface", sha, status="answered", verdict="not-inflection",
               reason="wording only", created=today))
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "first edit, answered at the boundary")
    _touch(root, "things/surface.md", "second edit, same sitting")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "second edit")
    rc, out = _run_cues(root, capsys)
    assert "- none" in out


def test_staged_unattended_is_told_to_raise_and_file_never_answer(tmp_path, capsys, monkeypatch):
    root = _seed_surface(tmp_path)
    _touch(root, "things/surface.md", "revise")
    monkeypatch.setenv("MDLLM_UNATTENDED", "1")
    rc, out = _run_staged(root, capsys)
    assert rc == 1
    assert "Unattended run" in out and "apply nothing" in out
    assert "native choice prompt" not in out and "Walk it now" not in out
    assert "cues . --staged --raise" in out


def test_staged_raise_prefills_the_walk_with_declared_and_literal_dependants(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    # A thing that reasons about the surface without linking to it: the
    # literal tier. And a cue naming it, which is not a dependant.
    write(root, "things/mention.md",
          "---\nid: mention\ntype: note\nstatus: active\ncreated: 2026-08-01\n---\n"
          "# M\n\nThis note reasons from surface without a link.\n")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "a literal reference")
    _touch(root, "things/surface.md", "this is how it needs to be")
    rc, out = _run_staged(root, capsys, raise_=True)
    assert rc == 0 and "walk list" in out
    today = __import__("datetime").date.today().isoformat()
    text = (root / "things" / "cues" / f"cue-surface-{today}.md").read_text(encoding="utf-8")
    assert "## The Walk" in text
    assert "- [ ] `leaf0` — linked_things `references`" in text
    assert "- [ ] `leaf1` — linked_things `references`" in text
    assert "- [ ] `mention` — names it in the body" in text
    assert "cue-surface" not in text.split("## The Walk")[1].split("Mark each")[0]
    assert "verdict:\n" in text  # the judgement is the agent's, never the floor's


def test_a_change_confined_to_a_generated_block_is_not_a_walk_candidate(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    p = root / "things" / "surface.md"
    p.write_text(p.read_text(encoding="utf-8")
                 + "\n<!-- generated:toolbox -->\nold rows\n<!-- /generated:toolbox -->\n",
                 encoding="utf-8")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "a managed block")
    p.write_text(p.read_text(encoding="utf-8").replace("old rows", "new rows"),
                 encoding="utf-8")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out  # the generator did the walk
    _touch(root, "things/surface.md", "an authored sentence")
    rc, out = _run_staged(root, capsys)
    assert rc == 1 and "`surface`" in out


def test_staged_opens_when_git_has_no_head(tmp_path, capsys):
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/surface.md",
          "---\nid: surface\ntype: insight\nstatus: active\ncreated: 2026-08-01\n---\n# I\n")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "could not look" in out


# ------------------------------------------ disposition is not a walk (Phase 3)
# A change that only records a disposition — a status the reckoning moved, a
# hold, a look-again date, a trigger re-dated — moves no claim, so neither the
# gate nor the cue listing owes a walk for it; withdrawing a claim still does.

def _dispose(root: Path, rel: str, old: str, new: str) -> None:
    p = root / rel
    p.write_text(p.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8")


def test_a_disposition_only_change_owes_no_walk_at_the_gate(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    _dispose(root, "things/surface.md", "status: active",
             "status: promoted\npromoted_to: leaf0\nversion: 1.1")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out
    _dispose(root, "things/surface.md", "status: promoted",
             "status: active\ndisposition: keep-active\ndisposition_reason: a razor\n"
             "settles_when: 2026-12-01")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "- none" in out


def test_withdrawing_a_claim_is_still_walked(tmp_path, capsys):
    root = _seed_surface(tmp_path)
    _dispose(root, "things/surface.md", "status: active", "status: dismissed")
    rc, out = _run_staged(root, capsys)
    assert rc == 1 and "`surface`" in out


def test_the_listing_skips_a_disposition_only_modification(tmp_path, capsys):
    root = _seed(tmp_path)  # spine: reasoned-from by fan-in
    _dispose(root, "things/spine.md", "status: active",
             "status: active\nsettles_when: 2026-12-01\ntriggers:\n"
             "  - type: time\n    condition: \"2026-11-01 reached\"\n    action: surface")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "re-dated")
    rc, out = _run_cues(root, capsys, since="2026-01-01")
    assert rc == 0 and "spine" not in out
    _modify(root, "things/spine.md", "a claim moved")
    rc, out = _run_cues(root, capsys, since="2026-01-01")
    assert "`spine`" in out and "modified in 1 commit(s)" in out


def _seed_close(tmp_path: Path) -> Path:
    """A surface and a plan with every box ticked: the mechanical band pends."""
    root = _seed_surface(tmp_path)
    write(root, "things/done.md",
          "---\nid: done\ntype: plan\nstatus: in-progress\ncreated: 2026-08-01\n---\n"
          "# D\n\n- [x] a\n")
    _sync_git(root, "add", "-A")
    _sync_git(root, "commit", "-q", "-m", "a finished plan")
    return root


def test_a_session_end_commit_owes_the_close(tmp_path, capsys, monkeypatch):
    from markdownllm.reckon import SESSION_END_ENV
    root = _seed_close(tmp_path)
    monkeypatch.delenv(SESSION_END_ENV, raising=False)
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "The close" not in out  # an ordinary commit is not asked
    monkeypatch.setenv(SESSION_END_ENV, "1")
    rc, out = _run_staged(root, capsys)
    assert rc == 1
    assert "## The close — what this session end owes the reckoning" in out
    assert "1 mechanical item(s) pending" in out and "`done`" in out
    assert "reckon . --close --apply" in out


def test_a_session_end_commit_opens_once_the_close_is_met(tmp_path, capsys, monkeypatch):
    from markdownllm.reckon import SESSION_END_ENV
    root = _seed_close(tmp_path)
    _dispose(root, "things/done.md", "status: in-progress", "status: completed")
    monkeypatch.setenv(SESSION_END_ENV, "1")
    rc, out = _run_staged(root, capsys)
    assert rc == 0 and "## The close — met" in out


def test_an_unattended_session_end_is_held_to_the_mechanical_band(tmp_path, capsys, monkeypatch):
    from markdownllm.reckon import SESSION_END_ENV
    from markdownllm.touchpoints import UNATTENDED_ENV
    root = _seed_close(tmp_path)
    monkeypatch.setenv(SESSION_END_ENV, "1")
    monkeypatch.setenv(UNATTENDED_ENV, "1")
    rc, out = _run_staged(root, capsys)
    assert rc == 1 and "mechanical item(s) pending" in out
    _dispose(root, "things/done.md", "status: in-progress", "status: completed")
    rc, out = _run_staged(root, capsys)
    assert rc == 0
