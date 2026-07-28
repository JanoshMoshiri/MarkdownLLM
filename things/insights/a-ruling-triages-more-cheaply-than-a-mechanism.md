---
id: a-ruling-triages-more-cheaply-than-a-mechanism
type: insight
status: active
version: 1.0
created: 2026-07-28
session: 2026-07-28
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "One session's evidence, strong but single. Promote when a third ruling resolves a proposal set as cheaply — or dismiss if the next hard question needs a mechanism to settle it after all."
tags: [rulings, doctrine, design-process, boundaries, restraint]
linked_things:
  - id: membrane-attention-cluster
    relation: informs
    notes: "The plan where both rulings were written before any build; three of six proposals resolved without code"
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "Same restraint from the other side: that insight says don't author primitives; this says write the boundary down instead of building against it"
  - id: cross-domain-readiness-is-a-shared-signal-not-a-producer-push
    relation: supports
    notes: "The ruling formalised what this insight already held — producer blindness as design, not deficit"
---

# A Ruling Triages More Cheaply Than A Mechanism — And Ages Better

## The Insight

When a design question arrives as a *list of proposed fixes*, the highest-value
move is often not to build the good ones — it is to **write down the boundary
that decides all of them**, then build only what survives.

Two rulings were written this session, each a paragraph:

1. **Producer blindness is a boundary, not a bug** — a producer never learns
   who consumes it; publication is an honest commit to the face, delivery is
   the consumer's poll.
2. **Repos are not membranes** — discovering local clones is a filesystem
   fact; a persisted membership registry is the forbidden thing.

Between them they resolved six proposals: three rejected with reasons, one
dissolved into an existing precedent, two confirmed as safe to build. The
builds that followed were small because the rulings had already removed the
hard part — deciding *whether*.

## Why It Holds

A mechanism answers one question and then needs maintaining. A ruling answers
the whole *class* of questions and needs nothing. The `who_i_know` field would
have been perhaps forty lines and a spec section; the ruling that it stays
permanently empty is four lines of comment and a spec subsection — and it also
answers un-expose pre-flight, shared work identity, and every future variant
of "shouldn't the producer just tell them?".

The asymmetry is sharpest under *pressure to be helpful*. An agent handed six
plausible fixes will tend to build the tractable ones, because building reads
as progress. But three of those six were coupling proposals that would have
quietly dissolved the estate's atomicity — and no amount of careful
implementation would have made them right. The cheapest possible response to
a wrong proposal is a written reason, filed where the next session will read
it before proposing it again.

## The Practice

- When a review arrives as a list, look for the **single question underneath
  it** before triaging item by item. Here it was: *is producer blindness a bug
  or a boundary?* Everything else resolved once that was settled.
- Write the ruling into the **normative spec**, not the plan — plans complete
  and stop being read; specs are loaded at reasoning time.
- State it as a ruling with its consequences enumerated, so it reads as
  *settled*, not as *unfinished*. The `who_i_know` comment now says "do not
  finish this" precisely because an empty field looks like a TODO to every
  fresh reader.
- Rulings are the human's to make. The agent's job is to surface the question
  cleanly enough that one paragraph can settle it.
