---
id: cue-workflow-state-specification-2026-10-07
type: cue
status: answered
version: 1.0
created: 2026-10-07
subject: workflow-state-specification
raised_at: 374b59657de2fb3b07edf8148a2cfdfbddf83a65
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "The spec gained two rules — carrier binding, and workflows that emerge from use — with no dependant revised: explicit runs, pins, membership and edge checks are untouched, and every dependant reasons from those."
informed_by:
  - id: workflows-emerge-from-use-2026-10-07
    commit: 374b59657de2fb3b07edf8148a2cfdfbddf83a65
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `workflow-state-specification` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-07: `workflow-state-specification` is a
definition surface (`specification`) and changes in the commit this cue rides in,
on top of `374b596`. 17 thing(s) depend on it: `a-check-is-only-as-trustworthy-as-who-controls-its-inputs`, `a-transcribed-identifier-is-unverifiable-by-reading`, `an-advisory-is-scoped-by-who-can-perform-its-remedy`, `between-sessions-surface-is-real-2026-09-21`, +13 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `a-check-is-only-as-trustworthy-as-who-controls-its-inputs` — linked_things `informs` — **consistent**: explicit runs keep the edge check the candidate cannot rewrite; a carrier departure is reported, never self-authorised
- [x] `a-transcribed-identifier-is-unverifiable-by-reading` — linked_things `informs` — **consistent**: the pin rules for explicit runs are untouched
- [x] `an-advisory-is-scoped-by-who-can-perform-its-remedy` — linked_things `informs` — **consistent**: the zero-run check's population rule stands; Phase 2 counts carrier things as runs, which keeps its remedy performable
- [x] `between-sessions-surface-is-real-2026-09-21` — linked_things `references`; informed_by pin — **consistent**: history
- [x] `coordination-claim-specification` — linked_things `complements` — **consistent**: a carrier thing may carry the same advisory claim a run thing did
- [x] `cross-domain-handoff-is-verified-external-input` — linked_things `informs` — **consistent**: mirrors are their source's runs, said in the new section
- [x] `operating-model-specification` — linked_things `extends` — **consistent**: 'each demand is instanced as a run' holds; under a carrier binding the instance is the carrier thing, which the new section names
- [x] `review-independent-operating-model-2026-08-26-codex` — linked_things `validates` — **consistent**: history
- [x] `run-membership-is-realisation-2026-09-22` — linked_things `informs`; informed_by pin — **consistent**: membership through `implements` is unchanged for explicit runs; a carrier thing is its own run and needs no membership edge
- [x] `standing-watch-specification` — linked_things `complements` — **consistent**: `watch --run` scopes an explicit run's members, unchanged; watching a carrier-bound workflow is a later consumer, not a contradiction
- [x] `structural-pointers-need-reverse-edge-indexing` — linked_things `informs` — **consistent**: `definition` stays the structural pointer; `carrier` names a type, not a thing, so it adds no edge to index
- [x] `substrate-floor-development` — linked_things `implements` — **consistent**: the root's own definition runs through explicit runs and stays so
- [x] `substrate-native-a2a` — linked_things `extends`; informed_by pin — **consistent**: its turn-taking runs through ticket and spec statuses, which is exactly the carrier shape the section now names; a candidate for binding, not a contradiction
- [x] `universal-workflow-methodology` — linked_things `implements` — **consistent**: the seven stages are the general method; emerged workflows are domain specialisations of it, as authored ones are
- [x] `workflow-run-is-the-decomposition-principle-applied-to-processes` — linked_things `informs` — **consistent**: definition and instance stay separate things; binding chooses the existing work thing as the instance rather than minting a pointer beside it
- [x] `workflows-emerge-from-use` — linked_things `extends` — **consistent**: the plan this section is Phase 0 of
- [x] `workflows-emerge-from-use-2026-10-07` — linked_things `informs`; informed_by pin — **consistent**: the ruling the section encodes
- [x] conceptual residue — `docs/operator-guide.md` and the routing table name `workflow-state.md` for run-state; their descriptions still hold and gain the carrier when Phase 2 ships the command: **consistent** for now
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `workflow-state-specification` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
**Inflection, nothing revised.** Two new sections add rules the spec did not have; every one of the seventeen dependants reasons from explicit runs, pins, membership or the edge check, which the new sections leave untouched by construction. Walked by the agent on detection, within the four bounds.
