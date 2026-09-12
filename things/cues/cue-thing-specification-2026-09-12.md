---
id: cue-thing-specification-2026-09-12
type: cue
status: answered
version: 1.0
created: 2026-09-12
subject: thing-specification
raised_at: 1da4bca054812b23b30c829779be786afa58f853
raised_by: "agent — the cue-carrier build session of 2026-09-12, answering under the operator's delegated authority for this build (unattended-cue-carrier-2026-09-12: an agent may answer on a person's stated ruling)"
verdict: inflection
verdict_reason: "An eighth reserved type; every restated list — the kernel line, the reserved-types line, the bullet list, the status paragraph, validate.thing's table, both schema comments, the README template list, and the entry file's generated block — was updated in the same pass; the 32 declared inbound edges hold because none enumerates the reserved set."
tags: [cue, cue-carrier, change-reconciliation]
---

# Cue: `thing-specification` was modified — inflection?

## The Change
Commit 1da4bca added `cue` to the reserved set in all four places thing.md lists it, and `subject` to the registry's public-field list; version 2.23.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Inflection.** A reserved type is a rule every domain inherits. Walked: the 32 declared edges (`mdllm touchpoints thing-specification`) — extensions and guides that build on the atom, none of which enumerates the reserved set, so none is falsified; the restated lists the insight `framework-reserved-types-need-thing-md-as-single-source` warned about, each updated in 1da4bca; `mdllm domain-kernel .` regenerated the entry file's types block from the tool. Sealed with the `reconcile:` commit that carries this cue.

*Answered by the build session under the operator's delegated authority for
this work; the operator may overturn any verdict here by editing it — the
cue stays on the record either way.*
