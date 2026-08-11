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
   is its adapter's problem. The scaffolded Claude settings are asserted to
   *realise* these intents, which is the seam the Phase 2A ports must honour.

Run: python -m pytest tools/tests/test_adapter_contract.py -q
"""

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
    target = _scaffold(tmp_path)
    golden = (FIXTURES / "claude_golden" / "settings.json.golden").read_bytes()
    golden = golden.replace(b"{rel_fw}", _rel_fw(target).encode("utf-8"))
    emitted = (target / ".claude" / "settings.json").read_bytes()
    assert emitted == golden, "Claude adapter bytes changed — Phase 2C regression"


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


def _intents_realised_by(settings: dict) -> dict:
    """Map a Claude-format settings dict back to framework lifecycle intents.

    This is deliberately the ONLY place a test knows the Claude JSON shape;
    the assertion layer below speaks intent vocabulary. When the Phase 2A
    ports exist, this translation moves into the Claude adapter and this
    helper collapses to a call into it.
    """
    realised: dict = {}
    hooks = settings.get("hooks") or {}
    ss_groups = hooks.get("SessionStart") or []
    if ss_groups:
        # One group, sequential commands — Claude's ordering guarantee.
        assert len(ss_groups) == 1, "ordering relies on a single hook group"
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


def test_scaffolded_settings_realise_the_lifecycle_intents(tmp_path):
    target = _scaffold(tmp_path)
    settings = json.loads((target / ".claude" / "settings.json")
                          .read_text(encoding="utf-8"))
    assert _intents_realised_by(settings) == LIFECYCLE_INTENTS


def test_estate_standard_shape_realises_the_lifecycle_intents():
    cfg = json.loads((FIXTURES / "estate_shapes" / "hooks-only.json")
                     .read_text(encoding="utf-8"))
    assert _intents_realised_by(cfg) == LIFECYCLE_INTENTS
