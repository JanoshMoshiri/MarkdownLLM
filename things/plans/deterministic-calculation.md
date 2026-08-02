---
id: deterministic-calculation
type: plan
status: in-progress
version: 1.0
created: 2026-08-02
priority: high
tags: [floor, calculation, arithmetic, provenance, quarantine, money]
linked_things:
  - id: a-true-primitive-is-discovered-not-authored
    relation: implements
    notes: "The primitive here is not `maths` — Python already has maths. It is the DECLARED DERIVATION: a figure that carries how it was derived, so the floor can recompute it forever and the assertion can never quietly drift from its own inputs. Everything else in this plan is that one spine."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: informs
    notes: "Two independent money-shaped domains reached the same wall — a derived figure asserted by reasoning, contradicted later by source. The second occurrence is the admission ticket."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: informs
    notes: "The Phase 4 check must be silent on a healthy corpus. A domain that declares nothing gets nothing; a declared derivation that agrees prints nothing. Only disagreement and non-evaluability speak."
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: references
    notes: "Admission gate: the check is pure arithmetic over declared inputs. It needs no allow-list, and if a future variant does, it is judgement in mechanical clothing and does not ship."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: informs
    notes: "Why the floor reports and never writes: a computed figure landing in frontmatter unasked is a change whose consequence the agent cannot foresee. `calc` prints; the human and the agent decide what to transcribe."
---

# Deterministic Calculation — the floor does every sum

## The felt gap

Two domains in this estate now turn bank data into money figures — one
consolidating personal expenditure across accounts, one preparing statutory
returns (VAT, corporation tax) from a business account. Both hit the same
wall, independently:

1. **A figure was asserted, not computed.** One domain carries a resolved
   `conflict` whose whole subject is a derived closing balance — an agent
   arithmetic chain over 54 transactions that produced &minus;£28.07 where the
   source statement says +£61.46. The discrepancy traced to a wrong *input*,
   which is exactly the failure a re-runnable derivation exposes on the day it
   is introduced rather than nine months later.

2. **A decision is explicitly staked on a tool that does not exist.** The other
   domain ruled that transaction detail lives as a markdown table in the body
   of the statement that ingested it — not as things, not in a spreadsheet.
   That ruling names its own cost in plain words: *"Arithmetic becomes the
   agent's job, and agents get arithmetic wrong."* It then names the answer:
   *"a deterministic Python tool that computes the totals ... The agent
   transcribes and reasons; the tool does every sum."* The decision sits at
   `confidence: medium` and says it earns `high` only when the tool exists.

This is not a feature request. It is a **named, buildable dependency that a
live domain decision already points at**, in a framework whose central
division of labour is that mechanical work belongs to the floor and never to
reasoning (`validate.thing.md`). Arithmetic is the most mechanical work there
is, and it is the one mechanical class the floor had no answer for.

## The primitive

Not "a maths module". The framework does not need Python to be taught
addition. What no domain can do today is state, in the thing itself, **how a
figure was derived**, and have that derivation evaluated deterministically —
on demand, and again at every commit thereafter.

So the primitive is the **declared derivation**:

```yaml
boxes:
  box4_vat_reclaimed: 16.80      # the assertion — what the domain claims
  box7_total_purchases_ex_vat: 84
computed:                         # the derivation — how the claim was reached
  boxes.box4_vat_reclaimed: "sum(purchases_breakdown.vat)"
  boxes.box7_total_purchases_ex_vat: "sum(purchases_breakdown.net)"
  boxes.box5_net_vat: "boxes.box3_total_vat_due - boxes.box4_vat_reclaimed"
```

Two surfaces over one evaluator, exactly as `triggers` has two (declared in the
thing, evaluated by the floor):

- **Compute** — `mdllm calc` evaluates the block on demand and prints the
  figures. This is the surface the ingestion workflow calls: the tool sums, the
  agent transcribes.
- **Check** — `validate` re-evaluates every declared derivation and reports
  where an assertion and its own derivation disagree. This is the surface that
  makes the first surface *durable*: a figure cannot silently drift from the
  inputs it was drawn from, and a later edit to a line item that does not
  update the total is caught at the boundary.

The assertion stays in the frontmatter. The derivation sits beside it. Neither
replaces the other, and the pair is the audit trail.

## Rulings taken

Recorded here so they are inspectable rather than settled silently.

**The floor reports, never writes.** `calc` prints; it does not edit
frontmatter. Same posture as `touchpoints` and `cascade`. A computed figure
landing in a thing unasked is an unforeseeable-consequence change, and this
framework hands those to the human.

**No implicit tolerance.** Computed and asserted values compare as exact
`Decimal`s. Money sums of 2dp inputs are exactly 2dp; anything that needs
rounding declares `round(x, 2)` in the expression. A fuzzy epsilon the operator
cannot predict is worse than a check that says what it means.

**Decimal everywhere, never float.** Values parse from source text to
`Decimal` directly. `£1,200.00`, `(45.60)`, `-£8.50` all parse; binary floating
point never touches a money figure.

**Disagreement is a Warning, not an Error, until a domain opts in.** A filed
return whose box is arithmetically odd but is *what was actually filed* must
stay recordable — recorded truth outranks internal consistency. `options:
{computed: strict}` in `_schema.yaml` promotes disagreement to Error, exactly
mirroring the established `options: {quarantine: strict}` precedent. Nothing
new is invented for this.

**Non-evaluability is reported, never silent.** An expression the floor cannot
parse or whose references do not resolve produces a Warning naming the reason.
The no-silent-default law the floor already applies to triggers.

