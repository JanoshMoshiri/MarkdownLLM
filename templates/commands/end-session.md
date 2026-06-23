---
description: End-of-session continuity ritual — deliberate, operator-invoked
---

Run the **session-end continuity ritual** for this domain — and only because the
operator chose to end here. This is deliberate by design: insights are harvested
when *you* judge the session worth it, never automatically. Follow
`{framework_root}/templates/prompts/session-end-continuity.md`:

1. Scan this session for insights worth preserving → create `type: insight` things.
2. Detect contradictions introduced this session → create `type: conflict` things.
3. Update `continuity.md` (open threads, pending decisions, mid-flight position).
4. Commit with a `session-end:` message, then regenerate the worklog:
   `python {framework_root}/tools/mdllm.py worklog --write`.

If the session has no domain-relevant changes worth harvesting, say so and stop —
not every session earns an insight.
