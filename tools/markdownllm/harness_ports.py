"""DRAFT adapter ports — Phase 2A of vendor-harness-adapter-foundation.

Status: proposed, not consumed. No production code imports this module yet;
scaffold and doctor still carry their inline Claude paths deliberately. The
Codex-owned Phase 2B challenge reviews these signatures against the second
vendor's real lifecycle shape; extraction onto them (and the registry) is
Phase 2C, only after the challenge returns.

Design constraints these types encode (plan: "Narrow adapter ports"):

- **The lifecycle contract is inward-owned and vendor-neutral.** Intents name
  framework acts (estate-sync, session-start, validate) and ordering; they
  never name a vendor event, config key, or file format. How a harness
  guarantees the ordering is its adapter's problem — Claude uses one
  sequential hook group; a harness that fires matching hooks concurrently
  needs a different mechanism for the same intent.
- **Small interfaces, not a harness god-object.** Render produces new-project
  artifacts; Inspect reads existing ones without changing them; capabilities
  are data, so an adapter that cannot honour one is a report, not an
  exception. (The Probe port and the Install/Merge service are deliberately
  NOT drafted here: probing earns its shape from Phase 3's diagnostic work
  and merging from Phase 5's install command — drafting them now would be
  designing from zero consumers.)
- **Inspection is read-only.** An InspectionReport carries what was found —
  including local extensions and content the adapter does not own — and no
  method on any port mutates an existing file. Phase 5 owns mutation.

Vocabulary note: `LIFECYCLE_INTENTS` here must stay equal to the frozen
literal in tools/tests/test_adapter_contract.py — the test asserts it, so a
drift between the draft and the Phase 0 freeze fails loudly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

# The application contract: ordered framework acts per lifecycle moment.
# session-start's ordering is semantic — orientation reads the git log, and
# the log is only whole after the fetch. post-write is advisory feedback; the
# git pre-commit hook remains the complete enforcement boundary and is NOT a
# harness intent (it is git-fs anchored, adapter-independent).
LIFECYCLE_INTENTS: dict[str, tuple[str, ...]] = {
    "session-start": ("estate-sync", "session-start"),
    "post-write": ("validate",),
}


@dataclass(frozen=True)
class HarnessContext:
    """Everything a renderer may know about the domain being projected.
    Mechanical facts only — no domain semantics, no vendor schema."""
    domain_root: Path
    framework_root_rel: str          # POSIX-style relative path to the framework
    platform: str = "any"            # informational; renderers must stay portable
    intents: dict[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(LIFECYCLE_INTENTS))


@dataclass(frozen=True)
class AdapterCapabilities:
    """What one adapter implements. Unsupported is data, never an exception —
    Liskov: every adapter answers the same questions honestly."""
    harness: str                     # e.g. "claude-code" — display identity only
    lifecycle_events: tuple[str, ...] = ()   # intents it can bind mechanically
    shortcuts: bool = False          # deliberate-ritual projections (commands)
    notes: str = ""                  # honest caveats, e.g. ordering mechanism


@dataclass(frozen=True)
class ManagedFragment:
    """The adapter-owned portion found inside an existing config artifact.
    `current` compares against what the SAME adapter's renderer would emit
    now — currency is derived from the renderer, never hand-maintained."""
    path: str                        # repo-relative artifact path
    present: bool
    current: bool | None = None      # None = present but not comparable
    intents_realised: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class InspectionReport:
    """Read-only findings about a domain's existing adapter artifacts.
    Everything the adapter does NOT own is reported, byte-preserved, in
    `operator_owned` — permissions, local hook extensions, unrelated vendor
    settings. Flattening any of it is a defect (requirement 5)."""
    harness: str
    fragments: tuple[ManagedFragment, ...] = ()
    operator_owned: tuple[str, ...] = ()     # descriptions, never rewrites
    extensions: tuple[str, ...] = ()         # local deviations inside managed
    #                                          fragments, e.g. an extra flag on
    #                                          a startup command — reported,
    #                                          never normalised


@runtime_checkable
class RenderPort(Protocol):
    """Produce NEW-project managed artifacts from a context. Returns
    repo-relative path -> exact bytes; writing them is the caller's act.
    Never called against a directory that already has adapter artifacts —
    that is inspection (here) or merge (Phase 5)."""

    def capabilities(self) -> AdapterCapabilities: ...

    def render(self, context: HarnessContext) -> dict[str, bytes]: ...


@runtime_checkable
class InspectPort(Protocol):
    """Parse existing artifacts without changing them. Must succeed (with an
    honest report) on every estate shape: absent, standard, composite,
    locally extended, invalid."""

    def capabilities(self) -> AdapterCapabilities: ...

    def inspect(self, domain_root: Path) -> InspectionReport: ...
