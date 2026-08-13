"""Ordered, advisory execution for project-harness lifecycle bindings.

These tests replace every subprocess, adapter lookup, and attestation writer
with an in-memory fake.  They exercise the real dispatcher without firing a
harness event, touching a Git directory, or creating project ``.codex`` state.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import lifecycle_runner as lr  # noqa: E402
from markdownllm.adapters.codex import CODEX  # noqa: E402
from markdownllm.cli import build_cli  # noqa: E402
from markdownllm.harness_ports import (  # noqa: E402
    DOMAIN_ROOT_ARG,
    HarnessContext,
    LifecycleBinding,
    LifecycleStep,
)


def _binding(*steps: LifecycleStep, moment: str = "test-moment") \
        -> LifecycleBinding:
    return LifecycleBinding(
        moment=moment, steps=steps, delivery="context")


def _completed(command, returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        command, returncode, stdout=stdout, stderr=stderr)


def test_execute_runs_steps_in_order_and_continues_after_failure(
        tmp_path, monkeypatch):
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        if command[2] == "first":
            return _completed(command, 7, stdout="first out")
        return _completed(command, 0, stderr="second note")

    monkeypatch.setattr(lr.subprocess, "run", fake_run)
    binding = _binding(
        LifecycleStep("first", (DOMAIN_ROOT_ARG, "--one")),
        LifecycleStep("second", (DOMAIN_ROOT_ARG,)),
    )

    result = lr.execute_lifecycle(
        tmp_path, binding, mdllm_entry=Path("floor.py"),
        interpreter="floor-python", timeout_per_step=9,
    )

    root = str(tmp_path.resolve())
    assert [call[0][2] for call in calls] == ["first", "second"]
    assert calls[0][0] == [
        "floor-python", "floor.py", "first", root, "--one"]
    assert calls[1][0] == [
        "floor-python", "floor.py", "second", root]
    assert all(call[1]["cwd"] == tmp_path.resolve() for call in calls)
    assert all(call[1]["timeout"] == 9 for call in calls)
    assert tuple(step.returncode for step in result.steps) == (7, 0)
    assert result.passed is False
    assert result.text.startswith("[steps: first=7, second=0]\n")
    assert "[first: exit 7]" in result.text
    assert "[second: exit 0]" in result.text


def test_timeout_is_labelled_and_does_not_stop_the_next_step(
        tmp_path, monkeypatch):
    operations = []

    def fake_run(command, **kwargs):
        operations.append(command[2])
        if command[2] == "slow":
            raise subprocess.TimeoutExpired(
                command, kwargs["timeout"], output=b"partial",
                stderr=b"still running")
        return _completed(command)

    monkeypatch.setattr(lr.subprocess, "run", fake_run)

    result = lr.execute_lifecycle(
        tmp_path,
        _binding(LifecycleStep("slow"), LifecycleStep("after")),
        timeout_per_step=4,
    )

    assert operations == ["slow", "after"]
    assert tuple(step.returncode for step in result.steps) == (124, 0)
    assert result.steps[0].stdout == "partial"
    assert "step timed out after 4.0s" in result.steps[0].stderr
    assert result.text.startswith("[steps: slow=124, after=0]\n")
    assert result.passed is False


def test_os_error_is_surfaced_and_later_steps_still_run(tmp_path, monkeypatch):
    operations = []

    def fake_run(command, **kwargs):
        operations.append(command[2])
        if command[2] == "missing":
            raise FileNotFoundError("interpreter disappeared")
        return _completed(command)

    monkeypatch.setattr(lr.subprocess, "run", fake_run)

    result = lr.execute_lifecycle(
        tmp_path,
        _binding(LifecycleStep("missing"), LifecycleStep("after")),
    )

    assert operations == ["missing", "after"]
    assert tuple(step.returncode for step in result.steps) == (127, 0)
    assert "FileNotFoundError" in result.steps[0].stderr
    assert result.passed is False


def test_total_budget_reserves_outer_hook_time_and_labels_unrun_steps(
        tmp_path, monkeypatch):
    clock = iter((0.0, 0.0, 101.0))
    calls = []
    monkeypatch.setattr(lr.time, "monotonic", lambda: next(clock))

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return _completed(command)

    monkeypatch.setattr(lr.subprocess, "run", fake_run)

    result = lr.execute_lifecycle(
        tmp_path,
        _binding(LifecycleStep("first", protected_seconds=75),
                 LifecycleStep("after-budget", protected_seconds=25)),
        total_timeout=105,
    )

    assert [call[0][2] for call in calls] == ["first"]
    assert calls[0][1]["timeout"] == 75.0
    assert tuple(step.returncode for step in result.steps) == (0, 124)
    assert "application budget of 100s exhausted" in result.steps[1].stderr
    assert result.text.startswith("[steps: first=0, after-budget=124]\n")
    assert result.passed is False


def test_later_step_inherits_unused_earlier_budget_without_stealing_its_floor(
        tmp_path, monkeypatch):
    clock = iter((0.0, 0.0, 60.0))
    calls = []
    monkeypatch.setattr(lr.time, "monotonic", lambda: next(clock))

    def fake_run(command, **kwargs):
        calls.append((command[2], kwargs["timeout"]))
        return _completed(command)

    monkeypatch.setattr(lr.subprocess, "run", fake_run)

    result = lr.execute_lifecycle(
        tmp_path,
        _binding(LifecycleStep("estate-sync", protected_seconds=75),
                 LifecycleStep("session-start", protected_seconds=25)),
        total_timeout=105,
    )

    assert calls == [("estate-sync", 75.0), ("session-start", 40.0)]
    assert result.passed is True


def test_output_limit_is_strict_and_keeps_every_step_attributable(
        tmp_path, monkeypatch):
    def fake_run(command, **kwargs):
        return _completed(command, stdout=command[2] * 400)

    monkeypatch.setattr(lr.subprocess, "run", fake_run)
    limit = 120

    result = lr.execute_lifecycle(
        tmp_path,
        _binding(LifecycleStep("first"), LifecycleStep("second")),
        output_limit=limit,
    )

    assert len(result.text) <= limit
    assert result.text.startswith("[steps: first=0, second=0]\n")
    assert "first=0" in result.text and "second=0" in result.text
    assert "truncated" in result.text


@pytest.mark.parametrize("limit", [0, 1, 8, 31])
def test_tiny_output_limits_never_overrun(limit):
    assert len(lr._bounded("x" * 100, limit)) <= limit


def test_invalid_execution_bounds_fail_before_any_subprocess(
        tmp_path, monkeypatch):
    def unexpected(*args, **kwargs):  # pragma: no cover - assertion helper
        raise AssertionError("subprocess must not run")

    monkeypatch.setattr(lr.subprocess, "run", unexpected)
    binding = _binding(LifecycleStep("one"))
    with pytest.raises(ValueError, match="non-negative"):
        lr.execute_lifecycle(tmp_path, binding, output_limit=-1)
    with pytest.raises(ValueError, match="positive"):
        lr.execute_lifecycle(tmp_path, binding, timeout_per_step=0)
    with pytest.raises(ValueError, match="total timeout must be positive"):
        lr.execute_lifecycle(tmp_path, binding, total_timeout=0)


class _OutputAdapter:
    name = "fake-harness"

    def __init__(self, *, raises: bool = False):
        self.raises = raises
        self.calls = []

    def format_lifecycle_output(self, moment, text, passed):
        self.calls.append((moment, text, passed))
        if self.raises:
            raise RuntimeError("cannot encode output")
        return f"envelope:{moment}:{passed}:{text}"


class _FormatOnlyAdapter:
    """Exactly the declared LifecycleOutputPort; no accidental attributes."""

    def format_lifecycle_output(self, moment, text, passed):
        return f"{moment}:{passed}:{text}"


def _args(**overrides):
    values = {
        "harness": "fake-harness",
        "moment": "session-start",
        "path": ".",
        "definition_hash": "sha256:pinned-definition",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _execution(*, passed=True, text="orientation"):
    return lr.LifecycleExecution(
        moment="session-start",
        steps=(
            lr.StepExecution("estate-sync", (".",), 0),
            lr.StepExecution(
                "session-start", (".",), 0 if passed else 3),
        ),
        text=text,
        passed=passed,
    )


def test_dispatch_attests_exact_hash_and_formats_through_adapter_port(
        tmp_path, monkeypatch, capsys):
    adapter = _OutputAdapter()
    recorded = []
    execution = _execution()
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: execution,
    )
    monkeypatch.setattr(
        lr, "record_execution_attestation",
        lambda *args, **kwargs: recorded.append((args, kwargs)),
    )

    result = lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness",
        definition_hash="sha256:pinned-definition", output_port=adapter)

    assert result == 0
    assert recorded == [( (
        tmp_path.resolve(), adapter.name, "session-start",
        "sha256:pinned-definition",
    ), {
        "outcome": "passed",
        "source": "fake-harness-project-hook",
        "detail": "estate-sync=0, session-start=0",
    })]
    assert adapter.calls == [("session-start", "orientation", True)]
    assert capsys.readouterr().out.strip() == \
        "envelope:session-start:True:orientation"


def test_failed_lifecycle_is_attested_and_advisory(tmp_path, monkeypatch):
    adapter = _OutputAdapter()
    recorded = []
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: _execution(passed=False),
    )
    monkeypatch.setattr(
        lr, "record_execution_attestation",
        lambda *args, **kwargs: recorded.append((args, kwargs)),
    )

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned-definition",
        output_port=adapter) == 0
    assert recorded[0][1]["outcome"] == "failed"
    assert adapter.calls[0][2] is False


def test_dispatch_uses_declared_output_port_without_hidden_name_dependency(
        tmp_path, monkeypatch):
    adapter = _FormatOnlyAdapter()
    recorded = []
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: _execution(),
    )
    monkeypatch.setattr(
        lr, "record_execution_attestation",
        lambda *args, **kwargs: recorded.append((args, kwargs)),
    )

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned-definition",
        output_port=adapter) == 0
    assert recorded[0][0][1] == "fake-harness"
    assert recorded[0][1]["source"] == "fake-harness-project-hook"


def test_attestation_failure_is_bounded_attributable_and_advisory(
        tmp_path, monkeypatch):
    adapter = _OutputAdapter()
    prefix = "[steps: estate-sync=0, session-start=0]\n"
    long_text = prefix + "x" * (2200 - len(prefix))
    assert len(long_text) == 2200
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: _execution(text=long_text),
    )

    def unavailable(*args, **kwargs):
        raise OSError("read-only Git directory")

    monkeypatch.setattr(lr, "record_execution_attestation", unavailable)

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned-definition",
        output_port=adapter) == 0
    # The first pure formatting pass precedes evidence.  Evidence failure then
    # produces one final envelope containing the advisory failure.
    _, text, passed = adapter.calls[-1]
    assert len(text) <= 2200
    assert text.startswith("[steps: estate-sync=0, session-start=0]\n")
    assert "attestation unavailable" in text
    assert passed is False


def test_adapter_translation_bug_is_surfaced_without_enforcement(
        tmp_path, monkeypatch, capsys):
    adapter = _OutputAdapter(raises=True)
    recorded = []
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: _execution(),
    )
    monkeypatch.setattr(lr, "record_execution_attestation",
                        lambda *args, **kwargs:
                        recorded.append((args, kwargs)))

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned-definition",
        output_port=adapter) == 0
    output = capsys.readouterr().out
    assert "lifecycle output translation failed" in output
    assert "RuntimeError: cannot encode output" in output
    assert recorded[0][1]["outcome"] == "failed"
    assert "output-format=RuntimeError" in recorded[0][1]["detail"]


def test_dispatch_rejects_adapter_without_lifecycle_output_port(capsys):
    assert lr.dispatch_lifecycle_event(
        Path("."), HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned-definition",
        output_port=object()) == 2
    assert "has no lifecycle output port" in capsys.readouterr().out


def test_cli_wires_hash_bound_internal_harness_event():
    args = build_cli().parse_args([
        "harness-event", "codex", "session-start", ".", "sha256:pinned",
    ])
    assert args.fn is lr.cmd_harness_event
    assert args.harness == "codex"
    assert args.moment == "session-start"
    assert args.definition_hash == "sha256:pinned"


def test_definition_hash_changes_with_inward_binding_semantics():
    standard = HarnessContext("../framework")
    changed_start = LifecycleBinding(
        moment="session-start",
        steps=(LifecycleStep("session-start"), LifecycleStep("estate-sync")),
        delivery="context",
    )
    changed = HarnessContext(
        "../framework",
        bindings=(changed_start, standard.binding("post-write")),
    )

    original_hash = CODEX.probe(
        Path("unused"), standard).definition_hashes["session-start"]
    changed_hash = CODEX.probe(
        Path("unused"), changed).definition_hashes["session-start"]

    assert original_hash != changed_hash
