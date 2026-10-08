"""The commit gate — the ask, where the change lands
(the-verdict-is-asked-where-the-change-lands-2026-10-05; cue-carrier Phase 7).

A third lifecycle moment, `pre-commit`, with delivery `gate`: the Claude Code
adapter binds it to a PreToolUse hook on the shell tools; the sh carrier and
the runner pay for the floor only on a `git commit`; a refusal becomes the
harness's deny envelope and opens by naming the native prompt; a gate that
cannot run opens; the two older moments render byte-identical to before; and
the pre-gate two-moment projection is recognised as legacy so every seat can
refresh into the gated shape with a reviewed diff.

Run: python -m pytest tools/tests/test_commit_gate.py -q
"""

from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import harness_ports as hp  # noqa: E402
from markdownllm import lifecycle_runner as lr  # noqa: E402
from markdownllm.adapter_install import (  # noqa: E402
    apply_install, preflight_install, target_for_adapter)
from markdownllm.adapters.claude_code import CLAUDE_CODE, SETTINGS_PATH  # noqa: E402
from markdownllm.adapters.codex import CODEX, HOOKS_PATH  # noqa: E402
from markdownllm.adapters.project_hook_emission import (  # noqa: E402
    LEGACY_SH_RESOLVE_V2)
from markdownllm.hook_contract import SH_RESOLVE  # noqa: E402

CTX = hp.HarnessContext("../..")
TWO = hp.HarnessContext("../..", bindings=(
    CTX.binding("session-start"), CTX.binding("post-write")))
FW_ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------- the binding

def test_binding_is_declared_as_a_gate_on_the_staged_cue_question():
    gate = CTX.binding("pre-commit")
    assert gate.delivery == "gate"
    assert gate.steps == (hp.LifecycleStep(
        "cues", (hp.DOMAIN_ROOT_ARG, "--staged"),
        protected_seconds=100, protected_characters=1900),)
    assert gate.failure == "surface-and-continue"  # a gate that cannot run opens
    assert hp.LIFECYCLE_INTENTS["pre-commit"] == ("cues",)


# ------------------------------------------------------- the projection

def test_claude_renders_a_pretooluse_group_on_the_shell_tools():
    settings = json.loads(CLAUDE_CODE.render(CTX)[SETTINGS_PATH])
    groups = settings["hooks"]["PreToolUse"]
    assert len(groups) == 1 and groups[0]["matcher"] == "Bash|PowerShell"
    handlers = groups[0]["hooks"]
    assert len(handlers) == 1 and handlers[0]["timeout"] == 120
    cmd = handlers[0]["command"]
    assert "harness-event claude-code pre-commit " in cmd
    # The economy: read the hook input, exit 0 unless it looks like a commit,
    # pipe it on to the runner which decides for real.
    assert "MDLLM_HOOK_INPUT=$(cat)" in cmd
    assert 'case "$MDLLM_HOOK_INPUT" in *git*commit*) ;; *) exit 0 ;; esac' in cmd
    assert "printf '%s' \"$MDLLM_HOOK_INPUT\" | mdllm_python" in cmd
    # No floor: an empty line (allow), never a refusal.
    assert "printf '%s\\n' ''" in cmd
    assert "CLAUDE_PROJECT_DIR" in cmd


def test_the_two_older_moments_render_byte_identical_to_the_pre_gate_shape():
    gated = json.loads(CLAUDE_CODE.render(CTX)[SETTINGS_PATH])["hooks"]
    before = json.loads(CLAUDE_CODE.render(TWO)[SETTINGS_PATH])["hooks"]
    assert gated["SessionStart"] == before["SessionStart"]
    assert gated["PostToolUse"] == before["PostToolUse"]
    assert set(gated) == {"SessionStart", "PostToolUse", "PreToolUse"}
    assert set(before) == {"SessionStart", "PostToolUse"}


def test_capabilities_name_the_gate():
    assert CLAUDE_CODE.capabilities().lifecycle_moments == (
        "session-start", "post-write", "pre-commit")


# ------------------------------------------------------------ the envelope

def test_refusal_is_claudes_deny_envelope_and_names_the_native_prompt():
    out = CLAUDE_CODE.format_lifecycle_output("pre-commit", "the floor's text", False)
    hs = json.loads(out)["hookSpecificOutput"]
    assert hs["hookEventName"] == "PreToolUse"
    assert hs["permissionDecision"] == "deny"
    reason = hs["permissionDecisionReason"]
    assert reason.startswith("MarkdownLLM refused this commit")
    assert "walk is not on record" in reason
    assert "AskUserQuestion" in reason and "only for a touchpoint you may not settle" in reason
    assert reason.endswith("the floor's text")


