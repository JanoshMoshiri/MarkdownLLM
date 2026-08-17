---
id: a-missing-contract-degrades-to-semantic-drift-not-breakage
type: insight
status: active
version: 1.0
created: 2026-08-17
confidence: high
origin: stated
source: session — Phase 6 entry-surface finding; nine domains ran their whole history with no automatic entry file
session: 2026-08-17
tags: [deterministic-floor, orchestration, interpretation-anchor, harness, semantic-validation]
linked_things:
  - id: claude-entry-surface-unprovisioned-for-no-adapter-domains
    relation: derived-from
    notes: "The finding that produced it: Claude's automatic entry route was never provisioned, so nine domains never auto-loaded their entry file."
  - id: mis-keyed-links-pass-the-floor-silently
    relation: complements
    notes: "The same blind spot from the other end — that one is a specific mechanical gap; this one is what the floor's coverage implies about how a missing contract fails."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Why the gap survived so long: the surface that delivers the contract is the one nobody exercises deliberately."
---

# A Missing Contract Degrades To Semantic Drift, Not Breakage

## The Insight

When the Tier-0 contract never reaches the agent, nothing visibly breaks. The
deterministic floor keeps validating every commit — required fields, schema
conformance, reference integrity, the session gate — so the work that lands is
*structurally indistinguishable* from work done with the contract in hand. What
degrades is the part the floor was never able to see: decomposition calls, the
exposure question at creation, cascading after a write, applying the domain's
own lenses and boundary tests.

So the failure mode of a missing contract is drift that validates. Not an error,
not a refusal — an estate that looks healthy while its judgement quietly went
unguided.

## The Evidence

Nine of thirteen domains had no automatic entry surface for the harness they
were being worked in, for their entire history. They were not blind — the
adapter's SessionStart hook delivered state (version, velocity, open loops,
conflicts, triggers) the whole time — but the rulebook only arrived when an
agent chose to go and read it.

Across that whole period the estate validated clean: 203 framework things and
every domain corpus, zero errors. That is the insight in one line. The floor
held the structure; nothing held the judgement.

## Why It Matters

Two consequences, pulling in opposite directions.

**It bounds the damage.** A missing contract is not a catastrophe to be
excavated. The mechanical layer was doing its job throughout, so the recoverable
error class is narrow and soft. This is what the floor buys: it converts a whole
category of silent structural corruption into something that cannot get past a
commit.

**It also makes the damage unfalsifiable.** Because the drift validates, there
is no signal to search for and no clean "before" to compare against. A
retrospective audit has nothing mechanical to grep for; it would be reading
judgement calls one at a time, forever.

## How To Apply

When a contract-delivery gap is found:

- **Do not audit backwards.** There is no test that separates a thing written
  with the rules from one written without them. The effort is unbounded and its
  result unfalsifiable.
- **Let the first properly-contracted session be the audit.** It will apply the
  rules that were previously absent — asking the exposure question, cascading,
  running the write skill's boundary tests — and whatever was skipped surfaces
  as findings on live work instead of archaeology.
- **Expect the first such session in each domain to be noisier**, and read that
  noise as the report rather than as a new problem.
- **Do not read a clean floor as evidence the contract arrived.** It is evidence
  of the floor, and only that.
