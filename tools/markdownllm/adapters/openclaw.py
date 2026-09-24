"""OpenClaw lifecycle output adapter.

OpenClaw is runtime-bound: its native plugin resolves the configured agent
workspace when a turn begins, then enters MarkdownLLM's neutral lifecycle
runner. No per-domain OpenClaw artifact belongs in the domain repository.

The native plugin owns hook registration and additive prompt delivery. This
adapter owns only the MarkdownLLM-side capabilities and output envelope.
"""

from __future__ import annotations

from pathlib import Path

from ..harness_ports import (
    AdapterCapabilities,
    HarnessContext,
    InspectionReport,
)

_OPEN = '<markdownllm-session-start outcome="{outcome}">'
_CLOSE = "</markdownllm-session-start>"


class OpenClawAdapter:
    """Run-time-bound OpenClaw projection with no project artifact."""

    name = "openclaw"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start",),
            notes=(
                "binds at prompt-build time through the native OpenClaw "
                "plugin; OpenClaw owns sessions; no post-write hook"),
        )

    def render(self, context: HarnessContext) -> dict[str, bytes]:
        del context
        return {}

    def inspect(
            self, domain_root: Path,
            context: HarnessContext) -> InspectionReport:
        del domain_root, context
        return InspectionReport(harness=self.name)

    def scaffold_guidance(self) -> str:
        return (
            "OpenClaw: no per-domain artifact - install the public plugin "
            "and designate this domain's OpenClaw agent explicitly")

    def format_lifecycle_output(
            self, moment: str, text: str, passed: bool) -> str:
        if moment != "session-start":
            raise ValueError(
                f"unsupported OpenClaw lifecycle moment: {moment}")
        outcome = "passed" if passed else "failed"
        return (
            _OPEN.format(outcome=outcome)
            + "\n"
            + text.rstrip("\r\n")
            + "\n"
            + _CLOSE
            + "\n"
        )


OPENCLAW = OpenClawAdapter()
