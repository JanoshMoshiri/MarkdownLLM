---
id: cold-read-of-the-seams-release
type: plan
status: not-started
version: 1.0
created: 2026-08-26
priority: medium
tags: [review, cold-read, verification, revision-binding, independence]
linked_things:
  - id: review-independent-seams-verification-2026-08-26-claude
    relation: references
    notes: "The verification this commissions a control for. That record's own limits section names why it cannot be the last word: the verifier designed the sprint and drafted its handover."
  - id: a-verifier-assumes-the-inputs-it-did-not-observe
    relation: implements
    notes: "The reason a third party is wanted rather than a second pass by the same agent: the designer-verifier's blind spot is structural, not effort-related."
  - id: framework-retrospective-2026-08b
    relation: references
    notes: "The retrospective fires 2026-08-27 and is the natural place to decide whether to commission this, at what depth, and against which snapshot."
---

# Cold Read of the Seams Release

**The need.** `3.36.0` shipped revision binding, the self-authorization
guard, activation semantics and two doctrine seams. It was designed in
one harness, built in another, and verified back in the first — but the
verifier was also the designer and the author of the handover brief. That
verification confirmed the build matches the design and that the guard
survives live attack; it cannot confirm that **the design itself was
right**, and it demonstrably could not see what the builder was actually
briefed with.

**The ask.** One independent agent, zero session context, adversarial
brief, reading the published `3.36.0` state — the house cold-read shape
(`reviews/REVIEW-independent-*`). Specific questions worth handing it,
without leading it:

- Does revision binding do what `workflow-state.md` v0.6 claims, and is
  the claim itself the right one?
- Is the self-authorization guard's separation sufficient, or does an
  unconsidered path re-open it (the `definition` id swap was seen and
  deliberately left; are there others)?
- Do the activation/fulfilment semantics carry their weight, or are they
  ceremony on references that already existed?
- Is `operating-model.md` still mechanism-free, or has 0.2 smuggled?

**Not a release gate.** `3.36.0` publishes without this. This is the
control group for a verification whose limits are recorded, and its value
falls if it waits long enough for the corpus to move underneath it.

**Timing.** The 2026-08-27 retrospective decides whether to run it, at
what depth, and against which commit — that judgement is the
retrospective's, not this plan's. If it declines, this closes as
`cancelled` with the reason recorded rather than lingering.
