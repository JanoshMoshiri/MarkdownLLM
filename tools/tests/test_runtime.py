"""Phase 1 of vendor-harness-adapter-foundation: the shared runtime port.

Pins the two repaired defects — the framework-root environment is reachable
from a nested domain's hooks, and the candidate probe proves the dependency
loads rather than merely that an interpreter exists — plus the single-owner
property: the resolution fragment appears in every emitted hook body via one
constant, never restated.

Run: python -m pytest tools/tests/test_runtime.py -q
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm import runtime  # noqa: E402
from markdownllm import scaffold as scaffold_mod  # noqa: E402

for _k in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_k, "floor-tests")
for _k in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_k, "floor-tests@local")


def _ns(**kw):
    import argparse
    return argparse.Namespace(**kw)


def _git_repo(p: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=p, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=p, check=True)


# ----------------------------------------------------------- probe semantics


def test_probe_separates_interpreter_from_dependency():
    # The repaired defect: these are two facts, not one. A real interpreter
    # probed for a module it lacks reports found-but-not-loaded — the case
    # the old `import sys` probe collapsed into a misleading success.
    ok = runtime.probe_candidate(sys.executable, dependency="yaml")
    assert ok["interpreter_found"] and ok["dependency_loaded"]
    partial = runtime.probe_candidate(
        sys.executable, dependency="zzz_module_that_does_not_exist")
    assert partial["interpreter_found"] and not partial["dependency_loaded"]
    absent = runtime.probe_candidate("no-such-interpreter-anywhere")
    assert not absent["interpreter_found"] and not absent["dependency_loaded"]


def test_probe_resolves_only_on_dependency(tmp_path):
    # resolved must never point at an interpreter that cannot run the floor.
    result = runtime.probe(tmp_path, Path(mdllm.__file__),
                           dependency="zzz_module_that_does_not_exist")
    assert result["resolved"] is None
    result = runtime.probe(tmp_path, Path(mdllm.__file__), dependency="yaml")
    assert result["resolved"] is not None  # the suite's own env proves it


def test_candidate_order_matches_the_sh_fragment(tmp_path):
    # The python-side mirror and the emitted sh fragment must never drift:
    # every path candidate's tail appears in SH_RESOLVE, in the same order.
    fw = Path(mdllm.__file__).resolve().parent
    cands = runtime.interpreter_candidates(tmp_path, fw)
    tails = [".venv/bin/python", ".venv/Scripts/python.exe"]
    assert [Path(c).as_posix().rsplit("/.venv/")[-1] for c in cands[:4]] == \
        ["bin/python", "Scripts/python.exe"] * 2
    assert cands[4:] == ["python3", "python", "py"]
    frag = runtime.SH_RESOLVE
    order = [frag.index(f'"$ROOT/{t}"') for t in tails]
    order += [frag.index(f'"$FW/{t}"') for t in tails]
    assert order == sorted(order)
    assert frag.index("$ROOT/.venv") < frag.index("$FW/.venv") < \
        frag.index("python3")


# ------------------------------------------------------- single-owner bodies


def test_every_hook_body_carries_the_shared_fragment_once():
    for body in (mdllm.HOOK_BODY, scaffold_mod.POST_COMMIT_HOOK_BODY,
                 mdllm.COMMIT_MSG_HOOK_BODY):
        assert body.count(runtime.SH_RESOLVE) == 1
        assert "import yaml" in body          # dependency probe
        assert '-c "import sys"' not in body  # the defective probe is gone
        assert '"$FW/.venv' in body           # framework env reachable


def test_powershell_entry_probes_the_dependency():
    ps1 = (Path(mdllm.__file__).resolve().parent / "mdllm.ps1").read_text(
        encoding="utf-8")
    assert "'import yaml'" in ps1
    assert "'import sys'" not in ps1


# ---------------------------------------------- nested-domain hook execution


def test_nested_domain_hook_derives_framework_env(tmp_path):
    # A domain scaffolded under an outer repo gets hooks whose FW derivation
    # walks up from $MDLLM — the framework venv is reachable by construction.
    _git_repo(tmp_path)
    target = tmp_path / "runtime-probe-check"
    rc = mdllm.cmd_scaffold(_ns(path=str(target)))
    assert rc == 0  # the birth commit itself already ran the new pre-commit
    hook = (target / ".git" / "hooks" / "pre-commit").read_text(encoding="utf-8")
    assert runtime.SH_RESOLVE in hook
    assert 'FW="$(dirname "$(dirname "$MDLLM")")"' in hook


def test_install_hook_execution_tests_the_real_hook(tmp_path, capsys):
    _git_repo(tmp_path)
    target = tmp_path / "runtime-exec-check"
    mdllm.cmd_scaffold(_ns(path=str(target)))
    # Scaffolded domains are born session_gate: strict — the execution test
    # runs the REAL floor, so satisfy the ritual first, as an operator would.
    mdllm.cmd_session_start(_ns(path=str(target), assistant=False))
    capsys.readouterr()
    rc = mdllm.cmd_install_hook(_ns(path=str(target)))
    out = capsys.readouterr().out
    if runtime.git_supports_hook_run(target):
        assert rc == 0 and "execution test: pre-commit ran and passed" in out
    else:
        assert rc == 0 and "UNTESTED" in out


def test_install_hook_reports_a_blocking_floor_honestly(tmp_path, capsys):
    # Without the session-start attestation the strict gate blocks — and the
    # execution test must say the hook ran and FAILED, not that installation
    # failed: wired-but-blocking is a floor state, not an install defect.
    _git_repo(tmp_path)
    target = tmp_path / "runtime-gate-check"
    mdllm.cmd_scaffold(_ns(path=str(target)))
    capsys.readouterr()
    rc = mdllm.cmd_install_hook(_ns(path=str(target)))
    out = capsys.readouterr().out
    if runtime.git_supports_hook_run(target):
        assert rc == 1 and "ran and FAILED" in out
    else:
        assert rc == 0 and "UNTESTED" in out
