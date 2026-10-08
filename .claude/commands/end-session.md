---
description: End-of-session continuity ritual — deliberate, operator-invoked
---

Run the **session-end continuity ritual** for this domain — and only because the
operator chose to end here. This is deliberate by design: insights are harvested
when *you* judge the session worth it, never automatically. Follow
`{framework_root}/templates/prompts/session-end-continuity.md`:

1. Scan this session for insights worth preserving → create `type: insight` things.
2. **The close — reckon what the workspace carries (the brake):** run
   `python {framework_root}/tools/mdllm.py reckon . --close --apply`. The floor
   applies the mechanical band and lists what this close owes, oldest first:
   the residue (at most four) goes to the operator in one native choice prompt,
   *not now* among the options and recorded as a hold; the settled items you
   decide by citing the record — insights: promote, dismiss, consolidate, link
   or hold; conflicts: rule, link or hold; cues: walk or answer by citation;
   fired triggers: act, re-date or disarm; work: start, unblock, pause or hold;
   workflows: write or bind. A hold is `mdllm reckon . --keep <id> --reason "…"`.
   Raise a cue for any reasoned-from thing you modified that no cue covers. The
   commit gate refuses the `session-end:` commit until the close is met — ten
   decisions today while a backlog stands, or the band emptied; an unattended
   session applies the mechanical band and drafts the rest, never answers.
3. Detect contradictions introduced this session → create `type: conflict` things.
4. Manage **open-loop things** — create/update a `plan` or work thing for new forward
   intent, move resolved ones to a terminal status (orient reads them; `continuity.md`
   is retired).
5. Commit with a rich `session-end:` message — the commit *is* the backward record
   (no WORKLOG file; `mdllm worklog` prints an on-demand view of git when wanted).
6. **Report publication debt:** run `python {framework_root}/tools/mdllm.py
   estate-sync . --status` and surface the result. Under literal
   `git.autopush: true`, `ahead +n (unpushed)` is an anomaly — an offline session
   or rejected push owed a routing decision. Under false, absent, or malformed
   policy it is expected debt awaiting a human-authorized push. Route each line;
   never resolve a rejection by force and never infer send authority from silence
   (git-workflow.md → The Outbound Rules;
   `autopush-requires-explicit-authority`).

If the session has no domain-relevant changes worth harvesting, say so and stop —
not every session earns an insight (publication debt still gets reported: step 6
reads git, not the session).
