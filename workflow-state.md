---
id: workflow-state-specification
type: specification
status: draft
version: 0.1
created: 2026-06-15
linked_things:
  - id: thing-specification
    relation: extends
  - id: interface-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: provenance-specification
    relation: complements
  - id: orchestration-specification
    relation: complements
  - id: workflow-run-is-the-decomposition-principle-applied-to-processes
    relation: informs
---

# Workflow Run-State

## What This Specifies

The framework models **knowledge state** richly — insights, conflicts, decisions, provenance, continuity, belief revision. It barely modelled **workflow state**. Workflows existed only as *definitions* (prose in a `*-workflow.skill.md`); there was no representation of a workflow *run* — the state of a multi-stage, multi-session process *instance* as it advances. Run-state had to be reconstructed by hand each session.

This spec adds run-state as two framework-reserved types:

- **`workflow-definition`** — the reusable process skeleton, with its stages expressed *as data* (not prose) and the transitions allowed between them.
- **`workflow-run`** — one live instance advancing through a definition: a cursor into the stage set, an advisory coordination claim, and a resume narrative.

It is a deliberately **narrow** primitive. Almost everything is inherited from `thing.md`; the proof it is genuine is how little it adds. If a draft of this grows large, it has smuggled in things that already exist.

## The Reframe: Decomposition Applied to Processes

Do not read this as a free-standing invention. It is the **decomposition principle of `thing.md` applied to processes.** A run is the *instance* of a workflow *definition* — exactly the `template-for` / `instance-of` pair the decomposition section already governs.

Today, a workflow definition living as prose inside a skill *violates* that principle: the skeleton and the (non-existent) instance are fused, so run-state smears across `continuity.md` and a pile of related things. Separating the definition (`template-for`) from the run (`instance-of`) finishes the decomposition. The cursor, claim, and resume point are what the *instance side* legitimately needs that no prior instance-thing did.

## Why It Is a Primitive (running the framework's own razor)

**Reducible — inherited, not reinvented:**

- It is a thing (`thing.md`): frontmatter + body, one identity, one reason to change.
- It accrues decisions with pinned inputs (`provenance.md`: `linked_things` → `type: decision`).
- It commits at stage transitions (`git-workflow.md` meaning boundaries).
- Its pointer to the definition is `instance-of` — an existing decomposition relation. **Do not add a redundant `definition:` field.**

**Irreducibly new — what earns primitive status:**

1. **The cursor — `current_stage`.** A pointer into an externally-defined, possibly-looping sequence. `status` models a thing's *own* lifecycle and cannot also carry "position N in a process defined elsewhere" without meaning two different things across domains (a cohesion violation). The two are distinct fields.
2. **The coordination claim — `held_by`.** A visible "who holds this instance right now," which nothing in the framework expressed because nothing had needed to.
3. **The per-instance resume point.** Continuity does this at *domain* granularity (`continuity.md`, one per domain); nothing did it per-run. It lives in the run's **body**, not a field.

## `workflow-definition` — The Structured Skeleton

A definition is a thing whose stages are **enumerable as data**, because `current_stage` can only mean something mechanically if the stage set is machine-readable. A real pipeline is rarely linear — iteration loops and backward passes make it a graph with cycles — so the definition expresses *allowed transitions*, not a sequence.

```yaml
---
id: <process>-definition
type: workflow-definition
status: stable          # reserved vocab: draft | evolving | stable | deprecated
created: <ISO-date>
stages:
  - id: intake
    to: [triage]
  - id: triage
    to: [research, intake]      # may loop back
  - id: research
    to: [draft]
  - id: draft
    to: [review]
  - id: review
    to: [draft, complete]       # rework loop, or finish
  - id: complete
    to: []                      # terminal
linked_things:
  - id: <a-filled-run-id>
    relation: template-for
---
```

- **`stages[].id`** — the stage set. The cheap mechanical fact: `run.current_stage` must be one of these.
- **`stages[].to`** — the directed edges out of each stage. This is the *semantic* fact: whether a given move was legal given the loops. An empty `to` marks a terminal stage.

The body holds what the stages *mean* — entry/exit criteria, what each stage produces, who acts. That prose is the definition's reason to change; the run never edits it.

## `workflow-run` — The Live Instance

