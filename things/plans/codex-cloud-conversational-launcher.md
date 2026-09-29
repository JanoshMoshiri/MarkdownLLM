---
id: codex-cloud-conversational-launcher
type: plan
status: not-started
version: 1.0
created: 2026-09-27
priority: medium
tags: [adapters, codex-cloud, bootstrap, discovery, publication]
dependencies: [codex-cloud-workspace]
linked_things:
  - id: cowork-adapter
    relation: references
  - id: interface-specification
    relation: references
  - id: git-workflow-specification
    relation: references
---

# Codex Cloud conversational launcher — deferred

The operator's desired experience is Cowork-like: start a Cloud task and ask
"spin up QMS", then load other domains or ordinary code repositories as the
work requires, without configuring a separate setup script for every domain.
On 2026-09-27 the operator chose to **test the existing QMS-primary Cloud
adapter first**. This plan records the possible next shape, not approval to
implement it. Exposure: no; this is framework adapter planning state.

## Candidate shape, subject to live evidence

One reusable launcher repository and Codex Cloud environment would provide
the host's required primary checkout. A checked-in skill and bootstrap would
run in the *working agent* phase, fetch an immutable published substrate pin,
and assemble requested domain and code repositories as independent clones.
Further repositories could be admitted during the same task only through an
explicit, inspectable operation that checks identity, revision, credentials,
history, clean state and per-repository publication policy. Each domain would
receive its own floor and complete session contract; ordinary code would keep
its own hooks. This would move domain selection out of environment settings,
not eliminate the one-time Cloud environment or GitHub authorisation.

The host's native diff/PR route would belong to the launcher repository, **not
to a secondary QMS clone**. A QMS result would need a separate reviewed Git
publication path. Native shell Git access to private secondary repositories
must be proved in setup and agent phases independently; otherwise a scoped
credential available in the agent phase would be required. Agent-phase network
policy, cache lifetime and credential exposure are design inputs, not assumed
capabilities. No token belongs in a prompt, manifest or committed URL.

## Gate 0 — test the current shape before deciding

The prerequisite `codex-cloud-workspace` plan remains in progress. Run a real
QMS-primary Cloud task, including a fresh setup and cached maintenance, and
record what the host actually selects, what the model receives, which hooks
fire, and whether the primary result can use the Codex PR route. Probe remote
Git reads in the *working agent* for QMS and at least one additional private
domain or code repository; do not infer them from the connector or setup log.
Check secondary publication and local debt separately from the primary PR.
Record friction in changing the manifest, adding a repository, selecting the
working domain and handling credentials. Separate a fixture pass from a live
Cloud result. Complete this evidence review before changing this plan to
`in-progress` or starting launcher implementation.

## Gate 1 — choose the next intervention

After the live test, compare three options against the observed friction:

1. Keep QMS and other domains as primary-repository environments, with the
   existing conversational configuration skill doing the occasional settings
   work. This retains each primary repository's native PR path.
2. Use one launcher environment and task-time assembly, accepting a distinct
   publication mechanism for every secondary writable repository.
3. Use a hybrid: primary environments where native PRs matter, plus a
   launcher for read-heavy or cross-domain work.

Proceed only after recording which option actually solves the operator's
manual-setup problem without weakening domain isolation, Git authority,
contract delivery or publication visibility. A prompt-driven feel alone is
not sufficient evidence.

## If the launcher is chosen later

- [ ] Specify the one-time environment boundary: primary launcher checkout,
  agent internet policy, repository authorisation and credential lifetime.
- [ ] Design a task-time `load` operation for domains and code repositories,
  including repeated loads, changed pins, dirty clones and failure recovery.
- [ ] Keep the primary/secondary publication distinction explicit; test a
  secondary commit through to remote receipt or a visible publication debt.
- [ ] Run a live Cloud QMS task plus an additional domain/code repository and
  compare its operator steps, safety and reliability with the current adapter.

Until Gate 0 and the operator's Gate 1 choice are complete, these are
acceptance questions, not implementation tasks.
