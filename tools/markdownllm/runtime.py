"""Python-side execution of the floor's interpreter policy.

The candidate policy itself — tables, emitted sh fragment, dependency name —
is contract data owned by ``hook_contract`` (the leaf); this module probes
and executes it.

Before this module (vendor-harness-adapter-foundation, Phase 1) the candidate
list lived three times in the emitted hook bodies and once more in mdllm.ps1,
and it carried two defects:

1. The framework-root environment was unreachable by construction: candidates
   keyed off the *domain* git root while `$MDLLM` resolved upward to the
   framework — so in managed shells whose only usable environment sits at the
   framework root, the floor died despite a working interpreter twenty
   characters away in the same command.
2. The probe (`import sys`) proved an interpreter exists, not that the floor's
   dependency loads — a bare python without PyYAML passed the probe and then
   blocked the commit with a message naming neither cause.

The fix, in one place: derive the framework root from the mdllm path itself
(the only value in scope that knows where the framework is), append its
environments to the candidate list, and probe by importing the actual
dependency. Probing by dependency also keeps the original Windows-Store-stub
defence: the stub fails any `-c` execution.

`probe()` is the python-side mirror of the sh fragment, returning the facts as
data — interpreter-found and dependency-loaded per candidate — for
`runtime-probe` (the reproducible cross-harness check) and for install-hook's
execution test. It is deliberately vendor-neutral: no harness names, no
harness config; presentation vocabulary belongs to Phase 3.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

# The candidate policy, the emitted sh fragment, and the dependency name are
# CONTRACT data and live in the leaf (hook_contract) — one owner shared with
# the hook producers and the byte-currency diagnosers. This module owns the
# Python-side EXECUTION of that policy: probing candidates, selecting the
# interpreter, and execution-testing installed hooks.
from .hook_contract import (
    FLOOR_DEPENDENCY, MDLLM_ENTRY, InterpreterCandidate,
    PATH_CANDIDATES, RELATIVE_CANDIDATES,
)




def interpreter_candidates(root: Path, fw_root: Path) \
        -> list[InterpreterCandidate]:
    """The candidate list, in exactly the sh fragment's order."""
    bases = {"root": root, "framework": fw_root}
    windows = sys.platform == "win32"
    relative = [InterpreterCandidate(str(bases[anchor] / Path(suffix)))
                for anchor, suffix, platform in RELATIVE_CANDIDATES
                if platform != "windows" or windows]
    path_candidates = [candidate for candidate, platform in PATH_CANDIDATES
                       if platform != "windows" or windows]
    return [*relative, *path_candidates]


def probe_candidate(candidate: str | InterpreterCandidate,
                    dependency: str = FLOOR_DEPENDENCY) -> dict:
    """Two independent facts about one candidate, never conflated:
    interpreter_found (it executes code at all) and dependency_loaded (the
    floor's dependency imports). A Store stub fails both; a bare python
    fails only the second — the case the old probe reported wrongly."""
    invocation = (candidate if isinstance(candidate, InterpreterCandidate)
                  else InterpreterCandidate(candidate))
    fact = {"candidate": invocation.executable,
            "prefix_args": list(invocation.prefix_args),
            "interpreter_found": False, "dependency_loaded": False}
    for flag, code in (("interpreter_found", "import sys"),
                       ("dependency_loaded", f"import {dependency}")):
        try:
            r = subprocess.run(invocation.command("-c", code),
                               capture_output=True, timeout=30)
            fact[flag] = r.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            pass
        if not fact["interpreter_found"]:
            break  # no interpreter => no dependency; don't fake a second probe
    return fact


def probe(root: Path, mdllm_entry: Path,
          dependency: str = FLOOR_DEPENDENCY) -> dict:
    """Probe every candidate; `resolved` is the first with the dependency
    loaded — the same selection the emitted hooks make. The resolved
    candidate is then made to EXECUTE the floor command itself
    (`command_executed`): importing the dependency proves the environment,
    not that the CLI's own import graph and entry run under that interpreter
    (Phase 2B acceptance finding — three facts, none promoted into another)."""
    fw_root = mdllm_entry.resolve().parent.parent
    candidates = interpreter_candidates(root, fw_root)
    facts = [probe_candidate(c, dependency) for c in candidates]
    selected = next((candidate for candidate, fact in zip(candidates, facts)
        if fact["dependency_loaded"]), None)
    resolved = selected.executable if selected else None
    command_executed = None
    if resolved is not None:
        try:
            r = subprocess.run(selected.command(str(mdllm_entry), "--help"),
                               capture_output=True, timeout=120)
            command_executed = r.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            command_executed = False
    return {"root": str(root), "framework_root": str(fw_root),
            "dependency": dependency, "candidates": facts,
            "resolved": resolved, "command_executed": command_executed}


def git_supports_hook_run(cwd: Path) -> bool:
    """`git hook run` arrived in 2.36 — the boundary for execution-testing an
    installed hook without staging a commit."""
    import re
    out = subprocess.run(["git", "--version"], cwd=cwd,
                         capture_output=True, text=True)
    m = re.search(r"(\d+)\.(\d+)", out.stdout or "")
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= (2, 36)


def _hook_path(root: Path, hook: str) -> Path | None:
    """Resolve the same hook path Git uses, including core.hooksPath."""
    resolved = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-path",
         f"hooks/{hook}"], cwd=root, capture_output=True, text=True)
    if resolved.returncode != 0 or not resolved.stdout.strip():
        resolved = subprocess.run(
            ["git", "rev-parse", "--git-path", f"hooks/{hook}"], cwd=root,
            capture_output=True, text=True)
    if resolved.returncode != 0 or not resolved.stdout.strip():
        return None
    path = Path(resolved.stdout.strip())
    return path if path.is_absolute() else root / path


