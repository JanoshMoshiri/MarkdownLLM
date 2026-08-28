---
id: gates-census-2026-08
type: artifact
status: stable
version: 1.1
created: 2026-08-27
session: 2026-08-27
tags: [gates-census, closed-loop, human-seats, phase-1, verdicts]
informed_by:
  - id: closed-loop-operating-state
    commit: 8f6d92c2b498ce18c2314fd7001c97a2ddcf5ca0
  - id: framework-retrospective-2026-08c
    commit: 7bffcb162f01c5cc6afb98756eca58bc5c5f79fe
linked_things:
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 1's output: the walk of every point where a session waits on the operator, each carrying a proposed verdict. Ratification flips this artifact evolving -> stable and produces the batch decision."
  - id: framework-retrospective-2026-08c
    relation: derived-from
    notes: "The retrospective posed the question — a census of gates, not a feeling. This is the census."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The classifier: consequence-gated (irrecoverable after the fact — stays human) versus familiarity-gated (a habit of the builder's presence — moves to structure)."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: references
    notes: "Row 7's doctrine: authority grants and permission-bearing installations are structurally the human's."
---

# Gates Census — August 2026

Phase 1 of `closed-loop-operating-state`, executed. Source material: the
doctrine surfaces (kernel, AGENTS.md, the six operative specs) at read base
`commit:f6ff5caa286b414e01ce982243f9e3916267ead3`, the commit stream, and the
open-loop plans carrying human-gated holds. Run concurrently with a live
Explorer session in the same repository — staged by explicit path; the v3.36
index-view floor is what makes concurrent commits safe at the boundary.

**The classifier** (from the 08c retrospective): a gate is
**consequence-gated** when the act it guards cannot be recovered after the
fact — it stays, and is named as a seat. A gate is **familiarity-gated** when
the human is present only because the human has always been present — it
moves to structure, with the mechanism named. Seats 1 (option-selection) and
2 (ambiguity) are *designed* human seats: the census confirms them rather
than moving them.

**Verdict key:** S1/S2/S3 = stays, at that seat · MOVE = familiarity-gated,
mechanism named · SPLIT = agent proposes, human ratifies at cadence.

## The Table — gate classes, with proposed verdicts

| # | Gate | Where it lives | Verdict | Mechanism / note |
|---|---|---|---|---|
| 1 | Push of the framework root (public release) | git-workflow.md; autopush declared false at root | **S3** | The release stays the deliberate act. This one gate wraps every root change in operator review — which is what lets rows 15/17 move. |
| 2 | Granting publication authority (`autopush: true` per repo) | git-workflow.md; estate-wide-autopush-2026-08-22 | **S3** | One-time standing grant per repo; publication never comes from silence. |
| 3 | Remote creation + first publish of a new domain | pre-domain-scaffold:isolate, step 5 | **S3** | Scaffold does steps 1–4 transactionally; the remote stays human. |
| 4 | `verified` flips on external things | thing.md quarantine; floor rejects born-verified and unattributed flips | **S3** | Regulated estates rest on this; `verified_by` names the human. |
| 5 | History rewrites and deletion of committed record | the 2026-07-27 privacy rewrite class | **S3** | Erasure is the least recoverable act in a system whose state is its history. |
| 6 | Money and external-party effects | domain radius (payments, filings, messages to people) | **S3** | Estate-wide; no domain automates these regardless of its autonomy. |
| 7 | Authority grants and permission-bearing installations (the dispatcher included) | agents-cannot-self-install-permission-bearing-hooks | **S3** | The one *constructive* class only the human can perform. Phase 2 needs exactly one of these. |
| 8 | Boundary-terms file contents | mdllm boundary; operator-owned, never committed | **S3** | The floor holds an invariant over the list; the list itself is the operator's. |
| 9 | Conflict resolution (belief revision rulings) | belief-revision.md; conflict things | **S2** | Stays as designed. Agent supplies proposed direction with evidence (08c's conflict already carries one). |
| 10 | Convergence and boundary calls (which domain owns a fact; supersede vs revise) | change-reconciliation.md; membrane rulings | **S2** | Stays as designed; the structure surfaces, never defaults. |
| 11 | Retrospective outputs with genuine alternatives | retrospective.md → What Should Change | **S1** | Stays as designed; arrives as option briefs with evidence, never homework. |
| 12 | Stall routing (park / re-scope / schedule) | the 21-day stall line | **SPLIT** | Agent proposes a disposition with a default and evidence; operator picks at seat cadence. Two instances queued today. |
| 13 | Deploy-when-felt lifts | the deploy-when-felt doctrine (derived-index.md, coordination-claim.md, the hold rulings) | **S1** | Only the operator can feel; the floor dates the chase so the wait is never silent. |
| 14 | Operator-calendar work (evals, undisclosable runs, felt-input sessions) | operator-gated-work-is-scheduled-on-the-operators-calendar | **S1** | Stays by nature; scheduled, not ambient. |
| 15 | Ritual-sanctioned spec updates (additive scans, tracking corrections, status truthing, kernel regen, index rebuilds) | retrospective.md item 4; the floor | **MOVE** | Already agent-run, proven at 08c. At the root, row 1's push gate is the review seat. At autopushing repos, stable-surface *redefinitions* queue at S1 first — additive changes flow. |
| 16 | Session launch and ritual invocation (orient, retrospective, session-end, sweeps) | bound prompts; the 08b dated chase | **MOVE** | The dispatcher (Phase 2): scheduled launches with exogenous stop conditions. The chase pattern stays as the portable floor. |
| 17 | Insight triage, dispositions, promotions | session-memory.md; 08c evidence | **MOVE** | Agent-run; promotions into specs inherit row 15's logic. |
| 18 | Priority and status assignment at write | write.thing.md cascade | **MOVE** | Agent proposes at write; contention escalates to S1. |
| 19 | Reconciliation walks and coherence fixes | change-reconciliation.md; mdllm coherence | **MOVE** | Already moved — floor plus rituals; the cues fire at commit. |
| 20 | Estate sweeps and imports-check runs | estate-sync; membrane clocks | **MOVE** | Scheduled once the dispatcher lands; divergence still *reported never resolved* (S2 on contact). |

**The census's own headline:** eight of twenty gate classes are
consequence-shaped and permanent. Six are designed seats working as designed.
Six are familiarity-shaped and move to structure — and four of those six have
already moved in practice; only the dispatcher (16) and the write-time
proposals (18) need building. The operator's standing surface, ratified,
becomes: **four seats, one push, one feel.**

## The Live Queue — what waits on the operator today

**Seat 2 (ambiguity):**
- `hard-hook-vocabulary-contradicts-observable-trigger-insight` — open
  conflict, proposed direction attached (both-valid via the anchor
  distinction; revise the insight).

**Seat 1 (options):**
- `thing-lifecycle.md` ruling — the corpus (287 things) is inside the spec's
  own 200–300 ceiling; reconcile or park, with reasons.
- `deterministic-calculation` closure — unruled for two retrospectives.
- Stall routing ×2 — `response-depth-control` (26d), `cohesiveness-sensors`
  (22d); dispositions proposed at ratification sitting.
- Razor doctrine promotion + portability rule/log split — approved-and-routed
  at 08c; **if row 15's verdict is ratified, both downgrade to agent
  execution** with row 1's push as the review.

**Seat 3 (irreversibles):**
- The push — the root sits at +14 unpushed and climbing while the Explorer
  arc is in flight; push when that arc closes, as one deliberate act.
- Ratification of this census — one sitting; produces the batch decision and
  flips this artifact to `stable`.
- The dispatcher authority grant — Phase 2's precondition, one act per
  harness.

**Seat 4 (breakage):** empty. The floor reports zero findings at 287 things.

## Ratified — 2026-08-28

**All twenty verdicts confirmed as proposed; no row flipped.** Recorded in
`gates-census-ratified-2026-08-28`, which also rules Phase 4's pilot domain.
This artifact is `stable`: the table below is now the estate's ratified seat
map rather than a proposal, and the eight consequence-permanent rows are the
confirmed exclusion list that `settled-reasoning-is-standing-authority` had
been resting on by reference.

Three Tier-1 items were deliberately *not* ratified here and stay the
operator's: the dispatcher authority grant (row 7's own class), the release
push, and the two stale mirrors' `verified` re-flips.

## What Ratification Looked Like

One sitting, three acts: confirm or flip each verdict in the table (a batch
`decision` thing records the result and this artifact goes `stable`); rule
the Seat 1 queue with the proposed defaults or against them; perform or
schedule the Seat 3 acts. Anything flipped from MOVE back to a seat is not a
defeat — it is the census doing its job: the line between gate and habit is
the operator's to draw, and this table is a proposal, not a verdict on the
operator.
