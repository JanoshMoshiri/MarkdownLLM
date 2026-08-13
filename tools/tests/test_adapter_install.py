"""Phase 5: conservative, byte-preserving adapter install/refresh."""

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.adapter_install import (  # noqa: E402
    AdapterInstallTarget,
    AtomicInstallError,
    InstallRefused,
    InstallStateChanged,
    TopLevelJsonFragmentPolicy,
    apply_install,
    preflight_install,
    target_for_adapter,
)
import markdownllm.adapter_install as install_module  # noqa: E402
from markdownllm.adapters.claude_code import (  # noqa: E402
    CLAUDE_CODE,
    SETTINGS_PATH,
)
from markdownllm.adapters.codex import (  # noqa: E402
    CODEX,
    CONFIG_PATH as CODEX_CONFIG_PATH,
    HOOKS_PATH as CODEX_HOOKS_PATH,
)
from markdownllm.harness_ports import (  # noqa: E402
    HarnessContext,
    InspectionReport,
    ManagedFragment,
)


FIXTURES = Path(__file__).parent / "fixtures" / "estate_shapes"
CTX = HarnessContext(framework_root_rel="../..")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _settings_path(root: Path) -> Path:
    return root / ".claude" / "settings.json"


def _put_shape(root: Path, shape: str) -> bytes:
    raw = (FIXTURES / f"{shape}.json").read_bytes()
    path = _settings_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return raw


def _claude_target(context: HarnessContext = CTX) -> AdapterInstallTarget:
    return target_for_adapter(CLAUDE_CODE, context)


def _codex_target() -> AdapterInstallTarget:
    return target_for_adapter(CODEX, CTX)


def test_absent_artifact_is_created_from_exact_renderer_bytes(tmp_path):
    plan = preflight_install(tmp_path, [_claude_target()])
    assert not plan.refused
    assert [(d.path, d.action) for d in plan.decisions] == [
        (SETTINGS_PATH, "create")]
    assert "+++ b/.claude/settings.json" in plan.owned_diff()

    result = apply_install(plan)

    assert result.written == (SETTINGS_PATH,)
    assert _settings_path(tmp_path).read_bytes() == (
        CLAUDE_CODE.render(CTX)[SETTINGS_PATH])


def test_permissions_only_merge_preserves_every_existing_byte(tmp_path):
    before = _put_shape(tmp_path, "permissions-only")
    # Split at the end of the final existing member.  A surgical merge must
    # leave both original slices exact and insert only between them.
    root_close = len(before.rstrip()) - 1
    member_end = root_close - 1
    while before[member_end] in b" \t\r\n":
        member_end -= 1
    prefix, suffix = before[:member_end + 1], before[member_end + 1:]
    prefix_hash, suffix_hash = _sha(prefix), _sha(suffix)

    plan = preflight_install(tmp_path, [_claude_target()])
    decision = plan.decisions[0]
    assert decision.action == "merge"
    assert not plan.refused
    assert decision.after is not None
    assert decision.after.startswith(prefix)
    assert decision.after.endswith(suffix)
    assert _sha(decision.after[:len(prefix)]) == prefix_hash
    assert _sha(decision.after[-len(suffix):]) == suffix_hash

    apply_install(plan)

    after = _settings_path(tmp_path).read_bytes()
    assert after == decision.after
    parsed = json.loads(after.decode("utf-8"))
    assert parsed["permissions"] == json.loads(before)["permissions"]
    report = CLAUDE_CODE.inspect(tmp_path, CTX)
    assert report.fragments[0].current is True
    assert any("permissions" in item for item in report.operator_owned)


@pytest.mark.parametrize("shape", ["hooks-only", "permissions-plus-hooks",
                                    "extended-startup"])
