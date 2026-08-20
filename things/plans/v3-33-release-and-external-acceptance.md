---
id: v3-33-release-and-external-acceptance
type: plan
status: not-started
version: 1.0
created: 2026-08-20
priority: high
tags: [release, acceptance, evidence, harness, publication, operator-owned]
linked_things:
  - id: codex-substrate-review-response-2026-08-20
    relation: extends
    notes: "Lifts that completed plan's external-acceptance register into an open carrier: a completed thing drops out of the orient view, and four of its five rows are real outstanding work."
  - id: independent-substrate-review-2026-08-20-claude
    relation: derived-from
    notes: "Closed the register's fifth row — the independent assessment — and named the register's own invisibility as a not-in-view gap."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: documents
    notes: "The destination for every fresh live row; the matrix stays the exact-build evidence boundary."
  - id: session-start-hardening
    relation: complements
    notes: "Owns the Tier-0 receipt probes; this plan only carries the fact that they remain owed and where their results land."
  - id: vendor-harness-adapter-foundation
    relation: complements
    notes: "Owns the two project-bound harness acceptances and the rollout-default decision."
  - id: cowork-adapter
    relation: complements
    notes: "Owns the remote re-test, the local transport packet, and the stale-bundle branch."
---

# v3.33 Release And External Acceptance (carrier)

The substrate remediation closed locally and correctly refused to self-certify
what only a product event or a human can establish. It recorded those as an
external-acceptance register — inside a plan it then marked `completed`.

A completed thing leaves the orient view. So the register that names the release
decision, three live-harness acceptances, and the independent review became
invisible the moment the plan closed honestly. This carrier exists for that
reason alone: to hold the rows where the next session will see them, without
re-opening a plan whose local work is genuinely done and without restating what
the subject plans own.

## The register, as it truthfully stands

| Row | State | Owner |
|---|---|---|
| Independent assessment of review, plan, commits, evidence and residuals | **Closed** 2026-08-20 — accepted the remediation, narrowed one finding, reopened one adjacent defect | recorded in `reviews/` |
| Fresh Claude Code lifecycle and Tier-0 receipt/read probe | Pending an exact-build rerun | `session-start-hardening` + `vendor-harness-adapter-foundation` |
| Fresh Codex instruction delivery, lifecycle dispatch and nested floor | Pending an exact-build rerun | same |
| Fresh Cowork remote re-test, local transport packet, stale-bundle branch | Pending exact client runs | `cowork-adapter` |
| Public v3.33 release and push | Not authorised, not performed | operator |

Every live row in the capability matrix currently reads *not tested for the
current fingerprint and receipt definition*. That is accurate and it is the
point: the delivery semantics changed after the records were made, so historical
evidence cannot accept them. Until at least one Claude and one Codex surface are
re-probed, the matrix cannot say current — and no public claim may say more than
the matrix does.

## The release act, and its one perishable detail

Publication of the release surface stays a deliberate human act; the repository
declares `autopush: false` and that remains controlling. Whoever takes the
decision inherits the standing walk: reconcile the changelog and compatibility
notes, confirm publication debt, judge artifact integrity, then publish.

One detail perishes on push: the install guidance names the last published
release commit and its verified installer hash. That naming is correct today and
becomes stale the moment v3.33 is published — so re-pinning it is part of the
release act, not a follow-up.

## Deliberately not here

The probe designs, the acceptance criteria, and the rollout-default decision
belong to the subject plans and are not restated. This carrier holds one fact —
*these rows are outstanding and this is who owns them* — and closes when the
rows do.

## Done when

- [ ] One Claude and one Codex surface re-probed against the current contract
      definition, recorded in the capability matrix with exact builds.
- [ ] The Cowork rows recorded to the same standard, or explicitly re-scoped.
- [ ] The release decision taken — published with the pin refreshed, or
      deliberately deferred with the reason written down.
