---
id: session-end-continuity
type: prompt
status: stable
version: 1.0
created: 2026-05-28
inputs:
  - name: session-conversation
    description: "The full session dialogue — questions asked, positions taken, decisions made, tensions surfaced"
  - name: existing-insights
    description: "Current active insights in things/insights/"
  - name: existing-things
    description: "Domain things that may be contradicted by session content"
  - name: open-loops
    description: "Non-terminal work things (plans, tasks) the session may open or close"
outputs:
  - name: new-insights
    description: "type: insight things created in things/insights/"
  - name: new-conflicts
    description: "type: conflict things created in things/conflicts/ (if contradictions found)"
  - name: updated-open-loops
    description: "Open-loop things created or moved to a terminal status this session"
bound_to:
  - hook: session-end
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: session-memory-specification
    relation: implements
  - id: belief-revision-specification
    relation: implements
---

# Session-End Continuity

## Purpose

At the end of a session, extract generative knowledge — emerging ideas, held views, unresolved tensions, open questions — and preserve it for future sessions. Without this step, every session starts cold.

## Reasoning Template

### 1. Scan For Insights

Review the session for:
- Non-obvious positions taken by either party
- Hypotheses agreed on but not acted on
- Questions raised but not answered
- Tensions identified but not resolved
- Reframings that changed how something is understood

Apply the **preservation test**: *Would a fresh agent starting this domain cold benefit from knowing this?* If yes, preserve. If routine, procedural, or already captured in a thing, skip.

### 2. Create Insight Things

For each insight worth preserving, create a `type: insight` thing in `things/insights/` following the structure defined in `session-memory.md`:

```yaml
---
id: [descriptive-kebab-case-id]
type: insight
status: active
version: 1.0
created: [ISO-date]
session: [YYYY-MM-DD]
source: human|agent|both
confidence: high|medium|low
origin: stated|inferred|synthesised
linked_things:
  - id: [related-thing-id]
    relation: informs|challenges|supports
---
```

### 3. Disposition The Standing Insights (the brake)

Capture (step 2) grows the insight population every session; this step prunes it, so
the two stay in balance — every act of capture is paired with an act of pruning.

Run `python {framework_root}/tools/mdllm.py validate <domain>` and act on **every
insight-disposition Info finding** the floor surfaces:
- *"active insight with no inbound edge from a live thing"* — force a disposition:
  **promote** (populate `promoted_to`; the insight's lesson has crystallised into a
  spec/decision/thing), **dismiss** (considered, set aside), **consolidate** (fold a
  genuine duplicate into a survivor), **link** it from live work (it has a real active
  dependant), or **mark `disposition: keep-active`** with a one-line `disposition_reason`
  (a standing razor or parked insight, deliberately kept).
- *"insight marked keep-active but has no `disposition_reason`"* — add the reason or
  re-disposition.

This is a **forcing function, not a corpus sweep**: the floor already lists exactly the
insights that need a decision, so none can quietly go dark. The deeper period-scoped
work (composition/consolidation, conflict + schema scans) stays the retrospective's.

### 4. Check For Contradictions

Scan for contradictions introduced this session:
- Did any new insight or modification assert something that conflicts with an existing thing?
- Do any two things now in view hold incompatible positions?

For each contradiction found:
- **If resolvable in-session** (one position clearly supersedes): update relevant things, declare `relation: supersedes`, mark old position deprecated if appropriate.
- **If not resolvable**: create a `type: conflict` thing in `things/conflicts/`, add `relation: contradicts` to both parties — an open conflict is an open loop, surfaced by orient.

Be conservative — only flag genuine semantic contradictions, not differences in emphasis or scope.

### 5. Update The Open Loops (Forward State Is Things, Not A Brief)

Forward state lives in the **thing graph**, not a hand-maintained brief
(`continuity.md` is retired — `orient-and-reconciliation-are-the-corpus-two-sides`).
The session-start orientation generates the forward view from it (`mdllm
session-start` → "Open loops"). So at session end:
- **New forward intent this session** → create or update an open-loop thing (a
  `plan` or domain work thing) at a non-terminal status. A loop worth carrying is a
  thing, so it is tracked, surfaced by orient, and *retired by status* when done.
- **Resolved this session** → move the relevant thing to a terminal status so orient
  stops surfacing it.
- **New contradictions** → the `conflict` things from step 4 are open loops already.

Do **not** maintain a continuity brief, list insight IDs, or write a backward
"decisions made" log — insight liveness is graph-keyed (step 3) and history lives in
the commit stream.

### 6. Commit

Commit all new insight things, conflict things, and updated open-loop things
following `git-workflow.md` conventions — including a `session-end:` commit, which is
the delimiter `mdllm worklog` groups sessions on. **Write a rich commit message:** the
commit *is* the backward record now — there is no WORKLOG file to regenerate (retired
in v3.17; `mdllm worklog` prints an on-demand view of the commit stream when you want
it). History lives in git and nowhere else.

## Extraction Heuristic

**Preserve if:**
- It's a held view that will influence future decisions
- It's an unresolved tension that needs to return
- It was surprising or contradicted a prior assumption
- It's a hypothesis agreed on but not yet tested
- It's a question that blocks progress on something

**Do not preserve if:**
- It's a routine status update or procedural confirmation
- It's a decision already captured in a thing
- It's context that won't affect anything in the future
- It was raised and fully resolved in the same session
