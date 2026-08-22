---
id: estate-wide-autopush-2026-08-22
type: decision
status: made
version: 1.0
created: 2026-08-22
decided_by: human
confidence: high
tags: [publication, autopush, estate, operator-ruling, multi-writer]
informed_by:
  - id: autopush-requires-explicit-authority
    commit: a14b0c3f9439cb14e5058bc5820526e65e2ee402
  - id: framework-kernel
    commit: 6601f2e4c47e6e12277d165b37fbc7e7204f6b1f
linked_things:
  - id: autopush-requires-explicit-authority
    relation: implements
    notes: "That decision made publication fail-closed and required an affirmative declaration; this is the operator supplying exactly that declaration, per repo, for all thirteen domains. It narrows nothing — it exercises the mechanism as designed."
  - id: estate-cadence-cluster
    relation: references
    notes: "The autopush leg this ruling switches on estate-wide."
---

# Decision: Every Domain Declares Autopush

The operator ruled (2026-08-22, by name and explicitly: *"that's a confirmed
request by me, Janosh — we want every domain to have auto push, because
that's the only way the prominence really works properly"*) that **all
thirteen domain repositories declare literal `git: autopush: true`**.

## Why

Remote sessions are arriving. The operator is bringing other agents onto the
estate — a second agent now works the QMS domains, and a harness adapter has
been handed to an external party. A remote session that clones a domain sees
only what was published; work that stops at a local commit is invisible to
it. Fail-closed publication was correct while one machine held the estate,
and becomes an obstacle the moment several do.

## Scope, and what it does not change

- **Domains: yes.** All thirteen declare it; the post-commit leg publishes
  each floor-validated commit.
- **Framework root: no.** It keeps `autopush: false`. A framework release is
  consumed by outsiders and gated by judgement with no mechanical
  completeness check, so that push stays the operator's deliberate act
  (`premature-publish-manufactures-discipline-eroding-urgency` stands).
- The mechanism is unchanged: still fail-closed, still literal-`true`-only,
  still bounded, still never forcing. A rejected push remains divergence
  surfaced and routed, never resolved by force.

## What it cost to make real

The declaration alone would have been inert. Every domain's mdllm hooks
predated the `MDLLM_ROUTE` format, so the tool classified them as operator
hooks and refused replacement — and those old post-commit bodies carried **no
autopush leg at all**. Each domain's three mdllm-marked hooks were verified by
marker, backed up, removed and reinstalled at the current contract. That gap
is recorded separately at `floor-structure-residue`.

## The consequence the operator owns

One private domain has no remote. Its declaration is live but inert today;
**the moment a remote is added, that domain begins publishing automatically
— and its subject matter is one where publication is not a neutral act.**
Its frontmatter also declares a branch name the repo does not use, which
should be corrected before any remote exists. Both were surfaced to the
operator at the time of the ruling and left as theirs to route; neither is
named here, because the estate's private domains do not enter this
repository's history.

## Re-open condition

If a domain ever needs to hold work back from the estate — an embargo, a
sensitive drafting period — the answer is to set that repo's declaration to
`false` deliberately, not to bypass the mechanism. Silence still authorises
nothing.
