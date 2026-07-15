---
id: mdllm-package-split
type: plan
status: in-progress
version: 1.0
created: 2026-07-15
priority: high
tags: [tooling, refactor, srp, floor, ratification-window]
linked_things:
  - id: independent-review-2026-07-14-fable
    relation: implements
    notes: "Review 7's over-engineering finding: the framework applies SRP to 60-line specs and exempts its 3,400-line largest artifact. Done now because ratification (QMS-AUTO-001) will fix the shape in place — restructure before the system description is written, or live with the single file."
---

# mdllm.py Package Split

Behaviour-preserving decomposition of `tools/mdllm.py` (~3,444 lines) into a
package at `tools/markdownllm/`, with `tools/mdllm.py` surviving as a thin
entry shim. Run under the code-architect domain's `refactoring-process`
workflow (its first real run — the run thing lives in that domain's repo).

## Constraints (discovered, not chosen)

1. **`python {framework_root}/tools/mdllm.py <cmd>` is a public contract** —
   cited in kernel.md, AGENTS.md, all nine domain AGENTS.md files, docs, and
   the pre-commit hook installed in every domain repo. The shim keeps this
   path working with zero fleet touch.
2. **The 105-test suite is the characterization oracle** — no monkeypatching,
   all access via `import mdllm`. The shim re-exports (explicitly, including
   underscore names) every symbol the tests use; the suite runs green
   *unmodified* throughout.
3. **Zero-install portability survives** — stdlib-only, no pyproject. The
   package sits beside the shim; script-dir resolution puts it on `sys.path`
   with no path hackery. (`tools/mdllm/` is impossible — import collision
   with `mdllm.py`; hence `tools/markdownllm/`.)

## Module map (cut by reason to change)

`model` (Thing/Finding/Corpus/parse/scan/schema/constants — imports nothing) ·
`validation` (levels 1–3, version sync) · `triggers` · `provenance` ·
`touchpoints` · `cascade` · `tokens` · `indexes` · `history` (changelog,
worklog) · `refresh` · `evals` · `kernel_gen` · `domain_kernel` · `session` ·
`coherence` · `doctor` (the one sanctioned aggregator — imports library
functions, never other commands) · `scaffold` (+ install_hook) ·
`mcp_server` · `imports_check` · `cli` (argparse wiring only).

Dependency direction: everything → `model`; `cli` → command modules; no
command module imports another.

## Sequence (risk-first)

1. `model` — the foundation; the cut most likely to expose hidden coupling.
2. `validation` — most load-bearing (pre-commit path), densest tests.
3. Independent leaves: triggers, provenance, touchpoints, cascade, tokens,
   indexes, history.
4. Tangled middles: refresh, evals, kernel_gen, domain_kernel, session,
   coherence.
5. doctor, scaffold, mcp_server, imports_check.
6. `cli` + shim finalisation.

One extraction move = one commit = one oracle run (pytest + golden CLI diff +
`validate .`). A red test is a divergence routed via the workflow's
`adjudicate` stage — restore / revise-as-decision / spawn — never a silent
test edit.

## Characterization additions

The tests pin functions; the CLI surface (argparse wiring, exit codes,
stdout) gets a golden-run script: every read-only subcommand executed against
the framework root and `examples/` corpora, output normalised (volatile
velocity/time strings) and diffed after each move. Script and baseline live
in the session scratchpad — the durable oracle is the test suite; the golden
runs are refactor-scoped.

## Out of scope

Splitting the test file itself (optional follow-up once the package shape
settles); any behavioural change, however tempting; renaming any subcommand
or flag.

## Exit criteria

All 105 tests green unmodified · golden CLI diff clean · `validate .` +
`coherence` clean · CHANGELOG entry + patch version bump · workflow-run in
code-architect closed with every divergence traced · `refactoring-process`
promoted draft→evolving on the strength of this run.