**A derivation over quarantined data is computable, and stamped.** The
provenance law is that no calculation may *rest on* an unverified external
thing. Computing the totals is precisely how a human comes to verify one, so
within-thing computation over an unverified statement is allowed — and every
line of that output carries the quarantine stamp, so a figure cannot be lifted
out of a provisional context without seeing it. Corpus selectors (Phase 3) are
the case the law really addresses: unverified external things are **excluded
from the aggregate and named individually**, never silently included and never
silently dropped.

**No new foundational spec.** Twenty-three specs already load at tier 0 for
every domain in the estate, and calculation is invoked, not ambient — unlike
triggers, nothing evaluates it at session start. The *rule* lands as short
sections in `thing.md` (the field), `validate.thing.md` (arithmetic is
mechanical; never re-perform it by reasoning) and `provenance.md` (the
quarantine binding made mechanical). The *grammar* lands in `docs/`, which is
where reference material belongs. If calculation later grows ambient
behaviour, promotion to its own spec is an honest later move.

## Deliberately not built

Named so a later session does not read the absence as an oversight:

- **`contains(...)` / substring matching on descriptions.** Bank descriptions
  are categorised by the agent at ingestion into a `Category` column;
  equality filtering serves that. Substring matching is speculative until a
  domain is actually blocked without it.
- **`**`, `%`, date arithmetic, cross-thing writes, units.** No felt need.
- **A query language.** The filter grammar is one comparison, optionally
  `and`/`or`-joined. The moment it wants a `group by`, the answer is a report
  in a thing, not a bigger DSL in the floor.

## Phases

### Phase 1 — the evaluator core
`tools/markdownllm/calc.py`. Safe evaluation by walking a whitelisted `ast`
tree (no `eval`, no `exec`, no name lookup outside the thing). Decimal money
parsing. Dotted-path resolution against the thing's own frontmatter — scalars
and columns (a path through a list of mappings yields the column of values).
Functions `sum count min max avg abs round`; operators `+ - * /`, unary minus,
parentheses. `mdllm calc <path> --thing <id> --expr "<expr>"` as the ad-hoc
surface. Self-tests.

### Phase 2 — body tables
`table("Heading").Column` and `table(1)`, resolving a markdown table in the
thing's body by its nearest preceding heading or by position. Non-identifier
headers via `table("X")["Amount (£)"]`. Filters as boolean subscripts:
`table("Transactions").Amount[Category == "Fuel"]`. Self-tests.

### Phase 3 — corpus selectors
`things(type="expense-record", tag="fy2025").amount` — a column drawn from the
frontmatter of every matching thing in the corpus. The quarantine law made
mechanical: unverified external things excluded and named. Self-tests.

### Phase 4 — the check
`computed:` evaluated in validation level 3; disagreement reported with both
values; `options: {computed: strict}` promotes to Error; `computed` registered
in `CORE_FIELDS` (criterion 2 — a field the framework ships as part of a
reserved contract and the tool reads). Silent on agreement, silent on domains
that declare nothing. Self-tests, including the quiet-when-healthy proof.

### Phase 5 — the write-up
`docs/calculation-reference.md` (the grammar); short sections in `thing.md`,
`validate.thing.md`, `provenance.md`; kernel blocks updated and `mdllm kernel`
regenerated; `framework-map` node and count; `CHANGELOG.md`; version 3.25.0 in
`.markdownllm` and `AGENTS.md`.

## Build record — 2026-08-02 (v3.25.0)

- [x] **Phase 1 — the evaluator core.** `tools/markdownllm/calc.py`; `mdllm calc`
      with three modes. 30 self-tests. Renaming to `evaluate_expression` was
      forced by a live collision: the shim already re-exports `triggers.evaluate`,
      and the second binding silently won — caught by three trigger tests going
      red, which is what the shim's re-export surface is for.
- [x] **Phase 2 — body tables.** Heading- and position-addressed, tolerant
      column matching, boolean-subscript filters. Every aggregate now reports
      its denominator: a filter that matched nothing produces a confident zero,
      and the count is the only thing that exposes it. 15 self-tests.
- [x] **Phase 3 — corpus selectors.** `things(...)` plus the quarantine law made
      mechanical. First live run refused `amount` and named the seven things
      using `net_amount` — the refuse-rather-than-shrink property, proved on
      contact rather than in a fixture. 10 self-tests.
- [x] **Phase 4 — the check.** `derivation_findings` in `validate_corpus`, so it
      runs in the pre-commit hook. `computed` registered in `CORE_FIELDS`.
      Quiet-when-healthy proved twice in tests and once across all thirteen
      live domains (zero new findings). 7 self-tests.
- [x] **Phase 5 — the write-up.** `docs/calculation-reference.md`; sections in
      `thing.md`, `validate.thing.md`, `provenance.md`; kernel regenerated;
      framework-map View 3 gains the node (23 → 24 subcommands); operator-guide
      toolbox row; CHANGELOG; v3.25.0.

241 tests pass; `validate`, `coherence` and `boundary` clean.

**What the build itself surfaced:** the no-silent-default law has an arithmetic
form that is sharper than its trigger form. A trigger that cannot be evaluated
wastes attention; a *sum* that quietly shrinks its denominator produces a number
that looks exactly like a right answer. Four separate refusals in this module
exist for that one reason, and each of them is a place a reasonable
implementation would have returned something.

## What closes this plan

Phases 1–5 shipped, and the estate's money domains adopting `computed:` on
their next real ingestion. The downstream decision that staked itself on this
tool earns its `high` confidence on the day the tool produces the totals for a
real reconciled statement — that is the domain's event to record, not this
plan's, and this plan does not tick it.

**Status after the build: one item outstanding, deliberately.** The framework
half is complete and released. Adoption is a domain-side event in a private
repo, and the plan stays `in-progress` until it happens rather than closing on
a capability nobody has used yet — `existence-is-not-currency` applies to the
floor's own features. The first real statement ingestion closes it.
