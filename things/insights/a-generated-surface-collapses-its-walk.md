---
id: a-generated-surface-collapses-its-walk
type: insight
status: promoted
version: 1.0
created: 2026-08-04
session: 2026-08-04
source: both
confidence: high
origin: synthesised
promoted_to: git-workflow-specification
tags: [change-reconciliation, generated-surfaces, kernel-blocks, doctrine, walk-cost, estate]
linked_things:
  - id: change-reconciliation-specification
    relation: complements
    notes: "A cost model for the Walk beat: the size of the human walk is not fixed by the change — it is fixed by how many restatements of the changed truth are authored rather than derived."
  - id: inflection-candidates-are-computable
    relation: complements
    notes: "Found in the same Assimilate pass. That insight is about noticing the walk is owed; this one is about how much walk a surface decision costs before any change is even contemplated."
  - id: cohesiveness-sensors
    relation: references
    notes: "The v3.24.0 move of AGENTS.md thing-type lists into a generated block derived from the schema was this insight applied before it was named — repeated drift promoted a fact into derivation, and that walk-class disappeared."
---

# A generated surface collapses its walk — restatement count is reconciliation cost

**What happened:** the Assimilate beat was run for the first time on a
framework-level inflection — the planned autopush doctrine revision
(estate-cadence-cluster, Phase 1). The textual pass found the push
doctrine restated on roughly fifteen surfaces across four layers: the
governing spec and its kernel extraction, the orchestration spec, the
sync tool's own docstrings and printed output, the operator guide, a
harness command, thirteen domain kernels' session-start blocks, and two
domains' hand-authored skills — one of them written three days earlier
by the same builder now planning the revision.

Then the shape of the fix split cleanly in two. The thirteen domain
kernels all derive their "Never push" line from **one string in the
kernel-block generator** — change it once, regenerate, and thirteen
touchpoints reconcile mechanically. The authored surfaces — spec prose,
guide, command, skills — each cost a genuine walk step: read, judge,
revise. Same doctrine, same change; the derived restatements cost one
edit, the authored restatements cost one walk *each*.

**The insight:** the human walk's size is not a property of the change —
it is a property of how the changed truth was *deployed*. A truth stated
once and derived everywhere reconciles by regeneration; a truth restated
by hand reconciles by walk, per restatement, forever. So every time
doctrine is written into a surface, the authored-vs-derived choice is
silently a purchase of future reconciliation cost — and the corpus's
walk-heaviness today is the sum of all the times authored was chosen
because it was cheaper at writing time.

**How to apply:** two directions. *Forward:* when writing a truth that
other surfaces will restate, prefer stating it in one governed place and
deriving the restatements (generated blocks, kernel extraction, tool
output quoting the spec) — accept an authored restatement only where the
surface must speak in its own voice, and count it as walk debt when you
do. *Backward:* when a walk keeps revisiting the same class of
touchpoint, that repetition is the signal to promote the restatement
into derivation — the v3.24.0 thing-types block did exactly this, and
that walk-class no longer exists. The corpus should get cheaper to
reconcile as it ages, not more expensive.
