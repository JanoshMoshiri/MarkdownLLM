---
id: a-session-harvest-must-read-the-commit-stream
type: insight
status: active
version: 1.0
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "A standing session-end rule for long and multi-harness work; no single active plan owns it, and every future harvest can apply it."
tags: [session-memory, git, compaction, harvest, multi-agent]
linked_things:
  - id: session-memory-specification
    relation: informs
    notes: "The extraction ritual names the commit stream as the backward record but does not yet require the insight scan to read it."
  - id: long-running-tasks-lack-pre-compaction-checkpoint
    relation: complements
    notes: "That insight protects uncommitted reasoning during compaction; this one recovers already-committed learning that surviving context no longer represents."
  - id: a-shared-worktree-merges-authorship-at-the-index
    relation: complements
    notes: "In multi-harness work the commit stream may contain valid intermediate harvests from another seat, so the final account must inspect and attribute rather than ignore them."
---

# A Session Harvest Must Read The Commit Stream

A long Codex conversation carried the vendor-adapter work across many days,
handoffs, compactions, live probes, and intermediate Claude session-end
commits. At its final close, the surviving context was dominated by the last
Gate 6 handoff and the per-domain trust walk. Reading only that tail produced
the conclusion that there was no new insight to harvest.

The commit stream disproved the account immediately. The same logical work
had already created seventeen insight things since the adapter effort began,
including the cross-seat boundary rule, the harness-bound side-effect rule,
the two-budget failure, the shared-index contention finding, and the injected
frontmatter boundary. The learning was safe on disk; the final narration was
wrong because it treated remaining context as the session.

The harvest therefore has two evidence sources with different jobs:

- **Surviving conversational context** carries uncommitted reframings and
  questions that have not yet become things.
- **The commit stream** carries what the session already made real, including
  intermediate harvests, decisions, evidence records, and work performed by
  another harness in the same logical undertaking.

Neither substitutes for the other. Context alone forgets after compaction;
git alone cannot contain an idea that was discussed but never written.

The rule is simple: before stating what a long session learned, inspect the
relevant commit range and then scan the remaining context for residue. If the
commit range already contains the lessons, report **"no additional insight"
rather than "no insight."** In multi-harness work, attribute the commits to
their seats, but do not confuse a change of author or an intermediate
`session-end:` delimiter with an absence from the operator's larger session.
