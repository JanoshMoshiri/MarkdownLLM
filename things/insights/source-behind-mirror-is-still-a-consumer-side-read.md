---
id: source-behind-mirror-is-still-a-consumer-side-read
type: insight
status: active
version: 1.0
created: 2026-07-28
session: 2026-07-28
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Standing design lens for the deferred cross-domain facets (discovery, awareness, permeability): ask what the face already carries before adding an axis. Promote if a second gap dissolves the same way."
tags: [cross-domain, sync, mcp, membrane, estate]
linked_things:
  - id: cross-domain-handoff-is-built-inbound-only
    relation: extends
    notes: "That insight collapsed the producer push onto a consumer poll; this collapses the 'other direction' onto the same poll"
  - id: mcp-domain-server-design
    relation: informs
  - id: cross-domain-sync-catchup
    relation: informs
    notes: "The v3.21.0 build that proved it — DIVERGED + estate-check"
---

# Source-Behind-Mirror Is Still A Consumer-Side Read — The Feared New Axis Dissolved

## The Insight

The estate audit named a sync direction no framework mechanism could see:
**source behind mirror** — a consumer's imported copy edited while the pins
still agree, content flowing backwards outside the loop. The audit assumed
detecting it required an **operator-axis, multi-root tool** reading several
domains at once, and flagged that as a real doctrine risk: one careless
framing away from the global index the design refuses, and from a domain
enumerating its consumers.

Building it showed the new axis was never needed. The face already serves
the exposed thing's *content*, not just its pin. So the second direction is
one extra comparison inside the existing consumer-side poll: **when the
pinned commit equals the source's current per-thing commit but the mirror's
body no longer matches the face, the loop was bypassed** — `diverged`, the
twin of `stale`, read through the same porch, obeying the same membrane.
The multi-root command (`estate-check`) then degenerates into *batching*:
per-consumer reads over operator-named roots, rolled up, ephemeral. It adds
convenience, not information — nothing it prints could not be produced by
each consumer alone.

The general shape: **before concluding a gap needs a new axis of visibility,
check whether the existing membrane already carries the missing signal as a
field you are not yet comparing.** The pin was being compared; the content
was crossing anyway, uncompared. The "missing direction" was a missing
comparison, not a missing channel.

## Why It Matters

- It preserved the isolation doctrine under pressure. The desync was being
  *felt* and the operator ordered deploy-now; the tempting build was the
  doctrine-risky multi-root reader. Because the signal turned out to live in
  the existing channel, the urgent version and the doctrine-clean version
  were the same build.
- It validated on first contact: the first estate run over eleven local
  domains caught one live `diverged` on the longest-standing consumer pair —
  the exact felt failure, mechanically visible, with the disposition
  correctly left to the operator.

## Status / Next

Standing design lens for any future cross-domain gap (discovery, awareness,
permeability — the adjacent facets the handoff insight deliberately
deferred): ask first what the face already carries. Promote toward spec
prose if a second gap dissolves the same way; dismiss if a future gap
genuinely does require a new axis and this lens misleads.
