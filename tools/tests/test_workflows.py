"""Workflows emerge from use; the work is the run
(workflows-emerge-from-use-2026-10-07; workflow-state.md → Carrier Binding,
Workflows Emerge From Use). `mdllm workflows` reads definitions with their
carrier-derived runs and departures; `--emergent` finds the paths a type keeps
travelling; `--draft` writes the skeleton. These tests pin each on a small
corpus with a real, dated git history.

Run: python -m pytest tools/tests/test_workflows.py -q
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import _sync_git, messages, thing_text, write  # noqa: E402


def all_findings(root):
    """The full validation pipeline, where the carrier check runs."""
    from markdownllm.validation import validate_corpus
    return validate_corpus(root)[1]

LOOP = ["draft", "review", "draft", "review", "cleared", "approved"]


def _commit(root: Path, msg: str, day: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": f"{day}T12:00:00",
           "GIT_COMMITTER_DATE": f"{day}T12:00:00"}
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=root, check=True, env=env)


def _spec(i: int, status: str) -> str:
    return thing_text(f"id: spec-{i}\ntype: spec\nstatus: {status}\ncreated: 2026-09-01")


def _set(root: Path, i: int, status: str) -> None:
    write(root, f"things/spec-{i}.md", _spec(i, status))


def _repo_with_loop(tmp_path: Path, things: int = 3, same_day: bool = False) -> Path:
    """`things` specs each travelling draft ⇄ review → cleared → approved,
    one move a day (or all on one day)."""
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    write(root, "_schema.yaml",
          "types:\n  spec:\n    statuses: [draft, review, cleared, approved]\n"
          "    terminal_statuses: [approved]\n")
    for i in range(things):
        _set(root, i, LOOP[0])
    _commit(root, "create: the specs", "2026-09-01")
    for step, status in enumerate(LOOP[1:], start=2):
        for i in range(things):
            _set(root, i, status)
        day = "2026-09-02" if same_day else f"2026-09-{step:02d}"
        _commit(root, f"review: specs move to {status}", day)
    return root


def _run(root: Path, capsys, **kw) -> str:
    from markdownllm.workflows import cmd_workflows
    ns = argparse.Namespace(path=str(root), emergent=kw.get("emergent", False),
                            draft=kw.get("draft", False))
    assert cmd_workflows(ns) == 0
    return capsys.readouterr().out


# ----------------------------------------------------------------- emergence

def test_a_path_travelled_across_days_emerges_with_evidence(tmp_path, capsys):
    root = _repo_with_loop(tmp_path)
    out = _run(root, capsys, emergent=True)
    assert "**Emergent (1):**" in out
    assert "`spec` — stages draft · review · cleared · approved" in out
    assert "15 moves, 3 things" in out


def test_same_day_bookkeeping_does_not_emerge(tmp_path, capsys):
    root = _repo_with_loop(tmp_path, same_day=True)
    out = _run(root, capsys, emergent=True)
    assert "**Emergent:** none" in out


def test_a_generic_lifecycle_is_not_a_workflow(tmp_path, capsys):
    root = tmp_path / "dom"
    (root / "things").mkdir(parents=True)
    _sync_git(root, "init", "-q")
    for i in range(4):
        write(root, f"things/p{i}.md", thing_text(f"id: p{i}\ntype: plan\nstatus: not-started\ncreated: 2026-09-01"))
    _commit(root, "plans", "2026-09-01")
    for day, status in (("2026-09-03", "in-progress"), ("2026-09-06", "completed")):
        for i in range(4):
            write(root, f"things/p{i}.md", thing_text(f"id: p{i}\ntype: plan\nstatus: {status}\ncreated: 2026-09-01"))
        _commit(root, f"advance: {status}", day)
    out = _run(root, capsys, emergent=True)
    assert "**Emergent:** none" in out


def test_an_unbound_definition_that_overlaps_is_named_instead_of_a_new_draft(tmp_path, capsys):
    root = _repo_with_loop(tmp_path)
    write(root, "things/loop.md",
          thing_text("id: spec-loop\ntype: workflow-definition\nstatus: draft\ncreated: 2026-09-10\n"
                     "stages:\n  - id: draft\n    to: [review]\n  - id: review\n    to: [draft, approved]\n"
                     "  - id: approved\n    to: []"))
    _commit(root, "define: a loop nobody bound", "2026-09-10")
    out = _run(root, capsys, emergent=True, draft=True)
    assert "an unbound definition overlaps: `spec-loop` — bind it" in out
    assert "not drafted `spec`: bind `spec-loop` instead" in out
    assert not (root / "things/workflows/spec-workflow.md").exists()


# --------------------------------------------------------------------- draft

def test_draft_writes_an_inferred_bound_definition_that_validates(tmp_path, capsys):
    root = _repo_with_loop(tmp_path)
    out = _run(root, capsys, emergent=True, draft=True)
    path = root / "things/workflows/spec-workflow.md"
    assert "**drafted** things/workflows/spec-workflow.md" in out and path.exists()
    text = path.read_text(encoding="utf-8")
    assert "origin: inferred" in text and "carrier:\n  type: spec" in text
    assert "- id: review\n    to: [cleared, draft]" in text
    assert "- id: approved\n    to: []" in text          # terminal from the schema
    assert "`review:` ×" in text                          # the act seen on the way in
    assert messages(all_findings(root), "Error") == []
    # Never overwrites.
    out = _run(root, capsys, emergent=True, draft=True)
    assert "kept `spec-workflow`" in out or "**Emergent:** none" in out


def test_a_bound_type_no_longer_emerges_and_its_runs_are_its_things(tmp_path, capsys):
    root = _repo_with_loop(tmp_path)
    _run(root, capsys, emergent=True, draft=True)
    _commit(root, "workflow: spec emerged", "2026-09-20")
    out = _run(root, capsys, emergent=True)
    assert "**Emergent:** none" in out
    assert "carrier `spec`: runs by stage: approved 3" in out


# ------------------------------------------------------------------- binding

def _bound_def(stages_to: str, carrier: str = "  type: spec\n", status: str = "evolving",
               wid: str = "spec-loop") -> str:
    return thing_text(f"id: {wid}\ntype: workflow-definition\nstatus: {status}\ncreated: 2026-09-10\n"
                      f"carrier:\n{carrier}stages:\n{stages_to}")


STAGES = ("  - id: draft\n    to: [review]\n  - id: review\n    to: [draft, cleared]\n"
          "  - id: cleared\n    to: [approved]\n  - id: approved\n    to: []")


def test_departures_since_the_definition_changed_are_reported_not_refused(tmp_path, capsys):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES))
    _commit(root, "define", "2026-09-10")
    _set(root, 0, "draft")       # approved -> draft: not an edge
    _commit(root, "rework", "2026-09-12")
    out = _run(root, capsys)
    assert "**1 departure(s)**" in out
    assert "`spec-0`: `approved` → `draft` on 2026-09-12" in out
    assert "the operator rules: it is their workflow" in out   # authored
    assert messages(all_findings(root), "Error") == []          # never refused


def test_carrier_map_values_must_be_stages(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES, carrier="  type: spec\n  map:\n    review: reviewing\n"))
    _commit(root, "define", "2026-09-10")
    errs = messages(all_findings(root), "Error")
    assert any("sends `review` to `reviewing`, which is not a stage" in m for m in errs)


def test_two_live_bindings_of_one_type_are_refused(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES))
    write(root, "things/loop2.md", _bound_def(STAGES, wid="spec-loop-2"))
    _commit(root, "two bindings", "2026-09-10")
    errs = messages(all_findings(root), "Error")
    assert any("already the carrier of" in m for m in errs)


def test_a_deprecated_binding_does_not_count(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES, status="deprecated"))
    write(root, "things/loop2.md", _bound_def(STAGES, wid="spec-loop-2"))
    _commit(root, "an old binding retired", "2026-09-10")
    assert not any("already the carrier of" in m for m in messages(all_findings(root), "Error"))


def test_an_explicit_run_of_a_bound_definition_warns(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES))
    write(root, "things/run.md",
          thing_text("id: run-1\ntype: workflow-run\nstatus: active\ncreated: 2026-09-10\n"
                     "definition: spec-loop\ncurrent_stage: draft"))
    _commit(root, "a run beside the carrier", "2026-09-10")
    warns = messages(all_findings(root), "Warning")
    assert any("counts the work twice" in m for m in warns)


def test_a_bound_definition_with_carrier_things_is_not_a_zero_run_definition(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES))
    _commit(root, "define", "2026-09-10")
    from markdownllm.coherence import coherence_findings
    infos = messages(coherence_findings(root, 15), "Info")
    assert not any("zero workflow-runs" in m for m in infos)
    # Unbound, the same definition with no run is still a zero-run definition.
    write(root, "things/loop.md", thing_text(
        "id: spec-loop\ntype: workflow-definition\nstatus: evolving\ncreated: 2026-09-10\n"
        f"stages:\n{STAGES}"))
    infos = messages(coherence_findings(root, 15), "Info")
    assert any("zero workflow-runs" in m for m in infos)


# ------------------------------------------------------- one loop, many types

def test_one_definition_may_bind_several_types(tmp_path, capsys):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/other.md", thing_text("id: other-1\ntype: other-spec\nstatus: review\ncreated: 2026-09-01"))
    write(root, "_schema.yaml",
          "types:\n  spec:\n    statuses: [draft, review, cleared, approved]\n"
          "    terminal_statuses: [approved]\n  other-spec:\n    statuses: [draft, review, cleared, approved]\n")
    write(root, "things/loop.md", _bound_def(STAGES, carrier="  type: [spec, other-spec]\n"))
    _commit(root, "one loop over two types", "2026-09-10")
    out = _run(root, capsys)
    assert "carrier `other-spec, spec`: runs by stage:" in out
    assert "approved 2" in out and "review 1" in out
    assert messages(all_findings(root), "Error") == []


# ---------------------------------------------------- the reckoning's workflows

def _reckon(root):
    from markdownllm.model import scan
    from markdownllm.reckon import reckon_report
    corpus, _ = scan(root)
    return reckon_report(root, corpus, workflows=True)


def test_the_reckoning_carries_an_emerged_workflow_for_the_agent(tmp_path):
    root = _repo_with_loop(tmp_path)
    rep = _reckon(root)
    wf = [i for i in rep["bands"]["settled"] if i.kind == "workflow"]
    assert wf and wf[0].thing_id == "spec" and "write the emerged workflow" in wf[0].proposal


def test_the_reckoning_says_bind_when_an_unbound_definition_overlaps(tmp_path):
    root = _repo_with_loop(tmp_path)
    write(root, "things/loop.md",
          thing_text("id: spec-loop\ntype: workflow-definition\nstatus: draft\ncreated: 2026-09-10\n"
                     f"stages:\n{STAGES}"))
    _commit(root, "define, unbound", "2026-09-10")
    rep = _reckon(root)
    wf = [i for i in rep["bands"]["settled"] if i.kind == "workflow"]
    assert wf and wf[0].proposal.startswith("bind `spec-loop`")


def test_a_departure_from_an_authored_workflow_is_residue(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md", _bound_def(STAGES))
    _commit(root, "define", "2026-09-10")
    _set(root, 0, "draft")
    _commit(root, "rework", "2026-09-12")
    rep = _reckon(root)
    assert any(i.kind == "workflow" and i.thing_id == "spec-loop" for i in rep["bands"]["residue"])


def test_an_idle_inferred_workflow_dissolves_mechanically(tmp_path):
    root = _repo_with_loop(tmp_path, things=2)
    write(root, "things/loop.md",
          _bound_def(STAGES).replace("created: 2026-09-10\n", "created: 2026-09-10\norigin: inferred\n"))
    _commit(root, "an inferred workflow", "2026-09-10")
    import datetime as dt
    from markdownllm.model import scan
    from markdownllm.reckon import reckon_report
    corpus, _ = scan(root)
    rep = reckon_report(root, corpus, workflows=True, today=dt.date(2026, 12, 31))
    mech = [i for i in rep["bands"]["mechanical"] if i.kind == "workflow"]
    assert mech and mech[0].proposal == "dissolve" and mech[0].fields == {"status": "deprecated"}
    # Recently used: nothing to dissolve.
    rep = reckon_report(root, corpus, workflows=True, today=dt.date(2026, 9, 20))
    assert not [i for i in rep["bands"]["mechanical"] if i.kind == "workflow"]
