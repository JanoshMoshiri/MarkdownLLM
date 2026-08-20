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
binding integrity — the installed bundle's hash against the exact cloned
framework commit's expectation — lands there too, alongside the ``ProbePort``
fingerprints that let a real bootstrap attest execution. This module is
the single place Cowork vocabulary may appear in code (architecture
fitness gate).
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Mapping

from ..harness_ports import (
    AdapterCapabilities, HarnessContext, InspectionReport,
)

BUNDLE_TEMPLATES_DIR = "cowork-bundle"
PLUGIN_NAME = "markdownllm-bootstrap"

# Platform constraint, learned at an install failure (2026-08-18): the
# harness rejects a plugin whose manifest or skill description exceeds 500
# characters, and it rejects it at INSTALL — the one moment the operator is
# furthest from the templates that caused it. So the build refuses instead,
# where the fix is one file away. A vendor limit belongs in the vendor
# adapter; a future bundle harness declares its own.
MAX_DESCRIPTION_CHARACTERS = 500

# The MECHANISM: the templates whose rendered forms decide how a session
# behaves. Hashed for run-time binding integrity — operator config (config.env) is
# deliberately outside the hash, so retargeting the estate never reads as
# mechanism drift, and a mechanism change always does.
_MECHANISM_TEMPLATES = (
    "SKILL.md.template",
    "SESSION.md.template",
    "bootstrap.sh.template",
)


def _frontmatter_description(text: str) -> str | None:
    """The `description:` value from a skill's YAML frontmatter, folded to
    the single line the harness measures (a block scalar wrapped over five
    source lines is still one description to the installer)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        return None
    body = match.group(1)
    field = re.search(r"^description:[ \t]*(.*(?:\n(?![A-Za-z_-]+:).*)*)",
                      body, re.M)
    if not field:
        return None
    return " ".join(field.group(1).split())


def description_findings(rendered: Mapping[str, bytes]) -> list[str]:
    """Every description the harness will measure, checked against its
    limit. Returns one finding per violation, naming the file, the length,
    and the overage — the install error names none of those."""
    out: list[str] = []
    for path, content in sorted(rendered.items()):
        text = content.decode("utf-8")
        if path.endswith(".claude-plugin/plugin.json"):
            try:
                description = json.loads(text).get("description", "")
            except json.JSONDecodeError:
                out.append(f"{path}: not valid JSON — the manifest would "
                           "be unreadable at install")
                continue
        elif path.endswith("SKILL.md"):
            description = _frontmatter_description(text)
            if description is None:
                out.append(f"{path}: no frontmatter `description:` — the "
                           "harness has nothing to trigger the skill on")
                continue
        else:
            continue
        if len(description) > MAX_DESCRIPTION_CHARACTERS:
            out.append(
                f"{path}: description is {len(description)} characters, "
                f"{len(description) - MAX_DESCRIPTION_CHARACTERS} over the "
                f"{MAX_DESCRIPTION_CHARACTERS}-character limit — shorten it "
                "in templates/cowork-bundle/ and rebuild")
    return out


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

    # -- BundlePort --------------------------------------------------------
    def bundle_hash(self, templates_root: Path) -> str:
        """The canonical mechanism hash — run-time binding-integrity anchor.

        Hashes the RAW template bytes (placeholders included, config
        excluded), so the framework can answer "what would I render now?"
        without knowing any operator's estate, and a built bundle can
        carry the answer it was built against.
        """
        digest = hashlib.sha256()
        base = templates_root / BUNDLE_TEMPLATES_DIR
        for name in _MECHANISM_TEMPLATES:
            digest.update(name.encode("utf-8"))
            # Line-ending-normalized: a Windows checkout must stamp the
            # same mechanism a Linux VM recomputes, or every cross-platform
            # build would read as STALE.
            digest.update((base / name).read_bytes().replace(b"\r\n", b"\n"))
        return digest.hexdigest()

    def bundle(self, templates_root: Path,
               config: Mapping[str, str]) -> dict[str, bytes]:
        """Render the account-level plugin bundle. Pure: path → bytes;
        the caller (bundle_service) writes, and keeps the output private —
        the rendered config.env names the operator's repositories."""
        framework_commit = config.get("FRAMEWORK_COMMIT", "")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", framework_commit):
            raise ValueError(
                "FRAMEWORK_COMMIT must be a full Git object id; refusing "
                "to render a bundle with moving or missing executable source")
        base = templates_root / BUNDLE_TEMPLATES_DIR
        mechanism = self.bundle_hash(templates_root)
        substitutions = {
            "{framework_version}": config.get("FRAMEWORK_VERSION", "unknown"),
            "{bundle_hash}": mechanism,
            "{git_name}": config.get("GIT_NAME", ""),
        }

        def render(template: str) -> bytes:
            text = (base / template).read_text(encoding="utf-8")
            for key, value in substitutions.items():
                text = text.replace(key, value)
            # LF always: bootstrap.sh runs under bash on Linux, where a
            # CRLF shebang is "bad interpreter"; the rest follow for
            # deterministic bytes regardless of build platform.
            return text.replace("\r\n", "\n").encode("utf-8")

        config_env = (
            "# markdownllm-bootstrap configuration — DERIVED from the local "
            "estate by\n"
            f"# `mdllm bundle --harness {self.name}` (framework "
            f"v{config.get('FRAMEWORK_VERSION', 'unknown')}). Edit freely; "
            "rebuild to re-derive.\n"
            f"FRAMEWORK_REPO={config.get('FRAMEWORK_REPO', '')}\n"
            f"FRAMEWORK_COMMIT={config.get('FRAMEWORK_COMMIT', '')}\n"
            f"GIT_NAME={config.get('GIT_NAME', '')}\n"
            f"GIT_EMAIL={config.get('GIT_EMAIL', '')}\n"
            f"DOMAINS={config.get('DOMAINS', '')}\n"
        ).encode("utf-8")

        skill = f"{PLUGIN_NAME}/skills/spin-up-domain"
        rendered = {
            f"{PLUGIN_NAME}/.claude-plugin/plugin.json":
                render("plugin.json.template"),
            f"{PLUGIN_NAME}/README.md": render("README.md.template"),
            f"{skill}/SKILL.md": render("SKILL.md.template"),
            f"{skill}/bootstrap.sh": render("bootstrap.sh.template"),
            f"{skill}/references/SESSION.md": render("SESSION.md.template"),
            f"{skill}/references/config.env": config_env,
            f"{skill}/references/config.env.example":
                (base / "config.env.example").read_bytes(),
        }
        problems = description_findings(rendered)
        if problems:
            raise ValueError(
                "this bundle would be rejected at install:\n  "
                + "\n  ".join(problems))
        return rendered


COWORK = CoworkAdapter()
