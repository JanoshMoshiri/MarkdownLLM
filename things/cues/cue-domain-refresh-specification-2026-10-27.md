---
id: cue-domain-refresh-specification-2026-10-27
type: cue
status: answered
version: 1.0
created: 2026-10-27
subject: domain-refresh-specification
raised_at: 0e17b5269c4a935401791dfdead0278cbc9195f3
raised_by: "floor — mdllm cues --staged --raise"
verdict: not-inflection
verdict_reason: "A new subsection states what the floor now does with a behind pin; detection, the algorithm and the seal are unchanged, and every dependant reads the pin as a reminder the way it still is"
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `domain-refresh-specification` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-27: the spec is a
definition surface and changes in the commit this cue rides in. 6 thing(s)
depend on it. What moved: version 1.6 → 1.7; one subsection added under *The
Refresh Process* — **The Pin Governs Drift** — stating the floor behaviour
shipped in the same commit: while `framework_version_seen` is current,
differing managed blocks are an Error as before; while it is behind the
running framework, they are Info and `domain-kernel --check` prints
`PIN-BEHIND` with exit 0; debt is paid once at the bump; an unattended run may
regenerate but never seals. Detection (the session-start version check), the
refresh algorithm, `--seal`, and the backfill list are unchanged. The
dispatch prompt (`dispatch-loop` 1.6 → 1.7) gains the matching allowance in
the same commit; the floor did not raise it separately.

## The Walk
- [x] `framework-discovery-specification` — linked_things `complements` — **consistent**: how a domain finds the framework; nothing about drift
- [x] `operator-guide` — linked_things `references` — **consistent**: its `domain-kernel` when-line ("after a refresh, or when coherence reports a drifted managed block") still holds — coherence still reports it, as Info behind the pin and Error at it; the toolbox block is generated and unchanged
- [x] `orchestration-specification` — linked_things `implements` — **consistent**: the `session-start:version-check` hard hook detects the mismatch exactly as before; what changed is what the commit boundary does with it, which that hook never owned
- [x] `the-record-holds-unattended` — linked_things `extends` — **consistent**: this commit is its Phase 1; the plan's progress line is updated in this commit by its own author
- [x] `vendor-harness-adapter-foundation` — linked_things `extends` — **consistent**: adapter hardening of the version check is untouched
- [x] `version-mismatch-triggers-validation-cascade` — linked_things `informs` — **consistent**: a mismatch still cascades into validation at session start; the insight says what to do when the cheap check fires, not what the commit gate refuses
- [x] conceptual residue — `docs/estate-mechanics.md` (*derived everywhere reconciles by regeneration — one generator string*): **consistent** — still one generator; what changed is *when* a domain is held to it (at its pin, not at every release). `AGENTS.md` → *On Output* says a stale generated artifact blocks the commit: **consistent** — that sentence is about the framework root, which has no pin and is unchanged. `kernel.md`: carries no domain-refresh block; nothing to regenerate
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle.

## The Answer
Every line held. The spec gained a statement of a floor behaviour that did
not exist before; no dependant reasoned from the old behaviour in a way the
new one contradicts, because every one of them treats the pin as the
reminder it still is. **Verdict: not-inflection.** The operator approved
the plan this implements (`the-record-holds-unattended` Phase 1) earlier the
same day; the design — pin-behind as Info, debt paid at the bump, the
dispatcher regenerates but never seals — is the plan's text.