def test_legacy_and_locally_extended_artifacts_refuse_without_writing(
        tmp_path, shape):
    """Every live estate shape is now legacy — and a refusal writes nothing.

    Before 5R.2 these shapes were current, so a normal install was a no-op.
    They are now the recognised historical form (or that form plus a local
    extension), which under the migration contract reports availability and
    writes nothing: a legacy fragment is replaced only by an explicit,
    reviewed refresh, never as a side effect of a plain install.

    The safety invariant is unchanged and is what this test still guards:
    the artifact's hash must be byte-identical afterwards.
    """
    before = _put_shape(tmp_path, shape)
    before_hash = _sha(before)

    plan = preflight_install(tmp_path, [_claude_target()])

    assert plan.refused, "legacy state must never be silently overwritten"
    # The refusal is enforced at apply time, not merely advertised at
    # preflight: applying a refused plan raises, and writes nothing.
    with pytest.raises(install_module.InstallRefused):
        apply_install(plan)
    assert _sha(_settings_path(tmp_path).read_bytes()) == before_hash, \
        "a refusal must leave the operator's bytes untouched"


def test_explicit_legacy_refresh_replaces_only_owned_hooks_value(tmp_path):
    before = _put_shape(tmp_path, "permissions-plus-hooks")
    text = before.decode("utf-8")
    span = install_module._json_span_at_path(text, ("hooks",))
    prefix = before[:span.start]
    suffix = before[span.end:]

    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)

    assert not plan.refused
    decision = plan.decisions[0]
    assert decision.action == "refresh"
    assert decision.after is not None
    assert decision.after.startswith(prefix)
    assert decision.after.endswith(suffix)
    assert json.loads(decision.after)["permissions"] == \
        json.loads(before)["permissions"]

    apply_install(plan)
    assert _settings_path(tmp_path).read_bytes() == decision.after
    assert CLAUDE_CODE.inspect(tmp_path, CTX).fragments[0].current is True


def test_legacy_extension_refuses_even_under_explicit_refresh(tmp_path):
    before = _put_shape(tmp_path, "extended-startup")

    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)

    assert plan.refused
    assert plan.decisions[0].action == "refuse"
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert _settings_path(tmp_path).read_bytes() == before


def test_exact_root_powershell_legacy_is_separately_refreshable(tmp_path):
    context = HarnessContext(framework_root_rel=".")
    before = (Path(__file__).resolve().parents[2] / ".claude" /
              "settings.json").read_bytes()
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_bytes(before)

    report = CLAUDE_CODE.inspect(tmp_path, context)
    assert report.fragments[0].legacy_id == "legacy-root-powershell-v1"
    plan = preflight_install(
        tmp_path, [_claude_target(context)], refresh_legacy=True)

    assert not plan.refused
    assert plan.decisions[0].action == "refresh"
    assert json.loads(plan.decisions[0].after)["permissions"] == \
        json.loads(before)["permissions"]


def test_local_overlay_with_hooks_refuses_refresh_without_touching_either_file(
        tmp_path):
    primary = _put_shape(tmp_path, "hooks-only")
    overlay = tmp_path / ".claude" / "settings.local.json"
    overlay_bytes = b'{"hooks":{"SessionStart":[]},"operator":true}\n'
    overlay.write_bytes(overlay_bytes)

    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)

    assert plan.refused
    assert "settings.local.json" in plan.decisions[0].reason
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert _settings_path(tmp_path).read_bytes() == primary
    assert overlay.read_bytes() == overlay_bytes


def test_non_hook_local_overlay_remains_read_only_during_refresh(tmp_path):
    _put_shape(tmp_path, "hooks-only")
    overlay = tmp_path / ".claude" / "settings.local.json"
    overlay_bytes = b'{ "permissions" : { "allow" : ["Read"] } }\n'
    overlay.write_bytes(overlay_bytes)

    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)

    assert not plan.refused
    apply_install(plan)
    assert overlay.read_bytes() == overlay_bytes


def test_explicit_refresh_keeps_current_fragment_as_noop(tmp_path):
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    current = CLAUDE_CODE.render(CTX)[SETTINGS_PATH]
    path.write_bytes(current)

    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)

    assert not plan.refused
    assert plan.decisions[0].action == "no-op"
    assert apply_install(plan).unchanged == (SETTINGS_PATH,)
    assert path.read_bytes() == current


def test_refresh_refusal_blocks_other_selected_create(tmp_path):
    before = _put_shape(tmp_path, "extended-startup")
    other = _OtherAdapter()

    plan = preflight_install(
        tmp_path,
        [AdapterInstallTarget(other, CTX), _claude_target()],
        refresh_legacy=True,
    )

    assert [decision.action for decision in plan.decisions] == [
        "create", "refuse"]
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert not (tmp_path / ".other").exists()
    assert _settings_path(tmp_path).read_bytes() == before


