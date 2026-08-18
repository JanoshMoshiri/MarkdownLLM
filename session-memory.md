---
id: session-memory-specification
type: specification
status: evolving
version: 1.5
created: 2026-05-27
linked_things:
  - id: thing-specification
    relation: extends
  - id: orchestration-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: belief-revision-specification
    relation: complements
---

# Session Memory

## What This Specifies

This document defines how the framework preserves **generative knowledge** — the ideas, views, hypotheses, and unresolved threads that surface during a session but are not yet ready to become specs, decisions, or domain things.

The framework already handles **resolved knowledge** well: a decision becomes a thing, a spec gets committed, a task gets status-tracked. But generative knowledge — the reasoning behind a decision, competing perspectives, open questions raised but deferred — disappears when a session ends. Without explicit preservation, every session starts cold.

This specification defines two primitives and one deliberate ritual to close
that gap — deliberate meaning *explicitly invoked* at session close, by the
operator or by the agent recognising the session is ending; it is a bound
prompt, never an automatic hook ("the session is ending" is not an
observable, agent-caused event).

---

## The Two Primitives

### `type: insight`

An insight is an emerging idea, held view, working hypothesis, or captured perspective that surfaced during a session and is worth carrying forward.

**What it is:**
- An emerging idea that isn't yet fully formed into a spec or decision
- A held view or position that will influence how future decisions should be made
- A hypothesis that was agreed on but not yet tested or acted on
- A tension that was identified but not resolved
- A question that was raised but not answered in the session

**What it is not:**
- A decision (update the relevant thing directly)
- A specification (create a `type: specification` thing)
- A routine status update or procedural confirmation

**Structure:**

```yaml
---
id: [descriptive-kebab-case-id]
type: insight
status: active|promoted|dismissed
version: 1.0
created: [ISO-date]
session: [YYYY-MM-DD]
source: human|agent|both
confidence: high|medium|low
origin: stated|inferred|synthesised
promoted_to: [thing-id]        # populate if status becomes promoted
disposition: keep-active       # optional; marks a standing/parked insight deliberately kept live
disposition_reason: [one line] # required when disposition is keep-active — why it stays live with no live dependant
linked_things:
  - id: [related-thing-id]
    relation: informs|challenges|supports
---

# [Insight Title]

## The Insight
[One to three sentences: the actual idea, view, or hypothesis]

## Why It Matters
[Why this is worth carrying forward — what decisions or threads it affects]

## Context
[What triggered this in the session — the question, tension, or observation that surfaced it]
```

**Lifecycle:**

| Status | Meaning |
|--------|---------|
| `active` | Still live — needs to return in a future session |
| `promoted` | Crystallised into a spec, decision, or domain thing — `promoted_to` field is populated |
| `dismissed` | Considered and deliberately set aside — kept for audit trail, not deleted |

**Location:** `things/insights/` within the domain.

---

### `type: continuity-brief` — RETIRED (superseded by orient)

The continuity brief — a single per-domain `continuity.md`, updated at session end
and loaded at session start — has been **retired**
(`dissolve-continuity-into-reconciliation`). It conflated the corpus's two sides in
one hand-maintained file, and both halves had better homes
(`orient-and-reconciliation-are-the-corpus-two-sides`):

- Its **backward** content (what was done) was always the **commit stream**'s (the
  WORKLOG was only ever an on-demand view of it, also retired in v3.17).
