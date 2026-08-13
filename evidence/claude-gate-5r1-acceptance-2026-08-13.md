---
id: claude-gate-5r1-acceptance-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, phase-5r, acceptance-gate, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side acceptance of Gate 5R.1 at 72744f4: all six handoff checks green on Windows and native Linux. Unblocks Claude-owned Phase 5R.2."
  - id: claude-phase5r0-red-acceptance-2026-08-12
    relation: derived-from
    notes: "The two fixtures accepted red here run green, unchanged — the red-to-green handoff the gate required."
  - id: posix-floor-record-2026-08-13
    relation: derived-from
    notes: "The WSL interop finding reported there is closed here: Windows-only tests now skip on host identity rather than executable presence."
---

# Claude acceptance — Gate 5R.1 at `72744f4`

Independent Claude-side acceptance of the Codex 5R.1 handoff. All six
required checks executed; all green. No neutral port was altered, and no
missing abstraction was found, so nothing is returned to Codex.

## Environment

| Fact | Value |
|---|---|
| Handoff commit | `72744f4` (tree clean apart from operator-owned untracked `.codex/`) |
| Windows host | Windows 11, NT 10.0.26200.0; native `powershell.exe` **5.1.26100.9168** |
| Windows Python | 3.12.13 (framework `.venv`) |
| Linux host | Ubuntu 26.04 LTS, kernel 6.18.33.2-microsoft-standard-WSL2 |
| Linux Python / pytest | 3.14.4 / 9.0.2 |
| Linux clone | `~/mdllm-posix`, hard-reset to the handoff commit |

## 1. The two previously-red fixtures — PASS

```
python -m pytest tools/tests/test_runtime.py::test_powershell_51_continues_after_stderr_writing_path_candidate \
                 tools/tests/test_codex_adapter.py::test_windows_runner_exit_is_surfaced_but_hook_still_returns_zero -q
2 passed in 3.90s
```

Fixtures unchanged from the accepted-red record. The native PowerShell 5.1
resolver now treats a stderr-writing candidate as one negative candidate fact
and continues, and the Codex hook reaches its runner instead of reporting no
floor-capable runtime.

## 2. Complete suite, Windows — PASS

```
python -m pytest tools/tests -q
442 passed in 531.13s (0:08:51)
```

## 3. Complete suite, native Linux at the handoff commit — PASS

```
.venv/bin/python -m pytest tools/tests -q -rs
439 passed, 3 skipped in 62.25s
SKIPPED tools/tests/test_codex_adapter.py:135: native Windows host is required
SKIPPED tools/tests/test_runtime.py:161:      native Windows host is required
SKIPPED tools/tests/test_runtime.py:208:      native Windows host is required
```

The skips are the substance of this check. WSL interop puts
`/mnt/c/.../powershell.exe` and `cmd.exe` on the Linux PATH, so the previous
`shutil.which` guards passed and a Linux run launched **Windows** PowerShell
across the boundary — a result that was evidence for neither platform. The
guards now gate on host identity, so the tests skip honestly. The finding
reported in `posix-floor-record-2026-08-13` is closed.

## 4. Installed Git pre-commit hook through Windows Git's real shell — PASS

Executed via `C:\Program Files\Git\bin\sh.exe` (not a PowerShell emulation of
it), against a clean tree: **exit 0**.

## 5. Inward boundary — no vendor schema in launch/runtime/lifecycle — PASS

Vendor vocabulary (`SessionStart`, `PostToolUse`, `matcher`,
`hookSpecificOutput`, `commandWindows`, `.claude/`, `.codex/`) appears **only**
in `adapters/claude_code.py` and `adapters/codex.py`.

- `runtime.py`, `harness_ports.py`, `harness_diagnostics.py` — import no
  adapter and name no vendor schema.
- `lifecycle_runner.py` — the neutral service `dispatch_lifecycle_event`
  receives `output_port: LifecycleOutputPort` by injection. Its
  `from .adapters import get` is **function-local inside `cmd_harness_event`**,
  which is the documented CLI composition root. Resolution happens at the
  root; the service depends only on the port. (Recorded because a module-level
  reading of the import list suggests otherwise; the placement is the point.)

## 6. Records — captured above and in this artifact's commit

## Noise in this run, disclosed

Two anomalies were caused by the acceptance runner, not by the code:

1. A first Windows suite reported 2 failures in `test_mdllm.py`
   (`test_session_start_floor_check_skips_non_repo` and
   `test_session_start_framework_root_is_not_a_stale_domain`). Cause:
   `--basetemp` pointed **inside** the repository, so pytest's "non-repo"
   temp directory sat under the framework's own `.git` and a floor status was
   correctly reported where the test expected none. Both pass with a default
   temp directory; the recorded run above uses one.
2. A first pre-commit check validated 677 things with 74 errors — leftover
   `.tmp-claude-*` scaffold fixtures from that same run. Removed; the recorded
   run is against a clean tree.

Neither anomaly reflects a defect in `72744f4`.

## Verdict

**Gate 5R.1 accepted.** Claude-owned Phase 5R.2 may begin.

Carried forward into 5R.2, unchanged: the live Claude runs require a
re-authenticated Claude Code CLI, and a POSIX live-dispatch record
additionally requires natively installed Node and Claude Code inside the
Linux host (the `claude` reachable there today is the Windows binary via
interop). The narrowed surface in `claude-platform-surface-narrowed`
therefore still stands.
