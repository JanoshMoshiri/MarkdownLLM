---
id: a-uniform-answer-is-a-dead-judgment
type: insight
status: active
version: 1.0
created: 2026-08-05
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "The measurement to watch: the estate's disposition distribution. It stays active until a domain retrospective produces the first promote/dismiss — or until the distribution itself becomes something a retrospective reads mechanically."
tags: [insight-lifecycle, disposition, retrospective, signal, session-memory]
linked_things:
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: complements
    notes: "Its mirror. That insight: a CHECK whose firing is uniform stops informing the operator. This one: a JUDGMENT whose answer is uniform stops informing the system. Together they bound the channel from both ends."
---

# A uniform answer is a dead judgment — 46 of 46 dispositions say keep-active

## The Insight

The insight-disposition prompt exists to extract a judgment: promote what
has shipped, dismiss what aged out, keep what still earns its place. The
2026-08-05 re-sweep measured the estate's lifetime answer distribution:
**46 dispositioned insights, 46 `keep-active`, zero `promote`, zero
`dismiss` — ever, anywhere.** Meanwhile the undispositioned population grew
in the same window.

When a judgment's answer distribution collapses to a single value, the
judgment has become a pass-through. The ritual is being *performed* (the
field gets filled, validate goes quiet) without being *made* (nothing is
ever pruned or promoted). The check's silence then reads as health while
the population monotonically grows — session memory as a ratchet, which is
exactly the "backlog rotting" retrospective.md warned about, now with the
rot wearing a completed checkbox.

## Why it happens, and where the fix lives

`keep-active` is the only answer available *at session end*, because
promote/dismiss need aggregate context a single session doesn't hold —
which insights shipped their lesson, which were superseded, which never got
cited again. That context is the retrospective's, and no domain has run one
yet (their cadence clocks mature from mid-August). So this is not a new
mechanism to build: it is a prediction to check. **If the first domain
retrospectives produce promote/dismiss verdicts, the vocabulary was fine
and the forcing function was just late. If they too come back all
keep-active, the disposition step is ceremony and should be said so.**

The general form travels beyond insights: any judgment field whose observed
distribution is a point mass deserves suspicion — the framework's own
`observation-is-a-distribution-not-a-value` candidate makes the same claim
about agent outputs, from the other direction.