def test_legacy_refresh_detects_concurrent_mutation_before_write(tmp_path):
    before = _put_shape(tmp_path, "hooks-only")
    plan = preflight_install(
        tmp_path, [_claude_target()], refresh_legacy=True)
    concurrent = before + b" "
    _settings_path(tmp_path).write_bytes(concurrent)

    with pytest.raises(InstallStateChanged):
        apply_install(plan)

    assert _settings_path(tmp_path).read_bytes() == concurrent


def test_invalid_artifact_refuses_with_diff_and_no_write(tmp_path):
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    before = b'{"permissions": true, "hooks": '
    path.write_bytes(before)

    plan = preflight_install(tmp_path, [_claude_target()])

    assert plan.refused
    assert plan.decisions[0].action == "refuse"
    assert plan.owned_diff() == ""
    assert "+++ b/.claude/settings.json" in plan.refusal_diff()
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert path.read_bytes() == before


def test_duplicate_managed_group_is_ambiguous_and_untouched(tmp_path):
    desired = json.loads(
        CLAUDE_CODE.render(CTX)[SETTINGS_PATH].decode("utf-8"))
    desired["hooks"]["PostToolUse"].append(
        desired["hooks"]["PostToolUse"][0])
    before = (json.dumps(desired, indent=2) + "\n").encode("utf-8")
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_bytes(before)

    plan = preflight_install(tmp_path, [_claude_target()])

    assert plan.refused
    assert plan.decisions[0].action == "refuse"
    assert "ambiguous" in plan.decisions[0].reason
    assert plan.owned_diff() == ""
    assert plan.refusal_diff()
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert _sha(path.read_bytes()) == _sha(before)


def test_duplicate_json_key_refuses_even_if_last_value_is_current(tmp_path):
    # json.loads (and therefore a vendor inspector) normally keeps only the
    # last duplicate key.  The mutation boundary must detect the ambiguity.
    rendered = CLAUDE_CODE.render(CTX)[SETTINGS_PATH]
    managed = rendered.decode("utf-8").strip()[1:-1].strip()
    before = ("{\n  \"hooks\": {},\n  " + managed + "\n}\n").encode()
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_bytes(before)

    plan = preflight_install(tmp_path, [_claude_target()])

    assert plan.refused
    assert "duplicate JSON key" in plan.decisions[0].reason
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert path.read_bytes() == before


def test_codex_operator_only_composite_receives_groups_losslessly(tmp_path):
    path = tmp_path / CODEX_HOOKS_PATH
    path.parent.mkdir(parents=True)
    before = (
        b'{\n  "operator-note" : { "spacing" : "must stay" },\n'
        b'  "hooks" : {\n    "Stop" : [ { "hooks" : [ '
        b'{ "type" : "command", "command" : "echo operator" } ] } ]\n'
        b'  },\n  "tail" : [ 1, 2, 3 ]\n}\n'
    )
    path.write_bytes(before)

    plan = preflight_install(tmp_path, [_codex_target()])

    assert not plan.refused
    decision = plan.decisions[0]
    assert decision.action == "merge"
    assert decision.after is not None
    for owned_bytes in (
            b'"operator-note" : { "spacing" : "must stay" }',
            b'"Stop" : [ { "hooks" : [ { "type" : "command", '
            b'"command" : "echo operator" } ] } ]',
            b'"tail" : [ 1, 2, 3 ]'):
        assert owned_bytes in decision.after
    parsed = json.loads(decision.after)
    assert parsed["hooks"]["Stop"] == json.loads(before)["hooks"]["Stop"]
    assert set(parsed["hooks"]) == {
        "Stop", "SessionStart", "PostToolUse"}

    apply_install(plan)

    assert path.read_bytes() == decision.after
    report = CODEX.inspect(tmp_path, CTX)
    fragment = next(f for f in report.fragments
                    if f.path == CODEX_HOOKS_PATH)
    assert fragment.current is True
    assert any("Stop" in extension for extension in report.extensions)


