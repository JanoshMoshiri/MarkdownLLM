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
  - name: continuity-brief
    description: "The domain's current continuity.md (if it exists)"
outputs:
  - name: new-insights
    description: "type: insight things created in things/insights/"
  - name: new-conflicts
    description: "type: conflict things created in things/conflicts/ (if contradictions found)"
  - name: updated-continuity-brief
    description: "Updated continuity.md with new threads, resolved threads removed"
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

### 3. Check For Contradictions

Scan for contradictions introduced this session:
- Did any new insight or modification assert something that conflicts with an existing thing?
- Do any two things now in view hold incompatible positions?

For each contradiction found:
- **If resolvable in-session** (one position clearly supersedes): update relevant things, declare `relation: supersedes`, mark old position deprecated if appropriate.
- **If not resolvable**: create a `type: conflict` thing in `things/conflicts/`, add `relation: contradicts` to both parties, and add the conflict to the continuity brief.

Be conservative — only flag genuine semantic contradictions, not differences in emphasis or scope.

### 4. Update The Continuity Brief

Load `continuity.md`. Update:
- Add new open threads from this session
- Remove threads that resolved this session
- Add new live insight IDs (with one-line summaries)
- Remove insights that were promoted or dismissed
- Update pending decisions
- Add any new open conflicts as open threads
- Refresh the questions list

If no `continuity.md` exists, create one using `templates/continuity-brief.md.template`.

### 5. Commit, Then Regenerate The WORKLOG

Commit all new insight things, conflict things, and the updated continuity brief
following `git-workflow.md` conventions — including a `session-end:` commit, which
is the delimiter `mdllm worklog` splits sessions on.

Then regenerate the WORKLOG as a closing **mechanical** step — it is not reasoning,
it is a generated artifact derived from the commit stream:

```sh
mdllm worklog --write   # rewrites WORKLOG.md in place from HEAD; never hand-edit
```

Commit the regenerated `WORKLOG.md`. The system name and id are read from the
local `AGENTS.md`, so the same command is correct in the framework and in any
domain repo. The WORKLOG records what *happened* (history); the continuity brief
above carries what's still *live* (state) — do not duplicate one into the other.

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
