---
id: continuity-briefs-solve-external-state-drift
type: insight
status: active
version: 1.0
created: 2026-06-05
session: 2026-06-05
source: both
confidence: high
origin: synthesised
linked_things:
  - id: session-memory-specification
    relation: informs
  - id: orchestration-specification
    relation: informs
---

# Continuity Briefs Solve External State Drift — The Framework Has None

The value of a continuity brief is proportional to how much real-world state changes between sessions *outside the agent's control*. Domains like eco-essentials have high external state drift: Amazon approval comes through, suppliers respond, DNS propagates. Things change while the agent is not running, and a continuity brief answers "what is live *right now*" without requiring the agent to infer it from session history.

The framework has no such external state. Nothing changes in the framework between sessions except what the agent does. The framework's state *is* the git history. WORKLOG + REVIEWLOG + AGENTS.md already serve the continuity purpose: the WORKLOG's most recent entry captures open threads, the REVIEWLOG tracks what's fixed vs. open, and AGENTS.md is comprehensive enough to orient any session cold.

A framework continuity.md would therefore duplicate what already exists, adding maintenance overhead with no equivalent benefit. The pattern should not be applied reflexively just because domains use it.

**The signal to create a framework continuity.md:** new framework sessions are consistently losing context — the agent is missing important open threads despite reading WORKLOG and REVIEWLOG. That signal has not appeared. Until it does, defer.

**Generalised heuristic:** Before creating a continuity brief for any domain, ask: "Does this domain have real-world state that changes between sessions?" If no, the WORKLOG is sufficient.
