---
id: a-control-that-must-stay-local-has-no-floor
type: insight
status: active
version: 1.0
created: 2026-08-17
session: 2026-08-17
source: both
confidence: high
origin: synthesised
tags: [boundary, disclosure, floor, drift, checks, local-state]
linked_things:
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: supports
    notes: "The failure occurred in the repo that wrote this insight: a history audit returning hundreds of hits, every one of them the framework's own test vocabulary."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: challenges
    notes: "Its promotion move — state the fact once and derive the restatements — is unavailable when the fact must never be committed. The escape is to promote an invariant *over* the content instead of the content."
  - id: boundary-disclosure-check
    relation: references
    notes: "The plan that built this control. Its local-file design is correct; this names the cost that design carries and the one check that can still be had."
  - id: scaffold-declares-visibility
    relation: references
    notes: "Its finding was the same control inert through emptiness across eleven domains. This is the inverse failure — the same control noisy through over-population — and both were invisible for weeks."
---

# A Control That Must Stay Local Has No Floor

## The Insight

`.boundary-terms` is the disclosure control for the framework's only public
repository, and it is deliberately **local: gitignored, never committed, never
cloned** — because a committed list of the terms you must not disclose discloses
them. That design is right. Its unnamed cost: **the artifact the floor exists to
protect this repo with is the one artifact the floor cannot reach.** No
`validate`, no `coherence`, no pre-commit check, no CI, no history, no blame.
Its entire integrity mechanism is a comment inside itself.

## The Evidence

The file recorded its own rule on 2026-07-28 — the floor's synthetic test
vocabulary was removed because *"keeping them here made the history audit
permanently red. Real terms only."*

By 2026-08-13 that vocabulary was back, together with a wider set of the same
class. A full-archive audit that day returned **hundreds of hits of which every
single one was framework test vocabulary and none was a real term.** Both
failure directions were live at once:

- the **audit** path was worthless — a permanently red report tells you nothing
  in either direction, which is [[a-check-that-always-fires-teaches-the-operator-to-ignore-it]]
  occurring inside the repo that wrote it;
- the **blocking** path was primed to falsely refuse any commit touching
  `tools/tests/`, where the same strings live by design — and a second agent was
  working in that directory at the time.

A comment stating the rule did not hold the rule. That is the whole finding: it
is not carelessness, it is the predictable behaviour of a fact with nothing
underneath it.

## Why The Usual Promotion Is Unavailable

[[repeated-drift-promotes-a-fact-into-the-floor]] says the second occurrence is
the signal, and this was at least the second. But its remedy — state the truth
once and derive every restatement — cannot apply. The truth here *must not be
committed at all*, so there is nowhere derivable to put it.

## The Escape: Promote An Invariant, Not The Content

The floor cannot own the list. It can own a rule **about** the list, without
ever holding a secret:

> A boundary term that appears in the repository's own tracked content is not a
> private identifier. Either it is noise, or it is a leak already committed.

Both outcomes are actionable, which is what makes it a real check rather than a
warning. It is same-builder (the corpus is the tool's own), it needs no
suppression list — the property that sank the retired-vocabulary check — and it
reads the local file in place without copying, committing, or printing it. This
is exactly the standard applied by hand when the file was cleaned on 2026-08-13:
each of the ten removals was justified by finding the term in tracked content,
and the four terms with zero occurrences were **kept**, because removing an
unevidenced term only weakens a control.

Routed to [[mechanical-coherence-checks-backlog]] as a candidate, not built here.

## How To Apply

When a control must stay outside the floor for a good reason, do not conclude
the floor has nothing to offer it. Separate the content from the invariant: ask
what could be checked *without* holding the protected material. The answer is
often a cross-reference against something the floor already sees — and it
converts a rule that lives in a comment into a rule that fires.
