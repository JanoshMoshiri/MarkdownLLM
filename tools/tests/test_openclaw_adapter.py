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


def test_registered_as_runtime_bound_session_start_adapter():
    assert adapters.get("openclaw") is OPENCLAW
    assert isinstance(OPENCLAW, RenderPort)
    assert isinstance(OPENCLAW, InspectPort)
    assert isinstance(OPENCLAW, LifecycleOutputPort)
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
