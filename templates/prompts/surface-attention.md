---
id: surface-attention
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: fired-triggers
    description: "Output from evaluate-triggers prompt — triggers whose conditions are true"
  - name: orientation-context
    description: "Output from session-orientation — current state awareness"
  - name: user-request
    description: "What the user asked for (if anything specific)"
outputs:
  - name: attention-items
    description: "Prioritized list of things to bring to user's attention"
  - name: delivery-mode
    description: "How to deliver: proactive mention, inline note, or hold until asked"
bound_to:
  - hook: session-start
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: evaluate-triggers
    relation: consumes-output-of
  - id: session-orientation
    relation: consumes-output-of
---

# Surface Attention

## Purpose

Decide which things deserve the user's attention and how prominently to present them. This is the final filter between "the system noticed something" and "the user hears about it." Not everything that fires a trigger needs to interrupt the user.

## Reasoning Template

### 1. Gather Candidates

Collect all things that need attention from:
- Fired triggers (from `evaluate-triggers`)
- Overdue items (from `session-orientation`)
- Recently unblocked items
- Items approaching due dates

### 2. Prioritize

Rank candidates by urgency and importance:

| Signal | Weight |
|--------|--------|
| Priority: critical | Highest — always surface |
| Overdue + high priority | High — surface prominently |
| Recently unblocked (was waiting) | Medium — mention as opportunity |
| Approaching due date (< 3 days) | Medium — mention as reminder |
| Stale trigger fired | Low — mention if space allows |
| Informational (progress update) | Lowest — hold unless asked |

### 3. Determine Delivery Mode

Based on what the user is doing:

**User opened with a specific task request:**
- Critical/overdue items → Brief heads-up before addressing their request: "Quick note: X is overdue. Now, regarding your request..."
- Everything else → Hold. Don't interrupt focused work.

**User opened with general intent ("what's up", "catch me up"):**
- Top 3-5 items → Present as a prioritized summary
- Lower items → Available if they ask for more

**User didn't ask anything yet (session just started):**
- Critical only → Proactive mention
- Everything else → Wait for user to engage

### 4. Format for Delivery

When surfacing items:
- Lead with the *why* — "X is overdue" not "trigger fired on X"
- Include the *action* — "Should we reprioritize?" not just "FYI"
- Group related items — "3 things unblocked after you completed Y" not three separate mentions
- Be concise — One sentence per item unless the user asks for detail

## Anti-Patterns

- **Don't dump everything.** The user doesn't need to hear about 12 items at session start.
- **Don't repeat yourself.** If you mentioned something last session and nothing changed, don't mention it again at the same priority level.
- **Don't cry wolf.** Low-priority items surfaced too aggressively train the user to ignore the system.
- **Don't hide critical items.** A critical overdue item gets mentioned regardless of what the user asked about.
