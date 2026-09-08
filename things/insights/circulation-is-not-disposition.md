---
id: circulation-is-not-disposition
type: insight
status: active
version: 1.0
created: 2026-09-08
session: 2026-09-08
source: both
confidence: high
origin: stated
tags: [conflict, lifecycle, session-memory, retrospective, review-finding]
linked_things:
  - id: belief-revision-specification
    relation: informs
    notes: "v1.3 adds the two readers (session-end brake, retrospective triage), the shared hold marker, and the while-open default this insight demanded."
  - id: session-memory-specification
    relation: informs
    notes: "Step 3's brake now reads conflict-disposition findings; the keep-active marker is shared with insights."
  - id: retrospective-specification
    relation: informs
    notes: "Produces item 3 (whole-set conflict triage); scan 6 re-reads held conflicts' stated reasons."
  - id: validate-thing-specification
    relation: informs
    notes: "The 30-day stale-conflict Info the spec promised from v1.0 is implemented (`conflict_age_findings`); it fires through a live inbound edge by design."
  - id: a-stated-dismissal-condition-needs-a-reader
    relation: supports
    notes: "Same lesson one object over: a stated reason on a held conflict is a condition, and scan 6 is its reader."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: supports
    notes: "The session-start open-conflicts line re-printed unchanged every session — exactly the check this insight describes."
  - id: review-external-conflict-lifecycle-2026-09-08
    relation: derived-from
    notes: "The external review that named the asymmetry: creation at three cadences, disposition at none."
---

# Circulation Is Not Disposition

## The Insight

An inbound edge from a live thing keeps a conflict *in circulation* — it
returns to the next session's orient view. It does not *rule* on it. The
framework had been treating the first as if it were the second: the floor's
only conflict check asked "does something live point at this?", the
session-start digest listed every open conflict, and nothing anywhere forced
a decision. A conflict linked from a live plan could sit for months with every
mechanical signal reading healthy, while the plan that pointed at it did other
work. Insights got a brake at session end and a triage at retrospective;
conflicts — the higher-stakes object, the one an auditor finds — got creation
at three cadences and disposition at none.

## Why It Matters

Two acts that look alike from the outside — *this is still live* and *this
has been decided* — need separate readers, or the cheaper one silently
substitutes for the dearer. The remedy is not a smarter liveness test; it is a
second question asked on a clock. So the age check fires *through* a live
edge, deliberately: thirty days untouched in the commit stream is the floor
asking "still live, yes — but has anyone ruled?", and the answer has to be a
disposition (rule, link from the work that will resolve it, or hold with a
stated reason), never the edge again. The same distinction explains why the
session-start line was not a reader: a list that re-prints unchanged every
session is a check that always fires, and it teaches the operator to scroll
past it (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`).

## Context

Surfaced by an external review on 2026-09-08 that read the two ritual command
files as the actual entry points rather than the specs as written, and found
the retrospective command firing three of the spec's seven scans (the
change-driven reconciliation pass — "the net beneath the net" — unwired) and
the conflict lifecycle asymmetric at both cadences. The review's proposed
smallest fix — wire scan 4, add a conflict-disposition beat mirroring the
insight brake — is what landed, plus the age check both specs had promised
since v1.0 and the floor had never carried. The same review left one seam
open for the operator: who declares an inflection when an unattended agent
commits (`change-reconciliation.md` → The Driver Names The Inflection).
