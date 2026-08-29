"""Phase 2b: the dispatch launch surface (`mdllm dispatch-payload`).

The composition half of the dispatcher — the corpus writes the launch text,
the scheduler merely carries it (`dispatch-host-design-2026-08-29`). Pinned
here:

- the payload EMITS the standing prompt's text, never a path to it, with an
  integrity trailer, so a channel that truncates is detectable in-context;
- `scope` is honoured: a scoped run says so and names its repos; an unscoped
  one declares the estate walk;
- a launch missing its stop condition or its launch context is REFUSED at
  composition, not discovered a hundred turns later inside the run;
- a scope that is not a repository is a launch typo, and fails here;
- the command WRITES NOTHING — it is a pure composition surface, safe inside
  a shell substitution on any host;
- every input the standing prompt declares is one this composer supplies, so
  a future input cannot be added to the prompt and silently go unsupplied.

Run: python -m pytest tools/tests/test_dispatch_payload.py -q
"""

import argparse
import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm.dispatch_payload import (  # noqa: E402
    DISPATCH_PROMPT_RELATIVE, DispatchPayloadRefused, build_launch,
    compose_payload, declared_input_names, read_dispatch_prompt, resolve_scope,
)

FRAMEWORK_ROOT = Path(__file__).resolve().parents[2]

pytestmark = pytest.mark.unit


def _args(path, **kw):
    defaults = dict(path=str(path), scope=None, stop_condition=None,
                    launch_context=None)
    defaults.update(kw)
    return argparse.Namespace(**defaults)


def _fake_estate(root: Path, prompt_body: str | None = None) -> Path:
    """A minimal estate: the prompt at its real relative path, one repo."""
    prompt = root / DISPATCH_PROMPT_RELATIVE
    prompt.parent.mkdir(parents=True, exist_ok=True)
    prompt.write_text(prompt_body if prompt_body is not None else (
        "---\n"
        "id: dispatch-loop\n"
        "type: prompt\n"
        "inputs:\n"
        "  - name: estate-root\n"
        "    description: the root\n"
        "  - name: scope\n"
        "    description: which repos\n"
        "  - name: stop-condition\n"
        "    description: the exogenous stop\n"
        "  - name: launch-context\n"
        "    description: who ticked\n"
        "---\n\n"
        "# Dispatch Loop\n\nWALK THE REPOS.\n"), encoding="utf-8")
    repo = root / "domain" / "pilot"
    (repo / ".git").mkdir(parents=True, exist_ok=True)
    return repo


# ------------------------------------------------------------- composition


def test_payload_emits_the_prompt_text_and_an_integrity_trailer(tmp_path,
                                                                capsys):
    _fake_estate(tmp_path)
    rc = mdllm.cmd_dispatch_payload(_args(
        tmp_path, stop_condition="one repo, then stop",
        launch_context="job pilot-dispatch, daily 07:00"))
    out = capsys.readouterr().out
    assert rc == 0
    # Emit, never point: the prompt's own text is in the payload.
    assert "WALK THE REPOS." in out
    # Frontmatter travels too — dispatch_guards is operative, not metadata.
    assert "id: dispatch-loop" in out
    prompt_text = (tmp_path / DISPATCH_PROMPT_RELATIVE).read_text(
        encoding="utf-8")
    digest = hashlib.sha256(
        prompt_text.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:12]
    assert f"sha256 {digest}" in out
    assert "emitted whole" in out
    # The launch facts are resolved into the text, not left as placeholders.
    assert "one repo, then stop" in out
    assert "job pilot-dispatch, daily 07:00" in out


def test_scope_is_honoured_and_defaults_to_the_estate_walk(tmp_path, capsys):
    _fake_estate(tmp_path)
    mdllm.cmd_dispatch_payload(_args(
        tmp_path, scope=["domain/pilot"], stop_condition="stop",
        launch_context="ctx"))
    scoped = capsys.readouterr().out
    assert "`domain/pilot`" in scoped
    assert "This run is **scoped**" in scoped
    assert "including the framework root" in scoped

    mdllm.cmd_dispatch_payload(_args(
        tmp_path, stop_condition="stop", launch_context="ctx"))
    estate = capsys.readouterr().out
    assert "the whole estate" in estate
    assert "This run is **scoped**" not in estate


def test_scope_renders_relative_to_the_estate_root(tmp_path):
    repo = _fake_estate(tmp_path)
    assert resolve_scope(tmp_path, [str(repo)]) == ("domain/pilot",)
    assert resolve_scope(tmp_path, ["domain/pilot"]) == ("domain/pilot",)
    assert resolve_scope(tmp_path, None) == ()


# ------------------------------------------------------------- refusals


