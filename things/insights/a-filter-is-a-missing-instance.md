---
id: a-filter-is-a-missing-instance
type: insight
status: active
version: 1.0
created: 2026-09-22
session: 2026-09-21/22
source: both
confidence: medium
origin: synthesised
tags: [decomposition, scope, workflow-run, standing-watch, diagnosis, discovery]
linked_things:
  - id: substrate-native-a2a
    relation: derived-from
    notes: "Phase 6: the fan-out defect that two independent diagnoses proposed to fix with a filter, and that a run already scoped."
  - id: run-membership-is-realisation-2026-09-22
    relation: derived-from
    notes: "The ruling that made the instance readable — once membership was one edge, the scope needed no filter at all."
  - id: workflow-run-is-the-decomposition-principle-applied-to-processes
    relation: extends
    notes: "That insight says a run is the instance of a definition. This one says: when a definition-scoped mechanism wants narrowing, the narrowing is usually that instance, unread."
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "Same test, applied to a filter proposal: does this name something that already exists, or add a body with new seams of its own?"
  - id: an-advisory-is-scoped-by-who-can-perform-its-remedy
    relation: extends
    notes: "That insight scopes an advisory by who can act on it. This one scopes a remedy by what the diagnoser can see — the second paragraph's case."
---

# A Filter Is a Missing Instance

## The Insight

When a mechanism scoped to a *definition* needs to narrow — "only this
stream", "only these ids", "only things matching X" — the instinct is a
filter: a regex, a `--match`, a tag. **Before adding one, look for the
instance the mechanism is failing to see.** A definition that is running in
two streams at once has two instances; if the mechanism cannot tell them apart,
the defect is that the instances are unnamed *to it*, not that a filter is
missing.

The case: a standing watch scoped to `two-agent-specification-loop` woke
every reviewer on every stream's turn. The domain agent proposed a
`SPEC_MATCH` regex in the shell watcher; the framework's first draft of the
fix was a `--match` flag on the floor command. Both were filters. Neither was
wrong about the symptom. But the two streams were already two
`workflow-run` things, each artefact already declared which run it realised,
and each run already carried its pin and its claim. The scope was `--run`.
Nothing was added to the artefacts; one edge was ruled as membership and the
mechanism was taught to read it.

The tell is that a filter encodes a rule *outside the substrate* — in a shell
invocation, a flag, a pattern somebody has to remember — which is the exact
class the loop's own history had already paid to eliminate. An instance
encodes the same rule as committed, validated, auditable state.

## Why a Correct Diagnosis Still Prescribed for the Wrong Artefact

The domain agent's diagnosis was right on every fact it stated: the shell
watcher's state lived under `$HOME`, per machine not per clone; `SPEC_DIRS`
could not separate streams sharing a directory. Its remedy was three
environment variables and a patch to that script. The collision it diagnosed
had already been fixed in the floor two days earlier, by construction —
invisible to it, because a domain agent sees its domain's tools and a
substrate fix reaches it only on refresh.

**A remedy is scoped by what the diagnoser can see.** A domain agent
prescribes for the artefact in front of it. When that artefact is one the
substrate has lifted, the prescription deepens the duplication the lift was
meant to end. The check before accepting such a remedy is cheap: has the
floor already moved under this script?

## Evidence and Confidence

One case, two independent diagnoses converging on a filter, one ruling that
dissolved it. Medium confidence: the pattern is clean but singular.
**Dismissal condition:** a definition-scoped mechanism genuinely needs a
narrowing that no existing instance carries — a filter that names nothing.
**Promotion:** into `thing.md`'s cohesion section, or `workflow-state.md`,
once a second mechanism reaches for a filter and finds a run instead.