def test_a_clean_gate_is_silence():
    assert CLAUDE_CODE.format_lifecycle_output("pre-commit", "clean", True) == ""


# -------------------------------------------------------------- the runner

def test_gate_applies_only_to_a_git_commit():
    def hook(command: str) -> str:
        return json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})

    assert lr.gate_applies(hook("git commit -m x"))
    assert lr.gate_applies(hook("git add -A && git commit -F msg.txt"))
    assert lr.gate_applies(hook("git -C domain/x commit -q -m y"))
    assert not lr.gate_applies(hook("git status"))
    assert not lr.gate_applies(hook("git log --oneline | grep commit"))
    assert not lr.gate_applies(hook("python tools/mdllm.py validate ."))
    assert not lr.gate_applies("")
    # Documented JSON without a shell command is not a commit.
    assert not lr.gate_applies(json.dumps({"tool_name": "Write",
                                           "tool_input": {"file_path": "x"}}))
    # A harness sending the command plain is still gated.
    assert lr.gate_applies("git commit -m plain")


class _Port:
    name = "fake-harness"

    def __init__(self):
        self.calls: list[tuple[str, bool]] = []

    def format_lifecycle_output(self, moment, text, passed):
        self.calls.append((moment, passed))
        return f"env:{moment}:{passed}"


def _execution(rc: int) -> lr.LifecycleExecution:
    step = lr.StepExecution(operation="cues", argv=(".", "--staged"),
                            returncode=rc, stdout="owed" if rc == 1 else "")
    return lr.LifecycleExecution(moment="pre-commit", steps=(step,),
                                 text=f"[steps: cues={rc}]\nowed",
                                 passed=(rc == 0))


def _dispatch(tmp_path, monkeypatch, capsys, *, stdin: str, rc: int):
    port = _Port()
    recorded = []
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin))
    monkeypatch.setattr(lr, "execute_lifecycle",
                        lambda root, binding: _execution(rc))
    monkeypatch.setattr(lr, "record_execution_attestation",
                        lambda *a, **kw: recorded.append(kw))
    code = lr.dispatch_lifecycle_event(
        tmp_path, CTX.binding("pre-commit"), harness="fake-harness",
        definition_hash="sha256:pinned", output_port=port)
    return code, port.calls, recorded, capsys.readouterr().out


def _commit_input() -> str:
    return json.dumps({"tool_name": "Bash",
                       "tool_input": {"command": "git add -A && git commit -m x"}})


def test_dispatch_is_silent_and_runs_nothing_for_a_call_the_gate_does_not_guard(
        tmp_path, monkeypatch, capsys):
    ran = []
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": "git status"}})))
    monkeypatch.setattr(lr, "execute_lifecycle",
                        lambda root, binding: ran.append(binding.moment))
    monkeypatch.setattr(lr, "record_execution_attestation",
                        lambda *a, **kw: ran.append("attested"))
    port = _Port()
    assert lr.dispatch_lifecycle_event(
        tmp_path, CTX.binding("pre-commit"), harness="fake-harness",
        definition_hash="sha256:pinned", output_port=port) == 0
    assert ran == [] and port.calls == []
    assert capsys.readouterr().out == ""


def test_dispatch_refuses_when_the_floor_owes_the_question(tmp_path, monkeypatch, capsys):
    code, calls, recorded, out = _dispatch(
        tmp_path, monkeypatch, capsys, stdin=_commit_input(), rc=1)
    assert code == 0  # the hook command itself always exits 0; the envelope refuses
    assert calls == [("pre-commit", False)]
    assert out.strip() == "env:pre-commit:False"
    # The gate ran as designed: a refusal is a passed gate, not a failed hook.
    assert recorded[0]["outcome"] == "passed"
    assert recorded[0]["detail"] == "cues=1"


def test_dispatch_opens_when_the_commit_carries_its_cue(tmp_path, monkeypatch, capsys):
    code, calls, recorded, out = _dispatch(
        tmp_path, monkeypatch, capsys, stdin=_commit_input(), rc=0)
    assert code == 0 and calls == [("pre-commit", True)]
    assert out.strip() == "env:pre-commit:True"
    assert recorded[0]["outcome"] == "passed"


def test_dispatch_opens_and_attests_failed_when_the_floor_cannot_run(
        tmp_path, monkeypatch, capsys):
    # A broken floor must not lock the repository: exit 2 (scan failure) or
    # 124 (timeout) opens the gate and leaves a failed attestation for doctor.
    for rc in (2, 124, 127):
        code, calls, recorded, out = _dispatch(
            tmp_path, monkeypatch, capsys, stdin=_commit_input(), rc=rc)
        assert code == 0 and calls == [("pre-commit", True)], rc
        assert recorded[0]["outcome"] == "failed", rc


