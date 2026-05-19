---
id: thing-specification
type: specification
status: evolving
version: 2.1
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: read-thing-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: validate-thing-skill
    relation: enforced-by
  - id: git-workflow-specification
    relation: complements
  - id: interface-specification
    relation: complements
---

# Thing Definition

## What Is A Thing?

A thing is the atomic unit of this framework. Everything is a thing. A project is a thing. A task within a project is a thing. A subtask is a thing. A dependency is a thing. A concept, an article, a recipe, a design pattern—all things. Even a simple action is a thing.

What kind of things? That depends on your domain. This is the specification that applies to any domain.

A thing is:
- **Self-contained:** It has all the information needed to understand what it is
- **Linkable:** It can reference other things and be referenced by them
- **Mutable:** It can change status, gain detail, gain context, split into sub-things
- **Reasonably scoped:** Large enough to be meaningful, small enough to be actionable

## Structure Of A Thing

Every thing file follows this pattern:

```
---
[YAML METADATA]
---

# [Title]

[Markdown narrative body]
```

### YAML Metadata

The metadata is the structural layer. It provides the minimal information Claude needs to parse and understand relationships.

#### Required Core Fields

These fields must be present in every thing to do:

**id** (string, unique)
- A stable identifier for this thing
- Format: lowercase, hyphens, no spaces (e.g., `brush-teeth`, `qbr-2026-q2`, `fix-bike-derailleur`)
- Used for linking and referencing
- Never changes once set

**type** (string)
- What kind of thing this is
- Values are domain-specific. Examples: `thing` (generic catch-all), `task`, `project`, `subtask`, `goal`, `milestone`, `item`, `concept`, `resource`, or any other type that emerges as you use the system
- Helps Claude understand scope and context

**status** (string)
- Current state of this thing
- Values: `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`
- Updated by Claude as work progresses

**created** (ISO 8601 date)
- When this thing was created
- Format: `2026-05-17` or `2026-05-17T14:30:00Z`
- Never changes

#### Recommended Fields

These aren't required, but they unlock richer reasoning from Claude:

**due_date** (ISO 8601 date)
- When this thing should be done
- Helps Claude prioritize and understand urgency
- Can be in future or past (if overdue)

**priority** (string)
- Relative importance
- Values: `low`, `medium`, `high`, `critical`
- Can change as circumstances change

**tags** (array of strings)
- Categorical labels relevant to your domain
- Examples depend on domain: `urgent`, `research`, `reviewed`, `published`, `draft`, `[category]`
- Helps Claude search and filter contextually
- Can be as specific or general as needed

**parent** (string - id reference)
- If this is a subtask, the id of the parent thing
- Establishes hierarchy
- Can be null or omitted if no parent

**linked_things** (array of objects)
- Relationships to other things
- Structure: `{ id: "thing-id", relation: "subtask|dependency|blocks|related|similar", notes: "optional context" }`
- Allows Claude to traverse the graph of your life

**dependencies** (array of strings - ids)
- List of things that must be done before this
- Helps Claude understand sequencing
- Can be empty

**blocks** (array of strings - ids)
- List of things this blocks from starting
- Inverse of dependencies
- Helps Claude understand impact

#### Emergent Fields

These fields will emerge over time as your system evolves:

Examples that might emerge:
- `energy_cost`: `low|medium|high` - how much mental/physical energy this requires
- `time_estimate`: minutes or hours needed
- `assigned_to`: who is responsible (if shared system)
- `progress`: percentage, subtask counts, checkboxes
- `resources`: list of tools, documents, or people needed
- `decision_point`: if blocked on a decision, what decision
- `review_date`: when to revisit and reassess
- `season`: quarterly/monthly/weekly context
- `context_switch_cost`: how disruptive is it to start/stop this

Don't predefined these. Let them emerge as you use the system and Claude suggests them.

#### Triggers (Optional)

Triggers are declarative conditions attached to a thing that signal when the agent should pay attention to it. They are not code. They don't execute anything. They are **attention signals** — metadata that tells the LLM "when you're next active, check whether this condition is true, and if so, direct your reasoning here."

This is a fundamental distinction from traditional event systems. In a traditional system, a trigger causes code to run. In this framework, a trigger causes the LLM to *think about something*. The LLM decides what to do. The trigger just says "look here."

**Why this matters:**

The framework is pull-based — a human initiates a session, and the agent reasons. Without triggers, the agent only thinks about what the human asks about. With triggers, the agent can proactively surface things that need attention based on conditions the human defined in advance.

