"""Residual totality at definition and Git-path boundaries.

These tests pin the diagnostic distinction needed by a fail-closed publication
policy, clean command failures for malformed YAML definitions, and NUL-framed
candidate parsing for every Git-valid path byte.
"""

from __future__ import annotations

import subprocess
import sys
from argparse import Namespace
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import hook_contract
from markdownllm import scaffold as scaffold_mod  # noqa: E402
from markdownllm import cli as cli_mod  # noqa: E402
from markdownllm.doctor import cmd_doctor  # noqa: E402
from markdownllm.evals import cmd_eval  # noqa: E402
from markdownllm.kernel_gen import cmd_kernel  # noqa: E402
from markdownllm.refresh import cmd_refresh  # noqa: E402
from markdownllm.session import cmd_session_start  # noqa: E402
from markdownllm.sync import (  # noqa: E402
    PublicationPolicyState,
    _autopush_enabled,
    publication_policy,
)
from markdownllm.touchpoints import _parse_name_status_z  # noqa: E402
from markdownllm.yaml_loader import (  # noqa: E402
    load_version_sentinel,
    load_yaml_mapping,
)


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args], check=True,
        capture_output=True, text=True,
    )


def _repo(root: Path) -> Path:
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    return root


@pytest.mark.parametrize(
    ("frontmatter", "state", "enabled", "reason"),
    [
        ("git:\n  autopush: true\n", PublicationPolicyState.LITERAL_TRUE,
         True, "boolean true"),
        ("git:\n  autopush: false\n", PublicationPolicyState.LITERAL_FALSE,
         False, "boolean false"),
        ("git:\n  autocommit: true\n", PublicationPolicyState.ABSENT,
         False, "autopush is absent"),
        ("git:\n  autopush: 'true'\n", PublicationPolicyState.MALFORMED,
         False, "must be the YAML boolean"),
        ("git:\n  autopush: false\n  autopush: true\n",
         PublicationPolicyState.MALFORMED, False, "duplicate key 'autopush'"),
    ],
)
def test_publication_policy_retains_reason(
        tmp_path, frontmatter, state, enabled, reason):
    (tmp_path / "AGENTS.md").write_text(
        f"---\n{frontmatter}---\n\n# Domain\n", encoding="utf-8")

    policy = publication_policy(tmp_path)

    assert policy.state is state
    assert policy.enabled is enabled
    assert reason in policy.reason
    assert _autopush_enabled(tmp_path) is enabled


def test_publication_policy_distinguishes_absent_and_unreadable(tmp_path):
    absent = publication_policy(tmp_path)
    assert absent.state is PublicationPolicyState.ABSENT
    assert absent.enabled is False

    (tmp_path / "AGENTS.md").write_bytes(b"---\ngit:\n  autopush: true\n---\n\xff")
    unreadable = publication_policy(tmp_path)
    assert unreadable.state is PublicationPolicyState.UNREADABLE
    assert unreadable.enabled is False
    assert "UTF-8" in unreadable.reason


@pytest.mark.parametrize(
    ("frontmatter", "expected"),
    [
        ("git:\n  autopush: true\n", "autopush ENABLED"),
        ("git:\n  autopush: false\n", "autopush OFF — literal"),
        ("name: Domain\n", "autopush OFF — authority absent"),
        ("git:\n  autopush: 'true'\n", "autopush OFF — malformed"),
    ],
)
def test_doctor_explains_every_publication_policy_state(
        tmp_path, capsys, frontmatter, expected):
    root = _repo(tmp_path / "domain")
    (root / "AGENTS.md").write_text(
        f"---\n{frontmatter}---\n\n# Domain\n", encoding="utf-8")

    cmd_doctor(Namespace(path=str(root), harness=None))

    output = capsys.readouterr().out
    assert expected in output
    assert "Traceback" not in output


