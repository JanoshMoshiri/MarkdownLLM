# Excluded trials — kept as evidence, left out of the report

`mdllm eval --report` builds its table from `results/*.json` and never from
this folder. Each batch here is excluded for a stated reason; the reasoning
behind the reasons is in `things/artifacts/eval-record-2026.md`.

| Batch (file prefix) | Why it is here |
|---|---|
| `20260611-125556-haiku-fw-t1` pre-fix smoke run (the other twenty `20260611-*` files in `results/` are the valid first 2×2) | Ran against the fixture's pre-fix id template through a broken runner; the fixture was corrected the same day and re-run. |
| `20260612-23282*` three cold-start trials | Died in two seconds with an unparseable one-turn result before the runner captured agent output — the same launch failure as the 2026-10-05 aborted batch below, which makes defect 7 a recurrence, not a one-off. |
| `20260617-*` leaked FAC trial | The bare control read the framework's files it was meant to be denied — withholding is not isolation; the valid trials stayed in `results/`. |
| `20260709-*` opus longitudinal arm, haiku t5 | Contaminated: a trial agent committed into the framework repository mid-run; the haiku arm stayed valid to four trials. |
| `20261005-00*` and `20261005-01*` (haiku/opus aliases) | Produced under the whole-checkout grant, before the 2026-10-05 cold review closed the answer key; by that control's rule, re-run under the guard before citing, never cited as they are. |
| `20261005-2*` with `aborted: true` | Exited at launch — one turn, six seconds, no cost — on every `bare` and `bare-coached` trial and eighteen of twenty-two framework trials; the runner scored them as failed assertions with `voided` unset (defects 6 and 7 in the record). |
