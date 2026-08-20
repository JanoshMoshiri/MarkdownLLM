# Calculation Reference — `computed:` and `mdllm calc`

The floor does every sum. A figure a domain derives says how it was derived,
and the tool computes it — on demand, and again at every commit.

This is reference material, not a foundational spec: nothing here loads at
session start. The three-line rule lives in `thing.md` (the field),
`validate.thing.md` (arithmetic is mechanical) and `provenance.md` (the
quarantine binding). Everything below is the grammar.

---

## Why

An agent asserting a total is the one mechanical job the framework used to
leave to reasoning. It goes wrong quietly: a line item is added, the total is
not updated, and nothing can tell — because nothing knew how the total was
reached. The fix is not to check the arithmetic harder. It is to write the
derivation down, so it can be re-run forever.

The assertion stays where it is. The derivation sits beside it. The pair is
the audit trail.

## The field

```yaml
---
id: vat-return-2026-02-to-04
type: vat-return
status: submitted
created: 2026-06-01

boxes:
  box3_total_vat_due: 0.00
  box4_vat_reclaimed: 16.80
  box5_net_vat: -16.80
  box7_total_purchases_ex_vat: 84

purchases_breakdown:
  - description: "Base recurring expenses"
    net: 69.00
    vat: 13.80
  - description: "Subscription — April 2026"
    net: 15.00
    vat: 3.00

computed:
  boxes.box4_vat_reclaimed: "sum(purchases_breakdown.vat)"
  boxes.box7_total_purchases_ex_vat: "sum(purchases_breakdown.net)"
  boxes.box5_net_vat: "boxes.box3_total_vat_due - boxes.box4_vat_reclaimed"
---
```

`computed:` maps a **target** — a dotted path to a field of this thing — to an
**expression**. `computed` is a core field: the framework ships it and the tool
reads it, so no domain declares it in `known_fields`.

A target with no asserted value is legitimate: the figure then lives only as
its derivation, and `mdllm calc` is how you read it.

## The two surfaces

```bash
mdllm calc .                                    # every declared derivation in the corpus
```

```bash
mdllm calc . --thing vat-return-2026-02-to-04   # one thing's block
```

```bash
mdllm calc . --thing statement-2026-01 --expr 'sum(table("Transactions").Amount[Category == "Fuel"])'
```

```bash
mdllm calc --expr "round(1200.00 * 0.2, 2)"     # pure arithmetic, no corpus
```

`calc` **reports, never writes** — it prints the figures and the agent
transcribes what belongs in the thing. It exits 1 when a derivation disagrees
with its asserted value or cannot be evaluated, so it can gate a script.

`mdllm validate` re-evaluates every block and reports disagreement as a
**Warning**, or an **Error** under `options: {computed: strict}` in
`_schema.yaml`. Warning is the default because a filed return whose box is
arithmetically odd but is *what was actually filed* must stay recordable.
A derivation that cannot be evaluated is always a Warning and never silent.

## The grammar

### Values

| Form | Means |
|---|---|
| `84`, `16.80`, `-8.50` | a number (always `Decimal`, never float) |
| `"Fuel"` | text, for filters and selectors |
| `boxes.box4` | a dotted path into this thing's frontmatter |
| `purchases.vat` | a path *through a list of mappings* — the column of `vat` values |
| `table("Transactions")` | a markdown table in this thing's body, by nearest preceding heading |
| `table(2)` | the second table in the body, by position |
| `table("T").Amount` | a column of that table |
| `table("T")["Amount (£)"]` | the same, when the header is not a plain identifier |
| `things(type="expense-record", tag="fy2025")` | things selected from the corpus |
| `things(...).net_amount` | that field across the selection |

Column names match tolerantly but never ambiguously: exactly, then
case-insensitively, then ignoring everything non-alphanumeric — so `.Amount`
reaches a header written `Amount (£)`. Two matches is an error, not a guess.

### Operators and functions

`+` `-` `*` `/`, unary `-`, and parentheses. Nothing else — no `**`, no `%`.

