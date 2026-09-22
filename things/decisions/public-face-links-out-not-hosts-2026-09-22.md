---
id: public-face-links-out-not-hosts-2026-09-22
type: decision
status: made
version: 1.0
created: 2026-09-22
session: 2026-09-22
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [documentation, publication, pages, selector, visibility, readme]
informed_by:
  - id: public-docs-face-is-derived-not-restated
    commit: 35aae16b2c185b6aa2d63c20d8eabae8d9432f28
  - id: public-docs-face-build
    commit: cdcdb36442c992692b684721050062c51930cc8c
linked_things:
  - id: public-docs-face-is-derived-not-restated
    relation: extends
    notes: "That ruling left the selector undecided — `docs/` as the working answer until something outside it wanted publishing. Something did (ten links), and this settles it without widening."
  - id: public-docs-face-build
    relation: informs
    notes: "Phase 3's three answers, weighed here; answer 1 taken, with the link-out mechanism the plan had not named. Phase 2's README link, made a must."
---

# Decision: The Public Face Links Out to the Repository — It Hosts No Duplicate

## Context

The docs site went live on 2026-09-22 ([[public-docs-face-build]] Phase 2:
`docs/` on `main`, GitHub Pages). The build's first honest count was ten links
from `docs/` that reach outside it — `README.md`, `kernel.md`, `thing.md`, one
insight, and the Explorer's own docs — none of which resolve on a site whose
selector is `docs/` alone. [[public-docs-face-is-derived-not-restated]] had
parked the selector question as "only real once something outside `docs/`
wants publishing." It was real on the first build.

The plan offered three answers: (1) `docs/` stands and the root specs stay on
the blob view; (2) the selector widens to a named set including the Tier-1 and
Tier-2 specs; (3) a per-thing public marker is earned, distinct from `exposed`.

## The Ruling

The operator, on seeing the live site and the count:

> "I think the live site should take you to the files but back to the GitHub
> page so we don't need to host duplicates. Also I want this live site to be
> linked from the readme file. I think that is a must."

**Answer 1, with a mechanism the plan had not named: the site links out.** A
link that leaves `docs/` is resolved, on the site, to the repository's own
page for that file at `main`. The documents keep the relative links that work
in the repository; the site derives the destination at view time from the
repository name it already carries. Nothing is rewritten in the source, and
nothing outside `docs/` is rendered twice.

And the README carries the site's address — at the top, and where it lists
the human-facing documents — so the repository's front page and the site's
front door point at each other.

## Why This and Not the Others

- **Widening the selector (2)** would render the 48KB specifications a second
  time, on a surface the ruling's own accessibility section says cannot fix
  their size. The repository already renders them, with history, blame and
  the exact commit. Duplicating a rendering is the restatement the whole
  plan exists to end — in a different medium.
- **A per-thing marker (3)** invents a vocabulary for an axis
  ([[scaffold-declares-visibility]]) whose only present consumer is the
  site, and the site now needs no marker: the boundary is the directory, and
  everything on the far side of it has one canonical page already.
- **Answer 1 as originally stated** left ten dead links. The link-out is what
  makes it hold: the reader is taken to the file, not to a 404.

## What It Costs

A reader who follows a link out of the site lands on GitHub's blob view — the
surface whose lack of nav and search motivated the site. That is accepted
deliberately: those files are the agent's specifications, and the human
document for each of them is the site's job ([[public-docs-face-build]] Phase
4, the digest question), not a second copy of the spec.

## Consequences

- `docs/_includes/head_custom.html` resolves outward links at view time
  (`data-leaves-site="repository"` marks each, so a stylesheet or a check can
  find them). Pins to `main`, not the build commit: Pages rebuilds on every
  push, so the site is always the current `main`, and so are its links.
- `README.md` links the site twice, as stated above.
- [[public-docs-face-build]] Phase 3 closes on this record. Phase 4 — the
  size-and-entry gap — is the question that remains, and it is sharper now:
  the site cannot host the specs, so the human digest is the only door left
  to build.
