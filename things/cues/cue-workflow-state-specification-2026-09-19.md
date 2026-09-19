---
id: cue-workflow-state-specification-2026-09-19
type: cue
status: answered
version: 1.0
created: 2026-09-19
subject: workflow-state-specification
raised_at: ce1a1e6a13c700759c02f9082e2aef40cd934911
raised_by: "agent — the substrate-native-a2a build session of 2026-09-19, under framework-agent-closes-settled-cues-2026-09-13; raised in the commit that made the change"
verdict: inflection
verdict_reason: "A reserved type gained a field. `workflow-definition` is reserved precisely so cross-domain consumers can rely on its semantics, so what it may carry is a definition surface rather than an expression of one. Additive and optional, so the walk found nothing requiring an edit — recorded below rather than assumed."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
tags: [cue, substrate-native-a2a, change-reconciliation, workflow-state]
---

# Cue: `workflow-state-specification` was modified — inflection?

## The Change

Commit `ce1a1e6`, version 0.6 → 0.7: `stages[].actor` on `workflow-definition`
— an optional role name, or list of role names, declaring who *acts* at a
stage. Plus the floor's shape check and a Division-of-Labour row.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer

**Inflection**, though a mild one, and the honest reason is narrower than it
first looks.

It is not an inflection because it is *new* — additive optional fields usually
are not. It is one because `workflow-definition` is a **reserved** type, and
this spec says why that matters: the types are reserved "so cross-domain
consumers can rely on the semantics." What a reserved type may carry is
therefore a definition surface in its own right, not a way of expressing one.
A consumer reading another domain's definition may now encounter a field that
did not exist, and the spec is where it learns what it means.

The competing reading — *nothing reasons differently, so nothing changed* — is
true of every existing definition and false of the type. Both are recorded
here so a later reader can see the verdict was chosen rather than defaulted.

Worth stating plainly, because a field naming who acts invites the error: this
is **not gate authority**. The spec keeps execution responsibility and gate
authority as two declarations, and only the first became data. A stage may be
executed by an agent and authorised by a human. No frontmatter field moves the
boundary that keeps the irreversible act with the person.

## The Walk

Thirteen declared inbound edges, walked at `ce1a1e6`.

- **Nothing requires an edit.** The field is optional and the floor is silent
  in its absence, so every definition written before today — including both
  live ones in the estate — remains valid unchanged. That optionality is what
  makes this a promotion rather than a migration, and it is tested first in
  `test_workflow_actors.py` for exactly that reason.
- **`operating-model-specification` extends this spec** and composes over
  definitions; it declares no stage set of its own and is unaffected.
- **`coordination-claim-specification` complements it.** Checked for overlap
  and there is none: `held_by` says who *holds* a contended object now,
  `actor` says who *acts* at a stage by declaration. One is runtime and
  advisory, the other is static and definitional.
- **The condition the spec itself set was met, not waived.** The paragraph
  admitting modality fields required "at least two live modules needing
  automation to consume them"; two exist, and three shell watchers were
  already consuming the table from outside the definition.

## The Seal

Sealed with no downstream edits. Remaining exposure is the ordinary one — the
field reaches other domains on the next release through `domain-refresh.md`.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`. The operator may overturn
this verdict by editing it — the cue stays on the record either way.*