- Its **forward** content (what's still live) is now the **thing graph**, surfaced by
  the generated **orient** view (`mdllm session-start` → "Open loops": non-terminal
  work things + open conflicts). An open thread worth carrying is a thing, tracked and
  retired by status — not a prose line that never gets pruned.
- Its **live-insight registry** is gone: insight liveness is a graph property (an
  inbound edge from a live thing, or a `disposition: keep-active` marker), not
  brief presence.

The `continuity-brief` type remains reserved-but-**deprecated** so domains mid-
transition validate while they still carry a `continuity.md`; removing the type from
the floor (`thing.md`, `_schema`, the reserved-status machinery) is a tracked
follow-on. New domains should not create one.

---

## The Session-Start Staleness Check

Insights re-enter each session as trusted context — but the domain keeps moving after
they're written. Without a check, a session can reason confidently from an insight
whose factual basis changed three sessions ago.

The check is **scoped, not a sweep**:

1. Take the **live insights** — `active`, with a live inbound edge or a
   `disposition: keep-active` marker (a small, bounded set; liveness is graph-keyed)
2. Identify things modified recently (git provides this for free: commits or diff
   since you were last active, scoped to `things/`)
3. Re-read only the live insights whose subject matter overlaps the changed
   things; surface any that no longer hold rather than silently reasoning from them

Cost: near-zero when nothing relevant changed; a few targeted reads when it did.
The full-corpus contradiction sweep remains a retrospective-cadence behaviour
(`belief-revision.md` → When To Scan For Conflicts) — this check exists precisely
so that gap doesn't leak into every session. Implemented as Step 0 of the
`session-orientation` prompt.

---

## The Session-End Extraction Ritual

This ritual is implemented as the **`session-end-continuity` prompt** bound to the `session-end` hook point. See `templates/prompts/session-end-continuity.md` for the full prompt template, and `orchestration.md` → Bindings for how it is invoked.

The prompt is explicitly invoked at session end — either by the user requesting it, or by the agent recognising the session is closing. It is not automatic; it requires a deliberate trigger.

### Step 1: Scan For Insights

First reconstruct the **logical session**, because the dialogue still visible to
the agent is not guaranteed to be the whole session. A harness may compact only
near its context ceiling, at an earlier threshold or cadence, repeatedly, or not
at all during the session. **Compaction changes the available context; it does
not create a session boundary.** The operator's declared start/end and task
continuity define the session.

Use two evidence sources together:

1. **Surviving dialogue** — scan the conversation still present after any
   compactions for uncommitted positions, questions, tensions, and reframings.
2. **The relevant commit range** — inspect `git log` / `mdllm worklog` across the
   logical session for work, decisions, evidence, and intermediate harvests
   already made real. In multi-harness work, attribute those commits to their
   seats; do not treat another agent's intermediate `session-end:` delimiter as
   the end of the operator's larger session.

Then review the reconstructed session for:
- Non-obvious positions taken by either party
- Hypotheses that were agreed on but not acted on
- Questions raised but not answered
- Tensions identified but not resolved
- Reframings that changed how something is understood

Apply the **preservation test**: *Would a fresh agent starting this domain cold benefit from knowing this?* If yes, preserve. If routine, procedural, or already captured in a thing, skip.

Report already-captured learning honestly. If the commit range contains the
session's insights and the surviving dialogue adds none, say **"no additional
insight"**, never "no insight." Neither source substitutes for the other:
context alone can be lossy after compaction; git cannot contain an idea that was
discussed but never written.

### Step 2: Create Insight Things

For each insight worth preserving, create a `type: insight` thing in `things/insights/`.

### Step 3: Disposition The Standing Insights (the brake)

Step 2 grows the insight population every session; this step prunes it, so the two stay
in balance — capture is paired with reckoning, and the population can't outrun the rate
it's triaged. This is the session-cadence counterpart to the retrospective's deeper
triage beat (`Insight Lifecycle Management` below).

Run `python {framework_root}/tools/mdllm.py validate .` and act on **every
insight-disposition Info finding** the floor surfaces — it lists exactly the insights
that need a decision, so none can quietly go dark:
- *"active insight with no inbound edge from a live thing"* — force a disposition:
  **promote** (populate `promoted_to`), **dismiss**, **consolidate** a genuine duplicate
  into a survivor, **link** it from live work, or mark **`disposition: keep-active`** with
  a one-line `disposition_reason`.
- *"keep-active with no `disposition_reason`"* — add the reason or re-disposition.

This is a forcing function, not a corpus sweep: the deeper composition/consolidation and
conflict/schema scans stay the retrospective's (`retrospective.md`).

### Step 4: Belief Revision — Check For Contradictions

Before closing out, scan for contradictions introduced this session:

- Did any new insight or modification assert something that conflicts with an existing thing?
- Do any two things now in view hold incompatible positions?

For each contradiction found:
1. If it can be resolved in-session (one position clearly supersedes the other): update the relevant things, declare `relation: supersedes` / `relation: superseded-by`, and mark the old position deprecated if appropriate.
2. If it cannot be resolved in-session: create a `type: conflict` thing in `things/conflicts/`, add `relation: contradicts` to both parties' `linked_things`. The open conflict *is* the open loop — orient surfaces it (`mdllm session-start` → "Open loops"); no separate brief entry is needed.

Be conservative — only flag genuine semantic contradictions, not differences in emphasis or scope. When uncertain, surface for human confirmation rather than silently creating a conflict thing. Full spec: `belief-revision.md`.

### Step 5: Manage Open-Loop Things

There is no brief to update — forward state lives in the thing graph, and the
generated **orient** view (`mdllm session-start` → "Open loops") reads it. So instead
of editing a singleton, reconcile the graph:
- New forward intent from this session → create or update a `plan` or work thing.
- Work that resolved this session → move it to a terminal status, so orient stops
  surfacing it.
- Open conflicts (from Step 4) are already open loops — orient surfaces them; nothing
  else to record.
- Insight liveness is graph-keyed, not brief-keyed: an `active` insight stays in
  circulation via an inbound edge from a live thing (or a `disposition: keep-active`
  marker), per *Insight Lifecycle Management* below — not by being listed anywhere.

### Step 6: Commit

Commit all new insight things, new conflict things, and the open-loop updates with a
rich `session-end:` message following `git-workflow.md` conventions. The commit **is**
the backward record — there is no `continuity.md` or `WORKLOG.md` to update; `mdllm
worklog` prints an on-demand, uncommitted view of the commit stream when wanted.

### Step 7: Report Publication Debt

Run `mdllm estate-sync . --status` and surface the result. Under autopush (the
default) every `ahead +n (unpushed)` line is an anomaly — an offline session, a
rejected push owed a routing decision, or an opted-out repo holding work for
its deliberate release. Route each line; never resolve a rejection by force,
and never push an opted-out repo yourself (`git-workflow.md` → The Outbound
Rules). This step reads git, not the session — it runs even when nothing was
harvested. *(A review-loop finding: every other session-end surface — the
git-workflow kernel, orchestration's hook 4, the bound prompt's declared
outputs, the command template — carried this step while the owning spec's
ritual stopped one step early.)*

---

## Insight Lifecycle Management

The lifecycle table above defines the *states* (`active` / `promoted` / `dismissed`); this section defines how an insight *moves* between them, because states without a driver silently accumulate. An insight is a thing, so its management is the thing-level cohesion discipline applied — not a mechanism special to insights.

**Promotion and dismissal are driven, not incidental.** Left alone, an `active` insight is never reckoned with. The driver is twofold: the **retrospective**'s insight-triage beat at period cadence (`retrospective.md` → What A Retrospective Produces), and the **end-session** disposition pass at session cadence (so per-session capture does not outrun retirement). Each walks the standing backlog and forces each `active` insight to a disposition — promote (populate `promoted_to`), dismiss, consolidate, or keep-active-with-a-stated-reason. Promotion is also a belief-revision trigger: a promoted insight's assertions stop being provisional, so they are scanned against their neighbours (`belief-revision.md`).

**An active insight must stay in circulation, and circulation is a graph property.** "Live" is defined by **an inbound edge from a non-terminal thing** — something still in play points back to the insight. An `active` insight that nothing live points to is *orphaned*: it returns to no future session and is invisible to the session-start staleness check. The floor surfaces this as a `validate` Info finding ("active insight with no inbound edge from a live thing", the twin of the open-conflict check); triage is where it is reckoned with — linked from live work, or moved to a terminal status. An insight with only **outbound** edges has discharged itself into the things it informed — that is a promotion signal, not a defect (see the worked case: `agents-drop-mechanical-birth-steps-not-semantic-ones` → `orchestration.md`). This replaces the prior "presence in `continuity.md`" definition: file-presence liveness was brittle — a backward-log cleanup could orphan a standing insight — and is being dissolved (`dissolve-continuity-into-reconciliation`).

**The keep-active marker.** Some insights are genuinely live with no active dependant — *standing razors* the framework reasons by, and *parked* insights awaiting a trigger. These are kept live not by a prose mention but by a stated disposition the floor reads: `disposition: keep-active` + a one-line `disposition_reason`. The orphan check honours it (the insight is no longer flagged); a `keep-active` with no reason is itself nudged, because the reason is the reckoning. This is the deliberate counterpart to letting an insight go terminal — "I have considered this and it stays live, and here is why" — and it is what stops the orphan check from nagging about insights that have already been triaged.

**Consolidation is composition, not a bespoke merge.** As a domain accumulates, several insights commonly fragment a single idea — they are one responsibility wearing several files. Consolidate them per `thing.md` → The Inverse: Composition: fold into the cohesive survivor, redirect inbound links, and tombstone the rest as `dismissed` with `superseded-by` pointing at the survivor. Mechanical candidate detection — insights sharing two or more `linked_things` targets — runs at retrospective cadence; the merge judgement is the agent's, applied conservatively (relate, don't merge). This is *not* contradiction resolution: insights that genuinely disagree are a `conflict` (`belief-revision.md`), not folded together.

