---
id: transport-follows-corpus-holdability-not-distance
type: insight
status: active
version: 1.0
created: 2026-08-08
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "The operator parked HTTP deployment as deploy-when-felt, so no live plan consumes this yet. It is held active precisely so the next session that reaches for the HTTP transport meets the rule before the reach, rather than re-deriving it."
source: "session — operator's question at the close of the v3.29.0 porch build: whether always-on HTTP porches were the right shape for an estate whose domains are all cloned in one place"
session: 2026-08-08
tags: [membrane, transports, cross-domain, git, deploy-when-felt]
linked_things:
  - id: mcp-domain-server-design
    relation: informs
    notes: "The design doc holds the phasing and the built transports; this holds the rule for choosing between them."
  - id: an-environments-reachable-set-is-not-an-architecture
    relation: complements
    notes: "Harvested from the same session's two halves — that one says reachability is not yours to design, this one says distance was never the reason you needed the wire."
  - id: cross-domain-handoff-is-verified-external-input
    relation: extends
    notes: "The hand-off's semantics are transport-independent; that is exactly what makes the transport choice a pure infrastructure question."
---

# Transport Follows Corpus-Holdability, Not Distance

## The Insight

The porch's two transports differ in exactly one respect: **who owns the
server's process lifecycle.** Over stdio the consumer spawns the producer
on demand; over HTTP something must already be running. The face, the
membrane, the egress-stripping and the reference triple are identical
either way. So the choice reduces to a single question — *can the consumer
spawn the producer itself?* — and that question is answered by whether the
consumer holds the producer's corpus, not by how far apart they are.

**Distance is already solved, at a different anchor.** `estate-sync` pulls
and autopush publishes, so every machine converges on the same corpus; a
consumer on another machine clones the producer and spawns it locally over
stdio, and the read still crosses the face properly. Reaching a peer's
porch over the wire buys nothing that git has not already delivered — and
it buys it at the git-fs anchor, which is the sturdier one.

**What HTTP actually buys is non-holdability**, in two shapes:

- **Must not hold** — confidentiality. Where every domain is cloned
  alongside every other, the membrane's curation is a discipline the agent
  follows, not a boundary the filesystem enforces; the full corpus is right
  there on disk. A consumer reading over HTTP genuinely cannot see what is
  unexposed, because it is not present. For an estate that is all one
  owner's, the discipline suffices; for a regulated domain it may not.
- **Cannot hold** — ephemerality. A fresh VM where cloning fourteen repos
  to read two things is absurd, and pointing at a porch is cheap.

## The Correction Underneath It

The framing that makes always-on porches look attractive is *"like an
always-on agent — loaded and ready."* **A porch is not an agent.** It holds
no LLM, loads no contract, and reasons about nothing; it is a stateless
projection of `exposed: true` things out of a repo, which is why it
re-scans per request and why `run_domain_task` was built and reverted. Its
being up costs a process, not a primed mind. The resident-and-ready thing
is the deferred A2A layer, and conflating the two inflates the perceived
value of keeping porches running.

Corollary worth keeping separate: **serving a face and operating a domain
are orthogonal.** Co-locating twelve domains on one machine does not
weaken the guarantee that each is operated under its own contract — the
session gate is per-clone and enforces identically at one machine or
twelve.

## Standing Position

Stdio stays the default for co-located domains; the HTTP leg stays built,
tested and inert until a consumer genuinely cannot hold a producer's
corpus. The trap the rule exists to prevent is adopting HTTP as the
default because it exists, and paying daemon lifecycle costs for isolation
the estate does not yet need. Operator's word, 2026-08-08: parked,
**deploy when felt**.
