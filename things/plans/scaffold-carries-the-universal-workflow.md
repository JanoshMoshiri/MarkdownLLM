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
`workflow-run` skeletons). Nothing delivers the methodology itself.
Since the 2026-08-25 channel correction the methodology is a **spec**
(`universal-workflow.md`) reaching every domain via framework version +
domain-refresh — so existing domains receive the doctrine with the next
refresh, and what scaffold owes a newborn is not the spec (it arrives
anyway) but a **ready specialisation**: a clean, domain-shaped
workflow-definition written in from birth.

**Parked (operator, 2026-08-25)** — deliberately, not dropped. The
direction when picked up is larger than a template drop: **scaffold
becomes a guided workflow of its own** — a walkthrough that asks the
operator questions and has them define their specialisation as they
answer, rather than handing them files to discover. The operator's own
evidence is the reason: *"I wrote the framework, and even I'm forgetting
it — somebody who doesn't know it will forget quicker and see it less."*
An unguided template repeats the organic-use failure this plan exists to
end.

## Phases

- [ ] **Design the guided birth.** Scaffold's semantic half becomes a
  walkthrough (likely a `workflow-definition` the scaffolding session
  runs): the questions that make an operator define their domain's
  specialisation — stages renamed for their context, entry-tier rule,
  gate authorities, which shape (accumulative/repeatable) their first
  loops take. The deterministic half (`mdllm scaffold`) stays
  transactional and unprompting; the guidance is the agent's leg.
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
