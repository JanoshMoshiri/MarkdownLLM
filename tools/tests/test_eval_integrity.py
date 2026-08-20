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
