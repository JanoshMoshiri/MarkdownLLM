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
from pathlib import Path

from ..harness_ports import HarnessContext, LifecycleBinding
from ..hook_contract import SH_RESOLVE

HASH_PLACEHOLDER = "<managed-definition-hash>"

# The v1 resolution fragment, frozen as data the day it changed (sprint 2's
# existence-guard commit). Legacy definitions are RECOGNITION data for
# historical installs and must embed the bytes those installs actually
# carry — computing them from the live renderer let them drift silently,
# which the frozen-hash tests caught the first time the renderer moved.
LEGACY_SH_RESOLVE_V1 = (
    Path(__file__).with_name("legacy") / "sh-resolve-v1.txt"
).read_text(encoding="utf-8")

# The v2 fragment: the live one on the day the commit gate landed
# (2026-10-05), frozen so the two-moment projection every seat carried until
# then stays recognisable as `legacy-two-moment-v2` — and refreshable into
# the gated shape — after the live fragment moves again.
LEGACY_SH_RESOLVE_V2 = (
    Path(__file__).with_name("legacy") / "sh-resolve-v2.txt"
).read_text(encoding="utf-8")


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


def gate_envelope(event: str, text: str) -> str:
    """The refusal envelope of a gate delivery: the harness is told to deny
    the tool call and the model reads ``text`` as the reason. Claude Code's
    PreToolUse contract; the one place a project hook is not advisory
    (the-verdict-is-asked-where-the-change-lands-2026-10-05)."""
    return json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "permissionDecision": "deny",
            "permissionDecisionReason": text,
        },
    }, separators=(",", ":"))


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
                        unavailable: str,
                        resolve_fragment: str | None = None,
                        stdin_prefilter: str | None = None) -> str:
    """One sh command entering the neutral ordered runner exactly once.

    Shell form in sh dialect is the portable carrier established by live
    dispatch (2026-08-13). Ordering is the runner's job, not the hook
    schema's: both harnesses launch matching handlers in parallel, so one
    handler is the only construction that can honour an ordered binding.
    Root resolution differs per harness and arrives as ``root_line``.
    ``resolve_fragment`` defaults to the live fragment; legacy definitions
    pass a frozen generation instead.

    ``stdin_prefilter`` is the gate's economy: a hook on the shell tools
    fires on every shell call, so the carrier reads the harness's hook
    input first and exits 0 (allow, silently) unless it matches the sh
    ``case`` pattern — only a commit pays for the interpreter and the scan.
    The input is then piped on to the runner, which decides for real.
    Without it the bytes are exactly the pre-gate carrier's.
    """
    fragment = SH_RESOLVE if resolve_fragment is None else resolve_fragment
    prefilter = ""
    pipe = ""
    if stdin_prefilter is not None:
        prefilter = (
            "MDLLM_HOOK_INPUT=$(cat)\n"
            f'case "$MDLLM_HOOK_INPUT" in {stdin_prefilter}) ;; *) exit 0 ;; esac\n'
        )
        pipe = "printf '%s' \"$MDLLM_HOOK_INPUT\" | "
    return (
        f"{root_line}\n"
        f"{prefilter}"
        f"MDLLM={mdllm_path}\n"
        f"{fragment}\n"
        'if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then\n'
        f"  printf '%s\\n' {shell_single_quote(unavailable)}\n"
        "else\n"
        f'  {pipe}mdllm_python "$MDLLM" harness-event {harness} {moment} '
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
