---
id: dissolve-continuity-into-reconciliation
type: plan
status: in-progress
version: 1.0
created: 2026-06-27
priority: high
tags: [continuity, reconciliation, insight-lifecycle, session-memory, retirement, orientation]
linked_things:
  - id: change-reconciliation-specification
    relation: implements
    notes: "Orientation = reconciliation bound to the session boundary; backward = assimilate-from-history, forward = the open inflection set"
  - id: session-memory-specification
    relation: references
    notes: "Re-keys insight liveness off continuity.md presence; retires the continuity-brief singleton"
  - id: retrospective-specification
    relation: references
    notes: "The insight-triage beat is the retirement mechanism; add an end-session forcing function and re-key the orphan check"
  - id: derived-index-specification
    relation: references
    notes: "Graph in-degree (relationships index) is the new liveness signal"
  - id: git-workflow-specification
    relation: references
    notes: "The commit is the durable checkpoint — open-loop things survive compaction by being committed"
  - id: llm-driven-systems-manifesto
    relation: implements
    notes: "Fewer primitives: continuity stops being a primitive and becomes an application of reconciliation"
---

# Plan: Dissolve Continuity Into Reconciliation

## Organizing Principle (the reframe)

**Orientation is change-reconciliation bound to the session boundary instead of to
a change.** The two halves map exactly:

