---
id: substrate-totality-residue
type: plan
status: not-started
version: 1.0
created: 2026-08-20
priority: high
tags: [floor, totality, triggers, imports, provenance, honesty, review-residue]
linked_things:
  - id: independent-substrate-review-2026-08-20-claude
    relation: derived-from
    notes: "The review that found and verified each defect in source; it is the evidence base and the acceptance oracle for this plan."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: implements
    notes: "The reading-discipline half made mechanical: the environment question must be answered before the content question, in the evaluator itself."
  - id: a-wrong-sum-is-indistinguishable-from-a-right-one
    relation: references
    notes: "The same argument one axis over — a confident negative and a confident freshness carry no evidence of the read that failed behind them."
  - id: validate-thing-specification
    relation: implements
    notes: "The no-silent-default law these branches currently break."
  - id: trigger-specification
    relation: references
    notes: "Owns the four typed results the import branch must return; this plan changes no vocabulary, only the branch that skips it."
---

# Substrate Totality Residue

The independent review of 2026-08-20 confirmed the typed-total trigger
architecture, the membrane's authority-before-I/O ordering, and the provenance
chain as sound — and then found three places where the floor still renders a
state it *could not look at* as a definite answer. That is the one class the
totality doctrine exists to prevent, and each instance is a small diff.

This plan owns only those defects. It introduces no vocabulary and no new
mechanism; every fix makes an existing declared result reachable in a branch
that currently skips it.

## The three

1. **An unreachable import route yields a confident `not-fired`.** The
   `state_is` branch gates only states prefixed `unevaluable-`. `unreachable`,
   `no-address-book-entry`, and `incomplete` fall through to the match test and
   report that no watched state matches — so a trigger watching for staleness
   reports a definite false while the source is simply unreachable. The sibling
   `porch_offers_unimported` branch already classifies the same condition as
   `unevaluable`; that inconsistency is the specification of the fix.
   *Care:* a domain may legitimately watch *for* `unreachable` as a value. The
   fix must return `unevaluable` for unavailability the trigger did not ask
   about, not for the state it did.

2. **A pin-current import whose content read failed reports `fresh`.** When the
   body read is absent, the divergence comparison is skipped and the row lands
   in `fresh`. One of the two directions the check promises was unverifiable,
   yet the report asserts full freshness. The stale branch already degrades
   conservatively in the same situation — again, the fix is stated by its own
   sibling.

3. **Provenance input existence matches by path suffix.** A pinned id is
   satisfied by any file whose path merely ends with the same name, so an
   unrelated similarly-named thing suppresses the broken-chain Error the check
   exists to raise. Match the exact basename or a full path segment.

## The smaller siblings, same class

- The estate trigger sweep swallows a failed retrospective computation and
  renders it identically to *no debt owed*.
- The quarantine predicate is spelled three inconsistent ways across modules
  (one normalises surrounding whitespace, two do not), so a single stray
  character makes a thing quarantined for arithmetic and invisible to the
  provenance and membrane checks.
- A neutral service returns the same empty value for *no remote configured* and
  *the command could not run*, producing a confident wrong diagnosis offline.

## What this plan does not do

No new trigger type, no new state, no suppression list, no widening of what the
floor judges. If a fix here starts to need an allow-list to stay quiet, it has
stopped being this plan's work.

## Done when

- [ ] Each of the three returns its honest typed result, with a regression test
      that fails if the branch reverts to a definite answer.
- [ ] The smaller siblings are either fixed or explicitly ruled acceptable, in
      writing.
- [ ] One deliberately unreachable route, exercised end to end, produces
      `unevaluable` in the trigger report and a non-`fresh` row in the imports
      report — proved on contact rather than in a fixture alone.
