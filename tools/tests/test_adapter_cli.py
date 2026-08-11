"""Integrated CLI contracts for harness diagnosis and safe installation.

These tests cross the argparse/application-service boundary while keeping all
adapter artifacts inside pytest temporary directories.  In particular, they
must never create or modify the repository's live ``.codex`` directory.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import cli  # noqa: E402
import markdownllm.doctor as doctor_module  # noqa: E402
from markdownllm.adapters.codex import CODEX, HOOKS_PATH  # noqa: E402
from markdownllm.harness_ports import HarnessContext  # noqa: E402
from markdownllm.harness_diagnostics import (  # noqa: E402
    record_execution_attestation,
)
from markdownllm.scaffold import MDLLM_ENTRY  # noqa: E402


def _run_cli(argv: list[str]) -> int:
    args = cli.build_cli().parse_args(argv)
    return args.fn(args)


def _context_for(root: Path) -> HarnessContext:
    framework_rel = Path(os.path.relpath(
        MDLLM_ENTRY.parents[1], root.resolve())).as_posix()
    return HarnessContext(framework_root_rel=framework_rel)


def _write_hooks(root: Path, raw: bytes) -> Path:
    path = root / HOOKS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def test_doctor_codex_reports_independent_facts_without_promoting_runtime(
        tmp_path, monkeypatch, capsys):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "AGENTS.md").write_text(
        "---\nname: adapter-cli-fixture\n---\n\n# Fixture\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(doctor_module, "runtime_probe", lambda *_: {
        "resolved": "fixture-floor-python",
        "command_executed": True,
        "candidates": [{
            "candidate": "fixture-floor-python",
            "interpreter_found": True,
            "dependency_loaded": True,
        }],
    })

    # The fixture intentionally has no Git pre-commit hook, so the overall
    # floor verdict is degraded.  Adapter facts remain independently visible.
    assert _run_cli([
        "doctor", str(tmp_path), "--harness", "codex",
    ]) == 1
    output = capsys.readouterr().out
    fact_lines = [line for line in output.splitlines()
                  if "harness codex/" in line]

    assert len(fact_lines) == 2
    assert any("codex/session-start" in line for line in fact_lines)
    assert any("codex/post-write" in line for line in fact_lines)
    for line in fact_lines:
        assert "support=supported" in line
        assert "configuration=absent" in line
        assert "currency=not-applicable" in line
        assert "trust=unknown" in line
        assert "runtime=command-runs" in line
        assert "execution=untested" in line
    assert "execution=passed" not in output
    assert "trust detail: Codex project trust" in output
    assert "runtime resolved: fixture-floor-python" in output
    assert "execution detail: current managed configuration is not " \
        "established" in output


def test_doctor_reports_inspected_operator_owned_project_data(
        tmp_path, monkeypatch, capsys):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "AGENTS.md").write_text(
        "---\nname: adapter-cli-owner-fixture\n---\n\n# Fixture\n",
        encoding="utf-8",
    )
    context = _context_for(tmp_path)
    config = CODEX.render(context)[HOOKS_PATH]
    parsed = json.loads(config)
    parsed["owner-note"] = {"keep": "operator bytes"}
    _write_hooks(
        tmp_path,
        (json.dumps(parsed, indent=2) + "\n").encode("utf-8"),
    )
    probe = CODEX.probe(tmp_path, context)
    for moment, definition_hash in probe.definition_hashes.items():
        record_execution_attestation(
            tmp_path, "codex", moment, definition_hash,
            outcome="passed", source="codex-project-hook",
            detail=f"{moment}=0",
        )
    monkeypatch.setattr(doctor_module, "runtime_probe", lambda *_: {
        "resolved": "fixture-floor-python",
        "command_executed": True,
        "candidates": [],
    })

    assert _run_cli([
        "doctor", str(tmp_path), "--harness", "codex",
    ]) == 1
    output = capsys.readouterr().out
    assert "operator-owned: top-level key 'owner-note' is operator-owned" \
        in output
    assert "execution=passed" in output
    assert "execution evidence: source=codex-project-hook; observed_at=" \
        in output
    assert "definition_current=true" in output
    assert "execution detail: session-start=0" in output


def test_codex_adapter_install_dry_run_is_no_write_then_apply_is_exact(
        tmp_path, capsys):
    artifact = tmp_path / HOOKS_PATH
    expected = CODEX.render(_context_for(tmp_path))[HOOKS_PATH]

    assert _run_cli([
        "adapter-install", str(tmp_path), "--harness", "codex",
        "--dry-run",
    ]) == 0
    dry_run_output = capsys.readouterr().out
    assert "CREATE" in dry_run_output
    assert "DRY RUN" in dry_run_output
    assert not artifact.exists()
    assert not (tmp_path / ".codex").exists()

    assert _run_cli([
        "adapter-install", str(tmp_path), "--harness", "codex",
    ]) == 0
    apply_output = capsys.readouterr().out
    assert "Applied: 1 written; 0 unchanged." in apply_output
    assert artifact.read_bytes() == expected


def test_codex_adapter_install_refuses_invalid_config_without_write(
        tmp_path, capsys):
    artifact = _write_hooks(tmp_path, b'{"hooks": definitely-not-json}\n')
    before = artifact.read_bytes()

    assert _run_cli([
        "adapter-install", str(tmp_path), "--harness", "codex",
    ]) == 1
    output = capsys.readouterr().out

    assert "REFUSE" in output
    assert "invalid" in output.lower()
    assert "no adapter artifact was written" in output
    assert artifact.read_bytes() == before


def test_codex_adapter_install_refuses_ambiguous_sources_without_write(
        tmp_path, capsys):
    hooks = _write_hooks(
        tmp_path, CODEX.render(_context_for(tmp_path))[HOOKS_PATH])
    config = tmp_path / ".codex" / "config.toml"
    config.write_text(
        "[[hooks.PostToolUse]]\n"
        'matcher = "Edit|Write"\n\n'
        "[[hooks.PostToolUse.hooks]]\n"
        'type = "command"\n'
        'command = "echo operator-owned-second-source"\n',
        encoding="utf-8",
    )
    hooks_before = hooks.read_bytes()
    config_before = config.read_bytes()

    assert _run_cli([
        "adapter-install", str(tmp_path), "--harness", "codex",
    ]) == 1
    output = capsys.readouterr().out

    assert "REFUSE" in output
    assert "ambiguous" in output.lower()
    assert "both project hooks.json" in output
    assert "no adapter artifact was written" in output
    assert hooks.read_bytes() == hooks_before
    assert config.read_bytes() == config_before


@pytest.mark.parametrize("argv", [
    ["doctor", "{target}", "--harness", "unknown-vendor"],
    ["adapter-install", "{target}", "--harness", "unknown-vendor"],
    ["scaffold", "{target}", "--harness", "unknown-vendor"],
])
def test_unknown_harness_selector_is_rejected_before_command_side_effects(
        tmp_path, argv):
    target = tmp_path / "must-not-exist"
    expanded = [str(target) if item == "{target}" else item for item in argv]

    with pytest.raises(SystemExit) as exc:
        cli.build_cli().parse_args(expanded)

    assert exc.value.code == 2
    assert not target.exists()
