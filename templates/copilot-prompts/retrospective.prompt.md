---
mode: agent
description: Periodic domain retrospective + reflexive conflict/schema sweep — operator-invoked
---

Write a `type: retrospective` thing for this domain (periodic quality reflection;
see `{framework_root}/retrospective.md`), then run the two reflexive prompts:

1. `detect-conflicts` (scan mode) — sweep every `linked_things` edge across the
   domain for contradictions; `{framework_root}/templates/prompts/detect-conflicts.md`.
2. `review-schema-coherence` — audit the emergent frontmatter vocabulary for fields
   that have drifted apart in name but converged in meaning;
   `{framework_root}/templates/prompts/review-schema-coherence.md`.

Commit the retrospective and any `type: conflict` things surfaced.
