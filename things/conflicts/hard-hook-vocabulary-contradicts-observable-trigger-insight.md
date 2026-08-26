---
id: hard-hook-vocabulary-contradicts-observable-trigger-insight
type: conflict
status: open
created: 2026-08-27
session: 2026-08-27
confidence: low
origin: inferred
parties:
  - hard-hooks-require-observable-agent-caused-triggers
  - orchestration-specification
linked_things:
  - id: hard-hooks-require-observable-agent-caused-triggers
    relation: contradicts
    notes: "Active at high confidence since 2026-05-28. Asserts hard status itself requires an agent-caused, agent-observable trigger, and names 'the two surviving hard hooks' as the complete set."
  - id: orchestration-specification
    relation: contradicts
    notes: "The current contract declares four hard hooks, two of them session-start (harness-session anchored), and states that hard/soft is config only and does not imply enforcement — a hard + interpretation hook is exactly as skippable as a soft one."
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "The reconciliation candidate: the anchor taxonomy redefined what 'hard' means after this insight was written, and the insight was never revised against it."
  - id: framework-retrospective-2026-08c
    relation: derived-from
    notes: "Surfaced by the 08c retrospective's first full-edge conflict scan."
---

# The Hard-Hook Vocabulary Contradicts the Observable-Trigger Insight

## The Clash

`hard-hooks-require-observable-agent-caused-triggers` (insight, active,
confidence high, 2026-05-28) asserts: *"For a hook to be genuinely 'hard'
(always fires, no exceptions, no configuration), it must be triggered by an
event the agent itself caused and can observe unambiguously"* — and names
`post-write:commit` and `pre-domain-scaffold:isolate` as *"the two surviving
hard hooks"*, explicitly ruling the session-boundary class out ("the session
is ending" is a state no agent can detect without an external signal).

The entry contract and `orchestration.md` today declare **four** hard hooks,
two of which — `session-start:version-check` and `session-start:estate-sync` —
are exactly the session-boundary class the insight excludes. And the anchor
model states the opposite definition of "hard": *hard/soft is config only —
always-on vs opt-in — and does **not** imply enforcement; a hard +
interpretation hook is exactly as skippable as a soft one.*

Both cannot be operative readings of "hard hook". A session reasoning from
the insight would refuse to classify `session-start:estate-sync` as hard; a
session reasoning from the contract already treats it as hard.

## How It Went Unnoticed

The insight predates the anchor taxonomy. When
`hook-enforcement-has-three-anchors` landed, "always fires" stopped being
what hard meant — enforcement moved to the anchor axis, and hard became
configuration. The insight was never revised against that inflection, and no
full-width conflict scan had run between then and the 08c retrospective. Its
`informs` edge into `orchestration-specification` is precisely the edge class
scan mode tests — the contradiction sat on a declared edge the whole time.

## Proposed Resolution — for the operator, not decided here

**Both-valid via the anchor distinction**, with a revision to the insight:

- What the insight got right survives intact as the *enforcement* claim: only
  an observable trigger can be **enforced** — agent-caused acts anchor at
  `git-fs`, harness events anchor at `harness-session` only where an adapter
  binds them, and nothing else fires mechanically. This is exactly the anchor
  model's own content; the insight anticipated it.
- What the insight got wrong is binding that requirement to the word "hard".
  Under the current vocabulary, hard is always-on config; the session-start
  hooks are legitimately hard *and* legitimately unenforced wherever no
  adapter binds them.
- Remedy: revise the insight (v1.1) to restate its principle in anchor
  vocabulary and mark it partially superseded by
  `hook-enforcement-has-three-anchors`, or dismiss it with the principle
  recorded as absorbed into the anchor taxonomy. Either ends the
  contradiction; the first preserves the historical reasoning.

Alternative recorded for completeness: reaffirm the insight and rename the
session-start hooks' classification — rejected as proposed direction because
the anchor vocabulary is load-bearing across the current contract and the
insight is the cheaper surface to move.

## Scope

The clash is vocabulary-level but operative: the insight's test ("can the
agent detect the trigger from its own actions? If no → bound prompt") would
misclassify two currently-declared hard hooks. No committed state disagrees
with the floor; nothing blocks on this. It is exactly the class of standing
contradiction the retrospective's scan exists to surface before it misleads
a future authoring session.
