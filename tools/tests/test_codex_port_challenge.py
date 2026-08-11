"""Phase 2B: non-installed Codex shape probe against the draft ports.

This is contract evidence, not a Codex adapter.  It renders bytes in memory
only and creates no project ``.codex`` state.  The assertions pin only facts
documented by the official Codex hooks reference on 2026-08-11; Phase 4 owns
the executable projection.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import harness_ports as hp  # noqa: E402


class _CodexShapeProbeRenderer:
    """Enough second-vendor shape to challenge the inward port, never ship."""

    def capabilities(self) -> hp.AdapterCapabilities:
        return hp.AdapterCapabilities(
            harness="codex",
            lifecycle_moments=("session-start", "post-write"),
            notes="one handler preserves ordered startup steps")

    def render(self, context: hp.HarnessContext) -> dict[str, bytes]:
        # Codex runs matching command hooks concurrently. One handler owns the
        # ordered binding; the future handler consumes context.binding(...).
        start = context.binding("session-start")
        write = context.binding("post-write")
        assert start.delivery == "context" and len(start.steps) == 2
        assert write.delivery == "feedback" and len(write.steps) == 1

        root_posix = '"$(git rev-parse --show-toplevel)"'
        root_windows = '"$(git rev-parse --show-toplevel)"'
        config = {
            "description": "MarkdownLLM lifecycle hardening (shape probe)",
            "hooks": {
                "SessionStart": [{
                    "matcher": "startup|resume|clear|compact",
                    "hooks": [{
                        "type": "command",
                        "command": (
                            "mdllm-codex-hook session-start --root "
                            f"{root_posix}"),
                        "commandWindows": (
                            "mdllm-codex-hook.exe session-start --root "
                            f"{root_windows}"),
                        "timeout": 120,
                        "additionalContextLimit": 2500,
                    }],
                }],
                "PostToolUse": [{
                    "matcher": "Edit|Write",
                    "hooks": [{
                        "type": "command",
                        "command": (
                            "mdllm-codex-hook post-write --json-feedback "
                            f"--root {root_posix}"),
                        "commandWindows": (
                            "mdllm-codex-hook.exe post-write --json-feedback "
                            f"--root {root_windows}"),
                        "timeout": 120,
                    }],
                }],
            },
        }
        return {".codex/hooks.json":
                (json.dumps(config, indent=2) + "\n").encode("utf-8")}


def _rendered_config() -> tuple[hp.HarnessContext, dict]:
    context = hp.HarnessContext(framework_root_rel="../..")
    renderer = _CodexShapeProbeRenderer()
    assert isinstance(renderer, hp.RenderPort)
    raw = renderer.render(context)[".codex/hooks.json"]
    return context, json.loads(raw)


def test_codex_shape_preserves_order_in_one_start_handler():
    context, config = _rendered_config()
    groups = config["hooks"]["SessionStart"]
    assert len(groups) == 1
    assert groups[0]["matcher"] == "startup|resume|clear|compact"
    assert len(groups[0]["hooks"]) == 1
    assert tuple(step.operation for step in
                 context.binding("session-start").steps) == \
        ("estate-sync", "session-start")


def test_codex_shape_is_cross_platform_rooted_and_bounded():
    _, config = _rendered_config()
    for event in ("SessionStart", "PostToolUse"):
        handler = config["hooks"][event][0]["hooks"][0]
        assert handler["command"] and handler["commandWindows"]
        assert "git rev-parse --show-toplevel" in handler["command"]
        assert "git rev-parse --show-toplevel" in handler["commandWindows"]
        assert handler["timeout"] > 0
    start = config["hooks"]["SessionStart"][0]["hooks"][0]
    assert 0 < start["additionalContextLimit"] <= 2500


def test_codex_post_write_uses_documented_alias_and_feedback_channel():
    context, config = _rendered_config()
    group = config["hooks"]["PostToolUse"][0]
    assert group["matcher"] == "Edit|Write"
    assert "--json-feedback" in group["hooks"][0]["command"]
    binding = context.binding("post-write")
    assert binding.delivery == "feedback"
    assert binding.failure == "surface-and-continue"


def test_inspection_shape_can_represent_both_codex_sources_and_ambiguity():
    report = hp.InspectionReport(
        harness="codex",
        fragments=(
            hp.ManagedFragment(
                path=".codex/hooks.json", present=True, readable=True,
                valid=True, current=True),
            hp.ManagedFragment(
                path=".codex/config.toml", present=True, readable=True,
                valid=True, current=None),
        ),
        findings=("both project hook sources are active",),
    )
    assert len(report.fragments) == 2 and report.findings
