"""Phase 2A of vendor-harness-adapter-foundation: the draft ports vs the freeze.

Phase 2C update: the 2A draft implementations collapsed into the production
adapter (markdownllm/adapters/claude_code.py) — these tests now pin the
production renderer and inspector through the same port assertions the draft
had to satisfy, so the challenge evidence became the regression net.

What is proven here:
- the context object carries ENOUGH to reproduce the golden Claude bytes
  (rendering is derived from the lifecycle intents, not pasted);
- the inspect signature can report every estate shape read-only — standard,
  composite, locally extended, permissions-only, absent — without flattening
  extensions or touching operator-owned content;
- the drafted intents equal the Phase 0 freeze, byte for byte.

Run: python -m pytest tools/tests/test_harness_ports.py -q
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import harness_ports as hp  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"


# ------------------------------------------------------------ contract equality


def test_lifecycle_intents_match_the_phase0_freeze():
    import test_adapter_contract as frozen
    assert hp.LIFECYCLE_INTENTS == frozen.LIFECYCLE_INTENTS


# ------------------------------------------- draft renderer (test-local only)


from markdownllm.adapters.claude_code import ClaudeCodeAdapter  # noqa: E402

# Phase 2C collapsed the 2A/2B draft implementations into the production
# adapter; these tests now pin the production classes directly, so currency
# derives from the one real renderer (no expected-command duplicate).


def test_production_renderer_reproduces_the_golden_bytes(tmp_path):
    renderer = ClaudeCodeAdapter()
    assert isinstance(renderer, hp.RenderPort)
    ctx = hp.HarnessContext(framework_root_rel="../..")
    out = renderer.render(ctx)
    golden = (FIXTURES / "claude_golden" / "settings.json.golden").read_text(
        encoding="utf-8").replace("{rel_fw}", "../..")
    for binding in ctx.bindings:
        token = "{hash_" + binding.moment.replace("-", "_") + "}"
        golden = golden.replace(
            token, renderer._definition_hash(ctx, binding))
    assert out[".claude/settings.json"].decode("utf-8") == golden, \
        "the context object does not carry enough to derive the golden bytes"


# ------------------------------------------ draft inspector (test-local only)


def _inspect_shape(tmp_path, shape):
    if shape is not None:
        dst = tmp_path / ".claude" / "settings.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(
            (FIXTURES / "estate_shapes" / f"{shape}.json").read_bytes())
    inspector = ClaudeCodeAdapter()
    assert isinstance(inspector, hp.InspectPort)
    before = (hashlib.sha256(dst.read_bytes()).hexdigest()
              if shape is not None else None)
    report = inspector.inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))
    if shape is not None:
        assert hashlib.sha256(dst.read_bytes()).hexdigest() == before, \
            "inspection mutated the source document"
    return report


def test_inspect_standard_shape_is_recognised_legacy_not_current(tmp_path):
    """The live estate's scaffolded shape is legacy-v1, and says so.

    Before 5R.2 this fixture was the current form. It is now exactly the
    recognised historical one: two parallel SessionStart handlers calling
    the floor CLI directly, which never guaranteed the ordered binding.
    Reporting it `current` would certify disproved behaviour; reporting it
    merely stale would lose the certainty a later, explicitly authorised
    migration needs.
    """
    r = _inspect_shape(tmp_path, "hooks-only")
    frag = r.fragments[0]
    assert frag.present and frag.readable and frag.valid
    assert frag.current is False
    assert frag.legacy_id == "legacy-v1"
    assert not r.extensions and not r.operator_owned


def test_inspect_extended_startup_reports_not_flattens(tmp_path):
    """Legacy bytes PLUS a local extension is mixed ownership: no legacy id.

    The extension is still reported rather than flattened, but recognition
    is withheld — inferring a migration over an operator's own edit is the
    one thing the refusal rule exists to prevent.
    """
    r = _inspect_shape(tmp_path, "extended-startup")
    frag = r.fragments[0]
    assert frag.present and frag.current is False
    assert frag.legacy_id is None, "mixed ownership must not be recognised"
    assert any("--assistant" in e for e in r.extensions)


def _mutated_standard(tmp_path, mutate):
    import json as _json
    src = _json.loads((FIXTURES / "estate_shapes" / "hooks-only.json")
                      .read_text(encoding="utf-8"))
    mutate(src)
    dst = tmp_path / ".claude" / "settings.json"
    dst.parent.mkdir(parents=True)
    dst.write_text(_json.dumps(src, indent=2) + "\n", encoding="utf-8")
    return ClaudeCodeAdapter().inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))


# v1.6 return item 3 — the four false-current/discovery regression cases.


def test_inspect_token_prefix_mutation_is_stale(tmp_path):
    # `--quiet` -> `--quietly` shares a prefix but is a DIFFERENT token: a
    # divergence, never an extension. Extensions exist only across a space.
    def mutate(src):
        g = src["hooks"]["PostToolUse"][0]["hooks"][0]
        g["command"] = g["command"].replace("--quiet", "--quietly")
    r = _mutated_standard(tmp_path, mutate)
    frag = r.fragments[0]
    assert frag.present and frag.current is False and frag.issues
    assert not any("--quietly" in e for e in r.extensions)


def test_inspect_extra_command_in_managed_group_is_stale(tmp_path):
    # An appended command INSIDE the managed group changes what the managed
    # moment does — exact hook counts, not zip-truncation.
    def mutate(src):
        src["hooks"]["PostToolUse"][0]["hooks"].append(
            {"type": "command", "command": "python ../../tools/mdllm.py "
                                           "coherence . --quiet"})
    r = _mutated_standard(tmp_path, mutate)
    frag = r.fragments[0]
    assert frag.present and frag.current is False
    assert any("count diverges" in i for i in frag.issues)


def test_inspect_changed_managed_hook_fields_are_stale(tmp_path):
    # Currency covers the complete renderer-owned entry.  Keeping the command
    # while changing its hook type cannot be accepted as an executable floor.
    def mutate(src):
        hook = src["hooks"]["PostToolUse"][0]["hooks"][0]
        hook["type"] = "prompt"
        hook["timeout"] = 30
    r = _mutated_standard(tmp_path, mutate)
    frag = r.fragments[0]
    assert frag.present and frag.current is False
    assert any("managed hook fields diverge" in i for i in frag.issues)


def test_inspect_duplicate_json_keys_are_invalid_not_current(tmp_path):
    adapter = ClaudeCodeAdapter()
    ctx = hp.HarnessContext(framework_root_rel="../..")
    settings_path = ".claude/settings.json"
    desired = json.loads(
        adapter.render(ctx)[settings_path].decode("utf-8"))
    path = tmp_path / settings_path
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"hooks": {}, "hooks": '
        + json.dumps(desired["hooks"])
        + '}\n',
        encoding="utf-8",
    )

    report = adapter.inspect(tmp_path, ctx)
    fragment = report.fragments[0]
    assert fragment.artifact_present and fragment.readable is True
    assert fragment.valid is False
    assert fragment.present is False and fragment.current is None
    assert any("duplicate JSON key 'hooks'" in issue
               for issue in fragment.issues)


def test_inspect_duplicate_managed_matcher_is_ambiguous(tmp_path):
    # A second group repeating the managed matcher must be a finding, and the
    # FIRST group's inspection must survive — never a silent overwrite.
    def mutate(src):
        src["hooks"]["PostToolUse"].append(
            {"matcher": "Write|Edit",
             "hooks": [{"type": "command", "command": "echo shadowed"}]})
    r = _mutated_standard(tmp_path, mutate)
    frag = r.fragments[0]
    assert frag.present
    assert frag.intents_realised["post-write"] == ("validate",)  # first wins
    assert any("ambiguous" in f for f in r.findings)
    assert frag.current is False  # ambiguity is not a current state


def test_inspect_operator_only_hooks_have_no_managed_fragment(tmp_path):
    # A config whose hooks are ALL operator-owned events carries no managed
    # fragment: present must be False, not bool(hooks).
    def mutate(src):
        src["hooks"] = {"PreToolUse": [
            {"matcher": "Bash", "hooks": [
                {"type": "command", "command": "echo operator"}]}]}
    r = _mutated_standard(tmp_path, mutate)
    frag = r.fragments[0]
    assert frag.artifact_present and frag.valid
    assert frag.present is False and frag.current is None
    assert any("PreToolUse" in e for e in r.extensions)


def test_inspect_wrong_framework_path_is_stale(tmp_path):
    # 2C constraint closing a draft gap: a config whose commands point at a
    # DIFFERENT framework path realises the same operations but is NOT
    # current — currency comes from the renderer's exact managed form.
    import json as _json
    src = _json.loads((FIXTURES / "estate_shapes" / "hooks-only.json")
                      .read_text(encoding="utf-8"))
    for group in src["hooks"]["SessionStart"] + src["hooks"]["PostToolUse"]:
        for h in group["hooks"]:
            h["command"] = h["command"].replace("../../tools/mdllm.py",
                                                "../../../elsewhere/mdllm.py")
    dst = tmp_path / ".claude" / "settings.json"
    dst.parent.mkdir(parents=True)
    dst.write_text(_json.dumps(src, indent=2) + "\n", encoding="utf-8")
    r = ClaudeCodeAdapter().inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))
    frag = r.fragments[0]
    assert frag.present and frag.valid
    assert frag.current is False
    assert frag.issues


def test_inspect_composite_preserves_operator_content(tmp_path):
    r = _inspect_shape(tmp_path, "permissions-plus-hooks")
    assert r.fragments[0].present
    assert any("permissions" in o for o in r.operator_owned)


def test_inspect_permissions_only(tmp_path):
    r = _inspect_shape(tmp_path, "permissions-only")
    assert not r.fragments[0].present
    assert any("permissions" in o for o in r.operator_owned)


def test_inspect_absent(tmp_path):
    r = _inspect_shape(tmp_path, None)
    assert not r.fragments[0].present


def test_inspect_malformed_returns_invalid_report(tmp_path):
    dst = tmp_path / ".claude" / "settings.json"
    dst.parent.mkdir(parents=True)
    dst.write_text("{not-json", encoding="utf-8")
    r = ClaudeCodeAdapter().inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))
    frag = r.fragments[0]
    assert frag.artifact_present and not frag.present
    assert frag.readable and frag.valid is False
    assert frag.current is None and frag.issues


def test_inspect_schema_invalid_returns_invalid_report(tmp_path):
    dst = tmp_path / ".claude" / "settings.json"
    dst.parent.mkdir(parents=True)
    dst.write_text('{"hooks": []}', encoding="utf-8")
    r = ClaudeCodeAdapter().inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))
    frag = r.fragments[0]
    assert frag.artifact_present and not frag.present
    assert frag.readable and frag.valid is False
    assert frag.current is None and frag.issues


def test_inspect_unreadable_returns_unreadable_report(tmp_path, monkeypatch):
    dst = tmp_path / ".claude" / "settings.json"
    dst.parent.mkdir(parents=True)
    dst.write_text("{}", encoding="utf-8")
    original = Path.read_text

    def denied(path, *args, **kwargs):
        if path == dst:
            raise PermissionError("probe")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", denied)
    r = ClaudeCodeAdapter().inspect(
        tmp_path, hp.HarnessContext(framework_root_rel="../.."))
    frag = r.fragments[0]
    assert frag.artifact_present and not frag.present
    assert frag.readable is False
    assert frag.valid is None and frag.current is None and frag.issues


def test_lifecycle_bindings_own_arguments_delivery_and_order():
    start = hp.HarnessContext("../..").binding("session-start")
    assert tuple(step.operation for step in start.steps) == \
        ("estate-sync", "session-start")
    assert all(step.argv == (hp.DOMAIN_ROOT_ARG,) for step in start.steps)
    assert tuple(step.timeout_seconds for step in start.steps) == (75, 25)
    assert start.total_timeout_seconds == 105
    assert start.runner_reserve_seconds == 5
    assert start.delivery == "context"

    write = hp.HarnessContext("../..").binding("post-write")
    assert write.steps == (hp.LifecycleStep(
        "validate", (hp.DOMAIN_ROOT_ARG, "--quiet"),
        timeout_seconds=100),)
    assert write.delivery == "feedback"
    assert start.failure == write.failure == "surface-and-continue"


def test_render_context_is_immutable_and_host_independent():
    first = hp.HarnessContext(framework_root_rel="../..")
    second = hp.HarnessContext(framework_root_rel="../..")
    assert ClaudeCodeAdapter().render(first) == \
        ClaudeCodeAdapter().render(second)
    try:
        first.framework_root_rel = "C:/machine-specific"
        raise AssertionError("frozen render context accepted mutation")
    except (AttributeError, TypeError):
        pass


# ----------------------------------------------------- vendor-neutral boundary


def test_ports_module_names_no_vendor_config():
    # The contract module may mention vendors only in prose examples; it must
    # contain no vendor config path, key, or schema assumption as CODE.
    src = Path(hp.__file__).read_text(encoding="utf-8")
    code_lines = [l for l in src.splitlines()
                  if l.strip() and not l.strip().startswith("#")
                  and '"""' not in l and "'''" not in l]
    joined = "\n".join(code_lines)
    for token in (".claude", "settings.json", "SessionStart", "PostToolUse",
                  ".codex", "hooks.json"):
        assert token not in joined, f"vendor artifact {token!r} leaked into " \
                                    "the application contract"
