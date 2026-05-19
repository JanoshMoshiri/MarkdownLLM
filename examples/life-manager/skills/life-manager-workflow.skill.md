---
id: life-manager-workflow-skill
name: Life Manager Workflow
type: skill
mode: workflow
status: stable
version: 2.0
created: 2026-05-18
linked_things:
  - id: life-manager-specification
    relation: implements
  - id: life-manager-read-thing-skill
    relation: orchestrates
  - id: life-manager-write-thing-skill
    relation: orchestrates
description: Process orchestration and execution patterns for life management
applies_to: "life-manager/**/*.md"
---

# Life Manager Workflow

## Primary Process: The Life Management Loop

Your life management operates in a continuous loop of planning, execution, review, and adaptation:

### Phase 1: Capture
What you're thinking about. New ideas, goals, obligations, thoughts.

- Create new things to capture what's on your mind
- Link them to existing things if they relate
- Set initial status and priority

### Phase 2: Clarify
Understanding what you've captured. What is this thing really? Why does it matter?

- Flesh out the narrative body with full context
- Create dependencies if this thing blocks or is blocked by others
- Set realistic scope (is this one thing or multiple things?)
- Link to relevant goals

### Phase 3: Commit
Deciding what you're actually going to do right now vs. later.

- Move thing from `status: planning` to `status: in-progress`
- Update due dates if you're committing to a timeline
- Link to calendar and notification systems

### Phase 4: Execute
Doing the work. Claude supports you with status updates, blockers, insights.

- Update thing narrative as you work
- Mark related tasks complete as you finish them
- Mark things blocked if you hit an obstacle
- Flag when you need help or clarification

### Phase 5: Review
Reflecting on what you've done and what's next.

- Mark things complete once finished
- Review what got blocked and why
- Identify patterns or learnings
- Look at updated priorities and dependencies

### Phase 6: Abandon/Defer
Acknowledging what you're not doing.

- Mark things `status: paused` if you're taking a break
- Mark things `status: cancelled` if you're not doing them
- Archive things that no longer apply
- This is healthy; not everything survives contact with reality

## Sub-Processes

### Weekly Review
Every week, step back and assess:

1. What did you complete? (Mark those things done)
2. What's blocked? (Update blocker status)
3. What's at risk? (Identify things at risk of falling off timeline)
4. What's next? (What should you focus on next week?)
5. What changed? (Did priorities shift? Goals change?)

**Trigger:** Fixed time each week (Sunday evening, Monday morning, etc.)

**Things involved:** All active projects and tasks

**Output:** Updated priorities, new blockers identified, clear next steps

### Quarterly Review
Every quarter, zoom out completely:

1. Did you achieve your quarterly goals? (Mark them achieved or deferred)
2. What worked? What didn't? (Patterns and learnings)
3. New quarter, new goals? (Create new goal things)
4. Portfolio changed? (Did you abandon projects? Start new ones?)
5. What's next? (Plan the next quarter at high level)

**Trigger:** At end of each quarter

**Things involved:** All goal things, all project things

**Output:** Quarter marked complete, new goals set, portfolio adjusted

## Decision Points

### Should I Create One Thing or Multiple?

**Create one thing if:**
- It can realistically be completed without subtasks
- It doesn't have clear phases or stages
- It's atomic and can't be meaningfully broken down

**Create multiple things if:**
- You can think of clear subtasks or phases
- Different parts might get blocked independently
- Different people or teams might be involved

### Should I Update or Create New?

**Update an existing thing if:**
- Something about it changed but the core thing is still the same
- You're making progress toward what was already defined
- The update is incremental

**Create a new thing if:**
- The scope has changed so much it's effectively a different thing
- You're pivoting direction significantly
- You're adding something entirely new

### When Should I Mark Something Done?

**Mark complete when:**
- All success criteria are met
- All linked deliverables are done
- You've reviewed and accepted the result

**Mark paused when:**
- You're not currently working on it but might return
- You're waiting for dependencies to be resolved
- You're intentionally stepping away temporarily

**Mark cancelled when:**
- You've decided not to do this and won't return to it
- Circumstances changed and it's no longer relevant
- You're deprioritizing it permanently

## Failure Modes and Recovery

### Problem: Too Much in Progress
**Signal:** More than 3-4 things marked `in-progress`

**Recovery:**
- Pause unnecessary things—move to `paused`
- Prioritize ruthlessly—what's actually urgent?
- Complete and close things to reduce cognitive load

### Problem: Long Blocked Chain
**Signal:** Multiple things blocked on same dependency

**Recovery:**
- Urgently unblock the root thing
- Or accept you won't work on dependent things and mark them paused
- Communicate blockers clearly so they don't surprise you

### Problem: Abandoned Thing (Ghost Projects)
**Signal:** Thing in `in-progress` for weeks with no updates

**Recovery:**
- Honest assessment: will you really finish this?
- If yes: identify the actual blocker and fix it or accept help
- If no: mark paused or cancelled and let it go

### Problem: Unrealistic Timeline
**Signal:** Multiple things due at same time, conflicting priorities

**Recovery:**
- Renegotiate timelines explicitly
- Defer non-critical things
- Ask for help to parallelize work
- Accept that some things will slide

## Integration with the Agent

When you make a request in Life Manager:

1. **Parse your intent:** Are you asking for insight (read mode) or making a change (write mode)?
2. **Load context:** Read relevant things from your `things/` directory
3. **Evaluate triggers:** Check for fired triggers (overdue, unblocked, threshold exceeded)
4. **Reason within the workflow:** Where are you in the loop? What phase applies?
5. **Recommend or execute:** Suggest what you should do next, or make updates if you've explicitly asked
6. **Validate:** After writes, run structural and referential checks
7. **Commit:** Persist changes with structured commit messages
8. **Report:** Tell you what changed and why, including any triggers that fired

## Trigger Integration

### Session Start Triggers
When the agent starts a session, evaluate:
- **Time-based:** Are any things overdue? What's due within 2 days? Is it weekly review day?
- **Dependency:** Did anything complete since last session that unblocks other things?
- **Threshold:** Are more than 5 things in-progress? Are any things stale (14+ days without update)?

Report triggered conditions before processing user request.

### Post-Write Triggers
After any write:
- Did completing a thing unblock dependents? → Notify user
- Did creating new things push in-progress above threshold? → Warn
- Did a status change cascade to related things? → Report

## Git Commit Points

Natural commit moments in the life management workflow:

- After capture (Phase 1): `create: [thing-id]`
- After clarify (Phase 2): `update: [thing-id] narrative`
- After commit/execute (Phase 3-4): `update: [thing-id] status`
- After review (Phase 5): `complete: [thing-id]` or `batch: weekly-review`
- After abandon/defer (Phase 6): `archive: [thing-id]`

Each commit represents one logical change to your life's state.

**Example flows:**

- **"What should I focus on?"** → Read all active things, analyze workflow phase, recommend priorities
- **"I finished X"** → Move X to complete, load all things blocked on X, unblock them, tell you what's now possible
- **"I'm blocked on Y"** → Create dependency thing, mark dependent things blocked, help you unblock Y or defer dependents
- **"Review my week"** → Run weekly review workflow, show you what you accomplished, what changed, what's next