**Structure:**

```yaml
triggers:
  - type: time|dependency|threshold|relationship
    condition: [what to check]
    action: [what to do if true]
```

**Trigger Types:**

**Time-based** — Conditions that depend on time passing.

```yaml
triggers:
  - type: time
    condition: due_date_passed
    action: surface
  - type: time
    condition: review_date_reached
    action: re_evaluate
  - type: time
    condition: stale
    threshold: 30d
    action: surface
```

- `due_date_passed` — The thing's `due_date` is in the past and status is not `completed` or `cancelled`
- `review_date_reached` — The thing's `review_date` has arrived
- `stale` — The thing hasn't been modified in longer than `threshold`

**Dependency-based** — Conditions that fire when something this thing depends on changes.

```yaml
triggers:
  - type: dependency
    watch: [prerequisite-task-id, approval-decision-id]
    on: status_changed_to
    value: completed
    action: unblock
```

- `watch` — The IDs of things being observed
- `on` — What change to watch for (status_changed_to, priority_changed, any_modification)
- `value` — The specific value that satisfies the condition (if applicable)
- When a watched thing meets the condition, this thing is surfaced for re-evaluation

**Threshold-based** — Conditions that fire when accumulated state crosses a boundary.

```yaml
triggers:
  - type: threshold
    condition: subtasks_complete
    threshold: 100%
    action: suggest_completion
  - type: threshold
    condition: blocked_duration
    threshold: 7d
    action: escalate
  - type: threshold
    condition: in_progress_count
    threshold: 5
    action: warn_overload
```

- `subtasks_complete` — All linked things with relation `subtask` have status `completed`
- `blocked_duration` — The thing has been in `blocked` status for longer than `threshold`
- `in_progress_count` — More than `threshold` things are simultaneously `in-progress` (system-level, not per-thing)

**Relationship-based** — Conditions that fire when a connected thing changes in any way.

```yaml
triggers:
  - type: relationship
    watch: parent-project-id
    on: priority_changed
    action: re_evaluate
  - type: relationship
    watch: related-goal-id
    on: status_changed_to
    value: cancelled
    action: surface
```

- More general than dependency triggers — watches any relationship, not just blocking dependencies
- Useful for propagating priority changes, detecting when a parent goal shifts, or noticing when related context changes

**Actions:**

Actions are also declarative. They tell the agent what kind of response is appropriate — not how to implement it.

| Action | Meaning |
|--------|---------|
| `surface` | Bring to the user's attention at next opportunity. "This needs your eyes." |
| `re_evaluate` | Load this thing at full context and reason about whether it's still correct (status, priority, scope). |
| `suggest_completion` | Conditions indicate this thing may be done. Propose marking it complete. |
| `unblock` | A dependency has been satisfied. Update status from `blocked` to the appropriate active state. |
| `escalate` | Something has been stuck too long or a risk condition exists. Flag prominently. |
| `warn_overload` | System-level signal that too many things are in-progress simultaneously. |
| `cascade` | Check all things downstream of this one (things that depend on it, things it blocks). |
| `notify` | Push through output route (calendar update, notification, reminder). |

**When Triggers Are Evaluated:**

Triggers are checked at three moments:

1. **Session start** — When the agent loads (AGENTS.md discovered, skills loaded), it scans active things for trigger conditions. Any that are met get surfaced immediately: "3 things need attention since your last session." This is the primary evaluation point.

2. **After every write** — When the agent modifies a thing (changes status, completes it, updates priority), it checks: "Do any other things have triggers watching this one?" If so, it evaluates those triggers and cascades. This is how completing a task automatically surfaces things it was blocking.

3. **Scheduled invocation** — An external mechanism (cron job, OS scheduler, GitHub Actions, a recurring calendar event) periodically invokes the agent with a "check triggers" intent. The agent scans all triggers, evaluates conditions, and either acts or reports back through the output route.

**Trigger Evaluation Is Idempotent:**

A trigger that's true stays true until the condition changes. If a thing is overdue, it's overdue every session. The agent doesn't need special "already fired" state — it reasons about *how long* the condition has been true and responds proportionally:

- First session overdue: "This is now past due."
- Fifth session overdue: "This has been overdue for a week. Should we reprioritise or cancel?"

Git history provides the temporal context. The agent can see when it last mentioned this trigger by reviewing recent commits or worklog entries. No additional state machinery is needed.

**Example: A Thing With Triggers**

