"""Harness adapter registry — Phase 2C of vendor-harness-adapter-foundation.

The one aggregation point where vendor adapters are known by name. Neutral
modules (scaffold, doctor) call `get()`/`default_harness()` and speak to the
ports; they never import a vendor module or branch on a vendor's config
shape. A future harness adds a registration here plus its own module, tests,
and docs — not another conditional in scaffold or doctor control flow
(Open/Closed, plan requirement: "adding a third harness requires a new
adapter, tests, and docs").

There is no scaffold default (Phase 8, ruled 2026-09-15 —
`scaffold-harness-is-an-explicit-selection-2026-09-15`): a birth names its
harness, is asked at a keyboard, or is refused with the list. `DEFAULT_HARNESS`
survives only as doctor's subject when no project adapter is present —
which harness to *report on*, never which to render.
"""

from __future__ import annotations

from .claude_code import CLAUDE_CODE
from .codex import CODEX
from .cowork import COWORK
from .perplexity import PERPLEXITY

DEFAULT_HARNESS = "claude-code"

# CLI spelling is an interface concern, not another registry entry.  Keep one
# canonical adapter identity so diagnostics, attestations, and install plans
# cannot split between ``claude`` and ``claude-code``.
ALIASES = {"claude": "claude-code"}


class HarnessSelectionRequired(LookupError):
    """No harness was named where one is required. Carries the registered
    choices so the edge that catches it can ask, or refuse with the list."""

    def __init__(self, choices: tuple[str, ...]):
        self.choices = choices
        super().__init__(
            "no harness selected; choose one of: " + ", ".join(choices))

_REGISTRY = {
    CLAUDE_CODE.name: CLAUDE_CODE,
    CODEX.name: CODEX,
    COWORK.name: COWORK,
    PERPLEXITY.name: PERPLEXITY,
}


def get(name: str):
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"no adapter registered for harness {name!r}; "
            f"known: {', '.join(sorted(_REGISTRY))}") from None


def names() -> tuple[str, ...]:
    return tuple(sorted(_REGISTRY))


def canonical_name(name: str) -> str:
    return ALIASES.get(name, name)


def selection(value: str | None) -> tuple[str, ...]:
    """Resolve a CLI selection without embedding vendor branches in callers.

    No value is not a choice: it raises ``HarnessSelectionRequired`` for the
    edge to ask or refuse — nothing renders until a harness is named. ``all``
    is deterministic; ``none`` is an honest empty projection. Unknown names
    fail before a caller creates or mutates anything.
    """
    if value is None:
        raise HarnessSelectionRequired(selection_choices())
    if value == "none":
        return ()
    if value == "all":
        return names()
    name = canonical_name(value)
    get(name)  # validate now, before any service writes
    return (name,)


def selection_choices() -> tuple[str, ...]:
    return tuple(sorted(set(names()) | set(ALIASES) | {"all", "none"}))


def register(adapter) -> None:
    """Add an adapter to the registry. The entry point for future harnesses —
    and for the architecture fitness gate's port-only fake, which proves the
    shared services never call beyond the declared contracts."""
    _REGISTRY[adapter.name] = adapter


def unregister(name: str) -> None:
    """Remove a registered adapter (test teardown; never used in production
    flow — an installed harness is removed by not registering it)."""
    _REGISTRY.pop(name, None)
