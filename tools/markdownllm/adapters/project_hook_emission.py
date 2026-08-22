"""Shared emission shape for the project-bound lifecycle adapters.

Claude Code and Codex converged on one project-hook emission shape: a POSIX
command entering the neutral ordered runner exactly once, a JSON
additional-context envelope, a definition hash computed over the managed
group with a stable placeholder, and quoting that keeps every
context-supplied byte literal. That convergence is contractual — this module
owns the shape as plain functions taking explicit parameters; each adapter
keeps its own vocabulary (event names, matchers, config paths, Windows
carriers, legacy definitions). Composition, not a base class: a hierarchy
would couple the adapters' independent evolution
(floor-structure-residue item 2, landed sprint 2).

Byte-compatibility note: the functions here reproduce the exact bytes both
adapters emitted before the collapse; the golden fixtures are the proof.
"""

from __future__ import annotations

import json

from ..harness_ports import HarnessContext, LifecycleBinding
from ..hook_contract import SH_RESOLVE

HASH_PLACEHOLDER = "<managed-definition-hash>"


def shell_single_quote(value: str) -> str:
    """Single-quote one literal for the POSIX hook command.

    Every byte the render context supplies stays literal: `$`, backticks,
    quotes and command substitutions inside a legal path must never become
    shell syntax.
    """
    return "'" + value.replace("'", "'\"'\"'") + "'"


def ps_quote(value: str) -> str:
    """Single-quote one literal for an inline PowerShell program."""
    return "'" + value.replace("'", "''") + "'"


def mdllm_posix_path(context: HarnessContext) -> str:
    """The mdllm.py path expression: `$ROOT` expands, context bytes stay
    literal."""
    rel = context.framework_root_rel.rstrip("/") or "."
    return '"$ROOT/"' + shell_single_quote(f"{rel}/tools/mdllm.py")


def unavailable_text(moment: str) -> str:
    """The shared no-floor message for the POSIX carrier."""
    return (f"MarkdownLLM {moment} could not run: no floor-capable Python "
            "or mdllm.py was found.")


def lifecycle_envelope(moment: str, text: str, passed: bool,
                       event: str) -> str:
    """The additional-context JSON envelope both harnesses consume.

    A passing post-write is quiet: silence is the correct feedback when
    nothing is wrong. Everything else is model-visible context — never a
    blocking decision; the Git pre-commit hook is the enforcement boundary
    (`surface-and-continue`).
    """
    if moment == "post-write" and passed:
        return ""
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": text,
        },
    }, separators=(",", ":"))


def posix_event_command(*, root_line: str, harness: str, moment: str,
                        definition_hash: str, mdllm_path: str,
                        unavailable: str) -> str:
    """One sh command entering the neutral ordered runner exactly once.

    Shell form in sh dialect is the portable carrier established by live
    dispatch (2026-08-13). Ordering is the runner's job, not the hook
    schema's: both harnesses launch matching handlers in parallel, so one
    handler is the only construction that can honour an ordered binding.
    Root resolution differs per harness and arrives as ``root_line``.
    """
    return (
        f"{root_line}\n"
        f"MDLLM={mdllm_path}\n"
        f"{SH_RESOLVE}\n"
        'if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then\n'
        f"  printf '%s\\n' {shell_single_quote(unavailable)}\n"
        "else\n"
        f'  mdllm_python "$MDLLM" harness-event {harness} {moment} '
        f'"$ROOT" {shell_single_quote(definition_hash)}\n'
        "fi\n"
        "exit 0"
    )


def binding_hash_payload(binding: LifecycleBinding, *,
                         include_output: bool = True) -> str:
    """The canonical binding payload both definition hashes are computed
    over. The literal attestation hash is excluded from its own input by the
    caller passing ``HASH_PLACEHOLDER`` into the handler it hashes."""
    payload = {
        "moment": binding.moment,
        "delivery": binding.delivery,
        "failure": binding.failure,
        "steps": [{
            "operation": step.operation,
            "argv": list(step.argv),
            "protected_seconds": step.protected_seconds,
            **({"protected_characters": step.protected_characters}
               if include_output else {}),
        } for step in binding.steps],
        "total_timeout_seconds": binding.total_timeout_seconds,
        "runner_reserve_seconds": binding.runner_reserve_seconds,
    }
    if include_output:
        payload.update({
            "output_limit_characters": binding.output_limit_characters,
            "output_reserve_characters": binding.output_reserve_characters,
        })
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
