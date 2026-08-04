---
id: divergence-is-an-unrouted-decision
type: insight
status: active
created: 2026-06-30
session: 2026-06-30
confidence: high
origin: external
verified: true
verified_by: Janosh Moshiri
source_domain: code-architect
source_domain: code-architect
source_id: divergence-is-an-unrouted-decision
source_commit: bd8fc48
promoted_to: llm-driven-systems-manifesto
tags: [primitive, drift, consistency, belief-revision, cross-domain]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: informs
    notes: "Named as a constitutional recognition in the manifesto (v2.6); the manifesto points here for the canonical articulation"
---

# A model–reality divergence is an unrouted decision — never resolve one silently or by blur

## The Insight

A model and the reality it describes will always diverge. The value is not in *preventing*
divergence — that is impossible — it is in the **discipline of routing each divergence**, and
in never letting one resolve by default or by blur. Every divergence between a model and its
reality is an *unrouted decision*. There are exactly three honest routes:

1. **Restore the model** — the divergence is a regression/violation; bring reality back to the
   spec.
2. **Revise the model** — the spec was incidental or wrong; change it, *with recorded
   rationale* — never a silent edit.
3. **Spawn new work** — the divergence revealed genuinely new scope; it hands off to a
   requirement-driven process rather than being absorbed here.

The two cardinal sins are the ways of *not* routing: **silent default** (let it resolve
however it falls out) and **blur** (call a regression an improvement, or call new scope a
bug-fix). The taxonomy is the safeguard; the recording is what keeps it honest and traceable.
Routing is *informed* by walking the graph both ways: **forward** (what does this cascade into
— blast radius) and **backward** (why is it this way — the provenance trace). A route chosen
without the backward walk is how an incidental behaviour gets mistaken for a contract.

## Why It Is a Primitive, Not a New Mechanism

This is the spine beneath machinery the framework **already has, un-unified**. Five faces of one
primitive, each grounded in an existing spec:

- **`change-reconciliation`** is the forward cascade once a divergence is routed — its driver
  *names the inflection*, its Walk has exactly three outcomes (consistent / revise /
  contradiction), and it already calls itself *"a primitive, not a checklist."*
- **`belief-revision`** is route 2 and the holding state before it — *"holding a contradiction
  in explicit tension is a valid, meaningful state,"* built precisely so the agent never
  *"synthesise[s] a plausible but wrong answer from both"* (the anti-blur law).
- **`provenance`** is the recorded *why* that makes a revision traceable, and the quarantine
  (`origin: external`, `verified: false`) that refuses to let an unrouted external divergence
  silently inform an output.
- **`validate`** is the no-silent-default law in mechanical form — *"do not silently fix issues
  — report what you found and changed."*
- **`re-quarantine-on-drift`** (the cross-domain MCP freshness check) is the same primitive on
  the horizontal/peer axis: a pinned model versus a moved reality re-opens the quarantine and
  hands the human the decision rather than resolving silently to "fresh."

It presents as *primal* rather than as a software tactic because a MarkdownLLM domain **is
itself a model of a reality it does not control** — the thing-graph is the model; git and the
world are the reality. So this is the constitutional primitive of *any* model-of-reality
substrate, which is exactly what the framework is. It also generalises lenses already at work:
requirements-as-hypothesis (the model is never frozen truth), failure-cost-sets-the-bar
(whether to take route 3 now turns on blast radius), and traceability-is-the-definition-of-done
(a routed divergence traces to a decision; an unrouted one is silent debt).

## Enshrinement — Named, Not Bolted On

Promoted to the manifesto (v2.6) as a **recognition**, deliberately adding **zero new
mechanism**. The win is not fewer files — the five faces each change at a different rate and
serve a different beat, so by the framework's own cohesion test they rightly stay separate
things. The win is fewer *roots*: five mechanisms that looked like five inventions now trace to
one named spine. The introduction obeyed the primitive itself — a model–reality divergence (the
manifesto did not name a pillar that reality showed was real) routed via **route 2**: revise the
framework's model, with recorded rationale, through the framework's own change process. See
`things/decisions/divergence-primitive-promotion`. Anything less — a sideways bolt-on — would
have disproved the primitive in the act of asserting it.

## Provenance

Originated in the **code-architect** domain (`source_id: divergence-is-an-unrouted-decision`,
`source_commit: b14ec95`), surfaced 2026-06-30 while designing how a `refactoring-process` should
treat a failing characterization test — not pass/fail but a three-way adjudication. Handed to the
framework as a **thin referential** over the domain-to-domain MCP channel (the porch carried a
pointer; the thing is the artifact), imported `origin: external` and held `verified: false` until
the operator confirmed it — which the operator did by making the promotion decision. The channel
test the handoff doubled as: passed.
