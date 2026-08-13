---
id: claude-phase5r0-matrix-completion-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [harness, adapters, claude-code, phase-5r, execution-evidence, launch-seam]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Claude-side completion of the remaining Gate 5R.0 dispatch matrix from 3d0aef7: exec-form observed, no-Git-Bash fallback proven unreachable on this host, POSIX returned as an operator scoping question."
  - id: claude-phase5r0-red-acceptance-2026-08-12
    relation: derived-from
    notes: "Continues the same probe method and evidence standard; part 1 of the matrix lives there."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Every claim below names the exact dispatch that earned it; unobservable branches are named as unobservable, not assumed."
---

# Claude Phase 5R.0 matrix completion — exec form, fallback reachability, portable-form determination

Continuation of the Claude-side Gate 5R.0 record from commit `3d0aef7`.
Same method as the 2026-08-12 record: inert probe projects under a path
containing a space, fired by real headless Claude Code (CLI 2.1.173,
Windows 11 26200), each record correlated with the harness-owned session
transcript (`hook_success` attachment under the same `session_id` delivered
on stdin). The CLI's expired OAuth again failed the model turn only; hook
dispatch precedes it and is unaffected. No neutral port was changed.

## Exec form (`command` + `args`) — OBSERVED, and it is truly shell-free

| Fact | Observation |
|---|---|
| Dispatch | **Supported in 2.1.173.** Parent chain `python.exe ← claude.exe` — **no shell process at all** between harness and target. |
| Argument boundaries | Exact argv pass-through: `two words` one element; `a"quote` and `back\slash` arrived byte-identical; no re-quoting layer. |
| Env expansion | **None.** A literal `$CLAUDE_PROJECT_DIR` arg arrived unexpanded. Exec form cannot reference environment in argv. |
| `CLAUDE_PROJECT_DIR` env | Set, **native backslash form** (shell form saw the forward-slash conversion Git Bash applies). |
| cwd | Project root, as in shell form. |
| Executable resolution | Bare `python` resolved via PATH — exec form does not remove the PATH dependency for bare names. |
| stdin / correlation | Same JSON payload; `hook_success` present in the harness transcript. |

## Windows PowerShell fallback without Git Bash — UNREACHABLE ON THIS HOST

Two attempts, two facts:

1. `CLAUDE_CODE_GIT_BASH_PATH` pointed at a nonexistent file → **hard startup
   refusal** ("Claude Code was unable to find CLAUDE_CODE_GIT_BASH_PATH
   path…"). An explicitly configured-but-invalid bash is an abort, not a
   fallback.
2. Every Git directory stripped from `PATH`, override unset → hooks
   dispatched **through Git Bash anyway** (`bash.exe ← bash.exe`,
   `MSYSTEM=MINGW64`). Claude Code self-locates Git Bash from its default
   install location without PATH.

Consequence: on any Windows machine with Git for Windows installed — which
includes every machine meeting the framework's own git floor via the
standard installer — the PowerShell fallback branch is **not exercisable**
without uninstalling or renaming Git, a system modification outside agent
authority. The fallback remains documentation-only: *designed-for at best,
never verified-on, on this estate's hosts*.

## POSIX dispatch — NOT AVAILABLE ON THIS HOST (operator question)

WSL is not installed on this machine, and installing it is a system change
the operator owns. Real POSIX Claude dispatch therefore cannot be observed
from this estate today. Options returned to the plan rather than assumed:

- **(a)** run the identical probe on a real macOS/Linux host (or WSL once
  the operator installs it) and record it as a separate evidence artifact;
- **(b)** narrow the *verified-on* claim to Windows-with-Git-for-Windows
  now, leaving POSIX *designed-for* with the sh-dialect argument below.

## Portable-form determination (the question the handoff asked)

Which form can portably invoke
`harness-event <harness> <moment> <root> <definition-hash>` without PATH
Python, absolute installation paths, or user-global configuration:

- **Exec form cannot host the invocation.** It is one argv with no env
  expansion and no logic. Interpreter *discovery* (project venv → framework
  venv → PATH candidates) is inherently conditional; exec form would need
  the interpreter already resolved, which is the problem being solved.
  Bare-name `command` reintroduces the PATH dependency.
- **Shell form in sh dialect is the single portable carrier.** On this
  Windows host, shell form runs under Git Bash — which Claude Code
  self-locates even with a stripped PATH — and the same sh-dialect bytes
  are what POSIX hosts run natively. One command, both platforms, and the
  candidate loop (relative venv probes before PATH names) removes the PATH
  Python assumption. This matches the seam the Codex adapter already uses
  (`command` in sh + fallback), now supported by live Claude dispatch
  evidence rather than schema reading.
- **The residual gap is named, not papered over:** a Windows host whose git
  floor is met *without* Git for Windows (no bash present) would take the
  documented PowerShell fallback — a branch this estate cannot execute or
  verify. Recommendation to the 5R.0 owner: scope the supported Claude
  Windows surface to Git-for-Windows-present, keep the fallback as an
  explicit designed-for-only branch (or drop it from claims), and let a
  real no-bash host promote it later if one ever exists.

## Facts worth carrying into the seam design

- Drive-letter case is normalised (`C:` → `c:`) between authoring and
  dispatch (both forms) — already flagged as a hashing watch-item.
- `CLAUDE_PROJECT_DIR` arrives forward-slash under Git Bash and native
  backslash under exec form: any consumer must treat the two spellings as
  one path identity.
- An invalid `CLAUDE_CODE_GIT_BASH_PATH` override aborts the harness
  entirely; diagnostics should surface that override's value when hooks
  mysteriously fail to fire.

## Not claimed

POSIX dispatch, the no-bash PowerShell fallback, and non-`startup`
SessionStart sources remain unobserved. Exec-form relative-path executable
resolution was not probed (bare name only). Nothing was repaired; the two
5R.0 reds remain red; the operator-owned `.codex/` directory is untouched.
