---
id: cue-git-workflow-cloud-pr-2026-09-24
type: cue
status: open
created: 2026-09-24
subject: git-workflow-specification
raised_at: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
raised_by: agent
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
