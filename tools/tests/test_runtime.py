"""Phase 1 of vendor-harness-adapter-foundation: the shared runtime port.

Pins the two repaired defects — the framework-root environment is reachable
from a nested domain's hooks, and the candidate probe proves the dependency
loads rather than merely that an interpreter exists — plus the single-owner
property: the resolution fragment appears in every emitted hook body via one
constant, never restated.

Run: python -m pytest tools/tests/test_runtime.py -q
"""

import os
import shutil
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
    assert result["command_executed"] is None  # unresolved => untested, never False
    result = runtime.probe(tmp_path, Path(mdllm.__file__), dependency="yaml")
    assert result["resolved"] is not None  # the suite's own env proves it


def test_probe_reports_command_executed_as_its_own_fact(tmp_path, monkeypatch):
    # 2B acceptance finding: importing the dependency proves the environment,
    # not that the floor CLI runs. The probe must execute the real entry under
    # the resolved interpreter and report that as a third, unpromoted fact.
    # Candidates are injected at the declared boundary (v1.6 return item 4):
    # the suite's own interpreter is the one floor-capable candidate every
    # harness running these tests is guaranteed to have — the test must not
    # borrow a PyYAML-capable PATH interpreter from the authoring harness.
    monkeypatch.setattr(runtime, "interpreter_candidates",
                        lambda root, fw: [sys.executable])
    result = runtime.probe(tmp_path, Path(mdllm.__file__), dependency="yaml")
    assert result["resolved"] == sys.executable
    assert result["command_executed"] is True
    # A resolved interpreter with a broken entry is executed=False, not True:
    broken = tmp_path / "not-mdllm.py"
    broken.write_text("import sys\nsys.exit(3)\n", encoding="utf-8")
    result = runtime.probe(tmp_path, broken, dependency="yaml")
    assert result["resolved"] == sys.executable
    assert result["command_executed"] is False


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
        emitted = body.format(rel="../../tools/mdllm.py")
        assert emitted.count(runtime.SH_RESOLVE) == 1
        assert "import yaml" in emitted          # dependency probe
        assert '-c "import sys"' not in emitted  # the defective probe is gone
        assert '"$FW/.venv' in emitted           # framework env reachable
        assert "dirname" not in emitted          # 2B: managed Git-hook shells
        #                                          lack the external utility set


def test_powershell_entry_probes_the_dependency():
    # Every candidate branch is pinned (v1.6 return item 4): the launcher has
    # exactly three execution paths — repository venv, PATH python/python3
    # loop, and the py -3 fallback — and each must probe the dependency
    # before executing the entry. A fourth unprobed branch fails the count.
    ps1 = (Path(mdllm.__file__).resolve().parent / "mdllm.ps1").read_text(
        encoding="utf-8")
    assert ps1.count("-c 'import yaml'") == 3
    assert "'import sys'" not in ps1
    probes = [ln for ln in ps1.splitlines() if "-c 'import yaml'" in ln]
    assert any("$venvPython" in ln for ln in probes)      # venv branch
    assert any("$command.Source" in ln for ln in probes)  # PATH loop
    assert any("-3" in ln for ln in probes)               # py launcher


def test_powershell_51_continues_after_stderr_writing_path_candidate(
        tmp_path):
    """The shared launcher must treat a failed native probe as one candidate.

    Windows PowerShell 5.1 turns native stderr into a terminating
    ``RemoteException`` while ``ErrorActionPreference`` is ``Stop``.  The
    committed command fixtures make that behavior independent of Microsoft
    Store aliases or the author's PATH: ``python`` is the known-bad first
    candidate and ``python3`` is the known-good successor.
    """
    powershell = shutil.which("powershell.exe")
    if powershell is None:
        import pytest
        pytest.skip("native Windows PowerShell 5.1 is required")

    fixture_dir = Path(__file__).parent / "fixtures" / "powershell"
    candidate_dir = tmp_path / "candidate-bin"
    candidate_dir.mkdir()
    shutil.copy2(fixture_dir / "stderr-python.cmd",
                 candidate_dir / "python.cmd")
    shutil.copy2(fixture_dir / "floor-python.cmd",
                 candidate_dir / "python3.cmd")

    tool_dir = tmp_path / "framework" / "tools"
    tool_dir.mkdir(parents=True)
    shutil.copy2(Path(mdllm.__file__).resolve().with_name("mdllm.ps1"),
                 tool_dir / "mdllm.ps1")
    (tool_dir / "mdllm.py").write_text(
        "raise SystemExit('fixture candidate owns execution')\n",
        encoding="utf-8")
    env = dict(os.environ)
    env["PATH"] = str(candidate_dir) + os.pathsep + env.get("PATH", "")

    completed = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-NonInteractive",
         "-ExecutionPolicy", "Bypass", "-File",
         str(tool_dir / "mdllm.ps1"), "runtime-probe", "."],
        env=env, capture_output=True, text=True, timeout=30,
        encoding="utf-8", errors="replace")

    version = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
         "$PSVersionTable.PSVersion.ToString()"],
        capture_output=True, text=True, timeout=10,
        encoding="utf-8", errors="replace")
    assert version.stdout.strip().startswith("5.1"), version.stdout
    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "MDLLM deterministic floor candidate executed" in completed.stdout


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
    assert 'FW="${MDLLM%/*/*}"' in hook  # parameter expansion, no dirname
    assert "dirname" not in hook


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


def test_hook_passes_when_no_path_python_works(tmp_path):
    # 2B acceptance finding: a PATH interpreter can mask framework-venv
    # selection. Here every PATH python is a failing stub, the domain has no
    # venv of its own, and the hook must still pass — which only the
    # framework-root environment (derived in-shell from $MDLLM, no dirname)
    # can explain.
    import pytest
    fw_venv = [p for p in (Path(mdllm.__file__).resolve().parent.parent
                           / ".venv" / "Scripts" / "python.exe",
                           Path(mdllm.__file__).resolve().parent.parent
                           / ".venv" / "bin" / "python") if p.is_file()]
    if not fw_venv:
        pytest.skip("no framework-root venv on this machine")
    if not runtime.git_supports_hook_run(Path.cwd()):
        pytest.skip("git predates `git hook run`")
    _git_repo(tmp_path)
    target = tmp_path / "fw-venv-selection-check"
    mdllm.cmd_scaffold(_ns(path=str(target)))
    mdllm.cmd_session_start(_ns(path=str(target), assistant=False))
    assert not (target / ".venv").exists()
    stubs = tmp_path / "failing-pythons"
    stubs.mkdir()
    for name in ("python", "python3", "py"):
        stub = stubs / name
        stub.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8", newline="\n")
        try:
            stub.chmod(stub.stat().st_mode | 0o111)
        except OSError:
            pass
    env = dict(os.environ)
    env["PATH"] = str(stubs) + os.pathsep + env.get("PATH", "")
    r = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=target,
                       env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    assert r.returncode == 0, (r.stderr or r.stdout)


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
