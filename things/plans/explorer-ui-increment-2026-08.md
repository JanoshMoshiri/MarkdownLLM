---
id: explorer-ui-increment-2026-08
type: plan
status: in-progress
version: 1.0
created: 2026-08-28
priority: high
tags: [explorer, ui, navigation, commits, memory, context, accessibility, release]
linked_things:
  - id: explorer-publication-readiness
    relation: complements
    notes: "The signing gate now waits on this increment: signing 0.2.0 bytes would sign code this plan replaces. Operator decision 2026-08-28 — UI first, sign once at the end."
  - id: explorer-publication-position
    relation: references
  - id: explorer-extraction-and-hosting
    relation: references
---

# Explorer UI increment (0.3.0)

The accepted 0.2.0 candidate is a working read-only Explorer whose interface
was specified before anyone lived in it. A first real week of operator use
produced a list of friction points, all of them structural rather than
cosmetic: three fixed regions that cannot yield to each other, a commit
history that shows commits but not what they changed, a memory list ordered
by an accident of the alphabet, and structural references rendered as raw
JSON the reader cannot follow.

This plan carries that increment whole. There is no minimum viable subset —
the operator asked for every item actioned, plus the quality-of-life residue
found along the way.

## Position at the start

- The current tree is the reviewed, accepted, evidence-sealed 0.2.0 candidate.
- `explorer-publication-readiness` is `blocked` at the signing gate only.
- **This increment invalidates that seal.** Thirty human UAT dispositions,
  the technical evidence trace and the unsigned candidate hash all describe
  a tree this plan replaces. Resealing happens once, at the end, against
  the final 0.3.0 source — not per phase.

## Decisions taken at the outset

Recorded rather than rediscovered mid-build:

