---
id: dissolve-continuity-into-reconciliation
type: plan
status: completed
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
  - id: long-running-tasks-lack-pre-compaction-checkpoint
    relation: references
    notes: "The compaction-survival constraint rests on this named gap; keeping it live via a real dependant, not a prose mention"
  - id: orient-and-reconciliation-are-the-corpus-two-sides
    relation: references
    notes: "The conceptual capstone — orient (session-memory state) is the dual of reconciliation (work-content state); this plan operationalises orient's forward view"
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
- **A2 — the `## Live Insights` restatement (DONE 2026-06-27, after B).** Removed the
  whole section (143 lines, 459 → 316) once Phase B re-keyed liveness onto the graph,
  so the deletion changed no orphan findings (the check no longer reads the brief).
  Continuity is now forward-only (Open Threads), 316 lines from the original 733 — its
  spec. Also fixed the session-start prompt's staleness check to walk graph-live
  insights, not "live insights in continuity.md".

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

### Phase C — Forcing function at end-session + the keep-active marker (DONE 2026-06-27)
**Built.** (a) The keep-active marker (`disposition: keep-active` + `disposition_reason`,
read by the floor's orphan check) — applied to the 5 standing/parked insights, backlog
5 → 0, 97 tests pass. (b) The forcing function — the end-session ritual
(`session-end-continuity.md` + both `end-session` commands) gains a **mandatory
disposition step** between capture and the continuity update, so per-session capture is
paired with pruning; it also drops the now-defunct "maintain live insight IDs in the
brief" instruction (liveness is graph-keyed). The deeper period sweep stays the
retrospective's.

Bind a **mandatory** disposition pass to end-session (not only the periodic
retrospective). The floor lists retirement candidates — orphaned (no live inbound
edge), promoted-but-not-archived, duplicate-cluster (composition pre-filter).
End-session **must** disposition each (promote / dismiss / consolidate /
keep-active-with-reason). The brake lives at the same ritual as the growth, so every
act of capture is also an act of pruning. Retrospective keeps the deeper period-scoped
sweep. (No wall-clock "decayed" signal — the staleness window was dropped in B.)

**The keep-active marker (the backlog forced this).** A *deliberately parked* or
*standing-razor* insight is genuinely live but has no natural active dependant; it
must be recordable as keep-active in a way the floor reads, so it stops being flagged
without a fake edge. Design: a frontmatter field (e.g. `disposition: keep-active` +
a one-line `disposition_reason`) the orphan check honours. This is C's core build.

**Backlog triage (2026-06-27 — first run of this disposition pass, done by hand):**
of the 10 orphans the B re-key surfaced —
- **Promoted (3):** `reflexive-behaviors-are-indexes-plus-prompts` → derived-index.md;
  `version-mismatch-triggers-validation-cascade` → orchestration.md;
  `a-crossing-thing-carries-its-producers-private-graph` → mcp-domain-server-design
  (egress source-scoping shipped).
- **Linked to a real dependant (1):** `long-running-tasks-lack-pre-compaction-checkpoint`
  ← this plan (compaction-survival) — now live, off the backlog.
- **Dismissed (1):** `framework-reserved-types-need-thing-md-as-single-source` — fix
  shipped, residual is generic SRP on a stable type set.
- **Keep-active (5):** `boundary-respect-was-interpretation-not-enforcement`,
  `felt-deployment-lands-in-undisclosable-work`,
  `modeling-cognition-yields-a-learning-loop-not-a-coherence-loop`,
  `repeated-drift-promotes-a-fact-into-the-floor`,
  `cross-domain-readiness-is-a-shared-signal-not-a-producer-push` (parked). The
  **first customers of the keep-active marker** — flagged until C builds it. Backlog
  after this pass: **5**, all keep-active.

### Phase D — Generated orientation; retire the file (DONE 2026-06-27)
**D1 — the generator.** `mdllm session-start` now emits the **forward** view
(`_orient_forward`): open conflicts + non-terminal work things (knowledge/reference/
artifact types excluded), the complement to velocity's backward commit-stream read.
Header reframed "version+velocity (backward) and open-loops (forward)". Capstone
insight `orient-and-reconciliation-are-the-corpus-two-sides` captured (born live).

**D2 — migration + retirement (a retrospective-reconciliation of continuity itself).**
The 316-line brief was triaged: ~7 `[COMPLETE]`/done entries and the stale MCP entry
(it described the *reverted* Phase 3 as built) **dropped** — history is in git; 4
deferred uses/exercises **dropped** (reasoning preserved in git + insights); the
operator-chosen forward threads migrated to **3 plan things** —
`mechanical-coherence-checks-backlog`, `pretooluse-action-boundary-gate` (paused),
`evidence-and-eval-backlog`. **continuity.md deleted.** Rituals rewired: session-start
prompt + `session-orientation` (graph-keyed staleness check), session-end (manages
open-loop things, not a brief), `session-memory.md` (continuity-brief type marked
RETIRED/deprecated).

**Follow-ons (tracked, not done here):**
- The `continuity-brief` **type** stays reserved-but-deprecated; removing it from the
  floor (`thing.md`, `_schema`, reserved-status machinery, the orphan-check special-
  case) is a clean teardown for when domains have all dropped their `continuity.md`.
- **Cross-domain:** two jmtm items in the old brief (annual-accounts `decision`
  filing **due 2026-07-31**; 8 unlinked expense/profile records) belong to the jmtm
  domain, not the framework — move them into jmtm's own corpus (operator).
- `framework-v3-transformation-plan` shows as a stale in-progress open loop (orient
  working) — close it to `completed` if its phases are all done.

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
