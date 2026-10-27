---
id: cue-operator-guide-2026-10-27
type: cue
status: answered
version: 1.0
created: 2026-10-27
subject: operator-guide
raised_at: 0ca893d3178f3928dcd517c4972ca0f1bfa3a240
raised_by: "floor — mdllm cues --staged --raise"
verdict: not-inflection
verdict_reason: "One authored when-line gains a clause for a new flag; the toolbox block regenerated from the CLI; no dependant describes the command's modes in a way the clause contradicts"
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `operator-guide` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-27: the guide is a
definition surface and changes in the commit this cue rides in. 27 thing(s)
depend on it. What moved: the authored when-line for `estate-sync` gains a
clause — `--silence-exit` from a scheduled task, to be rung (exit 5) when
the dispatcher has gone quiet; the silence line prints at every session
start regardless, only when the newest dispatch digest is older than twice
the cadence the digests show. The generated toolbox block was regenerated
by `mdllm docs` from the CLI's own help (the new flag's help text). No other
line moved. The flag and the line are `the-record-holds-unattended`
Phase 2, shipped in the same commit.

## The Walk
- [x] `documentation-rulings-2026-10-20` — linked_things `informs` — **consistent**: the wording ruling; the clause uses *operator* and *workspace* as ruled
- [x] `first-hour-guide` — linked_things `complements` — **consistent**: names `estate-sync` at session start only; the flag is not a first-hour act
- [x] `framework-map` — linked_things `complements` — **consistent**: lists the subcommand in View 3; flags are not drawn
- [x] `glossary` — linked_things `complements` — **consistent**: *standing watch (the doorbell)* and *dispatcher* rows describe the ring's purpose; the flag is one way to pull the bell
- [x] `limitations-guide` — linked_things `complements` — **consistent**
- [x] `review-documentation-audit-2026-10-20-claude` — linked_things `informs` — **consistent**: audited the toolbox's completeness, which is now mechanical; the authored one-liners stay judgement and this is one
- [x] `assistant-register` — names it in the body — **consistent**: how awareness is *said*; the silence line's register follows the attention-first ordering it set
- [x] `cross-domain-sync-catchup` — names it in the body — **consistent**: historical
- [x] `cue-carrier` — names it in the body — **consistent**
- [x] `derived-transport-is-not-derived-content` — names it in the body — **consistent**: the toolbox block is derived transport, regenerated here as it says
- [x] `deterministic-calculation` — names it in the body — **consistent**
- [x] `estate-git-sync` — names it in the body — **consistent**: the plan that built `estate-sync` with its two modes; a third flag added after its completion does not change what it recorded building
- [x] `explorer-white-label-presentation-2026-09` — names it in the body — **consistent**: paused; unrelated surface
- [x] `framework-retrospective-2026-06d` — names it in the body — **consistent**: historical
- [x] `framework-upward-signal` — names it in the body — **consistent**: paused; its estate read is a different read
- [x] `harness-native-onramp-supersedes-desktop` — names it in the body — **consistent**
- [x] `independent-review-2026-06-11-fable` — names it in the body — **consistent**: historical
- [x] `independent-review-2026-07-02-fable` — names it in the body — **consistent**: historical
- [x] `markdownllm-desktop-is-primary-accessible-product` — names it in the body — **consistent**: superseded decision; unrelated
- [x] `membrane-attention-cluster` — names it in the body — **consistent**: the membrane's attention; the silence line sits beside it in the same attention band and does not change it
- [x] `public-docs-face-build` — names it in the body — **consistent**: built the toolbox's generated/authored split this edit respects
- [x] `response-depth-control` — names it in the body — **consistent**
- [x] `review-holistic-substrate-2026-10-21-codex` — names it in the body — **consistent**: a review of the record at a date
- [x] `review-loop-2026-08-10` — names it in the body — **consistent**: historical
- [x] `run-floor-sprint-1-2026-08` — names it in the body — **consistent**: a completed run
- [x] `run-floor-sprint-3-2026-08` — names it in the body — **consistent**: a completed run
- [x] `scaffold-carries-the-universal-workflow` — names it in the body — **consistent**
- [x] conceptual residue — `docs/estate-mechanics.md` describes `estate-sync` as fetch + ff-only at session start: **consistent** — still what it does; the silence read is a line it prints, not a mode of syncing. `docs/first-hour.md`: nothing to add — the flag is for a scheduled task, not a first session
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle.

## The Answer
Every line held. An authored one-liner gained a clause for a flag shipped in
the same commit; the derived block followed the CLI. **Verdict:
not-inflection.**
