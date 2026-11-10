---
id: the-session-gate-has-no-human-committer
type: insight
status: active
version: 1.0
created: 2026-11-10
session: 2026-11-10
source: agent
confidence: high
origin: inferred
linked_things:
  - id: validate-thing-specification
    relation: informs
    notes: "The session gate it specifies attests that the Tier-0 contract was emitted into an agent session; nothing in it names a human committing directly."
  - id: the-substrate-picks-no-surface-2026-11-10
    relation: informs
    notes: "Editing from a vault tool and committing in a human's name is the open question that decision leaves; this is its first blocker."
disposition: keep-active
disposition_reason: "Parked until an edit route from a vault tool is designed; it is that design's first blocker. Promote into validate.thing.md's session gate when an operator evidence class is ruled on."
settles_when: 2027-01-10
---

# The session gate has no human committer

## The Insight

The session gate (`validation.session_gate_findings`) asks one question of
every commit in a strict workspace: was a `session-start` attestation written
in this clone within 24 hours? Every commit is therefore treated as an
agent's. Ten of the operator's sixteen workspaces, including every one in the
regulated deployment, are strict.

A human who edits a record in a vault tool and commits it is stopped unless
an agent happened to run there today. The obvious workaround, having the tool
run `session-start` before committing, would make the attestation claim that
an agent received the contract when none did. That is the false record the
gate exists to prevent.

## Why It Matters

Any route that lets a human commit directly needs a declared, different
evidence class: the operator committing through a named tool, recorded as
such. Without it the choices are to keep every write agent-mediated, or to
weaken the gate. The investigation of 2026-11-06 found this before any code
was written. Recorded here so the next design starts from it rather than
rediscovering it.
