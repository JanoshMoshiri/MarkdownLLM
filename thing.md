---
id: thing-specification
type: specification
status: evolving
version: 2.20
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: read-thing-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: interface-specification
    relation: complements
---

# Thing Definition

<!-- kernel -->
**A thing** = one markdown file: YAML frontmatter + narrative body. One identity, one reason to change.

**Required fields:** `id` (kebab-case, stable, unique), `type`, `status`, `created` (ISO 8601).

**Recommended:** `due_date`, `priority` (low/medium/high/critical), `tags[]`, `parent`, `linked_things[{id, relation, notes?}]`, `dependencies[]`, `blocks[]`, `confidence` (high/medium/low; default high), `origin` (stated/inferred/synthesised/external; default stated), `verified` (external things only). Cross-domain: `source_domain`+`source_id`+`source_commit` (the reference triple pinning a cross-domain import; all three or the import is uncheckable) · `exposed` (opt-in membership of the domain's served face; default false, relational graph stripped on egress). Emergent fields: add only when they serve reasoning.

**Status:** the domain declares per-type vocabularies in `_schema.yaml` (enforced by `mdllm validate`); default when undeclared: not-started/in-progress/blocked/paused/completed/cancelled. Reserved types are fixed: specification/guide/manifesto/skill/prompt → draft/evolving/stable/deprecated · insight → active/promoted/dismissed · conflict → open/resolved · retrospective → draft/complete · continuity-brief → live · index → live/stale · decision → made/superseded · workflow-definition → draft/evolving/stable/deprecated · workflow-run → active/paused/completed/abandoned. A type may also declare `terminal_statuses` — which of its own statuses mean *settled*; the declaration replaces the universal terminal set for that type, and every forward-work check (orientation, triggers, cascade) reads it through one `is_terminal`. Not declarable on reserved types (the tool owns their settled sets).

**Reserved types:** `insight`, `continuity-brief`, `conflict`, `retrospective`, `decision`, `workflow-definition`, `workflow-run` (see session-memory.md, belief-revision.md, retrospective.md, provenance.md, workflow-state.md). Internal: `guide`/`manifesto`. `specification`: framework specs + a domain's scaffold-delivered specification skill, nothing else. Domain-usable with fixed vocabulary: `skill` (read/write/workflow skills)/`prompt` (lifecycle statuses, tool-owned). Generated: `index`. The tool's `RESERVED_STATUSES` is the authority on this set — restated lists have lagged it on three surfaces at once.

**Quarantine:** `origin: external` ⇒ `verified: false` until a human confirms; no decision/calculation/output may rest on an unverified external thing (provenance.md). The flip is an auditable event: commit external things unverified, flip in a *separate* commit naming the human in `verified_by` — the floor rejects born-verified and unattributed flips (Warning; Error under `options: {quarantine: strict}`). Cross-domain imports carry the reference triple; `mdllm imports-check` re-checks pin *and* content against the source's face — `stale` or `diverged` re-opens the quarantine as an external inflection (change-reconciliation.md).

**Derived figures:** a figure the domain *derives* declares how, in `computed: {field-path: expression}` — the floor evaluates it (`mdllm calc`) and re-checks it at every commit (`validate`: Warning, Error under `options: {computed: strict}`). The assertion stays in place; the derivation sits beside it. Never assert a total you could declare a derivation for — arithmetic is mechanical, and reasoning gets it wrong silently. Grammar: `docs/calculation-reference.md`.

**Cohesion (one reason to change):** decompose when content serves a different audience, changes at a different rate, or is independently reusable (`instance-of`/`derived-from`/`template-for`/`applies-to` = split). Compose the inverse: one responsibility spread across several things → consolidate into the cohesive survivor and mark the rest `superseded-by` it. Merge duplication, never contradiction.

**Loading:** L1 metadata only · L2 +relationships · L3 full body. Match depth to query; never load everything for a broad question.
<!-- /kernel -->

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
- Seven types are **framework-reserved** and have fixed semantics regardless of domain:
  - `insight` — an emerging idea or held view from a session, preserved for future context
  - `continuity-brief` — **retired (v3.17), reserved-but-deprecated**: was the domain's forward-looking session brief, now superseded by the generated orient view (open-loop things); kept reserved only so domains mid-transition still validate
  - `conflict` — a documented contradiction between two other things, held as a first-class thing until resolved
  - `retrospective` — a periodic quality reflection on domain reasoning; one per period, not per session
  - `decision` — a judgement made from knowledge, with inputs pinned to git commits via `informed_by`
  - `workflow-definition` — a reusable process skeleton with its stages expressed as data and the transitions allowed between them
  - `workflow-run` — one live instance advancing through a `workflow-definition`: a `current_stage` cursor, an advisory `held_by` claim, and a resume narrative
  - See `session-memory.md`, `belief-revision.md`, `retrospective.md`, `provenance.md`, and `workflow-state.md` for full specifications.
- Two types are **framework-internal**: `guide` and `manifesto`. These are used by the framework's own files only. They carry lifecycle status semantics (`draft`, `evolving`, `stable`, `deprecated`) and should not be used for domain things.
- `specification` is framework-defined with the same lifecycle vocabulary and has exactly **two legitimate homes**: the framework's own spec files, and a domain's *specification skill* — the one scaffold-delivered file that states why the domain exists (`templates/domain-specification.skill.md.template` types it `specification`, and every scaffolded domain carries it that way). Any other domain use is misuse. *(The tenth review caught v2.18's "framework-internal only" claim contradicting the scaffold's own delivery — the classification followed neither the template nor the estate; this one follows both.)*
- Two types are **framework-defined and domain-usable with a fixed vocabulary**: `skill` (a domain's read, write, and workflow skills — the specification skill is `type: specification`, above) and `prompt` (the reasoning prompts in `prompts/`). They carry the same lifecycle vocabulary, built into the tool; domains use them freely but cannot redeclare their statuses.
- One type is **framework-generated**: `index`. An index thing is a regenerable cache that aggregates one signal (triggers, relationships, schema fields, provenance) across a domain's things, living in `things/_index/`. It is produced by the agent, not authored by hand, and uses status `live`/`stale`. The things are always the source of truth; the index is a derived copy. Full specification: `derived-index.md` (the signal set is the tool's — `mdllm index` — not this list).

**status** (string)
- Current state of this thing
- **The domain owns its status vocabulary.** Each domain declares the valid
  statuses per thing type in its normative schema (`things/_schema.yaml`, read by
  `tools/mdllm.py`). A compliance domain's return might move
  `open → figures-ready → submitted → paid → reconciled`; a task domain might use
  the universal defaults. Model the domain's real state machine — don't force it
  into a generic one. (Resolution of conflict `status-vocabulary-universal-vs-domain`, 2026-06-11.)
- The universal default vocabulary — used when no schema declares one for the
  type: `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`
- Framework-reserved types keep fixed vocabularies domains cannot redefine:
  `specification`/`guide`/`manifesto`/`skill`/`prompt` use `draft`, `evolving`,
  `stable`, `deprecated`; `insight` uses `active`, `promoted`, `dismissed`;
  `conflict` uses `open`, `resolved`; `retrospective` uses `draft`, `complete`;
  `continuity-brief` uses `live`; `index` uses `live`, `stale`;
  `workflow-definition` uses `draft`, `evolving`, `stable`, `deprecated`;
  `workflow-run` uses `active`, `paused`, `completed`, `abandoned`
- **A type may declare which of its statuses mean *settled*** — the optional
  per-type `terminal_statuses` list in `_schema.yaml`, alongside `statuses`
  (v3.19.0). A domain whose lifecycle is mostly steady-state needs this so
  finished-or-in-force things (a signed document at `approved-current`, a
  pointer at `live`) stop counting as forward work. A declaration *replaces*
  the universal terminal set (`completed`, `cancelled`, `resolved`, …) for
  that type — explicit beats implicit; values outside the type's own
  vocabulary are ignored and reported at Warning, as is a declaration on a
  framework-reserved type (the tool owns the reserved types' settled sets).
  Every check that asks "is this still forward work?" — orientation's
  open-loop count, `triggers`' overdue and `subtasks_complete` scans,
  `cascade`'s unblock and roll-up passes — routes through one
  `is_terminal(schema, meta)`, so the domain declares its lifecycle once and
  all agree. A type that declares nothing behaves exactly as before.
- Updated by the agent as work progresses

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
- Common relation values: `subtask`, `related`, `informs`, `implements`, `extends`, `references`, `complements`, `documents`
- Keep the vocabulary small: declare it in `_schema.yaml`, prefer the forward direction over inverse pairs (the link lives on the dependent thing), and don't duplicate the `dependencies`/`blocks` fields as relations
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
- List of things that must be done before this — a **hard prerequisite**, not a
  soft association
- Helps Claude understand sequencing
- Can be empty
- The floor enforces the prerequisite reading: a thing in a terminal status may
  not depend on unfinished work (terminal dependencies — completed, cancelled,
  deprecated, … — count as resolved). If a relationship is "builds on" / "relates
  to" / "informs" rather than "must finish first", model it as `linked_things`,
  not `dependencies` — that is the correct fix when the gate fires, not a reason
  to weaken it (see
  [hard-invariants-encode-a-semantic-assumption](things/insights/hard-invariants-encode-a-semantic-assumption.md))

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
- Values: `stated` (explicitly said by the human), `inferred` (concluded by the agent from other things), `synthesised` (assembled by the agent from multiple sources), `external` (ingested from outside the human-agent pair — bank statements, emails, third-party documents; see `provenance.md`)
- Critical for LLM trust calibration: an `inferred` thing should be treated differently from a `stated` one
- Defaults to `stated` if omitted — only add when the content was not directly expressed by a human
- Works in tandem with `confidence`: a thing that is both `origin: inferred` and `confidence: low` should always be surfaced for human review before being acted on
- **`origin: external` triggers quarantine**: the thing carries `verified: false` until a human confirms its content, and no decision, calculation, or output may rest on it while unverified. Full rule: `provenance.md`

**verified** (boolean)
- Only meaningful on `origin: external` things: whether a human has confirmed the ingested content (reconciliation, review, spot-check)
- `false` on creation; flipped to `true` with a narrative note of how it was verified
- The flip is an auditable event with its own discipline (separate commit, `verified_by` naming the human) — full rule: `provenance.md`

**source_domain / source_id / source_commit** (strings — the cross-domain reference triple)
- Present only on `origin: external` things imported from *another domain's exposed face* (`provenance.md` → Cross-Domain Imports; design record: `docs/plans/mcp-domain-server.md`)
- `source_domain` — the producing domain, named as in the consumer's `.mcp.json` address book entry
- `source_id` — the thing's id in the producer's id-space (foreign to this domain; never resolved locally)
- `source_commit` — the producer-computed commit that last touched the exposed thing at import time: the pin `mdllm imports-check` compares against the source's current face
- All three are required for the import to be sync-checkable; an import missing any part reports `INCOMPLETE` and counts as unchecked coverage, never as fresh

**exposed** (boolean)
- Opt-in marker joining this thing to the domain's exposed face, served by `mdllm mcp-serve`
- Default false — nothing crosses the domain boundary unless its author opts it in (the semi-permeable membrane)
- Exposure is publication: an exposed thing's content and descriptive frontmatter cross to any consumer the operator wires; its relational graph (`linked_things`, `dependencies`, `parent`, `triggers`, `informed_by`, `parties`) never does — those ids live in this domain's id-space and are stripped on egress

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

Triggers are declarative attention signals — metadata telling the agent "when you're next active, check whether this condition is true, and surface it." They are not code; the LLM decides how to respond. The type and condition vocabulary is owned by `trigger-specification.md` — full specification including all types, condition values, action values, and evaluation semantics there, never restated here (this paragraph carried "four types" for three releases after `type: import` made it five; a count stated at the authority cannot lag).

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

### The Inverse: Composition

Decomposition has a mirror image, and a domain that only ever splits will fragment. When a single responsibility is spread across several things — three insights circling one idea, two methodologies that have converged, a rule restated in four places — cohesion has been lost *between* things rather than *within* one. The fix is the inverse move: consolidate the fragments into the one thing that cohesively owns the responsibility, and redirect what pointed at them.

This is the same Single Responsibility Principle read backwards. Decomposition asks *"does this thing hold more than one reason to change?"* Composition asks *"do these things share a single reason to change that no one of them fully owns?"* If yes, they are one responsibility wearing several files, and the duplication costs exactly what the coupling rules warn about: an update must touch every copy in lockstep, and reasoning must reconcile near-duplicates before it can act.

#### The Duplication Test

Before keeping two things separate, ask:

> *If this idea changed, how many things would I have to edit in lockstep to keep them consistent?*

If the honest answer is more than one, those things are not loosely coupled — they are a single responsibility that has been copied. Consolidate.

#### How To Consolidate

The inverse of extraction, run with the same care:

1. **Choose the survivor** — the thing that most cohesively owns the responsibility, or write a new one that does.
2. **Fold in** the distinct content of the fragments; drop what was mere restatement.
3. **Redirect** every inbound reference to the survivor.
4. **Tombstone** each absorbed thing: the survivor `supersedes` them, each fragment is `superseded-by` the survivor and moves to its terminal status (`dismissed` for an insight, `superseded` for a decision). Do not delete it — the tombstone keeps the merge walkable and git keeps the content. This reuses the framework's existing replacement vocabulary; no new relation is needed.

Two boundaries keep composition honest. It is **not contradiction resolution** — it merges things that *agree* but duplicate; two things that genuinely disagree are a `conflict`, resolved through `belief-revision.md`, not folded together. And it is run **conservatively** — when two things look redundant but carry distinct provenance or context, link them rather than collapse them. Relate, don't merge.

Like the full conflict scan, composition is a sweep-class refactor: it reshapes the corpus and wants the whole field in view, so it belongs at retrospective cadence rather than mid-session (`retrospective.md`).

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