| Function | Takes | Gives |
|---|---|---|
| `sum(col)` | a set of values | their total |
| `count(col)` / `count(things(...))` | a set | how many |
| `avg(col)` `min(col)` `max(col)` | a set | the obvious |
| `abs(x)` | one value | its magnitude |
| `round(x)` / `round(x, n)` | one value | rounded HALF_UP |

Every aggregate reports the denominator it ran over (`sum over 2 value(s)
from …`), because a filter that matched nothing produces a confident zero and
the count is the only thing that exposes it.

### Filters

A boolean subscript on a **table column** keeps the rows whose row satisfies
the condition:

```
sum(table("Transactions").Amount[Category == "Fuel"])
count(table("Transactions").Amount[Category == "Food" and Amount > 0])
sum(table("Transactions").Amount[Category == "Fuel" or Category == "Housing"])
count(table("Transactions").Amount[Amount > limits.large])
```

Inside a filter a bare name is *this row's cell in that column*; a dotted path
still reads frontmatter, so a row can be compared against a figure the thing
declares. Comparisons are `==` `!=` `<` `<=` `>` `>=`, joined with `and`, `or`,
`not`. Numbers compare numerically; text compares case-insensitively (`Fuel`
and `fuel` are the same category — a filter that disagreed would under-count in
silence). Ordering comparisons on text refuse rather than guessing.

Only table columns can be filtered: a frontmatter list has no sibling row to
test.

## Money

- **`Decimal`, never float.** The strict loader preserves the authored YAML
  numeric lexeme, so `16.80` reaches calculation as exact decimal text rather
  than through a binary-float round trip. Text parses as it arrives:
  `£1,200.00`, `(45.60)` (accounting negative), `-£8.50`, and bold or
  backticked table cells.
- **No implicit tolerance.** Computed and asserted compare exactly. Sums of
  2dp inputs are exactly 2dp; anything that needs rounding declares it.
- **`round()` is HALF_UP**, the money convention — not Python's banker's
  rounding — so an operator checking by hand gets the same answer.
- **Scale is presentation, but authored scale is retained.** With lexical
  inputs, `10.00 + 5.50` prints `15.50`; comparison remains numeric. A domain
  that needs an explicitly different output scale declares it with
  `round(x, 2)` (or the required scale) rather than relying on ambient
  formatting.

## Quarantine

`provenance.md`: **no calculation may rest on an unverified external thing.**
Mechanically:

- **Within the thing itself** — computing the totals of an unverified
  statement is allowed, because that is precisely how a human comes to verify
  it. Every line of the report is stamped `UNVERIFIED`, so a provisional
  figure cannot be lifted out of its context unseen.
- **Across the corpus** — `things(...)` **excludes** quarantined things from
  the aggregate **and names each one**, citing the rule. Excluding them
  silently would be the worse failure: a total that dropped its evidence
  without saying so. A `verified: true` external thing is included, which is
  what the flip is for.

Two more exclusions, both stated rather than silent: a thing is excluded from
its own `things(...)` selection (a derivation must not draw on the figure it
derives), and a selected thing that lacks the field refuses with the ids
rather than returning a smaller denominator.

## What the floor refuses

Every one of these reports a reason rather than producing a number:

- an unknown reference, a missing column, a heading matching no table;
- a column name matching two columns, a heading matching two tables;
- a key present in only some entries of a list, or some things of a selection;
- text compared with `<` or `>`; division by zero;
- a derivation that resolves to a set rather than a single figure (it names the
  aggregates that would fix it);
- anything outside the grammar — comprehensions, lambdas, conditionals, `**`,
  attribute access on Python objects, `__import__`, `open`. Expressions are
  parsed with `ast` and walked node by node against a whitelist; there is no
  `eval` and no name lookup outside the thing.

## Deliberately absent

Named so their absence reads as a decision, not an oversight: substring
matching on descriptions (categorise at ingestion and filter on the category),
date arithmetic, units, `group by`, and any form of writing back to a thing.
When a domain is genuinely blocked without one, that is the felt evidence for
adding it — and the answer to "group by" is probably a report in a thing, not
a bigger language in the floor.
