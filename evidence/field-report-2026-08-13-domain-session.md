---
id: field-report-2026-08-13-domain-session
type: artifact
status: stable
created: 2026-08-13
tags: [field-report, session-gate, harness, ergonomics, execution-evidence]
linked_things:
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "The first of the day's two instances, and the one that produced a blocking failure in real work."
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "Availability was never in question here: the command ran and exited 0. What was missing was the side effect the contract rests on."
---

# Field report — live domain session, 2026-08-13

Four findings from an operator's real working session against a live
regulated deployment (Windows 11, Git Bash, framework 3.31.0; the domain
sealed at `framework_version_seen: 3.30.0` and declaring
`options: {session_gate: strict}`). Reported with empirical evidence rather
than inference, and fixed the same day in `f7acffd`.

These are framework defects found by use. They are deliberately **not**
folded into the `vendor-harness-adapter-foundation` record: different reason
to change, different reviewer, and mixing them would muddy a phase gate
mid-flight.

## Finding 1 — the session gate fired against the harness that satisfies it

**Severity: blocking.** Under `session_gate: strict`, every session opened
through the scaffolded hook began with a commit-blocking Error.

The scaffolded `SessionStart` hook runs the assistant rendering. That path
returned before the attestation write, so the attestation was never
recorded. Verified empirically by the operator, not inferred:

- validate at session start: Error, *"attestation is 28h old (window 24h)"*
  — left over from the previous day;
- ran the assistant form: exit 0, attestation file **unchanged**;
- ran the plain form: attestation **updated**.

So the one path bound to a harness was the only path that did not attest.
The domain's schema comment records that the gate was declared strict so
"a harness that skips the contract is stopped at its first write" — but this
harness does not skip the contract. It emits it, and was stopped anyway.

**Fix.** The attestation attests to *emission*, not to a rendering format,
and both paths emit. The write was extracted to one helper called by both.
The two alternatives were rejected on doctrine: teaching the gate to
recognise a specific rendering would make the gate know about formats, and
reverting the scaffolded hook to the plain form would discard the assistant
rendering the operator rates as genuinely good.

## Finding 2 — retrospective debt could never reach assistant output

**Severity: silent gap.** The cadence check appends to both the plain
output and the shared `exceptions` list, but sits *after* the assistant
branch — and `exceptions` is passed into that rendering already built. A
domain owing a retrospective was therefore never told so in the assistant
block's exceptions section.

Invisible in the field only because this domain had run its retrospective
two days earlier.

**Fix.** The cadence findings are computed above the branch and appended to
`exceptions` there; the plain rendering still emits them at their original
position, so its output ordering is unchanged.

## Finding 3 — `install-hook` silently exceeds a harness tool timeout

**Severity: ergonomics.** The command's execution test fires a real
pre-commit, which is a full validate. On a 214-thing domain,
`install-hook && validate` is two full passes — about five minutes — which
blew a 120-second agent tool timeout and read as a hang.

**Fix.** `--no-test` skips the execution test and downgrades the claim
honestly: *installed but unproven; it will first fire at the next real
commit*. A regression test asserts the skip path never reports "ran and
passed" — a skipped test must not borrow the stronger fact.

## Finding 4 — the assistant block named an unopenable file

**Severity: ergonomics.** The block closed with "load `kernel.md`". The
kernel is framework state, so from inside a domain that path does not
exist and the first read fails. AGENTS.md already states it correctly as
`{framework_root}/kernel.md`.

**Fix.** The resolved path is emitted. A regression test asserts the
reference is not the bare name *and* resolves to a real file.

## What worked, recorded so it is not changed by accident

- `estate-sync` ran clean and reported per repo;
- the assistant rendering itself — where-you-left-off, ranked attention,
  open loops, conflicts, backdrop — was rated genuinely good in use;
- the "Not working as it should" section correctly caught both the
  3.30.0 → 3.31.0 version drift and the stale git hooks, and both remedies
  it named were right;
- after clearing the gate: 214 things, 0 errors, 1 warning, 10 info.

None of the above was touched by the fixes.

## The pattern

Findings 1 and 3 are both cases of a harness-bound path behaving unlike the
path everyone tests, and finding 1 is the sharper one: the command ran,
exited 0, and produced correct output while omitting the side effect the
operator's contract depends on. A second, mechanically unrelated instance
appeared the same day in the adapter work, where a reconciled root's
orientation truncated inside a per-step budget while still exiting 0.

That pattern is captured as
[[the-harness-bound-path-is-the-least-tested-path]]: availability is not
sufficiency, and a harness-bound path earns an execution test that asserts
the *side effect*, not merely that the command ran.

## Verification

Four regression tests, each carrying the field date and the reason:
gate-satisfies-its-own-harness, cadence-reaches-both-renderings,
skip-must-not-claim-execution, kernel-must-be-openable. Full suite **460
passed** after the fixes (456 before, plus these four).
