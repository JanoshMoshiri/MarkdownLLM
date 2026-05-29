---
id: thing-specification
type: specification
status: stable
version: 2.9
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: read-thing-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: validate-thing-specification
    relation: enforced-by
  - id: git-workflow-specification
    relation: complements
  - id: interface-specification
    relation: complements
  - id: trigger-specification
    relation: extended-by
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
- Four types are **framework-reserved** and have fixed semantics regardless of domain:
  - `insight` — an emerging idea or held view from a session, preserved for future context
  - `continuity-brief` — the domain's live forward-looking session-continuity document (one per domain)
  - `conflict` — a documented contradiction between two other things, held as a first-class thing until resolved
  - `retrospective` — a periodic quality reflection on domain reasoning; one per period, not per session
  - See `session-memory.md`, `belief-revision.md`, and `retrospective.md` for full specifications.
- Three types are **framework-internal**: `specification`, `guide`, and `manifesto`. These are used by the framework's own spec files only. They carry lifecycle status semantics (`draft`, `evolving`, `stable`, `deprecated`) and should not be used for domain things.

**status** (string)
- Current state of this thing
- Values for domain things (tasks, projects, goals, etc.): `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`
- Values for framework specification things (`type: specification`, `type: guide`, `type: manifesto`): `draft`, `evolving`, `stable`, `deprecated` — these reflect lifecycle maturity, not workflow state
- Values for insight things (`type: insight`): `active`, `promoted`, `dismissed` — see `session-memory.md`
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
- Structure: `{ id: "thing-id", relation: "[type]", notes: "optional context" }`
- Allows Claude to traverse the graph of your life
- Common relation values: `subtask`, `dependency`, `blocks`, `related`, `similar`, `informs`, `implements`, `complements`
- Decomposition relation values — signal that two things should be structurally separate (see **Thing Cohesion and Decomposition**):
  - `instance-of` — this thing is a specific occurrence of the referenced methodology, pattern, or template
  - `derived-from` — this thing's content was produced by applying the referenced thing
  - `template-for` — this thing is a reusable skeleton; the referenced thing is a filled-in instance
  - `applies-to` — this thing is a methodology, rule, or pattern applied to the referenced subject
- Framework-reserved relation values (fixed semantics across all domains):
  - `supersedes` — this thing's content replaces the referenced thing's content
  - `contradicts` — this thing is in active unresolved tension with the referenced thing; a `type: conflict` thing must exist listing both parties
  - `superseded-by` — the inverse of `supersedes`; this thing's content has been replaced

**dependencies** (array of strings - ids)
- List of things that must be done before this
- Helps Claude understand sequencing
- Can be empty

**blocks** (array of strings - ids)
- List of things this blocks from starting
- Inverse of dependencies
- Helps Claude understand impact

**confidence** (string)
- How certain the domain is that the content of this thing is correct
- Values: `high`, `medium`, `low`
- Defaults to `high` if omitted — so only add when there is genuine uncertainty
- Particularly important for `type: insight` and `type: specification` things where the LLM should calibrate how firmly to treat content as ground truth
- When `confidence: low`, the LLM should surface the uncertainty rather than reason from the thing as fact

**origin** (string)
- The provenance of this thing's content — who or what produced it
- Values: `stated` (explicitly said by the human), `inferred` (concluded by the agent from other things), `synthesised` (assembled by the agent from multiple sources)
- Critical for LLM trust calibration: an `inferred` thing should be treated differently from a `stated` one
- Defaults to `stated` if omitted — only add when the content was not directly expressed by a human
- Works in tandem with `confidence`: a thing that is both `origin: inferred` and `confidence: low` should always be surfaced for human review before being acted on

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

Triggers are declarative attention signals — metadata telling the agent "when you're next active, check whether this condition is true, and surface it." They are not code; the LLM decides how to respond. Four types: `time`, `dependency`, `threshold`, `relationship`. Full specification including all condition values, action values, and evaluation semantics: see `trigger-specification.md`.

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

## Thing Cohesion and Decomposition

A well-formed thing is cohesive: everything within it belongs together, changes together, and serves the same audience. When a thing violates this, reasoning costs rise — the LLM must load irrelevant content, mentally filter before acting, and risk cross-contaminating stable knowledge with volatile data. Loose coupling between things and tight coherence within them is what keeps the system cheap to reason on.

### The Decomposition Principle

**A thing has a single identity and a single reason to change.**

If content within a thing:
- Serves a different audience than the rest of the thing
- Changes at a different rate
- Could be reused independently in another context

...it is a candidate for extraction into its own thing, linked back via `linked_things`.

