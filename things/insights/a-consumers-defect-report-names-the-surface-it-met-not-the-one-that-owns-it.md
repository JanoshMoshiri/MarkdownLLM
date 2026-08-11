---
id: a-consumers-defect-report-names-the-surface-it-met-not-the-one-that-owns-it
type: insight
status: active
version: 1.0
created: 2026-08-11
session: 2026-08-11
source: agent
confidence: high
origin: inferred
exposed: true
tags: [membrane, porch, diagnosis, upward-signal, attribution]
disposition: keep-active
disposition_reason: "Dismiss when an upstream-filed ask carries a mechanical ownership trace as part of its shape (the filer names the surface AND the evidence for who authors the fact), so the verification is built in rather than owed by the receiver. Until then this is live at every porch-filed finding."
linked_things:
  - id: shared-domain-failures-are-a-framework-signal-without-a-path
    relation: extends
    notes: "That insight established the signal must travel up. This is the receiving discipline once it does: the signal arrives correctly identifying the FAILURE and confidently misidentifying its OWNER, so the framework verifies attribution mechanically before acting on it."
  - id: asks-travel-as-exposed-things
    relation: informs
    notes: "The ask crosses well; the causal claim inside it does not carry the same warrant as the observation. Read the observation as evidence and the attribution as a hypothesis."
  - id: substrate-reconciliation-2026-08-09
    relation: informs
    notes: "The case: two domains filed high-confidence findings blaming the bootstrap plugin; the mechanical trace put both defects in the framework's own generator, which the plugin had faithfully reproduced. Fixing the named surface would have bought one session and left the cause."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: complements
    notes: "Same family. That one: a check reporting on what it cannot see. This one: a filer reporting on the only layer it can see — the surface it met — with the owning layer outside its view by construction."
---

# A consumer's defect report names the surface it met, not the one that owns it

Two domains independently filed findings against `markdownllm-bootstrap` on
2026-08-08 — both careful, both `exposed`, both high confidence, and both
wrong about the owner. The QMS insight stated that the bootstrap's
required-reading list "was short against the domain's own naming." The
mechanical trace found the opposite: the list matched the domain's generated
tier-routing block *exactly*, and it was the framework's generator that never
routed `prompts/`. The sibling domain's finding had the same shape — an
agent obeying the generated instruction "load skills relevant to session
intent" over the kernel's unconditional "read the specification skill before
writing," and filing it as a plugin defect.

Neither report was careless. They were **structurally unable** to name the
right owner: a consumer sees the surface it met. The layer that *authored*
the fact sits outside its view, and the carrier reproduces the fact
faithfully — which is exactly what makes the carrier look responsible.

## The receiving discipline

An upstream-filed finding carries two claims with very different warrants:

- **The observation** — *these four steps went unperformed; the reading list
  omitted these files* — is first-hand evidence, and usually sound.
- **The attribution** — *therefore the defect is in X* — is a hypothesis
  formed from one vantage, and it inherits that vantage's blind spot.

So: take the observation as evidence, treat the attribution as a lead, and
**trace ownership mechanically before fixing anything** — read the generator,
not the artifact; the schema, not the list; the code, not the prose that
describes it. The question is always *which surface authored this fact?*, and
it is nearly always answerable in minutes.

The cost of skipping the trace is not a wasted fix — it is a fix that
*appears* to work. Patching the named carrier removes the symptom for one
session while the owning surface keeps minting the same defect into every
consumer, including the ones that have not noticed yet.

## Why this is on the porch

Every domain in the estate can file upstream, and the estate wants them to.
This is the counterpart discipline on the receiving side, and it belongs
where both producers and consumers can read it: file the observation with
confidence, hold the attribution loosely, and let whoever receives it prove
the owner mechanically.
