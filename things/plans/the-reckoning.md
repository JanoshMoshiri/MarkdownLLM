---
id: the-reckoning
type: plan
status: in-progress
version: 1.6
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
    condition: "2026-11-02 reached"
    action: surface
    note: "Four weeks of the rate line (Phase 5): does disposed keep pace with created across the four live workspaces? The two-week question was answered yes on 2026-10-20 — one attended close (2026-10-08) and one tick's draft (2026-10-11), both recorded in Phase 3."
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
- [x] **Phase 2 — The floor applies, and the rate goes on the wall.** *Done 2026-10-05: `--apply` writes the mechanical band in place (promote, resolve, complete; never a trigger), `--rates` and the digest line; first live reads by hand — QMS residue 11 (its open conflicts in circulation, put to the operator the same day), overview 0 once mirrors were left to their source. The `reckon:` prefix enters git-workflow's table the way prefixes do: after use.*
      `reckon --apply` performs the mechanical band only — a status derivable
      from a field or a git fact — and prints the receipt; the `reckon:`
      commit convention. The session-start digest gains one line per
      workspace: created against disposed this week, open-age distribution,
      walks against definition-surface changes. First live run by hand on the
      QMS (20 open conflicts, 87 active insights) and overview (86): the
      residue counted and put to the operator.
- [x] **Phase 3 — Two actors.** *First use by hand, 2026-10-08: the
      framework root's session end applied the mechanical band (three insights
      already promoted in fact, one plan with every box ticked). One friction
      seen at once: the walk gate owed a walk for each insight whose only
      change was the status the reckoning applied. A disposition-only change,
      status and its resolution fields, should not be a walk candidate;
      build that with the gate here.* *Built 2026-10-08, shape agreed with the
      operator that morning (the decision's 10-08 refinement): `mdllm reckon
      --close` — the mechanical band, then ten decisions a day from one
      oldest-first queue, the residue leading and at most four, the time-bound
      kinds ahead of the rest; `--keep` writes a hold and its next look; a
      hold leaves the band until that date; a disposition-only change owes no
      walk at the gate or in the cue listing; the gate's step asks a
      `session-end:` commit the close's question, flagged by the runner from
      the command, so no projection changed and every seat has it without a
      refresh; the session-end prompt and its three command copies run the
      close; the dispatch prompt applies, drafts and files. The first live
      read: the root met (ten decisions that day), the engineering workspace
      owing its mechanical item and the binding of its specification loop.
      Waits on the evidence: one attended close through it, one tick's
      drafts.* *Attended half, 2026-10-08: the framework root's close ran
      through it — ten items off the oldest end of the queue: four insights
      promoted into the specs that already carry them, five held with a
      reason and a look-again date, one fired trigger acted on and re-dated;
      the backlog 45 → 35, the gate owing no walk for the nine disposed
      insights, and the `session-end:` commit passing the gate's close leg.
      The tick's half waits on the next scheduled run.* *Tick's half,
      2026-10-10: the dispatcher's 08:30 run reckoned the busiest live
      workspace unattended — applied the mechanical band (a plan with every
      box ticked → completed), committed it alone as `reckon:`, and filed a
      `## Reckoning` section in its digest. It drafted nothing: the close
      told an unattended run "met" once the mechanical band was applied and
      hid the owed list it exists to draft. Fixed the same day; the live
      unattended close now hands it eight items, the four emerged workflow
      bindings first. Phase 3 ticks when one run drafts.* *Done 2026-10-11:
      the next run drafted five decisions under `## Reckoning` in its digest —
      the four emerged workflow bindings, each citing the floor's own count,
      and one hold citing the record — applied none, and said the bindings
      belong to an attended session because they change a definition
      surface. The 2026-10-13 run found the close already met by that day's
      attended decisions.* Attended: the commit-message leg refuses a
      `session-end:` commit while the mechanical band is pending; the
      session-end prompt runs the reckoning, decides what the close owes by
      citation, and puts the owed residue through the native prompt. Unattended:
      the dispatch prompt's ritual applies the mechanical band, drafts the
      settled one and files the residue. Done when one attended session ends
      through it and one tick drafts one.
- [x] **Phase 4 — Retention is promotion.** *Built 2026-10-20 as
      `run-reckoning-phase-4-2026-10`, the definition's first run with a
      second seat — Claude built, Codex reviews once at the pinned commit,
      the operator seals. The promotion path's evidence was already on the
      record: the 2026-10-17 promotion of `change-safety-is-defense-in-depth`
      into change-reconciliation.md tripped the walk gate on the spec it
      entered (`cue-change-reconciliation-specification-2026-10-17`).
      `retrospective.md` 1.9 reads scans 5 and 6 off `mdllm reckon` and
      points scan 7's promotion half at it; `reckon --composition` carries
      the pre-filter (opt-in, a shared spec weighted zero); `reckon --keep`
      writes one field set on work and insights alike, and the three plans
      it had held without the marker were migrated. The phase ticks on the
      build; the run closes on the review.* The promotion path: a surviving
      insight folded into a skill with `promoted_to` set, tripping the walk
      gate; `retrospective.md` scans 5 and 6 rewritten as reads of the
      reckoning and scan 7's promotion half pointed at it. Done when one
      insight promoted into a skill trips the walk. *Scope added 2026-10-17
      at the retrospective: scan 5's composition pre-filter (insights sharing
      two or more `linked_things` targets, weighted so a shared specification
      counts for less than a shared insight or decision) has been scripted by
      hand at two retrospectives running and found the same spec-dominated
      noise both times — it belongs among the reckoning's reads when scans 5
      and 6 are rewritten, not in a retrospective's scratch script. The
      2026-10 retrospective ran scans 5 and 6 as reads of `mdllm reckon`
      (its settled band supplied the triage list and the held reasons) with
      the spec text unchanged — the first evidence for this phase, not its
      completion.*
- [ ] **Phase 5 — See the rate.** Four weeks of the digest line across the
      four live workspaces; thresholds decided from what it shows, not
      before. Done when the chase is visible and winning in all four.

## Done when

- [ ] An attention item cannot exist without an evaluable exit rule, and
      `mdllm reckon` names every item's candidate with evidence.
- [x] A session cannot end with the mechanical band pending. *Where the
      harness projects the gate (Claude Code), since 2026-10-08; Codex with
      `cue-carrier` (g).*
- [x] One tick has reckoned a workspace unattended and filed its residue.
      *2026-10-10 applied, 2026-10-11 drafted; no residue was owed.*
- [ ] The digest shows the rate, and in the four live workspaces disposed
      keeps pace with created over four weeks.

## Trigger answered 2026-10-20

The two-week check fired on 2026-10-19 and the answer is yes on both counts: the framework root's session end ran through the close on 2026-10-08 (ten decisions off the oldest end of the queue), and the dispatcher's 2026-10-11 run drafted five decisions under `## Reckoning` in its digest. Re-dated to 2026-11-02 for Phase 5's question — four weeks of the rate line.
