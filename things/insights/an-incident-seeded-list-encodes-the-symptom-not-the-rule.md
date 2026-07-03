---
id: an-incident-seeded-list-encodes-the-symptom-not-the-rule
type: insight
status: active
disposition: keep-active
disposition_reason: "Standing design razor with no single live consumer to key liveness to: it applies at every future defensive enumeration (strip lists, allow lists, field registries). Paid for by a real two-version leak."
version: 1.0
created: 2026-07-03
session: 2026-07-03
source: both
confidence: high
origin: synthesised
tags: [egress, boundary, defensive-lists, class-vs-instance, review-findings]
linked_things:
  - id: a-crossing-thing-carries-its-producers-private-graph
    relation: extends
    notes: "That insight states the rule (every relational field is producer-private); this names why its own implementation still leaked — the list under the rule was seeded from the incident, not derived from the rule."
---

# An Incident-Seeded List Encodes the Symptom, Not the Rule

## The Insight

When a fix takes the form of a **membership list** — fields to strip, paths to
block, names to quarantine — there are two ways to populate it, and they look
identical in the diff. One *derives the members from the rule's class
definition* ("every field that carries producer-local ids"). The other
*enumerates what the triggering incident touched* ("the fields the road-test
consumer tripped on"). The second ships the same day and passes the same tests,
but it defends against the incident, not the class: **every member of the class
the incident happened not to exercise is silently outside the defence.**

The worked case: `_MCP_INTERNAL_GRAPH` was born from the first cross-domain
road test, where a consumer tried to resolve a producer-local `linked_things`
id. The list faithfully covered the graph fields that incident made visible —
`linked_things`, `dependencies`, `blocks`, `parent`, `definition`, `triggers` —
and the insight written the same day stated the general rule. But the rule was
never *re-derived at the list*: `informed_by` (provenance pins) and `parties`
(conflict members) carry producer-local ids just as much, and they leaked
across the MCP boundary for two versions until an external review read the
schema against the list (review 6, finding 2; fixed in v3.17.4, ff440a1).

The subtle part is that the insight corpus *had the rule*. Knowing the rule and
encoding the rule are different acts; the list is where the rule either becomes
mechanical or quietly narrows to an anecdote.

## How to Apply

At any defensive enumeration:

1. **State the rule beside the list** — a comment naming the class ("every
   relational field", not "the fields from the road test"), so the next field
   author knows membership is derived, not historical.
2. **Walk the class definition once** — the schema, the CORE_FIELDS registry,
   the spec — and admit every member, including ones no incident has exercised.
3. In review, the question is never "does the list cover the bug?" but **"what
   else satisfies the rule this list claims to enforce?"**

## Context

Synthesised 2026-07-03 during the reviews-5+6 remediation session, from review
6's finding that the MCP egress strip list missed `informed_by` and `parties`
— one field-class over from the exact leak the list was built to close.
