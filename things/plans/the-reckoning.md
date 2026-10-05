---
id: the-reckoning
type: plan
status: in-progress
version: 1.1
created: 2026-10-05
session: 2026-10-05
priority: critical
tags: [digestion, reckoning, disposition, floor, session-end, dispatcher, closed-loop, insight, conflict, trigger, import]
linked_things:
  - id: the-reckoning-is-the-digestion-beat-2026-10-05
    relation: implements
    notes: "The ruling this plan builds: disposition gets an actor at a boundary, with the floor/agent/human split of the walk."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 3's seat queue: the reckoning's residue band is the one view that phase left open."
  - id: cue-carrier
    relation: references
    notes: "The walk gate's shape, reused: a floor command behind a boundary, prefilled by the floor, judged by the agent, ruled by the human."
  - id: session-memory-specification
    relation: extends
    notes: "The brake becomes a command and a gate."
  - id: retrospective-specification
    relation: extends
    notes: "Scans 5 and 6 become reads of the reckoning."
  - id: circulation-is-not-disposition
    relation: references
    notes: "The diagnosis this plan answers."
triggers:
  - type: time
    condition: "2026-10-19 reached"
    action: surface
    note: "Two weeks: has one attended session ended through the reckoning, and has one tick drafted one? If neither, the actor is the problem, not the command."
---

# Plan: The Reckoning

**What this delivers.** The release half of the loop. Every attention item in
a workspace — insight, conflict, cue, fired trigger, import, stale work —
carries an exit rule the floor can evaluate; one command computes every
item's disposition candidate with its evidence in three bands; the floor
applies the mechanical band, the agent decides the settled band, the operator
rules on the residue through the harness's own prompt; and the act has two
actors at boundaries the harness owns, the session-end commit and the
dispatcher's tick. Knowledge that survives is promoted into the operating
layer, where the walk gate keeps it coherent. A rate on the digest says
whether the chase is winning.

**What it does not deliver.** Any disposition of meaning by the floor. A
Codex binding (after Claude Code proves it). Hand-clearing of the nine
dormant workspaces.

## Phases

- [x] **Phase 0 — Record the ruling.** `the-reckoning-is-the-digestion-beat-2026-10-05`
      in the operator's words; this plan. *Done 2026-10-05.*
- [x] **Phase 1 — The floor reads.** *Done 2026-10-05: `mdllm reckon`, 16 tests; first live reads — root 4 mechanical / 50 settled / 0 residue, QMS 121 settled / 11 residue (its open conflicts in circulation), overview 0 residue once mirrors were left to their source, engineering 1 / 62 / 0.* `mdllm reckon [path]`: one view over every
      attention item with its computed disposition candidate and evidence,
      banded mechanical / settled / residue. Exit rules per type declared in
      `session-memory.md` (insight), `belief-revision.md` (conflict),
      `change-reconciliation.md` (cue), `trigger-specification.md` (fired
      trigger satisfied), `provenance.md` (import), `thing.md` (stale work);
      a per-item `settles_when` in trigger shape, evaluated by the trigger
      engine, overrides the default. Read-only; exit 0. Tests pin each band's
      predicate. Runs clean on the root.
- [ ] **Phase 2 — The floor applies, and the rate goes on the wall.**
      `reckon --apply` performs the mechanical band only — a status derivable
      from a field or a git fact — and prints the receipt; the `reckon:`
      commit convention. The session-start digest gains one line per
      workspace: created against disposed this week, open-age distribution,
      walks against definition-surface changes. First live run by hand on the
      QMS (20 open conflicts, 87 active insights) and overview (86): the
      residue counted and put to the operator.
- [ ] **Phase 3 — Two actors.** Attended: the commit-message leg refuses a
      `session-end:` commit while the mechanical band is pending; the
      session-end prompt runs the reckoning, decides the settled band by
      citation, and puts the residue through the native prompt. Unattended:
      the dispatch prompt's ritual applies the mechanical band, drafts the
      settled one and files the residue. Done when one attended session ends
      through it and one tick drafts one.
- [ ] **Phase 4 — Retention is promotion.** The promotion path: a surviving
      insight folded into a skill with `promoted_to` set, tripping the walk
      gate; `retrospective.md` scans 5 and 6 rewritten as reads of the
      reckoning and scan 7's promotion half pointed at it. Done when one
      insight promoted into a skill trips the walk.
- [ ] **Phase 5 — See the rate.** Four weeks of the digest line across the
      four live workspaces; thresholds decided from what it shows, not
      before. Done when the chase is visible and winning in all four.

## Done when

- [ ] An attention item cannot exist without an evaluable exit rule, and
      `mdllm reckon` names every item's candidate with evidence.
- [ ] A session cannot end with the mechanical band pending.
- [ ] One tick has reckoned a workspace unattended and filed its residue.
- [ ] The digest shows the rate, and in the four live workspaces disposed
      keeps pace with created over four weeks.
