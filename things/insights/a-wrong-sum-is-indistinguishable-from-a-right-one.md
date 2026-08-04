---
id: a-wrong-sum-is-indistinguishable-from-a-right-one
type: insight
status: active
version: 1.0
created: 2026-08-04
session: 2026-08-02
source: build
confidence: high
origin: stated
tags: [arithmetic, calculation, no-silent-default, floor, refusal, failure-modes]
linked_things:
  - id: deterministic-calculation
    relation: informs
    notes: "Four separate refusals in calc.py exist for this one reason, and each is a place a reasonable implementation would have returned something. The insight was found by building them, not before."
  - id: divergence-is-an-unrouted-decision
    relation: complements
    notes: "Same family — the floor detects, the agent routes, the operator decides. This is the case where failing to detect produces not a missed routing but a confident false answer."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: complements
    notes: "The opposite failure on the same axis. That one is about noise costing attention; this one is about silence costing correctness. A calculation floor has to satisfy both: quiet when healthy, refusing when uncertain."
---

# A Wrong Sum Is Indistinguishable From A Right One — Which Is Why Arithmetic Refuses

## The Insight

The no-silent-default law has an **arithmetic form that is sharper than its
trigger form**, and the difference is about what the failure *looks like*.

A trigger that cannot be evaluated and says nothing costs **attention**: some
work does not surface, and the gap is at least the kind of thing a person can
notice is missing. A *sum* that cannot be computed honestly and returns
something anyway costs **correctness**, and it is unnoticeable by construction:

> **`14,203.55` computed over the wrong denominator looks exactly like
> `14,203.55` computed over the right one.**

There is no surface feature of a number that reveals what it was drawn from.
Every other class of floor output carries some shape you can inspect — a list
you can read, a status you can compare, a reference you can follow. A figure
carries nothing. It is the one output where the only evidence of correctness is
the process that produced it, which means the process has to refuse rather than
approximate.

## Why It Matters

Building `calc.py` produced four separate refusals, and each one is a place
where a reasonable implementation would have quietly returned a value:

1. **A key present in only some entries of a list.** The obvious behaviour is to
   sum the entries that have it. That silently changes the denominator, and the
   resulting total is a real number that is not the number anyone asked for.
2. **A selected thing missing the field.** Same shape, one level up: a new
   expense record without `amount` would shrink a period total invisibly.
3. **A filter that matched nothing.** `sum()` of nothing is legitimately zero —
   so this one cannot refuse, and instead every aggregate reports the count it
   ran over. A confident zero is the single most dangerous output in the module,
   because zero is a plausible answer to almost any money question.
4. **A quarantined input.** Excluding it is correct; excluding it *silently* is
   worse than including it, because a total that dropped its evidence reads
   exactly like a total that had none to drop.

Cases 1, 2 and 4 all had the same tempting implementation — skip the awkward
input and carry on — and all three would have produced numbers that pass every
review a human can perform by looking at them.

## The Generalisation

**Where an output carries no evidence of its own derivation, the floor's duty
shifts from reporting to refusing.** Most of the framework's mechanical surfaces
are safe to be incomplete, because incompleteness is visible in the output. A
calculation is not, so its incompleteness has to be converted into something
that is: a refusal with a reason, or a denominator printed beside the figure.

This is also the argument for the declared derivation itself, one level up. An
asserted total is a number with its provenance deleted; the whole `computed:`
mechanism exists because the only way to make a figure inspectable is to keep
the derivation next to it.

## What Would Change This

Nothing observed so far. The counter-pressure to watch for is the opposite
failure — refusals so eager that operators stop declaring derivations at all.
The mitigation already in place is that a refusal must always name the specific
input that caused it (which entries, which ids), so it reads as a fixable fact
about the corpus rather than as the tool being difficult.
