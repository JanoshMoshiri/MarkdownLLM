---
id: a-crossing-thing-carries-its-producers-private-graph
type: insight
status: promoted
version: 1.2
created: 2026-06-26
promoted_to: mcp-domain-server-design
session: 2026-06-26
source: both
confidence: high
origin: synthesised
tags: [cross-domain, mcp, egress, id-space, serialization, boundary]
linked_things:
  - id: cross-domain-handoff-is-built-inbound-only
    relation: supports
  - id: cross-domain-handoff-is-verified-external-input
    relation: supports
  - id: provenance-specification
    relation: informs
---

# What Crosses A Domain Boundary Includes The Producer's Private Graph — Source-Scope It On Egress

## The Insight

Exposure controls *which* things cross a domain boundary; it does not control
*what is inside* a crossing thing. A thing carries its frontmatter **relationship
graph** (`linked_things`, `dependencies`, `parent`, `definition`, `triggers`), and
those ids live in the **producer's id-space** — foreign and unresolvable in the
consumer's. Shipped raw, they masquerade as consumer-resolvable links and the
consumer tries (and fails) to resolve them. So egress must **source-scope**: strip
(or explicitly namespace) the producer's internal graph, leaving descriptive
frontmatter + content + the provenance triple. The relationship graph stays
reasoning-opaque across the seam — the same comprehensible-alone discipline native
links obey, applied to serialization.

The general rule, beyond MCP: **at any boundary where a thing is serialized into a
foreign id-space, its internal references do not cross as live links** — they are
either dropped or made visibly foreign.

### The third category (added v1.2, 2026-08-30)

The original split was binary — the producer's *relationship graph* (stripped)
versus *descriptive frontmatter* (crosses). One field belongs to neither, and
sat on the wrong side for two months: **`exposed` is the producer's
face-membership flag.** It is not a relationship and not a description of the
thing; it is a statement about *this producer's* served face. Crossing, it
told the consumer "publish this" — so a consumer landing the render verbatim
re-exported the import without ever making its own exposure call. Exposure by
copy, which is exactly the decision `write.thing.md` asks each author to make
deliberately.

Found live when the estate's first mirror re-sync landed both mirrors carrying
the flag. Now stripped beside the structural set
(`_EGRESS_PRODUCER_MARKERS`), with `thing.md` v2.22 stating the rule.

Two lessons ride with it, both sharper than the fix:

- **The test asserted the leak.** `test_mcp_get_deliverable_stamps_triple`
  *required* `exposed: true` to cross — written into this insight's own
  originating fix, where the binary split made `exposed` look descriptive by
  elimination. A test built from the symptom encodes the symptom as the
  contract, and then defends it. This insight's own commit comment warned
  about a list "built from the road test's symptom, not from the rule"; the
  same commit did it again, one field over.
- **So the operative question is not "is this a relationship?"** but
  ***whose* fact is this?** Any field asserting something about the producer's
  own configuration — its face, its policy, its local state — belongs to the
  producer and does not cross, whether or not it names an id.

## Why It Matters

It closes a leak the exposure model alone misses, and it is a clean second axis to
the cross-domain work: `cross-domain-handoff-is-built-inbound-only` is about the
*direction* of the seam; this is about the *granularity* of what crosses through
it. A crossing thing is content + description + provenance — never the producer's
private wiring. If a cross-domain link is ever genuinely wanted, it must be a
*deliberate, source-scoped* exposure, not a raw leak of foreign ids.

## Context

Surfaced 2026-06-26 on the first live cross-domain read: the consumer agent fetched
the architecture deliverable and tried to resolve a `linked_things` id that lived
only in the producer's domain — finding nothing. The fix (`mdllm`
`_mcp_egress_meta`) strips the internal graph on both crossing paths
(`get_deliverable` and the `thing://` resource read); descriptive fields and the
reference triple still cross. The consumer's *read* surfaced the design edge — the
second time this arc that the consuming side, not the producing side, exposed it.
