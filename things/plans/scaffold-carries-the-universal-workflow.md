---
id: scaffold-carries-the-universal-workflow
type: plan
status: not-started
version: 1.0
created: 2026-08-25
priority: high
tags: [scaffold, workflow, template, birth, adoption]
linked_things:
  - id: universal-workflow-methodology
    relation: references
    notes: "The thing this plan makes travel: every scaffolded domain should be born carrying the methodology, not discover it later."
  - id: operating-model-specification
    relation: references
    notes: "The composition doctrine a newborn domain should be able to reach from its first session."
---

# Scaffold carries the universal workflow

**The need (operator, 2026-08-25):** the methodology exists in the
substrate, exposed — but a domain only benefits if it *arrives*. The
operator has been running the loop organically, in his head, precisely
because no domain was born with it as a declared, reflectable structure.
Every scaffolded domain should take the workflow with it from birth, the
overall ideas encoded from the beginning.

**Current state:** `mdllm scaffold` instantiates a fixed template set
(entry file, four skills, prompts, generic `workflow-definition` /
`workflow-run` skeletons). Nothing delivers `universal-workflow-methodology`
itself. Existing domains can import it from the framework face today
(reference triple + quarantine + verify) — this plan is about *future*
births, not the existing estate.

## Phases

- [ ] **Design the delivery shape.** Two candidates, decide with pinned
  inputs: (a) scaffold copies the methodology into the newborn's
  `things/` as a pre-pinned import — source triple to the framework
  commit at scaffold time, `origin: external`, quarantined until the
  human verifies — the domain is born with it on its floor; or (b) the
  domain-workflow skill template gains a section referencing it on the
  framework's face with import instructions — lighter, defers the copy.
  Option (a) matches the felt need (born carrying it); the quarantine
  flip doubles as the operator's conscious adoption act.
- [ ] **Template work.** Whichever shape wins: the template file(s),
  including instance guidance — how a domain declares its specialised
  definitions `implements` against the atom, and where the two shapes
  (accumulative / repeatable) and entry-tier declaration belong.
- [ ] **Scaffold change + tests.** The transactional birth sequence
  gains the new step; focused tests; budgets unchanged.
- [ ] **Docs walk.** `first-hour.md` and `operator-guide.md` learn that
  a newborn domain arrives with the methodology; `domain-refresh.md` if
  the import shape interacts with refresh.

Run this through `substrate-floor-development` when picked up — it is a
floor change and earns the full traversal.
