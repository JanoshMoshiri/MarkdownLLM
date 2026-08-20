---
id: workflow-state-specification
type: specification
status: evolving
version: 0.5
created: 2026-06-15
linked_things:
  - id: thing-specification
    relation: extends
  - id: coordination-claim-specification
    relation: complements
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

The framework models **knowledge state** richly — insights, conflicts, decisions, provenance, orientation, belief revision. It barely modelled **workflow state**. Workflows existed only as *definitions* (prose in a `*-workflow.skill.md`); there was no representation of a workflow *run* — the state of a multi-stage, multi-session process *instance* as it advances. Run-state had to be reconstructed by hand each session.

This spec adds run-state as two framework-reserved types:

- **`workflow-definition`** — the reusable process skeleton, with its stages expressed *as data* (not prose) and the transitions allowed between them.
- **`workflow-run`** — one live instance advancing through a definition: a cursor into the stage set, an advisory coordination claim, and a resume narrative.

It is a deliberately **narrow** primitive. Almost everything is inherited from `thing.md`; the proof it is genuine is how little it adds. If a draft of this grows large, it has smuggled in things that already exist.

## The Reframe: Decomposition Applied to Processes

Do not read this as a free-standing invention. It is the **decomposition principle of `thing.md` applied to processes.** A run is the *instance* of a workflow *definition* — exactly the `template-for` / `instance-of` pair the decomposition section already governs.

Today, a workflow definition living as prose inside a skill *violates* that principle: the skeleton and the (non-existent) instance are fused, so run-state smears across session notes and a pile of related things. Separating the definition from the run finishes the decomposition. The cursor, claim, and resume point are what the *instance side* legitimately needs that no prior instance-thing did.

**A note on the pointer.** Conceptually this is the `template-for`/`instance-of` relationship the decomposition section describes. *Mechanically*, the run carries the pointer as a singular structural field — `definition:` — not a `linked_things` relation. This follows the `parent` precedent: a singular, load-bearing pointer that the floor must resolve to exactly one target earns its own field rather than living as a relation the floor has to scan and filter. The decomposition principle still justifies the *separation* (definition and run are two things); the field is just how the instance names its template.

## Why It Is a Primitive (running the framework's own razor)

**Reducible — inherited, not reinvented:**

- It is a thing (`thing.md`): frontmatter + body, one identity, one reason to change.
- It accrues decisions with pinned inputs (`provenance.md`: `linked_things` → `type: decision`).
- It commits at stage transitions (`git-workflow.md` meaning boundaries).
- It names its definition with a structural `definition:` field, modelled on `parent` — the framework's existing pattern for a singular load-bearing pointer.

**Irreducibly new — what earns primitive status:**

1. **The cursor — `current_stage`.** A pointer into an externally-defined, possibly-looping sequence. `status` models a thing's *own* lifecycle and cannot also carry "position N in a process defined elsewhere" without meaning two different things across domains (a cohesion violation). The two are distinct fields.
2. **The per-instance resume point.** Session orientation does this at *domain* granularity (open-loop things, surfaced by the orient view); nothing did it per-run. It lives in the run's **body**, not a field.

(A third candidate — the **coordination claim** `held_by` — turned out *not* to be workflow-specific: it is a general advisory-claim convention that belongs to any contended singleton, so it has been decomposed out into its own micro-spec, `coordination-claim.md`. A `workflow-run` simply *uses* it.)

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
    to: [draft, done]           # rework loop, or finish
  - id: done
    to: []                      # terminal — see the convention below
---
```

The definition carries no link back to its runs: a definition has many runs, and each run points *up* to it via its `definition:` field, exactly as children point up to a `parent` rather than the parent enumerating children.

- **`stages[].id`** — the stage set. The cheap mechanical fact: `run.current_stage` must be one of these (floor-checked — see Division of Labour).
- **`stages[].to`** — the directed edges out of each stage. Whether an authored edge exists for an old→new cursor move is a mechanical fact; whether the work deserves that move remains semantic.
- **`to: []` means terminal — by definition.** An empty edge list is the explicit marker of a terminal stage, not "edges not written yet." A definition with a non-terminal stage whose edges are genuinely unfinished is simply a draft the author has not completed; there is no ambiguous third state. (If a future definition-completeness linter is built, this is the rule it enforces.)

The body holds what the stages *mean* — entry/exit criteria, what each stage produces, who acts. That prose is the definition's reason to change; the run never edits it.

## `workflow-run` — The Live Instance

```yaml
---
id: run-<instance>
type: workflow-run
status: active          # reserved vocab: active | paused | completed | abandoned
created: <ISO-date>
definition: <process>-definition        # the structural pointer to the definition
current_stage: research                 # MUST be a stage id in the definition
held_by: <operator-or-agent-id>         # advisory claim (coordination-claim.md); omit when unheld
linked_things:
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

- **`definition`** — the structural pointer to the `workflow-definition` this run instances. Singular and required; the floor resolves it to read the stage set.
- **`current_stage`** — the cursor. Changing it *is* a stage transition; commit it at that boundary.
- **`held_by`** — the advisory coordination claim defined in `coordination-claim.md`; not a lock. Omit (or clear) when the instance is unheld.
- **`status`** — the run's *own* lifecycle, orthogonal to `current_stage`: `active`, `paused`, `completed` (only once a terminal stage is reached), or `abandoned`.

