---
id: coordination-claim-specification
type: specification
status: draft
version: 0.1
created: 2026-06-16
linked_things:
  - id: thing-specification
    relation: extends
  - id: git-workflow-specification
    relation: complements
  - id: workflow-state-specification
    relation: complements
---

# Coordination Claim

## What This Specifies

An **advisory claim** is a small, visible "who holds this right now" marker that two operators (or two sessions) read and respect by convention. It is the framework's answer to *same-target contention* — the residue left after structural decomposition has separated everything that can be separated.

It is its own concept, not part of any one consumer. A `workflow-run` uses it (`workflow-state.md`), but so could a shared index or any contended singleton. Because the claim changes for its own reasons — coordination, not workflow semantics or thing structure — it earns its own spec rather than living inside `thing.md` or `workflow-state.md`. That is the decomposition principle of `thing.md` applied to this spec itself.

## What It Is Not

- **Not a lock.** Nothing enforces it. It is read and honoured by agents and operators; it cannot *prevent* a write. Its whole value is visibility.
- **Not a substitute for decomposition.** Reach for a claim only on a genuinely shared single object. If two operators contend because state is smeared across one singleton, the first fix is to *decompose* it so they touch different files (the run-state decomposition in `workflow-state.md` is the worked example). A claim covers the irreducible remainder.
- **Not git's job duplicated.** Git remains the system of record and the audit trail. The claim coordinates *before* the write; git records *after* it.

## The Convention

Two optional frontmatter fields on the contended thing:

```yaml
held_by: <operator-or-agent-id>   # who currently holds this thing
held_until: <ISO-8601 timestamp>  # optional lease; the claim is stale after this
```

- **`held_by` present, no `held_until`** — held until explicitly released (set back to empty/absent). Use when a session will clear its own claim.
- **`held_by` present, `held_until` in the future** — a lease: the holder expects to be done by then.
- **`held_until` in the past** — the claim is *advisory-expired*. The next operator may take over: set `held_by` to themselves and note the takeover in the body. An expired claim is a hint that the prior holder left without releasing, not a guarantee they are gone.
- **`held_by` absent** — unheld; proceed.

The discipline for an agent at session start: if a thing it intends to modify carries a live `held_by` that is not this session, **surface it and ask** rather than writing through it. If the claim is expired, surface the takeover before proceeding.

## Reading vs Writing the Claim

The claim itself is committed state, so taking or releasing it is an ordinary write under the `post-write:commit` hard hook. This is deliberate: the claim's history is in git like everything else, so "who held this and when" is auditable after the fact.

## Deploy When Felt

This convention is **reserved, not mandatory**. Deploy it on a thing only once that thing is actually contended — most things in most domains are touched by one writer and need no claim. `workflow-run` carries it because multi-operator, multi-session runs are its motivating case. A shared derived index is the next-most-likely adopter (a single-writer singleton that becomes a merge-conflict magnet the moment two sessions run), but it does not carry the fields until a domain feels the collision.

## Related, Not Yet Specified: Working-Tree Contention

The claim above coordinates writes to a *thing*. A coarser version of the same problem is contention over the *working tree itself* — two sessions editing the same checkout, where the truly shared mutable object is git's index, not any one thing. A thing-level `held_by` cannot fix that; it needs a repo-level or session-level signal (a committed "session active" marker, or simply respecting git's own lock files and never running mutating git commands while another writer is live). This is recorded here as the adjacent concern the same idea points at — to be specified if and when the multi-session workflow makes it a recurring cost rather than a one-off.
