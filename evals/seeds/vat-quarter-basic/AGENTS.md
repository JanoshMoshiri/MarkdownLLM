---
name: Meridian Web Studio Ltd — VAT
description: Synthetic UK VAT compliance domain for framework evals (fictional company, fabricated figures)
version: 1.0
applies_to: "**/*.md"
framework_root: ../../..
git:
  autocommit: true
  branch: main
---

# Meridian Web Studio Ltd — VAT Agent

Fictional UK web consultancy on standard-rate VAT (20%), quarterly returns.
This domain exists for framework evals: prepare VAT returns from the records in
`things/`.

## On Startup

Load `{framework_root}/kernel.md` — the framework's operative rules. This
domain's types and status vocabularies are declared in `things/_schema.yaml`.

## VAT Return Workflow

1. **Open** — create a `type: vat-return` thing for the period, id
   `vat-return-[YYYY-MM]-to-[MM]` (e.g. `vat-return-2026-02-to-04`, matching
   the `filing-deadline-vat-[YYYY-MM]-to-[MM]` convention), status `open`.
   Link the period's `filing-deadline` thing with `relation: has-deadline`.
2. **Output VAT** — sum `vat_amount` across all `income-record` things dated in
   the period. Record as `output_vat`.
3. **Input VAT** — sum `vat_amount` across `expense-record` things dated in the
   period where `vat_reclaimable: true`. Blocked categories (client
   entertainment) are never reclaimable. Record as `input_vat`.
4. **Net** — `net_vat_due = output_vat - input_vat`. Set status
   `figures-ready`. Note the workings in the narrative.
5. Link each included record to the return; commit per the framework's
   `post-write:commit` hard hook with `action: description` messages.

## Thing Types

Declared with status vocabularies in `things/_schema.yaml`:
`vat-return`, `income-record`, `expense-record`, `filing-deadline`.
