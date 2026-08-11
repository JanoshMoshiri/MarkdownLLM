"""Harness adapter registry — Phase 2C of vendor-harness-adapter-foundation.

The one aggregation point where vendor adapters are known by name. Neutral
modules (scaffold, doctor) call `get()`/`default_harness()` and speak to the
ports; they never import a vendor module or branch on a vendor's config
shape. A future harness adds a registration here plus its own module, tests,
and docs — not another conditional in scaffold or doctor control flow
(Open/Closed, plan requirement: "adding a third harness requires a new
adapter, tests, and docs").

The scaffold default remains Claude for this compatibility release; changing
it is a Phase 8 product decision, not architecture cleanup.
"""

from __future__ import annotations

from .claude_code import CLAUDE_CODE
from .codex import CODEX

DEFAULT_HARNESS = "claude-code"

# CLI spelling is an interface concern, not another registry entry.  Keep one
# canonical adapter identity so diagnostics, attestations, and install plans
# cannot split between ``claude`` and ``claude-code``.
ALIASES = {"claude": "claude-code"}

_REGISTRY = {
    CLAUDE_CODE.name: CLAUDE_CODE,
    CODEX.name: CODEX,
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

    No value preserves the compatibility default. ``all`` is deterministic;
    ``none`` is an honest empty projection. Unknown names fail before a caller
    creates or mutates anything.
    """
    if value is None:
        value = DEFAULT_HARNESS
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
