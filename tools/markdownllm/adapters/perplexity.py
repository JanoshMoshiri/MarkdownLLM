"""The Perplexity adapter — the fourth registered harness.

Perplexity Computer is estate-level and run-time bound, like Cowork: an
account-level skill bundle assembles the workspace (cloning the framework
and the selected domains) *after* the session has started, so there is
never a per-domain artifact to render, inspect, or hash. ``render()``
returning no artifacts is that fact stated through the port — not a stub
awaiting content.

What makes Perplexity a different class from Cowork is the credential
path: Perplexity has a connected GitHub credential, injected per tool
call by the harness. The bootstrap therefore uses ambient credentials
throughout — ``gh auth setup-git`` configures the credential helper, and
the framework's own ambient-credential mode (active when ``GH_PAT`` is
unset) carries clone, assemble, and publish. No personal access token is
pasted, stored on disk, written into git config, or echoed into the
transcript. This is strictly safer than the PAT flow Cowork is forced into
because Claude Code and Codex have no GitHub connector.

What this adapter truthfully claims today:

- **session-start is bound** — the skill performs the ordered lifecycle
  mechanically after assembly, for the session that invoked it. Execution
  reports ``untested`` until a real bootstrap attests against a probe
  fingerprint (as Cowork does): installation is not activation, and a
  static probe is not an event.
- **post-write feedback is NOT bound** — nothing in Perplexity fires
  validation on individual writes; the git pre-commit hook is the first
  check that sees them. Declared so doctor can say it rather than imply
  otherwise.
- **Trust is unknown** — Perplexity exposes no stable project-trust surface.

The bundle (full skill, friendly skill, session contract, reference
bootstrap, configuration) is rendered from framework-owned templates; the
output is a Perplexity Agent Skill (``SKILL.md`` + ``references/``), not a
Claude Code plugin manifest — there is no ``plugin.json`` and no PAT
field. This module is the single place Perplexity vocabulary may appear in
code (architecture fitness gate).
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Mapping

from ..harness_ports import (
    AdapterCapabilities, HarnessContext, InspectionReport,
)

BUNDLE_TEMPLATES_DIR = "perplexity-bundle"
SKILL_NAME = "markdownllm-bootstrap"
FRIENDLY_SKILL_NAME = "markdownllm-bootstrap-friendly"

# Perplexity Skill (agentskills.io) frontmatter `description` limit.
MAX_DESCRIPTION_CHARACTERS = 1024

# The MECHANISM: the templates whose rendered forms decide how a session
# behaves. Hashed for run-time binding integrity — operator config
# (config.env) is deliberately outside the hash, so retargeting the estate
# never reads as mechanism drift, and a mechanism change always does.
_MECHANISM_TEMPLATES = (
    "SKILL.md.template",
    "SKILL.friendly.md.template",
    "SESSION.md.template",
    "bootstrap.sh.template",
)


def _frontmatter_description(text: str) -> str | None:
    """The `description:` value from a skill's YAML frontmatter, folded to
    the single line the harness measures (a block scalar wrapped over
    several source lines is still one description to the installer)."""
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
    """Every description the harness will measure, checked against the
    Perplexity Skill limit. Returns one finding per violation, naming the
    file, the length, and the overage. No ``plugin.json`` is rendered, so
    only ``SKILL.md`` frontmatter descriptions are measured."""
    out: list[str] = []
    for path, content in sorted(rendered.items()):
        if not path.endswith("SKILL.md"):
            continue
        text = content.decode("utf-8")
        description = _frontmatter_description(text)
        if description is None:
            out.append(f"{path}: no frontmatter `description:` — the "
                       "harness has nothing to trigger the skill on")
            continue
        if len(description) > MAX_DESCRIPTION_CHARACTERS:
            out.append(
                f"{path}: description is {len(description)} characters, "
                f"{len(description) - MAX_DESCRIPTION_CHARACTERS} over the "
                f"{MAX_DESCRIPTION_CHARACTERS}-character limit — shorten it "
                "in templates/perplexity-bundle/ and rebuild")
    return out


class PerplexityAdapter:
    """Capabilities plus honest emptiness: no per-domain managed artifacts."""

    name = "perplexity"

    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(
            harness=self.name,
            lifecycle_moments=("session-start",),
            notes=(
                "binds at run time through the account-level skill bundle, "
                "not through project configuration; uses ambient GitHub "
                "credentials (connected connector) — no PAT; no post-write "
                "feedback — writes meet the floor at commit time"),
        )

    # -- RenderPort --------------------------------------------------------
    def render(self, context: HarnessContext) -> dict[str, bytes]:
        """No project artifacts, for any context — the binding lives in the
        bundle. Diagnostics read this as configuration: not-applicable."""
        return {}

    # -- InspectPort -------------------------------------------------------
    def inspect(self, domain_root: Path,
                context: HarnessContext) -> InspectionReport:
        """Nothing of Perplexity's lives in a domain repo; report exactly
        that. No fragments means doctor's presence detection can never claim
        a Perplexity installation from repo contents — there is none to find."""
        return InspectionReport(harness=self.name)

    # -- ScaffoldNoticePort ------------------------------------------------
    def scaffold_guidance(self) -> str:
        return ("Perplexity: no per-domain artifact — sessions bind through "
                "the account-level skill bundle at run time, using ambient "
                "GitHub credentials (no PAT)")

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
        """Render the account-level skill bundle as a Perplexity Agent Skill
        (``SKILL.md`` + ``references/``), in two surfaces: a full/operator
        skill and a friendly/simple skill. Pure: path -> bytes; the caller
        (bundle_service) writes, and keeps the output private — the rendered
        config.env names the operator's repositories and (for the friendly
        surface) the operator's profile name and domain subset, none of which
        belong in public source. No ``plugin.json``; no PAT field."""
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
            "rebuild to re-derive. Ambient GitHub credentials — no PAT.\n"
            f"FRAMEWORK_REPO={config.get('FRAMEWORK_REPO', '')}\n"
            f"FRAMEWORK_COMMIT={config.get('FRAMEWORK_COMMIT', '')}\n"
            f"GIT_NAME={config.get('GIT_NAME', '')}\n"
            f"GIT_EMAIL={config.get('GIT_EMAIL', '')}\n"
            f"DOMAINS={config.get('DOMAINS', '')}\n"
            "# Optional — friendly-surface fields. Empty by default: the full\n"
            "# surface ignores them; the friendly surface fills them in its own\n"
            "# (operator-edited) config. Present here so the bootstrap's lookup\n"
            "# is never absent-unsafe under `set -u`.\n"
            "FRIENDLY_PROFILE_NAME=\n"
            "FRIENDLY_DOMAINS=\n"
        ).encode("utf-8")

        # The friendly surface carries optional profile config (the operator's
        # name and a domain subset). These are private to the rendered bundle
        # and never appear in the public templates as real values — only the
        # documented empty placeholders in config.env.example do.
        friendly_config_env = (
            "# markdownllm-bootstrap-friendly configuration — DERIVED from "
            "the local estate by\n"
            f"# `mdllm bundle --harness {self.name}`. Edit freely; rebuild "
            "to re-derive. Ambient GitHub credentials — no PAT.\n"
            f"FRAMEWORK_REPO={config.get('FRAMEWORK_REPO', '')}\n"
            f"FRAMEWORK_COMMIT={config.get('FRAMEWORK_COMMIT', '')}\n"
            f"GIT_NAME={config.get('GIT_NAME', '')}\n"
            f"GIT_EMAIL={config.get('GIT_EMAIL', '')}\n"
            f"DOMAINS={config.get('DOMAINS', '')}\n"
            "# Optional: the operator's first name, to personalise the "
            "greeting.\n"
            "FRIENDLY_PROFILE_NAME=\n"
            "# Optional: restrict the friendly skill to a subset of "
            "domains (whitespace-separated owner/repo).\n"
            "FRIENDLY_DOMAINS=\n"
        ).encode("utf-8")

        rendered = {
            # Full / operator skill.
            f"{SKILL_NAME}/README.md": render("README.md.template"),
            f"{SKILL_NAME}/SKILL.md": render("SKILL.md.template"),
            f"{SKILL_NAME}/references/bootstrap.sh":
                render("bootstrap.sh.template"),
            f"{SKILL_NAME}/references/SESSION.md": render("SESSION.md.template"),
            f"{SKILL_NAME}/references/config.env": config_env,
            f"{SKILL_NAME}/references/config.env.example":
                (base / "config.env.example").read_bytes(),
            # Friendly / simple skill (separate Perplexity Skill). Shares the
            # bootstrap transport so the friendly skill is self-contained.
            f"{FRIENDLY_SKILL_NAME}/SKILL.md":
                render("SKILL.friendly.md.template"),
            f"{FRIENDLY_SKILL_NAME}/references/bootstrap.sh":
                render("bootstrap.sh.template"),
            f"{FRIENDLY_SKILL_NAME}/references/config.env":
                friendly_config_env,
            f"{FRIENDLY_SKILL_NAME}/references/config.env.example":
                (base / "config.env.example").read_bytes(),
        }
        problems = description_findings(rendered)
        if problems:
            raise ValueError(
                "this bundle would be rejected at install:\n  "
                + "\n  ".join(problems))
        return rendered


PERPLEXITY = PerplexityAdapter()
