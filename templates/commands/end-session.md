---
description: End-of-session continuity ritual — deliberate, operator-invoked
---

Run the **session-end continuity ritual** for this domain — and only because the
operator chose to end here. This is deliberate by design: insights are harvested
when *you* judge the session worth it, never automatically. Follow
`{framework_root}/templates/prompts/session-end-continuity.md`:

1. Scan this session for insights worth preserving → create `type: insight` things.
2. **Disposition the standing insights (the brake):** run `python
   {framework_root}/tools/mdllm.py validate .` and act on every insight-disposition
   finding — promote, dismiss, consolidate, link from live work, or mark
   `disposition: keep-active` + a reason. Capture (step 1) grows the population; this
   prunes it, so the two stay balanced.
3. Detect contradictions introduced this session → create `type: conflict` things.
4. Update `continuity.md` — **forward** open threads only (liveness is graph-keyed;
   history lives in git/WORKLOG, not the brief).
5. Commit with a `session-end:` message, then regenerate the worklog:
   `python {framework_root}/tools/mdllm.py worklog --write`.

If the session has no domain-relevant changes worth harvesting, say so and stop —
not every session earns an insight.
