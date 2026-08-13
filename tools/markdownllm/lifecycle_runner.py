"""Execute inward lifecycle bindings for project harness adapters.

One handler owns one binding, so ordering is deterministic even in harnesses
that launch multiple matching handlers concurrently.  The runner is neutral:
it knows lifecycle moments, commands, and evidence, while the selected adapter
serializes the event's stdout through ``LifecycleOutputPort``.

Every invocation is advisory.  Failures are surfaced to the harness and
attested, but the command exits zero; the Git pre-commit hook remains the
complete enforcement boundary.
"""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from .harness_diagnostics import record_execution_attestation
from .harness_ports import (
    DOMAIN_ROOT_ARG,
    HarnessContext,
    LifecycleBinding,
    LifecycleOutputPort,
)
from .scaffold import MDLLM_ENTRY


@dataclass(frozen=True)
class StepExecution:
    operation: str
    argv: tuple[str, ...]
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True)
class LifecycleExecution:
    moment: str
    steps: tuple[StepExecution, ...]
    text: str
    passed: bool


def _bounded(text: str, limit: int) -> str:
    if limit < 0:
        raise ValueError("output limit must be non-negative")
    if len(text) <= limit:
        return text
    marker = "[earlier lifecycle output truncated]\n"
    if limit <= len(marker):
        return marker[:limit]
    return marker + text[-(limit - len(marker)):]


def _labelled(steps, body: str, limit: int) -> str:
    if limit < 0:
        raise ValueError("output limit must be non-negative")
    summary = "[steps: " + ", ".join(
        f"{item.operation}={item.returncode}" for item in steps) + "]\n"
    if len(summary) >= limit:
        return summary[:limit]
    return summary + _bounded(body, limit - len(summary))


def execute_lifecycle(
        root: Path, binding: LifecycleBinding, *,
        mdllm_entry: Path = MDLLM_ENTRY,
        interpreter: str | None = None,
        timeout_per_step: int | None = None,
        total_timeout: int | None = None,
        output_limit: int = 2200) -> LifecycleExecution:
    """Run every step in declared order and retain bounded, labelled output."""

    if output_limit < 0:
        raise ValueError("output limit must be non-negative")
    if timeout_per_step is not None and timeout_per_step <= 0:
        raise ValueError("step timeout must be positive")
    total = (binding.total_timeout_seconds if total_timeout is None
             else total_timeout)
    if total <= 0:
        raise ValueError("total timeout must be positive")
    if binding.runner_reserve_seconds < 0:
        raise ValueError("runner reserve must be non-negative")
    application_budget = total - binding.runner_reserve_seconds
    if application_budget <= 0:
        raise ValueError("runner reserve must leave application time")
    root = Path(root).resolve()
    python = interpreter or sys.executable
    results: list[StepExecution] = []
    chunks: list[str] = []
    deadline = time.monotonic() + application_budget
    for index, step in enumerate(binding.steps):
        argv = tuple(str(root) if item == DOMAIN_ROOT_ARG else item
                     for item in step.argv)
        command = [python, str(mdllm_entry), step.operation, *argv]
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            result = StepExecution(
                operation=step.operation, argv=argv, returncode=124,
                stderr=f"lifecycle application budget of "
                       f"{application_budget}s exhausted")
            results.append(result)
            chunks.append(f"[{step.operation}: exit {result.returncode}]\n"
                          f"{result.stderr}")
            continue
        later_required = sum(
            float(timeout_per_step or later.timeout_seconds)
            for later in binding.steps[index + 1:])
        available = remaining - later_required
        if available <= 0:
            result = StepExecution(
                operation=step.operation, argv=argv, returncode=124,
                stderr="lifecycle budget reserved for later required steps")
            results.append(result)
            chunks.append(f"[{step.operation}: exit {result.returncode}]\n"
                          f"{result.stderr}")
            continue
        step_timeout = min(
            float(timeout_per_step or step.timeout_seconds), available)
        try:
            run = subprocess.run(
                command, cwd=root, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=step_timeout)
            result = StepExecution(
                operation=step.operation, argv=argv,
                returncode=run.returncode,
                stdout=run.stdout or "", stderr=run.stderr or "")
        except subprocess.TimeoutExpired as exc:
            result = StepExecution(
                operation=step.operation, argv=argv, returncode=124,
                stdout=(exc.stdout.decode("utf-8", "replace")
                        if isinstance(exc.stdout, bytes) else (exc.stdout or "")),
                stderr=(exc.stderr.decode("utf-8", "replace")
                        if isinstance(exc.stderr, bytes) else (exc.stderr or ""))
                       + f"\nstep timed out after {step_timeout:.1f}s")
        except OSError as exc:
            result = StepExecution(
                operation=step.operation, argv=argv, returncode=127,
                stderr=f"{type(exc).__name__}: {exc}")
        results.append(result)
        body = "\n".join(part.rstrip() for part in
                         (result.stdout, result.stderr) if part.rstrip())
        chunks.append(f"[{step.operation}: exit {result.returncode}]"
                      + (f"\n{body}" if body else ""))

    text = _labelled(results, "\n\n".join(chunks), output_limit)
    return LifecycleExecution(
        moment=binding.moment, steps=tuple(results), text=text,
        passed=all(step.returncode == 0 for step in results))


