---
id: run-reckoning-phase-4-2026-10
type: workflow-run
status: active
version: 1.3
created: 2026-10-20
definition: substrate-floor-development
definition_commit: e01966a71111cd839135ce9623c032217c234fe6
current_stage: reconcile
held_by: claude
tags: [run, floor, the-reckoning, two-seat-review, codex]
informed_by:
  - id: the-reckoning
    commit: 379f4970290d4f8792bf5ed898fb591bbd95b588
  - id: operator-rulings-at-the-reckoning-2026-10-20
    commit: cb192bf747eab0651aadc08730a374ef2a36abdd
linked_things:
  - id: the-reckoning
    relation: implements
    notes: "Phase 4 is this run's work inventory: the promotion path, scans 5-7 as reads of the reckoning, the pre-filter in the reckoning, one hold field set."
  - id: substrate-floor-development
    relation: references
    notes: "The definition this run follows. Used for explicit runs only — the operator ruled on 2026-10-20 that plan does not become its carrier."
  - id: operator-rulings-at-the-reckoning-2026-10-20
    relation: references
    notes: "Ruling 3 (leave the carrier) is why this is a declared run and not a carried one."
  - id: framework-retrospective-2026-10
    relation: references
    notes: "Scan 7 found the definition had no run while three arcs enacted its shape; this is the first run since, and the first with a second seat."
  - id: ad-hoc-message-loop
    relation: references
    notes: "Instantiated at the root by the Codex seat during its review (finding 2) so the ticket could wake a watch; the loop both seats now arm."
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: references
    notes: "The two-seat shape this run exercises: a ticket per work item, the reviewer's seat named, the operator at seal."
  - id: execution-independence-is-not-judgement-independence
    relation: references
    notes: "Why the reviewer is Codex and not a second Claude: a different lineage is a second judgement, a second instance is a second pair of hands."
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: references
    notes: "Why the review runs once at the pinned commit and stops: findings dispositioned, not a loop run until the reviewer is silent."
---

# Run: The Reckoning, Phase 4 — the first two-seat substrate change

## Where This Is

At `reconcile`: the review came back with four findings, three fixed in a `build` loop-back and one remedied by the reviewer; this stage is the dark-region walk for the spec and the four command surfaces. Born at `design`: the problems, requirements and the cut were
settled before this run existed — `the-reckoning` Phase 4 names the four
pieces (the promotion path tripping the walk gate; `retrospective.md` scans 5
and 6 rewritten as reads of the reckoning and scan 7's promotion half pointed
at it; the composition pre-filter moved into `mdllm reckon`; one hold field
set for work and insights), and the 2026-10 retrospective supplied the
evidence for each by running them by hand first. The design is the plan's
text plus one call recorded here: the pre-filter is an **opt-in read**
(`reckon --composition`), not a band on the digest's path, because it is a
quality read and a check that always fires teaches the operator to ignore it.

**The two seats.** This is the first substrate change run with a reviewer of
a different lineage, on the operator's decision of 2026-10-20: Claude builds
in the MAIN clone and commits at a pinned SHA; a ticket
(`ticket-reckoning-phase-4-review`) hands the review to the Codex seat, which
reads once at that commit and files findings; the dispositions land before
the seal, and the seal — the push — stays the operator's. The definition's
stages carry no `actor` yet; if this shape holds, the follow-up is to give
them one (`build` builder, `verify` reviewer, `seal` operator) or to mint a
`substrate-change-loop` beside the engineering workspace's
`two-agent-review-loop`, and that is the operator's call on this run's
evidence, not this run's.

## Stage record

- **design (2026-10-20)** — the plan's Phase 4 text and the retrospective's
  evidence; the one design call above. No separate design thing: the cut is
  four small pieces on one module and one spec.
- **build (2026-10-20)** — `reckon.py`: `keep()` writes `disposition:
  keep-active` on work as on insights (one field set; three plans migrated);
  `composition_candidates()` and `reckon --composition` (settled band, kind
  `composition`, a shared spec weighted zero); 39 tests green in
  `test_reckon.py` (one amended, one added). `retrospective.md` 1.9: scans 5
  and 6 as reads of the reckoning, scan 7's promotion half pointed at it; the
  four retrospective command surfaces follow. `_schema.yaml` declares
  `ticket` (claude, codex, closed) so the review can be requested as a thing;
  the entry file's generated block regenerated. The promotion-path evidence
  is prior: the 2026-10-17 promotion of `change-safety-is-defense-in-depth`
  into change-reconciliation.md tripped the gate
  (`cue-change-reconciliation-specification-2026-10-17`).

- **verify (2026-10-20, from e5de9fa)** — the build committed at
  `e5de9fa4081227fc06c26c331d5222117a4d95b8`; `ticket-reckoning-phase-4-review`
  raised to the Codex seat with that SHA and the four pieces as scope, one
  pass, findings as the ticket body, no fixes; the full suite ran once at this
  boundary on the builder's side: **1111 passed, 14 skipped** (11m31s,
  Windows, Python 3.12) — the builder's half of verify is green; the
  reviewer's half is the ticket. The run is held by the reviewer until the
  ticket comes back `claude`.

- **verify → build → verify (2026-10-21)** — the Codex seat's review landed
  on the ticket (`c0f20e1`): four findings, each confirmed by execution or
  file comparison at the pinned revision. (1) The report re-sorted the
  composition band alphabetically, losing the helper's weight-first rank —
  **defect**, fixed at the band sort with a report-level test whose heaviest
  pair sorts last by id. (2) The ticket type alone armed no watch: no
  `ad-hoc-message-loop` at the root, no actors on the definition — **defect**,
  remedied by the reviewer itself (`ac74fa9`, under the Codex seat's own
  identity, on the operator's separate instruction to turn the watch on): a
  departure from the ticket's *no fixes* that the record can attribute,
  accepted. (3) Scan 5's authored rule omitted the spec-only inclusion
  exception the code implements — **drift**, fixed in the spec and the four
  surfaces. (4) The Copilot surfaces lacked step 9, the chase hand-over —
  **pre-existing drift**, fixed. Reviewer's non-findings: mirrors excluded,
  the read off the digest's path, the three migrated holds unchanged in
  behaviour, the floor still marking no verdict. Verify re-run: 39 reckon
  tests green; the full suite re-run at this boundary for the one-line sort
  change.
- **reconcile (2026-10-21)** — the walk on `retrospective-specification`'s
  one-clause change raised at the gate and answered; the four surfaces
  diffed pairwise and identical; indexes rebuilt.

## Next

The ticket is back in the Codex seat for one line — confirm or decline the
finding-1 fix — then `closed`. The builder's watch is armed on this run
(`--role claude --remote . --branch main --exit-on-wake`). Then `seal`: the
plan's Phase 4 stays ticked, the CHANGELOG entry is the release's, and the
push is the operator's. The follow-up the operator named — turn this shape
into the standing workflow for substrate changes — is proposed on this run's
evidence, not inside it.

## Notes

**What the first run showed.** The reviewer found a real defect the builder's own tests passed over (the sort), a drift the builder introduced (the exception unstated) and one it inherited, and a channel defect (no watch) it fixed itself — four findings, zero disputed, in one pass. The builder's gate was blocked for a day by a third seat's uncommitted edits in the same working copy — the documentation session — which is the seat ruling's cause three, observed live. Two seats, two clones, one ticket: the shape held.

The seat for this clone is undeclared (`mdllm seat . --set claude --agent
claude-code` is one line) and changes the public repository's commit
identity — the operator's to give, asked for at the ticket.
