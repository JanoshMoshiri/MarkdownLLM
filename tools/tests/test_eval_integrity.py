"""Evidence-boundary regressions from the 2026-08-20 substrate review."""

from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.evals import (  # noqa: E402
    _agent_failure,
    _command_version,
    _eval_run_dir,
    _results_exit_code,
    _run_id,
    _seed_fingerprint,
    _validation_control_failure,
    check_assertions,
)
from markdownllm.yaml_loader import load_yaml  # noqa: E402


def _thing(frontmatter: str) -> str:
    return f"---\n{frontmatter}\n---\n\n# Example\n\nBody.\n"


def test_validates_clean_uses_complete_validation_including_scan_findings(tmp_path):
    # An unparseable frontmatter document is a scan Error.  The old eval path
    # discarded scan findings and reported this corpus clean.
    (tmp_path / "broken.md").write_text(
        "---\nid: broken\ntype: task\nstatus: [unterminated\n---\n\n# Broken\n",
        encoding="utf-8")
    passed, failed, lines = check_assertions(
        {"assertions": [{"validates_clean": True}]}, tmp_path)
    assert (passed, failed) == (0, 1)
    assert "Errors: 1" in lines[0]


def test_numeric_assertion_compares_retained_decimal_lexemes_not_float_values(
        tmp_path):
    (tmp_path / "things").mkdir()
    (tmp_path / "things" / "amount.md").write_text(_thing(
        "id: amount\n"
        "type: note\n"
        "status: active\n"
        "created: 2026-08-20\n"
        "value: 0.100000000000000005"), encoding="utf-8")
    fixture = load_yaml(
        "assertions:\n"
        "  - field:\n"
        "      id: amount\n"
        "      name: value\n"
        "      equals: 0.100000000000000006\n",
        source="fixture")
    # These collapse to one binary float.  Their retained YAML tokens do not.
    assert float(fixture["assertions"][0]["field"]["equals"]) == 0.1
    passed, failed, _ = check_assertions(fixture, tmp_path)
    assert (passed, failed) == (0, 1)


def test_validation_error_is_an_unconditional_agent_trial_leg():
    summary = {"errors": 1, "warnings": 0, "info": 0}
    assert _validation_control_failure([], summary)
    assert not _validation_control_failure(
        [{"validates_clean": True}], summary), \
        "the explicit assertion owns the same failure and is not double-counted"
    assert not _validation_control_failure([], {**summary, "errors": 0})


def test_agent_failure_keeps_process_transport_and_agent_state_distinct():
    assert _agent_failure(SimpleNamespace(returncode=7), {"subtype": "success"}) \
        == "process exited 7"
    assert _agent_failure(SimpleNamespace(returncode=0), None) \
        == "agent stdout is not a JSON object"
    assert _agent_failure(SimpleNamespace(returncode=0), []) \
        == "agent stdout is not a JSON object"
    assert "agent reported error" in _agent_failure(
        SimpleNamespace(returncode=0), {"is_error": True, "subtype": "tool_error"})
    assert _agent_failure(SimpleNamespace(returncode=0), {"subtype": "success"}) is None


