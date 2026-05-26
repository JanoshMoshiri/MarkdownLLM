---
id: orchestration-specification
type: specification
status: stable
version: 1.2
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

This document defines the orchestration pattern — an **opt-in** tool for domains that need structured reasoning flow beyond what the framework's narrative specs naturally provide.

Orchestration introduces three primitives:

1. **Hook points** — Named moments in the lifecycle where reasoning can be attached
2. **Prompts** — Reusable reasoning templates smaller than skills, more structured than trigger actions
3. **Bindings** — Declarations that connect hook points to prompts

## Hard Hooks vs Soft Hooks

All hooks described in this document — the bindings, prompts, and domain-level hook points — are **soft hooks**: opt-in, configured per domain, active only when a binding explicitly declares them. A domain that omits orchestration entirely continues to work fine; the narrative specs guide the LLM through reasoning without structural enforcement.

Some behaviors, however, are fundamental to the framework's integrity regardless of domain, configuration, or context. These are **hard hooks** — non-negotiable procedures that fire unconditionally. No binding declaration is needed. No domain configuration enables or disables them. They are part of the agent's standing operating contract with the framework.

### The Distinction

| | Soft Hook | Hard Hook |
|---|---|---|
| **Activation** | Requires a binding declaration | Always active — no configuration needed |
| **Skippable?** | Yes, if not bound | Never |
| **Defined by** | Domain AGENTS.md or workflow skill | Framework AGENTS.md |
| **Purpose** | Domain-specific structured reasoning | Framework integrity invariants |

### Framework-Level Hard Hooks

These two hard hooks are part of every agent's operating contract with the framework. They fire regardless of whether a domain uses orchestration.

#### `post-write:commit` — Commit Every Thing

**When it fires:** After any `.md` file containing YAML frontmatter is created or modified.

**What must happen:**
1. Identify the owning git repository — walk up the directory tree from the modified file until a `.git` directory is found
2. Stage the modified files: `git add` from that repo's root
3. Commit with a structured message following git-workflow.md conventions
4. Do not complete the response without this step

**Why it's hard:** Git is the framework's state machine. An uncommitted change is a change that doesn't exist yet — the "single source of truth" principle is violated by any thing that exists only in a working directory. This cannot be left to convention or memory.

**What failure looks like:** Thing files created in a session but never committed. State that exists in files but not in history. The session ends and the work is only partially real.

#### `pre-domain-scaffold:isolate` — Every Domain Gets Its Own Repo

**When it fires:** When creating a new domain — specifically, when generating a new `AGENTS.md` in a new directory under the framework.

**What must happen, in order:**
1. `git init` inside the new domain directory — before any domain files are committed anywhere
2. Add the domain's path to the framework's `.gitignore` — immediately, as part of the same operation
3. Commit the `.gitignore` change to the framework repo — so the framework never tracks the domain
4. Commit the domain files to the domain's own repo
5. Create a remote repository and push

**Why it's hard:** The nested repo isolation pattern is architectural. Domain git history must never appear in framework git history. If domain files are committed to the framework repo first, the separation is compromised — undoing it requires a soft reset, a `.gitignore` update, and re-committing to the right repo. Friction that is entirely avoidable if the isolation happens upfront.

**What failure looks like:** Domain AGENTS.md and skills appearing in `git log` of the framework repo. A remediation session required just to restore the correct structure.

### Declaring Domain-Level Hard Hooks

Domains can declare their own hard hooks in their AGENTS.md using a `hard_hooks` block. A domain hard hook is a behavior that must fire for that domain's integrity, regardless of context.

```yaml
hard_hooks:
  - hook: session-end
    action: "Update WORKLOG.md and commit before the session closes"
  - hook: post-write
    action: "After updating any return thing, check if its companion deadline thing needs updating"
```

Domain hard hooks are scoped to that domain only. They do not propagate to the framework. They are the domain's standing operating procedures — behaviors the domain agent must always perform, with no exceptions.

---

## When To Use Orchestration

Orchestration is **not mandatory**. The framework's narrative specs (write.thing.md, thing.md triggers, validate.thing.md) already guide LLM reasoning effectively through prose. LLMs naturally calibrate effort from narrative instruction — they reason about whether something is relevant, how deep to go, and whether the context warrants it.

**Use orchestration when:**
- Your domain has strict phase-gated workflows (e.g., compliance, regulated environments)
- Consistency matters more than flexibility (multi-person teams, audit requirements)
- Specific high-consequence moments must never be skipped (pre-deployment checks, approval gates)
- You need repeatable, documented reasoning that fires identically every time

**Don't use orchestration when:**
- Narrative prose in skills and specs is sufficient for the LLM to reason correctly
- Your domain is exploratory or evolving quickly
- Rigidity would slow down natural reasoning and iteration
- The LLM already handles the reasoning well without explicit structure

The difference: narrative prose is a *nudge* — the LLM decides how much attention to pay. A bound prompt is a *procedure* — the LLM executes it completely. Choose accordingly.

## The Primitives

### Why A Separate Specification

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

- **generate-phase-report** — (Business Flow) Structure findings into a phase report with embedded questions
- **format-expert-questions** — (Business Flow) Extract uncertainties and format them for expert review
- **apply-compliance-lenses** — (Compliance) Evaluate a change through all regulatory lenses
- **prioritize-by-energy** — (Life Manager) Factor energy cost into priority recommendations

## Bindings

