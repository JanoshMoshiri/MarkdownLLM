---
id: a-crossing-thing-carries-its-producers-private-graph
type: insight
status: promoted
version: 1.1
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