1. **The substrate is labelled `MarkdownLLM`, not `Substrate`.** This
   contradicts `FR-EST-002` as written ("First source is labelled Substrate
   independent of folder name"). The requirement is amended, not bypassed:
   the substrate *is* the MarkdownLLM framework in every estate, so naming it
   is more informative than naming its role, and the group heading above it
   already carries the role.
2. **Commit files open as they were at that commit**, with changed lines
   highlighted green. Removed lines are not rendered. This is a real read-boundary
   extension — historical blob content does not come through the confined
   filesystem reader — and carries its own safety envelope (below).
3. **Historical blobs are raw-only.** Line highlighting is line-oriented, and
   raw display keeps the markdown renderer and its link resolver entirely out
   of the historical-content path. One less boundary to prove.
4. **Memory groups reverse to true Z→A**: Retrospectives, Insights, Decisions,
   Conflicts. Conflicts land last, not Decisions — stated so the order is
   chosen rather than discovered.
5. **Desktop collapse and the mobile overlay are separate mechanisms.** The
   existing `nav-open`/`context-open` body classes with `inert` are a modal
   overlay for narrow viewports. Desktop collapse is a grid-column change with
   no modality. Conflating them would trap focus on a desktop that has no
   dialog.

## Phase 1 — The shell yields

The three regions are fixed at `270px | 1fr | 250px` and nothing can give.

- [x] Left navigation collapses to a rail via a chevron control; `aria-expanded`
      carried, state persisted in `localStorage` beside the theme choice.
- [x] Right context panel collapses to the right via its own chevron, same
      contract.
- [x] Collapse is a desktop mechanism: no `role="dialog"`, no `aria-modal`, no
      focus trap, no `inert` siblings. The narrow-viewport overlay keeps all four.
- [x] Centre region gains a horizontal scroll container so wide content scrolls
      inside itself and the page body never scrolls sideways.
- [x] The mid-width band (roughly 900–1240px) squeezes the split view rather
      than dropping it: collection list narrows to a usable minimum before the
      layout stacks.
- [x] Both collapse controls reachable and operable by keyboard, with a visible
      focus ring in both themes.

## Phase 2 — Overview earns its commits

- [x] `Eligible files` metric relabels to `Files`. The DTO field
      `counts.eligible_files` is unchanged — this is a display label, and
      eligibility stays the normative term in the requirements.
- [x] Commit rows become activatable (button semantics, keyboard, focus ring).
- [x] Activating a commit opens the collection master/detail pattern already
      used by Skills and Memory: changed paths on the left, selected file on
      the right.
- [x] **Backend — file list.** New `CommitDetail` port + use case + route
      (`/api/v1/commit`). Adapter runs `diff-tree` against the first parent,
      renames off, so each path appears once with a plain add/modify/delete
      status. Merge commits read against first parent.
- [x] **Backend — historical content.** Blob read at `<sha>:<path>`, bounded by
      the same `file_bytes` limit as live reads, binary-sniffed and refused
      rather than rendered, returned raw.
- [x] **Backend — changed lines.** Unified-zero hunk headers give the added-line
      ranges on the new side directly; no diff body is parsed and no removed
      line is transported.
- [x] **Safety envelope.** The git argument allowlist currently admits only
      fixed templates. Admitting a path argument is the sharp edge of this
      phase: paths are validated through `RelativePath.parse` and the
      eligibility rules *before* reaching a git invocation, `--` terminates
      option parsing, and length is bounded. New mutation entries cover
      option-injection and boundary-escape attempts.
- [x] Deleted paths list with their status and state plainly that the file was
      deleted in this commit, instead of failing to load.
- [x] Green highlighting is not carried by colour alone — a gutter marker keeps
      it readable under colour-independence review.

## Phase 3 — Memory reads the way it is used

- [x] Group order reverses to Z→A in the collection reader's sort. The
      pagination revision hash is computed from the ordered candidate list, so
      the cursor contract stays coherent.
- [x] Each group heading becomes a collapsible section with a chevron and
      `aria-expanded`.
- [x] Collapse state survives re-render and pagination — loading more into a
      collapsed group must not silently expand it, and must not hide newly
      appended items with no indication.

## Phase 4 — The document and its context

- [x] Raw view drops the frontmatter disclosure entirely. The header is already
      on screen in raw; the fold is duplication. Styled view keeps it.
- [x] Structural references become navigable. `informed_by`, `linked_things`,
      `dependencies`, `parent`, `blocks` and `definition` render as labelled
      chips rather than JSON, each activating to open the referenced thing.
- [x] **Backend — id resolution.** References carry thing *ids*, not paths, and
      point outside the memory collection (plans, artifacts, specs). A bounded
      id→path index over the source, built with the same scan limits as the
      collection reader, resolves them in one request rather than one per chip.
- [x] Unresolvable ids render as inert chips that say so, never as dead controls.
- [x] Context panel stops silently truncating frontmatter at twelve entries.
- [x] Long values stop breaking one character per line in the narrow panel —
      the current `overflow-wrap: anywhere` against a too-narrow column is what
      turns a path into a vertical stack of letters.

## Phase 5 — Quality-of-life residue

Found while reading, not requested — actioned under the operator's standing
instruction to fix what is noticed.

- [x] Commit timestamps render unambiguously rather than in ambiguous
      month/day order.
- [x] The `.mobile-only` class name stops describing the collapse controls once
      they exist at desktop; naming follows behaviour.
- [x] `renderDocument` shadows the global `document` with its parameter; it
      works only because the body reaches for `window.document`. Renamed.
- [x] Commit SHA abbreviation is quadratic in page size — bounded rewrite while
      the code is open.
- [x] Every new control audited for role, name, state, focus order and target
      size, in both themes and at 200% zoom.

## Phase 6 — Governance reconciliation

Docs and tests move with each phase; evidence reseals once.

- [x] `docs/requirements.md` — amend `FR-EST-002`; add functional requirements
      for region collapse, commit detail, historical read, reference navigation
      and memory section state; add the historical-read safety requirement.
- [x] `docs/design.md` — new endpoints, the collapse mechanism and its
      separation from the overlay, the historical-read boundary.
- [x] `docs/test-specification.md` — new and amended CT/BT/ST identifiers and
      mutation matrix entries.
- [x] `tests/traceability.yaml` — new rows; existing rows whose dispositions
      this increment invalidates are reopened rather than left reading as passed.
- [x] Test suites extended alongside each phase, not after all of them.
- [x] Technical evidence re-run at 0.3.0: pytest 144, mutation 21/21, adapter
      swap, immutability, performance 5/5 budgets, clean offline install.
- [x] The Windows lifecycle record describes 0.2.0 bytes and was never exercised
      on this source. Re-stamping it with the new subject hash would assert an
      observation nobody made, so it is retained under a superseded name where
      it carries no evidence, and the seven requirements resting on it are
      reopened as owed at the signed build.
- [x] The public demo estate now carries structural references, so the reference
      feature has a fictional fixture to be demonstrated and evidenced against —
      including one cross-domain reference that legitimately does not resolve.
- [x] Public user guide describes region collapse, commit contents, historical
      reading and reference navigation.
- [ ] Browser evidence re-executed and recorded against the final subject.
- [ ] Evidence index resealed; `verify_evidence` run and its result reported
      honestly, including what it reports as unmet.
- [ ] Operator re-dispositions the affected acceptance journeys (19 reopened).

## Phase 7 — Version and handback

- [x] Version to 0.3.0 across pyproject, package, packaging and the install
      oracle.
- [ ] Changelog and the framework version decision — deferred to the signed
      release boundary by `explorer-publication-readiness`, and the operator's.
- [ ] Rebuild the unsigned candidate from final source; record its hash.
- [ ] Hand the signing gate back to `explorer-publication-readiness` — the
      credentials and timestamp service remain the operator's to supply, and
      that plan closes on the signed bytes.

## Found while building, not while planning

Three defects in my own work that the plan did not anticipate, recorded because
each is a class rather than an incident:

1. **Duplicate mutant identities.** M15–M19 were appended to a manifest that
   already held M15 and M16; YAML last-key-wins hid the originals. Appending to
   a keyed manifest without reading it is the same mistake as restating an enum.
2. **A mutant that stopped testing its claim.** M07's anchor string became
   ambiguous when a new encoder branch introduced a second occurrence, silently
   retargeting the mutation at a branch its oracle does not cover. A mutation
   anchor is a coupling to source text, and it decays without saying so.
3. **A field used for two purposes.** Recording evidence invalidation by
   overwriting `disposition` conflated *how a requirement is verified* with
   *whether its evidence still stands*. The reopening needed its own field.

## What would make this plan wrong

- If historical blob reading proves to need more boundary surface than the
  safety envelope in Phase 2 can cover, decision 2 gets revisited and the
  commit view degrades to current-file-with-status rather than growing an
  unproven read path.
- If reference resolution at estate scale is slower than a single bounded scan
  allows, the id→path index becomes a derived artefact rather than a live read.
