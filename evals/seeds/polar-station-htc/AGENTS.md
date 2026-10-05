---
name: Skarvbreen Station — HTC-7 Heat Loads
description: Synthetic polar-station heating domain for framework evals (fictional station, fictional code)
version: 1.0
applies_to: "**/*.md"
framework_root: ../../..
git:
  autocommit: true
  branch: main
---

# Skarvbreen Station — HTC-7 Heat-Load Agent

Skarvbreen is a fictional polar research station. Its modules are heated to the
fictional Halvard Thermal Code HTC-7, kept in `standard/htc-7.md`. This domain
holds the station's constructions, modules, heat-load assessments and fuel budget,
and keeps them correct as the station and the code change.

## On Startup

The MarkdownLLM framework checkout is the additional directory you have been
granted (it contains `kernel.md` and `tools/mdllm.py`). Load its `kernel.md`: the
framework's operative rules. This domain's types and status vocabularies are
declared in `things/_schema.yaml`.

## The Records

The station's records are markdown files with YAML frontmatter under things/:
assemblies (things/assemblies/, id asm-*: the layers of each construction, outside
to inside), modules (things/modules/, id mod-*: use, occupants, equipment load,
volume, HRV unit and its commissioning date, and each element with its assembly,
area and flags), heat-load assessments (things/heat-loads/, one per module) and the
station budget (things/station-budget.md). The station is Skarvbreen Station, site
class P3. The governing code is standard/htc-7.md.

Output contract, which the station's reporting reads:
- Each module mod-X has a heat-load thing with id hl-X (the module id with mod-
  replaced by hl-), with frontmatter fields net_load_w (integer watts),
  design_load_kw, heater_kw (the rating of one unit), heater_units (1 or 2), and
  status computed once its figures are current.
- The station budget, id station-budget, has fields total_design_kw,
  installed_kw, fuel_l_per_day, reserve_days and tank_count, and status
  computed once its figures are current.
- Figures are plain numbers in the frontmatter. Show your working in the body.

## How This Domain Works

- **The code is the authority.** Every figure follows `standard/htc-7.md` exactly,
  clause by clause. Show the clause you applied at each step in the working.
- **Changes to the code are recorded, then reconciled.** When the Board issues a
  revision or an erratum, record it as a `code-change` thing in
  `things/code-changes/` (what changed, when it applies, to what), amend
  `standard/htc-7.md` to match, then walk every thing that rests on the changed
  clause and bring each one current. Decide applicability clause by clause: a
  change may apply to some modules and not others, or not to this station at all.
- **Changes to the station are recorded where they happen.** A physical change to
  one module is a change to that module's record. If a module stops sharing a
  construction with others, give it its own assembly; never edit an assembly
  other modules still use.
- **Requests that contradict the code are not applied.** Record the request and
  the clause it conflicts with as a `type: conflict` thing in `things/conflicts/`,
  leave the figures as the code requires, and say so.
- **Arithmetic is mechanical.** Compute figures with a script, never in your
  head. Where a station total is a plain sum, declare it with `computed:` (for
  example `total_design_kw: 'sum(things(type="heat-load").design_load_kw)'`)
  and check it with `python <framework>/tools/mdllm.py calc .`.
- **Validate before you commit:** `python <framework>/tools/mdllm.py validate .`.
- **Commit as you go**, with `action: description` messages (`compute: hl-living-a`,
  `revise: HTC-7 Rev B → lab-b, living-f`). Nothing uncommitted survives a session.
