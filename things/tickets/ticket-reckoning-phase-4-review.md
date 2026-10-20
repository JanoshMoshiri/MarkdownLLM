---
id: ticket-reckoning-phase-4-review
type: ticket
status: claude
created: 2026-10-20
tags: [a2a, ticket, review, the-reckoning, substrate, two-seat]
linked_things:
  - id: run-reckoning-phase-4-2026-10
    relation: implements
    notes: "The run this review is the verify stage of; the ticket is the turn token between its two seats."
  - id: the-reckoning
    relation: references
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: references
    notes: "One ticket per work item; the work item is this run's review."
---

# Review: Reckoning Phase 4 — Codex to Claude

Reviewed **commit:e5de9fa4081227fc06c26c331d5222117a4d95b8** once, in an isolated checkout of that revision. This is the requested review of the build, not a seal or approval to publish. No Phase 4 implementation fixes were made.

## Findings

1. **Defect — composition ranking is lost in the final report.**
   `tools/markdownllm/reckon.py:506` re-sorts every band by `(kind, thing_id)`, undoing `composition_candidates()`'s weight-first ordering at line 550. Reproduced with a pair `z-high-1 <> z-high-2` sharing three non-spec targets, `a-low-1 <> a-low-2` sharing one non-spec target plus a spec, and a zero-weight spec-only pair. The helper returns high, low, spec-only; the report displays low, spec-only, high. Preserve the helper's ranking when exposing composition items. `tools/tests/test_reckon.py:705` only checks helper order, and its strongest pair is also alphabetically first; the later report assertions check membership. Add a report-level check whose strongest pair sorts last by id. **Confirmed by execution at the pinned revision.**

2. **Defect — the ticket declaration alone does not provide an armable root watch.**
   `_schema.yaml:48` makes the ticket valid, but the pinned tree has no `ad-hoc-message-loop` definition. The only root lifecycle definition, `things/workflows/substrate-floor-development.md`, declares no stage actors; `tools/markdownllm/watch.py:508` refuses a missing definition and lines 542–551 refuse an actorless one. The request was committed only in the MAIN clone, whereas origin/main still held the release; an origin/main watch could not see it either. Thus the request was readable manually, but not yet deliverable through the requested A2A watch. **Confirmed by the pinned-tree inventory, the arming code, and local/remote ref reads. Operational remedy, separately authorised by the operator's request to turn on the watch:** commit `ac74fa95b74cee40bde5270dbe5da0d28867566a` instantiates the shipped Claude/Codex ticket-loop template, with no new gate, in both local checkouts. My run-scoped watch now reads MAIN through its local Git ref, with a persisted state file and a blocking command attached to this active turn. No GitHub release publication was made.

3. **Drift — scan 5 omits the spec-only inclusion exception.**
   `retrospective.md:132`, `templates/commands/retrospective.md:48` and the other three command surfaces describe a shared spec as counting for nothing, without stating that a pair sharing only specs is still admitted once it shares three. `tools/markdownllm/reckon.py:547` implements that exception correctly, and treats specification, manifesto and guide as spec targets. State the exception in the authored rule so the documented inclusion criterion matches the implemented one. **Confirmed by execution: two shared spec targets excluded; three included at weight zero.**

4. **Drift — the Copilot surfaces still omit the next retrospective chase.**
   `templates/copilot-prompts/retrospective.prompt.md:62` and `.github/prompts/retrospective.prompt.md:62` go straight to the commit, while `templates/commands/retrospective.md:61` and `.claude/commands/retrospective.md:61` arm the next chase and disarm the answered one. `retrospective.md:94` requires that handover. **Pre-existing drift, not introduced by this build:** the same difference is present in the parent revision. The requested scans 5–7 otherwise agree across the four command surfaces. **Confirmed by file comparison and parent-revision grep; no runtime test.**

## Checks and non-findings

- Three focused existing tests passed: composition, a work hold, and validation of the hold written by `keep()` (`3 passed, 36 deselected`). The full suite remains the builder's gate.
- Focused probes confirmed mirror exclusion, the default composition opt-out, the two/three-spec threshold and the report-order defect. The existing composition fixture covers the helper's common cases, not the whole ordering/threshold/exclusion contract.
- All three migrated plans remain valid holds. Their status and next-look behaviour is identical with and without the new marker: Explorer publication readiness is blocked until 2027-01-18, floor structure residue is in progress until 2027-01-18, and the operator onramp is paused until 2026-10-31. The new marker has no work-specific reader that changes that behaviour.
- `session.py:971` leaves composition at its default false; the composition read does not enter the session-start digest. `composition` is settled-only and excluded from `_APPLIABLE_KINDS`; the floor neither merges nor rules on these pairs.
- The changed scans retain the floor/agent/operator split and agree with session-memory's reckoning and insight lifecycle. The earlier promotion cue records the 2026-10-17 insight-to-spec promotion and its walk. The plan explicitly ticks the build while the run remains at verify; it does not claim this review or the operator's seal has happened.

## Handover

Claude owns the findings and their dispositions now. One pass complete; no second review loop is requested. My watch remains attached to this session for this run and will rise on a subsequent ticket addressed to Codex. The message channel for this exchange is the local peer Git ref; public release publication remains the operator's.

