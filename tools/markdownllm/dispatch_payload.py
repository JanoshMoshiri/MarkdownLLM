"""Compose the dispatch launch text (`mdllm dispatch-payload`).

One responsibility: turn a scope, a stop condition and a launch context into
the exact text a scheduler tick hands a headless session. Nothing else.

**Read-only by construction.** This module opens files and prints; it never
writes, never commits, never touches the network. That is what makes it safe
to put inside a shell substitution on any host:

    <runtime> --oneshot "$(python3 tools/mdllm.py dispatch-payload . \\
        --scope domain/<repo> --stop-condition '...' --launch-context '...')"

**Emit, never point** (`dispatch-host-design-2026-08-29`, grounded in
`emitted-content-is-read-instructed-content-is-economised`): the payload
carries the standing dispatch prompt's *text*, not a path to it. A tick that
handed over a path would be instructing rather than emitting, and instructed
content is economised — measured, not assumed. The integrity trailer exists
for the same reason the kernel emission has one: a channel that truncates
produces sincere believed compliance unless the cut is detectable in-context.

**The prompt's declared inputs are the contract.** The composer reads the
`inputs:` block of `templates/prompts/dispatch-loop.md` and refuses to launch
unless it can supply every declared name. So a future input added to the
prompt cannot silently go unsupplied at launch: the composer fails loudly
instead of emitting a payload that under-specifies the run.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from .model import parse_frontmatter

# The standing dispatch prompt — the inside half of the dispatcher, versioned
# where every other operative surface lives. Referenced by path because
# templates/ sits outside the corpus id-space by design (dispatch-design-2026-08,
# decision 2); emitted by content because a path is not a contract.
DISPATCH_PROMPT_RELATIVE = "templates/prompts/dispatch-loop.md"

# Inputs this composer knows how to supply, mapped to the prompt's declared
# `inputs:` names. A declared input outside this set is a refusal, not a
# silently missing value.
ESTATE_ROOT_INPUT = "estate-root"
SCOPE_INPUT = "scope"
STOP_CONDITION_INPUT = "stop-condition"
LAUNCH_CONTEXT_INPUT = "launch-context"

# Only `scope` has a default (the estate-wide walk). The other three are
# launch facts: a run without them is invalid by the prompt's own rule, and
# composing a payload that pretends otherwise would launder the invalidity.
OPTIONAL_INPUTS = frozenset({SCOPE_INPUT})

_TRAILER = (
    "[dispatch prompt emitted whole — {lines} lines, sha256 {digest}. This "
    "trailer is the integrity mark: if it is missing, or the prompt above "
    "ends mid-sentence, the channel cut the emission — do no work, write the "
    "digest saying the launch text arrived truncated, and end.]")


class DispatchPayloadRefused(Exception):
    """A launch that must not be composed, with the reason a human can act on."""


@dataclass(frozen=True)
class DispatchLaunch:
    """The resolved launch facts — the prompt's declared inputs, filled."""

    estate_root: Path
    scope: tuple[str, ...]
    stop_condition: str
    launch_context: str

    def scope_line(self) -> str:
        if not self.scope:
            return ("the whole estate — root + domain(s)/* as the estate-sync "
                    "walk finds them (the default walk)")
        return ", ".join(f"`{item}`" for item in self.scope)


def prompt_source(root: Path) -> Path:
    return root / Path(DISPATCH_PROMPT_RELATIVE)


def read_dispatch_prompt(root: Path) -> tuple[dict, str]:
    """The standing prompt's frontmatter and its whole text, verbatim.

    The text is emitted frontmatter and all: `dispatch_guards` is operative
    content (depth limit, serialization, stop-condition requirement, the
    dead-man), not metadata about the prompt.
    """
    source = prompt_source(root)
    if not source.is_file():
        raise DispatchPayloadRefused(
            f"the standing dispatch prompt is missing at "
            f"`{DISPATCH_PROMPT_RELATIVE}` (looked under {root}) — there is "
            f"no dispatch procedure to launch, and a payload composed without "
            f"one would be a session with a stop condition and no instructions")
    text = source.read_text(encoding="utf-8")
    meta, _, _ = parse_frontmatter(text)
    return (meta or {}), text


def declared_input_names(meta: dict) -> tuple[str, ...]:
    """The `inputs:` names the prompt declares, in declaration order."""
    declared = meta.get("inputs")
    if not isinstance(declared, list):
        return ()
    names = []
    for entry in declared:
        if isinstance(entry, dict) and isinstance(entry.get("name"), str):
            names.append(entry["name"])
    return tuple(names)


def resolve_scope(root: Path, requested: list[str] | None) -> tuple[str, ...]:
    """Validate each requested repo and render it relative to the estate root.

    A scope naming a directory that is not a repository is a launch error and
    not a run-time surprise: the tick is dumb, so the composition surface is
    where a mistyped pilot path has to fail.
    """
    if not requested:
        return ()
    resolved: list[str] = []
    for raw in requested:
        candidate = Path(raw)
        target = candidate if candidate.is_absolute() else root / candidate
        if not target.is_dir():
            raise DispatchPayloadRefused(
                f"scope `{raw}` is not a directory under {root} — a dispatch "
                f"run works repositories, and a scope it cannot find is a "
                f"launch typo, not a run to attempt")
        if not (target / ".git").exists():
            raise DispatchPayloadRefused(
                f"scope `{raw}` is not a git repository (no .git) — the "
                f"dispatch loop serializes per repo and commits per repo; a "
                f"directory that is not one has no floor and no record")
        try:
            rendered = target.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            rendered = target.resolve().as_posix()
        resolved.append(rendered or ".")
    return tuple(resolved)


