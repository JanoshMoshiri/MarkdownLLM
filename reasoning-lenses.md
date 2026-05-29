---
id: reasoning-lenses-specification
type: specification
status: stable
version: 1.0
created: 2026-05-29
linked_things:
  - id: read-thing-specification
    relation: invoked-by
  - id: write-thing-specification
    relation: invoked-by
  - id: domain-specification-guide
    relation: referenced-by
---

# Reasoning Lenses

## What This Specifies

This document defines the multi-lens reasoning pattern: how domain agents apply multiple simultaneous perspectives when reading or modifying things. This content was previously duplicated across `read.thing.md` and `write.thing.md`; this spec is the canonical source for both.

## What Are Reasoning Lenses?

Reasoning lenses are domain-defined perspectives declared in `[domain]-specification.skill.md`. When a domain defines lenses, every significant read or write operation should be evaluated through all of them before responding to the user.

The lenses pattern is **optional** — it applies only when the domain's spec skill defines them. Not all domains need lenses.

## Applying Lenses in Read Mode

When answering questions or providing analysis, apply lenses after loading the relevant things:

1. **Read the lenses** — From `[domain]-specification.skill.md`, identify all defined reasoning lenses
2. **Evaluate through each lens** — Apply each perspective to the question or situation
3. **Surface conflicts** — If lenses disagree or tension exists, make that explicit to the user
4. **Learn from examples** — If uncertain how a lens applies, load `type: example` things to understand the pattern
5. **Explain your reasoning** — Tell the user which lenses you considered and how they guided your analysis

### Example: Compliance Domain (Read Mode)

If the domain defines lenses like Domain Logic, Compliance Logic, and Audit Logic:

**User:** "Should we store client emails in this new system?"

Your response (through all lenses):
- **Domain Logic:** "Yes, we need them for case management"
- **Compliance Logic:** "Only if we ensure UK data residency and access controls"
- **Audit Logic:** "Only if we can explain the decision and trace all access"

Result: "Yes, but with these conditions: [list]. Here's the audit trail that justifies this."

### When Lenses Conflict (Read Mode)

If lenses give conflicting guidance:

```
Domain Logic says: "Combine these datasets for efficiency"
Compliance Logic says: "That violates minimization principle"
Audit Logic says: "We can explain it, but it's a risk"

Your response: "I see tension between efficiency and compliance. Here's 
the tradeoff. You decide which lens takes priority, then we implement accordingly."
```

Don't hide conflicts; surface them. That's where user judgment matters.

## Applying Lenses in Write Mode

When making or proposing changes, apply lenses **before** modifying anything:

1. **Read the lenses** — From `[domain]-specification.skill.md`, identify all defined reasoning lenses
2. **Evaluate the proposed change through each lens** — What does each perspective say?
3. **Check for conflicts** — Do all lenses agree the change is sound?
4. **If conflict exists, surface it** — Don't proceed silently; explain the tension
5. **Learn from examples** — If uncertain, load `type: example` things to understand patterns
6. **Explain your reasoning** — Tell the user which lenses you considered and why you're proceeding (or not)

### Example: Compliance Domain (Write Mode)

**User:** "Mark this data processing task as complete"

You reason through the lenses:
- **Domain Logic:** "Yes, the task is done"
- **Compliance Logic:** "Did we maintain audit trail? UK data residency?"
- **Audit Logic:** "Can we explain why this is complete? Is the decision traceable?"

Your response:
```
I can mark this complete, but let me confirm:
✓ Domain Logic: Yes, the task is finished
✓ Compliance Logic: Confirmed UK processing, audit trail attached
✓ Audit Logic: Decision is documented and traceable

Proceeding with completion and documenting the decision.
```

### When Lenses Conflict (Write Mode)

**User:** "Consolidate these two datasets for easier analysis"

You evaluate:
- **Domain Logic:** "Yes, consolidation helps analysis"
- **Compliance Logic:** "No, violates data minimization principle"
- **Audit Logic:** "We can explain it, but it's risky"

Your response:
```
I see a conflict:
- Domain Logic says YES (efficiency gain)
- Compliance Logic says NO (violates minimization)
- Audit Logic flags RISK (defensible but weak)

I won't proceed without your decision. Which is your priority?
Would you like me to suggest alternative approaches that don't violate minimization?
```

Don't hide conflicts. Raise them. The user decides how to resolve tensions between lenses.

## Key Principle

**Lenses make disagreement first-class.** The value of multi-lens reasoning is not consensus — it's surfacing the tensions that would otherwise be silently resolved by default. When lenses agree, proceed with confidence. When they conflict, stop and surface it. The user decides; the agent explains the tradeoffs.
