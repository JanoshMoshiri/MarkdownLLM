---
id: home-renovation-process
type: workflow-definition
status: stable
created: 2026-06-15
tags: [home, renovation, process]
stages:
  - id: quotes
    to: [materials]
  - id: materials
    to: [fitting, quotes]        # a quote may need revisiting if a choice blows the budget
  - id: fitting
    to: [snagging, materials]    # a fitting can surface a materials problem (wrong size, damage)
  - id: snagging
    to: [complete, fitting]      # snags may send work back to the fitter
  - id: complete
    to: []                       # terminal
---

# Home Renovation — Definition

A reusable skeleton for running a room renovation from quotes to a signed-off
finish. A run of this process is a `type: workflow-run` thing that names this
definition in its structural `definition:` field and carries a `current_stage`
pointing at one of the stages below. The same skeleton fits a kitchen, a bathroom, or a loft —
only the run differs.

## Stages

**quotes**
- Entry: scope is roughly known; ready to approach contractors.
- Produces: comparable quotes and a hiring decision (`type: decision`).
- Exit: a contractor is chosen → `materials`.

**materials**
- Entry: contractor chosen; selections needed before work can be scheduled.
- Produces: confirmed choices (worktop, units, fixtures) and their lead times.
- Exit: all long-lead choices made → `fitting`. May loop back to `quotes` if a
  selection blows the budget and the scope must be re-priced.

**fitting**
- Entry: materials confirmed and a fitter booked.
- Produces: the installed work.
- Exit: install complete → `snagging`. May loop back to `materials` if the
  install surfaces a materials problem (wrong size, damage on arrival).

**snagging**
- Entry: install complete; walk-through done.
- Produces: a snag list and its resolution.
- Exit: snags cleared and invoice settled → `complete`. May loop back to
  `fitting` while snags remain.

**complete (terminal)**
- Entry: signed off, paid, site cleared.
- "Done" means the run has nothing left to advance.

## Notes

This body is the definition's reason to change — it changes when the *process*
improves, not when a particular renovation moves. Instance-specific state (which
room, where it is now, who is holding it) lives in the run, never here.