def build_launch(root: Path, *, scope: list[str] | None,
                 stop_condition: str | None,
                 launch_context: str | None) -> DispatchLaunch:
    """Resolve the launch facts, refusing an invalid launch at composition.

    The prompt's own rule: a launch without a stop condition is invalid and
    the session must halt at the digest. Composing that payload anyway would
    spend a whole run to discover what is knowable here — and
    `an-agent-in-a-loop-optimises-the-loop-not-the-goal` makes the exogenous
    stop non-negotiable rather than advisory.
    """
    if not root.is_dir():
        raise DispatchPayloadRefused(f"estate root {root} is not a directory")
    missing = [name for name, value in (
        (STOP_CONDITION_INPUT, stop_condition),
        (LAUNCH_CONTEXT_INPUT, launch_context))
        if not (value or "").strip()]
    if missing:
        raise DispatchPayloadRefused(
            "refusing to compose a payload without "
            + " and ".join(f"`--{name}`" for name in missing)
            + " — the dispatch prompt declares both as required at launch, "
              "and a run given neither a stop nor an attribution is invalid "
              "before it starts")
    return DispatchLaunch(
        estate_root=root,
        scope=resolve_scope(root, scope),
        stop_condition=(stop_condition or "").strip(),
        launch_context=(launch_context or "").strip(),
    )


def _integrity(text: str) -> tuple[int, str]:
    normal = text.replace("\r\n", "\n")
    lines = normal.count("\n") + (0 if normal.endswith("\n") else 1)
    return lines, hashlib.sha256(normal.encode("utf-8")).hexdigest()[:12]


def compose_payload(launch: DispatchLaunch, prompt_meta: dict,
                    prompt_text: str) -> str:
    """The launch text: resolved inputs, then the standing prompt, then the mark."""
    declared = declared_input_names(prompt_meta)
    supplied = {
        ESTATE_ROOT_INPUT: launch.estate_root.as_posix(),
        SCOPE_INPUT: launch.scope_line(),
        STOP_CONDITION_INPUT: launch.stop_condition,
        LAUNCH_CONTEXT_INPUT: launch.launch_context,
    }
    unsupplied = [name for name in declared
                  if name not in supplied and name not in OPTIONAL_INPUTS]
    if unsupplied:
        raise DispatchPayloadRefused(
            "the standing dispatch prompt declares input(s) this composer "
            "cannot supply: " + ", ".join(f"`{n}`" for n in unsupplied)
            + " — the prompt and the launch surface have diverged; teach "
              "`dispatch-payload` the new input rather than launching a run "
              "that silently lacks it")

    lines, digest = _integrity(prompt_text)
    out = [
        "# Dispatch launch (composed by `mdllm dispatch-payload`)",
        "",
        "You are a dispatch session, launched by a scheduler tick rather than "
        "by a human. Everything you need is in this message: the resolved "
        "launch inputs first, then the standing dispatch prompt in full. "
        "Nothing below is a pointer to be read later.",
        "",
        "## Launch inputs (resolved)",
        "",
        f"- **{ESTATE_ROOT_INPUT}**: `{supplied[ESTATE_ROOT_INPUT]}`",
        f"- **{SCOPE_INPUT}**: {supplied[SCOPE_INPUT]}",
        f"- **{STOP_CONDITION_INPUT}**: {supplied[STOP_CONDITION_INPUT]}",
        f"- **{LAUNCH_CONTEXT_INPUT}**: {supplied[LAUNCH_CONTEXT_INPUT]}",
        "",
    ]
    if launch.scope:
        out += ["This run is **scoped**: work only the repository/repositories "
                "named above. Everything outside that scope — including the "
                "framework root — is out of bounds for this run, even if its "
                "floor reports work due.", ""]
    out += [
        f"## The standing dispatch prompt — `{DISPATCH_PROMPT_RELATIVE}` (emitted)",
        "",
        prompt_text.rstrip("\n"),
        "",
        _TRAILER.format(lines=lines, digest=digest),
        "",
    ]
    return "\n".join(out)


def cmd_dispatch_payload(args) -> int:
    root = Path(args.path).resolve()
    try:
        launch = build_launch(
            root,
            scope=getattr(args, "scope", None),
            stop_condition=getattr(args, "stop_condition", None),
            launch_context=getattr(args, "launch_context", None))
        meta, text = read_dispatch_prompt(root)
        payload = compose_payload(launch, meta, text)
    except DispatchPayloadRefused as refusal:
        print(f"mdllm: dispatch-payload refused this launch — {refusal}",
              file=sys.stderr)
        return 2
    print(payload)
    return 0
