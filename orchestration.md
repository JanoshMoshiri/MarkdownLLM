---
id: orchestration-specification
type: specification
status: draft
version: 1.0
created: 2026-05-20
linked_things:
  - id: thing-specification
    relation: extends
  - id: write-thing-specification
    relation: integrates-with
  - id: git-workflow-specification
    relation: integrates-with
  - id: interface-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Orchestration

## What This Specifies

This document defines the orchestration layer of the LLM-driven systems framework — how reasoning is triggered, what reasoning happens when it's triggered, and how the two are bound together.

The framework already has the building blocks:

- **Triggers** (in `thing.md`) define conditions on individual things
- **Skills** define comprehensive instruction sets for major operations
- **Workflows** (in domain skill files) define phase-by-phase sequences
- **Git commit points** (in `git-workflow.md`) define when state becomes real

What's missing is the connective tissue. This document introduces three primitives that make orchestration explicit, portable, and composable:

1. **Hook points** — Named moments in the lifecycle where reasoning can be attached
2. **Prompts** — Reusable reasoning templates smaller than skills, more structured than trigger actions
3. **Bindings** — Declarations that connect hook points to prompts

Together, these turn implicit "the LLM should probably check X after Y happens" into explicit, declarative orchestration that any LLM can follow without guessing.

## Why A Separate Specification

Triggers in `thing.md` answer: "When should this *thing* get attention?"

Orchestration answers: "When something happens *anywhere in the system*, what reasoning should fire?"

The distinction is scope. A trigger is scoped to one thing — it watches conditions relevant to that thing. Orchestration is scoped to the *flow* — it watches lifecycle events and binds reasoning to them. A trigger might say "when my dependency completes, surface me." A hook point says "whenever *any* thing completes, evaluate downstream cascades."

Keeping this separate preserves single responsibility:
- `thing.md` — what a thing is
- `orchestration.md` — how reasoning flows between things

## Hook Points

A hook point is a named moment in the system lifecycle where reasoning can be attached. It's not code. It doesn't execute anything. It's a **declared opportunity** — a moment where the agent checks: "Is there a prompt bound to this moment? If so, invoke it."

### Framework-Level Hook Points

These exist in every domain. They fire based on framework mechanics, not domain logic.

| Hook Point | When It Fires | Available Context |
|------------|---------------|-------------------|
| `session-start` | Agent loads and discovers AGENTS.md | All things, git log since last session |
| `session-end` | Before the session closes | All modified things, uncommitted changes |
| `pre-commit` | After changes are staged, before `git commit` | Staged files, changed thing metadata |
| `post-commit` | After a successful commit | Commit message, changed thing IDs, diffs |
| `post-write` | After any thing is modified (before commit) | Modified thing, its linked_things, triggers |
| `on-create` | After a new thing is created | New thing, potential parent/linked things |
| `on-status-change` | After a thing's status field changes | Thing, old status, new status, downstream |
| `on-error` | When validation or reasoning encounters a conflict | Error context, affected things |

### Domain-Level Hook Points

Domains define their own hook points for domain-specific lifecycle events. These are declared in the domain's workflow skill.

```yaml
hook_points:
  - name: phase-gate
    fires: "When expert confirms a phase is complete"
    context: [current-phase-report, next-phase-requirements]
    
  - name: expert-review-needed
    fires: "When LLM generates output requiring human judgment"
    context: [generated-output, uncertainties, embedded-questions]
    
  - name: approval-checkpoint
    fires: "When a go/no-go decision point is reached"
    context: [analysis-report, risk-summary, recommendations]
```

Domain hook points follow the same pattern as framework hook points — they're named moments with declared context. The difference is they emerge from domain workflows rather than framework mechanics.

### How Hook Points Relate To Triggers

Triggers and hook points are complementary, not redundant:

- **Triggers** are *conditions* attached to individual things. They're pull-based — evaluated when the agent scans.
- **Hook points** are *events* in the lifecycle. They're push-based — they fire when something happens.

A trigger says: "Check if I'm overdue." A hook point says: "Something just changed — what should happen next?"

In practice, the `session-start` hook is when triggers get evaluated. The `post-write` hook is when dependency triggers cascade. The hook point is the *mechanism* that makes trigger evaluation happen at the right time.

## Prompts

A prompt is a reusable reasoning template. It's smaller than a skill (which is a comprehensive instruction set) and more structured than a trigger action (which is a single word like `surface`).