```yaml
---
id: run-<instance>
type: workflow-run
status: active          # reserved vocab: active | paused | complete | abandoned
created: <ISO-date>
current_stage: research                 # MUST be a stage id in the definition
held_by: <operator-or-agent-id>         # advisory coordination claim; omit when unheld
linked_things:
  - id: <process>-definition
    relation: instance-of               # the definition pointer (inherited)
  - id: decision-<some-call>
    relation: informs                   # accrued decisions (provenance)
---

# Run: <human title>

## Where This Is
One paragraph: the current stage, why it is there, and what the last
transition was. This is the resume point — written so the next session
reads its state rather than reconstructing it.

## Next
The immediate next move and what it is blocked on, if anything.
```

Field discipline:

- **`current_stage`** — the cursor. Changing it *is* a stage transition; commit it at that boundary.
- **`held_by`** — advisory only. The agent reads and respects it; it is not a lock. Omit (or clear) when the instance is unheld.
- **`status`** — the run's *own* lifecycle, orthogonal to `current_stage`. A run can be `paused` mid-pipeline, or `complete` only once it reaches a terminal stage.

## What Not to Duplicate

- **No `stage_history` array.** The history of `current_stage` changes *is* the commit log — git is the event stream (`git-workflow.md`). Frontmatter holds the present cursor; git holds the path.
- **No `definition:` field.** The `instance-of` link already points at the definition.
- **No resume field.** The resume narrative is the body.

Keep that discipline and the run thing stays tiny — the tell that the primitive is clean.

## Division of Labour: Floor vs Agent

This follows the framework's standard split (`validate.thing.md`):

| Check | Owner | What |
|---|---|---|
| `current_stage` ∈ definition's stage set | **floor** (mechanical) | Cheap set-membership. Lands *when felt* — after the discipline has run on a real domain, not before. |
| Was this a *legal* transition? | **agent** (semantic, Layer 2) | Judges the move against `stages[].to` and the loop structure. |

Do **not** push cyclic-traversal legality into the floor. That is Layer 2, and forcing it mechanical is how this spec would bloat.

## Concurrency and Coordination

Run-state decomposition is most of the concurrency answer, not a separate workstream:

- **Different instances → different files.** Two operators working two different runs touch two different files; git merges them without thought. The old hazard — `continuity.md` as a single-writer singleton — is decomposed away.
- **Same-instance contention** is rare and small. The `held_by` advisory claim handles it: a committed, visible "who holds this," read and respected by convention. Not a distributed lock.
- **Git stays the system of record.** It is the audit trail. If a separate coordination layer is ever introduced for true runtime concurrency, treat it strictly as coordination and checkpoint its state back into the committed run-state thing at every meaning boundary. The durable schema is the contract — designed once, shared by a purely-local domain and any future coordinated deployment.

## Hand-off (interface.md)

A run produces deliverables, and those deliverables become another domain's inputs — a cross-domain hand-off. This is the case that argues for *reserving* the type rather than leaving it a domain pattern: any consumer that must read `current_stage` from outside the domain needs fixed semantics. (See the cross-domain hand-off gap in the review; the run is its first concrete use-case.)

## Maturity Path

Mature this on the ladder the framework already has — **reserve-but-draft**:

1. The originating idea is captured as `workflow-run-is-the-decomposition-principle-applied-to-processes` (`type: insight`).
2. The types are *reserved* (fixed status vocabularies, built into the floor) so cross-domain consumers can rely on the semantics — but this spec stays **`draft`**.
3. Exercise it on a real domain before promoting past draft. The filled instance in `examples/life-manager/` (a renovation process + a live run) is the first exercise.
4. Let the `mdllm` membership check (`current_stage` ∈ definition stages) land **when felt**, after the discipline has run — not ahead of need.

A type being reserved but undeployed in most domains is expected: it is exactly how the framework treats `conflict`, `retrospective`, and `index`. "Spec when foreseeable, deploy when felt" means primitives are *available*, not mandatory. A recipe domain never minting a workflow run is no different from its never minting a conflict.

## Relationship to Other Specifications

- **thing.md** — This extends the decomposition principle to processes; `workflow-definition`/`workflow-run` are a `template-for`/`instance-of` pair.
- **git-workflow.md** — Stage transition = checkpoint boundary; the commit log is the run's `stage_history`.
- **provenance.md** — A run's accrued decisions are `type: decision` things linked from it, inputs pinned to commits.
- **interface.md** — A run produces deliverables on hand-off; the cross-domain consumer reads `current_stage`.
- **orchestration.md** — A domain may bind reasoning to stage transitions (a domain hook point), but the run-state thing works without orchestration.
