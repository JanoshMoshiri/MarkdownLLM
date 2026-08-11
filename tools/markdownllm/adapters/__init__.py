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

DEFAULT_HARNESS = "claude-code"

_REGISTRY = {
    CLAUDE_CODE.name: CLAUDE_CODE,
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