# ------------------------------------------------- the other harnesses

def test_codex_binds_two_moments_and_stays_current_without_the_gate(tmp_path):
    assert CODEX.capabilities().lifecycle_moments == ("session-start", "post-write")
    rendered = CODEX.render(CTX)[HOOKS_PATH]
    assert b"pre-commit" not in rendered and b"PreToolUse" not in rendered
    dst = tmp_path / HOOKS_PATH
    dst.parent.mkdir(parents=True)
    dst.write_bytes(rendered)
    fragment = CODEX.inspect(tmp_path, CTX).fragments[0]
    assert fragment.current is True, fragment
    assert set(fragment.intents_realised) == {"session-start", "post-write"}


# ------------------------------------------------ legacy recognition (v2)

def test_resolve_fragment_v2_is_frozen_data():
    frozen = FW_ROOT / "tools/markdownllm/adapters/legacy/sh-resolve-v2.txt"
    assert frozen.is_file() and LEGACY_SH_RESOLVE_V2 == frozen.read_text(encoding="utf-8")
    assert "mdllm_python()" in LEGACY_SH_RESOLVE_V2


def test_legacy_two_moment_v2_projection_is_frozen_migration_input():
    # Exact bytes, like legacy-output-tail-v1 — recognition data must not
    # drift with the live renderer. Frozen the day the gate landed.
    expected = {
        ".": (5085, "a8097b910ba332b5a87b2f5476ce5c8b529c96c564736ab1232a6411da27c685"),
        "../..": (5093, "c34bfd114562b70db4a10a8b66b0a45146cda9a3069ca8dba4431662f014367c"),
    }
    for framework_root_rel, frozen in expected.items():
        definitions = CLAUDE_CODE.legacy_definitions(
            hp.HarnessContext(framework_root_rel=framework_root_rel))
        projection = next(item.owned_fragment for item in definitions
                          if item.legacy_id == "legacy-two-moment-v2")
        assert b"PreToolUse" not in projection
        assert (len(projection), hashlib.sha256(projection).hexdigest()) == frozen


def test_legacy_two_moment_v1_projection_is_frozen_migration_input():
    # The generation between output-tail-v1 and the existence guards: the v1
    # fragment with the full hash — what this repository's own seat carried
    # into the day the gate landed.
    expected = {
        ".": (4549, "221905e9697ac002f483608a67b4b7ce5157e80c5e51432098e9630fbbbd6a03"),
        "../..": (4557, "1780d9acc86b986fe170be361401dabb72183bfa6e8a092ffafa8f90b24a24c6"),
    }
    for framework_root_rel, frozen in expected.items():
        definitions = CLAUDE_CODE.legacy_definitions(
            hp.HarnessContext(framework_root_rel=framework_root_rel))
        projection = next(item.owned_fragment for item in definitions
                          if item.legacy_id == "legacy-two-moment-v1")
        assert b"PreToolUse" not in projection
        assert b"&& mdllm_probe" in projection  # the v1 fragment: no existence guard before the probe
        assert (len(projection), hashlib.sha256(projection).hexdigest()) == frozen


def test_v1_generation_seat_is_recognised_and_refreshes_into_the_gated_shape(tmp_path):
    definitions = CLAUDE_CODE.legacy_definitions(CTX)
    fragment_bytes = next(item.owned_fragment for item in definitions
                          if item.legacy_id == "legacy-two-moment-v1")
    dst = tmp_path / SETTINGS_PATH
    dst.parent.mkdir(parents=True)
    # An operator-owned top-level member beside the managed hooks, as the
    # framework root's own settings carry.
    installed = {"permissions": {"allow": ["Bash(git add *)"]}}
    installed.update(json.loads(fragment_bytes))
    dst.write_text(json.dumps(installed, indent=2) + "\n", encoding="utf-8")

    report = CLAUDE_CODE.inspect(tmp_path, CTX)
    fragment = report.fragments[0]
    assert fragment.present and fragment.current is False
    assert fragment.legacy_id == "legacy-two-moment-v1"
    assert any("permissions" in item for item in report.operator_owned)

    plan = preflight_install(
        tmp_path, [target_for_adapter(CLAUDE_CODE, CTX)], refresh_legacy=True)
    assert not plan.refused, plan.decisions
    assert [(d.path, d.action) for d in plan.decisions] == [(SETTINGS_PATH, "refresh")]
    apply_install(plan)
    after = json.loads(dst.read_text(encoding="utf-8"))
    assert after["permissions"] == {"allow": ["Bash(git add *)"]}  # untouched
    assert after["hooks"] == json.loads(CLAUDE_CODE.render(CTX)[SETTINGS_PATH])["hooks"]
    assert CLAUDE_CODE.inspect(tmp_path, CTX).fragments[0].current is True


