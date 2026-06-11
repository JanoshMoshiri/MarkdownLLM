---
id: fixture-fixes-correct-bugs-not-difficulty
type: insight
status: active
version: 1.0
created: 2026-06-11
confidence: medium
origin: synthesised
source: session — Stage 2 smoke test (vat-quarter-basic)
session: 2026-06-11
tags: [evals, fixture-design, experiment-validity, stage-2]
linked_things:
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: supports
  - id: operative-rules-are-a-small-fraction-of-spec-prose
    relation: relates-to
---

# Fixture Fixes Correct Bugs, Not Difficulty

## The Insight

During the first live Stage 2 smoke test (haiku, vat-quarter-basic, framework
condition), two issues surfaced against the fixture:

1. The seed's `vat-return-[YYYY-MM]-to-[YYYY-MM]` id template (in AGENTS.md)
   didn't match the fixture's expected id or the seed's own
   `filing-deadline-vat-2026-02-to-04` naming — an internal inconsistency
   within the fixture itself, independent of the model. Fixed: the template
   now matches the established convention.
2. The agent wrote `relations: {has-deadline: ...}` instead of the
   framework's `linked_things: [{id, relation}]` schema — a genuine test of
   whether the agent reads kernel.md closely enough to find the relevant
   field among ~8 "recommended fields" packed into one dense line. Left as-is.

The distinguishing question: **does the failure stem from the fixture
contradicting itself, or from the model's reasoning/attention within a
self-consistent spec?** Only the former is a fixture bug. The latter is the
thing being measured — "fixing" it (e.g. spelling out `linked_things`
explicitly in the VAT workflow) would make the framework condition easier in
a way that doesn't generalize, and would break comparability with the bare
condition and with opus runs in the same cell.

## Why It Matters

Governs how to triage future Stage 2 trial failures before/during the 2×2
run: check fixture self-consistency first (id templates, schema field names
matching across seed files) and fix those unconditionally. But genuine
reasoning/attention gaps — even ones an obvious wording tweak would "fix" —
are findings, not bugs, and should be left in place so the experiment
measures what it's designed to measure.

## Context

Observed 2026-06-11, first live haiku framework trial on vat-quarter-basic:
scored 1/7 → 6/7 after fixing (1) two Windows-only `mdllm.py` subprocess bugs
(resolving `claude.exe` directly rather than the `.cmd` shim, which on Windows
mangled `--permission-mode acceptEdits` and `Bash(git:*)` via cmd.exe argument
quoting) and (2) the id-template inconsistency. The remaining 1/7
(`linked_things` vs `relations`) was left as a known finding for the 2×2 run
rather than patched.
