---
id: cue-git-workflow-cloud-pr-2026-09-24
type: cue
status: answered
created: 2026-09-24
subject: git-workflow-specification
raised_at: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
raised_by: agent
verdict: inflection
verdict_reason: "Cloud clones now have explicit PR/manual outbound restraints and a primary inbound HEAD restraint. The owning declaration still grants publication. This reconciliation walks the shared policy and sync readers, hooks, guarded publish, kernel, setup and operator route; isolated Git tests seal the new branch."
linked_things:
  - id: codex-cloud-workspace
    relation: references
---

# Cue: clone-local PR publication restraint

The approved cloud-workspace plan defaults hosted work to PR publication.
The shared publication reader now recognises a clone-local restraint that
disables automatic sends without rewriting the domain's committed policy.
`git-workflow.md` describes that additional condition and its generated kernel
is regenerated. Literal `git.autopush: true` remains necessary; no local
configuration grants authority. Explicit one-shot publication keeps its
existing authority and branch checks.

The touched direct consumers are publication_policy, autopush, publish, doctor,
the generated kernel, cloud setup and operator instructions. Other clones are
unchanged when the local key is absent. The 36 declared dependants and two
literal references were enumerated with touchpoints; the release walk must
decide whether this narrowing is an inflection and seal the cue accordingly.
Exposure: no; the question belongs to this framework release.

**Inflection.** The multi-repository Cloud shape adds a manual restraint for
secondary clones and an observe-only inbound setting for the host-selected
primary. The shared publication policy and estate sync are updated, the kernel
is regenerated, the adapter and operator instructions are reconciled, and
real Git fixtures exercise the primary PR restraint, a manual secondary and
literal declared autopush. This reconciliation commit seals that walk.