A binding connects a hook point to one or more prompts. It's the declaration that says: "When this moment happens, invoke this reasoning."

### Binding Structure

Bindings are declared in a domain's AGENTS.md or workflow skill.

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

### Binding Scope

Bindings are domain-level declarations. Each domain defines its own bindings based on what structured reasoning it needs. There are no framework-level bindings that domains inherit — orchestration is entirely opt-in.

A domain's bindings live in its workflow skill or AGENTS.md. They can attach to:
- **Framework hook points** (session-start, post-write, pre-commit, etc.) — these moments exist in every domain
- **Domain hook points** — custom moments defined by the domain's workflow

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

## Relationship To Existing Specs

Orchestration doesn't replace the narrative specs — it's an additional tool for domains that need more structure:

- **thing.md** triggers remain the primary attention mechanism. They work through natural LLM reasoning without orchestration. Domains that adopt orchestration can use the `post-write` hook to make trigger evaluation more systematic.
- **write.thing.md** already guides the LLM to consider downstream effects through prose. Orchestration is for domains where "consider" isn't reliable enough and "always execute this checklist" is needed.
- **git-workflow.md** commit points are natural moments where orchestration hooks can attach — but they work fine without explicit hooks, driven by the narrative spec alone.
- **Workflow skills** (like a domain's phase gates) are the primary use case for domain-level orchestration — structured workflows where phase transitions need explicit, repeatable reasoning.

## Design Principles

1. **Declarative, not imperative** — Hooks declare *when*, prompts declare *what*, bindings declare *which*. None of them contain code or execution logic.

2. **Composable** — Multiple prompts can bind to one hook. Prompts can be reused across hooks. Domains define their own bindings independently.

3. **Transparent** — Reading the bindings tells you exactly what happens at each lifecycle moment. No hidden behavior, no implicit chains.

4. **LLM-native** — Prompts are natural language reasoning templates, not function signatures. The LLM reads them and reasons accordingly. There is no runtime, no interpreter, no execution engine — just structured attention direction.

5. **Opt-in** — A domain starts with zero orchestration (narrative specs handle everything). As the domain matures and identifies moments where structured reasoning adds value, it can adopt hooks, prompts, and bindings incrementally.

6. **Idempotent** — Running the same prompt at the same hook with the same context produces the same reasoning. No side effects beyond the thing modifications the prompt recommends.

## When To Create A Prompt vs. Leave It Implicit

Not everything needs a prompt. Over-specifying reasoning constrains the LLM rather than enabling it. The framework's strength is that LLMs reason well from narrative prose — prompts should sharpen that reasoning, not replace it.

### Create A Prompt When

- The same reasoning pattern repeats across multiple workflows or domains
- A hook point needs structured thinking that an LLM might skip or handle inconsistently
- The reasoning involves a specific sequence of checks that must happen in order (like validation or cascading)
- Getting it wrong has consequences (missed cascades, broken references, unsurfaced conflicts)

### Leave It Implicit When

- The reasoning is obvious from context and the skill instructions are sufficient
- The LLM naturally handles it without structured guidance
- The prompt would just restate what's already in a skill file
- The scenario is rare or domain-specific enough that a general template wouldn't fit

### Red Flags: Signs Of Over-Specification

Watch for these — they indicate a prompt is becoming too prescriptive:

- **The reasoning template is longer than the narrative prose it replaced.** A prompt should be tighter than a skill paragraph, not more verbose.
- **The template contains conditional branching logic** ("if X but not Y unless Z"). This is programming in prose. The LLM can reason about conditions — it doesn't need them scripted.
- **The prompt duplicates logic from another prompt or skill.** If two prompts cover overlapping territory, merge or eliminate one.
- **The prompt specifies exact output text rather than output structure.** Guide the shape of reasoning, not the words.
- **Domain-level prompts exceed ~10 for a single domain.** This suggests the domain is encoding procedures rather than reasoning guidance. Consider whether some prompts should be absorbed into the workflow skill's narrative.

### The Litmus Test

Read the prompt's reasoning template and ask: "Is this a checklist a competent person would use, or a procedure manual an intern would follow?" If it reads like a procedure manual, it's over-specified. Simplify until it reads like a checklist.

### Quantity Guidance

The framework provides 6 prompt templates (in `templates/prompts/`) as starting points. A domain that adopts orchestration should typically use 2–5 prompts for its unique reasoning patterns. If a domain has more than 10 prompts, that's a signal to review whether some should be consolidated or left implicit.

## File Organization

```
framework-root/
├── orchestration.md              ← this file (the specification — defines the pattern)
├── templates/
│   └── prompts/                  ← starting-point prompt templates
│       ├── cascade-completion.md
│       ├── evaluate-triggers.md
│       ├── validate-before-commit.md
│       ├── session-orientation.md
│       ├── surface-attention.md
│       └── detect-conflicts.md
└── domains/
    └── [domain]/
        ├── skills/
        │   └── [domain]-workflow.skill.md  ← domain hook points + bindings declared here
        └── prompts/                        ← domain-level prompts (copied/adapted from templates or created fresh)
            ├── generate-phase-report.md
            └── format-expert-questions.md
```

Prompts are things. They live in the domain's `prompts/` directory, have frontmatter, have IDs, and can be linked to other things. They follow the same structural rules as everything else in the framework. The framework's `templates/prompts/` provides starting points — domains copy and adapt what they need rather than inheriting a mandatory set.
