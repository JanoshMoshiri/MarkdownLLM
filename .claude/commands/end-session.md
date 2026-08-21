---
description: End-of-session continuity ritual — deliberate, operator-invoked
---

Run the **session-end continuity ritual** for this domain — and only because the
operator chose to end here. This is deliberate by design: insights are harvested
when *you* judge the session worth it, never automatically. Follow
`templates/prompts/session-end-continuity.md`:

1. Scan this session for insights worth preserving → create `type: insight` things.
2. **Disposition the standing insights (the brake):** run `python tools/mdllm.py
   validate .` and act on every insight-disposition finding — promote, dismiss,
   consolidate, link from live work, or mark `disposition: keep-active` + a reason.
   Capture (step 1) grows the population; this prunes it, so the two stay balanced.
3. Detect contradictions introduced this session → create `type: conflict` things.
4. Manage **open-loop things** — create/update a `plan` or work thing for new forward
   intent, move resolved ones to a terminal status (orient reads them; `continuity.md`
   is retired).
5. Commit with a rich `session-end:` message — the commit *is* the backward record
   (no WORKLOG file; `mdllm worklog` prints an on-demand view of git when wanted).
6. **Report publication debt:** run `python tools/mdllm.py estate-sync . --status`
   and surface the result. Autopush is **fail-closed**: only a repo declaring
   literal `git: autopush: true` publishes after commit — false, absent, or
   malformed policy is off, and publication authority never comes from
   silence. In an opted-out repo, `ahead +n (unpushed)` is the normal
   standing state of work awaiting its deliberate release — report it, never
   resolve it. Only under *explicitly enabled* autopush is an unpushed line
   an anomaly (offline session, or a rejected push owed a routing decision).
   Never resolve a rejection by force, and never push an opted-out repo
   yourself (git-workflow.md → Publication;
   `autopush-requires-explicit-authority`).

If the session has no domain-relevant changes worth harvesting, say so and stop —
not every session earns an insight (publication debt still gets reported: step 6
reads git, not the session).
