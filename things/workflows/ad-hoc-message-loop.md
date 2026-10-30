---
id: ad-hoc-message-loop
type: workflow-definition
status: draft
version: 1.2
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
  - id: a2a-conversations-run-on-their-own-branch-2026-10-09
    relation: references
    notes: "2026-10-24: explicit conclusion is distinct from ordinary ticket closure; branch lifecycle support remains planned."
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

Nothing is owed at present, and no seat wakes. Either party explicitly
concludes the conversation in committed state; ordinary ticket closure and
the work item's completion do not substitute for that declaration. A later
request on an item whose ticket is ordinarily closed reopens the ticket to
its addressee through a declared edge.

The branch lifecycle that detects that declaration and terminates its
watch remains planned in `a2a-conversations-on-their-own-branch`. This
definition's stages and transitions are unchanged; `closed` continues to
mean nothing is owed now.

## Session wake

The watch observes committed peer state. Each seat arms it the way its
harness rises on an exit (`standing-watch.md` → Harness bindings): the
Claude seat as a background command through `/watch claude
ad-hoc-message-loop`, which Claude Code keeps running across turns and
re-invokes the agent on when it exits; the Codex seat bound to its session
as the operator directs. A blocking watch inside a bounded tool call dies
at the tool's timeout and is not a binding — the earlier wording here told
a seat without an adapter to do exactly that, and the record of 2026-10-11
shows what followed: turns "picked up through the operator's chat prompt,
not an automatic wake". A detached process alone is still not evidence that
a session will rise; the receipt is the harness re-invoking on the exit,
and the stall ring (`the-seat` Phase 7) is the backstop when it does not.
The existing request is read explicitly when first arming: a new watch
establishes a baseline and does not ring for an already-addressed ticket.
