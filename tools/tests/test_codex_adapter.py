"""Codex adapter contract: pure projection and conservative inspection.

All project config is created under pytest temporary directories.  These
tests never install or create a live repository ``.codex`` layer.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.adapters.codex import (  # noqa: E402
    CODEX, CONFIG_PATH, HOOKS_PATH,
)
from markdownllm.adapter_install import (  # noqa: E402
    InstallPolicyPort,
    LegacyDefinitionPort,
)
from markdownllm.harness_ports import (  # noqa: E402
    HarnessContext, InspectPort, LifecycleOutputPort, RenderPort,
)
from markdownllm.harness_diagnostics import ProbePort  # noqa: E402


CTX = HarnessContext(framework_root_rel="../framework")
ROOT_CTX = HarnessContext(framework_root_rel=".")


def _rendered() -> dict:
    return json.loads(CODEX.render(CTX)[HOOKS_PATH].decode("utf-8"))


def _windows_payload(command: str) -> str:
    marker = "set _MDLLM_HOOK="
    start = command.index(marker) + len(marker)
    end = command.index("&where.exe", start)
    return base64.b64decode(command[start:end]).decode("utf-16-le")


def _write_json(root: Path, value: object) -> Path:
    path = root / HOOKS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return path


def _fragment(report, path: str):
    return next(fragment for fragment in report.fragments
                if fragment.path == path)


def test_codex_adapter_satisfies_its_declared_service_ports():
    assert isinstance(CODEX, RenderPort)
    assert isinstance(CODEX, InspectPort)
    assert isinstance(CODEX, ProbePort)
    assert isinstance(CODEX, LifecycleOutputPort)
    assert isinstance(CODEX, InstallPolicyPort)
    assert isinstance(CODEX, LegacyDefinitionPort)
    assert CODEX.capabilities().lifecycle_moments == (
        "session-start", "post-write")


def test_root_legacy_definition_is_frozen_and_root_scoped():
    definitions = CODEX.legacy_definitions(ROOT_CTX)

    assert [item.legacy_id for item in definitions] == [
        "legacy-root-v1", "legacy-root-fixed-step-v1",
        "legacy-output-tail-v1"]
    assert all(item.path == HOOKS_PATH for item in definitions)
    assert [(len(item.owned_fragment),
             hashlib.sha256(item.owned_fragment).hexdigest())
            for item in definitions] == [
        (14328,
         "9f590fc9483ef0463d52ad32cd6c2624ba2e95b1a7621b4dd68a964ed641da53"),
        (15508,
         "7e17affd756a09e6a96d67e01b8ef7d2d72e2499071d21c9c1851b72bb580df0"),
        (15508,
         "4c229fca8a71ed7a528268867823505bc9d0f1ebc131cf0d7bc27e1c61618aa3"),
    ]
    nested = CODEX.legacy_definitions(CTX)
    assert [item.legacy_id for item in nested] == ["legacy-output-tail-v1"]
    assert [(len(item.owned_fragment),
             hashlib.sha256(item.owned_fragment).hexdigest())
            for item in nested] == [
        (15646,
         "fa36d164c1190fd3e33ed20fea0a15c9beaaa149353fd57b8011f4a7ef5bfcf9")]


def test_inspect_names_only_the_exact_unextended_root_legacy(tmp_path):
    legacy = CODEX.legacy_definitions(ROOT_CTX)[0].owned_fragment
    path = tmp_path / HOOKS_PATH
    path.parent.mkdir(parents=True)
    path.write_bytes(legacy)

    exact = _fragment(CODEX.inspect(tmp_path, ROOT_CTX), HOOKS_PATH)
    assert exact.current is False
    assert exact.legacy_id == "legacy-root-v1"

    changed = legacy.replace(b'"timeout":120', b'"timeout":119', 1)
    assert changed != legacy
    path.write_bytes(changed)
    mutated = _fragment(CODEX.inspect(tmp_path, ROOT_CTX), HOOKS_PATH)
    assert mutated.current is False
    assert mutated.legacy_id is None


def test_inspect_names_pre_budget_root_as_exact_legacy(tmp_path):
    definition = next(
        item for item in CODEX.legacy_definitions(ROOT_CTX)
        if item.legacy_id == "legacy-root-fixed-step-v1")
    path = tmp_path / HOOKS_PATH
    path.parent.mkdir(parents=True)
    path.write_bytes(definition.owned_fragment)

    fragment = _fragment(CODEX.inspect(tmp_path, ROOT_CTX), HOOKS_PATH)

    assert fragment.current is False
    assert fragment.legacy_id == "legacy-root-fixed-step-v1"


def test_render_is_pure_deterministic_and_project_local(tmp_path):
    before = sorted(tmp_path.rglob("*"))
    first = CODEX.render(CTX)
    second = CODEX.render(CTX)
    assert first == second
    assert set(first) == {HOOKS_PATH}
    assert sorted(tmp_path.rglob("*")) == before


def test_render_has_one_bounded_cross_platform_handler_per_moment():
    config = _rendered()
    assert config["description"].startswith("MarkdownLLM")
    for event, matcher in (
            ("SessionStart", "startup|resume|clear|compact"),
            ("PostToolUse", "Edit|Write")):
        groups = config["hooks"][event]
        assert len(groups) == 1
        assert groups[0]["matcher"] == matcher
        handlers = groups[0]["hooks"]
        assert len(handlers) == 1
        handler = handlers[0]
        assert handler["type"] == "command"
        assert handler["command"] and handler["commandWindows"]
        assert 0 < handler["timeout"] <= 120
        assert 0 < handler["additionalContextLimit"] <= 2500
        assert "git rev-parse --show-toplevel" in handler["command"]
        windows_payload = _windows_payload(handler["commandWindows"])
        assert "git rev-parse --show-toplevel" in windows_payload
        assert "../framework/tools/mdllm.py" in handler["command"]
        assert "..\\framework\\tools\\mdllm.ps1" in \
            windows_payload
        assert handler["commandWindows"].startswith(
            "cmd.exe /d /v:on /s /c")
        assert "where.exe pwsh.exe" in handler["commandWindows"]
        assert "powershell.exe -NoLogo" in handler["commandWindows"]
        assert len(handler["commandWindows"]) < 8191


def test_posix_framework_path_is_shell_literal_not_executable_syntax(
        tmp_path):
    shell = shutil.which("sh")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    marker = tmp_path / "must-not-be-created"
    hostile = f"../missing$(touch {marker.as_posix()})'`touch ignored`$HOME"
    context = HarnessContext(framework_root_rel=hostile)
    command = json.loads(CODEX.render(context)[HOOKS_PATH])["hooks"][
        "SessionStart"][0]["hooks"][0]["command"]

    assignment = command.splitlines()[1]
    assert assignment.startswith('MDLLM="$ROOT/"\'')
    assert assignment.endswith("/tools/mdllm.py'")
    assert "'\"'\"'" in assignment
    assert f'"$ROOT/{hostile}' not in assignment
    if shell is None:
        return

    completed = subprocess.run(
        [shell, "-c", command], cwd=tmp_path,
        capture_output=True, text=True, timeout=30)

    assert completed.returncode == 0
    assert not marker.exists()


def test_windows_runner_exit_is_surfaced_but_hook_still_returns_zero(
        tmp_path):
    if os.name != "nt":
        pytest.skip("native Windows host is required")
    if shutil.which("cmd.exe") is None or shutil.which("powershell.exe") is None:
        pytest.skip("stock Windows command hosts are required")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    framework = tmp_path / "fixture-framework" / "tools"
    framework.mkdir(parents=True)
    (framework / "mdllm.ps1").write_text("exit 23\n", encoding="utf-8")
    shutil.copy2(
        Path(__file__).resolve().parents[1] / "resolve-runtime.ps1",
        framework / "resolve-runtime.ps1")
    context = HarnessContext(framework_root_rel="fixture-framework")
    windows = json.loads(CODEX.render(context)[HOOKS_PATH])["hooks"][
        "PostToolUse"][0]["hooks"][0]["commandWindows"]
    payload = _windows_payload(windows)
    # Force the selector's absence branch without changing the rendered
    # payload.  This proves stock Windows PowerShell can enter the same body.
    fallback = windows.replace(
        "where.exe pwsh.exe", "where.exe mdllm-no-such-host.exe", 1)
    fixture_dir = Path(__file__).parent / "fixtures" / "powershell"
    candidate_dir = tmp_path / "candidate-bin"
    candidate_dir.mkdir()
    # Codex's declared PATH order is python3 then python.  The same committed
    # failed-candidate fixture is therefore exposed as python3 here; unlike the
    # shared runner test, no good successor is needed because the framework
    # runner is the intended fallback.
    shutil.copy2(fixture_dir / "stderr-python.cmd",
                 candidate_dir / "python3.cmd")
    env = dict(os.environ)
    env["PATH"] = str(candidate_dir) + os.pathsep + env.get("PATH", "")

    completed = subprocess.run(
        fallback, shell=True, cwd=tmp_path,
        env=env, capture_output=True, text=True, timeout=60)

    assert completed.returncode == 0
    assert "hookSpecificOutput" in completed.stdout
    assert "non-zero status" in completed.stdout
    assert "Resolve-MdllmPython" in payload
    assert "-TimeoutSeconds 10" in payload
    assert "'-ExecutionPolicy', 'Bypass', '-File', $runner" in payload
    assert "$executable = $hostExecutable" in payload
    assert "$PSNativeCommandUseErrorActionPreference = $false" in payload
    assert payload.count("harness-event codex post-write") == 1
    assert "finally { exit 0 }" in payload
    assert windows.endswith('&exit /b 0"')


def test_session_start_order_is_inside_one_command_handler():
    handler = _rendered()["hooks"]["SessionStart"][0]["hooks"][0]
    for command in (handler["command"],
                    _windows_payload(handler["commandWindows"])):
        assert command.count("harness-event codex session-start") == 1
        assert "estate-sync" not in command
        assert "sha256:" in command
    assert tuple(step.operation for step in
                 CTX.binding("session-start").steps) == (
                     "estate-sync", "session-start")
    # No second command handler exists for Codex to launch concurrently.
    assert len(_rendered()["hooks"]["SessionStart"][0]["hooks"]) == 1


def test_post_write_translates_failure_to_codex_json_feedback():
    handler = _rendered()["hooks"]["PostToolUse"][0]["hooks"][0]
    posix = handler["command"]
    windows = _windows_payload(handler["commandWindows"])
    assert "harness-event codex post-write" in posix
    assert "harness-event codex post-write" in windows
    assert "validate" not in posix
    assert "sha256:" in posix and "sha256:" in windows
    assert posix.rstrip().endswith("exit 0")
    assert "exit 0" in windows


def test_output_translation_is_structured_and_post_write_is_quiet_on_pass():
    startup = json.loads(CODEX.format_lifecycle_output(
        "session-start", "orientation", True))
    assert startup == {"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "orientation",
    }}
    assert CODEX.format_lifecycle_output("post-write", "", True) == ""
    failure = json.loads(CODEX.format_lifecycle_output(
        "post-write", "validation failed", False))
    assert failure["hookSpecificOutput"] == {
        "hookEventName": "PostToolUse",
        "additionalContext": "validation failed",
    }


def test_probe_hashes_match_the_literals_baked_into_each_handler(tmp_path):
    config = _rendered()
    probe = CODEX.probe(tmp_path, CTX)
    assert probe.trust == "unknown"
    assert "/hooks" in " ".join(probe.remediations)
    assert set(probe.definition_hashes) == {"session-start", "post-write"}
    assert probe.definition_hashes["session-start"] != \
        probe.definition_hashes["post-write"]
    for moment, event in (
            ("session-start", "SessionStart"),
            ("post-write", "PostToolUse")):
        handler = config["hooks"][event][0]["hooks"][0]
        expected = probe.definition_hashes[moment]
        assert expected in handler["command"]
        assert expected in _windows_payload(handler["commandWindows"])


def test_definition_hash_includes_ordered_inward_binding_semantics(tmp_path):
    changed_bindings = tuple(
        replace(binding, steps=tuple(reversed(binding.steps)))
        if binding.moment == "session-start" else binding
        for binding in CTX.bindings
    )
    changed = HarnessContext(
        framework_root_rel=CTX.framework_root_rel,
        bindings=changed_bindings,
    )

    original_probe = CODEX.probe(tmp_path, CTX)
    changed_probe = CODEX.probe(tmp_path, changed)

    assert original_probe.definition_hashes["session-start"] != \
        changed_probe.definition_hashes["session-start"]
    assert original_probe.definition_hashes["post-write"] == \
        changed_probe.definition_hashes["post-write"]
    changed_config = json.loads(
        CODEX.render(changed)[HOOKS_PATH].decode("utf-8"))
    changed_command = changed_config["hooks"]["SessionStart"][0]["hooks"][0][
        "command"]
    assert changed_probe.definition_hashes["session-start"] in changed_command


def test_inspect_absent_reports_both_project_sources_without_writing(tmp_path):
    report = CODEX.inspect(tmp_path, CTX)
    assert report.harness == "codex"
    assert len(report.fragments) == 2
    for fragment in report.fragments:
        assert not fragment.artifact_present
        assert not fragment.present
        assert fragment.current is None
    assert not list(tmp_path.rglob("*"))


def test_inspect_current_is_format_insensitive_and_preserves_operator_data(
        tmp_path):
    config = _rendered()
    config["owner-note"] = {"keep": "byte-for-byte"}
    _write_json(tmp_path, config)
    before = (tmp_path / HOOKS_PATH).read_bytes()

    report = CODEX.inspect(tmp_path, CTX)

    fragment = _fragment(report, HOOKS_PATH)
    assert fragment.present and fragment.valid and fragment.current
    assert fragment.intents_realised == {
        "session-start": ("estate-sync", "session-start"),
        "post-write": ("validate",),
    }
    assert "top-level key 'owner-note' is operator-owned" in \
        report.operator_owned
    assert not report.findings
    assert (tmp_path / HOOKS_PATH).read_bytes() == before


@pytest.mark.parametrize("mutation", [
    "matcher", "posix-command", "windows-command", "timeout",
])
def test_inspect_detects_stale_managed_fields(tmp_path, mutation):
    config = _rendered()
    group = config["hooks"]["SessionStart"][0]
    handler = group["hooks"][0]
    if mutation == "matcher":
        group["matcher"] = "startup"
    elif mutation == "posix-command":
        handler["command"] += " --changed"
    elif mutation == "windows-command":
        handler["commandWindows"] += " --changed"
    else:
        handler["timeout"] = 3
    _write_json(tmp_path, config)

    fragment = _fragment(CODEX.inspect(tmp_path, CTX), HOOKS_PATH)

    assert fragment.present and fragment.valid
    assert fragment.current is False
    assert fragment.issues


def test_inspect_reports_extensions_without_flattening_current_fragment(
        tmp_path):
    config = _rendered()
    config["hooks"]["SessionStart"][0]["hooks"][0][
        "statusMessage"] = "Operator-owned status"
    config["hooks"]["Stop"] = [{
        "hooks": [{"type": "command", "command": "echo operator"}],
    }]
    path = _write_json(tmp_path, config)
    before = path.read_bytes()

    report = CODEX.inspect(tmp_path, CTX)

    fragment = _fragment(report, HOOKS_PATH)
    assert fragment.current is True
    assert any("statusMessage" in item for item in report.extensions)
    assert any("Stop" in item for item in report.extensions)
    assert path.read_bytes() == before


def test_unknown_field_inside_managed_handler_is_conservatively_stale(
        tmp_path):
    config = _rendered()
    config["hooks"]["SessionStart"][0]["hooks"][0]["futureBehavior"] = True
    _write_json(tmp_path, config)

    fragment = _fragment(CODEX.inspect(tmp_path, CTX), HOOKS_PATH)

    assert fragment.current is False
    assert any("may change hook semantics" in issue
               for issue in fragment.issues)


def test_inspect_reports_duplicate_managed_group_as_ambiguous(tmp_path):
    config = _rendered()
    duplicate = json.loads(json.dumps(
        config["hooks"]["PostToolUse"][0]))
    config["hooks"]["PostToolUse"].append(duplicate)
    _write_json(tmp_path, config)

    report = CODEX.inspect(tmp_path, CTX)

    fragment = _fragment(report, HOOKS_PATH)
    assert fragment.current is False
    assert any("ambiguous" in item for item in report.findings)


def test_inspect_rejects_duplicate_json_keys_at_any_depth(tmp_path):
    rendered = CODEX.render(CTX)[HOOKS_PATH].decode("utf-8")
    duplicate = rendered.replace(
        '"timeout": 120,', '"timeout": 1,\n          "timeout": 120,', 1)
    path = tmp_path / HOOKS_PATH
    path.parent.mkdir(parents=True)
    path.write_text(duplicate, encoding="utf-8")

    fragment = _fragment(CODEX.inspect(tmp_path, CTX), HOOKS_PATH)

    assert fragment.valid is False
    assert "duplicate JSON key 'timeout'" in fragment.issues[0]


@pytest.mark.parametrize("value, expected_issue", [
    ("{ definitely-not-json", None),
    ({"hooks": []}, "hooks is not an object"),
    ({"hooks": {"SessionStart": "not-a-list"}}, "not a list"),
])
def test_inspect_reports_malformed_and_schema_invalid_json(
        tmp_path, value, expected_issue):
    path = tmp_path / HOOKS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value), encoding="utf-8")

    fragment = _fragment(CODEX.inspect(tmp_path, CTX), HOOKS_PATH)

    assert fragment.readable is True
    assert fragment.valid is False
    assert fragment.current is None
    if expected_issue:
        assert expected_issue in fragment.issues[0]


def test_inspect_reports_unreadable_shape_without_throwing(tmp_path):
    # A directory at the artifact path makes read_text fail portably.
    (tmp_path / HOOKS_PATH).mkdir(parents=True)

    fragment = _fragment(CODEX.inspect(tmp_path, CTX), HOOKS_PATH)

    assert fragment.readable is False
    assert fragment.valid is None
    assert fragment.current is None


def test_inline_toml_is_an_active_unknown_currency_source(tmp_path):
    path = tmp_path / CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "[[hooks.SessionStart]]\n"
        'matcher = "startup|resume|clear|compact"\n\n'
        "[[hooks.SessionStart.hooks]]\n"
        'type = "command"\n'
        'command = "echo operator-managed-inline-hook"\n',
        encoding="utf-8",
    )

    report = CODEX.inspect(tmp_path, CTX)

    fragment = _fragment(report, CONFIG_PATH)
    assert fragment.present
    assert fragment.current is None
    assert any("config.toml" in item for item in report.findings)
    assert any("unknown" in item for item in report.findings)


def test_two_project_hook_sources_are_reported_as_ambiguous(tmp_path):
    _write_json(tmp_path, _rendered())
    config_path = tmp_path / CONFIG_PATH
    config_path.write_text(
        "[[hooks.PostToolUse]]\n"
        'matcher = "Edit|Write"\n\n'
        "[[hooks.PostToolUse.hooks]]\n"
        'type = "command"\n'
        'command = "echo second-source"\n',
        encoding="utf-8",
    )

    report = CODEX.inspect(tmp_path, CTX)

    assert all(fragment.present for fragment in report.fragments)
    assert any("both project hooks.json" in item
               for item in report.findings)


def test_malformed_inline_toml_is_invalid_not_an_exception(tmp_path):
    path = tmp_path / CONFIG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("[[hooks.SessionStart]\n", encoding="utf-8")

    report = CODEX.inspect(tmp_path, CTX)
    fragment = _fragment(report, CONFIG_PATH)

    assert fragment.readable is True
    assert fragment.valid is False
    assert fragment.current is None
    assert any("ownership cannot be ruled out" in item
               for item in report.findings)
