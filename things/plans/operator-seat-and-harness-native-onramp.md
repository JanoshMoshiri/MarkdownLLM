---
id: operator-seat-and-harness-native-onramp
type: plan
status: not-started
version: 1.1
created: 2026-09-06
session: 2026-09-06
priority: high
tags: [onramp, seat, accessibility, adapters, explorer, vocabulary, cowork, claude-code, perplexity]
linked_things:
  - id: harness-native-onramp-supersedes-desktop
    relation: implements
    notes: "The decision this plan carries forward; ratified by the operator 2026-09-06."
  - id: the-onramp-is-the-operators-own-sentence
    relation: informs
    notes: "Governs every phase: the operator's sentence is the input; no substrate vocabulary reaches the seat; what the operator learns is the seat's four ideas."
  - id: an-attestation-bound-to-a-whole-tree-hash-is-terminal-by-construction
    relation: references
    notes: "Phase 1's Explorer increment reseals evidence last — the ordering that insight learned the hard way."
  - id: closed-loop-operating-state
    relation: references
    notes: "The seat is the loop's human half. The three triggers that fired 2026-09-06 all pointed at it; this plan is how someone other than the framework's author sits in it."
  - id: first-hour-guide
    relation: references
    notes: "Phase 5 gives it the persona it lacks."
  - id: a-surface-without-a-floor-accumulates-repairs-not-progress
    relation: informs
    notes: "Why nothing here is an application: every phase is a skill, a string change or a guide — forms the floor can read."
triggers:
  - type: time
    condition: "2026-09-20 reached"
    action: "If no phase has started, surface it plainly: the direction was ratified on felt evidence and the substrate backlog is also waiting. Ask which goes first — the onramp or the eval backlog — rather than letting both idle."
---

# Operator Seat and Harness-Native Onramp

Born 2026-09-06 from the reversal of the Desktop direction. The finding it
serves: a second onboarding session spent ninety minutes on steps that were
already mechanised, landed none of the substrate's vocabulary, and produced
the sentence that should have been the whole interaction — the domain by its
ordinary name, plus "today". This plan builds the translation from that
sentence to the machinery, and the rendering back.

Two constraints hold throughout. **Nothing here is an application** — every
phase is a skill, an adapter, a string change or a guide, and each lives in a
harness the operator already has. **Nothing here changes the substrate** —
domains stay ordinary Markdown/Git repositories, operable by any compatible
route, and no phase makes any of this mandatory for a valid Domain.

## Phases

### Phase 0 — Record the freeze (product repository)

- [ ] The Desktop repository's README states: Engineering Preview, frozen at
      the issued 0.1.6 installer (`commit:e9b0032946fcabec721cf6b1c6ce48b7e2f386df`);
      the API-key route loads but does not send; setup-journey, discovery,
      registry-identity and subscription-route requirements retained as input
      to this plan. A write in that repository — a separate act.

### Phase 1 — Explorer vocabulary pass (0.4.3 → 0.4.4)

- [ ] Inventory the user-facing strings: "substrate", "source files", and
      their kin — the words the operator reported as impenetrable.
- [ ] Replace with ordinary words. Working proposal: "MarkdownLLM" or "the
      framework" where "substrate" appears as a source name; "files", or the
      domain's own name, for "source files". Keep "memories" and "skills" —
      those land.
- [ ] UI strings only. No behaviour, boundary, API or packaging change.
- [ ] Reseal evidence last, in one pass, against the finished tree.

### Phase 2 — The intent sentence

- [ ] Collect the trigger phrasings from real operator language — "I want to
      work on X today", "let's do X", "what's going on with X" — gathered,
      not invented.
- [ ] The skill resolves X to a domain repository, runs the bootstrap
      silently (clone-or-sync, refresh against the current framework,
      floor, session-start), and hands over to the seat rendering.
- [ ] Refresh is part of the sentence, never a separate step. The manual
      substrate update was the ninety minutes.

### Phase 3 — Routes

- [ ] Claude Code: skill or plugin; execution evidence recorded.
- [ ] Cowork: extend the existing `spin-up-domain` bootstrap skill; evidence
      recorded.
- [ ] Perplexity: probe first — can it receive the entry contract and
      operate Git on the operator's behalf? Record the result either way.
      No route claim until the probe earns it.
- [ ] Each route's row in `interface.md` updated from its evidence, never
      ahead of it.

### Phase 4 — The seat rendering

- [ ] Orientation in the operator's words: the domain's name, "today",
      "since you were last here", "needs your ruling" with the evidence
      pinned. The four trigger buckets stay apart — fired, upcoming,
      horizon, your judgement — because collapsing them manufactures strain.
- [ ] Zero substrate vocabulary on the seat: no domain, session, harness,
      refresh, kernel, tier, estate, floor.
- [ ] Rulings flow back as commits under the existing conventions. The
      operator never sees Git; the record is still Git.

### Phase 5 — The persona

- [ ] `first-hour.md` gains the domain-expert newcomer: the four seat ideas,
      in ten minutes, before any tool — the agent writes things down in
      files you can read; nothing is real until it is committed and you can
      always see what changed; the agent proposes and some things only you
      can rule on; what you rule on accumulates.

## Gates — the human's, listed, never worked around

- Publication of any skill, plugin or adapter.
- Trust grants for any route that runs Git on the operator's behalf.
- The Perplexity route claim.

## Stop condition

Phases 1–5 done or gated. This plan does not resume Desktop work, the
white-label increment, or Explorer hosting; those are dispositioned by the
decision it implements and stay where they are.
