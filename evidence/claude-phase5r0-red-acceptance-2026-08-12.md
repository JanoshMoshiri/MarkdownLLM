---
id: claude-phase5r0-red-acceptance-2026-08-12
type: artifact
status: stable
created: 2026-08-12
tags: [harness, adapters, claude-code, phase-5r, red-gate, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side Gate 5R.0 acceptance: independent native PS 5.1 red rerun plus the real Claude Code dispatch observations the gate requires."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Every fact below was earned by executing the real host or the real harness, never by schema inspection."
---

# Claude Phase 5R.0 acceptance — independent red rerun + real dispatch observations

Claude-side record for Gate 5R.0. Two parts: (1) the independent rerun of the
committed native Windows PowerShell 5.1 regression fixtures, unchanged,
confirming both reds; (2) real Claude Code hook-dispatch observations from an
inert probe project, as the gate's execution-form matrix requires. Per the
handoff, nothing was repaired and no neutral port was changed.

## Part 1 — Native PowerShell 5.1 red rerun (unchanged fixtures)

| Fact | Value |
|---|---|
| Repository commit | `214967a` (plan: record Phase 5R native PS5 red gate) |
| Native host | `powershell.exe` 5.1.26100.9168 |
| OS | Microsoft Windows NT 10.0.26200.0 (Windows 11 Pro) |
| Date | 2026-08-12 (evening, Europe/London) |
| Command | `.\.venv\Scripts\python.exe -m pytest tools/tests/test_runtime.py::test_powershell_51_continues_after_stderr_writing_path_candidate tools/tests/test_codex_adapter.py::test_windows_runner_exit_is_surfaced_but_hook_still_returns_zero -q --basetemp .tmp-claude-phase5r-red` |
| Result | **2 failed** in 9.22s — both red, as the gate predicts |

Failure modes match the handoff's expectations exactly:

1. **Shared launcher red** (`test_runtime.py`): `mdllm.ps1:41`
   (`& $command.Source -c 'import yaml' 2>$null`) terminates with
   `NativeCommandError` / `RemoteException` when the stderr-writing fixture
   candidate runs under native 5.1 with `ErrorActionPreference = 'Stop'`.
   Exit 1; resolution never reaches the known-good `python3` successor.
2. **Codex hook red** (`test_codex_adapter.py`): the hook returns 0 with a
   well-formed `hookSpecificOutput` envelope, but reports "no floor-capable
   Python or framework runner was found" — the resolver died on the failed
   candidate instead of continuing to the framework runner and surfacing its
   exit 23 as "non-zero status".

The reruns were invoked from PowerShell 7 as the outer shell; the fixtures
themselves launch native `powershell.exe` and assert
`$PSVersionTable.PSVersion` starts with `5.1` from inside that host, so the
red is a native-5.1 fact, not a compatibility-mode artifact. Basetemp
`.tmp-claude-phase5r-red` was removed after the record was taken.

## Part 2 — Real Claude Code dispatch observations (5R.0 matrix)

Method: inert probe project at a path **containing a space**, with one
SessionStart matcher group holding **two** command handlers, each invoking a
Python recorder with a quoted two-word argument and a 3-second hold. Fired by
real headless Claude Code (`claude -p`, CLI 2.1.173) opening the project.
The model turn itself failed on an expired CLI OAuth token; dispatch happens
before the model call, so all hook facts below are unaffected.

| 5R.0 fact | Observation |
|---|---|
| Execution form | Shell form (command string). **Actual Windows shell: Git Bash** — parent chain `python.exe ← bash.exe ← bash.exe ← claude.exe`; `MSYSTEM=MINGW64`, `SHELL=C:\Program Files\Git\bin\bash.exe`. No PowerShell in the dispatch path on this host. |
| Ordering | **Parallel, confirmed.** Two handlers in one group started 11.5 ms apart with fully overlapping 3-second windows — and handler B (declared second) started *before* handler A. Intra-group declaration order is not even start order. |
| cwd | The project root (drive-letter case normalised to lower). Matches the stdin payload's `cwd`. |
| `CLAUDE_PROJECT_DIR` | Set; forward-slash form; **space in path preserved intact**. |
| Argument boundaries | `"two words"` arrived as **one** argv element through Git Bash double-quote handling. |
| stdin receipt | JSON payload received: `session_id`, `transcript_path`, `cwd`, `hook_event_name: SessionStart`, `source: startup`. |
| Transcript correlation | The harness-owned session transcript (`<transcript_path>/273bfa10….jsonl`) contains `hook_success` attachments (`hookName: SessionStart:startup`) embedding each probe's stdout, under the same `session_id` the probes received on stdin. Harness record ↔ probe record correlation holds without any manually minted evidence. |
| `--debug` stderr | Empty file in CLI 2.1.173 headless mode; the session transcript is the harness-owned record and supersedes it. |

## Consequences for the gate (observations, not port changes)

- The **parallel-dispatch red is now a live-harness fact on Windows**, not
  only a documentation citation: the frozen two-handler legacy form cannot
  guarantee `estate-sync → session-start` on the exact platform this estate
  runs on. Declaration order gave the *reverse* start order in this run.
- On a Windows host with Git for Windows present, the portable Claude launch
  seam must be **sh-compatible first**; the PowerShell fallback is reached
  only where Git Bash is absent. This matches the v1.10 pinned matrix; no
  neutral-port change is suggested by this evidence.
- One question for the 5R.0 owner, per the handoff's report-don't-redesign
  rule: the harness normalises the project path's drive-letter case
  (`C:` → `c:`) between config authoring and dispatch. If any managed
  definition hash ever incorporates an absolute path, case normalisation
  must be part of the hashing rule; the current relative-path design avoids
  this, so this is a watch-item, not a defect.

## Not claimed

No repair was made; the two reds remain red at `214967a`. No neutral port was
modified. These observations cover Claude Code CLI 2.1.173 headless on this
Windows host only; the `resume`/`clear`/`compact` SessionStart sources, POSIX
dispatch, PS-fallback-without-Git-Bash, and exec-form (`args`) dispatch remain
unobserved and stay owned by the remaining 5R.0 matrix work.
