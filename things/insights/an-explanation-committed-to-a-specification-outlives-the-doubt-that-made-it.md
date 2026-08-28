---
id: an-explanation-committed-to-a-specification-outlives-the-doubt-that-made-it
type: insight
status: active
version: 1.0
created: 2026-08-28
session: 2026-08-28
source: execution
confidence: high
origin: observed
tags: [epistemics, specification, diagnosis, harness, evidence, explorer]
linked_things:
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: extends
    notes: "The harness co-authors the observation as well as the work: a pane that silently stops compositing produced the anomaly that produced the false explanation."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: complements
  - id: explorer-ui-increment-2026-08
    relation: derived-from
---

# An explanation committed to a specification outlives the doubt that made it

## What happened

A grid track would not change when its width came from a custom
property. I investigated, found that removing a CSS transition made it
work, and reasoned to a cause: the hardened Git-for-Windows environment
nulls system configuration, `core.autocrlf` disappears, and end-of-line
handling shifts underneath the diff. It was coherent, it fitted the
evidence I had, and I wrote it into `design.md` as a load-bearing
justification for a flag — *"required, not cosmetic"* — with the causal
chain spelled out.

Days later, closing the increment, a review asked whether that flag had a
side effect. I went to reproduce the original behaviour and could not.
Not in a clean fixture, not in the real repository, not with the hardened
environment, not without it, not through the adapter itself. Eight
configurations, all correct, flag or no flag.

The real cause was elsewhere and much duller: the browser pane I was
observing through does not composite frames. A CSS transition therefore
*never advances* — it pins its property at the start value for ever — and
a running transition outranks even an `!important` inline style. Every
"the value will not apply" observation was one symptom of one silent
tool degradation, and it had nothing to do with git at all.

## The asymmetry that makes this dangerous

A hypothesis in a head is cheap to revise; it carries its own
uncertainty. **The act of writing it into a specification strips that
uncertainty off.** Every later reader — including me, a day later —
receives it as a settled fact with a mechanism attached, and a mechanism
is precisely what makes a claim feel checked. Nobody re-derives a stated
cause. They build on it.

Worse, the explanation was *useful*: it justified a real flag that
appeared to fix a real problem. Utility is not evidence. The flag was
inert; the fix had been removing the transition, which I did in the same
edit.

## The two failures, separated

They are worth keeping apart because they have different remedies:

1. **I diagnosed from a degraded instrument without knowing it was
   degraded.** The pane never announced that it had stopped compositing;
   its silence read as normal operation. *Remedy:* when a tool's output
   is the sole basis for a causal claim, establish independently that the
   tool is working — here, one check that any transition advances at all
   would have exposed it.

2. **I recorded the diagnosis at the confidence of a finding rather than
   of a hypothesis.** *Remedy:* an explanation that has not been
   reproduced under variation should say so in the text that carries it.
   "Observed once, mechanism inferred, not yet reproduced" costs nine
   words and would have survived contact with the truth.

## The rule this leaves

> A specification may record what was observed at any confidence. It may
> record *why* only at the confidence that the why has been reproduced.

The correction is now in the repository: the flag and its account are
both removed, and the commit says plainly that the account could not be
reproduced in any configuration. That is the shape the record should take
— the retraction stated, not the paragraph quietly deleted.