---

## Extraction Heuristic

**Preserve if:**
- It's a held view that will influence future decisions
- It's an unresolved tension that needs to return
- It was surprising or contradicted a prior assumption
- It's a hypothesis agreed on but not yet tested or acted on
- It's a question that blocks progress on something

**Do not preserve if:**
- It's a routine status update or procedural confirmation
- It's a decision already captured in a thing
- It's context that won't affect anything in the future
- It was raised and fully resolved in the same session

Capture stays lean — preserve only what a cold agent would thank you for. Git history has everything else.

---

## Initialising Session Memory In A Domain

Session memory needs **no special files** — `continuity.md` and `WORKLOG.md` are both
retired (v3.17). A new domain has session memory from its first commit:
- **Backward** (what was done) = the commit stream (`mdllm worklog` views it on demand).
- **Forward** (what's still live) = open-loop things + open conflicts, surfaced by the
  generated orient view (`mdllm session-start`).
- **Insights** = `type: insight` things, kept live by the graph (an inbound edge or a
  `disposition: keep-active` marker).

A domain still carrying a legacy `continuity.md` should dissolve it on refresh — the
same way the framework did (`dissolve-continuity-into-reconciliation`): backward → git,
forward → things, insights → graph.

---

## Relationship To Other Specs

- **thing.md** — `insight` and `continuity-brief` are framework-reserved types defined here. All other type mechanics (frontmatter, linking, triggers) are inherited from `thing.md` — including the cohesion discipline (decompose / compose) that governs insight consolidation (`thing.md` → The Inverse: Composition).
- **orchestration.md** — The `session-end-continuity` prompt is bound to the `session-end` hook point; it closes with a rich `session-end:` commit (the backward record is git — no WORKLOG file). It is an explicitly invoked prompt, not an automatic hook — the user or agent triggers it at session close.
- **write.thing.md** — Creating and updating insight things follows standard write operations. The session-end ritual is an extension of the write workflow.
- **git-workflow.md** — Insight things are committed following standard conventions. The session-end commit is the natural pairing of the `post-write:commit` hard hook.
