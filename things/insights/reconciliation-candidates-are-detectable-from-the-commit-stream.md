---
id: reconciliation-candidates-are-detectable-from-the-commit-stream
type: insight
status: active
disposition: keep-active
disposition_reason: "Design hypothesis, deliberately not built — a nice-to-have; reconciliation is manageable without it. Promote to a spec/feature when the manual noticing actually starts to cost."
version: 1.0
created: 2026-06-27
session: 2026-06-27
source: operator
confidence: medium
origin: synthesised
tags: [change-reconciliation, mechanization, commit-stream, fan-in, detection, floor, razor, undecided]
linked_things:
  - id: change-reconciliation-specification
    relation: informs
  - id: orient-and-reconciliation-are-the-corpus-two-sides
    relation: supports
    notes: "This is the work-content (reconciliation) side; the signal is the commit stream itself"
  - id: directional-graph-reads-come-in-inbound-outbound-pairs
    relation: supports
  - id: mechanism-pairs-come-from-two-reflection-axes
    relation: supports
---

# Reconciliation Candidates Are Deterministically Detectable From The Commit Stream

## The Insight

The **noticing** half of change-reconciliation can be mechanical, even though the
cue and the walk stay human. The signal is already in git, and the spec's own premise
draws the line: *"a fresh thing on a clean slate carries no consistency risk — risk
enters only at change to something the domain already reasons from."* Git classifies
every change against exactly that line:

- **Added (`A`)** → a new thing → no reconciliation risk → skip.
- **Modified (`M`)** / **Deleted (`D`)** → a change to an existing thing → **candidate**.

Then weight by **fan-in** (the `relationships` index already knows each thing's
inbound-edge count): a modification to a high-fan-in thing is *inflection-shaped*; a
modification to a leaf almost never is. So the floor can compute, from the commit
stream alone: *"since last session you modified `X` (8 dependents) and `Y` (1) —
reconciliation candidates, ranked."*

## The Razor

**Mechanize the noticing, not the deciding.** This does not auto-trigger
reconciliation and does not name the inflection — the floor only says a change has
the *shape* of one; the driver still decides whether it *is* one, and the walk stays
human (`change-reconciliation.md` → The Driver Names The Inflection). It hardens the
spec's existing line — *"an agent may offer to reconcile when it notices it has
changed a thing with many dependents"* — from an `interpretation` hope (the agent
remembers to look) into a deterministic surface. Same detect-surface-don't-dispose
shape as the orphan check and orient.

## Why It Matters

It closes a real gap: `touchpoints <id>` is manual — you must already *know* to run it
on `X`. This tells you **which `X`**, completing the toolchain: **detect-candidates**
(this, from git) → **assimilate** (`touchpoints`) → **walk** (human) → **seal**. The
only fully-manual step left — *noticing you should reconcile at all* — becomes a
surface.

## Design Notes (for when it's built)

- **v1 (cheap):** modified-or-deleted × fan-in, at session-boundary / post-commit.
  Over-includes status-only changes — fine; Info, non-blocking, human filters.
- **v2 (sharper, only if v1's noise annoys):** parse the diff — a *frontmatter* change
  (status/edges → `cascade`'s territory) vs a *body* change (claims → reconciliation's
  contradiction risk). A body change to a high-fan-in thing is the gold-standard
  candidate.
- Lives as a detect/surface/rank read — never trigger, never walk.

## Status

A standing operator idea (~2 weeks). Deliberately **not built** — nice-to-have,
reconciliation works without it. `keep-active`; promote when the manual noticing
starts to cost.