This is the Single Responsibility Principle applied to knowledge units. It keeps things small enough to reason on cheaply, stable enough to link with confidence, and clean enough to reuse without copying.

### The Consumer Test

Before creating or expanding a thing, ask:

> *If I needed to reuse part of this in a different context, would I have to copy-paste and strip out irrelevant material?*

If yes — **decompose**. Extract the reusable content into its own thing and link from both consumers. The original thing stays coherent. The extracted thing becomes independently useful.

### Rate of Change Hierarchy

Content that changes at different rates belongs in different things. Mixing stability levels within a single thing makes every update a potential source of contamination.

| Content Type | Change Cadence | Should Not Contain |
|---|---|---|
| Methodology | Stable — changes when the *process* improves | Instance data from specific engagements |
| Environment baseline | Changes when *infrastructure* changes | The discovery process used to produce it |
| Derived output | Changes per engagement or run | The methodology that produced it |
| Template | Structural skeleton — rarely changes | Specific filled-in values or instances |

**Rule of thumb:** If updating one part of the thing should never require reading or modifying another part — they belong in separate things.

### Concrete Examples

#### Anti-Pattern: Coupled (Do Not Do This)

```yaml
---
id: production-env-assessment-org-alpha
type: methodology
status: stable
---
```

```markdown
# Production Environment Assessment

## Methodology
1. Interview infrastructure leads
2. Review IaC repositories
3. Map service dependencies
4. Assess compliance posture

## Org Alpha Baseline
- Cloud: AWS eu-west-1
- Services: 47 microservices
- Compliance: ISO 27001 certified
- Key constraint: No third-party egress without security review
```

**Problem:** The methodology is stable and reusable across any organisation. The Org Alpha baseline is specific and will change when their environment changes. When Org Alpha updates their cloud region, you must open the methodology thing to make that edit — risking accidental methodology drift and preventing clean reuse of the methodology elsewhere.

#### Decomposed (Do This)

**Thing 1 — The methodology:**
```yaml
---
id: production-env-assessment-methodology
type: methodology
status: stable
linked_things:
  - id: org-alpha-production-baseline
    relation: instance-of
---
```

```markdown
# Production Environment Assessment Methodology

A repeatable process for discovering production environment constraints and landscape for professional organisations.

1. Interview infrastructure leads
2. Review IaC repositories
3. Map service dependencies
4. Assess compliance posture
```

**Thing 2 — The derived instance:**
```yaml
---
id: org-alpha-production-baseline
type: environment-baseline
status: evolving
linked_things:
  - id: production-env-assessment-methodology
    relation: derived-from
---
```

```markdown
# Org Alpha Production Environment Baseline

Derived from the production environment assessment methodology.

- Cloud: AWS eu-west-1
- Services: 47 microservices
- Compliance: ISO 27001 certified
- Key constraint: No third-party egress without security review
```

Now each thing has a single reason to change. The methodology improves independently. The baseline updates when Org Alpha's environment changes. Either can be loaded independently without contamination from the other.

### Relationship Types as Decomposition Indicators

Certain relation values in `linked_things` are signals that two things should be — or already are — separate. When you find yourself wanting to express one of these relations, the framework is telling you that separation is the right structure.

| Relation | What It Signals |
|---|---|
| `instance-of` | A specific occurrence of a pattern, methodology, or template — always a separate thing |
| `derived-from` | Content was produced by applying another thing — the output belongs in its own thing |
| `template-for` | A reusable skeleton with a specific instantiation — template and instance are different things |
| `applies-to` | A methodology, rule, or pattern applied to a specific subject — separate the general from the specific |

**Rule:** If you are about to embed content that could honestly be described by one of these relations — stop. Create the second thing instead. Link them. The relation becomes the coupling mechanism, and loose coupling is the goal.

## Special Type: Example

For building pattern libraries and teaching LLMs domain-specific reasoning, create things with `type: example`. See `example-things.md` for the full specification, including the frontmatter template, when to use examples, and why examples work better than rules for inductive LLM learning.

## Multi-Level Context Windows

The same thing file can be loaded at three granularities: metadata only (broad landscape scan), metadata + relationships (graph traversal), or full context (deep work on a specific thing). See `read.thing.md` for the complete loading strategy, decision guidance, and examples.

## Why This Structure Works

- **Parseable:** The YAML is reliable for Claude to extract structure
- **Flexible:** New fields can be added without breaking anything
- **Composable:** Every thing relates the same way, enabling graphs and trees
- **Narrative:** The body keeps the human reasoning and context intact
- **Emergent:** The schema evolves as your life evolves
- **Scalable:** The same files work at multiple levels of granularity
