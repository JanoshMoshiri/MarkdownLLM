---
id: operator-guide
type: guide
status: draft
version: 1.2
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
| Re-check by hand that a thing marked done didn't still hang on unfinished prerequisites | `mdllm validate` blocks a terminal-status thing that still depends on unfinished work — completing on top of an open prerequisite is an Error at the commit boundary (v3.15.0); if the edge was never really a prerequisite, model it as `linked_things` instead |
| Notice when a derived index no longer matched the things | `mdllm index check` rebuilds and diffs; index drift is detectable, and CI checks it on every push |
| Mentally track deadlines and re-raise them to the agent | `mdllm triggers` evaluates time/dependency/threshold/import conditions mechanically; the scheduled-triggers adapter surfaces them even with no session open |
| Wonder whether the framework had moved on since the domain was scaffolded | The `session-start:version-check` hard hook compares the version sentinel against the domain's `framework_version_seen` every session — and since v3.4.0 the sentinel itself is drift-proofed (it had silently stalled once; that class of failure is now an Error the framework's own hook blocks) |
| Reconstruct *why* a judgment call was made months ago | `type: decision` things pin their inputs to exact commits (`informed_by`); `mdllm provenance` enforces the chain |
| Worry that a workflow that worked last quarter silently regressed | Eval fixtures assert the contracted end state against committed domain state — a regression net you can run any time |

The pattern across every row: things you held in your head on the domain's
behalf became things the machinery holds by construction.

## What It Feels Like: Six Scenarios

### 1. An ordinary session — nothing changed, and that's the point

You open a domain workspace and ask about the current VAT quarter. Before
answering, the agent has already: loaded the domain AGENTS.md plus the
framework kernel (operative rules at a small fraction of the full-spec cost),
checked the framework version sentinel (silent when nothing changed),
read the generated **orient** view (the open loops — non-terminal work and open
conflicts — that replace the retired hand-kept session brief), and evaluated
triggers (a filing deadline inside its horizon gets surfaced unprompted). None
of this is visible unless something needs your attention.
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

Everything runs through one entry point: `python {framework_root}/tools/mdllm.py
<subcommand> [path]` (the implementation lives in the `tools/markdownllm/`
package beside it — one module per responsibility). Most of these run *for*
you — via the pre-commit hook, CI, or the agent — but all of them are yours
to invoke directly.