def test_pre_gate_seat_is_recognised_and_refreshes_into_the_gated_shape(tmp_path):
    # Today LEGACY_SH_RESOLVE_V2 is the live fragment, so a two-binding render
    # IS the projection every seat carried until the gate.
    assert LEGACY_SH_RESOLVE_V2 == SH_RESOLVE
    dst = tmp_path / SETTINGS_PATH
    dst.parent.mkdir(parents=True)
    dst.write_bytes(CLAUDE_CODE.render(TWO)[SETTINGS_PATH])

    fragment = CLAUDE_CODE.inspect(tmp_path, CTX).fragments[0]
    assert fragment.present and fragment.current is False
    assert fragment.legacy_id == "legacy-two-moment-v2"

    target = target_for_adapter(CLAUDE_CODE, CTX)
    plain = preflight_install(tmp_path, [target])
    assert plain.refused, "a recognised legacy seat needs the explicit, reviewed refresh"
    plan = preflight_install(tmp_path, [target], refresh_legacy=True)
    assert not plan.refused
    assert [(d.path, d.action) for d in plan.decisions] == [(SETTINGS_PATH, "refresh")]
    apply_install(plan)
    assert dst.read_bytes() == CLAUDE_CODE.render(CTX)[SETTINGS_PATH]
    assert CLAUDE_CODE.inspect(tmp_path, CTX).fragments[0].current is True


# ---------------------------------------------------------------- the tick

def test_the_dispatch_tick_marks_its_launches_unattended():
    tick = (FW_ROOT / "tools/dispatch/tick.ps1").read_text(encoding="utf-8-sig")
    assert "$env:MDLLM_UNATTENDED = '1'" in tick


# ------------------------------------------------- the close's leg (Phase 3)
# The gate asks a `session-end:` commit a second question — has the close
# given the reckoning what it owes — without a second binding: the runner
# reads the subject where the command carries it and flags the step through
# the environment, so every seat's projection stays byte-identical.

_COMMIT = "git " + "commit"


def test_a_session_end_commit_is_recognised_where_its_subject_is_written(tmp_path):
    assert lr.is_session_end_commit(f'{_COMMIT} -m "session-end: 2026-10-08 — x"')
    assert lr.is_session_end_commit(f"git add -A && {_COMMIT} -qm 'session-end: x'")
    assert lr.is_session_end_commit(
        f"{_COMMIT} -m \"$(cat <<'EOF'\nsession-end: x\n\nbody\nEOF\n)\"")
    assert lr.is_session_end_commit(f"{_COMMIT} -m @'\nsession-end: x\n'@")
    (tmp_path / "msg.txt").write_text("\nsession-end: from a file\n", encoding="utf-8")
    assert lr.is_session_end_commit(f"{_COMMIT} -F msg.txt", tmp_path)
    assert lr.is_session_end_commit(f'{_COMMIT} -F "{tmp_path / "msg.txt"}"')
    (tmp_path / "other.txt").write_text("floor: x\n", encoding="utf-8")
    assert not lr.is_session_end_commit(f"{_COMMIT} --file=other.txt", tmp_path)
    assert not lr.is_session_end_commit(f'{_COMMIT} -m "fix: the session-end: line"')
    assert not lr.is_session_end_commit(f"{_COMMIT} -F missing.txt", tmp_path)


def test_dispatch_flags_a_session_end_commit_for_the_step(tmp_path, monkeypatch, capsys):
    from markdownllm.reckon import SESSION_END_ENV
    seen = []

    def run(root, binding):
        seen.append(lr.os.environ.get(SESSION_END_ENV))
        return _execution(0)

    monkeypatch.setattr(lr, "execute_lifecycle", run)
    monkeypatch.setattr(lr, "record_execution_attestation", lambda *a, **kw: None)
    monkeypatch.delenv(SESSION_END_ENV, raising=False)
    for command in (f'{_COMMIT} -m "session-end: x"', f"{_COMMIT} -m x"):
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": command}})))
        lr.dispatch_lifecycle_event(
            tmp_path, CTX.binding("pre-commit"), harness="fake-harness",
            definition_hash="sha256:pinned", output_port=_Port())
    capsys.readouterr()
    assert seen == ["1", None]
