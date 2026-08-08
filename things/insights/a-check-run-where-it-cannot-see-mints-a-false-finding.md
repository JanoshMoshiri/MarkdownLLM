---
id: a-check-run-where-it-cannot-see-mints-a-false-finding
type: insight
status: active
version: 1.0
created: 2026-08-08
session: 2026-08-08
source: agent
confidence: high
origin: synthesised
tags: [floor, degraded-environment, null-result, imports, false-negative]
linked_things:
  - id: cowork-integrity-estate-sweep
    relation: informs
    notes: "Phase 2 held the lived instance: a conflict recorded 0/101 imports pinned from a single-repo container; the full-estate re-run read 77/101 with the control working. The record was corrected by amendment the same day."
  - id: mechanical-coherence-checks-backlog
    relation: informs
    notes: "The backlog's null-result primitive is this insight's mechanical half — does the tool distinguish nothing-found from could-not-look? The INCOMPLETE-bucket conflation item is the imports-check instance."
---

# A check run where it cannot see mints a false finding

A documented check that is never run leaves the same evidence as no check —
the estate already knew that. This is the sharper corollary the breach
produced: **a check run in an environment where it cannot see is worse than
no check**, because it emits output, and output gets read as a finding.

The lived instance: the regulated deployment's QMS domain ran
`imports-check` from a session container holding only its own repo. The
tool answered honestly — `COVERAGE: 0/101`, everything bucketed
could-not-check — but the session's prose turned the bucket into a
positive claim ("none of the 101 carries the reference triple") and raised
a conflict on it. Re-run from the full estate the same day: 77/101 pinned,
75 fresh, the control demonstrably working. The false finding was minted
at the boundary between an honest tool and a reader who did not ask *what
could this run see from here?*

The general rule: absence-shaped output (0 stale, 0 found, empty list) is
only a finding when the run could have found things. Every consumer of a
floor report owes the environment question before the content question —
and tool-side, every command whose result can be empty should say whether
it looked and could not, or looked and found nothing (the null-result
primitive). The mechanical residue of this insight lives in the coherence
backlog; this thing carries the reading discipline no tool can.
