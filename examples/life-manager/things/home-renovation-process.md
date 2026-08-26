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
- Performer: the homeowner gathers the scope; contractors prepare quotes.
- Gate authority: the homeowner authorises the hiring decision.
- Exit: a contractor is chosen → `materials`.

**materials**
- Entry: contractor chosen; selections needed before work can be scheduled.
- Produces: confirmed choices (worktop, units, fixtures) and their lead times.
- Performer: the homeowner makes selections with supplier and contractor input.
- Gate authority: the homeowner accepts cost and specification before fitting.
- Exit: all long-lead choices made → `fitting`. May loop back to `quotes` if a
  selection blows the budget and the scope must be re-priced.

**fitting**
- Entry: materials confirmed and a fitter booked.
- Produces: the installed work.
- Performer: the appointed contractor executes the installation.
- Gate authority: the homeowner accepts readiness for the snagging review.
- Exit: install complete → `snagging`. May loop back to `materials` if the
  install surfaces a materials problem (wrong size, damage on arrival).

**snagging**
- Entry: install complete; walk-through done.
- Produces: a snag list and its resolution.
- Performer: homeowner and contractor inspect; the contractor clears snags.
- Gate authority: the homeowner accepts the resolved work and final invoice.
- Exit: snags cleared and invoice settled → `complete`. May loop back to
  `fitting` while snags remain.

**complete (terminal)**
- Entry: signed off, paid, site cleared.
- Performer: the homeowner closes the project record.
- Gate authority: the homeowner owns final acceptance.
- "Done" means the run has nothing left to advance.

## Notes

This body is the definition's reason to change — it changes when the *process*
improves, not when a particular renovation moves. Instance-specific state (which
room, where it is now, who is holding it) lives in the run, never here.
