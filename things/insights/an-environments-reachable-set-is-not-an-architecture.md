---
id: an-environments-reachable-set-is-not-an-architecture
type: insight
status: active
version: 1.0
created: 2026-08-08
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "A standing rule about how to read a blocked probe, not work any one live thing consumes. It applies to every future cross-boundary capability the estate builds — the porch's authorization leg first, but not only that."
source: "session — the v3.29.0 porch probe: a Cowork VM consumer refused the CONNECT to an operator-run tunnel before any packet left the VM, then proposed a re-architecture toward what it could reach"
session: 2026-08-08
tags: [membrane, transports, harness, egress, probes, doctrine]
linked_things:
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: complements
    notes: "That insight names the harness constraining what the agent believes; this one names it constraining what the agent can reach. Same co-author, two different powers — and this one is invisible from the producer's seat entirely."
  - id: mcp-domain-server-design
    relation: informs
    notes: "The probe record in Build Status is this insight's evidence; the design doc holds the incident, this holds the rule."
  - id: portability-claims-need-execution-tests
    relation: extends
    notes: "Execution testing proves the build works where it runs; this adds that the consumer's environment is a second execution surface the producer cannot test from its own seat."
---

# An Environment's Reachable Set Is Not An Architecture

## The Insight

The v3.29.0 HTTP porch was proven across every leg its author controlled:
loopback bind, per-run token, JSON-RPC over the wire, tokenless requests
401'd *at the porch* through a public tunnel. Zero of six consumer probes
then ran, because the consuming harness — an Anthropic Cowork VM — routes
egress through a default-deny proxy whose allowlist (anthropic.com, package
registries, GitHub, private ranges) does not include arbitrary hosts. The
CONNECT was refused before a packet left the VM.

**The rule: a transport you control can be vetoed by an environment you
don't, and building the transport buys you no consumer.** Reachability is
*granted* by the consumer's environment, not *designed* by the producer.
For any cross-boundary capability, the reachability question therefore
belongs to the consumer's environment and should be answered there first —
a five-minute egress probe from the intended consumer would have preceded
the tunnel, not followed it. Nothing about the producer-side proof was
wasted; it simply proved a different claim than the one the probe was
asked to settle.

## The Sharper Half: The Reachable Set Proposes An Architecture

The consumer agent, having characterised the boundary honestly, observed
that **GitHub was on the allowlist** and proposed the natural consequence:
serve the domain face from a git repo the consumer can clone, which "would
be consumable from here today, where an HTTP porch is not" — and argued it
was the more robust anchor besides, being git-fs rather than
network-reachability.

That reasoning is locally excellent and would have traded away a decided
doctrine. The two-axis rule (`mcp-domain-server-design`) holds that
vertical/substrate reads go to git and horizontal/peer reads cross through
the face — because a git-direct peer read breaches the membrane *and*
re-introduces the id-space leak, needing the source's internal file path.
The proposal's whole warrant was that one proxy's allowlist happened to
include one host.

**So: when a constraint blocks you, the set of things still reachable will
propose an architecture. That proposal is an artefact of someone else's
policy, not a design principle, and it must be judged against doctrine
rather than adopted because it works.** The tell is the shape of the
argument — *"X is what we can reach, and conveniently X is also better"* —
where the second clause arrived after the first and would not have been
made without it. Note it, name why it is refused, and let it re-open only
as its own decision if the consumer class it serves becomes real.

## Standing Consequence

The porch's external-agent test is not blocked on the porch. It needs a
consumer environment chosen for its egress — and that is now a
prerequisite to state before the next probe is built, not a discovery to
make after.
