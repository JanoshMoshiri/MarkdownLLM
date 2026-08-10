# Ninth Independent Review — 2026-08-09 (cold, post-v3.30.0)

**Reviewer:** independent agent (Fable subagent, zero session context, adversarial
brief: "recent changes deserve MORE suspicion, not less; a clean verdict must be
evidenced"). Commissioned by the operator immediately after the v3.30.0
substrate reconciliation shipped and rolled out estate-wide — "nothing is fixed
unless tested."
**Corpus:** framework root @ HEAD (897c2f1, v3.30.0), all four seams: spec↔spec,
spec↔generator, spec↔tool, prose↔prose.
**Method:** full reads of the six foundational specs + kernel + Tier 2 specs +
load-bearing tool modules; kernel blocks verified byte-for-byte against
kernel.md; restated facts grepped and checked against their authorities;
read-only floor runs (validate, coherence) — both clean.

## Verdict

**7 real contradictions found**, every one in hand-restated prose — the exact
defect class v3.30.0 claimed to end, on surfaces its walk missed. The
mechanically-derived surfaces were found in genuinely good order (spec↔generator:
zero findings). All 7 were verified against the files by the commissioning
session and fixed in the v3.30.1 pass this review seals.

## Findings (all CONFIRMED and fixed in v3.30.1)

1. **Kernel carried pre-v3.17 doctrine on the always-loaded path.** The
   validate.thing.md kernel block (hence kernel.md, Tier 0) described insight
   disposition as "flags as missing from the brief" — the continuity brief
   retired in v3.17; the floor's actual finding is graph-liveness ("no inbound
   edge from a live thing"). *Fixed: kernel block reworded to the graph
   mechanism; kernel regenerated.*
2. **validate.thing.md contradicted its own kernel on retrospective cadence.**
   Kernel: moved to the floor in v3.24.0. Body's Layer-2 table: still listed as
   an agent reasoning check — instructing the agent to re-perform by reasoning a
   check the same spec forbids re-performing. *Fixed: row removed with the
   reason stated in place.*
3. **thing.md restated the trigger-type count as four.** `type: import` made it
   five in v3.27; the tool evaluates it, the templates teach it, the authority
   (trigger-specification.md) lists it. Three releases of lag. *Fixed: count
   removed; authority named.*
4. **trigger-specification.md's fire conditions predated `terminal_statuses`.**
   `due_date_passed` said "not completed or cancelled"; the kernel, the tool
   (`is_terminal`), and the prompt templates all say non-terminal per the
   type's declared set. In a domain like the regulated QMS (approved-current =
   settled), the two readings disagree on whether a trigger fires. *Fixed:
   both conditions now read through `is_terminal`. v1.4.*
5. **example-things.md misstated the reserved set — and implied `example` is
   reserved.** A four-item "all other framework-reserved types" list against
   the tool's thirteen; `example` is in fact domain-declarable. The fourth
   incomplete reserved-list restatement (v3.30.0 fixed three). *Fixed: routes
   to the tool's authority; `example`'s non-reserved status stated. v1.1.*
6. **derived-index.md didn't know its own fourth index.** The provenance index
   is "a standard derived index" per provenance.md and the tool rebuilds it by
   default; the index authority spec, thing.md's aside, the CLI docstring, and
   the operator guide all enumerated three signals. *Fixed at all five
   surfaces. v1.1.*
7. **CORE_FIELDS violated its own admission criterion.** thing.md recommends
   `priority`/`tags[]`/`confidence` (and documents `version`); the tool's
   admission rule says "a domain must never be made to register the framework's
   own vocabulary" — yet none were admitted, and the framework root itself had
   registered all four in its own `_schema.yaml`. The regression test even used
   `tags` as its example of a flaggable field, encoding the defect. *Fixed:
   four fields admitted with the criterion cited; test updated to a genuinely
   non-framework field.*

Cosmetic residue also fixed: "Level 4" vocabulary in cli.py and the operator
guide (current spec says Layer 2); framework-map's `mcp-serve` edge label
missing `--http`; root AGENTS.md locating the `TIERS` map in the shim rather
than `tools/markdownllm/repo.py`.

## Evidenced-consistent (verified, not assumed)

Kernel blocks byte-identical to kernel.md · reserved statuses identical across
tool/thing.md/validate.thing.md/schema comments/template · exactly four hard
hooks, identically enumerated in spec, generator, and root AGENTS.md · autopush
doctrine uniform across every live surface · continuity retirement consistent
everywhere except finding 1 · one startup sequence (the generated block), with
discovery and refresh deferring to it · version sentinel = AGENTS = CHANGELOG ·
scaffold delivers exactly what the specs claim (4 skills, 8 graph-stripped
prompts, blocks filled after prompts land, strict gate at birth) · spot-checked
constants (24h gate, 30d quarantine, 60d retrospective, fan-in ≥ 3, 26
subcommands) all match their prose.

## The lesson, in the framework's own terms

The reconciliation's method was sound and its seams held where derivation
already ruled; every survivor lived in prose restating a fact owned elsewhere.
Two consequences carried forward: (a) the reviewer's recommendation — promote
the trigger-type count, reserved-list restatements, and index-signal
enumerations into derived surfaces — lands in `mechanical-coherence-checks-backlog`
as candidate checks; (b) the review confirms the sweep-vs-author asymmetry the
estate already recorded: the author of a fix is the wrong certifier of it, and
a cold read found in nine minutes what the author's walk could not see at all.