@pytest.mark.parametrize("missing", ["stop_condition", "launch_context"])
def test_refuses_a_launch_missing_a_required_input(tmp_path, capsys, missing):
    _fake_estate(tmp_path)
    kw = {"stop_condition": "stop", "launch_context": "ctx"}
    kw[missing] = None
    rc = mdllm.cmd_dispatch_payload(_args(tmp_path, **kw))
    captured = capsys.readouterr()
    assert rc == 2
    # No payload at all — a refused launch must not be launchable by accident.
    assert captured.out.strip() == ""
    assert "refused this launch" in captured.err
    assert missing.replace("_", "-") in captured.err


def test_refuses_a_blank_stop_condition(tmp_path, capsys):
    _fake_estate(tmp_path)
    rc = mdllm.cmd_dispatch_payload(_args(
        tmp_path, stop_condition="   ", launch_context="ctx"))
    assert rc == 2
    assert capsys.readouterr().out.strip() == ""


def test_refuses_a_scope_that_is_not_a_repository(tmp_path, capsys):
    _fake_estate(tmp_path)
    (tmp_path / "not-a-repo").mkdir()
    rc = mdllm.cmd_dispatch_payload(_args(
        tmp_path, scope=["not-a-repo"], stop_condition="stop",
        launch_context="ctx"))
    err = capsys.readouterr().err
    assert rc == 2
    assert "not a git repository" in err

    rc = mdllm.cmd_dispatch_payload(_args(
        tmp_path, scope=["domain/absent"], stop_condition="stop",
        launch_context="ctx"))
    assert rc == 2
    assert "not a directory" in capsys.readouterr().err


def test_refuses_when_the_standing_prompt_is_missing(tmp_path, capsys):
    rc = mdllm.cmd_dispatch_payload(_args(
        tmp_path, stop_condition="stop", launch_context="ctx"))
    assert rc == 2
    assert "standing dispatch prompt is missing" in capsys.readouterr().err


def test_refuses_a_prompt_input_the_composer_cannot_supply(tmp_path):
    _fake_estate(tmp_path, prompt_body=(
        "---\nid: dispatch-loop\ninputs:\n"
        "  - name: stop-condition\n    description: s\n"
        "  - name: launch-context\n    description: c\n"
        "  - name: budget-ceiling\n    description: invented later\n"
        "---\n\n# Dispatch Loop\n"))
    meta, text = read_dispatch_prompt(tmp_path)
    launch = build_launch(tmp_path, scope=None, stop_condition="stop",
                          launch_context="ctx")
    with pytest.raises(DispatchPayloadRefused) as refusal:
        compose_payload(launch, meta, text)
    assert "budget-ceiling" in str(refusal.value)


# ------------------------------------------------------------- read-only


def _tree_fingerprint(root: Path) -> dict[str, str]:
    out = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            out[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()).hexdigest()
        else:
            out[path.relative_to(root).as_posix() + "/"] = "dir"
    return out


def test_the_command_writes_nothing(tmp_path, capsys):
    _fake_estate(tmp_path)
    before = _tree_fingerprint(tmp_path)
    for kw in ({"stop_condition": "stop", "launch_context": "ctx"},
               {"stop_condition": "stop", "launch_context": "ctx",
                "scope": ["domain/pilot"]},
               {"stop_condition": None, "launch_context": "ctx"}):
        mdllm.cmd_dispatch_payload(_args(tmp_path, **kw))
    capsys.readouterr()
    assert _tree_fingerprint(tmp_path) == before


# --------------------------------------------- against the real prompt file


def test_every_input_the_real_prompt_declares_is_supplied(capsys):
    # The contract test: a name added to the standing prompt's `inputs:` block
    # with no matching launch flag would otherwise ship a payload that
    # under-specifies the run. compose_payload refuses instead, and this pins
    # the framework's own prompt on the supplied side of that line.
    meta, text = read_dispatch_prompt(FRAMEWORK_ROOT)
    declared = declared_input_names(meta)
    assert "scope" in declared, "the scope input is the Phase 2b addition"
    launch = build_launch(FRAMEWORK_ROOT, scope=None,
                          stop_condition="marginal value exhausted",
                          launch_context="pilot job, daily")
    payload = compose_payload(launch, meta, text)
    assert text.rstrip("\n") in payload


def test_the_real_prompt_carries_the_phase_2b_guards():
    meta, _ = read_dispatch_prompt(FRAMEWORK_ROOT)
    guards = meta.get("dispatch_guards") or {}
    assert guards.get("dead_man") == "armed", "2b arms the dead-man"
    assert guards.get("claim") == "advisory-per-repo"
    assert guards.get("scope") == "declared-at-launch"


def test_dispatch_payload_is_registered_on_the_live_cli():
    parser = mdllm.build_cli()
    sub = next(a for a in parser._subparsers._group_actions)
    assert "dispatch-payload" in sub.choices
    args = parser.parse_args([
        "dispatch-payload", ".", "--scope", "domain/pilot",
        "--stop-condition", "queue drained", "--launch-context", "job x"])
    assert args.scope == ["domain/pilot"]
    assert args.stop_condition == "queue drained"
    assert args.launch_context == "job x"
    assert args.fn is mdllm.cmd_dispatch_payload
