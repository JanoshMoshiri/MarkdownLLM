"""Contract tests for the MarkdownLLM side of the OpenClaw adapter."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm import adapters  # noqa: E402
from markdownllm.adapters.openclaw import OPENCLAW  # noqa: E402
from markdownllm.harness_ports import (  # noqa: E402
    HarnessContext,
    InspectPort,
    LifecycleAdmissionPort,
    LifecycleOutputPort,
    RenderPort,
)


CTX = HarnessContext(framework_root_rel="../..")
FIXTURE_DOMAIN = (
    Path(__file__).resolve().parents[2]
    / "integrations"
    / "openclaw"
    / "tests"
    / "fixtures"
    / "openclaw-domain"
)


def test_public_fixture_domain_discovers_framework_and_emits_start(capsys):
    assert mdllm.cmd_session_start(
        SimpleNamespace(path=str(FIXTURE_DOMAIN))) == 0
    output = capsys.readouterr().out
    assert "Session Start" in output
    assert "Version: in sync" in output

    admission = OPENCLAW.admit_lifecycle(
        FIXTURE_DOMAIN, CTX, "session-start")
    assert admission.allowed is True
    assert "OpenClaw Adapter Fixture" in admission.text
    assert 'outcome="passed"' in admission.text

def _framework(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / ".markdownllm").write_text(
        "framework: Fixture\nversion: 1.0\n", encoding="utf-8")
    (root / "kernel.md").write_text("# Kernel\n", encoding="utf-8")


def test_binding_refuses_missing_entry_and_missing_sentinel(tmp_path):
    missing_entry = OPENCLAW.admit_lifecycle(
        tmp_path, CTX, "session-start")
    assert missing_entry.allowed is False
    assert "no domain AGENTS.md" in missing_entry.text

    domain = tmp_path / "domain"
    domain.mkdir()
    (domain / "AGENTS.md").write_text(
        "---\nname: Broken\nframework_root: ../missing\n---\n",
        encoding="utf-8",
    )
    missing_sentinel = OPENCLAW.admit_lifecycle(
        domain, CTX, "session-start")
    assert missing_sentinel.allowed is False
    assert "does not resolve" in missing_sentinel.text


def test_binding_supports_declared_and_ancestor_framework_roots(tmp_path):
    framework = tmp_path / "framework"
    _framework(framework)

    declared = tmp_path / "declared"
    declared.mkdir()
    (declared / "AGENTS.md").write_text(
        "---\nname: Declared\nframework_root: ../framework\n---\n",
        encoding="utf-8",
    )
    result = OPENCLAW.admit_lifecycle(
        declared, CTX, "session-start")
    assert result.allowed is True
    assert f"framework_root: {framework.resolve()}" in result.text

    nested = framework / "domains" / "nested"
    nested.mkdir(parents=True)
    (nested / "AGENTS.md").write_text(
        "---\nname: Nested\n---\n", encoding="utf-8")
    fallback = OPENCLAW.admit_lifecycle(
        nested, CTX, "session-start")
    assert fallback.allowed is True
    assert "domain: Nested" in fallback.text


def test_binding_rejects_absolute_framework_root(tmp_path):
    framework = tmp_path / "framework"
    _framework(framework)
    domain = tmp_path / "domain"
    domain.mkdir()
    (domain / "AGENTS.md").write_text(
        "---\nname: Mismatch\nframework_root: "
        + framework.as_posix()
        + "\n---\n",
        encoding="utf-8",
    )
    result = OPENCLAW.admit_lifecycle(domain, CTX, "session-start")
    assert result.allowed is False
    assert "must be relative" in result.text


def test_registered_as_runtime_bound_session_start_adapter():
    assert adapters.get("openclaw") is OPENCLAW
    assert isinstance(OPENCLAW, RenderPort)
    assert isinstance(OPENCLAW, InspectPort)
    assert isinstance(OPENCLAW, LifecycleOutputPort)
    assert isinstance(OPENCLAW, LifecycleAdmissionPort)
    assert OPENCLAW.capabilities().lifecycle_moments == ("session-start",)


def test_no_project_artifact_or_false_installation_claim(tmp_path):
    assert OPENCLAW.render(CTX) == {}
    report = OPENCLAW.inspect(tmp_path, CTX)
    assert report.harness == "openclaw"
    assert report.fragments == ()


def test_session_start_output_is_plain_additive_context():
    rendered = OPENCLAW.format_lifecycle_output(
        "session-start",
        "[steps: estate-sync=0, session-start=0]\norientation",
        True,
    )
    assert rendered.startswith(
        '<markdownllm-session-start outcome="passed">\n')
    assert "[steps: estate-sync=0, session-start=0]" in rendered
    assert rendered.endswith("</markdownllm-session-start>\n")


def test_unsupported_post_write_refuses_honestly():
    with pytest.raises(ValueError, match="unsupported OpenClaw"):
        OPENCLAW.format_lifecycle_output("post-write", "quiet", True)
