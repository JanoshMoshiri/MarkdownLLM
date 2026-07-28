---
id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
type: insight
status: active
version: 1.0
created: 2026-07-28
session: 2026-07-28
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Design lens for every future check the floor gains — vocabulary/threshold selection is part of correctness. Promote if a second check ships with a calibration defect found the same way."
tags: [floor, checks, calibration, boundary, alerting, trust]
linked_things:
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: supports
    notes: "Same family: a check needing constant suppression is mis-specified. Here the defect was in the operator-owned vocabulary, not the check's logic"
  - id: boundary-disclosure-check
    relation: references
    notes: "The check whose first full history audit surfaced this — 550+ hits, every one synthetic test vocabulary"
---

# A Check That Always Fires Teaches The Operator To Ignore It

*(Sibling claim, held in a consuming domain rather than here: a control the
floor cannot evaluate is not a control. This is its other half — nor is one
that fires on everything.)*

## The Insight

The first full-history run of the disclosure-boundary audit returned red:
550+ hits across three terms. Every one was `client-x` / `client-y` /
`client-z` — the floor's **own synthetic test vocabulary**, present in the
public test suite by design, left in the local terms file from live-testing
the mechanism.

Nothing was leaking. The check was working perfectly. And it was worthless,
because a check that cannot come back green trains its operator to stop
reading it — and the one day it goes red for a real reason, it looks exactly
like the other days.

## What This Means Mechanically

For a check whose ruleset is **operator-owned** (terms, thresholds,
suppression entries), calibration of that ruleset is not configuration
around the check — **it is part of the check's correctness.** A perfectly
implemented matcher over a mis-specified vocabulary is a broken control.

The failure is quiet in a specific way: it does not produce a wrong answer,
it produces an *unreadable* one. Signal-to-noise is a correctness property of
an alerting mechanism, not an aesthetic one.

## The Practice

- **Run the full-history / full-corpus form of any new check immediately**,
  not just the incremental gate. The gate form (staged diff, one commit) had
  been green all session and revealed nothing; only the audit form exposed
  the mis-calibration.
- **Green must be reachable.** If a check cannot return clean on a healthy
  corpus, fix the ruleset before trusting the check.
- **Keep the floor's synthetic test vocabulary out of operator rulesets** —
  test fixtures live in the public repo forever by design, so any term the
  test suite uses is permanently un-matchable as a real secret.
- The operator's instinct here was right and worth keeping: *sweep manually
  right after installing the mechanism, before trusting it.* The sweep's
  finding was not a leak — it was a calibration defect that would have
  silently devalued the tool.
