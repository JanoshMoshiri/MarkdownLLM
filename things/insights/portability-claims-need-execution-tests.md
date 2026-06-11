---
id: portability-claims-need-execution-tests
type: insight
status: active
version: 1.0
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
- Candidate mechanical follow-up: `install-hook` could self-test by running
  the script it just emitted once (exit status only) and reporting
  floor-unavailable immediately, instead of leaving the discovery to the
  first blocked commit.

## Context

Surfaced when the first commit of `framework-map.md` was blocked on the
authoring machine by the freshly-"portable" hook (session 7, 2026-06-11).
Diagnosis: `(Get-Command python).Source` showed a real 3.12 install, while
both Store stubs existed in `WindowsApps` and git's sh resolved `python3` to
a stub. Fix landed in `tools/mdllm.py` `HOOK_BODY` (commit `32d5c6f`),
reinstalled, and both session commits passed through the repaired hook.
