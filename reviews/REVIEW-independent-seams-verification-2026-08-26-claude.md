---
id: review-independent-seams-verification-2026-08-26-claude
type: artifact
status: stable
version: 1.0
created: 2026-08-26
origin: stated
tags: [review, verification, adversarial, revision-binding, builder-verifier-split]
linked_things:
  - id: run-operating-model-seams-2026-08
    relation: validates
    notes: "Post-seal independent verification of the build the run carried: a different agent, in a different harness, from the one that built it — the deliberate half of the builder/verifier split."
  - id: a-check-is-only-as-trustworthy-as-who-controls-its-inputs
    relation: validates
    notes: "The guard this insight demanded was attacked live, twice, and held both times."
---

# Independent Verification — Operating-Model Seams (Claude, 2026-08-26)

**Verifier:** the Claude session that designed the sprint, verifying a
build executed entirely by a Codex session — different agent, different
harness, per the operator's deliberate routing. **Range verified:**
`fcbe7ab..0e7f317` (claim through session-end), 12 commits.

## Verdict

**Confirmed sound.** The build matches the committed design, the
self-authorization guard held under live attack on the real pre-commit
path, stage discipline held across all twelve commits, and the reconcile
obligations the design declared were paid — including the
two-versions-stale example corpora. Two minor accuracy defects were found
in the worked example and corrected post-review (v1.1); one process
lesson was promoted to the checks backlog.

## What was verified independently (not taken from the builder's records)

1. **Implementation read in full.** The guard fires on *any*
   `definition_commit` delta during a cursor move — including a pin being
   added or removed, not only changed. Pins are full-SHA-only (a
   YAML-degraded all-digit scalar is rejected at the type level).
   Resolution is rename-proof: current path first, id scan of the pinned
   tree as fallback, with per-commit caching shared across all three
   check sites through one resolver instance. Nested corpora resolve
   revisions at the owning repository root.
2. **Live adversarial attacks** in a scratch repository against the real
   `precommit` path:
   - *Re-pin + move in one commit* (choose a friendlier revision and use
     its edge): **rejected** with the designed message.
   - *Stale-pin edge theft* (keep the old pin, take an edge only the
     current definition allows): **rejected twice independently** —
     membership at the pinned revision and edge legality at the pinned
     revision, each error naming the pin.
   - *Malformed pin*: **rejected**.
   - *The legal path* — migrate alone, then advance alone under the new
     pin: **both clean**, proving migration semantics end to end.
3. **Focused suite re-run:** 12 passed in 43.6s (N6 ≤ 120s).
4. **Wiring:** `workflow_run_findings` and the fulfilment advisory run
   inside `validate_corpus`; `definition_commit` admitted to
   `CORE_FIELDS`; the `validate.thing.md` edit sits outside its kernel
   block, so no kernel regeneration was owed — checked, not assumed.
5. **Reconcile walk:** templates carry pin + activation +
   executor/authority guidance; both example corpora re-pinned to 3.35.0;
   the life-manager run is a real pinned instance with initiating
   evidence; insights dispositioned with reasons; the root AGENTS.md
   types block regenerated for the new `example` vocabulary.

## Findings

1. **(Corrected, v1.1)** The worked example's stage table used paraphrased
   stage labels rather than the atom's ids, and said "eleven" tests where
   twelve shipped (the twelfth landed at reconcile, after the row was
   written). An example that renames the stages teaches a drifted
   vocabulary — fixed to the canonical ids with the specialisation's
   extra gates noted.
2. **(Promoted to backlog)** The builder found and repaired a second
   mistranscribed `informed_by` SHA — the design's pin named a
   nonexistent commit and survived five commits before reconcile caught
   it. Two mistranscriptions in one sprint, caught by two different
   parties, is the felt evidence for structural-pin resolution at the
   commit boundary (`mechanical-coherence-checks-backlog`).
3. **(Observation, no action)** Changing a run's `definition` id without
   a cursor move remains unguarded in the same way pin changes are —
   consistent with the standing doctrine that separate commits are the
   reviewable unit; noted so a future reader knows it was seen, not
   missed.
4. **(Open, operator's)** CHANGELOG and version were correctly left as
   the per-push seal judgement; the next release entry owes the
   domain-facing adoption note for `definition_commit`, and the root
   stands unpushed until the operator's release act.

## What this record is

The first completed builder/verifier round trip across harnesses: the
methodology's own sprint, built in one harness, adversarially verified in
another, with the worked example distilled between them. The four-line
handover prompt that carried it is the portability evidence: everything
else travelled in the repo.