def _duplicate_sentinel(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    sentinel = root / ".markdownllm"
    sentinel.write_text(
        "version: 1.0.0\nversion: 2.0.0\nfoundational_specs: []\n",
        encoding="utf-8",
    )
    return sentinel


def test_doctor_reports_malformed_sentinel_without_traceback(tmp_path, capsys):
    root = _repo(tmp_path / "framework")
    _duplicate_sentinel(root)

    assert cmd_doctor(Namespace(path=str(root), harness=None)) == 1

    output = capsys.readouterr().out
    assert "framework sentinel invalid/unreadable" in output
    assert "duplicate key 'version'" in output
    assert "Traceback" not in output


def test_kernel_refuses_malformed_sentinel_cleanly(tmp_path):
    _duplicate_sentinel(tmp_path)
    with pytest.raises(SystemExit) as raised:
        cmd_kernel(SimpleNamespace(path=str(tmp_path), check=False))
    message = str(raised.value)
    assert "kernel refused invalid/unreadable" in message
    assert "duplicate key 'version'" in message


def test_kernel_refuses_non_list_foundational_catalog_cleanly(tmp_path):
    (tmp_path / ".markdownllm").write_text(
        "version: 1.0.0\nfoundational_specs: thing.md\n", encoding="utf-8")
    with pytest.raises(SystemExit) as raised:
        cmd_kernel(SimpleNamespace(path=str(tmp_path), check=False))
    assert "`foundational_specs` must be a list" in str(raised.value)


def test_refresh_refuses_malformed_sentinel_cleanly(tmp_path):
    framework = tmp_path / "framework"
    _duplicate_sentinel(framework)
    domain = tmp_path / "domain"
    domain.mkdir()
    (domain / "AGENTS.md").write_text(
        "---\nname: Domain\nframework_root: ../framework\n"
        "framework_version_seen: 1.0.0\n---\n\n# Domain\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as raised:
        cmd_refresh(SimpleNamespace(path=str(domain), seal=False))
    message = str(raised.value)
    assert "refresh refused invalid/unreadable" in message
    assert "duplicate key 'version'" in message


def test_session_start_refuses_malformed_sentinel_cleanly(tmp_path):
    _duplicate_sentinel(tmp_path)
    with pytest.raises(SystemExit) as raised:
        cmd_session_start(SimpleNamespace(path=str(tmp_path), contract=False))
    message = str(raised.value)
    assert "session-start refused invalid/unreadable" in message
    assert "duplicate key 'version'" in message


def test_scaffold_refuses_malformed_framework_sentinel_cleanly(
        tmp_path, monkeypatch):
    framework = tmp_path / "framework"
    _duplicate_sentinel(framework)
    fake_entry = framework / "tools" / "mdllm.py"
    fake_entry.parent.mkdir()
    fake_entry.write_text("# fake entry\n", encoding="utf-8")
    monkeypatch.setattr(hook_contract, "MDLLM_ENTRY", fake_entry)

    with pytest.raises(SystemExit) as raised:
        scaffold_mod.cmd_scaffold(SimpleNamespace(
            path=str(tmp_path / "new-domain"), harness="none",
            autopush="false"))
    message = str(raised.value)
    assert "scaffold refused invalid/unreadable" in message
    assert "duplicate key 'version'" in message


def test_eval_refuses_non_mapping_fixture_cleanly(tmp_path):
    fixture = tmp_path / "fixture.yaml"
    fixture.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

    with pytest.raises(SystemExit) as raised:
        cmd_eval(SimpleNamespace(
            path=str(tmp_path), report=False, fixture=str(fixture)))
    message = str(raised.value)
    assert "eval refused invalid fixture" in message
    assert "expected a YAML mapping" in message


def test_mapping_loader_rejects_scalar_and_sequence_roots():
    for source, text in (("scalar.yaml", "hello\n"),
                         ("sequence.yaml", "- one\n- two\n")):
        with pytest.raises(yaml.YAMLError) as raised:
            load_yaml_mapping(text, source=source)
        assert source in str(raised.value)
        assert "expected a YAML mapping" in str(raised.value)


@pytest.mark.parametrize("text", ["{}\n", "version:\n", "version: false\n"])
def test_version_sentinel_requires_non_empty_scalar_version(text):
    with pytest.raises(yaml.YAMLError) as raised:
        load_version_sentinel(text, source=".markdownllm")
    assert "requires a non-empty scalar `version`" in str(raised.value)


def test_cli_boundary_turns_uncaught_yaml_error_into_named_message(
        monkeypatch, capsys):
    class Parser:
        @staticmethod
        def parse_args():
            return SimpleNamespace(
                cmd="probe",
                fn=lambda _args: load_yaml_mapping(
                    "- not-a-mapping\n", source="probe.yaml"),
            )

    monkeypatch.setattr(cli_mod, "build_cli", lambda: Parser())

    assert cli_mod.main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "probe refused invalid YAML" in captured.err
    assert "probe.yaml" in captured.err
    assert "Traceback" not in captured.err


def test_name_status_z_parser_preserves_tabs_newlines_and_renames():
    modified = "things/tab\tand\nnewline.md"
    old = "things/old\tname\n.md"
    new = "things/new\nname\t.md"
    deleted = "things/deleted\n\t.md"
    raw = (b"M\0" + modified.encode() + b"\0R100\0" + old.encode()
           + b"\0" + new.encode() + b"\0D\0" + deleted.encode() + b"\0")

    assert _parse_name_status_z(raw) == [
        ("M", None, modified),
        ("R", old, new),
        ("D", deleted, deleted),
    ]


def test_candidates_use_nul_framed_name_status_in_real_git_repo(
        tmp_path, capsys):
    root = _repo(tmp_path / "domain")
    target = root / "definition.md"
    target.write_text(
        "---\nid: definition\ntype: specification\nstatus: draft\n"
        "created: 2026-08-20\n---\n\n# Definition\n",
        encoding="utf-8",
    )
    _git(root, "add", "definition.md")
    _git(root, "commit", "-q", "-m", "seed")
    target.write_text(target.read_text(encoding="utf-8") + "changed\n",
                      encoding="utf-8")
    _git(root, "add", "definition.md")

    from markdownllm.touchpoints import cmd_candidates
    assert cmd_candidates(Namespace(path=str(root), view="index")) == 0
    assert "cue: `definition`" in capsys.readouterr().out


def test_dependency_guidance_is_exactly_pinned():
    source = (Path(__file__).resolve().parents[1] / "markdownllm" / "model.py")
    text = source.read_text(encoding="utf-8")
    assert "python -m pip install PyYAML==6.0.3" in text
    assert "(pip install pyyaml)" not in text.lower()