def dispatch_lifecycle_event(root: Path, binding: LifecycleBinding, *,
                             harness: str, definition_hash: str,
                             output_port: LifecycleOutputPort) -> int:
    """Application service: execute, format, and attest one selected event."""
    root = Path(root).resolve()
    adapter = output_port
    if not isinstance(adapter, LifecycleOutputPort):
        print(f"mdllm: harness {harness!r} has no lifecycle output port")
        return 2

    execution = execute_lifecycle(root, binding)
    detail = ", ".join(
        f"{step.operation}={step.returncode}" for step in execution.steps)

    # Successful lifecycle commands are not a successful harness event until
    # their output can be serialized into that harness's documented channel.
    # Format before writing evidence so a broken envelope can never leave a
    # ``passed`` attestation behind.
    format_error: Exception | None = None
    try:
        rendered = adapter.format_lifecycle_output(
            binding.moment, execution.text, execution.passed)
    except Exception as exc:  # adapter output bugs surface without enforcement
        format_error = exc
        rendered = ("MarkdownLLM lifecycle output translation failed: "
                    f"{type(exc).__name__}: {exc}")
        detail += f", output-format={type(exc).__name__}"
    try:
        record_execution_attestation(
            root, harness, binding.moment, definition_hash,
            outcome=("passed" if execution.passed and format_error is None
                     else "failed"),
            source=f"{harness}-project-hook", detail=detail)
    except (OSError, ValueError) as exc:
        # Evidence failure is itself surfaced, but never turns an advisory
        # harness hook into a second enforcement boundary.
        existing_body = (execution.text.split("\n", 1)[1]
                         if execution.text.startswith("[steps: ")
                         and "\n" in execution.text else execution.text)
        execution = LifecycleExecution(
            moment=execution.moment, steps=execution.steps,
            text=_labelled(
                execution.steps, existing_body + "\n\n"
                + f"[attestation unavailable: {exc}]", 2200),
            passed=False)
        try:
            rendered = adapter.format_lifecycle_output(
                binding.moment, execution.text, execution.passed)
        except Exception as exc:  # preserve both advisory failures
            rendered = ("MarkdownLLM lifecycle output translation failed: "
                        f"{type(exc).__name__}: {exc}; {execution.text}")
    if rendered:
        print(rendered)
    return 0


def cmd_harness_event(args) -> int:
    """CLI composition root for the advisory lifecycle application service."""
    from .adapters import get as get_adapter

    adapter = get_adapter(args.harness)
    if not isinstance(adapter, LifecycleOutputPort):
        print(f"mdllm: harness {args.harness!r} has no lifecycle output port")
        return 2
    try:
        binding = HarnessContext(".").binding(args.moment)
    except KeyError:
        print(f"mdllm: unknown lifecycle moment {args.moment!r}")
        return 2
    return dispatch_lifecycle_event(
        Path(args.path), binding, harness=args.harness,
        definition_hash=args.definition_hash, output_port=adapter)