```yaml
---
id: quarterly-review-preparation
type: task
status: not-started
priority: high
created: 2026-05-01
due_date: 2026-06-15
dependencies: [data-collection, stakeholder-feedback]
triggers:
  - type: dependency
    watch: [data-collection, stakeholder-feedback]
    on: status_changed_to
    value: completed
    action: unblock
  - type: time
    condition: due_date_passed
    action: escalate
  - type: threshold
    condition: blocked_duration
    threshold: 14d
    action: surface
---
```

This thing will:
- Automatically surface as unblocked when both its dependencies complete
- Escalate if its due date passes without completion
- Surface for attention if it's been blocked for more than 2 weeks (suggesting the dependencies themselves might need help)

**Philosophy:**

Triggers encode your *future attention* as metadata. Instead of remembering to check on things, you declare the conditions under which they become relevant. The agent then handles the cognitive load of monitoring — across dozens or hundreds of things — and surfaces only what matters at any given moment.

This inverts the typical productivity pattern. Instead of maintaining a mental model of everything that's in flight, you define triggers once and trust the agent to tell you when conditions change. Your attention is directed by conditions, not by memory.

### Markdown Body

Everything after the YAML frontmatter is narrative. This is where the semantic richness lives—the context, the reasoning, the details that make this thing meaningful.

The body should include:
- **What This Is:** A clear explanation of what the thing actually is
- **Why It Matters:** Context about why you're doing this thing
- **Current Situation:** Where you are now with it
- **Next Steps:** What comes next, what's in progress
- **Blockers:** What's preventing progress, if anything
- **Notes:** Context, learnings, considerations

The structure of the body is flexible. Use headers, lists, prose, whatever makes sense. Claude will understand it.

## How To Create A Thing

1. **Choose an ID:** Make it descriptive but short. `chocolate-chip-cookies`, not `comprehensive-chocolate-chip-cookie-baking-instructions`. You'll reference these often.

2. **Choose a Type:** What is this in your domain? Start simple; it can change.

3. **Set Initial Metadata:** At minimum: id, type, status, created. Add other fields if they're relevant now.

4. **Write the Body:** Explain what this is and why it matters. Keep it brief unless detail is needed.

5. **Link If Needed:** If this relates to other things or has sub-things, add those references now or later as they become clear.

Example minimal thing (recipe domain):
```
---
id: chocolate-chip-cookies
type: recipe
status: not-started
created: 2026-05-17
tags:
  - dessert
  - baking
---

# Chocolate Chip Cookies

Classic chocolate chip cookies. Good for gatherings or just a snack.
```

Example richer thing (content/research domain):
```
---
id: ai-reasoning-article
type: article
status: in-progress
priority: high
due_date: 2026-06-01
created: 2026-05-17
tags:
  - ai
  - machine-learning
  - published
linked_things:
  - id: research-survey
    relation: dependency
  - id: code-examples
    relation: subtask
  - id: ai-limitations-article
    relation: related
---

# How LLMs Reason: A Technical Deep Dive

## What This Is
A comprehensive article exploring the mechanisms of LLM reasoning, from transformer architecture to in-context learning to multi-step inference.

## Why It Matters
This helps readers understand what's actually happening inside LLMs, moving beyond marketing claims to technical reality.

## Current Status
Research phase complete. Writing first draft now. Waiting on code examples to be finalized.

## Next Steps
- [ ] Complete research synthesis
- [ ] Write technical sections
- [ ] Add code examples and visualizations
- [ ] Get peer feedback

## Blockers
Waiting for collaborator to finish the code examples section.
```

## Evolution And Growth

Start simple. As you work with a thing, it will naturally gain detail. Claude will suggest new metadata fields. The body will expand with learnings and context. This is expected and good.

A thing might start as:
```
id: learn-rust
type: goal
status: not-started
```

And evolve to include energy cost estimates, resource lists, progress metrics, decision points, and rich narrative context as you actually work on it.

The system grows with your needs, not ahead of them.

## Special Type: Example

For building pattern libraries and teaching LLMs domain-specific reasoning, create things with `type: example`:

```yaml
---
id: example-[pattern-name]
type: example
pattern_type: [what kind of pattern]
demonstrates: [compliance/good-practice/anti-pattern/edge-case]
applies_to: [which domains or thing-types this pattern applies to]
created: 2026-05-18
---

# [Pattern Name]

## The Pattern
[Clear description of what this example demonstrates]

## Why It Matters
[The reasoning: why is this pattern important to follow?]

## Structure/Code Example
[Show the correct structure or code pattern]

## Anti-Patterns (What NOT to Do)
[Common mistakes or violations of this pattern]

## How to Adapt
[How to apply this pattern to your specific domain]
```

