---
id: a-declaration-is-inert-until-its-mechanism-is-current
type: insight
status: active
version: 1.0
created: 2026-08-23
session: 2026-08-22
source: both
confidence: high
origin: synthesised
tags: [policy, generated-mechanism, staleness, hooks, autopush, silent-failure]
linked_things:
  - id: a-sharing-parameter-no-caller-passes-is-a-fix-that-did-not-happen
    relation: extends
    notes: "Same family — a change landed where nothing consumes it. There the unwired side was the call site; here it is the generated mechanism, stale by vintage rather than absent by omission."
  - id: a-generated-contract-change-is-an-estate-migration
    relation: complements
    notes: "That insight names the outbound cost of changing a generator; this names what accumulates when the migration is never run — consumers whose bodies silently lack every leg added since."
  - id: existence-is-not-currency
    relation: complements
    notes: "The artifact existed and was stale. The new face: a *policy* can be perfectly current while the artifact that would enforce it is not, and nothing checks the pair."
---

# A Declaration Is Inert Until Its Mechanism Is Current

## The Insight

Configuration that is read by a **generated mechanism** has two halves, and
they age separately. The declaration is authored — you edit it, and it is
current the moment you save it. The mechanism is *rendered*, installed once,
and then frozen at whatever vintage it was installed at. Declaring a policy
that a mechanism older than the policy cannot read produces no error and no
warning: the config says the right thing, the mechanism does the old thing,
and the two never meet.

This is worse than a missing feature, because the declaration is *visible*.
Anyone auditing the estate reads the config, sees the policy, and concludes
it is in force.

## How It Surfaced

The operator ruled that all thirteen domains declare `git: autopush: true`,
so remote sessions would find published state. Setting it is a one-line edit
per domain — and it would have published **nothing**. Every domain's git
hooks predated the `MDLLM_ROUTE` format, and those post-commit bodies carried
no autopush leg at all: the leg was added to the *renderer* after those hooks
were installed. Thirteen domains would have carried a live, correct,
authoritative declaration that no installed byte could read.

It was caught by grepping a hook body before trusting the flag — not by any
check. `doctor` does report `Floor: STALE`, but nothing joins that fact to
"and therefore your newest declarations are unreadable."

## Why It Matters

- **The failure is silent and looks like success.** Both halves inspect
  clean in isolation. Only the *pair* is wrong, and no surface owns the pair.
- **Staleness is cumulative and invisible.** A hook installed at v3.20 lacks
  every leg added since. The estate had drifted three releases; the policy
  change is what finally exposed it, by accident.
- **Rollouts must reinstall, not just declare.** Any estate-wide policy that
  a generated mechanism enforces has two deliverables: the declaration *and*
  a current mechanism. Shipping one is shipping neither.

## The Rule

Before relying on a declaration, verify the mechanism that reads it is at
least as new as the feature the declaration names — read the installed bytes,
not the renderer's. When rolling a policy across an estate, reinstall the
mechanism in the same pass, and confirm the effect (here: an actual published
push) rather than the configuration.