def _git_windows_shell() -> str | None:
    """Find Git-for-Windows' own shell without trusting an arbitrary PATH sh."""
    git_executable = shutil.which("git")
    if not git_executable:
        return None
    git_path = Path(git_executable).resolve()
    # The normal layout is <root>/cmd/git.exe + <root>/bin/sh.exe (with
    # usr/bin as a compatible alternate).  Keep every candidate inside the
    # same resolved installation root as the git executable we are using.
    install_root = git_path.parent.parent
    for candidate in (
            install_root / "bin" / "sh.exe",
            install_root / "usr" / "bin" / "sh.exe"):
        try:
            resolved = candidate.resolve()
            resolved.relative_to(install_root.resolve())
        except (OSError, ValueError):
            continue
        if resolved.is_file():
            return str(resolved)
    return None


def run_git_hook(
        root: Path, hook: str, args: tuple[str, ...] = (), *,
        env: dict | None = None, expected_bytes: bytes | None = None,
        ) -> dict:
    """Execute a hook through Git, or through a conservative old-Git path.

    Git before 2.36 has no ``git hook run``.  On POSIX, direct argv execution
    (never ``shell=True``) gives the same shebang/executable semantics Git
    uses.  On Windows, direct shebang execution is not a platform primitive;
    fallback is permitted only for exact caller-attested bytes and an explicit
    ``sh`` executable.  Unknown operator scripts are never guessed through a
    shell.  If neither safe route exists the result stays explicitly untested.
    """
    root = Path(root).resolve()
    if git_supports_hook_run(root):
        result = subprocess.run(
            ["git", "hook", "run", hook, "--", *args], cwd=root, env=env,
            capture_output=True, text=True, encoding="utf-8",
            errors="replace")
        return {"hook": hook, "supported": True, "executed": True,
                "passed": result.returncode == 0, "via": "git-hook-run",
                "returncode": result.returncode,
                "stdout": result.stdout or "", "stderr": result.stderr or "",
                "detail": (result.stderr or result.stdout or "").strip()[-400:]}

    path = _hook_path(root, hook)
    if path is None or not path.is_file() or path.is_symlink():
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None, "via": "none", "returncode": None,
                "stdout": "", "stderr": "",
                "detail": "hook path is absent or not a regular file"}
    try:
        current = path.read_bytes()
    except OSError as exc:
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None, "via": "none", "returncode": None,
                "stdout": "", "stderr": "", "detail": str(exc)}
    if expected_bytes is not None and current != expected_bytes:
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None, "via": "none", "returncode": None,
                "stdout": "", "stderr": "",
                "detail": "hook bytes changed before compatibility execution"}

    command: list[str] | None = None
    if os.name != "nt":
        if os.access(path, os.X_OK):
            command = [str(path), *args]
    elif expected_bytes is not None:
        shell_path = _git_windows_shell()
        if shell_path:
            command = [shell_path, str(path), *args]
    if command is None:
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None, "via": "none", "returncode": None,
                "stdout": "", "stderr": "",
                "detail": "no semantics-preserving old-Git execution route"}
    try:
        result = subprocess.run(
            command, cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace")
    except OSError as exc:
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None, "via": "none", "returncode": None,
                "stdout": "", "stderr": "", "detail": str(exc)}
    return {"hook": hook, "supported": True, "executed": True,
            "passed": result.returncode == 0, "via": "direct-compatible",
            "returncode": result.returncode,
            "stdout": result.stdout or "", "stderr": result.stderr or "",
            "detail": (result.stderr or result.stdout or "").strip()[-400:]}


def execution_test_hook(
        root: Path, hook: str = "pre-commit", *,
        expected_bytes: bytes | None = None) -> dict:
    """Run the installed hook through git itself. `supported: False` is a
    valid result, not a failure — untested stays distinct from passed/failed
    (portability-claims-need-execution-tests)."""
    # Exact caller-supplied bytes make the Windows shell fallback safe: an
    # operator replacement is reported untested rather than executed. Runtime
    # consumes this contract; it never imports the scaffold producer.
    return run_git_hook(root, hook, expected_bytes=expected_bytes)


def cmd_runtime_probe(args) -> int:
    """The reproducible runtime/commit probe (plan Phase 1): run it at the
    framework root or in a directly opened nested domain, in any harness's
    shell. Exit 0 iff a floor-capable interpreter resolves."""
    root = Path(args.path).resolve()
    result = probe(root, MDLLM_ENTRY)
    print(f"## Runtime Probe — {root}")
    print(f"framework_root: {result['framework_root']}")
    print(f"dependency: {result['dependency']}\n")
    for f in result["candidates"]:
        if f["dependency_loaded"]:
            state = "OK    interpreter + dependency"
        elif f["interpreter_found"]:
            state = "PART  interpreter found, dependency missing"
        else:
            state = "--    not found"
        print(f"  {state}  {f['candidate']}")
    if result["resolved"]:
        print(f"\nresolved: {result['resolved']}")
        if result["command_executed"]:
            print("command-executed: OK — the floor CLI ran under the "
                  "resolved interpreter")
            return 0
        print("command-executed: FAILED — the dependency loads but the floor "
              "CLI did not run; the environment is only partially usable")
        return 1
    print("\nresolved: NONE — the floor cannot run here. Install Python 3.10+ "
          f"with {result['dependency']!r}, or create a .venv at the framework "
          "root or this repo's root.")
    return 1
