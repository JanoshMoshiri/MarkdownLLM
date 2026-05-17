# Thing To Do - Skill Definition

## What Is A Thing To Do?

A thing to do is the atomic unit of the life management system. Everything is a thing to do. A project is a thing to do. A task within that project is a thing to do. A subtask is a thing to do. A dependency or blocker is a thing to do. Even a simple action like "brush teeth" is a thing to do.

A thing to do is:
- **Self-contained:** It has all the information needed to understand what it is
- **Linkable:** It can reference other things to do and be referenced by them
- **Mutable:** It can change status, gain detail, gain context, split into subtasks
- **Reasonably scoped:** Large enough to be meaningful, small enough to be actionable

## Structure Of A Thing To Do

Every thing to do file follows this pattern:

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
- Values: `thing-to-do` (catch-all for simple actions), `task`, `project`, `subtask`, `goal`, `milestone`, `recurring`, or any other type that emerges as you use the system
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
- Categorical labels
- Examples: `work`, `health`, `finance`, `learning`, `project-x`
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

## How To Create A Thing To Do

1. **Choose an ID:** Make it descriptive but short. `brush-teeth`, not `personal-hygiene-daily-tooth-brushing-routine`. You'll type these a lot.

2. **Choose a Type:** Is this a project? A task? A simple action? Start simple; it can change.

3. **Set Initial Metadata:** At minimum: id, type, status, created. Add due_date if there's a deadline. Add tags for categorization.

4. **Write the Body:** Explain what this is and why it matters. Keep it brief unless detail is needed.

5. **Link If Needed:** If this relates to other things or has subtasks, add those references now or later as they become clear.

Example minimal thing:
```
---
id: brush-teeth
type: thing-to-do
status: not-started
created: 2026-05-17
tags:
  - health
  - daily
---

# Brush Teeth

Morning dental hygiene. Do this before breakfast.
```

Example richer thing:
```
---
id: quarterly-planning
type: project
status: in-progress
priority: high
due_date: 2026-06-15
created: 2026-05-17
tags:
  - planning
  - quarterly
  - work
linked_things:
  - id: gather-metrics
    relation: subtask
  - id: stakeholder-alignment
    relation: subtask
  - id: budget-review
    relation: dependency
---

# Quarterly Planning Q2 2026

## What This Is
High-level planning session to set direction for Q3. Involves reviewing Q2 performance, gathering team feedback, and establishing priorities.

## Why It Matters
This shapes how we allocate resources and where we focus energy for the next quarter. It's a forcing function for alignment.

## Current Status
Just started. Waiting on Q2 metrics to be finalized.

## Next Steps
- [ ] Get final metrics from finance
- [ ] Conduct team one-on-ones
- [ ] Draft priorities
- [ ] Present to stakeholders

## Blockers
Budget review not complete yet.
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

## Why This Structure Works

- **Parseable:** The YAML is reliable for Claude to extract structure
- **Flexible:** New fields can be added without breaking anything
- **Composable:** Every thing relates the same way, enabling graphs and trees
- **Narrative:** The body keeps the human reasoning and context intact
- **Emergent:** The schema evolves as your life evolves
