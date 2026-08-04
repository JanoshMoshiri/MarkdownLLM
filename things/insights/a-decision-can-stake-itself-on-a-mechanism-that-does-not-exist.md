---
id: a-decision-can-stake-itself-on-a-mechanism-that-does-not-exist
type: insight
status: active
version: 1.0
created: 2026-08-04
session: 2026-08-02
source: both
confidence: high
origin: stated
tags: [decisions, confidence, provenance, cross-domain, forward-work, belief-revision]
linked_things:
  - id: deterministic-calculation
    relation: informs
    notes: "The build this pattern produced: the design arrived already specified, in prose, by a domain decision written days earlier in a different repo. The framework session executed rather than designed."
  - id: the-rough-true-account-is-generative-infrastructure
    relation: complements
    notes: "Adjacent but distinct. That one says a true record of what happened out-builds a polished one. This one is about the FORWARD half — a record of what has not happened yet, held open by a field the floor already reads."
  - id: existence-is-not-currency
    relation: complements
    notes: "The pair: a capability that exists but is unused earns nothing, and a decision that depends on a capability that does not exist should not claim to be settled. Both are refusals to bank something not yet real."
  - id: a-ruling-triages-more-cheaply-than-a-mechanism
    relation: complements
    notes: "That one routes work by ruling instead of building. This one is what a ruling does when it CANNOT route the work away — it names the mechanism it needs and holds itself open until someone builds it."
---

# A Decision Can Stake Itself On A Mechanism That Does Not Exist

## The Insight

A `decision` is normally read as a settled question. But a decision can be
*deliberately* unsettled in a specific, productive way: it can name the
mechanism that would make it safe, record that the mechanism does not exist,
and hold its own `confidence` down until it does.

This converts a standing risk into an **executable work item held in the corpus
by a field the floor already reads**.

## The Instance

A money domain ruled that transaction detail lives as a table in a statement's
body — not as things, not in a spreadsheet. The ruling did three things beyond
deciding:

1. **Named its cost in plain words**, and named it as the strongest argument for
   the option not taken: *"Arithmetic becomes the agent's job, and agents get
   arithmetic wrong."*
2. **Named the answer as a thing that did not exist**: a deterministic tool that
   computes the totals, with the division stated — *the agent transcribes and
   reasons; the tool does every sum*.
3. **Held `confidence: medium` and said what would raise it**: the tool
   existing and having produced the totals for one real reconciled statement.

When a later session in the *framework* repo was asked for a calculation floor,
the design work was already done. Not sketched — specified, including the
division of labour, the failure mode it defends against, and the acceptance
condition. The session executed rather than designed, and the resulting build
was better-aimed than one starting from "add a maths module" could have been.

## Why It Matters

Three properties, none of which a to-do list has:

- **It survives the session that noticed it.** The need was felt while ruling on
  something else. Recorded in the decision, it stayed felt; recorded in a
  backlog, it would have become one line competing with forty others.
- **It carries its own reasoning.** The later session did not have to re-derive
  whether the need was real — the decision had already argued it, against the
  alternative, with the cost stated.
- **It self-surfaces without a trigger.** `confidence: medium` on a decision is
  a standing question mark. Anyone reading that decision meets the gap; no
  reminder had to fire, and no one had to remember.

The third is the sharpest point. A held-down confidence field is a *passive*
signal that works whenever the thing is read, which is exactly when it is
relevant — as opposed to an active trigger, which fires when a clock says so.

## The Generalisation

**When a decision's safety depends on something that does not exist yet, say so
in the decision and stake the confidence on it.** The alternatives are worse:
recording the decision at `high` hides a real dependency behind a false
settlement, and recording the gap only in a backlog separates the need from the
reasoning that justifies it.

This also cuts the other way, and should be stated: a decision staked this way
is **genuinely not settled**, and a session that reads one should not treat it
as load-bearing until the stake is met. That is the honest cost of the pattern
and the reason it works.

## What Would Change This

If staked decisions accumulate faster than they are discharged, `confidence:
medium` degrades into background noise and stops being a question mark. The
signal to watch: a domain where several decisions are all waiting on mechanisms
nobody is building. At that point the route is triage — discharge or overturn —
not a mechanism for tracking the staking.
