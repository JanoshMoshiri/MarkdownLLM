---
id: portability-claims-need-execution-tests
type: insight
status: active
version: 1.4
created: 2026-06-11
session: 2026-06-11
source: both
confidence: high
origin: stated
linked_things:
  - id: agents-md-discovery-is-harness-dependent
    relation: supports
    notes: "Second hook failure, second environment, second cause — the floor's availability is measured per environment, never asserted"
  - id: orchestration-specification
    relation: informs
    notes: "The post-write:commit hard hook silently depends on the pre-commit hook actually executing"
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
    notes: "A portability claim is a tracking artifact for a capability; it drifts the same way"
---

# Portability Claims Need Execution Tests, Not Resolution Tests

## The Insight

A claim that the floor works in an environment is verified only by *executing*
the capability there — resolving it (path exists, command found, file present)
is not verification. The pre-commit hook has now failed in two environments
for two different reasons, and both failures were discovered only by
attempting a real commit:

1. **Cowork sandbox (session 6):** the hook hardcoded one machine's absolute
   path and a bare `python` — unresolvable there. Fixed with runtime
   resolution: `command -v python3 || command -v python`.
2. **The authoring machine (session 7):** that fix itself failed. Windows
   ships Microsoft Store alias stubs named `python3`/`python` that
   `command -v` happily resolves but that only print an install hint and exit
   nonzero. The real install provides `python` but not `python3`, so the
   chain matched the stub first and blocked every commit. Fixed by executing
   each candidate (`"$c" -c "import sys"`) instead of resolving it.

The session-6 fix was tested where it was written (the sandbox) and declared
portable. The very next environment falsified the claim — the fix had
upgraded the hook from *resolution by hardcoding* to *resolution by lookup*,
but verification still stopped short of execution.

3. **Codex desktop harness (2026-08-11):** its PowerShell shell had no
   `python` on PATH, while its bundled Python 3.12 lacked PyYAML. The generic
   candidate chain therefore found neither a usable interpreter nor the
   dependency the floor needs. The repair is deliberately a Codex-harness
   adapter, not a universal runtime claim: a gitignored repository `.venv`,
   `tools/mdllm.ps1` as its entry point, and generated hooks that prefer
   `.venv/Scripts/python.exe` (or `.venv/bin/python` on POSIX). `mdllm doctor`,
   validation, coherence, and the real pre-commit hook all executed through
   it at the framework root; commit `4e1ad73` is the audit record. That
   evidence did not exercise the nested-domain fallback branch.

4. **Codex managed Git-hook shell, nested-domain branch (2026-08-11):** the
   Phase 1 resolver did execute candidates, but first derived the framework
   root with external `dirname`. This shell's hook PATH does not contain
   `dirname`. A root commit still passed because the root-local venv was found
   before the broken framework fallback mattered; a directly opened domain
   with no local venv failed. The execution test had exercised *a successful
   branch*, not the branch supporting the portability claim.

5. **The cross-harness test fixture itself (2026-08-11):** the repaired
   resolver passed real framework-root, directly-opened-domain, fresh-hook,
   and masked-PATH probes in Codex. Its new `command_executed` unit test still
   failed there because it moved the entry under a temporary root and then
   silently relied on PATH to supply another PyYAML-capable interpreter.
   Claude's environment satisfied that undeclared fixture dependency; Codex's
   did not. The failing test was evidence about the test harness, not a failure
   of the production fallback it purported to isolate.

6. **Claude adapter byte freeze versus lifecycle semantics (2026-08-12):** the
   extraction correctly proved that the new adapter emitted exactly the old
   `.claude/settings.json` bytes. The frozen shape contained two matching
   SessionStart handlers and the test named their array order “sequential.” A
   current contract review established that Claude launches matching handlers
   in parallel. Byte equality therefore proved faithful extraction of a legacy
   artifact, not preservation of the intended `estate-sync → session-start`
   behavior. A contract fixture needs a semantic execution test in addition to
   a golden byte test.

## Why It Matters

- This is the same epistemic rule the framework already applies elsewhere,
  now recognised as one pattern: token costs are re-measured with
  `mdllm tokens`, never asserted (AGENTS.md); vendor support is
  *designed-for* until *verified-on* (README action item from the independent
  review); indexes are validated by rebuild-and-diff, not trusted. The floor's
  own availability belongs on that list.
- **The commit test is the floor's execution probe.** Any first session in a
  new environment should attempt a real commit through the hook before
  relying on `post-write:commit` — a hook that cannot run degrades the floor
  silently, and the hard hook's guarantee with it.
- **Exercise the claimed fallback, not merely the resolver.** A candidate
  chain can pass through an earlier branch while a later branch is unusable.
  Portability evidence must remove or disable earlier candidates, run with the
  target shell's real command set, and force the exact fallback under claim.
  Shell syntax portability also includes utility availability: an external
  `dirname`, `realpath`, or similar command is a dependency even when `/bin/sh`
  itself exists.
- **An execution test has its own runtime contract.** If the fixture needs a
  floor-capable candidate after relocating the subject, it must construct or
  inject that candidate explicitly. Borrowing PATH from the authoring harness
  turns a supposedly cross-harness test into an accidental measurement of the
  machine running it.
- **A golden is evidence of identity, not consequence.** Preserve it when
  extracting or migrating an artifact, but separately exercise the vendor's
  current scheduling, cwd, output, and trust semantics. A test name or comment
  cannot promote serialized order into runtime order.
- Candidate mechanical follow-up: `install-hook` could self-test by running
  the script it just emitted once (exit status only) and reporting
  floor-unavailable immediately, instead of leaving the discovery to the
  first blocked commit.
- A Codex-desktop success is evidence for that exact adapter and environment,
  not evidence that every desktop or managed shell supplies the same Python
  contract. The compatibility table must preserve that scope.

## Context

Surfaced when the first commit of `framework-map.md` was blocked on the
authoring machine by the freshly-"portable" hook (session 7, 2026-06-11).
Diagnosis: `(Get-Command python).Source` showed a real 3.12 install, while
both Store stubs existed in `WindowsApps` and git's sh resolved `python3` to
a stub. Fix landed in `tools/mdllm.py` `HOOK_BODY` (commit `32d5c6f`),
reinstalled, and both session commits passed through the repaired hook.
