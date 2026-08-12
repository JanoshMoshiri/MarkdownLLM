"""Adapter ports — the inward application contract of
vendor-harness-adapter-foundation.

Status: accepted and consumed. Drafted in Phase 2A, challenged and corrected
against the official Codex lifecycle shape in the Codex-owned Phase 2B
(evidence/codex-port-challenge-2026-08-11.md), and consumed by the adapter
registry (markdownllm/adapters/) since the Phase 2C extraction. Scaffold and
doctor speak to these ports; vendor config shapes live only in the adapters.

Design constraints these types encode (plan: "Narrow adapter ports"):

- **The lifecycle contract is inward-owned and vendor-neutral.** Intents name
  framework acts (estate-sync, session-start, validate) and ordering; they
  never name a vendor event, config key, or file format. How a harness
  guarantees the ordering is its adapter's problem. A handler array is not an
  ordering primitive: adapters for concurrently launched handlers must enter
  the neutral ordered runner through one managed handler.
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
from types import MappingProxyType
from typing import Literal, Mapping, Protocol, runtime_checkable

DOMAIN_ROOT_ARG = "{domain_root}"


@dataclass(frozen=True)
class LifecycleStep:
    """One deterministic-floor invocation in an ordered lifecycle binding.

    ``argv`` is inward-owned command data, not a shell string.  Adapters map
    ``DOMAIN_ROOT_ARG`` to their stable repository-root expression and encode
    the result for their own shell/config format.
    """

    operation: str
    argv: tuple[str, ...] = (DOMAIN_ROOT_ARG,)


@dataclass(frozen=True)
class LifecycleBinding:
    """Vendor-neutral policy for one lifecycle moment.

    Tuple order is authoritative. ``delivery`` tells an adapter whether the
    result belongs in startup context or post-action feedback. ``failure`` is
    deliberately non-enforcing: harness hooks surface failures, while the Git
    pre-commit hook remains the complete enforcement boundary.
    """

    moment: str
    steps: tuple[LifecycleStep, ...]
    delivery: Literal["context", "feedback"]
    failure: Literal["surface-and-continue"] = "surface-and-continue"


# The application contract: complete ordered invocations per lifecycle moment.
# session-start's ordering is semantic — orientation reads the git log, and
# the log is only whole after the fetch. post-write is advisory feedback; the
# git pre-commit hook remains the complete enforcement boundary and is NOT a
# harness intent (it is git-fs anchored, adapter-independent).
LIFECYCLE_BINDINGS: tuple[LifecycleBinding, ...] = (
    LifecycleBinding(
        moment="session-start",
        steps=(LifecycleStep("estate-sync"), LifecycleStep("session-start")),
        delivery="context",
    ),
    LifecycleBinding(
        moment="post-write",
        steps=(LifecycleStep("validate", (DOMAIN_ROOT_ARG, "--quiet")),),
        delivery="feedback",
    ),
)

# Phase 0 froze this compact view. Keep it as a derived, immutable compatibility
# surface; the bindings above own arguments and delivery semantics.
LIFECYCLE_INTENTS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    binding.moment: tuple(step.operation for step in binding.steps)
    for binding in LIFECYCLE_BINDINGS
})


@dataclass(frozen=True)
class HarnessContext:
    """Pure mechanical input to a projection — no host or vendor state.

    ``framework_root_rel`` is POSIX-style and relative to the domain Git root.
    A renderer must emit every target-platform variant it supports regardless
    of the host doing the rendering; absolute paths and host inspection do not
    belong in this context.
    """

    framework_root_rel: str
    bindings: tuple[LifecycleBinding, ...] = LIFECYCLE_BINDINGS

    def binding(self, moment: str) -> LifecycleBinding:
        for item in self.bindings:
            if item.moment == moment:
                return item
        raise KeyError(moment)


@dataclass(frozen=True)
class AdapterCapabilities:
    """What one adapter implements. Unsupported is data, never an exception —
    Liskov: every adapter answers the same questions honestly."""
    harness: str                     # e.g. "claude-code" — display identity only
    lifecycle_moments: tuple[str, ...] = ()  # inward moments it binds mechanically
    notes: str = ""                  # display only; never a diagnostic status


@dataclass(frozen=True)
class ManagedFragment:
    """The adapter-owned portion found inside an existing config artifact.
    `current` compares against what the SAME adapter's renderer would emit
    now — currency is derived from the renderer, never hand-maintained."""
    path: str                        # repo-relative artifact path
    present: bool                    # managed fragment is present
    artifact_present: bool = True    # containing config artifact exists
    readable: bool | None = None     # None when artifact is absent
    valid: bool | None = None        # None when absent or unreadable
    current: bool | None = None      # None when fragment absent/unreadable/invalid
    intents_realised: dict[str, tuple[str, ...]] = field(default_factory=dict)
    issues: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.artifact_present and (self.present or any(
                value is not None for value in
                (self.readable, self.valid, self.current))):
            raise ValueError("an absent artifact has no fragment or file facts")
        if not self.present and self.current is not None:
            raise ValueError("an absent managed fragment has no currency")
        if self.readable is False and any(
                value is not None for value in (self.valid, self.current)):
            raise ValueError("an unreadable fragment has no validity/currency")
        if self.valid is False and self.current is not None:
            raise ValueError("an invalid fragment has no currency")


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
    findings: tuple[str, ...] = ()           # cross-fragment ambiguity/warnings


@runtime_checkable
class RenderPort(Protocol):
    """Purely project managed artifacts from a context.

    Returns repo-relative path -> exact bytes; it never reads or writes the
    filesystem. The same projection is therefore safe to call for a new
    project or to derive desired bytes for currency/merge comparison. Writing
    or merging them is a separate caller's act.
    """

    def capabilities(self) -> AdapterCapabilities: ...

    def render(self, context: HarnessContext) -> dict[str, bytes]: ...


@runtime_checkable
class InspectPort(Protocol):
    """Parse existing artifacts without changing them. Must succeed (with an
    honest report) on every expected estate shape: absent, unreadable,
    malformed, schema-invalid, standard, composite, and locally extended.
    ``context`` lets inspection derive currency from the same renderer instead
    of maintaining a second expected fragment."""

    def capabilities(self) -> AdapterCapabilities: ...

    def inspect(self, domain_root: Path,
                context: HarnessContext) -> InspectionReport: ...


# --------------------------------------------------------------------------
# Service-facing ports (v1.6 return item 1). Every method a shared service
# calls on an adapter is declared here — an adapter that implements only
# Render/Inspect must pass through scaffold and doctor untouched, never crash
# them. Services test each port with isinstance and skip what an adapter does
# not offer; absence is a valid answer, not an error (Interface Segregation).


@runtime_checkable
class ShortcutPort(Protocol):
    """Deliberate-ritual shortcut projections — inert files the operator
    invokes by hand, a separate concern from lifecycle hooks. The adapter
    owns only WHERE each template belongs; the caller owns placeholder
    substitution and writing."""

    def shortcut_sources(self, templates_root: Path) -> Mapping[str, Path]: ...


@runtime_checkable
class ScaffoldNoticePort(Protocol):
    """One adapter-owned line for scaffold's completion output. Display data
    only — never consulted for any decision."""

    def scaffold_guidance(self) -> str: ...


@dataclass(frozen=True)
class DiagnosticPresentation:
    """Adapter-supplied display strings for the shared doctor advisory —
    data, not behaviour. The install decision, extension surfacing, and
    status glyphs are doctor's neutral logic; only the vendor wording lives
    in the adapter. Pinned until Phase 3 settles the diagnostic vocabulary."""
    installed: str
    absent: str


@runtime_checkable
class DiagnosticPresentationPort(Protocol):
    def diagnostic_presentation(self) -> DiagnosticPresentation: ...


@runtime_checkable
class LifecycleOutputPort(Protocol):
    """Translate one neutral lifecycle execution into harness stdout.

    The application service owns step execution and evidence; the adapter
    owns only the event-specific output envelope.  In particular, a harness
    whose post-action stdout is ignored can serialize its documented feedback
    channel without teaching the neutral runner that vendor schema.
    """

    def format_lifecycle_output(
            self, moment: str, text: str, passed: bool) -> str: ...