def test_codex_operator_groups_in_owned_event_arrays_are_preserved(tmp_path):
    path = tmp_path / CODEX_HOOKS_PATH
    path.parent.mkdir(parents=True)
    before = json.dumps({
        "hooks": {
            "SessionStart": [{
                "matcher": "operator-only-reason",
                "hooks": [{"type": "command", "command": "echo start"}],
            }],
            "PostToolUse": [{
                "matcher": "Bash",
                "hooks": [{"type": "command", "command": "echo post"}],
            }],
        },
        "operator": True,
    }, separators=(",", ":")).encode("utf-8")
    path.write_bytes(before)

    plan = preflight_install(tmp_path, [_codex_target()])

    assert not plan.refused and plan.decisions[0].action == "merge"
    after = plan.decisions[0].after
    assert after is not None
    parsed = json.loads(after)
    assert parsed["operator"] is True
    assert parsed["hooks"]["SessionStart"][0]["matcher"] == \
        "operator-only-reason"
    assert parsed["hooks"]["PostToolUse"][0]["matcher"] == "Bash"
    assert len(parsed["hooks"]["SessionStart"]) == 2
    assert len(parsed["hooks"]["PostToolUse"]) == 2


@pytest.mark.parametrize("alternate_shape", ["malformed", "unreadable"])
def test_codex_install_refuses_uninspectable_alternate_config(
        tmp_path, alternate_shape):
    alternate = tmp_path / CODEX_CONFIG_PATH
    alternate.parent.mkdir(parents=True)
    if alternate_shape == "malformed":
        alternate.write_text("[[hooks.SessionStart]\n", encoding="utf-8")
    else:
        alternate.mkdir()

    plan = preflight_install(tmp_path, [_codex_target()])

    assert plan.refused
    assert plan.decisions[0].action == "refuse"
    assert "config.toml" in plan.decisions[0].reason
    assert not (tmp_path / CODEX_HOOKS_PATH).exists()


def test_codex_stale_and_duplicate_managed_json_are_refused(tmp_path):
    path = tmp_path / CODEX_HOOKS_PATH
    path.parent.mkdir(parents=True)
    rendered = CODEX.render(CTX)[CODEX_HOOKS_PATH]
    stale = rendered.replace(b'"timeout": 120', b'"timeout": 7', 1)
    path.write_bytes(stale)
    stale_plan = preflight_install(tmp_path, [_codex_target()])
    assert stale_plan.refused
    assert path.read_bytes() == stale

    duplicate = rendered.replace(
        b'"timeout": 120,', b'"timeout": 1,\n          "timeout": 120,',
        1)
    path.write_bytes(duplicate)
    duplicate_plan = preflight_install(tmp_path, [_codex_target()])
    assert duplicate_plan.refused
    assert "duplicate JSON key" in duplicate_plan.decisions[0].reason
    assert path.read_bytes() == duplicate


class _OtherAdapter:
    name = "other-test-harness"
    relpath = ".other/hooks.json"
    payload = b'{"hooks": []}\n'

    def render(self, _context):
        return {self.relpath: self.payload}

    def inspect(self, domain_root, _context):
        path = domain_root / ".other" / "hooks.json"
        if not path.exists():
            fragment = ManagedFragment(
                path=self.relpath, present=False, artifact_present=False)
        else:
            exact = path.read_bytes() == self.payload
            fragment = ManagedFragment(
                path=self.relpath, present=True, readable=True, valid=True,
                current=exact)
        return InspectionReport(self.name, fragments=(fragment,))


def test_one_refusal_blocks_every_selected_adapter_before_any_write(tmp_path):
    # The first adapter is ready to create a file; the second is ambiguous.
    # All-selected preflight means apply writes neither.
    other = _OtherAdapter()
    invalid = _settings_path(tmp_path)
    invalid.parent.mkdir(parents=True)
    invalid.write_bytes(b'{"hooks": nope}')
    invalid_hash = _sha(invalid.read_bytes())

    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(other, CTX),
        _claude_target(),
    ])

    assert [d.action for d in plan.decisions] == ["create", "refuse"]
    assert plan.refused
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert not (tmp_path / ".other").exists()
    assert _sha(invalid.read_bytes()) == invalid_hash


