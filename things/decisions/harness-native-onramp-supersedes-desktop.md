---
id: harness-native-onramp-supersedes-desktop
type: decision
status: made
version: 1.1
created: 2026-09-06
session: 2026-09-06
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [onramp, seat, desktop, explorer, accessibility, adapters, interface, direction]
informed_by:
  - id: markdownllm-desktop-is-primary-accessible-product
    commit: 5ebefa732c769be99e1e5d2c450c2ba0e5f29572
  - id: the-onramp-is-the-operators-own-sentence
    commit: 64774c5b0ece07063b0354957b5009aa2d34fd0d
linked_things:
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: supersedes
    notes: "Three days of telemetry, one onboarding session and one diagnosis reversed it. Its record stands; its requirements are retained as onramp input."
  - id: the-onramp-is-the-operators-own-sentence
    relation: derived-from
    notes: "The evidence: ninety minutes of already-mechanised steps that landed nothing, and the sentence the person reached for instead."
  - id: interface-specification
    relation: informs
    notes: "v1.7 replaces the first-party Desktop route with the harness-native onramp; the substrate stays route-agnostic and each route's claim is earned by its own evidence."
  - id: closed-loop-operating-state
    relation: references
    notes: "The seat is the human half of the loop that plan is closing. The three triggers that fired on 2026-09-06 all pointed at it."
  - id: the-record-answers-the-direction-question-first
    relation: references
    notes: "How the Context section was reached: telemetry, the prior record's own repair list and the fired triggers answered before judgement did."
  - id: a-surface-without-a-floor-accumulates-repairs-not-progress
    relation: references
    notes: "The diagnosis paragraph is this insight's first instance; the freeze is its first application."
---

# Decision: the harness-native onramp supersedes Desktop as the accessible product

## Context

Three days after `markdownllm-desktop-is-primary-accessible-product`, the record held three
things that decision had not anticipated.

**The telemetry.** Since 1 September every commit to `things/` was Explorer or Desktop —
installer, packaging, first-run persistence, settings retry, panel matching — while the
substrate's three highest-priority open plans went untouched for five to six weeks. The Desktop
record's own "current increment boundary" had become a list of repairs (0.1.2 → 0.1.3 → 0.1.6),
and nothing in the product had the substrate's property of converging: no floor validates a
window. The product repository's latest issued installer is 0.1.6; the operator's test of the
API-key route loads but does not send the request.

**The evidence.** Ninety minutes in a second onboarding session, bringing someone up to the
current framework version, landed none of the vocabulary; every step performed was already
mechanised; and the person's own phrasing of intent — the domain by its ordinary name, plus
"today" — was the interface the framework's premise already implies
(`the-onramp-is-the-operators-own-sentence`).

**The diagnosis.** A vendor-agnostic onramp is a harness. A harness competes on the one axis —
client engineering — where the framework has no floor and the vendors have the money, and it is
not the moat. The moat is what a domain accumulates when it is run: pinned decisions, resolved
conflicts, verified imports, insights that survived retrospectives — an artifact no vendor's
memory produces and no vendor owns. The accessible route has to make *that* legible to someone
who is not the framework's author, and it has to ride the harness the person already has.

## Decision

1. **MarkdownLLM Desktop is frozen** at its issued 0.1.6 installer, product repository
   `commit:e9b0032946fcabec721cf6b1c6ce48b7e2f386df`, as an Engineering Preview. No further
   increments accumulate into it. It is not deleted: its setup journey, domain discovery,
   registry identity and subscription-route requirements are recorded input to the onramp below.

2. **The accessible route is harness-native.** The operator's own intent sentence — the domain's
   ordinary name plus "today", or whatever phrasing the operator actually uses — in a harness
   they already use, backed by a skill or adapter that performs setup, sync, refresh, floor and
   session-start silently and renders orientation in the operator's language. Routes: Claude
   Code (evidenced entry route), Cowork (the bootstrap skill exists), Perplexity (a candidate
   the operator's colleague already uses; whether it can receive the entry contract and operate
   Git is a probe to run, not a claim to make). Each route's claim is earned by its own
   execution evidence, per `interface.md`.

3. **The operator seat is the one new surface.** What `session-start` and `orient` already
   compute — what changed, what stalled, what fired, what needs a ruling — rendered without the
   substrate's vocabulary: the domain's name, "today", "needs your ruling", evidence pinned.
   Not an application; a rendering in whatever route the operator is in.

4. **Explorer stays** at 0.4.3 as the optional read-only viewer, with exactly one further
   increment: a vocabulary pass replacing "substrate", "source files" and their kin with
   ordinary words, keeping "memories" and "skills", which land. Nothing else accumulates into it.

5. **The white-label increment stays parked** and **the hosted Explorer plan stays cancelled**.
   Neither reason changes — only the surface they would have served no longer exists.

6. **The substrate is unchanged.** Domains remain ordinary Markdown/Git repositories, operable
   through any compatible route; no application, plugin or skill becomes mandatory for a valid
   Domain.

## Consequences

- `interface.md` v1.7, `docs/operator-guide.md` v2.0 and `docs/first-hour.md` v1.7 are revised
  in the same commit: Desktop recorded as frozen, the onramp named, the route table updated.
  `first-hour.md` admits the persona it lacks.
- `operator-seat-and-harness-native-onramp` carries the forward work — Explorer vocabulary pass,
  the intent-sentence skill, the routes, the seat rendering, the persona.
- The Desktop repository's README should state the freeze. That is a write in the product
  repository and a separate act.
- The substrate backlog — `evidence-and-eval-backlog`, `response-depth-control`,
  `cohesiveness-sensors` — resumes its priority. The legible before/after that would convince a
  stranger is still the highest-leverage unbuilt thing.
- `markdownllm-desktop-is-primary-accessible-product` moves to `superseded`;
  `explorer-extraction-and-hosting` notes that its cancellation stands for a different reason.

## What is NOT decided

Which route the onramp lands in first; the Perplexity probe's outcome; any publication of a
plugin, skill or adapter (the human's act, every time); whether a paired mobile client ever
exists.

## Exposure

No. Product direction; nothing here changes what a valid Domain is.
