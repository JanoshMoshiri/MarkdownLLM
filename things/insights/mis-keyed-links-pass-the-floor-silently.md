---
id: mis-keyed-links-pass-the-floor-silently
type: insight
status: active
version: 1.0
created: 2026-06-16
confidence: medium
origin: synthesised
source: session — sleeping-bag-fac smoke (haiku framework trial, 20260616-233024)
session: 2026-06-16
tags: [evals, stage-2, floor, validate, linked-things, fixture-design, coherence]
linked_things:
  - id: first-2x2-measured-convention-following-not-reasoning
    relation: extends
  - id: fixture-fixes-correct-bugs-not-difficulty
    relation: supports
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: complements
---

# A Mis-Keyed Relation Passes The Floor Silently

## The Insight

In the `sleeping-bag-fac` smoke (haiku, framework condition,
`20260616-233024-haiku-fw-t1`) the agent computed **all five FAC figures
correctly** (4, −1, −5, 2, −5 — every trap cleared) and *did* intend to link
each assessment to its trip and bag. But it wrote the edges under a
non-canonical key:

```yaml
relations:
  - type: assesses
    target: trip-aonach-ridge
  - type: references
    target: bag-alpine-pro
```

instead of the framework's canonical `linked_things: [{id, relation}]`. Two
facts followed, and the second is the durable one:

1. **The agent invented the syntax** because the seed gave it nothing to copy.
   Our seed is unusually all-orphan (the input bags and trips legitimately do
   not link to each other), so there was no in-corpus `linked_things` exemplar.
   Absent an example, the model produced a plausible-but-wrong shape.
2. **The floor accepted it silently.** `mdllm validate` returned
   `validates clean (Errors: 0)` while the index never saw the edges — the five
   `assesses` link assertions all failed. An unknown top-level `relations:`
   mapping is neither parsed as a relation nor flagged as suspect; the declared
   edge is simply *lost*, with no error and no warning.

So a load-bearing structural edge can be written, look right to a human reading
the file, and be a complete no-op — and the commit boundary passes it.

## Why It Matters

This is a corpus-general mechanical gap, not a fixture quirk. Any agent, in any
domain, can drop a relation into a near-miss key (`relations`, `relation`,
`links`, `related_to`) and the floor will not notice. It is the same family as
[[mechanical-assimilation-is-blind-to-prose-dependencies]] — a declared
dependency the index cannot walk — except here the edge is in *frontmatter*,
machine-readable, and still missed, which makes it sharper: this one is
mechanically catchable.

**Candidate floor check (corpus-general, cheap):** in `validate`, emit a Warning
when a thing's frontmatter carries a top-level mapping/list field whose name is a
near-synonym of `linked_things` (`relations`, `relation`, `links`, `related`,
`related_to`) but `linked_things` itself is absent or does not contain those
targets. The judgment (is this really a link?) stays advisory — a Warning, not an
Error — but the silent-loss case becomes visible. It would have turned this
trial's five invisible edges into five Warnings at the commit boundary.

## Relationship To The First 2×2

The `vat-quarter-basic` run attributed all its variance to the single
`has-deadline` link and read it as *model capability under load*
([[first-2x2-measured-convention-following-not-reasoning]]). This smoke offers a
second, mechanical candidate cause for link misses generally: the agent may be
linking correctly *in intent* but under the wrong key. The two are separable —
in the VAT run opus+framework scored the link 5/5, proving the canonical form is
reachable — so this is a contributing mechanism, not a replacement explanation.
It means link-assertion failures should be inspected at the frontmatter level
before being scored as reasoning failures.

## Disposition

Per the operator's call (2026-06-16) and [[fixture-fixes-correct-bugs-not-difficulty]]:
the seed is **left unpatched** — adding a `linked_things` exemplar would correct
the agent's syntax but would also hide the floor gap this trial exposed. The
framework cells therefore cap near 16/21 (figures + status + existence pass;
the five links fail), and that is reported honestly per-assertion. The
condition-neutral reasoning core — the `fac_celsius` figures — is the
discriminator, and it is unaffected. The candidate floor check above is the
real follow-up.
