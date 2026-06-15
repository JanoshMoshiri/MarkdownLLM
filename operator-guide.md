---
id: operator-guide
type: guide
status: draft
version: 1.0
created: 2026-06-11
linked_things:
  - id: domain-specification-guide
    relation: complements
  - id: validate-thing-specification
    relation: references
  - id: provenance-specification
    relation: references
  - id: domain-refresh-specification
    relation: references
  - id: orchestration-specification
    relation: references
  - id: git-workflow-specification
    relation: references
---

# The Operator's Guide — Working In A Domain Since v3

## Who This Is For

You — the human in the partnership. Every other document in this framework is
written for agents to consume; this one is written for the person who opens a
domain workspace, talks to the agent, and is ultimately accountable for what
the domain produces. It covers what changed between v2.9 and v3.4 *from the
operator's chair*: what you no longer have to carry, what now happens without
you, what you can newly ask for, and what remains irreducibly your job.

It is deliberately experiential rather than normative. For the rules
themselves, the specs remain canonical — each scenario links to the spec that
governs it.

## The Shift In One Paragraph

Under v2.x, the agent *promised* to validate its own work — a checklist it
reasoned through after every write — and you were the backstop. You caught
the broken link, the status value that didn't exist, the index that quietly
drifted, and told the agent to go fix itself. The v3 finding that forced the
change: a live domain had 17 of 17 things violating a validation rule at
Error severity, and nothing noticed. Since v3.0, every check that can be
expressed as code *is* code (`tools/mdllm.py`), wired into git so that
nonconforming work physically cannot be committed. The framework calls this
**replacing diligence with construction**. Your role narrows to the part
that was always genuinely yours: judgment.

## What You No Longer Have To Carry

| You used to… | Now… |
|---|---|
| Spot-check structure, statuses, and links after the agent wrote things | The pre-commit hook runs `mdllm validate`; commits containing Errors are blocked before they exist |
| Remember which status values are legitimate for which thing type | `things/_schema.yaml` declares them; the validator enforces exactly what the domain declared |
| Notice when a derived index no longer matched the things | `mdllm index check` rebuilds and diffs; index drift is detectable, and CI checks it on every push |
| Mentally track deadlines and re-raise them to the agent | `mdllm triggers` evaluates time/dependency/threshold conditions mechanically; the scheduled-triggers adapter surfaces them even with no session open |
| Wonder whether the framework had moved on since the domain was scaffolded | The `session-start:version-check` hard hook compares the version sentinel against the domain's `framework_version_seen` every session — and since v3.4.0 the sentinel itself is drift-proofed (it had silently stalled once; that class of failure is now an Error the framework's own hook blocks) |
| Reconstruct *why* a judgment call was made months ago | `type: decision` things pin their inputs to exact commits (`informed_by`); `mdllm provenance` enforces the chain |
| Worry that a workflow that worked last quarter silently regressed | Eval fixtures assert the contracted end state against committed domain state — a regression net you can run any time |

The pattern across every row: things you held in your head on the domain's
behalf became things the machinery holds by construction.

## What It Feels Like: Six Scenarios

### 1. An ordinary session — nothing changed, and that's the point

You open a domain workspace and ask about the current VAT quarter. Before
answering, the agent has already: loaded the domain AGENTS.md plus the
framework kernel (~5.3k tokens of operative rules instead of ~26.5k of full
specs), checked the framework version sentinel (silent when nothing changed),
and evaluated triggers (a filing deadline inside its horizon gets surfaced
unprompted). None of this is visible unless something needs your attention.
The conversation is the same conversation it always was — the floor only
exists underneath it.

*Specs: `orchestration.md` (hard hooks), `kernel.md`, `trigger-specification.md`.*

### 2. The hook says no

The agent writes a thing with a status the schema doesn't permit, or a
`linked_things` reference to an id that doesn't exist. The commit is rejected
and the validator's output says exactly why. The agent reads it, fixes the
thing, and commits again — usually without involving you at all. Two rules
worth internalising:

- **Never bypass the hook.** `--no-verify` is not a workaround; it is the
  bug being reinstalled.
- **If validation blocks a change that is genuinely legitimate, the schema
  is wrong** — and that is a real finding. Update `things/_schema.yaml`
  deliberately, with the agent, as its own committed change. Domains own
  their vocabularies; the schema is meant to describe how your domain
  actually works, not constrain it into someone else's workflow.

*Spec: `validate.thing.md` v2.0 (the division of labour).*

### 3. A judgment call worth keeping

The agent works out that entertainment VAT in a quarter's figures is blocked
from recovery and excludes it. That's a judgment over domain knowledge whose
correctness someone may need to defend later — so it becomes a
`type: decision` thing in `things/decisions/`, with `informed_by` entries
pinning the exact things (at exact commits) the judgment rested on. Eight
months later, "why did we exclude that?" is answered with receipts, not
archaeology. The quarantine rule rides along: nothing may rest on an
`origin: external` thing that hasn't been marked `verified` — ingested
content can't silently become load-bearing.