Think of the hierarchy:

```
Skill (full instruction set, many paragraphs)
  └── Prompt (focused reasoning template, one specific task)
        └── Trigger Action (single-word signal: surface, escalate, cascade)
```

A skill says "here's how to do everything about reading things." A prompt says "here's how to evaluate whether downstream things should be unblocked after a completion." A trigger action says "unblock."

### Prompt Structure

Prompts live in the domain's skills directory or in the framework root. They follow the thing pattern — YAML frontmatter + markdown body — but with `type: prompt`.

```yaml
---
id: cascade-completion
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: completed-thing
    description: "The thing that was just completed"
  - name: downstream-things
    description: "Things that have dependency triggers watching the completed thing"
outputs:
  - name: status-changes
    description: "List of things whose status should change"
  - name: notifications
    description: "Things to surface to the user"
---

# Cascade Completion

## Reasoning Template

When a thing is completed, evaluate its downstream impact:

1. Load all things that list the completed thing in their `dependencies` or `triggers.watch`
2. For each downstream thing:
   - Are all its dependencies now satisfied? → Change status from `blocked` to `not-started`
   - Is this the last subtask of a parent? → Suggest parent completion
   - Does this unblock a critical-priority item? → Surface immediately
3. Report what changed and what needs user attention
```

### What Makes A Prompt Different From A Skill

| Aspect | Skill | Prompt |
|--------|-------|--------|
| **Scope** | Comprehensive — covers an entire operation mode | Focused — handles one specific reasoning task |
| **Size** | Many sections, full instructions | One reasoning template, typically under 50 lines |
| **Invocation** | Loaded at session start, always active | Invoked at specific hook points |
| **Composability** | Self-contained | Composable — multiple prompts can fire at one hook point |
| **Inputs/Outputs** | Implicit (reads whole domain) | Explicit (declared in frontmatter) |

### Framework Prompts

These are prompts that ship with the framework and apply to any domain:

- **cascade-completion** — Evaluate downstream impact when a thing completes
- **evaluate-triggers** — Scan active things for trigger conditions that are now true
- **validate-before-commit** — Run structural and referential validation on staged changes
- **session-orientation** — At session start, summarize what's changed since last session
- **surface-attention** — Determine which things need user attention and in what priority order
- **detect-conflicts** — Check if a proposed change conflicts with existing state (lens conflicts, dependency violations)

### Domain Prompts

Domains define their own prompts for domain-specific reasoning:

- **generate-phase-report** — (ProducFlow) Structure findings into a phase report with embedded questions
- **format-expert-questions** — (ProducFlow) Extract uncertainties and format them for expert review
- **apply-compliance-lenses** — (Compliance) Evaluate a change through all regulatory lenses
- **prioritize-by-energy** — (Life Manager) Factor energy cost into priority recommendations

## Bindings

A binding connects a hook point to one or more prompts. It's the declaration that says: "When this moment happens, invoke this reasoning."

### Binding Structure

Bindings are declared in a domain's AGENTS.md or workflow skill, or in the framework root for framework-level bindings.

```yaml
bindings:
  - hook: post-write
    when: "status changed to completed"
    invoke:
      - cascade-completion
      - evaluate-triggers
    
  - hook: pre-commit
    invoke:
      - validate-before-commit
    
  - hook: session-start
    invoke:
      - session-orientation
      - evaluate-triggers
      - surface-attention
    
  - hook: phase-gate
    when: "expert confirms phase complete"
    invoke:
      - validate-phase-completeness
      - generate-next-phase-report
```

### Binding Semantics

- **hook** — Which hook point this binding attaches to
- **when** (optional) — Additional condition that narrows when the binding fires. Without `when`, the binding fires every time the hook point fires.
- **invoke** — Ordered list of prompts to execute. Order matters — earlier prompts may produce context that later prompts consume.

### Binding Order and Composition

When multiple bindings attach to the same hook point, they execute in declaration order. This is intentional — it means you can reason about what happens at each lifecycle moment by reading the bindings top to bottom.

```yaml
# These all fire at session-start, in this order:
bindings:
  - hook: session-start
    invoke: [session-orientation]      # First: understand what changed
  - hook: session-start
    invoke: [evaluate-triggers]         # Second: check what's now true
  - hook: session-start
    invoke: [surface-attention]         # Third: decide what to tell the user
```

### Framework vs Domain Bindings