| Command | What it does | When you'd type it yourself |
|---|---|---|
| `validate [path]` | Levels 1–3 mechanical validation; exit 1 on Errors | Sanity-checking a domain's whole corpus on demand |
| `triggers [path]` | Evaluates time/dependency/threshold/import conditions, deadline horizon (import = live face reads via imports-check) | "What needs attention?" without starting a full session |
| `index [path] check\|rebuild` | Rebuild-and-diff derived indexes (`--signal triggers\|schema\|relationships\|provenance`) | Suspected index drift; after bulk edits |
| `provenance [path]` | Validates decision chains and the external-content quarantine | Auditing why-trails before relying on a decision |
| `touchpoints <id> [path]` | The Assimilate beat: one thing's declared inbound set + literal body references — "what did I just put at risk?" | Before changing a load-bearing thing; during an inflection walk |
| `autopush [path]` | The post-commit publication leg: pushes the validated commit per the repo's standing declaration (absence = on); bounded, never forces | Run by the post-commit hook — invoke by hand only when diagnosing publication debt |
| `candidates [path]` | The cue advisory's derivation: which things are reconciliation cue candidates and why | When a pre-commit cue line surprises you |
| `cascade <id> [path]` | Mirror of touchpoints: the declared downstream set a completion unblocks — "what did I just unblock?" | After completing a thing with dependants |
| `eval [path] --fixture <f>` | Asserts a fixture's contracted end state against committed domain state | Regression check after framework or skill changes |
| `eval --run [--model M --trials N --bare --report]` | Seeds an isolated workspace, runs a headless agent, scores trials | Running the framework-vs-bare experiment |
| `tokens [path]` | Measures spec token cost by loading tier | Checking session-cost impact after spec edits |
| `kernel [--check]` | Regenerates `kernel.md` from spec kernel blocks; `--check` gates drift | Framework maintenance (CI runs `--check` for you) |
| `domain-kernel [path] [--check]` | Regenerates the managed `<!-- generated:NAME -->` blocks in a domain's AGENTS.md (session-start, tier-routing, types, hooks, floor); `--check` gates drift | After a refresh, or when coherence reports a drifted block |
| `session-start [path]` | Emits the mechanical session-start ritual: version check, floor state, velocity, open loops, verified flips, and trigger evaluation | The SessionStart adapter runs it for you; by hand when orienting without a harness |
| `coherence [path]` | Dark-region checks: generated-artifact (kernel/index) freshness, `foundational_specs`↔filesystem, stale `stable` labels, dead vocabulary. Corpus-general; framework-only checks switch on at a `.markdownllm` root. Runs in the pre-commit hook | After adding/removing a spec; suspected drift between catalog and disk |
| `changelog --since <tag>` | Drafts a CHANGELOG entry from the commit stream | Framework release prep |
| `worklog [path] [--write]` | Prints an on-demand session-grouped view of the commit stream (sessions split on `session-end:` commits); `--write` saves a gitignored local snapshot | Reviewing recent session history — not a committed file (retired v3.17) |
| `refresh <domain> [--seal]` | Floor-only domain refresh: reports the version delta + unseen CHANGELOG entries; `--seal` bumps `framework_version_seen` after adoption | Bringing a stale domain current with the framework |
| `install-hook [path]` | Installs the three mdllm git hooks: pre-commit (boundary + validate + coherence, blocking), commit-msg (disclosure boundary, blocking), post-commit (autopush — on a repo with a remote and no `autopush: false`, commits PUBLISH from then on) | Once per domain repo, at floor adoption |
| `doctor [path] [--harness claude\|codex\|all]` | Probes the floor and, when selected, reports adapter support, project configuration, currency, trust, runtime, and real-event execution independently; static config or a runnable command never counts as an executed lifecycle event | New machine, new harness, after a refresh, or "is the floor actually on here?" |
| `adapter-install [path] --harness <name> [--dry-run]` | Preflights a project-local adapter, shows every decision and exact owned diff, then creates or safely merges only the selected adapter surface; ambiguity is refused | Run with `--dry-run` first for an existing domain; rerun without it only after deciding to change that project's harness configuration |
| `scaffold <path> [--harness claude\|codex\|all\|none]` | Deterministic domain birth: templates, nested repo, `.gitignore` isolation, Git hook, first commit, and only the selected outer harness projection. Omitting the flag preserves the Claude compatibility default | Creating a new domain — the mechanical half is one command, while `none` proves the substrate does not depend on an adapter |
| `mcp-serve <domain> [--http --port N --token]` | Serves the domain's exposed face (`exposed: true` things only) over MCP — stdio by default, Streamable HTTP with `--http` (loopback-only; non-loopback binds refused until the OAuth 2.1 leg). `--token` mints a per-run bearer token for tunnelled cross-machine probes | Wired into a consumer's `.mcp.json` (stdio: `command`; HTTP: `url` + optional `headers` carrying the token); stdio you rarely run by hand, `--http` you run when a porch should outlive its callers |
| `imports-check [path]` | Checks a consumer's external imports against their sources' faces — both directions: `stale` (source moved) and `diverged` (mirror moved); summary states coverage | "Are my imports still honest?" — after a session in any producing domain, or on suspicion |
| `estate-check [roots...]` | Batches `imports-check` over consumer roots with a roll-up — named explicitly, or (no args) the local clones the `estate-sync` walk finds; ephemeral, per-consumer, never an index | The estate-wide sync question, when you run more than one domain |
| `triggers --estate` | The attention sweep: per-domain trigger evaluation over the same local-clone walk, with a roll-up (fired / not-evaluable per domain) | After `estate-sync`, when the question is "what needs doing across the estate?" |
| `estate-sync [root]` | Fetch + ff-only pull across the estate's repos (root + `domain(s)/*`); divergence reported never resolved; never pushes; `--status` = publication debt from cached refs, no network | Session start (the adapter runs it before orientation); `--status` at session end |
| `boundary [path] [--history]` | Disclosure-boundary check of staged content/filenames/commit messages against the local gitignored `.boundary-terms` (absent ⇒ no-op) | Before any publication event, `--history` for a full-archive audit |
| `calc [path] [--thing ID] [--expr E]` | Evaluates declared derivations (`computed:` blocks): sums a body table, a frontmatter list, or a field across selected things; reports, never writes; exit 1 on disagreement. `validate` re-checks the same blocks at every commit | Ingesting a statement or preparing a return — the tool does every sum; `--expr` for an ad-hoc pivot. Grammar: `docs/calculation-reference.md` |

