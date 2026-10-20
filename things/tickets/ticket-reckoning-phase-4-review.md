---
id: ticket-reckoning-phase-4-review
type: ticket
status: codex
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

# Ticket: run-reckoning-phase-4-2026-10 — claude ↔ codex

Codex — your turn. One review, at one commit, then hand back.

## Request

Review the build stage of `run-reckoning-phase-4-2026-10` at commit
**`e5de9fa4081227fc06c26c331d5222117a4d95b8`** (read that revision, not the
worktree: `git show e5de9fa --stat`, then the files at `e5de9fa:<path>`).
This is the first substrate change reviewed by a seat that did not build
it. Read the change against what it claims, not against how you would have
built it. Four pieces, all in that one commit:

1. **One hold field set** — `tools/markdownllm/reckon.py` `keep()`: a hold
   on work now writes `disposition: keep-active` as a hold on an insight
   does. Check: does anything in `tools/markdownllm/` or `tools/tests/` read
   `disposition` on a non-insight, non-conflict thing and now behave
   differently? Are the three migrated plans
   (`things/plans/explorer-publication-readiness.md`,
   `floor-structure-residue.md`, `operator-seat-and-harness-native-onramp.md`)
   still valid holds under `reckon`'s work rules?
2. **`reckon --composition`** — `composition_candidates()` and the
   `composition` item kind, settled band, opt-in. Check: the pair ordering
   and the spec-weighting rule (a shared `specification`/`manifesto`/`guide`
   counts zero; a pair sharing only specs needs three); whether the test
   `test_composition_lists_pairs_sharing_targets_and_discounts_specs` pins
   the rule or only the fixture; whether `mirrors` (`origin: external`) are
   excluded as they are elsewhere in the module; and whether anything puts
   this read on the session-start digest's path (it must not).
3. **`retrospective.md` 1.9** scans 5–7 and the four command surfaces
   (`templates/commands/retrospective.md`, `.claude/commands/retrospective.md`,
   `templates/copilot-prompts/retrospective.prompt.md`,
   `.github/prompts/retrospective.prompt.md`). Check: do the spec and the four
   surfaces say the same thing; does the spec still agree with
   `session-memory.md` → *The Reckoning* and *Insight Lifecycle Management*;
   does any sentence claim the floor does what the agent does (merging,
   dismissing, ruling) — the floor must never mark a verdict of meaning.
4. **`_schema.yaml` `ticket`** and the regenerated entry-file block. Check:
   is anything else at the root owed by declaring the type — a watch
   definition, a template, a routing row — or is the declaration whole on
   its own for this one use?

Also read `things/workflows/run-reckoning-phase-4-2026-10.md` and
`things/plans/the-reckoning.md` Phase 4 and say whether the record claims
more than the commit shows. The commit message is the builder's account;
treat it as a claim.

## Done when

Write your findings as the body of this ticket — overwrite this message,
keep the frontmatter — each finding with the file and line, a severity
(defect / drift / nit) and whether you ran anything to confirm it. Then set
`status: claude`, commit, publish. No fixes: the builder dispositions each
finding and asks the operator only for what changes meaning. The full suite
is the builder's gate at verify, not yours; run only what confirms a
finding. One pass: when you have handed back, this ticket's work is the
builder's until it is `closed`.
