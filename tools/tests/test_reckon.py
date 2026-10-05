"""The reckoning (the-reckoning-is-the-digestion-beat-2026-10-05) — `mdllm
reckon` names every attention item's disposition candidate with evidence, in
three bands, and never marks a verdict. These tests pin each band's predicate
on a small corpus with a real git history.

Run: python -m pytest tools/tests/test_reckon.py -q
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import _sync_git, thing_text, write  # noqa: E402

TODAY = dt.date(2026, 10, 5)


def _commit(root: Path, msg: str, day: str = "2026-10-05") -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": f"{day}T12:00:00",
           "GIT_COMMITTER_DATE": f"{day}T12:00:00"}
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=root, check=True, env=env)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/plan-a.md",
          thing_text("id: plan-a\ntype: plan\nstatus: in-progress\ncreated: 2026-07-01\n"
                     "priority: high", "# A\n\n- [x] one\n- [ ] two\n"))
    _commit(root, "seed", "2026-07-01")
    return root


def _reckon(root: Path, **kw) -> dict:
    from markdownllm.model import scan
    from markdownllm.reckon import reckon_report
    corpus, _ = scan(root)
    return reckon_report(root, corpus, today=TODAY, **kw)


def _ids(rep: dict, band: str) -> dict[str, str]:
    return {it.thing_id: it.proposal for it in rep["bands"][band]}


# ------------------------------------------------------------------ insights

def test_promoted_to_that_resolves_is_mechanical(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/i1.md",
          thing_text("id: i1\ntype: insight\nstatus: active\ncreated: 2026-09-30\n"
                     "promoted_to: plan-a"))
    _commit(root, "an insight already promoted in fact")
    rep = _reckon(root)
    assert _ids(rep, "mechanical") == {"i1": "promote"}
    assert rep["bands"]["mechanical"][0].fields == {"status": "promoted"}


def test_orphan_insight_past_its_interval_is_settled_and_a_young_one_is_quiet(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/old.md",
          thing_text("id: old\ntype: insight\nstatus: active\ncreated: 2026-07-01"))
    write(root, "things/young.md",
          thing_text("id: young\ntype: insight\nstatus: active\ncreated: 2026-09-30"))
    _commit(root, "two orphans")
    rep = _reckon(root)
    assert _ids(rep, "settled").get("old") == "dismiss or consolidate"
    assert "young" not in _ids(rep, "settled")


def test_settles_when_overrides_the_default_interval(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/soon.md",
          thing_text("id: soon\ntype: insight\nstatus: active\ncreated: 2026-10-01\n"
                     "settles_when: 2026-10-03"))
    write(root, "things/later.md",
          thing_text("id: later\ntype: insight\nstatus: active\ncreated: 2026-06-01\n"
                     "settles_when: 2026-12-01"))
    _commit(root, "declared exits")
    rep = _reckon(root)
    assert "soon" in _ids(rep, "settled")
    assert "later" not in _ids(rep, "settled")


def test_cited_insight_is_quiet_until_twice_the_interval_then_asks_for_promotion(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/cited.md",
          thing_text("id: cited\ntype: insight\nstatus: active\ncreated: 2026-05-01"))
    write(root, "things/citer.md",
          thing_text("id: citer\ntype: plan\nstatus: in-progress\ncreated: 2026-10-01\n"
                     "linked_things:\n  - id: cited\n    relation: references"))
    _commit(root, "a long-lived cited insight")
    rep = _reckon(root)
    assert _ids(rep, "settled").get("cited", "").startswith("promote into the operating layer")


def test_held_insight_past_its_interval_is_residue(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/held.md",
          thing_text("id: held\ntype: insight\nstatus: active\ncreated: 2026-07-01\n"
                     "disposition: keep-active\n"
                     "disposition_reason: until the eval lands"))
    _commit(root, "a held insight")
    rep = _reckon(root)
    # A hold states its own exit; the agent reads it and disposes or re-dates.
    assert _ids(rep, "settled").get("held", "").startswith("read the stated condition")
    held = next(i for i in rep["bands"]["settled"] if i.thing_id == "held")
    assert "until the eval lands" in held.evidence
    assert "held" not in _ids(rep, "residue")


def test_mirrored_items_are_their_source_workspaces_to_reckon(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/mirror.md",
          thing_text("id: mirror\ntype: insight\nstatus: active\ncreated: 2026-06-01\n"
                     "origin: external\nsource_domain: elsewhere\nsource_id: mirror\n"
                     "source_commit: 0000000000000000000000000000000000000000"))
    _commit(root, "a mirrored insight")
    rep = _reckon(root)
    assert all("mirror" not in _ids(rep, b) for b in ("mechanical", "settled", "residue"))


# ----------------------------------------------------------------- conflicts

def test_conflict_with_one_superseded_party_is_mechanical(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/d1.md", thing_text("id: d1\ntype: decision\nstatus: superseded\ncreated: 2026-08-01"))
    write(root, "things/d2.md", thing_text("id: d2\ntype: decision\nstatus: made\ncreated: 2026-08-01"))
    write(root, "things/c1.md",
          thing_text("id: c1\ntype: conflict\nstatus: open\ncreated: 2026-08-01\n"
                     "linked_things:\n  - id: d1\n    relation: contradicts\n"
                     "  - id: d2\n    relation: contradicts"))
    _commit(root, "a conflict whose loser is superseded")
    rep = _reckon(root)
    assert _ids(rep, "mechanical") == {"c1": "resolve: superseded"}
    assert rep["bands"]["mechanical"][0].fields["resolved_by"] == "d2"


def test_aged_conflict_in_circulation_is_residue_and_out_of_it_is_settled(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/p1.md", thing_text("id: p1\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(root, "things/p2.md", thing_text("id: p2\ntype: note\nstatus: active\ncreated: 2026-08-01"))
    write(root, "things/live.md",
          thing_text("id: live\ntype: conflict\nstatus: open\ncreated: 2026-08-01\n"
                     "linked_things:\n  - id: p1\n    relation: contradicts\n"
                     "  - id: p2\n    relation: contradicts"))
    write(root, "things/quiet.md",
          thing_text("id: quiet\ntype: conflict\nstatus: open\ncreated: 2026-08-01\n"
                     "linked_things:\n  - id: p1\n    relation: contradicts\n"
                     "  - id: p2\n    relation: contradicts"))
    write(root, "things/holder.md",
          thing_text("id: holder\ntype: plan\nstatus: in-progress\ncreated: 2026-10-01\n"
                     "linked_things:\n  - id: live\n    relation: references"))
    _commit(root, "two aged conflicts", "2026-08-01")
    rep = _reckon(root)
    assert _ids(rep, "residue").get("live", "").startswith("rule: choose a side")
    assert _ids(rep, "settled").get("quiet", "").startswith("rule, link from live work")


def test_fresh_conflict_is_quiet(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/p1.md", thing_text("id: p1\ntype: note\nstatus: active\ncreated: 2026-10-01"))
    write(root, "things/p2.md", thing_text("id: p2\ntype: note\nstatus: active\ncreated: 2026-10-01"))
    write(root, "things/new.md",
          thing_text("id: new\ntype: conflict\nstatus: open\ncreated: 2026-10-01\n"
                     "linked_things:\n  - id: p1\n    relation: contradicts\n"
                     "  - id: p2\n    relation: contradicts"))
    _commit(root, "a fresh conflict", "2026-10-01")
    rep = _reckon(root)
    assert all("new" not in _ids(rep, b) for b in ("mechanical", "settled", "residue"))


# ---------------------------------------------------------------------- cues

def test_open_cue_is_settled(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/cue-plan-a.md",
          thing_text("id: cue-plan-a\ntype: cue\nstatus: open\ncreated: 2026-09-20\n"
                     "subject: plan-a\nraised_at: HEAD\nraised_by: test"))
    _commit(root, "an open cue")
    rep = _reckon(root)
    assert _ids(rep, "settled").get("cue-plan-a") == "answer by citation, or walk"


# ---------------------------------------------------------------------- work

def test_plan_with_every_box_ticked_is_mechanical(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/done.md",
          thing_text("id: done\ntype: plan\nstatus: in-progress\ncreated: 2026-09-01",
                     "# D\n\n- [x] one\n- [x] two\n"))
    _commit(root, "a finished plan still open")
    rep = _reckon(root)
    assert _ids(rep, "mechanical") == {"done": "complete"}


def test_untouched_work_past_the_stall_line_is_settled_and_a_cancelled_parent_is_residue(tmp_path):
    root = _repo(tmp_path)   # plan-a: in-progress, committed 2026-07-01, one box open
    write(root, "things/parent.md",
          thing_text("id: parent\ntype: plan\nstatus: cancelled\ncreated: 2026-06-01"))
    write(root, "things/child.md",
          thing_text("id: child\ntype: plan\nstatus: in-progress\ncreated: 2026-06-01\n"
                     "parent: parent", "# C\n\n- [ ] x\n"))
    _commit(root, "a child of a cancelled plan", "2026-06-01")
    rep = _reckon(root)
    assert _ids(rep, "settled").get("plan-a", "").startswith("pause")
    assert _ids(rep, "residue").get("child", "").startswith("cancel or re-parent")


def test_fresh_work_is_quiet(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/fresh.md",
          thing_text("id: fresh\ntype: plan\nstatus: in-progress\ncreated: 2026-10-04",
                     "# F\n\n- [ ] x\n"))
    _commit(root, "fresh work", "2026-10-04")
    rep = _reckon(root)
    assert all("fresh" not in _ids(rep, b) for b in ("mechanical", "settled", "residue"))


# ------------------------------------------------------------------ triggers

def test_fired_trigger_is_settled_and_a_self_answering_one_is_mechanical(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/t1.md",
          thing_text("id: t1\ntype: plan\nstatus: in-progress\ncreated: 2026-09-01\n"
                     "triggers:\n  - type: time\n    condition: \"2026-09-20 reached\"\n"
                     "    action: surface\n    note: \"ask whether the cut is still owed\"",
                     "# T\n\n- [ ] x\n"))
    _commit(root, "a fired trigger", "2026-09-01")
    rep = _reckon(root)
    assert any(i.thing_id == "t1[0]" and i.kind == "trigger" for i in rep["bands"]["settled"])


# --------------------------------------------------------------- the surface

def test_clean_corpus_reports_none_and_the_cli_exits_zero(tmp_path, capsys):
    root = tmp_path / "clean"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "things/fresh.md",
          thing_text("id: fresh\ntype: plan\nstatus: in-progress\ncreated: 2026-10-04",
                     "# F\n\n- [ ] x\n"))
    _commit(root, "fresh", "2026-10-04")
    from markdownllm.reckon import cmd_reckon
    rc = cmd_reckon(argparse.Namespace(path=str(root), imports=False))
    out = capsys.readouterr().out
    assert rc == 0 and "## The reckoning" in out and "- none" in out
    assert "`--imports`" in out  # the membrane is read only on request


def test_render_lists_each_band_with_evidence(tmp_path, capsys):
    root = _repo(tmp_path)
    write(root, "things/i1.md",
          thing_text("id: i1\ntype: insight\nstatus: active\ncreated: 2026-09-30\n"
                     "promoted_to: plan-a"))
    _commit(root, "promoted in fact")
    from markdownllm.reckon import cmd_reckon
    cmd_reckon(argparse.Namespace(path=str(root), imports=False))
    out = capsys.readouterr().out
    assert "**Mechanical (1):**" in out and "insight `i1` → promote" in out
    assert "**Settled (1):**" in out and "work `plan-a` → pause" in out
    assert "Residue" not in out  # green is reachable


# --------------------------------------------------------- apply (Phase 2)

def test_apply_writes_only_the_mechanical_band_in_place(tmp_path, capsys):
    root = _repo(tmp_path)
    write(root, "things/i1.md",
          thing_text("id: i1\ntype: insight\nstatus: active\ncreated: 2026-09-30\n"
                     "promoted_to: plan-a"))
    write(root, "things/d1.md", thing_text("id: d1\ntype: decision\nstatus: superseded\ncreated: 2026-08-01"))
    write(root, "things/d2.md", thing_text("id: d2\ntype: decision\nstatus: made\ncreated: 2026-08-01"))
    write(root, "things/c1.md",
          thing_text("id: c1\ntype: conflict\nstatus: open\ncreated: 2026-08-01\n"
                     "parties:\n  - d1\n  - d2\n"
                     "linked_things:\n  - id: d1\n    relation: contradicts\n"
                     "  - id: d2\n    relation: contradicts"))
    write(root, "things/done.md",
          thing_text("id: done\ntype: plan\nstatus: in-progress\ncreated: 2026-09-01",
                     "# D\n\n- [x] one\n- [x] two\n"))
    write(root, "things/old.md",
          thing_text("id: old\ntype: insight\nstatus: active\ncreated: 2026-07-01"))
    _commit(root, "a corpus with every mechanical shape and one settled")
    from markdownllm.reckon import cmd_reckon
    rc = cmd_reckon(argparse.Namespace(path=str(root), imports=False, apply=True, rates=False))
    out = capsys.readouterr().out
    assert rc == 0 and "**Applied (3):**" in out
    assert "status: promoted" in (root / "things/i1.md").read_text(encoding="utf-8")
    c1 = (root / "things/c1.md").read_text(encoding="utf-8")
    assert "status: resolved" in c1 and "resolution: superseded" in c1 and "resolved_by: d2" in c1
    assert "status: completed" in (root / "things/done.md").read_text(encoding="utf-8")
    # The settled band is never touched: the orphan insight stays active.
    assert "status: active" in (root / "things/old.md").read_text(encoding="utf-8")
    # Applied, the mechanical band is empty on the next read: green is reachable.
    rep = _reckon(root)
    assert rep["bands"]["mechanical"] == []


def test_apply_leaves_a_self_answering_trigger_to_the_agent(tmp_path, capsys):
    root = _repo(tmp_path)
    write(root, "things/t1.md",
          thing_text("id: t1\ntype: plan\nstatus: in-progress\ncreated: 2026-09-01\n"
                     "triggers:\n  - type: time\n    condition: \"2026-12-20 reached\"\n"
                     "    action: \"surface — already answered on 2026-09-02; do not re-ask\"",
                     "# T\n\n- [ ] x\n"))
    _commit(root, "an armed trigger that answers itself")
    from markdownllm.reckon import cmd_reckon
    cmd_reckon(argparse.Namespace(path=str(root), imports=False, apply=True, rates=False))
    out = capsys.readouterr().out
    text = (root / "things/t1.md").read_text(encoding="utf-8")
    assert "triggers:" in text and "do not re-ask" in text  # untouched by the floor
    assert "Applied (0)" in out or "left to the agent" in out or "nothing to apply" in out


# --------------------------------------------------------- rates (Phase 2)

def test_rates_count_intake_disposal_and_walks_in_the_window(tmp_path):
    root = _repo(tmp_path)
    write(root, "things/i1.md", thing_text("id: i1\ntype: insight\nstatus: active\ncreated: 2026-10-01"))
    write(root, "things/c1.md",
          thing_text("id: c1\ntype: conflict\nstatus: open\ncreated: 2026-10-01\n"
                     "linked_things:\n  - id: i1\n    relation: contradicts"))
    write(root, "things/skill.md", thing_text("id: skill\ntype: skill\nstatus: active\ncreated: 2026-10-01"))
    _commit(root, "intake", "2026-10-03")
    p = root / "things/skill.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nrevised\n", encoding="utf-8")
    write(root, "things/cue-skill.md",
          thing_text("id: cue-skill\ntype: cue\nstatus: answered\ncreated: 2026-10-04\n"
                     "subject: skill\nraised_at: HEAD\nraised_by: test\nverdict: not-inflection\n"
                     "verdict_reason: wording"))
    _commit(root, "a surface changed and walked", "2026-10-04")
    p = root / "things/c1.md"
    p.write_text(p.read_text(encoding="utf-8").replace("status: open", "status: resolved\nresolution: dismissed"),
                 encoding="utf-8")
    _commit(root, "a conflict disposed", "2026-10-05")
    from markdownllm.model import scan
    from markdownllm.reckon import rates
    corpus, _ = scan(root)
    rt = rates(root, corpus, days=3650)  # the window covers the fixture's dates
    assert rt["created"] == {"insight": 1, "conflict": 1, "cue": 1}
    assert rt["disposed"] == 1
    assert rt["surface_changes"] == 1 and rt["walks"] == 1


def test_rates_line_reads_as_one_digest_line(tmp_path, capsys):
    root = _repo(tmp_path)
    from markdownllm.reckon import cmd_reckon
    rc = cmd_reckon(argparse.Namespace(path=str(root), imports=False, apply=False, rates=True))
    out = capsys.readouterr().out.strip()
    assert rc == 0 and out.startswith("- **Reckoning (last 7d):** intake")
    assert "mechanical /" in out and "`mdllm reckon`" in out
