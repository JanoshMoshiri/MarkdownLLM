"""Tests for the ``perplexity`` adapter — the fourth registered harness.

Perplexity is estate-level and run-time bound, like Cowork: an account-level
skill bundle assembles the workspace after the session starts, so no
per-domain artifact ever exists. The honest diagnostic states pinned here are
the port stretch that registration forced (mirrored from Cowork), plus the
bundle-rendering guarantees that distinguish Perplexity: ambient credentials
(no PAT field, no ``plugin.json``), two skill surfaces (full + friendly), and
a full-commit SHA requirement.

Run: python -m pytest tools/tests/test_perplexity_adapter.py -q
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402  (registers tools/ on sys.path side effects)
from markdownllm import adapters  # noqa: E402
from markdownllm.adapters.perplexity import PERPLEXITY  # noqa: E402
from markdownllm.harness_diagnostics import diagnose_harness  # noqa: E402
from markdownllm.harness_ports import (  # noqa: E402
    HarnessContext, InspectPort, RenderPort,
)


def _ns(**kw):
    import argparse
    defaults = {"harness": None}
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _git_repo(p: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


# The real framework templates directory — bundle() reads from here.
TEMPLATES_ROOT = Path(__file__).resolve().parents[2] / "templates"

CTX = HarnessContext(framework_root_rel="../..")

_FULL_COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _bundle_config() -> dict[str, str]:
    return {
        "FRAMEWORK_REPO": "OWNER/MarkdownLLM",
        "FRAMEWORK_COMMIT": _FULL_COMMIT,
        "FRAMEWORK_VERSION": "0.0.0",
        "GIT_NAME": "Test Operator",
        "GIT_EMAIL": "t@example.com",
        "DOMAINS": "OWNER/domain-a OWNER/domain-b",
    }


# ----------------------------------------------------------------- registry

def test_registered_with_honest_capabilities():
    assert "perplexity" in adapters.names()
    adapter = adapters.get("perplexity")
    assert isinstance(adapter, RenderPort)
    assert isinstance(adapter, InspectPort)
    caps = adapter.capabilities()
    assert caps.harness == "perplexity"
    # session-start is bound (at run time, by the bundle); post-write is NOT —
    # nothing in Perplexity fires validation on individual writes.
    assert caps.lifecycle_moments == ("session-start",)
    assert "run time" in caps.notes
    assert "post-write" in caps.notes or "commit time" in caps.notes
    assert "no PAT" in caps.notes


def test_default_harness_unchanged():
    # Registering a fourth adapter is not a product decision about defaults
    # (that is the foundation plan's Phase 8, owner: operator).
    assert adapters.DEFAULT_HARNESS == "claude-code"
    assert "perplexity" in adapters.selection_choices()


# ------------------------------------------------------- honest emptiness

def test_renders_no_project_artifacts():
    assert PERPLEXITY.render(CTX) == {}
    assert PERPLEXITY.render(HarnessContext(framework_root_rel=".")) == {}


def test_inspect_reports_nothing_to_find(tmp_path):
    report = PERPLEXITY.inspect(tmp_path, CTX)
    assert report.harness == "perplexity"
    assert report.fragments == ()
    # No fragment can ever satisfy doctor's presence detection —
    # `any(fragment.artifact_present ...)` over an empty tuple is False —
    # so repo contents can never claim a Perplexity installation exists.
    assert not any(f.artifact_present for f in report.fragments)


# ------------------------------------------------------------- diagnostics

def test_diagnose_session_start_is_not_applicable_configuration(tmp_path):
    diagnostic = diagnose_harness(PERPLEXITY, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}

    ss = facts["session-start"]
    assert ss.support == "supported"
    assert ss.configuration == "not-applicable"
    assert ss.currency == "not-applicable"
    assert ss.legacy_id is None
    assert ss.launch_currency == "not-applicable"
    assert ss.trust == "unknown"  # Perplexity exposes no project-trust surface
    # Untested until a real bootstrap attests against a fingerprint.
    assert ss.execution.state == "untested"
    assert "fingerprint" in ss.execution.detail
    # The absent-configuration remediation must NOT fire: there is nothing
    # to adapter-install toward this harness.
    assert not any("adapter-install" in r for r in ss.remediations)
    # The honest remediation that does fire: a real event, not a static probe.
    assert any("real session-start event" in r for r in ss.remediations)


def test_diagnose_post_write_is_unsupported(tmp_path):
    diagnostic = diagnose_harness(PERPLEXITY, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}

    pw = facts["post-write"]
    assert pw.support == "unsupported"
    assert pw.configuration == "not-applicable"
    assert pw.currency == "not-applicable"
    assert pw.execution.state == "not-applicable"
    assert pw.trust == "not-applicable"


def test_render_time_adapters_unaffected_by_the_stretch(tmp_path):
    # The not-applicable branch keys on an empty render, so the render-time
    # adapters must keep their existing absent-configuration reading on an
    # empty domain (their renderers emit artifacts; configuration facts stay
    # derived from inspection).
    claude = adapters.get("claude-code")
    diagnostic = diagnose_harness(claude, tmp_path, CTX)
    facts = {f.capability: f for f in diagnostic.capabilities}
    assert facts["session-start"].configuration != "not-applicable"


# ------------------------------------------------------------------ scaffold

def test_scaffold_perplexity_selection_equals_none_selection(tmp_path):
    """`--harness perplexity` must add not one byte over `--harness none`:
    the entry pointers are neutral scaffold surface, and Perplexity's
    projection is honestly empty."""
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    _git_repo(tmp_path / "a")
    _git_repo(tmp_path / "b")
    none_target = tmp_path / "a" / "parity-domain"
    perplexity_target = tmp_path / "b" / "parity-domain"
    assert mdllm.cmd_scaffold(_ns(path=str(none_target), harness="none")) == 0
    assert mdllm.cmd_scaffold(
        _ns(path=str(perplexity_target), harness="perplexity")) == 0

    def tree(root: Path) -> set[str]:
        return {p.relative_to(root).as_posix()
                for p in root.rglob("*")
                if p.is_file() and ".git" not in p.relative_to(root).parts}

    assert tree(perplexity_target) == tree(none_target)


def test_harness_event_refuses_perplexity_without_output_port(tmp_path):
    # The neutral runner is deliberately not bound: the CLI must refuse
    # honestly, not crash, until a real session-start event attests.
    from markdownllm.lifecycle_runner import cmd_harness_event
    rc = cmd_harness_event(_ns(
        harness="perplexity", moment="session-start", path=str(tmp_path),
        definition_hash="unused"))
    assert rc == 2


# ------------------------------------------------------------- bundle / hash

def test_bundle_hash_is_stable_hex():
    h = PERPLEXITY.bundle_hash(TEMPLATES_ROOT)
    assert len(h) == 64
    int(h, 16)  # valid hex
    # Deterministic across calls.
    assert PERPLEXITY.bundle_hash(TEMPLATES_ROOT) == h


def test_bundle_renders_expected_files_and_no_plugin_json():
    rendered = PERPLEXITY.bundle(TEMPLATES_ROOT, _bundle_config())
    keys = set(rendered)

    # Full / operator skill.
    assert "markdownllm-bootstrap/SKILL.md" in keys
    assert "markdownllm-bootstrap/README.md" in keys
    assert "markdownllm-bootstrap/references/SESSION.md" in keys
    assert "markdownllm-bootstrap/references/bootstrap.sh" in keys
    assert "markdownllm-bootstrap/references/config.env" in keys
    assert "markdownllm-bootstrap/references/config.env.example" in keys
    # Friendly / simple skill (separate Perplexity Skill, self-contained).
    assert "markdownllm-bootstrap-friendly/SKILL.md" in keys
    assert "markdownllm-bootstrap-friendly/references/bootstrap.sh" in keys
    assert "markdownllm-bootstrap-friendly/references/config.env" in keys
    assert "markdownllm-bootstrap-friendly/references/config.env.example" in keys
    assert len(rendered) == 10

    # Perplexity is not a Claude Code plugin — no plugin manifest is rendered.
    assert not any(k.endswith("plugin.json") for k in keys)


def test_bundle_uses_ambient_credentials_no_pat_field():
    rendered = PERPLEXITY.bundle(TEMPLATES_ROOT, _bundle_config())
    # An active PAT-intake instruction — the thing the cowork bundle does and
    # this adapter must NOT — is characterised by telling the operator to
    # paste a token. Negated mentions ("no ... is ever pasted") are fine.
    paste_instruction = (
        "paste your", "paste their", "paste a token",
        "paste a personal access", "paste the token", "paste it",
    )
    for key, content in rendered.items():
        text = content.decode("utf-8")
        lower = text.lower()
        # No PAT field defined in any config, no Basic-auth header, and no
        # active instruction to obtain/paste a token.
        assert "GH_PAT=" not in text, f"{key}: must not define a GH_PAT field"
        assert "Authorization: Basic" not in text, (
            f"{key}: must not embed a Basic-auth header")
        for phrase in paste_instruction:
            assert phrase not in lower, (
                f"{key}: must not instruct pasting a token ({phrase!r})")


def test_config_envs_carry_empty_friendly_fields():
    # Both config.env files carry empty FRIENDLY_PROFILE_NAME=/FRIENDLY_DOMAINS=
    # placeholders — the friendly surface fills them (operator-private); the
    # full surface leaves them empty. Present in BOTH so the bootstrap's
    # FRIENDLY_DOMAINS lookup is never absent-unsafe under `set -u`/`set -e`
    # when the full (non-friendly) skill runs.
    example = (TEMPLATES_ROOT / "perplexity-bundle" / "config.env.example").read_text(
        encoding="utf-8")
    assert "FRIENDLY_PROFILE_NAME=" in example
    assert "FRIENDLY_DOMAINS=" in example

    rendered = PERPLEXITY.bundle(TEMPLATES_ROOT, _bundle_config())
    for cfg_path in (
        "markdownllm-bootstrap/references/config.env",
        "markdownllm-bootstrap-friendly/references/config.env",
    ):
        cfg = rendered[cfg_path].decode("utf-8")
        profile_line = [ln for ln in cfg.splitlines()
                        if ln.startswith("FRIENDLY_PROFILE_NAME=")][0]
        assert profile_line == "FRIENDLY_PROFILE_NAME=", (
            f"{cfg_path}: profile field must be empty until operator-edited")
        subset_line = [ln for ln in cfg.splitlines()
                       if ln.startswith("FRIENDLY_DOMAINS=")][0]
        assert subset_line == "FRIENDLY_DOMAINS=", (
            f"{cfg_path}: domain subset must be operator-supplied, not injected")


def test_no_private_names_in_public_source():
    # The operator's private identifiers must never live in committed source.
    # The forbidden markers are supplied out of band (env var) so the
    # operator's private names never appear in this test file itself; CI and
    # other contributors skip this scan, the operator runs it locally with
    # their own markers.
    import os
    import pytest
    raw = os.environ.get("MDLLM_PRIVATE_MARKERS", "").strip()
    if not raw:
        pytest.skip(
            "set MDLLM_PRIVATE_MARKERS=a,b,... to run the private-name leak scan")
    markers = tuple(m.strip().lower() for m in raw.split(",") if m.strip())
    tracked = [
        TEMPLATES_ROOT / "perplexity-bundle" / "SKILL.md.template",
        TEMPLATES_ROOT / "perplexity-bundle" / "SKILL.friendly.md.template",
        TEMPLATES_ROOT / "perplexity-bundle" / "SESSION.md.template",
        TEMPLATES_ROOT / "perplexity-bundle" / "bootstrap.sh.template",
        TEMPLATES_ROOT / "perplexity-bundle" / "config.env.example",
        TEMPLATES_ROOT / "perplexity-bundle" / "README.md.template",
        Path(__file__).resolve().parent.parent / "markdownllm" / "adapters"
            / "perplexity.py",
    ]
    for path in tracked:
        text = path.read_text(encoding="utf-8").lower()
        for marker in markers:
            assert marker not in text, (
                f"{path}: public source must not contain {marker!r}")


def test_bootstrap_honors_friendly_domains_subset():
    # The shared bootstrap restricts `mdllm assemble` to FRIENDLY_DOMAINS when
    # the operator has set a subset (the friendly skill's private config);
    # absent/empty, the full DOMAINS set is assembled unchanged.
    rendered = PERPLEXITY.bundle(TEMPLATES_ROOT, _bundle_config())
    bootstrap = rendered[
        "markdownllm-bootstrap/references/bootstrap.sh"].decode("utf-8")
    assert "FRIENDLY_DOMAINS" in bootstrap
    # The override writes a temp config with DOMAINS replaced by the subset.
    assert "ASSEMBLE_CONFIG" in bootstrap
    assert "grep -vE '^DOMAINS='" in bootstrap
    # Absent-safe under `set -euo pipefail`: the FRIENDLY_DOMAINS lookup must
    # not exit the script when the field is absent from a full-surface config.
    assert "|| true" in bootstrap


def test_bundle_requires_full_commit_sha():
    import pytest
    bad = _bundle_config()
    bad["FRAMEWORK_COMMIT"] = "deadbeef"  # not 40 hex
    with pytest.raises(ValueError):
        PERPLEXITY.bundle(TEMPLATES_ROOT, bad)


def test_bundle_skill_descriptions_under_limit():
    # description_findings raises in bundle(); a passing bundle means every
    # SKILL.md frontmatter description is within the Perplexity limit.
    rendered = PERPLEXITY.bundle(TEMPLATES_ROOT, _bundle_config())
    skill_texts = [c.decode("utf-8") for k, c in rendered.items()
                   if k.endswith("SKILL.md")]
    assert len(skill_texts) == 2  # full + friendly
