---
id: posix-live-dispatch-record-2026-08-14
type: artifact
status: stable
created: 2026-08-14
tags: [portability, posix, execution-evidence, phase-6, live-dispatch]
linked_things:
  - id: claude-platform-surface-narrowed
    relation: implements
    notes: "Executes the promotion trigger that decision defined: a real POSIX dispatch record lifts POSIX from designed-for to verified-on, by evidence rather than by amendment."
  - id: posix-floor-record-2026-08-13
    relation: derived-from
    notes: "Completes the other half. That record verified the deterministic floor on Linux; this one verifies live harness dispatch and the full lifecycle."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Acceptance asserts emitted content, ordered step results, a floor commit and hash-bound attestation — never that a command ran."
---

# POSIX live dispatch — the Claude lifecycle verified on Linux

The half that could not be faked. `posix-floor-record-2026-08-13` verified
the deterministic floor on Linux; this record verifies **real Claude Code
dispatch and the complete lifecycle** on the same host, which required a
natively installed Node and Claude Code — the `claude` reachable through WSL
interop is the Windows binary and cannot produce POSIX evidence.

## Host

| Fact | Value |
|---|---|
| Distribution | Ubuntu 26.04 LTS (WSL2, kernel 6.18.33.2) |
| Claude Code | 2.1.232, installed via Linux npm |
| Binary check | `file` reports **ELF 64-bit LSB executable, x86-64, GNU/Linux** |
| PATH order | `/usr/local/bin/claude` resolves **before** the `/mnt/c` interop entry |
| Node | v22.22.1 (`/usr/bin/node`) |
| Framework | clone at `ea4ea12`, Linux filesystem (not `/mnt/c`) |

The binary check matters: the package installs its executable as
`claude.exe` even on Linux. `file` confirms a genuine ELF binary, so the
name is packaging noise, not a Windows process running under interop. Had it
been the latter, every record below would have been Windows evidence wearing
a Linux hat.

## Dispatch matrix — real events

| Fact | Shell form | Exec form |
|---|---|---|
| launcher (`parent_chain`) | `python3 ← sh ← claude` | `python3 ← claude` (shell-free) |
| platform reported by the hook | `linux` / `posix` | `linux` / `posix` |
| argv boundaries | `two words` one element | preserved |
| cwd | project root | project root |
| `CLAUDE_PROJECT_DIR` | set, native POSIX path, **space preserved** | set |
| stdin payload | full (`hook_event_name`, `source: startup`, `transcript_path`) | full |

**Native `sh` is the launcher.** The sh-dialect carrier chosen at Gate 5R.0
from Windows evidence now has its POSIX half: the same bytes that run under
Git Bash on Windows run under `/bin/sh` here, with no PowerShell branch
involved.

**Parallel dispatch is confirmed on POSIX.** Two handlers declared in one
matcher group started **4.4 ms** apart with **3.05 s** of overlap. The
one-handler projection is therefore required on both platforms — not a
Windows-specific workaround, as a Windows-only record might have suggested.

## Full lifecycle — a scaffolded domain on Linux

Projection shape: **1** SessionStart handler, `timeout: 120`, delegating to
`harness-event claude-code session-start`.

| Step | Result |
|---|---|
| ordered SessionStart, three separate real sessions | `[steps: estate-sync=0, session-start=0]` in every one |
| valid write → PostToolUse | **quiet** — no attachment, as designed |
| invalid write → PostToolUse | `[steps: validate=1]` + validation report, advisory, tool action not blocked |
| commit through the git floor | exit 0 under `session_gate: strict` |
| doctor, session-start | `execution=passed`, `definition_current=true`, `source=claude-code-project-hook` |
| doctor, post-write | `execution=failed`, `definition_current=true`, `validate=1` |

The last row is deliberate and worth keeping: the most recent post-write
event was the *controlled failure*, and the diagnostic reports it as failed
rather than letting the earlier passing write stand as the record. The
quiet-pass case is proven by the session-start attestation and the floor
commit, not by an absent attachment.

## An honest scaffold failure, correctly reported

The first Linux scaffold ended with **BIRTH SEQUENCE INCOMPLETE — the
isolation invariant did not fully hold**, naming two FAIL lines: the outer
`.gitignore` was updated but its commit failed, and the first domain commit
failed. Cause: a fresh WSL user with no `git config user.name/user.email`.

This is an environment gap, not a framework defect, and it is recorded as
*positive* evidence: the scaffold refused to claim a successful birth,
identified both failing legs, and printed the exact remedy. After setting
the identity, birth completed cleanly — `first commit made
(framework_version_seen: 3.31.0)`.

## Promotion

`claude-platform-surface-narrowed` defined the trigger: a real POSIX
dispatch record lifts POSIX from designed-for to verified-on by evidence,
with no plan amendment required. Both halves now exist — the floor
(2026-08-13) and live dispatch with full lifecycle (this record).

**POSIX is verified-on for the Claude Code lifecycle**, on the host
described above.

## Not claimed

Non-`startup` SessionStart sources (`resume`, `clear`, `compact`) remain
unobserved on both platforms. macOS is untested — this is Linux. Codex
dispatch on POSIX is a separate claim with a separate owner. Copilot
compatibility remains separate and unevidenced. The no-Git-Bash Windows
PowerShell fallback remains unreachable and therefore unverified.
