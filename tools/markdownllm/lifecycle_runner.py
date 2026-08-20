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

import os
import re
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


_TRUNCATION_MARKER = "\n[truncated]\n"


def _bounded(text: str, limit: int) -> str:
    """Bound one indivisible section while retaining both of its edges."""
    if limit < 0:
        raise ValueError("output limit must be non-negative")
    if len(text) <= limit:
        return text
    if limit <= len(_TRUNCATION_MARKER):
        return _TRUNCATION_MARKER[:limit]
    retained = limit - len(_TRUNCATION_MARKER)
    head = (retained + 1) // 2
    tail = retained - head
    return text[:head] + _TRUNCATION_MARKER + (text[-tail:] if tail else "")


def _structural_sections(text: str) -> tuple[str, ...]:
    """Split Markdown-like command output without understanding its meaning.

    Headings, blank-delimited paragraphs, labelled runner blocks, and
    top-level emphasized list headings are structural boundaries.  Nested list
    items remain attached to their heading.  Plain consecutive list items
    remain one section, so an estate listing is represented as a list rather
    than fourteen unrelated semantic priorities.
    """
    sections: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            sections.append("\n".join(current))
            current.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        top_level = line == line.lstrip()
        structural_start = top_level and (
            line.startswith("#")
            or line.startswith("[")
            or bool(re.match(r"^[-*+] \*\*[^*]+\*\*", line))
        )
        if structural_start:
            flush()
        current.append(line)
    flush()
    return tuple(sections) or ((text,) if text else ())


def _fair_limits(lengths: tuple[int, ...], available: int) -> tuple[int, ...]:
    """Share a strict character budget without assigning semantic priority."""
    if available <= 0 or not lengths:
        return tuple(0 for _ in lengths)
    limits = [0] * len(lengths)
    active = set(range(len(lengths)))
    remaining = available
    while active and remaining:
        share, extra = divmod(remaining, len(active))
        if share == 0:
            for index in sorted(active)[:extra]:
                limits[index] += 1
            break
        consumed = 0
        completed: list[int] = []
        for position, index in enumerate(sorted(active)):
            grant = share + (1 if position < extra else 0)
            need = lengths[index] - limits[index]
            used = min(grant, need)
            limits[index] += used
            consumed += used
            if limits[index] >= lengths[index]:
                completed.append(index)
        remaining -= consumed
        active.difference_update(completed)
        if consumed == 0:
            break
    return tuple(limits)


def _bounded_structurally(text: str, limit: int) -> str:
    """Keep every structural section represented inside one strict bound."""
    if limit < 0:
        raise ValueError("output limit must be non-negative")
    if len(text) <= limit:
        return text
    sections = _structural_sections(text)
    if len(sections) <= 1:
        return _bounded(text, limit)
    separator_size = 2 * (len(sections) - 1)
    if separator_size >= limit:
        return _bounded(text, limit)
    limits = _fair_limits(
        tuple(len(section) for section in sections), limit - separator_size)
    return "\n\n".join(
        _bounded(section, section_limit)
        for section, section_limit in zip(sections, limits))


def _scaled_protections(protections: tuple[int, ...], available: int) \
        -> tuple[int, ...]:
    total = sum(protections)
    if total <= available:
        return protections
    if available <= 0:
        return tuple(0 for _ in protections)
    raw = [available * value / total for value in protections]
    scaled = [int(value) for value in raw]
    for index in sorted(
            range(len(raw)), key=lambda item: raw[item] - scaled[item],
            reverse=True)[:available - sum(scaled)]:
        scaled[index] += 1
    return tuple(scaled)


def _labelled(steps, bodies: tuple[str, ...] | str, limit: int,
              binding: LifecycleBinding | None = None) -> str:
    """Render bounded labelled output, reserving every declared later share."""
    if limit < 0:
        raise ValueError("output limit must be non-negative")
    summary = "[steps: " + ", ".join(
        f"{item.operation}={item.returncode}" for item in steps) + "]\n"
    if len(summary) >= limit:
        return summary[:limit]
    if isinstance(bodies, str) or binding is None:
        return summary + _bounded_structurally(
            bodies if isinstance(bodies, str) else "\n\n".join(bodies),
            limit - len(summary))

    separator_size = 2 * max(0, len(bodies) - 1)
    available = max(0, limit - len(summary) - separator_size)
    declared_application = (binding.output_limit_characters
                            - binding.output_reserve_characters)
    # A diagnostic/test override scales the declared application share rather
    # than deleting the runner's label reserve. Production uses the exact
    # binding limit, leaving the declared reserve for summary, labels, and
    # truncation markers.
    scaled_application = (
        declared_application * limit // binding.output_limit_characters)
    available = min(available, scaled_application)
    protections = _scaled_protections(
        tuple(step.protected_characters for step in binding.steps), available)
    rendered: list[str] = []
    remaining = available
    for index, (result, body) in enumerate(zip(steps, bodies)):
        later_required = sum(protections[index + 1:])
        step_limit = max(0, remaining - later_required)
        label = f"[{result.operation}: exit {result.returncode}]"
        if step_limit <= len(label):
            block = label[:step_limit]
        elif body:
            block = label + "\n" + _bounded_structurally(
                body, step_limit - len(label) - 1)
        else:
            block = label
        rendered.append(block)
        remaining -= len(block)
    return summary + "\n\n".join(rendered)


def execute_lifecycle(
        root: Path, binding: LifecycleBinding, *,
        mdllm_entry: Path = MDLLM_ENTRY,
        interpreter: str | None = None,
        timeout_per_step: int | None = None,
        total_timeout: int | None = None,
        output_limit: int | None = None) -> LifecycleExecution:
    """Run every step in declared order and retain bounded, labelled output."""

    output_limit = (binding.output_limit_characters
                    if output_limit is None else output_limit)
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
            chunks.append(result.stderr)
            continue
        later_required = sum(
            float(timeout_per_step or later.protected_seconds)
            for later in binding.steps[index + 1:])
        available = remaining - later_required
        if available <= 0:
            result = StepExecution(
                operation=step.operation, argv=argv, returncode=124,
                stderr="lifecycle budget reserved for later required steps")
            results.append(result)
            chunks.append(result.stderr)
            continue
        # Default execution lets the current step inherit budget unused by
        # earlier steps.  Only later steps' protected allocations are held
        # back.  ``timeout_per_step`` remains an explicit diagnostic/test cap,
        # not the production allocation policy.
        step_timeout = (min(float(timeout_per_step), available)
                        if timeout_per_step is not None else available)
        try:
            # The channel marker: steps invoked through the runner emit into
            # a bounded hook channel, and channel-aware emitters (session-
            # start's kernel emission) must defer loudly rather than let the
            # structural bound cut their content — a partial kernel with
            # elision marked still recreates the believed-loaded failure
            # (session-start-hardening Phase 2). Environment, not argv: the
            # rendered hook configs and their definition hashes stay
            # byte-identical across the estate.
            run = subprocess.run(
                command, cwd=root, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=step_timeout,
                env={**os.environ,
                     "MDLLM_LIFECYCLE_CHANNEL": binding.moment})
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
        chunks.append(body)

    text = _labelled(
        results, tuple(chunks), output_limit, binding=binding)
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
