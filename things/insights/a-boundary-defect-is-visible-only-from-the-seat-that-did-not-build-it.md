---
id: a-boundary-defect-is-visible-only-from-the-seat-that-did-not-build-it
type: insight
status: active
version: 1.0
created: 2026-08-17
session: 2026-08-11
source: both
confidence: high
origin: stated
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: derived-from
    notes: "The plan's own history is the evidence: v1.1 → v1.6 across six alternating Claude/Codex review rounds, each rejection catching a real defect the authoring seat could not see."
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: complements
    notes: "The same-seat loop decays — finds shrink into residue of the loop's own fixes. The cross-seat gate did not decay across six rounds, because each round reviewed a boundary neither seat owns alone; the two loop shapes have different economics."
  - id: an-interface-is-what-its-consumers-call-not-what-it-declares
    relation: supports
    notes: "The sharpest single instance: the undeclared service interface was invisible to the agent who wrote both sides of it, and obvious to the agent who had to implement against only the declaration."
  - id: portability-claims-need-execution-tests
    relation: complements
    notes: "One class of cross-seat find is exactly this insight's subject matter: the authoring harness's runtime assumptions (PATH pythons, external dirname, PyYAML availability) travel invisibly until the other shell executes them."
---

# A boundary defect is visible only from the seat that did not build it

## What happened

The vendor-harness-adapter plan went v1.1 → v1.6 through alternating review
between two agents in two harnesses, each round a cold read of the other's
work against the live tree. Every round found real defects — and every find
had the same shape: it sat exactly where the author's position could not see.

- The **frame** excludes: the adapter-scoped author never looked at spec prose
  addressing one vendor, because prose was outside "adapter foundation" by
  construction. The wider-framed reviewer met it in the first minute.
- The **runtime** doesn't hurt: `dirname`-dependent resolution and
  PATH-python masking cost the author nothing, because the authoring shell
  had both. The managed shell felt them immediately, as failures.
- The **same hand** hides the seam: one agent authored both the ports and
  their consumers, so the undeclared interface satisfied itself; the agent
  who had to implement from the declaration alone hit the gap at once
  (`an-interface-is-what-its-consumers-call-not-what-it-declares`).

None of these were capability gaps. Both agents ran the same greps, read the
same files. What differed was position: reviewer versus generator, wide frame
versus scoped frame, felt pain versus documented claim.

## The rule

**A boundary between two implementations is reviewable only from both of its
sides, and the finds do not decay the way same-seat review finds do.** The
same-seat adversarial loop converges on its own fix residue; the cross-seat
gate kept yielding first-class defects for six rounds, because each handoff
exposes the work to assumptions the author *structurally* could not test —
not would not, could not. The alternating acceptance gate (author stops,
counterpart audits against its own runtime and its own implementation burden,
work returns with named items) is the mechanism that converts that structural
blindness into a work queue.

## Cost and when to pay it

The gate is expensive — six rounds, two harnesses, explicit handoff records.
It earned its cost here because the artifact under construction *was* a
cross-harness boundary. For work that lives entirely inside one seat, the
same-seat loop plus one cold read remains the measured optimum
(`an-adversarial-review-loop-converges-on-its-own-fix-residue`). Choose the
loop shape by where the artifact's consumers sit, not by habit.
