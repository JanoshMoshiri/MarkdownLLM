---
id: posix-floor-record-2026-08-13
type: artifact
status: stable
created: 2026-08-13
tags: [portability, posix, floor, execution-evidence, phase-5r]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "POSIX half of the Gate 5R.0 platform question: the deterministic floor executed on real Linux. Live Claude dispatch on POSIX remains unobserved, so the narrowed surface stands."
  - id: claude-platform-surface-narrowed
    relation: references
    notes: "Partially satisfies the promotion trigger: the floor half is now verified-on Linux; the live-dispatch half still gates full POSIX promotion."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Executed rather than reasoned: every row below is a command run on a real Linux kernel, including the branches Windows structurally cannot reach."
---

# POSIX floor record — the deterministic floor executed on real Linux

First execution of the framework's floor on a genuine POSIX host. Scope is
deliberately the **floor half** of the POSIX question: interpreter
resolution, validation, generated-artifact currency, and the Git commit
boundary. Live Claude Code hook dispatch on POSIX is **not** covered here and
remains unobserved.

## Host

| Fact | Value |
|---|---|
| Distribution | Ubuntu 26.04 LTS |
| Kernel | Linux 6.18.33.2-microsoft-standard-WSL2 (WSL2) |
| Python | 3.14.4 (system), venv-built |
| PyYAML / pytest | 6.0.3 / 9.0.2 |
| Git | 2.53.0 |
| Framework commit | `27b0723` |
| Clone | fresh `git clone` into the Linux filesystem (`~/mdllm-posix`), not `/mnt/c` |

Cloning into the Linux filesystem is deliberate: a `/mnt/c` working copy
would test the 9p bridge rather than POSIX.

## Interpreter resolution — the branch Windows cannot reach

`mdllm runtime-probe` on Linux:

```
OK    interpreter + dependency  <root>/.venv/bin/python
--    not found                 <root>/.venv/Scripts/python.exe
OK    interpreter + dependency  python3
--    not found                 python
--    not found                 py
resolved: <root>/.venv/bin/python
command-executed: OK — the floor CLI ran under the resolved interpreter
```

The `.venv/bin/python` candidate and the `python3`-present/`python`-absent
ordering are structurally unreachable on Windows. They now have a live
record, and the resolved interpreter actually executed the floor CLI.

## Floor results

| Check | Result |
|---|---|
| `validate .` | clean across the corpus (0 errors, 0 warnings) |
| `coherence .` | only the known `claude-adapter-baseline` label note (Info) |
| `kernel . --check` | in sync |
| `index . check` | relationships + provenance in sync |
| `provenance .` | pre-existing dated-pin advisories only |
| `install-hook .` | pre-commit + commit-msg + post-commit installed; **execution test passed** |
| `doctor .` | **FLOOR ACTIVE — mechanical validation enforced at the commit boundary** |

## Full suite: 437 passed, 2 failed (39.20s)

The two failures are exactly the two frozen Phase 5R.0 reds. **But they
should not have executed at all**, and the reason is a portability finding
in its own right.

### Finding: WSL interop defeats the Windows-only skip guards

Both tests guard with `shutil.which("powershell.exe")` / `cmd.exe` and skip
when absent. Under WSL, binfmt_misc interop (`WSLInterop: enabled`) puts
Windows executables on the Linux PATH:

```
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
/mnt/c/Windows/system32/cmd.exe
```

So the guards pass, and a Linux pytest run launches **Windows** PowerShell
across the interop boundary. The resulting failure differs from the native
Windows failure (`fixture candidate owns execution` here vs
`NativeCommandError` natively) — an environment-mixed result that is
evidence for neither platform.

Consequences worth carrying into 5R.1, which is centralising runtime
candidates:

1. **Host-shell tests need a POSIX exclusion, not only a which-guard.**
   Presence of `powershell.exe` on PATH does not mean the host is Windows.
   Gate on `os.name`/`sys.platform` as well, or the suite silently reports a
   cross-boundary result as a platform failure.
2. **Candidate resolution should consider interop.** On WSL a `/mnt/c`
   Windows binary can satisfy a bare-name PATH probe. The current POSIX
   ordering resolves the venv first and is unaffected, but any future
   bare-name fallback could select a Windows interpreter from Linux.
3. The 5R.0 reds remain **red on their native host** (recorded 2026-08-12);
   nothing here weakens or repairs them.

Excluding those two host-specific tests, the suite is **green on Linux**:
437 passing on Python 3.14.4 — a materially newer interpreter than the
Windows run's 3.12.13, so this doubles as forward-compatibility evidence.

## What this does and does not promote

**Promotes:** the deterministic floor — resolution, validation, generated
artifacts, and the Git commit boundary — from designed-for to **verified-on
Linux**.

**Does not promote:** live Claude Code dispatch on POSIX. Inside WSL,
`claude` and `npm` resolve to `/mnt/c/...` Windows binaries through interop;
invoking those would produce Windows evidence wearing a Linux hat. Real
POSIX dispatch needs a natively installed Node and Claude Code CLI, and an
authenticated session. Until that record exists,
`claude-platform-surface-narrowed` stands unchanged.