def test_harness_build_is_observed_not_inferred(monkeypatch):
    monkeypatch.setattr(
        "markdownllm.evals.subprocess.run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=0, stdout="2.1.229 (Claude Code)\n", stderr=""))
    assert _command_version("claude") == "2.1.229 (Claude Code)"


def test_failed_trial_makes_the_command_boundary_nonzero():
    assert _results_exit_code([{"failed": 0}, {"failed": 1}]) == 1
    assert _results_exit_code([{"failed": 0}]) == 0


def test_run_ids_do_not_collide_within_one_clock_tick(monkeypatch):
    class Frozen(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 8, 20, 12, 0, 0, 123456, tzinfo=tz)

    monkeypatch.setattr("markdownllm.evals.dt.datetime", Frozen)
    ids = {_run_id("model/name", "fw", 1) for _ in range(50)}
    assert len(ids) == 50
    assert all("model-name" in rid for rid in ids)


def test_eval_workspace_refuses_to_live_under_the_source_tree(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    monkeypatch.setenv("MDLLM_EVAL_RUN_ROOT", str(source / "evals" / "runs"))
    with pytest.raises(ValueError, match="outside"):
        _eval_run_dir(source, "trial")


def test_eval_workspace_accepts_a_disjoint_root(tmp_path, monkeypatch):
    source = tmp_path / "source"
    isolated = tmp_path / "isolated"
    source.mkdir()
    monkeypatch.setenv("MDLLM_EVAL_RUN_ROOT", str(isolated))
    assert _eval_run_dir(source, "trial") == (isolated / "trial").resolve()


# --- the seed-integrity guard ---------------------------------------------
# 2026-07-09: a perturb agent edited the shared source seed and committed it to
# the framework repo; every trial seeded afterward inherited the change and a
# whole arm was scored against inputs it never had.  Workspace isolation moved
# the copy out of the repo but the framework condition still grants --add-dir
# over the framework checkout, so the seed stays reachable.  These pin the
# detector: the fingerprint sees any mutation, committed or not.


def _seed_tree(root: Path) -> Path:
    seed = root / "seed"
    (seed / "things").mkdir(parents=True)
    (seed / "AGENTS.md").write_text("# Agent\n", encoding="utf-8")
    (seed / "things" / "trip.md").write_text(
        _thing("id: trip\ntype: note\nstatus: active\ncreated: 2026-09-22\n"
               "elevation_m: 2400"), encoding="utf-8")
    return seed


def test_seed_fingerprint_is_stable_across_reads(tmp_path):
    seed = _seed_tree(tmp_path)
    assert _seed_fingerprint(seed) == _seed_fingerprint(seed)


def test_seed_fingerprint_moves_when_a_fact_is_edited_in_place(tmp_path):
    """The exact 2026-07 mutation: a value changed inside an existing file."""
    seed = _seed_tree(tmp_path)
    before = _seed_fingerprint(seed)
    trip = seed / "things" / "trip.md"
    trip.write_text(trip.read_text(encoding="utf-8").replace("2400", "3300"),
                    encoding="utf-8")
    assert _seed_fingerprint(seed) != before


def test_seed_fingerprint_moves_on_addition_and_on_deletion(tmp_path):
    seed = _seed_tree(tmp_path)
    before = _seed_fingerprint(seed)

    added = seed / "things" / "extra.md"
    added.write_text(_thing("id: extra\ntype: note\nstatus: active\n"
                            "created: 2026-09-22"), encoding="utf-8")
    assert _seed_fingerprint(seed) != before
    added.unlink()
    assert _seed_fingerprint(seed) == before

    (seed / "AGENTS.md").unlink()
    assert _seed_fingerprint(seed) != before


def test_seed_fingerprint_distinguishes_content_from_placement(tmp_path):
    """Path is hashed alongside content, so moving a file is a mutation —
    a rename that preserves bytes still changes what a trial was seeded from."""
    seed = _seed_tree(tmp_path)
    before = _seed_fingerprint(seed)
    trip = seed / "things" / "trip.md"
    trip.rename(seed / "things" / "trip-renamed.md")
    assert _seed_fingerprint(seed) != before


def test_seed_fingerprint_does_not_consult_git(tmp_path):
    """A HEAD comparison would have moved WITH the 2026-07 damage, because the
    agent committed it. The digest must read bytes, not revisions."""
    seed = _seed_tree(tmp_path)
    before = _seed_fingerprint(seed)
    (seed / ".git").mkdir()
    (seed / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
    after_git_dir = _seed_fingerprint(seed)
    assert after_git_dir != before, (
        "files under the seed are hashed wholesale; this documents that a .git "
        "directory inside a seed would itself count as content")


# ---- 2026-10-05 cold-review controls -----------------------------------------
# The framework arm used to be granted the whole checkout — including evals/,
# every fixture's expected figures. It now gets a pruned view; the view, the
# transcript and the assertion tags each carry a guard.

from markdownllm.evals import (  # noqa: E402
    FRAMEWORK_VIEW_INCLUDE,
    _answer_key_hits,
    build_framework_view,
    check_assertions_detailed,
)


def test_framework_view_never_contains_the_answer_key(tmp_path, monkeypatch):
    root = tmp_path / "fw"
    (root / "evals").mkdir(parents=True)
    (root / "evals" / "x-longitudinal.yaml").write_text("answers", encoding="utf-8")
    (root / "things").mkdir()
    (root / "things" / "secret.md").write_text("x", encoding="utf-8")
    (root / "kernel.md").write_text("rules", encoding="utf-8")
    (root / "tools" / "markdownllm" / "tests").mkdir(parents=True)
    (root / "tools" / "markdownllm" / "evals.py").write_text("code", encoding="utf-8")
    (root / "tools" / "markdownllm" / "tests" / "t.py").write_text("test", encoding="utf-8")
    monkeypatch.delenv("MDLLM_EVAL_FRAMEWORK_DIR", raising=False)
    view = build_framework_view(root, tmp_path / "runs")
    assert (view / "kernel.md").read_text(encoding="utf-8") == "rules"
    assert (view / "tools" / "markdownllm" / "evals.py").is_file()
    assert not (view / "evals").exists()
    assert not (view / "things").exists()
    assert not (view / "tools" / "markdownllm" / "tests").exists()
    assert "evals" not in FRAMEWORK_VIEW_INCLUDE


def test_prepared_framework_view_with_evals_is_refused(tmp_path, monkeypatch):
    prepared = tmp_path / "prepared"
    (prepared / "evals").mkdir(parents=True)
    monkeypatch.setenv("MDLLM_EVAL_FRAMEWORK_DIR", str(prepared))
    with pytest.raises(SystemExit):
        build_framework_view(tmp_path / "fw", tmp_path / "runs")


def test_answer_key_references_in_a_transcript_are_detected():
    assert _answer_key_hits("read C:/x/evals/polar-station-longitudinal.yaml")
    assert _answer_key_hits("python evals/generators/polar_station_htc.py")
    assert _answer_key_hits("cat things/station-budget.md") == []
    # The run root itself must not trip the guard (the first smoke voided
    # every trial on its own workspace path).
    assert _answer_key_hits(r"cwd C:\Temp\mdllm-evals\20261005-x-fw-t1\things") == []


def test_reset_keeps_runner_artefacts_and_tolerates_clean_failure(tmp_path):
    import subprocess as sp
    from markdownllm.evals import _reset_to_committed, _uncommitted_work
    ws = tmp_path / "ws"
    (ws / "things").mkdir(parents=True)
    (ws / "things" / "a.md").write_text("x", encoding="utf-8")
    sp.run(["git", "init", "-q"], cwd=ws, check=True)
    sp.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A"], cwd=ws, check=True)
    sp.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "seed"],
           cwd=ws, check=True)
    (ws / "agent-stdout-1-build.json").write_text("{}", encoding="utf-8")
    (ws / "scratch.py").write_text("print()", encoding="utf-8")
    (ws / "things" / "b.md").write_text("new", encoding="utf-8")
    (ws / "things" / "a.md").write_text("edited", encoding="utf-8")
    assert sorted(_uncommitted_work(ws)) == ["things/a.md", "things/b.md"]
    assert _reset_to_committed(ws) is None
    assert (ws / "agent-stdout-1-build.json").exists()      # transcript survives
    assert not (ws / "scratch.py").exists()                  # scratch does not
    assert not (ws / "things" / "b.md").exists()
    assert (ws / "things" / "a.md").read_text(encoding="utf-8") == "x"


def test_assertions_carry_their_changed_tag_and_count_things_of_type(tmp_path):
    things = tmp_path / "things"
    things.mkdir()
    (things / "a.md").write_text(_thing("id: a\ntype: conflict\nstatus: open\ncreated: 2026-01-01"),
                                 encoding="utf-8")
    fixture = load_yaml(
        "assertions:\n"
        "  - things_of_type: {type: conflict, min: 1}\n"
        "    changed: true\n"
        "  - things_of_type: {type: decision, min: 1}\n"
        "    changed: false\n"
        "  - thing_exists: a\n")
    records = check_assertions_detailed(fixture, tmp_path)
    assert [(r["passed"], r["changed"]) for r in records] == [
        (True, True), (False, False), (True, None)]
    assert "[changed]" in records[0]["line"] and "[unchanged]" in records[1]["line"]
    passed, failed, lines = check_assertions(fixture, tmp_path)
    assert (passed, failed) == (2, 1) and len(lines) == 3
