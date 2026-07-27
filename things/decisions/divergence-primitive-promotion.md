---
id: divergence-primitive-promotion
type: decision
status: made
created: 2026-06-30
session: 2026-06-30
decided_by: human
confidence: high
source: code-architect
informed_by:
  - id: divergence-is-an-unrouted-decision
    commit: aae0712
linked_things:
  - id: llm-driven-systems-manifesto
    relation: informs
    notes: "The decision enshrined the primitive as a recognition in manifesto v2.6"
  - id: divergence-is-an-unrouted-decision
    relation: informs
---

# Decision: Promote "A Divergence Is an Unrouted Decision" to a Framework Primitive

## Context

The insight `divergence-is-an-unrouted-decision` originated in the **code-architect**
domain and was handed to the framework over the domain-to-domain MCP channel as a thin
referential (reference triple: `code-architect` / `divergence-is-an-unrouted-decision` /
`b14ec95`). It claims that a model–reality divergence is an *unrouted decision* — route it
(restore / revise / spawn), never resolve by silent default or blur — and that this is the
single spine beneath four-to-five mechanisms the framework already has un-unified. The
question put to the framework: enshrine it, and if so, in what form?

## Inputs Considered

- The canonical articulation (`informed_by`, pinned at `9166772`) and its claim that
  `change-reconciliation`, `belief-revision`, `provenance`, `validate`, and
  `re-quarantine-on-drift` are five faces of one primitive — verified against each spec's
  actual text, not asserted.
- The framework's restraint razor: net concepts must go *down*; ceremony is rejected; a
  promotion earns standing only by *clarifying*, never by adding a layer.
- The cohesion test (`thing.md`): the five faces change at different rates and serve
  different beats, so they rightly stay separate things — a structural merge would destroy
  information.

## Options

1. **Decline / keep domain-local.** Leave the primitive in code-architect. Rejected: the
   evidence (this domain, a prior regulated domain, and the framework's own five-faced
   machinery) shows it is real at substrate level, and the framework is its natural host.
2. **Add a new specification.** Write a `divergence-routing.md` spec sitting above the five
   mechanisms. Rejected: that is the bolt-on the primitive itself warns against — it adds a
   sixth thing and new ceremony, disproving the primitive in the act of asserting it.
3. **Name it as a recognition at manifesto altitude, zero new mechanism (chosen).** Add a
   law to the manifesto that names the spine and points each existing mechanism at it; the
   limbs stay where they are and gain a one-line back-reference.

## Decision

Take **option 3**, by **route 2** of the primitive itself: the framework's model did not name
a pillar that reality (multiple domains) shows is real, so revise the model — *with this
recorded rationale* — through the framework's own change process. Enshrined in
`llm-driven-systems.manifesto.md` v2.6 as the recognition "The Primitive Beneath: A Divergence
Is an Unrouted Decision," with `implements` edges and one-line naming added to
`change-reconciliation`, `belief-revision`, `provenance`, and `validate`. **No new mechanism,
no new check, no new hook** — the acceptance test was: after promotion, is there anything new an
agent must *do*? There is not. The only change is that five mechanisms now visibly trace to one
named root.

The operator made the call; the reasoning was developed jointly with the framework agent.

## Consequences

- The manifesto carries the primitive as a constitutional recognition (v2.6); the canonical
  insight is `active` and cited from it.
- The five faces are unchanged in behaviour; each now names the spine it implements.
- The kernel is untouched — the primitive is rationale/recognition, not a Tier-0 operative
  rule; `mdllm kernel --check` reports in sync.
- The cross-domain handoff that delivered this doubled as the live test of the MCP comms
  channel (manifest → `get_deliverable` with provenance triple). It passed.
- Reversible: the enshrinement is two commits (`9166772` and this seal); revert restores the
  prior manifesto and drops the edges, losing nothing but the name.
