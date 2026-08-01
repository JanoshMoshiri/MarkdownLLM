---
id: response-depth-control
type: plan
status: not-started
version: 1.0
created: 2026-08-01
priority: high
tags: [interface, register, verbosity, depth, operator-experience, configuration]
linked_things:
  - id: assistant-register
    relation: extends
    notes: "assistant-register specifies the default depth and the rules that govern it. This plan adds the control surface: who selects depth, how, and the guarantee that depths are projections of one rendering rather than competing variants. Its Phase 0 findings are this plan's evidence base."
  - id: tiered-loading-is-tiered-reading-applied-to-specs
    relation: implements
    notes: "The third instance of one primitive. Tiered loading (L1/L2/L3, depth matched to query) -> tiered reading of specs -> tiered reporting of responses. Discovered, not invented: the spine is already named, this adds no new mechanism, only a new target and an operator-held selector."
  - id: interface-specification
    relation: extends
    notes: "The response is an output type interface.md never specified; depth is the dimension along which that output type varies. Both halves land in the same Response Register section."
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: informs
    notes: "Why the selector must be cheap and mechanical rather than a remembered discipline: a depth rule the agent must hold across every turn has unbounded scope and will decay exactly as the register did in its own test drive."
  - id: operative-rules-are-a-small-fraction-of-spec-prose
    relation: references
    notes: "Three depths, one selector, one projection rule — if the control surface cannot be stated in a few lines it has become a mode system, which is the design this plan's parent explicitly rejected."
---

# Response Depth Control — the operator holds the dial, and the depths are one rendering

## Why this is a separate plan

`assistant-register` establishes that the response is an unspecified output
type and fixes its **default**: report substance, withhold the derivation,
expand where a human decides. Its first test drive (2026-08-01) proved the
default necessary — a derivation dump the operator had to read twice, restated
into four buckets and immediately understood.

It also produced a requirement the parent plan does not carry: **the verbose
response is genuinely useful, and the operator wants to choose it.** Not
always, not never — on demand. That is a different concern from the parent's:
it serves the operator configuring their own experience rather than the spec
author fixing a default, it changes at a different rate, and it is reusable
against any output the framework produces, not only conversational turns.
Decomposition test met on all three counts (thing.md cohesion).

## The distinction that makes this compatible with the parent's rejection

`assistant-register` considered and **rejected** two registers — `operator`
vs `engineer`, declared per-domain. That rejection stands, and this plan does
not reopen it. The rejected design had two properties that made it wrong:

1. **The domain chose the audience.** A per-domain declaration decides for
   whoever sits down, and no audience wants the floor echoed at them.
2. **"Engineer mode" was the status quo wearing a job title** — the existing
   verbosity, relabelled and thereby protected from ever being fixed.

What is proposed here differs on both. **The operator chooses, not the
domain** — the same person wants different depth at different moments, which
is a dial in the reader's hand, not a mode in the domain's config. And the
deep setting is not the old verbosity preserved: it is the *retained
derivation*, which only exists because the default withholds it. Depth is
downstream of the register, not an escape hatch from it.

## The design that the drift objection actually permits

The parent plan rejected a `--brief` variant with a one-line reason: **two
renderings drift.** That objection is correct and fatal to any design with
two output paths. It is not fatal to this one, because depth here is a
**projection, not a variant**.

One computation. One assembled result, carrying its grounds. The default
projects the conclusion layer; deeper settings reveal layers that were
computed and retained anyway. There is no second rendering to drift *from* —
the deep view is the same object with less hidden, and the default view is
provably a subset of it.

This is the framework's own tiered-loading primitive pointed at output, and
the tiers map cleanly onto the ones already specified for input:

- **D1 — conclusion.** What changed, what needs you, what's next. The default.
- **D2 — conclusion plus grounds.** Each claim carries the mechanical fact
  behind it (which trigger fired, which `due_date`, which dependency). The
  natural answer to "show me why" about a whole response rather than one line.
- **D3 — full derivation.** The working: what was searched, what was rejected
  and why, the paths not taken. What the failed Phase 0 report was, except
  asked for.

Rule 5 of the register ("show me why must always work") is then not a special
case but the D1->D2 transition, available per-claim and per-turn.

## What is decided, and what is not

**Decided** (carried from the parent's evidence, not reopened here):

- Depth is operator-held, never domain-declared.
- Depths are projections of one rendering; no second code path, no second
  prose surface.
- D1 is the default everywhere, including for a newcomer's first session.
- Depth never suppresses a human-decides expansion. Rule 4 outranks the dial:
  a consequential or irreversible call is stated in full at every depth. The
  dial controls how much *working* is shown, never how much *consequence* is
  disclosed — the failure the parent's `consequence-is-recoverable-only-in-
  retrospect` link exists to prevent.

**Open — the figuring-out this plan exists to hold:**

1. **Where the selector lives.** Per-turn ask ("show me why", "full detail")
   is free and needs no configuration. A per-session setting and a persistent
   operator default both need a home. Candidate precedent in this repo:
   `.boundary-terms` — operator-local, real, never committed. A committed
   setting would put the domain back in charge of the audience, which is the
   rejected design returning by the back door.
2. **Does the agent honour a dial it cannot see?** A setting in a local file
   is mechanical for the *tool's* output but interpretation-anchored for the
   *agent's* prose — the same unbounded-scope decay that broke the register
   in its own drive. Likely the same answer as the parent's: name a format
   per depth so conformance is checkable, rather than a verbosity to hold.
3. **Do three depths survive contact, or is it two?** D2 may be the only one
   ever asked for, with D3 served by `git log` and the transcript. The
   parent's Option C (never repeat what the commit already records) may
   dissolve D3 entirely — the full derivation already has a durable home.
4. **Does the dial leak into tool output as well as prose?** `mdllm
   session-start --assistant` is D1; `--why` was sketched as D2. If the same
   selector governs both, the operator learns one control; if not, two.
5. **Escalation, not just selection.** When the agent judges a response
   genuinely needs D2 to be honest, may it volunteer the extra layer? Or does
   that reopen the drift the default exists to close?

## Phases

- [ ] **Phase 0 — Sit behind the parent's second drive.** No build. The
  working session `assistant-register` Phase 0 now calls for (a live domain,
  operator's real questions, every turn judged) is also this plan's evidence
  run: log each turn where the operator *wanted* more, what depth would have
  served, and whether they would have set a dial or just asked. Open question
  3 is answered by that log or not at all.
- [ ] **Phase 1 — Fix the projection contract.** Specify D1/D2/D3 as layers
  of one result in `interface.md` beside the register rules; state the
  subset guarantee and the rule-4 override in the kernel block. No selector
  yet — the contract must be stateable before the control is.
- [ ] **Phase 2 — The free selector.** Per-turn ask, no configuration: the
  register's retained derivation made reliably reachable in conversation.
  Cheapest possible test of whether a persistent setting is wanted at all.
- [ ] **Phase 3 — The persistent selector, if Phase 2 says it is needed.**
  Operator-local, uncommitted, `.boundary-terms`-shaped; tool output and
  agent prose reading the same value.
- [ ] **Phase 4 — Walk the dark region.** `mdllm coherence`, then the
  prose-only residue: operator-guide and first-hour describe the dial as
  part of the first session, not an advanced feature.

## The frame this plan serves

The operator's framing, adopted verbatim into the parent's findings and
restated here because it governs every open question above: **the
communication channel is the system's interface.** Not a report about the
system — the system, as far as the operator can see it. A capable engine
behind an unreadable screen is not a capable system; it is an unusable one.
Depth control is the part of that interface the operator holds in their own
hand.