- **Backward** — "what happened / what is load-bearing now" = the
  retrospective-reconciliation *assimilate-from-history* mode = the commit stream
  (already the WORKLOG's job, already what velocity reads). Derivable, never
  hand-maintained.
- **Forward** — "what's open / what's next" = the set of **open inflections not yet
  resolved** = first-class non-terminal things. The irreducible authored residue.

So `continuity-brief` stops being a primitive and becomes an *application* of
reconciliation + the thing graph. Fewer concepts, not more — the project's own razor.

## What We Found (the diagnosis, sharpened)

1. **continuity.md violates its own spec.** It is defined forward-looking
   (session-memory.md: "Next session's agent"), but ~250 of its 733 lines are
   `## Decisions Made This Session` backward logs + a `## Live Insights` section that
   restates insight things. All of that is already in git, WORKLOG, and the
   decision/insight things. Only **Open Threads** + **Questions For Next Session** are
   legitimate forward residue.
2. **Insight liveness is welded to continuity.** session-memory.md:227–229: *"'Live'
   is defined by presence in continuity.md."* The floor orphan-check
   (`validate` Info) lists active insights *not in continuity.md*. So the file cannot
   die until liveness is re-keyed onto something else — which is precisely the #3
   retirement mechanism. #2 and #3 are one problem, welded at this line.
3. **The retirement engine mostly exists already** — the retrospective's
   **insight-triage** beat (promote / dismiss / consolidate / keep-with-reason) +
   its mechanical **orphan check** and **composition pre-filter**. The gaps are only:
   it is keyed to continuity (breaks on dissolution); it is bound to the *periodic*
   retrospective, so per-session capture outruns it; and it lacks a hard forcing
   function (relies on the driver remembering to triage).

## The Fade-Class (why insights specifically need a sweep)

Insights are the only thing-type whose end-of-life is a **fade, not an event**. A
task *completes*; a spec is *rewritten*; a domain thing is *cancelled* — the work
triggers retirement. An insight is never false; it just stops being load-bearing or
gets absorbed. Decay is not an event, so nothing triggers its retirement — which is
why insights, and only insights, rot into a pile. The same is true of parked
open-loops and deferred decisions. Anything fade-class needs a **periodic sweep**:
floor *detects + surfaces* candidates, agent *dispositions*, human *cues* the
consequential calls. Same constitutional line as reconciliation — the floor makes
you unable to not-see; it never decides for you.

## Phases

### Phase A — Strip continuity to its spec (independent; do first)
The audit split this in two by what each cut depends on:

- **A1 — backward session logs (DONE 2026-06-27).** Removed the `## Pending
  Decisions` placeholder and all 11 `## Decisions Made This Session` blocks
  (~274 lines, 733 → 459). Audited recoverable first: every block points to its
  home (retrospective things, named commits, insight things, spec changes in git);
  the operator was already hand-pruning these to WORKLOG (the oldest block said so).
  Pure enforcement of the forward-only spec; nothing promoted because nothing was
  orphaned.
- **A2 — the `## Live Insights` restatement (GATED on Phase B).** It is redundant
  with the insight things, but deleting it *now* would orphan every insight under
  the current "live = presence in continuity.md" rule and the `validate` orphan
  check. So it can only go once Phase B re-keys liveness onto the graph. ~140 lines,
  removed in B.

### Phase B — Re-key insight liveness off continuity onto the graph (DONE 2026-06-27)
**Built.** The floor now computes `referenced_by_live` (inbound edges whose source
is non-terminal) and keys the insight/conflict orphan check on it instead of
continuity-brief text; the check is no longer brief-gated. `session-memory.md` and
`retrospective.md` redefine **live** as "an inbound edge from a non-terminal thing";
the session-start prompt no longer asserts brief-presence liveness. Tests re-keyed
(graph liveness + the terminal-source-doesn't-count case); 96 pass.

**Outcomes:**
- The re-key surfaced an **11-insight backlog** (active insights kept live only by
  prose, nothing in the graph pointing back) — the real worklist, previously hidden.
- `agents-drop-mechanical-birth-steps-not-semantic-ones` **promoted** → it had only
  outbound edges (discharged into `orchestration.md` / `mdllm scaffold`); status
  `promoted`, `promoted_to: orchestration-specification`. Backlog now 10.
- **Decided here (was an open question):** dropped the wall-clock staleness window —
  liveness is purely structural (inbound from a live thing). A wall-clock grace makes
  `validate` time-dependent/flaky and, more importantly, no-grace is *more* faithful
  to "link rather than mention": a new insight should be linked from the work it
  informs, not kept live by age. Newborn-grace is handled instead by a keep-active
  disposition (below), not by a timer.
- **New Phase C input (surfaced here):** a *deliberately parked* insight (e.g.
  `cross-domain-readiness-…`, "capture don't decide", awaiting a trigger) legitimately
  has no live inbound edge and should not be flagged forever. The fix is a
  **keep-active disposition the floor reads** (a frontmatter marker / stated reason
  that exempts it), not a prose mention — built in C alongside the forcing function.

The original plan text for B:
In session-memory.md, redefine **live**:
`active` ∧ (inbound edge from a non-terminal thing ∨ within a staleness window).
Re-point the floor orphan-check from "not in continuity.md" to "no inbound edge from
a non-terminal thing" (the `relationships` index already computes in-degree). The
session-start staleness check walks this graph set, not the brief's live IDs.

**Concrete first case (surfaced live by A1):** removing the backward logs orphaned
`agents-drop-mechanical-birth-steps-not-semantic-ones` — it had been kept "live"
only by a mention in a deleted decision-log block. It is **in-degree 0** yet
`informs orchestration-specification` and motivated `mdllm scaffold`, so its lesson
already crystallised into a shipped spec → a **promotion**, not a re-hide. Carried
as a known transitional `validate` Info (non-blocking) until B re-keys liveness;
this insight is B's first disposition. It is the live proof that file-presence
liveness is brittle — a backward-log cleanup should never orphan a standing insight.

### Phase C — Forcing function at end-session
Bind a **mandatory** disposition pass to end-session (not only the periodic
retrospective). The floor lists retirement candidates — orphaned (no live inbound
edge), decayed (active past the staleness window, never built on),
promoted-but-not-archived, duplicate-cluster (composition pre-filter). End-session
**must** disposition each (promote / dismiss / consolidate / keep-with-reason). The
brake lives at the same ritual as the growth, so every act of capture is also an act
of pruning. Retrospective keeps the deeper period-scoped sweep.

### Phase D — Generated orientation; retire the file
`mdllm orient <domain>` generates the session-start view: **backward** (recent
commits / velocity, already there) + **forward** (open-loop things, open conflicts,
Questions). Migrate continuity's remaining forward residue into open-loop things.
Retire continuity.md the file; update session-memory.md, the session-start hook
(orchestration.md), the scaffold, and `templates/`. Orientation is now a generated
join — nothing hand-maintained.

## Dependencies & Ordering
A (independent, now) → B (liveness must leave the file before the file dies) →
C (forcing function uses the re-keyed candidates) → D (completes the dissolution).
A delivers standalone value and could be the whole win if we stop there.

## Compaction-Survival (a constraint, already satisfied)
Forward intent must be cheap to write *as you go*, or a mid-session compaction loses
it. Open-loop things are committed things, and "the commit is the moment state
becomes real" (git-workflow.md) — so an open loop written mid-session survives
compaction by being committed. No new mechanism required; just write+commit the loop
when it appears, not only at session-end.

## Out Of Scope / Deliberately Not Doing
- No new primitive invented; continuity becomes an application of existing ones.
- No auto-deletion: floor surfaces, agent dispositions, human cues. Same line as
  reconciliation and as the "mechanize?" answer.
- change-reconciliation's *correctness* model (maintained at change) is untouched;
  this is the *quality* sweep, the retrospective's sanctioned territory.

## Open Design Decisions (defer to felt need during the build)
- Do open-loops need a dedicated `type`, or reuse existing non-terminal things
  (deferred `decision`, `plan`, deferred `insight`, in-progress `workflow-run`)?
  Lean: reuse; add a type only if felt.
- Is `orient` a new subcommand or folded into `mdllm session-start`? Lean: extend
  session-start.
- The staleness window N (days) for the decayed-insight signal — pick on first run.
