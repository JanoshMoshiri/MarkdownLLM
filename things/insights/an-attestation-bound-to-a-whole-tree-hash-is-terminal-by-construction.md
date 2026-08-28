---
id: an-attestation-bound-to-a-whole-tree-hash-is-terminal-by-construction
type: insight
status: active
version: 1.0
created: 2026-08-28
session: 2026-08-28
source: execution
confidence: high
origin: observed
tags: [evidence, sealing, ordering, release, explorer]
linked_things:
  - id: some-changes-are-verifiable-only-by-publishing
    relation: complements
    notes: "That names evidence a repository cannot produce about itself; this names the ordering constraint on the evidence it can."
  - id: explorer-ui-increment-2026-08
    relation: derived-from
---

# An attestation bound to a whole-tree hash is terminal by construction

## The observation

The Explorer's evidence bundle binds every artefact to one subject hash
over the whole reviewable tree — source, tests, tools, docs, packaging.
Some artefacts also *carry* that hash internally, because an observation
about behaviour has to say which bytes it observed.

Closing the increment, I re-stamped the browser evidence, rebuilt the
index and ran the verifier. It failed: subject mismatch. So I fixed the
mismatch and ran again. It failed again. Four cycles, each triggered by
an edit that was itself a *response to the previous verification* — a
traceability pointer, a manifest field, the verifier's own rule. Every
correction moved the tree, and moving the tree invalidated the
attestation I had just made about it.

I was not fighting a bug. I was fighting an ordering I had not noticed
was mandatory.

## Why this is structural

A hash over the whole tree makes attestation **the last act, or a lie**.
There is no partial ordering to exploit:

- Anything that edits the tree *after* stamping invalidates the stamp.
- The verifier's own findings usually require tree edits to resolve.
- So "verify, fix, verify" is not a loop that converges — each pass
  restarts the thing it is trying to finish.

The convergent order is different in kind:

1. Finish **every** change to the reviewable tree, including the ones the
   verifier will ask for.
2. Re-run the producers whose output is no longer true of that tree.
3. **Then** stamp, index and verify, in one uninterrupted pass.
4. Treat any further edit as a full re-attestation, not a touch-up.

## The trap inside it

Evidence artefacts are excluded from the subject — that is what makes
step 3 stable, since stamping does not move what it attests to. But the
exclusion is easy to over-trust. `tests/traceability.yaml` sits under
`tests/` and *is* in the subject; `tests/evidence/` is not. Two files a
directory apart, on opposite sides of the boundary. Every wasted cycle I
spent came from editing the first while thinking I was editing the
second.

## The rule

> Where evidence names its subject by whole-tree hash, sealing is a
> terminal operation. Plan the increment so that the last thing that
> happens is the seal — and know exactly which paths are inside the
> subject, because the ones that surprise you are the ones adjacent to
> the excluded directory.

A mechanical aid exists and is worth building: have the sealing tool
refuse to run against a dirty working tree, so the ordering is enforced
rather than remembered.
