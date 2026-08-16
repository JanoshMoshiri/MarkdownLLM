"""Phase 0 of vendor-harness-adapter-foundation: freeze the contract and evidence.

Three freezes, defined BEFORE any adapter class exists:

1. **Golden Claude artifacts** — the exact bytes the scaffold's Claude
   projection emits today (`fixtures/claude_golden/`). Phase 2C extraction
   must keep these byte-identical without editing the fixtures.
2. **Estate shapes** — the `.claude/settings.json` configurations that exist
   in the live estate (`fixtures/estate_shapes/`): hooks-only (the scaffolded
   standard), permissions-only, permissions-plus-hooks, a locally extended
   startup command, and absence. Doctor's *current* reading of each is pinned
   here so the Phase 2C inspect-port move cannot silently change it.
3. **Lifecycle intents** — the application contract as data. The intents name
   framework acts, never vendor events; how a harness guarantees the ordering
   is its adapter's problem. The legacy Claude settings preserve the command
   list but do not realise its order because matching handlers run in parallel.

Run: python -m pytest tools/tests/test_adapter_contract.py -q
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"

for _k in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_k, "floor-tests")
for _k in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_k, "floor-tests@local")


# ------------------------------------------------------------------ contract
# The minimal lifecycle intents already felt in production (plan: "Application
# contract"). Ordering is part of the intent — estate-sync must complete before
# session-start because orientation reads the git log, and the log is only
# whole after the fetch. `post-write` is advisory feedback; the git pre-commit
# hook remains the complete enforcement boundary and is NOT a harness intent.

LIFECYCLE_INTENTS = {
    "session-start": ("estate-sync", "session-start"),  # ordered, sequential
    "post-write": ("validate",),                        # advisory, quiet
}


def _ns(**kw):
    import argparse
    return argparse.Namespace(**kw)


def _git_repo(p: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


def _scaffold(tmp_path: Path, name: str = "adapter-baseline-probe") -> Path:
    _git_repo(tmp_path)
    target = tmp_path / name
    rc = mdllm.cmd_scaffold(_ns(path=str(target)))
    assert rc == 0
    return target


FW_ROOT = Path(mdllm.__file__).resolve().parents[1]  # tools/mdllm.py → repo root


def _rel_fw(target: Path) -> str:
    return Path(os.path.relpath(FW_ROOT, target)).as_posix()


# ------------------------------------------------- 1. golden Claude artifacts


def test_scaffold_settings_matches_golden(tmp_path):
    """The current golden freezes the projection's SHAPE.

    The definition hash is derived from the framework-relative path, so it
    cannot be a literal in a path-generic fixture. Substituting it from the
    adapter's own `_definition_hash` asserts the invariant that matters: an
    installed handler carries exactly the hash its renderer would produce,
    so an outdated handler can never mint current attestation evidence.
    """
    from markdownllm.adapters.claude_code import CLAUDE_CODE
    from markdownllm.harness_ports import HarnessContext

    target = _scaffold(tmp_path)
    rel_fw = _rel_fw(target)
    golden = (FIXTURES / "claude_golden" / "settings.json.golden").read_bytes()
    golden = golden.replace(b"{rel_fw}", rel_fw.encode("utf-8"))
    context = HarnessContext(framework_root_rel=rel_fw)
    for binding in context.bindings:
        token = ("{hash_" + binding.moment.replace("-", "_") + "}").encode()
        digest = CLAUDE_CODE._definition_hash(context, binding)
        assert token in golden, f"golden lost its {binding.moment} hash slot"
        golden = golden.replace(token, digest.encode("utf-8"))
    emitted = (target / ".claude" / "settings.json").read_bytes()
    assert emitted == golden, "Claude adapter bytes changed unexpectedly"


def test_legacy_v1_golden_is_frozen_migration_input():
    """The pre-5R.2 projection stays byte-immutable as recognition data.

    It is no longer the desired renderer output: Claude runs matching
    handlers in parallel, so its two SessionStart handlers never guaranteed
    the ordered binding. Phase 5R.3 recognises exactly these bytes to offer
    an operator-approved migration, which is only sound while they cannot
    drift.
    """
    legacy = (FIXTURES / "claude_golden" /
              "settings.json.legacy-v1.golden").read_text(encoding="utf-8")
    session = legacy.split('"SessionStart"')[1].split('"PostToolUse"')[0]
    assert session.count('"type": "command"') == 2, \
        "legacy-v1 is the TWO-handler shape; that is what makes it legacy"
    assert "{rel_fw}/tools/mdllm.py estate-sync ." in legacy
    assert "{rel_fw}/tools/mdllm.py session-start ." in legacy
    assert "harness-event" not in legacy, \
        "legacy-v1 predates the neutral runner; it calls the CLI directly"


def test_output_tail_legacy_projection_is_frozen_migration_input():
    """The 5R.5 tail-allocation projection is exact recognition data."""
    from markdownllm.adapters.claude_code import CLAUDE_CODE
    from markdownllm.harness_ports import HarnessContext

    expected = {
        ".": (4549,
              "b7af154f3f2c46db65901deea6c757a64576e056277a8c96b00d953bc6055489"),
        "../..": (4557,
                 "d673dfbf4d6cab47e7e7a1702b241f87bc5b6cbac5638c5ff7b1d487959bc14e"),
    }
    for framework_root_rel, frozen in expected.items():
        definitions = CLAUDE_CODE.legacy_definitions(
            HarnessContext(framework_root_rel=framework_root_rel))
        projection = next(
            item.owned_fragment for item in definitions
            if item.legacy_id == "legacy-output-tail-v1")
        assert (len(projection), hashlib.sha256(projection).hexdigest()) \
            == frozen


def test_scaffold_commands_are_template_copies(tmp_path):
    # One owner for repeated facts: the command files are copies of
    # templates/commands/*, byte-for-byte — the template is the golden.
    target = _scaffold(tmp_path)
    src_dir = FW_ROOT / "templates" / "commands"
    deployed = sorted((target / ".claude" / "commands").glob("*.md"))
    assert [p.name for p in deployed] == sorted(
        p.name for p in src_dir.glob("*.md"))
    for copy in deployed:
        assert copy.read_bytes() == (src_dir / copy.name).read_bytes()


def test_scaffold_completion_guidance_frozen(tmp_path, capsys):
    _scaffold(tmp_path)
    out = capsys.readouterr().out
    golden = (FIXTURES / "claude_golden" / "scaffold-guidance.golden").read_text(
        encoding="utf-8").rstrip("\r\n")
    emitted = next(line for line in out.splitlines()
                   if "hardened out of the box:" in line)
    assert emitted == golden


# --------------------------------------------------------- 2. estate shapes


def _domain_with_settings(tmp_path: Path, shape: str | None) -> Path:
    _git_repo(tmp_path)
    (tmp_path / "AGENTS.md").write_text(
        "---\nname: D\n---\n\n# D\n", encoding="utf-8")
    if shape is not None:
        src = FIXTURES / "estate_shapes" / f"{shape}.json"
        dst = tmp_path / ".claude" / "settings.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def test_estate_shape_fixtures_parse():
    shapes = sorted((FIXTURES / "estate_shapes").glob("*.json"))
    assert [p.stem for p in shapes] == [
        "extended-startup", "hooks-only", "permissions-only",
        "permissions-plus-hooks"]
    for p in shapes:
        json.loads(p.read_text(encoding="utf-8"))


def test_doctor_current_reading_of_each_shape(tmp_path, capsys):
    # Pins doctor's PRESENT behaviour (presence-as-capability, defect 2 of the
    # plan): any shape with a SessionStart key reports "installed", including
    # the locally extended one; permissions-only and absence report the opt-in
    # hint. Phase 3 replaces this vocabulary; until then it must not drift.
    expect = {
        "hooks-only": True,
        "permissions-only": False,
        "permissions-plus-hooks": True,
        "extended-startup": True,
        None: False,  # no settings file at all
    }
    for shape, installed in expect.items():
        d = tmp_path / (shape or "no-settings")
        d.mkdir()
        _domain_with_settings(d, shape)
        mdllm.cmd_doctor(_ns(path=str(d)))
        out = capsys.readouterr().out
        if installed:
            assert "SessionStart adapter installed" in out, shape
        else:
            assert "no SessionStart adapter" in out, shape


def test_extended_startup_shape_carries_local_extension():
    # The estate really contains this shape: the second SessionStart command
    # carries a domain-owned argument. Requirement 5 (merge, Phase 5) and the
    # Phase 2C inspect port must both see the extension, never flatten it.
    cfg = json.loads((FIXTURES / "estate_shapes" / "extended-startup.json")
                     .read_text(encoding="utf-8"))
    cmds = [h["command"] for g in cfg["hooks"]["SessionStart"] for h in g["hooks"]]
    assert cmds[1].endswith("session-start . --assistant")


# ------------------------------------------------------ 3. lifecycle intents


def _legacy_command_lists_in(settings: dict) -> dict:
    """Map legacy Claude settings back to their unordered command lists.

    This is deliberately the ONLY place a test knows the Claude JSON shape;
    it is byte/operation migration evidence, not an ordering proof. Current
    Claude runs matching handlers in parallel, including handlers in one group.
    """
    realised: dict = {}
    hooks = settings.get("hooks") or {}
    ss_groups = hooks.get("SessionStart") or []
    if ss_groups:
        assert len(ss_groups) == 1, "legacy-v1 shape has one matcher group"
        acts = []
        for h in ss_groups[0]["hooks"]:
            cmd = h["command"]
            assert "tools/mdllm.py" in cmd
            acts.append(cmd.split("tools/mdllm.py ")[1].split()[0])
        realised["session-start"] = tuple(acts)
    for g in hooks.get("PostToolUse") or []:
        if g.get("matcher") == "Write|Edit":
            acts = tuple(h["command"].split("tools/mdllm.py ")[1].split()[0]
                         for h in g["hooks"])
            realised["post-write"] = acts
    return realised


def test_scaffolded_settings_delegate_each_moment_to_the_neutral_runner(
        tmp_path):
    """A fresh scaffold emits ONE handler per moment, entering the runner.

    Claude launches matching handlers in parallel, so a per-step handler
    list cannot express an ordered binding at all. The ordering now lives
    where it always belonged — the application service — and the vendor
    schema carries a single delegating handler with an explicit timeout.
    """
    target = _scaffold(tmp_path)
    settings = json.loads((target / ".claude" / "settings.json")
                          .read_text(encoding="utf-8"))
    for event, moment in (("SessionStart", "session-start"),
                          ("PostToolUse", "post-write")):
        groups = settings["hooks"][event]
        assert len(groups) == 1
        handlers = groups[0]["hooks"]
        assert len(handlers) == 1, f"{event} must not fan out into handlers"
        command = handlers[0]["command"]
        assert f"harness-event claude-code {moment} " in command
        assert handlers[0]["timeout"] == 120, "never inherit a vendor default"
        # The ordered steps are the runner's business, not the schema's.
        for operation in LIFECYCLE_INTENTS[moment]:
            assert f"mdllm.py {operation} " not in command


def test_estate_standard_legacy_shape_preserves_lifecycle_command_lists():
    cfg = json.loads((FIXTURES / "estate_shapes" / "hooks-only.json")
                     .read_text(encoding="utf-8"))
    assert _legacy_command_lists_in(cfg) == LIFECYCLE_INTENTS