Requires Python 3.10+ and PyYAML (`tiktoken` optional, for `tokens`).

### Project harness adapters

Adapters harden the portable lifecycle; they are not the substrate. A domain
without one still operates through `AGENTS.md` interpretation and the Git
floor. For an existing project, inspect before writing:

```powershell
./tools/mdllm.ps1 doctor . --harness codex
./tools/mdllm.ps1 adapter-install . --harness codex --dry-run
```

The Codex project adapter is implemented and unit/integration tested, while a
Phase 5R repair gate now precedes its live Phase 6 acceptance. A live preflight
found a PowerShell 5.1 candidate-probe failure and exposed duplicated launch
policy; do not apply an adapter diff until the corrected renderer passes that
gate. The preflight-created framework-root `.codex/hooks.json` is untracked test
state awaiting rerender and an explicit ownership decision, not accepted
configuration.

Installing the corrected reviewed diff remains an operator action. The
[official Codex hook documentation](https://developers.openai.com/codex/hooks) names
`/hooks` as a **CLI** inspection/trust command; it was not available in the
observed Desktop chat command palette, so Desktop and CLI trust evidence must
not be conflated. `doctor` reports execution as `untested` until a real
lifecycle event is correlated with harness-owned transcript evidence and a
fresh definition-hash-bound record. The installer never mutates user-global
Codex configuration.

The shared runtime underneath adapters has separately been exercised in the
Codex desktop managed shell at the framework root and from a directly opened
nested domain, including a real nested-repository commit through the Git
floor. That runtime evidence must not be relabelled as Codex lifecycle or
trust evidence.

Claude Code's core framework path remains proven in use, but its generated
project lifecycle form is also inside Phase 5R. The historical projection puts
two SessionStart handlers in one matching group; the current Claude contract
runs matching handlers in parallel, so those bytes are now a legacy migration
input rather than the desired renderer. Existing `.claude/settings.json` and
`.claude/settings.local.json` files are not silently rewritten. A future
explicit refresh must show its diff, preserve permissions and unrelated groups
byte-for-byte, and refuse locally extended or ambiguous managed hooks.

## Running More Than One Domain

Each domain stays a sealed repo that is comprehensible by reading only itself
plus its quarantined external imports. When domains need each other's output,
the connection runs through three pieces — all operator-wired, none automatic:

- **The exposed face.** A producer opts individual things into its face with
  `exposed: true`; `mdllm mcp-serve` serves exactly that set (content and
  descriptive frontmatter — the internal relationship graph is stripped on
  egress). Nothing crosses by default; publication is an authoring decision.
- **The address book.** A consumer's `.mcp.json` `mcpServers` map names which
  producers it may read and how to spawn them. You wire it by hand, per trust
  zone. Discovery is never organic — a domain is reached because you listed
  it.
- **The membrane's direction.** Everything a consumer learns about a peer
  crosses through the face — including "have you changed?". A producer never
  learns who consumes it, keeps no consumer registry, and pushes nothing;
  the consumer polls. Imports arrive `origin: external`, `verified: false`,
  carrying the reference triple (`source_domain`/`source_id`/`source_commit`),
  and nothing rests on them until you verify (`provenance.md`).

The standing sync loop is then one command per consumer — `mdllm
imports-check` — or one `mdllm estate-check` (no args walks your local
clones; name roots explicitly to scope it) across the
consumers you name. It reports both failure directions: **stale** (the source
moved under your pin — re-read, re-verify, re-quarantine) and **diverged**
(the pinned commit is current but the mirror's content differs from the face —
someone edited the copy instead of the source; route it as an external
inflection, `change-reconciliation.md`). The summary line always states its
coverage: `0 stale` over zero checkable imports says so in words rather than
reading as all-clear. A useful cadence: run it at session start in any
consuming domain, and estate-wide after a working session in any producing
one.

`estate-check` is deliberately *batching, not an index*: output is ephemeral
and grouped per consumer, and no artifact maps producers to consumers — the
isolation rules survive the convenience. Roots are named per invocation, or
discovered from the local clones on this machine — a filesystem fact, not an
estate manifest (see The Machine Axis below). Each consumer's report now ends
with **face coverage**: what every address-book source *offers* vs what this
domain imported — because coverage counts pins that exist, a consumer that
imported nothing used to score a perfect report over an unread face.
Importing nothing may be correct; the line makes it a visible disposition
instead of an invisible default.

### The Direction of the Membrane Is a Ruling

One question came up hard enough to write the answer into `provenance.md`:
*shouldn't producers know their consumers, warn before withdrawing, push on
publish?* **No — by ruling, not by omission.** A producer never learns who
consumes it; publication is an honest commit to the face; delivery is the
consumer's poll. This is the atomicity of the estate: a domain's audience is
a fact held nowhere, so it can never be wrong, leak, or couple. The humane
edge is etiquette: **deprecate on the face before withdrawing** — the pin
moves, every consumer's next check shows the deprecation, then withdraw. And
a work item shared across domains has **one owner**; everyone else imports
it through the face, so completion arrives as `stale` at the next poll —
cascade without a reverse map.

### The Attention Loop

Triggers can now watch the membrane: `type: import` fires on the state
`imports-check` computes (`stale` / `diverged` / `withdrawn`) or when a face
offers things you haven't imported — the trigger that once sat in prose and
fired unseen is mechanically evaluable. Human-gated waits stay prose and gain
a **dated chase-by** partner (`trigger-specification.md`), so waiting on a
person is visible instead of silent. The estate-wide question — *what needs
doing?* — is one loop at the estate root:

```
mdllm estate-sync .        # fresh clones first — the sweep is only as honest as the log
mdllm triggers --estate    # per-domain evaluation, rolled up
mdllm estate-check         # membrane freshness + face coverage, per consumer
```

Everything in the loop is ephemeral batching over reads any domain could
make alone; nothing persists, nothing indexes, nothing tells a producer who
was watching.

### The Machine Axis

The membrane loop above syncs domains with *each other*. There is a second,
plainer sync: the same domain worked from more than one machine — your local
install and a cloud session today, collaborators tomorrow. Orientation reads
`git log`, and in a multi-machine estate the log is only whole on the remote,
so every session **syncs before it orients**: `mdllm estate-sync` walks the
root and every nested domain repo, fetches, and takes fast-forwards silently
(they are pure transport of state already committed elsewhere). Everything
else is reported, never resolved: `DIVERGED (+a/+b)` means both machines
committed since the last sync and the merge is *your* decision
(`divergence-is-an-unrouted-decision`); `dirty` means a working tree it
refused to touch; `offline` means it degraded gracefully and you are
orienting from last-fetched state — the session never blocks on the network.

The mirror runs at session end: `estate-sync --status` reports **publication
debt** — commits that are real on this machine and invisible to the estate.
Under autopush (the default since v3.26.0: the post-commit hook publishes
each floor-validated commit unless a repo declares `git: autopush: false`)
this report is an **anomaly detector** — any line means an offline session,
a rejected push awaiting your routing, or an opted-out repo holding work for
its deliberate release. Where autopush is off, the push stays yours
(git-workflow.md → The Outbound Rules); the report means you no longer have
to remember it. Note `estate-sync`
*discovers* its repos where `estate-check` refuses to: the guardrail there
protects relational information (a producer must never enumerate consumers),
while a walk for `.git` directories reveals nothing `ls` doesn't — repos, not
membranes. After a sync that moved anything, the tool suggests the
`estate-check` you may owe: pulled source commits can flip a consumer's
imports stale.

## What Is Still Yours

The floor is deliberately mechanical, which means everything above it is
deliberately you:

- **Semantic validation.** A VAT figure that is plausible, well-formed,
  correctly statused, and *wrong* passes every mechanical check. Whether a
  thing makes sense remains the agent's semantic-layer reasoning and, finally,
  your review.
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
