---
id: a-controls-guarantee-can-rest-on-a-coincidence-of-its-birth-environment
type: insight
status: active
version: 1.0
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: inferred
exposed: true
tags: [controls, assurance, session-gate, attestation, harness, anchors, integrity]
linked_things:
  - id: cowork-integrity-estate-sweep
    relation: challenges
    notes: "That sweep's Phase 10 chose the session gate as the deterministic fail-safe and described session-start as the command that 'emits the contract'. The code emitted the ritual and a POINTER to the contract. Both readings were true where the sweep was written, and only one was true where the gate was aimed."
  - id: hook-enforcement-has-three-anchors
    relation: extends
    notes: "The anchor taxonomy asks which surface makes a hook FIRE. This adds the second question, which the taxonomy does not force: given that it fired, what did it actually establish? A git-fs control can fire perfectly and still vouch for less than its prose claims."
  - id: existence-is-not-currency
    relation: complements
    notes: "Same family of over-reading a mechanical signal. There: a file exists, therefore it is current. Here: a command ran, therefore what its specification says it emits was emitted."
  - id: a-boundary-defect-is-visible-only-from-the-seat-that-did-not-build-it
    relation: supports
    notes: "The gap was invisible from the authoring harness for a structural reason, not a careless one: there the contract WAS in context at the moment the attestation was written — supplied by entry-file injection, a different mechanism entirely."
  - id: a-consumers-defect-report-names-the-surface-it-met-not-the-one-that-owns-it
    relation: complements
    notes: "Both are about tracing a claim to its true owner. There the consumer misattributes a defect upward; here the producer misattributes a guarantee to its own control when the environment was quietly supplying it."
---

# A control's guarantee can rest on a coincidence of its birth environment

## What was found

The session gate (v3.28.0) was the estate's answer to a real integrity
breach: a domain could be written to for weeks by an agent that never
loaded its contract, with the floor green throughout. The gate makes that
loud — `mdllm session-start` writes a per-clone attestation, and
`validate` blocks a commit without a fresh one. It was specified, built,
tested, live-tested, accepted by the operator, and documented with
unusual care about its own limits: it proves the contract was *emitted
into the session*, not that it was *heeded*.

Reading the emitter against that claim while building for a different
harness, the smaller gap appeared. `session-start` emits the ritual and
the status — version, velocity, open loops, triggers — and an
instruction: *"Load `kernel.md` (operative kernel)."* It does not emit
the contract. It emits a **pointer** to it.

In every harness the gate had ever run in, that distinction was
invisible, because the entry file had already arrived by injection before
the command ever ran. The contract was in context at attestation time —
supplied by the harness, not by the command the attestation names. The
gate's claim was therefore true, and true for a reason outside the gate.

Point the same gate at a harness with no entry-file discovery — where a
bootstrap clones the workspace *after* the session starts — and the
coincidence stops holding. The command still runs. The attestation is
still written. The commit is still permitted. And the contract was never
in the room. **The one failure the gate exists to prevent passes the
gate**, in precisely the environment the gate was built for.

## The general shape

A control establishes something. What it establishes is fixed by its
mechanism; what it *appears* to establish is fixed by its prose read in
the environment where the prose was written. When those environments are
the same — and while a control has only ever run in one place, they always
are — the difference cannot be felt. The control does not fail. It
succeeds, on a premise nobody wrote down, because nobody in that room had
to.

This is not the anchor question restated. Anchors ask *what makes it
fire*, and the gate's answer was correct and strong: git-fs, mechanical,
harness-agnostic. It fired exactly as designed. The second question — the
one the anchor taxonomy does not force you to ask — is: **given that it
fired, what did it establish?** A control can be perfectly anchored and
still vouch for a fact that some *other* mechanism was quietly supplying.

The tell is a specification sentence describing what a command does that
nobody has verified against what the command emits. Phase 10's own words
were *"the block names the one command, and that command emits the
contract."* The first clause was code. The second was belief — accurate
in situ, and load-bearing everywhere else.

## What was done

`session-start --contract` now emits the contract's **content** — the
operative kernel, the entry file, and a reading list derived from the
filesystem at emission time — ahead of orientation, and the attestation
records that it did so with a distinct token. The gate's claim now rests
on the gate in every harness, not on injection in some of them.

## Why this is on the porch

Domains declaring `session_gate: strict` rest an assurance argument on
this control, and this narrows what it proved for them before today: in
any session assembled by a bootstrap rather than opened on an existing
workspace, a fresh attestation evidenced that the ritual ran, not that
the contract was present. Nothing is retroactively invalid — the estate's
Cowork sessions ran under a bootstrap that printed a handoff and a
reading list, which is weaker than injection but is not nothing. It is a
correction to the *strength of the claim*, and a domain whose auditors
may one day ask "what did this control establish?" should carry the
honest answer rather than the flattering one.

## The standing check

When a control is carried into an environment it was not born in, do not
re-verify only that it *runs*. Re-derive what it **proves** there — by
reading its mechanism against its prose, in the new environment's terms.
A control that travels unchanged can still arrive meaning less than it
did at home.