**Blocked-ness lives on the work, not the cursor.** There is deliberately no `blocked` run-status. A run is a *pointer* into a process; it is `active` whenever it is live, even while the underlying work is stuck. Blockage is a property of the *work things* the run coordinates (a `task` blocked on a dependency, a deadline overdue) — read it there, not from the cursor. This keeps the run tiny and stops two things from claiming the same fact.

## What Not to Duplicate

- **No `stage_history` array.** The history of `current_stage` changes *is* the commit log — git is the event stream (`git-workflow.md`). Frontmatter holds the present cursor; git holds the path.
- **No reverse link from the definition.** Runs point up via `definition:`; the definition does not enumerate its runs.
- **No resume field.** The resume narrative is the body.

Keep that discipline and the run thing stays tiny — the tell that the primitive is clean.

## Division of Labour: Floor vs Agent

This follows the framework's standard split (`validate.thing.md`):

| Check | Owner | What |
|---|---|---|
| `definition` resolves, and `current_stage` ∈ its stage set | **floor** (mechanical) | Pure referential integrity — the same class as "`linked_things` targets must exist." Enforced now: `mdllm validate` errors on a missing `definition`, an unresolved one, a `definition` that is not a `workflow-definition`, or a `current_stage` the definition does not declare. |
| Does the prior definition declare this old→new edge? | **floor** (mechanical) | At pre-commit, compares the frozen index candidate with `HEAD`. The governing edge list comes from the prior committed definition, so the candidate cannot authorize its own move by rewriting the graph. A definition migration and cursor advance must be separate meaning-boundary commits. New runs have no prior transition and are allowed. |
| Should the run advance now? | **agent** (semantic, Layer 2) | Judges stage exit criteria, evidence, authorization, and whether the work deserves the mechanically-permitted move. |

Both membership and edge existence earn their place because each is a finite lookup over declared data, not judgement. A typo'd `current_stage` and an undeclared transition are the same honour-system hole at adjacent moments. The floor therefore compares the exact candidate tree to the prior commit and rejects an edge the prior definition does not declare. It does **not** infer entry/exit criteria, decide whether evidence is adequate, or advance a run; those remain Layer 2. (Cross-domain case: when the `definition` lives in another corpus the floor cannot see, membership remains unresolvable and is skipped rather than fabricated.)

## Concurrency and Coordination

Run-state decomposition is most of the concurrency answer, not a separate workstream:

- **Different instances → different files.** Two operators working two different runs touch two different files; git merges them without thought. The old hazard — a single-writer domain-level singleton (the retired `continuity.md` was one) — is decomposed away.
- **Same-instance contention** is rare and small. A `workflow-run` carries the advisory `held_by` claim defined in `coordination-claim.md` — a committed, visible "who holds this," read and respected by convention, not a distributed lock. The claim convention is general (it applies to any contended singleton), which is why it lives in its own spec rather than here; this spec only declares that a run *uses* it.
- **Git stays the system of record.** It is the audit trail. If a separate coordination layer is ever introduced for true runtime concurrency, treat it strictly as coordination and checkpoint its state back into the committed run-state thing at every meaning boundary. The durable schema is the contract — designed once, shared by a purely-local domain and any future coordinated deployment.

## Hand-off (interface.md)

A run produces deliverables, and those deliverables become another domain's inputs — a cross-domain hand-off. This is the case that argues for *reserving* the type rather than leaving it a domain pattern: any consumer that must read `current_stage` from outside the domain needs fixed semantics. (See the cross-domain hand-off gap in the review; the run is its first concrete use-case.)

## Maturity Path

Mature this on the framework's **reserve-but-draft** ladder — now one rung up, at **reserved-and-evolving**:

1. The originating idea is captured as `workflow-run-is-the-decomposition-principle-applied-to-processes` (`type: insight`).
2. The types are *reserved* (fixed status vocabularies, built into the floor) so cross-domain consumers can rely on the semantics — held since they were first reserved.
3. Exercised on a real domain. Beyond the `examples/life-manager/` demonstration pair (a renovation process + a live run), the primitive is now in active use in a live domain — which is what promotes this spec from `draft` to `evolving`. Remaining hardening (for example, a definition-completeness linter) lands as that use reveals the need.
4. The floor's referential and transition-shape checks are **enforced**: `definition` resolves; `current_stage` belongs to its stage set; and an existing run's candidate move follows an edge declared by the prior committed definition. What stays with the agent is transition *merit*: whether exit criteria and authorization justify using that edge.

A type being reserved but undeployed in most domains is expected: it is exactly how the framework treats `conflict`, `retrospective`, and `index`. "Spec when foreseeable, deploy when felt" means primitives are *available*, not mandatory. A recipe domain never minting a workflow run is no different from its never minting a conflict.

## Relationship to Other Specifications

- **thing.md** — This extends the decomposition principle to processes (definition and run are separate things); the run names its definition with a structural `definition:` field modelled on `parent`.
- **coordination-claim.md** — Defines the advisory `held_by`/`held_until` convention a run uses for same-instance contention; general, not workflow-specific.
- **git-workflow.md** — Stage transition = checkpoint boundary; the commit log is the run's `stage_history`.
- **provenance.md** — A run's accrued decisions are `type: decision` things linked from it, inputs pinned to commits.
- **interface.md** — A run produces deliverables on hand-off; the cross-domain consumer reads `current_stage`.
- **orchestration.md** — A domain may bind reasoning to stage transitions (a domain hook point), but the run-state thing works without orchestration.
