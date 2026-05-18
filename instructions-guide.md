# Instructions Guide

When you create a domain using this framework, you define it through a structured set of files. This guide explains how those files work together to create a complete, coherent domain specification.

## Domain Structure: Five Essential Components

Every domain requires these five components (in priority order):

### 1. Instructions File (`[domain].instructions.md`)
The philosophical and operational charter for your domain—where you explain *why* this system exists and *how* it should work within your specific context.

**Purpose:** Establish the paradigm, principles, and reasoning patterns that guide all work within the domain.

**Not a technical specification** (that's for `thing.skill.md`). Rather, it's your domain's constitution: the beliefs and paradigm shifts that justify why you're using this framework for this particular problem.

### 2. Application File (`[domain].application.md`)
A thing that defines what this domain *is* and *does* at the top level.

**Purpose:** Serve as the entry point that answers: "What problem does this application solve? What does it deliver? How does it work?"

**Structure:** A thing file (`type: application`) with metadata and narrative that explains:
- The problem it solves
- What it delivers (inputs → process → outputs)
- How it works (references to workflows/processes)
- Who uses it and why
- Related files and resources

**Why this matters:** Without an explicit application definition, you have guidance documents but no atomic "thing" that defines the domain itself. The application thing becomes the single point of reference for everything else.

### 3. Workflow/Process Thing(s) (`[name].md`)
One or more atomic things that define how the application executes.

**Purpose:** Orchestrate the steps, phases, or processes that the application uses to accomplish its work.

**Structure:** Things with `type: workflow` or `type: process` that describe:
- Phases or major steps
- What happens at each step
- Roles and responsibilities
- Expert checkpoints
- Handoff points and conditions for transition

**Why this matters:** Workflows are the operational heartbeat. They coordinate when LLMs work in different modes, when expert input is required, and how findings accumulate.

**Can you have multiple workflows?** Yes. Complex domains may have several processes or workflows. Each is an atomic thing that the application thing references.

### 4. Domain-Specific Read Prompt (`read.prompt.md`)
Guidance for how Claude (or other LLMs) should traverse, understand, and reason about things within this domain.

**Purpose:** Teach the LLM how to read and analyze things in your specific domain context.

**Content:** Domain-specific versions of:
- How to load and traverse things
- What thing types exist in this domain
- Reasoning patterns specific to this domain (especially if you've defined reasoning lenses)
- Examples of typical read-mode queries
- How to apply domain-specific analysis

**Where it lives:** `domains/[domain]/read.prompt.md`

**Based on:** Generic `read.prompt.md` in the root, tailored to your domain's instructions and workflow.

### 5. Domain-Specific Write Prompt (`write.prompt.md`)
Guidance for how Claude should create, update, and manage things within this domain.

**Purpose:** Teach the LLM how to make decisions and updates within your domain context.

**Content:** Domain-specific versions of:
- How to create new things with appropriate metadata
- How to update existing things based on user requests
- How to apply domain-specific reasoning (especially reasoning lenses)
- How to think about dependencies, impacts, and consequences
- When to ask for clarification vs. when to proceed
- Examples of typical write-mode tasks

**Where it lives:** `domains/[domain]/write.prompt.md`

**Based on:** Generic `write.prompt.md` in the root, tailored to your domain's instructions and workflow.

---

## How These Five Components Interact

```
instructions.md
  ↓ (defines philosophy and principles)
application.md (thing)
  ↓ (describes what it does)
workflow.md (thing) + [other process things]
  ↓ (orchestrates execution)
read.prompt.md + write.prompt.md
  ↓ (guide LLM behavior)
[instances: data things created by users]
```

**Example flow:**

1. **User reads instructions.md** → Understands why this domain exists and what drives decisions
2. **User reads application.md** → Understands what problem is being solved and what gets delivered
3. **User follows workflow.md** → Knows the steps, phases, and checkpoints
4. **User invokes read.prompt.md** → Claude reads and analyzes things according to domain rules
5. **User invokes write.prompt.md** → Claude creates/updates things according to domain rules
6. **Instances accumulate in git** → The domain's data grows and evolves

---

## Minimal Domain vs. Complex Domain

### Minimal Domain (1-2 workflows)
All five components are required, but they can be concise:
- **instructions.md** — 500-800 words explaining philosophy
- **application.md** — Describes what the domain does and delivers
- **workflow.md** — Single atomic workflow thing
- **read.prompt.md** — Tailored read guidance
- **write.prompt.md** — Tailored write guidance

**Example:** Life Manager, simple project tracking

### Complex Domain (multiple workflows/processes)
All five components scale to handle complexity:
- **instructions.md** — More detailed; may define multiple reasoning lenses
- **application.md** — Describes top-level application; references multiple workflows
- **[workflow-1].md, [workflow-2].md, [process-3].md** — Multiple orchestration things, each handling different aspects
- **read.prompt.md** — More detailed guidance for navigating complex domains
- **write.prompt.md** — More detailed guidance for creating different thing types

**Example:** Prototype-to-Production (with Phase 1-5 orchestration), Financial System (with transactions, budgets, forecasting workflows)

---

## Creating an Instructions File

## Instructions File Structure

Your domain's `[domain].instructions.md` should include:

### Philosophy
**Why does this domain exist? What problem are you solving?**

Explain the paradigm shift. What traditional approaches fail? How does this framework invert or improve on them? This section should feel like the opening argument—why should someone care?

Examples:
- Life Manager: "Traditional productivity apps separate concerns (input/UI → processing/logic → output/notifications). This system inverts the model entirely."
- Project Management: "Typical project tools force rigid categorization. This system lets structure emerge alongside work."
- Creative Writing: "Writing tools are either too structured (outlining) or too free-form (blank page). This system structures the *metadata* while keeping the narrative free."

### Core Principles
**What beliefs drive this system?**

List 4-7 core principles that guide how things work in your domain. These should be:
- Specific enough to inform decisions
- Universal enough to apply across use cases in the domain
- Grounded in the philosophy above

Examples from life-manager:
- "Atomic Units: Everything is a thing. No special cases."
- "Minimal Core, Emergent Detail: Start simple; let the schema grow with your needs."

### How It Works
**What is the flow? How do users interact with this system?**

Describe the loop: how does a user interact with the LLM? What happens? How does data flow? Keep it concrete but concise.

The life-manager example:
> "1. Your life exists as a collection of things in git
> 2. Each thing is a markdown file with YAML metadata and narrative
> 3. When you need help, you talk to Claude
> 4. Claude reads relevant things, reasons about what you're asking
> 5. Claude updates your files or creates insights..."

### What This System Is / What It Is Not
**Set clear expectations.**

Clarify boundaries. What is this system NOT trying to do? What integration points does it have with other tools? This prevents feature creep and confused users.

Examples:
- "Not a calendar (but it drives calendar entries)"
- "Not a database (but it acts like one through git)"
- "Not replacing human intuition (but augmenting decision-making)"

## Creating Your Application File

Once your instructions are written, create `[domain].application.md` as a thing file:

```yaml
---
id: application-[domain-name]
type: application
status: active
created: [ISO date]
schema_version: 2.0
linked_things:
  - id: [primary-workflow]
    relation: primary-process
  - id: [secondary-workflow] (if applicable)
    relation: related-process
---

# [Domain Name] Application

## What This Application Is
[One clear paragraph: the domain's purpose and scope]

## The Problem It Solves
[What's broken about traditional approaches? What does this framework invert?]

## What It Delivers
**Input:** [What goes in?]
**Process:** [What happens?]
**Output:** [What comes out?]

## How It Works
[References to workflow(s): "This application executes via [workflow-name], which orchestrates..."]

## Key Principles
[List 3-5 core principles guiding this application]

## Who Uses This Application
[Describe the roles and how they interact with the application]

## Related Files
[Links to instructions, workflows, prompts, thing.skill.md]
```

The application thing is your domain's entry point. Someone reading it should immediately understand what problem you're solving and what the system delivers.

## Before You Write

Ask yourself:

1. **Why am I using LLMs for this domain?** — What would be hard without LLM reasoning? What becomes possible with semantic understanding?

2. **What traditional approach am I replacing or inverting?** — What's broken about the status quo?

3. **What are my non-negotiables?** — What principles must hold true for this to work?

4. **Who is this for?** — If someone reads your instructions and disagrees with the philosophy, should they use this system? (If yes, your instructions aren't clear enough.)

## Defining Domain-Specific Reasoning Patterns

If your domain involves constraints, compliance, complex tradeoffs, or specialized reasoning (law, finance, healthcare, etc.), define **reasoning lenses** that guide how LLMs should think within your domain.

### What Are Reasoning Lenses?

Reasoning lenses are multiple perspectives through which an LLM should evaluate decisions or changes. Instead of encoding constraints as rules, you encode them as reasoning patterns.

**Example: A compliance-heavy domain might define:**

```markdown
## Reasoning Lenses

When working within this domain, reason through these three perspectives:

### Lens 1: Domain Logic
"What does this thing or change accomplish in the domain's terms?"
What is the business or operational outcome?

### Lens 2: Compliance Logic  
"Would this violate GDPR, data residency, audit requirements, 
or other regulatory constraints? How could it be mitigated?"

### Lens 3: Audit Logic
"Can we explain this decision to a regulator or auditor? 
Is the change traceable and justified?"

All three lenses must align before proceeding.
If they conflict, surface the conflict to the user for resolution.
```

**Why this works:**
- LLMs naturally reason through multiple perspectives
- Lenses encode constraints without being rigid rules
- Conflicts become explicit (domain says yes, compliance says no)
- The LLM learns to weigh tradeoffs rather than just following rules
- Decisions are explainable (we reasoned through all three lenses)

### Creating Your Lenses

In your `[domain].instructions.md`, add a "Reasoning Lenses" section that:

1. **Names each lens** — Give it a clear, domain-specific name
2. **Explains the lens** — What perspective does it represent?
3. **Lists what matters** — What signals or symptoms should trigger attention?
4. **Describes outcomes** — What should LLMs do if lenses conflict?

### Reinforcing Lenses Through Examples

Create `type: example` things that show how each lens applies:

```yaml
---
id: example-multi-lens-reasoning
type: example
pattern_type: reasoning
demonstrates: all-lenses-aligned
applies_to: [your-domain]
---

# Example: All Lenses Aligned

## The Decision
[Describe a decision made within the domain]

## Lens 1: Domain Logic ✓
[Shows why this makes sense for domain goals]

## Lens 2: Compliance Logic ✓  
[Shows how this respects constraints]

## Lens 3: Audit Logic ✓
[Shows how this is traceable/explainable]

Result: All lenses aligned → proceed confidently
```

Then create contrasting examples showing conflicts or failures.

## Examples

See `domains/life-manager/life-manager.instructions.md` for a complete, real-world example. Notice how it:
- Opens with the paradigm shift (why this matters)
- Explains the three decoupled layers
- Lists core principles with context
- Describes the interaction loop
- Sets boundaries on what the system is and isn't

## Length

Your instructions don't need to be long. Life-manager is ~800 words. That's enough to be complete without being overwhelming.

## Remember

Your instructions file is not enforcing rules; it's expressing *why* the rules exist. When someone (including a future version of you) reads your domain's instructions, they should understand not just what to do, but why it matters.

The best instructions files make you think: "Oh, I see. That's actually clever."
