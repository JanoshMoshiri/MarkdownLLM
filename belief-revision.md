---
id: belief-revision-specification
type: specification
status: stable
version: 1.2
created: 2026-05-27
linked_things:
  - id: thing-specification
    relation: extends
  - id: validate-thing-specification
    relation: complements
  - id: session-memory-specification
    relation: complements
  - id: orchestration-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Belief Revision

## What This Specifies

As a domain matures, it accumulates things — specs, insights, decisions, plans — that may begin to conflict with each other. A new insight contradicts an earlier spec. Two approaches to the same problem point in opposite directions. A principle, held firmly in one session, gets challenged by evidence in a later one.

Without a formal mechanism to surface and hold these contradictions, they accumulate silently. The domain ends up holding two conflicting positions simultaneously, and the agent — lacking explicit guidance — synthesises a plausible but wrong answer from both.

This specification defines:
- `type: conflict` — a first-class thing for documented contradictions between two other things
- Two new relation types: `supersedes` and `contradicts`
- The three resolution outcomes and what each means
- How conflicts are detected, created, and resolved

---

## `type: conflict`

A conflict is a clash between two perspectives, positions, or pieces of content in the domain. It is not a sub-state of an insight. It is not a failed spec. It is its own thing — the documented fact that two things in the domain do not agree, and that this disagreement has not yet been resolved.

A conflict may or may not resolve. Holding a contradiction in explicit tension is a valid, meaningful state. The framework should make "we don't know which of these is right yet" first-class — not a gap to be papered over.

### Structure

```yaml
---
id: [descriptive-conflict-id]
type: conflict
status: open|resolved
created: [ISO-date]
session: [YYYY-MM-DD]
parties:
  - [thing-id-a]
  - [thing-id-b]
resolution: superseded|both-valid|dismissed    # populate when resolved
resolved_by: [thing-id]                        # the surviving position, if superseded
confidence: low|medium
origin: stated|inferred
linked_things:
  - id: [thing-id-a]
    relation: contradicts
  - id: [thing-id-b]
    relation: contradicts
---

# [Conflict Title — name the tension, not the things]

## The Clash
[One clear paragraph: what do these two things disagree about? State the contradiction plainly.]

## Position A — [thing-id-a]
[One paragraph: what does thing A assert? Quote or paraphrase directly.]

## Position B — [thing-id-b]
[One paragraph: what does thing B assert? Quote or paraphrase directly.]

## The Resolution Question
[What needs to be known, decided, or experienced to resolve this?
What kind of answer would close it?]

## Resolution
[Populated when status changes to resolved. What was decided, and why.]
```

**Notes on fields:**

- `parties` — the IDs of the two things in conflict. Usually two; can be more.
- `resolution` — only populated when `status: resolved`
- `resolved_by` — only populated when `resolution: superseded`; points to the thing whose position survived
- `confidence: low|medium` — conflicts are never `confidence: high`; if you're certain, the conflict is already resolved
- `origin: stated` — a human explicitly identified the contradiction; `origin: inferred` — the agent detected it during a session

**Location:** `things/conflicts/` within the domain.

---

## New Relation Types

Two new valid values are added to `linked_things.relation`:

### `supersedes`

This thing's content replaces the referenced thing's content. Most often the referenced position was held previously and is now considered incorrect or outdated — replacement by *correction*, which is this spec's concern. The same relation also marks replacement by *consolidation*: a thing whose content, while not wrong, has been absorbed into the referent because the two duplicated a single responsibility (`thing.md` → The Inverse: Composition). The relation is neutral as to which; the distinction is whether a `conflict` was involved.

```yaml
linked_things:
  - id: old-spec-id
    relation: supersedes
    notes: "Replaces the earlier position on X because Y"
```

When a thing declares `supersedes`, the referenced thing should be updated to reflect this — either marked `status: deprecated` or given a corresponding `linked_things` entry pointing back with relation `superseded-by`.

### `contradicts`

This thing is in active unresolved tension with the referenced thing. Both positions exist; neither has won. When `contradicts` is declared, a `type: conflict` thing **must** exist listing both parties. The `contradicts` relation without a conflict thing is a validation error.

```yaml
linked_things:
  - id: conflicting-spec-id
    relation: contradicts
```

---

## The Three Resolution Outcomes

Every conflict resolves — or doesn't — in one of three ways:

### 1. `superseded`
One position replaces the other. The conflict is closed. `resolved_by` points to the surviving thing. The other thing should be marked deprecated or updated with a `superseded-by` link.

