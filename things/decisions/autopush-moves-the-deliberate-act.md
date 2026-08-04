---
id: autopush-moves-the-deliberate-act
type: decision
status: made
created: 2026-08-04
session: 2026-08-04
decided_by: human
confidence: high
linked_things:
  - id: estate-cadence-cluster
    relation: implements
    notes: "Phase 1's doctrine half; the mechanism half is the post-commit hook + `mdllm autopush`."
  - id: git-workflow-specification
    relation: informs
    notes: "The revised surfaces: the kernel block's Publication line, the Should-Not-Do first bullet, and the new Outbound Rules section."
  - id: premature-publish-manufactures-discipline-eroding-urgency
    relation: references
    notes: "Stands unrevised. Its publish is a release event on a judgement surface; this decision's push is transport of floor-validated working state. The carve-out IS the reconciliation of the two: release surfaces declare autopush: false."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: references
    notes: "Why --force stays structurally outside the mechanism and why release publishes keep the human: transport of committed state is recoverable; overwriting a remote or publishing a release is not."
---

# Decision: the deliberate act moves from each push to the declaration

**Decided by:** the operator, 2026-08-04, voice, after one working day of
repeatedly overriding the no-push rule and the deep dive that followed.

## The question

v3.22.0's doctrine line — *"the push stays the human's deliberate act"* —
was written when publication was a judgement call made per push. The estate
then crossed the dimension line that release predicted and deferred on
("`git.autopush` deliberately deferred until a collaborator exists"): work
became multi-domain within a day, domains consume each other's porches
through floor-driven sync, and the operator became his own collaborator
across machines and sessions. Once orientation reads the estate, an
unpushed commit is not private working state — it is state withheld from
the thing that orients on it. Keep the per-push human act, or move it?

## The decision

Publication of floor-validated commits becomes mechanical — a post-commit
hook leg — **default ON with per-repo opt-out** (`git: autopush: false`;
absence means on). The operator ruled the default direction explicitly:
the opt-out set is the small one; most usage wants captured state
published.

The old line is **revised, not deleted**. The deliberate act did not
disappear; it moved up one level, to two places where it does more work:

1. **The declaration.** Which repos opt out is a human judgement made once
   and owned in config — the same shape as every hardening the framework
   has done (judgement at configuration time, mechanism at run time).
2. **The routing of every non-clean outcome.** A rejected push is
   divergence on the push side — surfaced, never forced, never
   pull-rebase-retried; the operator routes it. `--force` is structurally
   outside the mechanism's vocabulary.

## The alternative considered and why it lost

Keeping per-push deliberation (status quo, possibly with better debt
reporting). It lost on evidence: the operator overrode the rule repeatedly
in a single day, which means the deliberation had already degraded into
ceremony — a rule that is routinely overridden protects nothing and trains
override. Meanwhile the cost of unpushed state had become structural
(imports-check cannot see it, estate-sync cannot deliver it, consumers read
a stale face), and the protections that actually matter were never at push
time: exposure discipline is authoring-time, and consumer trust is gated by
the quarantine flip, which autopush does not touch.

## The carve-out that keeps the old truth true

`premature-publish-manufactures-discipline-eroding-urgency` stands
unrevised. A **release** publish — outsider-consumed, judgement-gated, no
mechanical completeness check — is a different act sharing a verb. Release
surfaces (the framework root's public repo) declare `autopush: false`, so
the default-on rule itself is what keeps their pushes deliberate.

## What this governs

The kernel block Publication line and Outbound Rules section of
git-workflow.md; the post-write:commit hard hook's description
(orchestration.md, the generated domain hooks blocks); the `mdllm autopush`
mechanism and post-commit hook body; the estate-sync `--status` footer; the
operator guide; the end-session ritual's publication-debt reading; and every
domain surface that restated the old line — walked and revised in the same
release under `estate-cadence-cluster`.