*Spec: `provenance.md`.*

### 4. Deadlines find you

You don't open a session for weeks. The scheduled-triggers adapter
(`adapters/scheduled-triggers.ps1`, registered in Task Scheduler) runs
`mdllm triggers` against the domain on a schedule and surfaces anything whose
condition has fired — a confirmation statement coming due, a blocked thing
whose dependency cleared. Separately, the GitHub Actions workflow runs
validation, provenance, and index-drift checks on every push, so a domain
with a remote has CI watching its floor.

*Specs: `trigger-specification.md`; `adapters/`.*

### 5. Locking in a workflow

A workflow now produces an agreed, contracted end state — say, a completed
VAT quarter with known-correct figures. You encode that end state as a
fixture in `evals/`, and `mdllm eval <domain> --fixture <file>` asserts it
against committed domain state from then on: a regression net that catches
the agent (or a future framework change) breaking something that used to
work. `eval --run` goes further — it seeds an isolated workspace and replays
the task through a fresh headless agent, which is how the framework runs its
own structure-beats-scale experiments.

*Spec: `evals/README.md`.*

### 6. The framework moved

You open a domain and the agent reports: framework is at 3.4.0, this domain
last saw 2.9 — refresh available. Refresh is **report-first by
specification**: the agent reads the CHANGELOG delta, compares it against
what the domain actually uses, and proposes adoptions. Only with your
authorisation does it touch anything, and it may only touch the domain's
AGENTS.md and skills — never your things. Crossing the v3 boundary, expect
one substantive conversation: agreeing the domain's schema (what types and
statuses it really uses), triaging whatever the first validation pass
surfaces, then one command to install the hook.

*Spec: `domain-refresh.md`.*

## The Toolbox

Everything lives in one file: `python {framework_root}/tools/mdllm.py
<subcommand> [path]`. Most of these run *for* you — via the pre-commit hook,
CI, or the agent — but all of them are yours to invoke directly.

| Command | What it does | When you'd type it yourself |
|---|---|---|
| `validate [path]` | Levels 1–3 mechanical validation; exit 1 on Errors | Sanity-checking a domain's whole corpus on demand |
| `triggers [path]` | Evaluates time/dependency/threshold conditions, deadline horizon | "What needs attention?" without starting a full session |
| `index [path] check\|rebuild` | Rebuild-and-diff derived indexes (`--signal triggers\|schema\|relationships`) | Suspected index drift; after bulk edits |
| `provenance [path]` | Validates decision chains and the external-content quarantine | Auditing why-trails before relying on a decision |
| `eval [path] --fixture <f>` | Asserts a fixture's contracted end state against committed domain state | Regression check after framework or skill changes |
| `eval --run [--model M --trials N --bare --report]` | Seeds an isolated workspace, runs a headless agent, scores trials | Running the framework-vs-bare experiment |
| `tokens [path]` | Measures spec token cost by loading tier | Checking session-cost impact after spec edits |
| `kernel [--check]` | Regenerates `kernel.md` from spec kernel blocks; `--check` gates drift | Framework maintenance (CI runs `--check` for you) |
| `changelog --since <tag>` | Drafts a CHANGELOG entry from the commit stream | Framework release prep |
| `worklog [path] [--write]` | Generates WORKLOG.md from the commit stream (sessions split on `session-end:` commits) | Keeping the session log current without hand-maintaining it |
| `refresh <domain> [--seal]` | Floor-only domain refresh: reports the version delta + unseen CHANGELOG entries; `--seal` bumps `framework_version_seen` after adoption | Bringing a stale domain current with the framework |
| `install-hook [path]` | Installs the git pre-commit validation hook | Once per domain repo, at floor adoption |
| `doctor [path]` | Probes the environment: prerequisites, hook *execution*, framework version drift (downward + upstream); exit 1 = degraded mode | New machine, new harness, or "is the floor actually on here?" |
| `scaffold <path>` | Deterministic domain birth: templates, nested repo, `.gitignore` isolation, hook, first commit | Creating a new domain — the mechanical half is one command |

Requires Python 3.10+ and PyYAML (`tiktoken` optional, for `tokens`).

## What Is Still Yours

The floor is deliberately mechanical, which means everything above it is
deliberately you:

- **Semantic validation.** A VAT figure that is plausible, well-formed,
  correctly statused, and *wrong* passes every mechanical check. Whether a
  thing makes sense remains the agent's Level 4 reasoning and, finally, your
  review.
- **Schema design.** The validator enforces whatever the schema says; saying
  the right thing is a domain-knowledge decision only you can confirm.
- **Authorising refresh adoptions.** Domains never silently self-modify on
  framework updates.
- **Deciding which judgments deserve decision records.** Provenance is for
  decisions whose correctness someone may later need to defend — taste, not
  rule.
- **Evolving the framework.** Domains read the framework; only humans (with
  the framework agent) change it.

The honest summary: v3 did not make the system smarter, it made the system
*unable to silently be wrong* about the mechanical layer — so that when you
do spend attention, it lands on judgment instead of bookkeeping.