**Use when:** New evidence, reasoning, or experience clearly invalidates one position. The old view was not wrong to hold — it was the best available understanding at the time — but the new view is better.

### 2. `both-valid`
Both positions are true, in different contexts or at different levels of abstraction. Neither is wrong. The conflict was a false binary. Both things survive; they may gain context notes explaining when each applies.

**Use when:** The contradiction was apparent rather than real — e.g., "always do X" and "never do X" are both true once you understand they apply to different scenarios.

### 3. `dismissed`
The question is moot, or the contradiction was discovered to be irrelevant. No position wins because the framing was wrong.

**Use when:** The domain moved on, the question no longer matters, or the contradiction was based on a misreading of one of the things.

---

## Conflict Detection

Conflicts can be surfaced in two ways:

### 1. Human-stated
The human identifies the contradiction directly: "X and Y seem to disagree." The agent creates a `type: conflict` thing, links both parties, and adds `relation: contradicts` entries to both things.

### 2. Agent-inferred
At session end (as part of the session-end belief revision step in `session-memory.md`), the agent scans for: did anything created or modified this session assert something that conflicts with an existing thing? If yes, create a conflict thing with `origin: inferred` and `confidence: low`, then surface it to the human for confirmation before committing.

The agent should be conservative with inferred conflicts — only flag genuine semantic contradictions, not differences in emphasis or scope. When uncertain, ask rather than assert.

---

## When To Scan For Conflicts

Human-stated and session-end detection both rely on a contradiction being *noticed* in the course of other work. That leaves a gap: contradictions that already exist in the corpus but that no single session happens to look at. As a domain grows, standing contradictions accumulate silently — exactly the failure this spec exists to prevent. Systematic scanning closes the gap by making conflict detection a scheduled reflexive behaviour, not only a reactive one.

Scanning is implemented by the `detect-conflicts` prompt in **scan mode** (`templates/prompts/detect-conflicts.md`). It runs at two cadences, chosen so the cost is proportional to the value:

### Event-triggered — when claims gain authority (`on-status-change`)

When a `type: specification` thing moves to `status: stable`, or a `type: insight` is promoted, its assertions stop being provisional and start being load-bearing. That transition is the right moment to check them against what the domain already holds. The scan is scoped to *that thing and its immediate `linked_things` neighbours* — a small Level 2 load (~3–6k tokens), affordable on every such transition.

### Periodic — full sweep at retrospective

A retrospective is the natural place for the expensive, complete check: walk every relationship edge in the domain and test connected things for contradiction. This is where standing conflicts that no event surfaced finally get caught. To keep a full sweep affordable, the scan walks a `relationships` derived index (`things/_index/relationships.md`) where one exists — the edge list — loading full Level 2 context only for the endpoints of suspect edges, rather than loading the whole domain. Without an index, the full sweep falls back to a Level 2 load of all things, which is why it is reserved for retrospective cadence rather than run every session. See `derived-index.md`.

Whatever surfaces a conflict — human, session-end, or scan — the resolution machinery is identical: create a `type: conflict` thing, link both parties with `relation: contradicts`, surface for confirmation, and resolve into one of the three outcomes.

---

## Conflict Lifecycle

```
Detected (open)
    ↓
Held in tension — surfaces as an open loop (orient reads open conflicts)
    ↓
Resolution reached (in-session or across sessions)
    ↓
Resolved — outcome declared (superseded / both-valid / dismissed)
    ↓
Referenced things updated accordingly
    ↓
Conflict thing status: resolved (kept as audit trail)
```

Resolved conflict things are **not deleted**. They are part of the domain's intellectual history — the record of what was contested and how it was settled. They may be eligible for disposition to semi-active storage (see `thing-lifecycle.md`) once resolved and aged.

---

## Relationship To Other Specs

- **thing.md** — `conflict` joins `insight` and `continuity-brief` as a framework-reserved type. `supersedes` and `contradicts` are added as valid `linked_things.relation` values.
- **validate.thing.md** — A `relation: contradicts` without a corresponding conflict thing is a validation error. Open conflicts older than 30 days without updates are surfaced as Info.
- **session-memory.md** — The session-end ritual includes a belief revision step: scan for new contradictions, create conflict things where found.
- **orchestration.md** — The `session-end` bound prompts encompass belief revision alongside insight extraction. The `detect-conflicts` prompt (scan mode) is bound to `on-status-change` and `retrospective` for systematic detection.
- **derived-index.md** — The `relationships` derived index makes the full-domain conflict sweep affordable by providing the edge list to walk, so the scan loads full context only for suspect endpoints.
