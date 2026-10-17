"""Ordered, advisory execution for project-harness lifecycle bindings.

These tests replace every subprocess, adapter lookup, and attestation writer
with an in-memory fake.  They exercise the real dispatcher without firing a
harness event, touching a Git directory, or creating project ``.codex`` state.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import lifecycle_runner as lr  # noqa: E402
from markdownllm.adapters.codex import CODEX  # noqa: E402
from markdownllm.adapters.claude_code import CLAUDE_CODE  # noqa: E402
from markdownllm.cli import build_cli  # noqa: E402
from markdownllm.harness_ports import (  # noqa: E402
    DOMAIN_ROOT_ARG,
    HarnessContext,
    LifecycleBinding,
    LifecycleAdmission,
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


# ------------------------------------------------ the startup-context share
# The session-start binding since 2026-10-18 (session-start-hardening Phase
# 6): a 9,800-character envelope under Claude Code's 10,000-character cap on a
# hook's additionalContext, allocated reader-first — the digest takes what it
# needs, the sync report takes the rest — and cut on whole trailing lines with
# one marker. The 2,200-character envelope before it cut a ~5,000-character
# digest mid-bullet on every line (measured 2026-10-17).

_UPCOMING = ("- **Upcoming (within 30d — not yet fired) (2):**\n"
             "    - `the-reckoning`: time condition '2026-10-19 reached'"
             " - fires in 1d\n"
             "    - `the-seat`: time condition '2026-10-29 reached'"
             " - fires in 11d")


def _digest(at_least: int) -> str:
    """A session-start digest in its emitted shape — the heading, the
    numbered steps, then `- **Heading:**` sections in attention order with
    nested bullets, 'Upcoming' last — grown past ``at_least`` characters."""
    head = "\n".join((
        "# MarkdownLLM — Session Start (run before the user's first request)",
        "",
        "The live request will pull you toward itself; do these first:",
        "1. **Kernel NOT emitted** (hook channel budget) — read `kernel.md`"
        " END TO END before acting on anything below.",
        "",
        "- **Significant-read base:** `commit:" + "e" * 40 + "` — pin any"
        " full-corpus read to these immutable bytes.",
        "",
    ))
    sections: list[str] = []
    while len(head) + sum(len(s) + 1 for s in sections) < at_least:
        index = len(sections)
        sections.append(
            f"- **Section {index} ({index}):** attention line {index}\n"
            f"    - `thing-{index:03d}` (plan, in-progress) untouched {index}d")
    return head + "\n".join(sections) + "\n" + _UPCOMING


def _sync_report(repos: int) -> str:
    """The estate-sync report in its runner-channel shape (sync.py): the
    heading and counts line as one section, the attention lines, the quiet
    lines, the closing line."""
    attention = "\n".join(
        f"- `repo-{index:02d}`: fetch-failed — undiagnosed (remote:"
        " Repository not found.) — orienting from last-fetched state"
        for index in range(repos - 2))
    quiet = ("- `quiet-repo-a`: up-to-date\n"
             "- `quiet-repo-b`: local-only")
    return "\n".join((
        f"## Estate Sync — estate ({repos} repo(s))",
        f"{repos} repo(s): {repos - 2} fetch-failed · 1 local-only"
        " · 1 up-to-date — attention first, quiet last",
        "", attention, "", quiet, "",
        "This is a batch of per-repo reads — ephemeral, never an index."
        " Sync before orienting.",
    ))


def _run_session_start(tmp_path, monkeypatch, *, digest: str, sync: str):
    def fake_run(command, **kwargs):
        return _completed(
            command, stdout=(sync if command[2] == "estate-sync" else digest))

    monkeypatch.setattr(lr.subprocess, "run", fake_run)
    binding = HarnessContext(".").binding("session-start")
    result = lr.execute_lifecycle(tmp_path, binding)
    sync_block, digest_block = result.text.split(
        "\n\n[session-start: exit 0]\n")
    sync_block = sync_block.split("[estate-sync: exit 0]\n", 1)[1]
    return binding, result, sync_block, digest_block


def _whole_lines_of(block: str, original: str) -> bool:
    """Every line of a cut block is a whole line of what was emitted —
    nothing cut mid-bullet — except the one marker."""
    emitted = set(original.splitlines())
    return all(line in emitted for line in block.splitlines()
               if line != "[truncated]")


def test_startup_context_lands_the_digest_and_the_sync_report_whole(
        tmp_path, monkeypatch):
    digest = _digest(5000)
    sync = _sync_report(18)
    assert 5000 <= len(digest) <= 5400 and 1900 <= len(sync) <= 2300

    binding, result, sync_block, digest_block = _run_session_start(
        tmp_path, monkeypatch, digest=digest, sync=sync)

    assert len(result.text) <= binding.output_limit_characters == 9800
    assert result.text.startswith("[steps: estate-sync=0, session-start=0]\n")
    assert digest_block == digest and sync_block == sync
    assert "[truncated]" not in result.text
    # Claude's envelope carries the text as one additionalContext string,
    # which is what the 10,000-character cap measures.
    envelope = json.loads(CLAUDE_CODE.format_lifecycle_output(
        "session-start", result.text, True))
    assert envelope["hookSpecificOutput"]["additionalContext"] == result.text
    assert len(envelope["hookSpecificOutput"]["additionalContext"]) <= 10_000
    # Presentation is bounded; execution evidence retains the complete raw
    # output so compaction never reclassifies omitted text as disposable.
    assert result.steps[0].stdout == sync
    assert result.steps[1].stdout == digest


def test_busy_digest_is_cut_on_whole_trailing_lines_with_one_marker(
        tmp_path, monkeypatch):
    digest = _digest(12_000)
    sync = _sync_report(16)

    binding, result, sync_block, digest_block = _run_session_start(
        tmp_path, monkeypatch, digest=digest, sync=sync)

    assert len(result.text) <= binding.output_limit_characters
    # The digest took first: the leading sections whole, in order, and the
    # cut on a whole line at the tail — one marker, last.
    assert digest_block.count("[truncated]") == 1
    assert digest_block.endswith("\n[truncated]")
    assert digest_block.startswith(digest[:600])
    assert _whole_lines_of(digest_block, digest)
    assert len(digest_block) >= 9000
    assert "**Upcoming" not in digest_block  # the trailing section, whole
    # The sync report gave way first — down to its protected share, which
    # keeps the heading, the counts line and the first attention lines.
    assert sync_block.count("[truncated]") == 1
    assert sync_block.startswith(
        "## Estate Sync — estate (16 repo(s))\n16 repo(s): 14 fetch-failed")
    assert _whole_lines_of(sync_block, sync)
    assert len(sync_block) < 600  # its 450 share plus what the digest left
    assert "quiet-repo" not in sync_block


def test_sync_report_is_compressed_before_the_digest_is_cut(
        tmp_path, monkeypatch):
    # Together over the envelope; the digest alone fits. The digest lands
    # whole and the sync report loses its quiet tail, on whole lines.
    digest = _digest(8000)
    sync = _sync_report(16)
    assert len(digest) + len(sync) > 9600

    binding, result, sync_block, digest_block = _run_session_start(
        tmp_path, monkeypatch, digest=digest, sync=sync)

    assert len(result.text) <= binding.output_limit_characters
    assert digest_block == digest
    assert sync_block.count("[truncated]") == 1
    assert sync_block.endswith("\n[truncated]")
    assert sync_block.startswith("## Estate Sync — estate (16 repo(s))\n")
    assert "- `repo-00`: fetch-failed" in sync_block
    assert "quiet-repo" not in sync_block
    assert _whole_lines_of(sync_block, sync)


@pytest.mark.parametrize("limit", [0, 1, 8, 13, 40, 90, 200, 400])
def test_tail_bound_never_overruns_and_never_cuts_a_kept_line(limit):
    text = _sync_report(6)
    bounded = lr._bounded_tail(text, limit)
    assert len(bounded) <= limit
    if limit >= 100:  # past the degenerate budget: whole lines, one marker
        assert bounded.count("[truncated]") == 1
        assert _whole_lines_of(bounded, text)
    assert lr._bounded_tail(text, len(text)) == text


def test_feedback_delivery_keeps_the_fair_share_across_findings(
        tmp_path, monkeypatch):
    # A findings list has no order of importance: every section keeps a
    # share, as before (post-write validate, the gate's cues).
    findings = "\n\n".join(
        f"## Finding {index}\n" + f"detail-{index} " * 60 for index in range(6))

    monkeypatch.setattr(
        lr.subprocess, "run",
        lambda command, **kwargs: _completed(command, stdout=findings))
    binding = HarnessContext(".").binding("post-write")
    result = lr.execute_lifecycle(tmp_path, binding)

    assert len(result.text) <= binding.output_limit_characters == 2200
    for index in range(6):
        assert f"## Finding {index}" in result.text
    assert result.text.count("[truncated]") == 6


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


class _AdmissionAdapter(_OutputAdapter):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = allowed

    def admit_lifecycle(self, domain_root, context, moment):
        del domain_root, context, moment
        return LifecycleAdmission(
            allowed=self.allowed,
            text="binding passed" if self.allowed else "binding refused",
        )



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


def test_lifecycle_admission_refusal_skips_ordered_steps(
        tmp_path, monkeypatch):
    adapter = _AdmissionAdapter(False)
    recorded = []

    def unexpected(*args, **kwargs):  # pragma: no cover - assertion helper
        raise AssertionError("refused lifecycle must not execute")

    monkeypatch.setattr(lr, "execute_lifecycle", unexpected)
    monkeypatch.setattr(
        lr, "record_execution_attestation",
        lambda *args, **kwargs: recorded.append((args, kwargs)),
    )

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned",
        output_port=adapter) == 0
    assert adapter.calls == [
        ("session-start", "binding refused", False)]
    assert recorded[0][1]["outcome"] == "failed"
    assert recorded[0][1]["detail"] == "admission=refused"


def test_lifecycle_admission_passes_context_to_ordered_output(
        tmp_path, monkeypatch):
    adapter = _AdmissionAdapter(True)
    recorded = []
    monkeypatch.setattr(
        lr, "execute_lifecycle",
        lambda root, binding: _execution(text="orientation"),
    )
    monkeypatch.setattr(
        lr, "record_execution_attestation",
        lambda *args, **kwargs: recorded.append((args, kwargs)),
    )

    assert lr.dispatch_lifecycle_event(
        tmp_path, HarnessContext(".").binding("session-start"),
        harness="fake-harness", definition_hash="sha256:pinned",
        output_port=adapter) == 0
    _, text, passed = adapter.calls[0]
    assert passed is True
    assert "binding passed" in text
    assert "orientation" in text
    assert recorded[0][1]["detail"].startswith("admission=passed")



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
    binding = HarnessContext(".").binding("session-start")
    prefix = "[steps: estate-sync=0, session-start=0]\n"
    long_text = prefix + "x" * (binding.output_limit_characters - len(prefix))
    assert len(long_text) == binding.output_limit_characters
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
    assert len(text) <= binding.output_limit_characters
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


def test_definition_hash_changes_with_output_allocation_semantics():
    standard = HarnessContext("../framework")
    start = standard.binding("session-start")
    changed_start = replace(
        start,
        steps=(start.steps[0], replace(
            start.steps[1], protected_characters=
            start.steps[1].protected_characters + 1)),
    )
    changed = HarnessContext(
        "../framework",
        bindings=(changed_start, standard.binding("post-write")),
    )

    for adapter in (CODEX, CLAUDE_CODE):
        original = adapter.probe(
            Path("unused"), standard).definition_hashes["session-start"]
        revised = adapter.probe(
            Path("unused"), changed).definition_hashes["session-start"]
        assert revised != original
