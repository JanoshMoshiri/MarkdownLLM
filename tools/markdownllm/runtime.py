"""Shared runtime resolution — one owner for "which interpreter runs the floor".

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

import subprocess
from pathlib import Path

# The dependency that makes an interpreter *usable* by the floor, not merely
# present. One name, probed everywhere the floor may run.
FLOOR_DEPENDENCY = "yaml"

# Emitted into every hook body after ROOT and MDLLM are set. Kept free of
# braces so the surrounding template's .format(rel=...) passes it through.
# Candidate order: domain-local environment first (a domain that manages its
# own venv wins), then the framework-root environment derived from MDLLM,
# then PATH interpreters. POSIX and Windows venv layouts are both covered.
# The framework root comes from parameter expansion, NOT dirname: managed
# Git-hook shells (Codex, Phase 2B finding) run without the external utility
# set on PATH, and $MDLLM always ends tools/mdllm.py, so stripping the last
# two path components is exact and needs no subprocess at all.
SH_RESOLVE = """FW="${MDLLM%/*/*}"
PY=""
for c in "$ROOT/.venv/bin/python" "$ROOT/.venv/Scripts/python.exe" \\
         "$FW/.venv/bin/python" "$FW/.venv/Scripts/python.exe" \\
         python3 python py; do
  if "$c" -c "import yaml" >/dev/null 2>&1; then PY="$c"; break; fi
done"""


def interpreter_candidates(root: Path, fw_root: Path) -> list[str]:
    """The candidate list, in exactly the sh fragment's order."""
    return [
        str(root / ".venv" / "bin" / "python"),
        str(root / ".venv" / "Scripts" / "python.exe"),
        str(fw_root / ".venv" / "bin" / "python"),
        str(fw_root / ".venv" / "Scripts" / "python.exe"),
        "python3", "python", "py",
    ]


def probe_candidate(candidate: str, dependency: str = FLOOR_DEPENDENCY) -> dict:
    """Two independent facts about one candidate, never conflated:
    interpreter_found (it executes code at all) and dependency_loaded (the
    floor's dependency imports). A Store stub fails both; a bare python
    fails only the second — the case the old probe reported wrongly."""
    fact = {"candidate": candidate,
            "interpreter_found": False, "dependency_loaded": False}
    for flag, code in (("interpreter_found", "import sys"),
                       ("dependency_loaded", f"import {dependency}")):
        try:
            r = subprocess.run([candidate, "-c", code],
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
    facts = [probe_candidate(c, dependency)
             for c in interpreter_candidates(root, fw_root)]
    resolved = next((f["candidate"] for f in facts if f["dependency_loaded"]),
                    None)
    command_executed = None
    if resolved is not None:
        try:
            r = subprocess.run([resolved, str(mdllm_entry), "--help"],
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


def execution_test_hook(root: Path, hook: str = "pre-commit") -> dict:
    """Run the installed hook through git itself. `supported: False` is a
    valid result, not a failure — untested stays distinct from passed/failed
    (portability-claims-need-execution-tests)."""
    if not git_supports_hook_run(root):
        return {"hook": hook, "supported": False, "executed": False,
                "passed": None}
    r = subprocess.run(["git", "hook", "run", hook], cwd=root,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return {"hook": hook, "supported": True, "executed": True,
            "passed": r.returncode == 0,
            "detail": (r.stderr or r.stdout or "").strip()[-400:]}


def cmd_runtime_probe(args) -> int:
    """The reproducible runtime/commit probe (plan Phase 1): run it at the
    framework root or in a directly opened nested domain, in any harness's
    shell. Exit 0 iff a floor-capable interpreter resolves."""
    from .scaffold import MDLLM_ENTRY
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
