---
id: cue-git-workflow-specification-2026-09-19
type: cue
status: answered
version: 1.0
created: 2026-09-19
subject: git-workflow-specification
raised_at: ce1a1e6a13c700759c02f9082e2aef40cd934911
raised_by: "agent — the substrate-native-a2a build session of 2026-09-19, under framework-agent-closes-settled-cues-2026-09-13; raised in the commit that made the change"
verdict: inflection
verdict_reason: "A new rule in the `<!-- kernel -->` block, which every session in every domain loads at Tier 0. The nearest precedent (cue-git-workflow-specification-retro-2026-09-13) rests explicitly on `the kernel block is untouched`; that distinction does not hold here, so the precedent does not transfer. The walk found nothing downstream requiring an edit — recorded below rather than assumed."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
tags: [cue, substrate-native-a2a, change-reconciliation, kernel]
---

# Cue: `git-workflow-specification` was modified — inflection?

## The Change

Commit `ce1a1e6` adds a turn-taking paragraph to the kernel block: where two
instances take turns through the repository, a turn has not passed until its
new state is visible on the remote — confirm from the ref, never from the
local clone. A commit can succeed while its push is rejected, leaving the
committing side with every local indication that it handed over while the
other side sees nothing.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer

**Inflection.** Two reasons the alternative reading fails.

First, it lands in the **kernel block**, so it reaches every session in every
domain at Tier 0, not only readers of this spec. The 2026-09-13 cue on this
same subject was ruled not-inflection *because* the kernel block was untouched
— the distinction was load-bearing there and it does not hold here.

Second, calling it mere re-expression is tempting and wrong. The rule is a
corollary of *publication makes it real to the estate*, which the kernel has
carried all along — but a corollary that a live domain had to rediscover the
expensive way is not "already said". The engineering loop wrote it
independently on 2026-09-19 under its own heading and called it *"the rule
that has no analogue in the sibling and the one most likely to bite first."*
It had an analogue. Nobody could find it, because the substrate stated it
about publication and never about turn-taking. Drawing the consequence is a
new path, not a rephrasing of an old one.

## The Walk

Thirty-two declared inbound edges, walked at `ce1a1e6`.

- **Nothing requires an edit.** Every inbound edge reasons from the
  commit-boundary rules, the Machine Axis, or the publication rules. None of
  those moved: the paragraph adds a consequence at the publication boundary
  and changes no rule already stated.
- **The one surface that could have contradicted it agrees.** `estate-git-sync`
  extends this spec and already holds divergence-is-reported-never-resolved;
  the new paragraph ends on exactly that ("an instance that cannot publish its
  turn is blocked and says so; it never resolves the divergence to get
  unstuck"), so the two are consistent by construction.
- **Downstream domains receive it through the existing path** — the framework
  version and `domain-refresh.md`. No domain artifact needs touching today,
  and none is asked to.
- **It is mechanically pinned**, not only stated: a test builds a bare remote
  and two clones, commits a handover *without* pushing, and asserts the other
  side sees nothing.

## The Seal

Sealed with no downstream edits. The reconciliation obligation this inflection
creates is discharged by the walk above; what remains is ordinary propagation
on the next release, by the mechanism that already exists.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`. The operator may overturn
this verdict by editing it — the cue stays on the record either way.*
