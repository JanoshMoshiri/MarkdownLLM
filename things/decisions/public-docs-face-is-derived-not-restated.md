---
id: public-docs-face-is-derived-not-restated
type: decision
status: made
created: 2026-08-13
session: 2026-08-13
decided_by: human
confidence: high
linked_things:
  - id: scaffold-declares-visibility
    relation: informs
    notes: "Its 2026-08-04 ruling — visibility and authorisation are different axes — is the reason the public docs face cannot reuse `exposed`. A consumer domain is an authorised reader; the internet is not."
  - id: a-generated-surface-collapses-its-walk
    relation: informs
    notes: "The wiki's disqualifying cost stated in the framework's own terms: it adds a full restatement layer over 243 tracked files, and restatement count IS reconciliation cost."
  - id: premature-publish-manufactures-discipline-eroding-urgency
    relation: informs
    notes: "Why the surface is decided now but the content waits. Docs written from an in-flight plan publish an aspiration and then quietly correct it."
  - id: vendor-harness-adapter-foundation
    relation: references
    notes: "The immediate occasion. Its gates are the condition on writing adapter documentation — not on making this decision."
---

# The public docs face is derived, never restated

The operator ruled (2026-08-13) on how MarkdownLLM's documentation reaches
readers who are not holding a clone. Three parts, one principle: **anything a
reader sees is derived from tracked state inside the floor, or it does not
exist.**

## The GitHub Wiki is ruled out — on mechanism, not preference

The wiki was the operator's starting proposal and was withdrawn once its
mechanism was understood. GitHub's wiki is a **separate git repository**
(`MarkdownLLM.wiki.git`) with its own history. Content placed there sits:

- outside the pre-commit floor hook — no `validate`, no coherence check, no
  `candidates` cue;
- outside `.github/workflows/validate.yml`;
- outside `mdllm boundary` — and this is the one repo where the disclosure
  boundary is load-bearing, per [[scaffold-declares-visibility]];
- unreachable by every `mdllm` command.

So a wiki is not a view of the source of truth. It is a **second source of
truth by construction**, and it is the copy that sits outside every control the
framework built. The failure mode is not "we must remember to sync" — it is
that no mechanism *could* check the sync, because the checking apparatus does
not reach across the repo boundary.

## The surface is GitHub Pages from `/docs` on `main`

Same repo, same commit, same hook, same boundary check, same CI. The published
site is **derived** — regen reconciles it — rather than copied. That is the
distinction the framework already runs on, and it is the only publishing shape
that keeps the one-source-of-truth property the operator asked for as a
*structural* fact rather than a discipline.

## The public face is a distinct selector from `exposed`

The tempting move is to point a docs build at `exposed: true` and be done.
**Ruled against.** `exposed` means *another domain may rest on this* — and a
consuming domain is an **authorised** reader wired by the operator. The
internet is not.

[[scaffold-declares-visibility]] settled this axis on 2026-08-04, in the
withdrawal of the audited-repo premise: *"Visibility and authorisation are
different axes, and conflating them produces protection aimed at people who are
entitled to see."* Reusing one flag for both re-conflates exactly the two axes
that ruling separated, and it would do so on the repo where the cost of getting
it wrong is highest.

The two faces are also not the same set in fact. `docs/` holds five curated
human-facing files; `exposed: true` currently marks four things, all of them
machine-facing cross-domain material. They serve different consumers and were
selected by different judgement.

**What is not yet decided:** what the public selector actually *is* — whether
`docs/` as a directory is sufficient, or whether a per-thing marker is
eventually earned. Not forced today. `docs/` is the working answer and the
question is only real once something outside `docs/` wants publishing.

## The content waits; the surface did not have to

Documentation of the harness adapter work is **not written until its gates are
green**. [[vendor-harness-adapter-foundation]] is 80KB of in-flight reasoning
with Phase 5R.2 open and debt recorded against it; documenting it now would
document the plan, not the thing, and then require quiet correction — the
erosion [[premature-publish-manufactures-discipline-eroding-urgency]] names, on
the repo that already carries `autopush: false` for that reason.

The two were deliberately separated: **what the surface is** is a decision that
costs nothing now and claims nothing; **what it says** is a description that
must wait on evidence. Bundling them is what would have delayed both.

## Accessibility is part of the surface, not a later polish

The operator named accessibility as a first-class concern, and the finding is
that the real gap today is **not format but size and entry**: `orchestration.md`
(48KB), the manifesto (41KB), `domain-specification-guide.md` (40KB) render in
GitHub's blob view with no persistent nav, no in-page search, and a layout that
assumes a sighted mouse user scrolling. A Pages build is where a document
outline, landmarks, a skip link, search, sensible measure, and
`prefers-color-scheme` become available at all. That is the stronger argument
for Pages than convenience was.

One gap is independent of this decision and fixed immediately rather than
deferred: **no mermaid diagram in the repo carries an accessible name or
description.** Three files use mermaid and none declare `accTitle`/`accDescr`,
so a screen reader currently meets an unlabelled graphic. The fix improves the
existing GitHub rendering, needs no publishing decision, and is being applied in
the same session as this decision.
