"""OpenClaw lifecycle output adapter.

OpenClaw is runtime-bound: its native plugin resolves the configured agent
workspace when a turn begins, then enters MarkdownLLM's neutral lifecycle
runner. No per-domain OpenClaw artifact belongs in the domain repository.

The native plugin owns hook registration and additive prompt delivery. This
adapter owns only the MarkdownLLM-side capabilities and output envelope.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from ..harness_ports import (
    AdapterCapabilities,
    HarnessContext,
    LifecycleAdmission,
    InspectionReport,
)
from ..model import parse_frontmatter
from ..yaml_loader import load_version_sentinel

_OPEN = '<markdownllm-session-start outcome="{outcome}">'
_CLOSE = "</markdownllm-session-start>"

def _failed_binding(reason: str) -> LifecycleAdmission:
    return LifecycleAdmission(
        allowed=False,
        text=(
            '<markdownllm-domain-binding outcome="refused">\n'
            + reason
            + "\n</markdownllm-domain-binding>"
        ),
    )


def _admit_domain(root: Path) -> LifecycleAdmission:
    root = root.resolve()
    if not root.is_dir():
        return _failed_binding("Configured OpenClaw workspace is not a directory.")

    agents = root / "AGENTS.md"
    if not agents.is_file():
        return _failed_binding(
            "Configured OpenClaw workspace has no domain AGENTS.md entry.")
    try:
        meta, _, error = parse_frontmatter(
            agents.read_text(encoding="utf-8"), source=agents)
    except (OSError, UnicodeError) as exc:
        return _failed_binding(
            f"Domain AGENTS.md is unreadable: {type(exc).__name__}.")
    if error or not isinstance(meta, dict):
        return _failed_binding(
            "Domain AGENTS.md has invalid or missing YAML frontmatter.")

    declared = meta.get("framework_root")
    if declared is not None:
        if not isinstance(declared, str) or not declared.strip():
            return _failed_binding(
                "Domain framework_root must be a non-empty relative path.")
        relative = Path(declared)
        if relative.is_absolute():
            return _failed_binding(
                "Domain framework_root must be relative to the domain root.")
        framework_root = (root / relative).resolve()
    else:
        framework_root = next(
            (candidate for candidate in (root, *root.parents)
             if (candidate / ".markdownllm").is_file()),
            None,
        )
        if framework_root is None:
            return _failed_binding(
                "No framework_root declaration or ancestor .markdownllm "
                "sentinel was found.")

    sentinel = framework_root / ".markdownllm"
    if not sentinel.is_file():
        return _failed_binding(
            "Domain framework_root does not resolve to a .markdownllm sentinel.")
    if not (framework_root / "kernel.md").is_file():
        return _failed_binding(
            "Resolved framework root has no Tier-0 kernel.md.")
    try:
        sentinel_data = load_version_sentinel(
            sentinel.read_text(encoding="utf-8"), source=sentinel)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return _failed_binding(
            f"Framework sentinel is invalid: {type(exc).__name__}.")

    domain_name = meta.get("name")
    if not isinstance(domain_name, str) or not domain_name.strip():
        return _failed_binding(
            "Domain AGENTS.md must declare a non-empty name.")

    version = str(sentinel_data["version"])
    return LifecycleAdmission(
        allowed=True,
        text=(
            '<markdownllm-domain-binding outcome="passed">\n'
            f"domain: {domain_name.strip()}\n"
            f"domain_root: {root}\n"
            f"framework_root: {framework_root}\n"
            f"framework_version: {version}\n"
            "</markdownllm-domain-binding>"
        ),
    )




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

    def admit_lifecycle(
            self, domain_root: Path, context: HarnessContext,
            moment: str) -> LifecycleAdmission:
        del context
        if moment != "session-start":
            return _failed_binding(
                f"Unsupported OpenClaw lifecycle moment: {moment}.")
        return _admit_domain(domain_root)

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