**When to use Example things:**

Example things are a teaching mechanism for LLMs. They serve as inductive learning—showing rather than telling how patterns should work.

**Why examples work better than rules:**

LLMs excel at **verifiable reasoning**—tasks where patterns can be checked against clear criteria—and struggle with non-verifiable tasks. Compliance patterns are inherently verifiable (data classified or not, access logged or not, etc.). A single rule ("classify personal data") is abstract; positive + negative examples create verifiability:

- **Positive example**: Shows what good classification looks like (verifiable)
- **Negative example**: Shows violations and consequences (verifiable contrast)
- **Together**: LLM learns the pattern boundary, not just a rule

This mirrors how humans learn—contrast creates clarity that rules alone don't provide.

**Common use cases:**
- Compliance patterns (GDPR, audit trails, data handling) — *especially useful for verifiable decisions*
- Architectural patterns (how to structure complex domains)
- Naming conventions (what field names mean what)
- Edge cases (showing how to handle ambiguous situations)
- Anti-patterns (showing what breaks and why) — *pairs negative examples with remediation*

**Examples are discoverable:** When an LLM encounters a domain with example things, it naturally learns from them. You don't need to explicitly reference them; they guide reasoning through pattern recognition.

**Scaling through examples:** As your system grows, your library of example things becomes organizational knowledge—versioned, auditable, and automatically referenced by any LLM working within your domains.

## Multi-Level Context Windows

A powerful feature of this framework is that the same thing file can be used at different levels of detail depending on context. An LLM (or human reasoning) can interact with a thing at multiple granularities:

### Level 1: Metadata Only
Load just the YAML frontmatter without the narrative body:
```yaml
id: project-alpha
type: project
status: in-progress
priority: high
due_date: 2026-06-15
tags: [work, launch]
linked_things:
  - id: feature-auth
    relation: subtask
  - id: budget-review
    relation: dependency
```

**Use case:** Quick overview across many things. "What's active? What's blocked? What has dependencies?" Scan 50-100 things to understand the landscape.

### Level 2: Metadata + Relationships
Include the YAML plus the linked_things, dependencies, and blocks fields, but omit the narrative body:
```yaml
id: project-alpha
type: project
status: in-progress
priority: high
linked_things: [...]
dependencies: [budget-review]
blocks: [deployment-plan]
```

**Use case:** Traversing the graph. "Show me what blocks X," "What depends on Y," "What's the critical path?" Understand connections without full details.

### Level 3: Full Context
The complete thing file with YAML, all metadata, and full narrative body:
```
---
id: project-alpha
...
---

# Project Alpha

## What This Is
A major product launch...

## Current Status
...

## Next Steps
...

## Dependencies
...
```

**Use case:** Deep work on a specific thing. Understanding not just what it is, but why it matters, what the context was, what learnings exist.

### How LLMs Use These Levels

When you ask an LLM (Claude or any agent) to help with your things, it should:

1. **Determine what context level is relevant** — Based on your query, what granularity is needed?
2. **Load contextually** — Fetch the appropriate level for the relevant things
3. **Reason across the loaded context** — Process holistically at that granularity
4. **Respond or act** — Provide insights or make updates appropriate to that level

This mirrors how neural networks process information at multiple abstraction levels simultaneously. The LLM doesn't pre-declare what matters; it reasons about relevance in the moment and loads what's needed.

### Progressive Adoption

You don't need to think about levels initially. When you start with a domain:
- Everything is Level 3 (full context)
- Your system is small enough that Claude reads everything

As your system grows:
- You naturally feel the need to ask broad questions ("What's my situation?") — that's Level 1
- You start asking about dependencies and relationships ("What blocks this?") — that's Level 2
- You drill into specific things for operational work — that's Level 3

You discover the levels organically. See the scalability-guide.md for more on when and how tiering becomes relevant.

## Why This Structure Works

- **Parseable:** The YAML is reliable for Claude to extract structure
- **Flexible:** New fields can be added without breaking anything
- **Composable:** Every thing relates the same way, enabling graphs and trees
- **Narrative:** The body keeps the human reasoning and context intact
- **Emergent:** The schema evolves as your life evolves
- **Scalable:** The same files work at multiple levels of granularity