Framework-level bindings (defined in the root AGENTS.md or this spec) provide baseline orchestration that every domain inherits. Domain-level bindings (defined in the domain's AGENTS.md or workflow skill) add domain-specific orchestration on top.

Domain bindings can:
- **Add** new bindings to framework hook points
- **Add** bindings to domain-specific hook points
- **Override** framework bindings for a specific hook if the domain needs different behavior (declared explicitly with `override: true`)

They cannot remove framework hook points — only extend them.

## Putting It Together

Here's how the three primitives compose during a typical interaction:

```
User: "I finished the data collection task"

1. Agent parses intent → write operation (mark complete)

2. Agent modifies thing: data-collection.status = completed
   └── Hook fires: on-status-change
       └── Binding: on-status-change → [cascade-completion, evaluate-triggers]
           ├── cascade-completion runs:
           │   "data-collection completed → quarterly-review-prep is unblocked"
           └── evaluate-triggers runs:
               "quarterly-review-prep had dependency trigger watching data-collection"

3. Agent stages changes for commit
   └── Hook fires: pre-commit
       └── Binding: pre-commit → [validate-before-commit]
           └── validate-before-commit runs:
               "Structural check: ✓ | Referential check: ✓ | Semantic check: ✓"

4. Agent commits
   └── Hook fires: post-commit
       (no bindings currently → nothing fires)

5. Agent reports to user:
   "Marked data-collection complete. This unblocked quarterly-review-prep —
    moved it from blocked to not-started. It's now your highest priority item."
```

## How This Changes Existing Specs

This specification doesn't replace anything. It formalizes what was implicit:

- **thing.md** triggers remain unchanged — they're thing-scoped conditions. Orchestration provides the *mechanism* for when triggers get evaluated (the `session-start` and `post-write` hooks).
- **write.thing.md** "After you make changes, consider what else needs updating" becomes explicit: the `post-write` hook with `cascade-completion` and `evaluate-triggers` bound to it.
- **git-workflow.md** commit points become hook points. "After validation and fixes" becomes the `pre-commit` hook.
- **Workflow skills** phase gates become domain hook points with prompts bound to them.

## Design Principles

1. **Declarative, not imperative** — Hooks declare *when*, prompts declare *what*, bindings declare *which*. None of them contain code or execution logic.

2. **Composable** — Multiple prompts can bind to one hook. Prompts can be reused across hooks. Domains inherit and extend framework bindings.

3. **Transparent** — Reading the bindings tells you exactly what happens at each lifecycle moment. No hidden behavior, no implicit chains.

4. **LLM-native** — Prompts are natural language reasoning templates, not function signatures. The LLM reads them and reasons accordingly. There is no runtime, no interpreter, no execution engine — just structured attention direction.

5. **Progressive** — A domain can start with zero custom hooks and zero custom prompts (framework defaults handle everything). As the domain matures, it can add precision where needed.

6. **Idempotent** — Running the same prompt at the same hook with the same context produces the same reasoning. No side effects beyond the thing modifications the prompt recommends.

## When To Create A Prompt vs. Leave It Implicit

Not everything needs a prompt. The test:

- **Create a prompt** when you find yourself writing the same reasoning pattern in multiple workflows, or when a hook point needs specific structured thinking that an LLM might otherwise skip or handle inconsistently.
- **Leave it implicit** when the reasoning is obvious from context and the LLM will handle it naturally from the skill instructions alone.

The framework's default prompts (cascade-completion, evaluate-triggers, validate-before-commit, session-orientation, surface-attention) cover the mechanical orchestration that should happen consistently. Domain prompts cover the *domain-specific reasoning* that the LLM needs structured guidance to perform well.

## File Organization

```
framework-root/
├── orchestration.md              ← this file (the specification)
├── prompts/                      ← framework-level prompts
│   ├── cascade-completion.md
│   ├── evaluate-triggers.md
│   ├── validate-before-commit.md
│   ├── session-orientation.md
│   └── surface-attention.md
└── domains/
    └── [domain]/
        ├── skills/
        │   └── [domain]-workflow.skill.md  ← domain hook points + bindings declared here
        └── prompts/                        ← domain-level prompts
            ├── generate-phase-report.md
            └── format-expert-questions.md
```

Prompts are things. They live in directories, have frontmatter, have IDs, and can be linked to other things. They follow the same structural rules as everything else in the framework.
