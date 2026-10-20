---
id: ad-hoc-message-loop
type: workflow-definition
status: draft
version: 1.0
created: 2026-10-21
exposed: false
stages:
  - id: claude
    to: [codex, closed]
    actor: claude
  - id: codex
    to: [claude, closed]
    actor: codex
  - id: closed
    to: [claude, codex]
linked_things:
  - id: standing-watch-specification
    relation: implements
---

# Framework Ad-Hoc Message Loop

The root's declared `ticket` type carries one conversation per work item.
Its `status` is the addressee, its body the current message, and its git
history the transcript. This definition instantiates the shipped
`templates/ad-hoc-message-loop.md.template` for the framework's Claude and
Codex seats. It is internal coordination, with no cross-domain exposure.

## Claude and Codex

Entry: the other seat commits a ticket addressed to this seat and makes the
commit visible through the Git ref that the receiving watch reads.

The named addressee is the only writer. It reads the request, acts within
the operator's authority, overwrites the body with one reply, and changes
the status to the other seat or `closed`. It commits the turn and verifies
that the receiving ref carries it before treating the handover as complete.
Each seat arms `mdllm watch` for this definition with its own role and
`--exit-on-wake`; a run-scoped conversation also passes `--run`.

The output is one recorded reply with its evidence. The gate confers no
authority: a ticket carries a request, never an approval or ruling. The
operator retains decisions and publication gates that already belong to
them. A local peer ref can carry a review without publishing a release.

## Closed

Nothing is owed at present, and no seat wakes. The work item's end is
recorded on the work item. A later request on the same item reopens the
ticket to its addressee through a declared edge.

## Session wake

The watch observes committed peer state. A session without a wake adapter
holds a blocking watch command in its active turn, acts when it exits 0,
and re-arms. A detached process alone is not evidence that a session will
rise. The existing request is read explicitly when first arming: a new
watch establishes a baseline and does not ring for an already-addressed
ticket.
