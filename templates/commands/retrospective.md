---
description: Periodic domain retrospective + reflexive conflict/schema/skill sweep — operator-invoked
---

Write a `type: retrospective` thing for this domain (periodic quality reflection;
see `{framework_root}/retrospective.md`), then run the three reflexive prompts:

1. `detect-conflicts` (scan mode) — sweep every `linked_things` edge across the
   domain for contradictions; `{framework_root}/templates/prompts/detect-conflicts.md`.
2. `review-schema-coherence` — audit the emergent frontmatter vocabulary for fields
   that have drifted apart in name but converged in meaning;
   `{framework_root}/templates/prompts/review-schema-coherence.md`.
3. `review-skill-coherence` — read the skills and the entry file against
   the commit stream since the last retrospective and force a per-skill
   disposition (confirm-current / update / park / retire);
   `{framework_root}/templates/prompts/review-skill-coherence.md`.

Commit the retrospective, any `type: conflict` things surfaced, and the
skill edits the dispositions imply.