def test_noop_changed_after_preflight_stops_before_other_writes(tmp_path):
    # Every selected input participates in the transaction, including no-ops.
    # Drift in the no-op must abort before the planned create is even staged.
    first = _OtherAdapter()
    exact = CLAUDE_CODE.render(CTX)[SETTINGS_PATH]
    path = _settings_path(tmp_path)
    path.parent.mkdir(parents=True)
    path.write_bytes(exact)
    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(first, CTX),
        _claude_target(),
    ])
    assert not plan.refused
    path.write_bytes(exact + b" ")

    other_path = tmp_path / ".other" / "hooks.json"
    with pytest.raises(InstallStateChanged):
        apply_install(plan)
    assert not other_path.parent.exists()


def _adapter(name: str, relpath: str, payload: bytes = b"managed\n"):
    adapter = _OtherAdapter()
    adapter.name = name
    adapter.relpath = relpath
    adapter.payload = payload
    return adapter


def test_portable_case_collision_is_ambiguous_before_write(tmp_path):
    upper = _adapter("upper", ".CODEX/hooks.json")
    lower = _adapter("lower", ".codex/hooks.json")

    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(upper, CTX),
        AdapterInstallTarget(lower, CTX),
    ])

    assert plan.refused
    assert [decision.action for decision in plan.decisions] == [
        "refuse", "refuse"]
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert not (tmp_path / ".codex").exists()


@pytest.mark.parametrize("relpath", [
    "C:AGENTS.md", "safe/file:stream", "CON", "safe/NUL.txt",
    "safe/trailing.", "safe/trailing ", "safe/*.json", "./safe.json",
    "safe//file.json",
])
def test_windows_drive_relative_and_colon_paths_refuse(tmp_path, relpath):
    unsafe = _adapter("unsafe", relpath)

    plan = preflight_install(
        tmp_path, [AdapterInstallTarget(unsafe, CTX)])

    assert plan.refused
    assert "project-relative" in plan.findings[0]
    with pytest.raises(InstallRefused):
        apply_install(plan)
    assert list(tmp_path.iterdir()) == []


def test_staging_failure_removes_only_new_empty_parent_dirs(
        tmp_path, monkeypatch):
    first = _adapter("first", ".first/deep/hooks.json")
    second = _adapter("second", ".second/hooks.json")
    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(first, CTX),
        AdapterInstallTarget(second, CTX),
    ])
    real_write = install_module._write_staged
    calls = 0

    def fail_second(path, payload, mode):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic staging failure")
        return real_write(path, payload, mode)

    monkeypatch.setattr(install_module, "_write_staged", fail_second)
    with pytest.raises(AtomicInstallError, match="could not stage"):
        apply_install(plan)

    assert not (tmp_path / ".first").exists()
    assert not (tmp_path / ".second").exists()


def test_apply_failure_rolls_back_and_removes_new_empty_parents(
        tmp_path, monkeypatch):
    first = _adapter("first", ".first/hooks.json")
    second = _adapter("second", ".second/hooks.json")
    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(first, CTX),
        AdapterInstallTarget(second, CTX),
    ])
    real_replace = install_module.os.replace
    calls = 0

    def fail_second(source, destination):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic replace failure")
        return real_replace(source, destination)

    monkeypatch.setattr(install_module.os, "replace", fail_second)
    with pytest.raises(AtomicInstallError, match="synthetic replace failure"):
        apply_install(plan)

    assert not (tmp_path / ".first").exists()
    assert not (tmp_path / ".second").exists()


def test_rollback_conflict_preserves_concurrent_bytes(
        tmp_path, monkeypatch):
    first = _adapter("first", ".first/hooks.json", b"first managed\n")
    second = _adapter("second", ".second/hooks.json", b"second managed\n")
    plan = preflight_install(tmp_path, [
        AdapterInstallTarget(first, CTX),
        AdapterInstallTarget(second, CTX),
    ])
    real_replace = install_module.os.replace
    calls = 0
    concurrent = b"concurrent operator bytes\n"

    def race_then_fail(source, destination):
        nonlocal calls
        calls += 1
        if calls == 1:
            real_replace(source, destination)
            Path(destination).write_bytes(concurrent)
            return
        raise OSError("synthetic later failure")

    monkeypatch.setattr(install_module.os, "replace", race_then_fail)
    with pytest.raises(AtomicInstallError, match="rollback failures"):
        apply_install(plan)

    assert (tmp_path / ".first" / "hooks.json").read_bytes() == concurrent
    assert not (tmp_path / ".second").exists()
