---
id: orient-and-reconciliation-are-the-corpus-two-sides
type: insight
status: active
version: 1.0
created: 2026-06-27
session: 2026-06-27
source: both
confidence: high
origin: synthesised
tags: [orient, change-reconciliation, session-memory, worklog, architecture, symmetry, capstone]
linked_things:
  - id: change-reconciliation-specification
    relation: complements
  - id: session-memory-specification
    relation: complements
  - id: mechanism-pairs-come-from-two-reflection-axes
    relation: supports
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Orient And Change-Reconciliation Are The Two Sides Of The Corpus

## The Insight

A MarkdownLLM corpus has two kinds of durable state, and one maintenance mechanism
for each:

- **Work-content state** — the domain things and their consistency, whose history
  *is* the WORKLOG. Maintained by **change-reconciliation**: *"is the work still
  coherent?"* — answered at the moment of change.
- **Session-memory state** — insights, open threads, where-we-are. Maintained by
  **orient**: *"where are we and what's live?"* — answered at the session boundary.

They are duals, not the same mechanism wearing two hats. Each has its own
**forward/backward** structure (the `mechanism-pairs-come-from-two-reflection-axes`
symmetry, one level up): reconciliation walks forward (touchpoints, at-change) and
backward (retrospective reconstruction from git); orient reads backward (the commit
stream — velocity) and forward (the open loops — non-terminal work + open conflicts).

## Why It Matters

It is the manifesto's own **reason-*within* vs. reason-*about*** line made structural.
Change-reconciliation serves reasoning *within* the work — keep the object-level
coherent. Orient serves reasoning *about* the work — the reflexive/learning layer,
keep the meta-level oriented. Naming the two sides gives a **placement test for any
new corpus-maintenance mechanism**: does it serve work-content consistency
(reconciliation's side) or session-memory currency (orient's side)? A mechanism that
seems to need both is usually two mechanisms not yet separated — the same razor that
kept `cascade`/`touchpoints` from collapsing into one.

It is also why `continuity.md` could dissolve without loss: it was conflating the
two sides in one hand-maintained file (backward work-history that belonged in
git/WORKLOG, plus forward session-memory that belongs in the thing graph). Splitting
it along this seam *is* the dissolution — backward → reconciliation's WORKLOG,
forward → orient's generated view.

## Context

Surfaced 2026-06-27 by the operator while finishing the continuity dissolution
(`dissolve-continuity-into-reconciliation`, Phase D): "orient is the counterpart to
change-reconciliation — reconciliation is focused on worklog state, orient on
session-memory state; two sides of the whole corpus." The build (`mdllm session-start`
now generates the forward open-loops view) is this insight made operational.
