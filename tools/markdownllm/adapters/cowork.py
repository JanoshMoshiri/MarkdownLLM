"""The Cowork adapter — Phase 0 of the ``cowork-adapter`` plan.

The third registered harness, and the first of a different class. Claude
Code and Codex are project-level and render-time bound: artifacts rendered
into the domain repo, currency checked against the same renderer at install
time. Cowork is estate-level and run-time bound: an account-level plugin
bundle assembles the workspace (cloning the framework and the selected
domains) *after* the session has started, so there is never a per-domain
artifact to render, inspect, or hash. ``render()`` returning no artifacts
is that fact stated through the port — not a stub awaiting content.

What this adapter truthfully claims today (Phase 0):

- **session-start is bound** — the bundle performs the ordered lifecycle
  mechanically after assembly, for the session that invoked it. Until the
  bundle build (plan Phase 3) supplies a definition fingerprint, execution
  reports ``untested``: installation is not activation, and a static probe
  is not an event.
- **post-write feedback is NOT bound** — nothing in Cowork fires validation
  on individual writes; the git pre-commit hook is the first check that
  sees them. Declared so doctor can say it rather than imply otherwise.
- **Trust is unknown** — Cowork exposes no stable project-trust surface.

The bundle itself (skill, bootstrap, publication guard, session contract)
is rendered by the Phase 3 build from framework-owned templates; run-time
currency — the installed bundle's hash against the freshly cloned
framework's expectation — lands there too, alongside the ``ProbePort``
fingerprints that let a real bootstrap attest execution. This module is
the single place Cowork vocabulary may appear in code (architecture
fitness gate).
"""

from __future__ import annotations

from pathlib import Path

from ..harness_ports import (
    AdapterCapabilities, HarnessContext, InspectionReport,
)


class CoworkAdapter:
    """Capabilities plus honest emptiness: no per-domain managed artifacts."""

    name = "cowork"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start",),
            notes=(
                "binds at run time through the account-level bundle, not "
                "through project configuration; no post-write feedback — "
                "writes meet the floor at commit time"),
        )

    # -- RenderPort --------------------------------------------------------
    def render(self, context: HarnessContext) -> dict[str, bytes]:
        """No project artifacts, for any context — the binding lives in the
        bundle. Diagnostics read this as configuration: not-applicable."""
        return {}

    # -- InspectPort -------------------------------------------------------
    def inspect(self, domain_root: Path,
                context: HarnessContext) -> InspectionReport:
        """Nothing of Cowork's lives in a domain repo; report exactly that.
        No fragments means doctor's presence detection can never claim a
        Cowork installation from repo contents — there is none to find."""
        return InspectionReport(harness=self.name)

    # -- ScaffoldNoticePort ------------------------------------------------
    def scaffold_guidance(self) -> str:
        return ("Cowork: no per-domain artifact — sessions bind through the "
                "account-level bundle at run time (plan: cowork-adapter)")


COWORK = CoworkAdapter()
