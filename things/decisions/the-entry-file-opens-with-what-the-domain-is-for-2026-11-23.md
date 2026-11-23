---
id: the-entry-file-opens-with-what-the-domain-is-for-2026-11-23
type: decision
status: made
version: 1.0
created: 2026-11-23
session: 2026-11-18/23
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [entry-contract, agents-md, purpose, domain-agents, blueprint, template, done-condition]
informed_by:
  - id: conformance-roadmap
    commit: 8b633511dd7dfbf455efbdd1244eaf0decdbd9ff
  - id: agentic-workflow-across-tools-needs-a-mechanically-validated-record
    commit: 8b633511dd7dfbf455efbdd1244eaf0decdbd9ff
linked_things:
  - id: conformance-roadmap
    relation: informs
    notes: "Rules on the Phase 4 item the session proposed; the check and the template change are that phase's work"
  - id: agentic-workflow-across-tools-needs-a-mechanically-validated-record
    relation: implements
    notes: "The question an agent must start from has to be in the first thing it reads"
  - id: domain-specification-guide
    relation: informs
    notes: "The guide and the entry template place the statement of purpose below the launch mechanics today"
---

# The Entry File Opens With What The Domain Is For

## Context

The session proposed, in `conformance-roadmap` Phase 4, that the entry
contract open with the problem it solves, after it had answered the narrow
question three times in a session that started from the mechanism. The
operator weighed whether every domain has a problem to solve. The session's
view was that it need not: a standing domain has a purpose and a steady
state to keep, and a building domain has an outcome.

The entry template already has a section, *What This System Does*. It sits
below about twenty-five lines of launch mechanics, and it asks for "the
vision and primary capability", not for what the domain must achieve.

The operator, 2026-11-23, on stating the end result:

> "It's definitely one thing I've noticed with this technology is the
> desired end result needs to be stated plainly, unambiguous. It needs to be
> forefront in any prompt."

And on the entry file:

> "But that is like the first thing that will be loaded in. That should
> define at the first line or couple of lines what that thing is. And if it
> doesn't, then it's not quite in the right order, is it?"

> "And if the agents file that's there at the beginning is not telling that
> agent what it is and what it must achieve in the first things it reads,
> then yeah, there's a little issue. So I would agree on that one."

## Decision

1. **A domain's entry file says, in its first lines, what the domain is and
   what it must achieve.** It comes before the launch mechanics and before
   anything about how the system is built.
2. **It holds for every domain,** whatever name a harness gives the entry
   file.

## Agreed In General, On The Session's Proposal

The operator answered "I'm in agreement with you" to the session's form of
it:

- a domain that builds towards something states its outcome; a domain that
  keeps something running states the steady state it keeps;
- the statement is plain enough that an agent can tell whether a piece of
  work serves it. A vague purpose is worse than none, because any work reads
  as serving it.

## Not Decided Here

- The wording of the framework root's own statement, and of each domain's.
  Each is the operator's to state.
- The check. Under the roadmap's rules it is written first and approved
  before the template or any entry file is changed.
- Nothing is changed by this record: not `AGENTS.md`, not the template, not
  any domain.

## Consequences

The entry template's order changes when Phase 4 opens, and the domain
kernel's generated blocks follow the authored statement, not the other way
round. Every existing domain owes a statement in its first lines; the count
of those without one is the gauge's first reading.
