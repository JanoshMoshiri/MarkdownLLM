---
id: operator-guide
type: guide
status: draft
version: 2.2
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
  - id: an-honest-ledger-replicates-full-compliance-does-not
    relation: implements
    notes: "The probe ladder section is that insight's verification method given operator-facing steps: demand evidence, treat the smooth yes as the tell."
  - id: session-start-hardening
    relation: references
    notes: "Phase 4 landed the probe ladder here; the five-run baseline it distils is that plan's Phase 0 record."
  - id: explorer-publication-position
    relation: derived-from
    notes: "v1.8 adds the optional read-only visual route while preserving the distinction between inspection and agent operation."
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: derived-from
    notes: "v1.9 records the Desktop direction without advertising an acceptance-pending candidate as released."
  - id: harness-native-onramp-supersedes-desktop
    relation: derived-from
    notes: "v2.0 records Desktop frozen and the harness-native onramp as the accessible route; the command-line sequence stays the published route until the onramp lands."
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
Error severity, and nothing noticed. Since v3.0, the framework moves earned,
enumerated structural checks into code (`tools/mdllm.py`) and wires them into
git. A current, runnable hook blocks candidate commits with mechanical Errors;
it does not prove semantic truth, agent adherence, or the completeness of the
rule set. The framework calls this **replacing diligence with construction**.
Your role narrows to the part that was always genuinely yours: judgment.

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

The pattern across every row: mechanically decidable facts you once held in
your head became checks the active floor can reproduce. Meaning and omissions
remain the work of the probabilistic agent and your review.

## What It Feels Like: Seven Scenarios

### 1. An ordinary session — nothing changed, and that's the point

You open a domain workspace and ask about the current VAT quarter. A supported
lifecycle route emits the startup contract or loudly defers the kernel with an
integrity fingerprint, then reports the version sentinel, generated **orient**
view (non-terminal work and open conflicts), and trigger results. Those are
delivery and mechanical-result facts, not proof the agent read or applied the
contract. `doctor`, the session attestation, and the probe ladder below keep
those evidence levels separate. The conversation can still feel ordinary; the
important difference is that missing or partial startup is named rather than
promoted to adherence.

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

### 7. Seeing the estate without opening a coding harness

You want to understand what exists before asking an agent to change anything.
The optional [MarkdownLLM Explorer](../explorer/README.md) opens the substrate
and nested domain estate as a read-only visual surface: repository commits, the
file tree, skills and memory, with Markdown rendered as a document. Windows has
an installer preview. On macOS, ask the framework agent to **open MarkdownLLM
Explorer**; it runs the tracked portable launcher and opens the browser.

Explorer is a viewer, not an agent route. It cannot accept instructions, invoke
skills, edit files, run `estate-sync`, validate, reconcile or publish. If its
view is stale, synchronise the underlying repositories through the normal
operator/agent workflow and refresh Explorer. Start with the [installation
guide](../explorer/docs/installation-guide.md) and then the [user
guide](../explorer/docs/user-guide.md).

The local service stops after 30 minutes without authenticated browser activity.
Ask the agent to open it again when needed; no server-management command needs
to be remembered.

*Boundary: `interface.md`; release position: `explorer-publication-position`.*

### 8. The accessible route

The accessible route is harness-native: you say what you want to work on, in the harness you
already use, and the agent does the rest — sync, refresh, floor, session start — and tells you
where things stand in your own words. That onramp is being built as a skill for Claude Code and
Cowork, with Perplexity as a candidate route pending a probe; see
`operator-seat-and-harness-native-onramp`. Until it lands, this guide's command-line sequence is
the published route.

MarkdownLLM Desktop, the local application tried as this route, is **frozen at its issued 0.1.6
installer as an Engineering Preview** (2026-09-06). It is not published and is not the first-use
path; its setup-journey requirements feed the onramp. The substrate never depended on it:
existing harnesses and the read-only Explorer remain valid routes and integrations.

*Direction: `harness-native-onramp-supersedes-desktop`; contract: `interface.md`.*

## The Toolbox

Everything runs through one entry point:
`python {framework_root}/tools/mdllm.py <subcommand> [path]` (the
implementation lives in the `tools/markdownllm/` package beside it — one
module per responsibility). Most of these run *for* you — via the pre-commit
hook, CI, or the agent — but all of them are yours to invoke directly.

<!-- generated:toolbox -->

| Subcommand | Usage | The tool's own description |
|---|---|---|
| `adapter-install` | `mdllm adapter-install --harness {all,claude,claude-code,codex,cowork,perplexity} [--dry-run] [--refresh-legacy] [path]` | show and safely apply a project-local harness adapter diff |
| `assemble` | `mdllm assemble --config CONFIG [--root ROOT] [filters ...]` | config-driven estate assembly for an environment that started without one: clone the configured domains, resolve real default branches (never guessing), install floor hooks, set identity, leak-check, then per domain run sync + session-start --contract (the Tier-0 contract enters the transcript) + full triggers + imports coverage; closes with the BRANCH MAP and an honest handoff. Credentials: ambient, or GH_PAT/MDLLM_GIT_TOKEN command-scoped |
| `autopush` | `mdllm autopush [--timeout TIMEOUT] [path]` | post-commit publication leg: push the current branch to its upstream only when AGENTS.md declares literal git.autopush: true (all other states are off); bounded, never forces, rejection surfaced as DIVERGED never resolved; exit 0 always |
| `boundary` | `mdllm boundary [--message FILE] [--history] [--audit-terms] [--quiet] [path]` | disclosure-boundary check: staged additions, filenames, or a commit message against the LOCAL .boundary-terms file (gitignored; absent => no-op) |
| `bundle` | `mdllm bundle --harness {claude-code,codex,cowork,perplexity} [--out OUT] [--hash]` | render a harness's estate-level distribution bundle from framework-owned templates — config derived from the local estate's remotes and git identity; output is PRIVATE (names your repos) and lands in a gitignored build directory |
| `calc` | `mdllm calc [--thing ID] [--expr E] [path]` | evaluate declared derivations (`computed:` blocks) — the floor does every sum; reports, never writes |
| `candidates` | `mdllm candidates [--view {worktree,index}] [path]` | pre-commit advisory: for staged MODIFIED things, surface the cue question (reasoned-from: definition surface or fan-in) and the serve-side notice (exposed => this change publishes); never blocks, exit 0 always |
| `cascade` | `mdllm cascade id [path]` | post-completion cascade: what a thing's completion unblocks downstream (mirror of touchpoints) |
| `changelog` | `mdllm changelog [--since SINCE] [path]` | draft a CHANGELOG entry from commits |
| `coherence` | `mdllm coherence [--window WINDOW] [--quiet] [--view {worktree,index}] [path]` | dark-region checks: generated-artifact freshness, catalog/filesystem, stale labels |
| `cues` | `mdllm cues [--raise] [--since SINCE] [path]` | the cue question, persisted: open `type: cue` things awaiting a human verdict, plus reasoned-from things modified since the last retrospective that no cue covers; session-start emits the same line every session — reports; --raise writes the open cue, never the verdict; exit 0 always |
| `dispatch-payload` | `mdllm dispatch-payload [--scope REPO] [--stop-condition TEXT] [--launch-context TEXT] [path]` | compose the dispatch launch TEXT for a scheduler tick: resolved inputs + the standing dispatch prompt emitted whole, with an integrity trailer. Read-only — prints and exits, writes nothing, so it is safe inside a shell substitution on any host |
| `docs` | `mdllm docs [--check] [path]` | regenerate the derived blocks in docs/ (the operator-guide toolbox, the framework-map edge list) from the live tool and spec frontmatter |
| `doctor` | `mdllm doctor [--harness {all,claude,claude-code,codex,cowork,perplexity}] [path]` | probe the environment: floor prerequisites, hook execution, framework version drift |
| `domain-kernel` | `mdllm domain-kernel [--check] [path]` | generate/refresh a domain AGENTS.md's managed operative blocks |
| `estate-check` | `mdllm estate-check [paths ...]` | operator-axis batch of imports-check over consumer roots — named explicitly, or (no args) the local clones the estate-sync walk finds; ephemeral per-consumer reads, never an index |
| `estate-sync` | `mdllm estate-sync [--status \| --require-fresh] [--timeout TIMEOUT] [paths ...]` | sync before orienting: fetch + ff-only pull across the estate's repos (root + domain(s)/*); divergence reported, never resolved; never pushes; --status = publication debt from cached refs, no network; --require-fresh = fail if sync used cached or unresolved state |
| `eval` | `mdllm eval [--fixture FIXTURE] [--run] [--model MODEL] [--trials TRIALS] [--bare] [--report] [--dry-run] [--timeout TIMEOUT] [path]` | check a golden-scenario fixture against domain state |
| `external-trust` | `mdllm external-trust [--path PATH] [--hash EXPECTED_HASH] [--allow {command,network,headers,body-read} [{command,network,headers,body-read} ...]] {review,trust,revoke} [server]` | review, hash-confirm, or revoke clone-local authority for one .mcp.json server entry; repository content is inert by default |
| `harness-event` | `mdllm harness-event {claude-code,codex,cowork,perplexity} {session-start,post-write} path definition_hash` | internal project-hook dispatch for one ordered lifecycle binding |
| `imports-check` | `mdllm imports-check [path]` | re-quarantine-on-drift: check a domain's external imports against their sources' exposed faces (both directions: stale = source moved, diverged = mirror moved) |
| `index` | `mdllm index [--signal {triggers,schema,relationships,provenance}] [path] {check,rebuild}` | check or rebuild derived indexes |
| `install-hook` | `mdllm install-hook [--no-test] [--uninstall] [path]` | install the three mdllm git hooks (pre-commit, commit-msg, post-commit) and execution-test pre-commit where git supports it |
| `kernel` | `mdllm kernel [--check] [path]` | generate kernel.md from spec kernel blocks |
| `mcp-serve` | `mdllm mcp-serve [--http] [--port PORT] [--host HOST] [--token [TOKEN]] path` | serve a domain's exposed face over MCP — the cross-domain producing side (read-only). Default transport is stdio (the client spawns the server); --http serves the same face over Streamable HTTP, loopback-only (public exposure waits for the OAuth 2.1 leg) |
| `precommit` | `mdllm precommit [path]` | the pre-commit legs (boundary + validate + coherence + candidates) run concurrently against one frozen candidate tree; composes the individual commands without changing their semantics |
| `provenance` | `mdllm provenance [--view {worktree,index,commit}] [--revision REV] [path]` | validate provenance chains (provenance.md) |
| `publish` | `mdllm publish [--authorize-once] [path]` | guarded publication: push the current commit only with standing literal git.autopush: true or an explicit one-shot human instruction; then use the repo's REAL default branch — branch READ (mdllm.defaultbranch / origin HEAD), never typed; checkout must match; remote ref must already exist (never creates one); fast-forward only; remote tip re-verified. Credentials: ambient, or GH_PAT / MDLLM_GIT_TOKEN via a command-scoped header (never on disk, redacted from output) for ephemeral containers where autopush honestly fails |
| `refresh` | `mdllm refresh [--seal] [path]` | floor-only domain refresh: report version delta + unseen CHANGELOG; --seal bumps seen |
| `runtime-probe` | `mdllm runtime-probe [path]` | report, per interpreter candidate, whether it exists and whether the floor's dependency loads — the reproducible runtime check for any harness's shell (framework root or a directly opened nested domain) |
| `scaffold` | `mdllm scaffold [--harness {all,claude,claude-code,codex,cowork,none,perplexity}] [--autopush {true,false}] path` | deterministic domain birth: templates, nested repo, .gitignore isolation, hook, first commit |
| `session-start` | `mdllm session-start [--contract] [--assert-head FULL_SHA] [path]` | emit the session-start ritual (version + velocity) for a harness startup hook to inject |
| `tokens` | `mdllm tokens [path]` | measure spec token costs by tier |
| `touchpoints` | `mdllm touchpoints id [path]` | Assimilate beat: what a thing's change disturbs (declared edges + literal refs) |
| `triggers` | `mdllm triggers [--estate] [path]` | evaluate trigger conditions; --estate sweeps every local clone with a roll-up (run after estate-sync) |
| `validate` | `mdllm validate [--quiet] [--view {worktree,index}] [path]` | Levels 1-3 mechanical validation |
| `watch` | `mdllm watch --role ROLE --definition DEFINITION [--run RUN] [--field FIELD] [--remote REMOTE] [--branch BRANCH] [--interval INTERVAL] [--exit-on-wake] [--once] [--state STATE] [path]` | the doorbell: poll the remote ref and report when a watched thing reaches a stage this role acts at; reads only, never writes |
| `worklog` | `mdllm worklog [--write] [path]` | print a session-grouped view of the commit stream (on-demand; not committed) |

<!-- /generated:toolbox -->

### When you'd type each one yourself

The table above is generated from the tool itself — `mdllm docs` rebuilds it,
and the pre-commit coherence leg refuses a commit where it has drifted. What
the tool cannot say is *when a human reaches for it*. That is authored, one
line per subcommand, here — and checked the other way: a subcommand with no
line, or a line for a subcommand that no longer exists, is a coherence Error.

- **`adapter-install`** — Run with `--dry-run` first. It preflights a *project-bound* adapter, shows every decision and the exact owned diff, and merges only the selected surface. `--refresh-legacy` replaces only an exact adapter-declared historical span, and only when doctor names a legacy ID — rerun without `--dry-run` only after reviewing that diff. A run-time-bound adapter has no install target; do not invent one.
- **`assemble`** — When a session starts somewhere the estate does not yet exist — a fresh cloud container, a new machine. It clones the configured domains, resolves their real default branches, installs the floor hooks, sets identity, leak-checks, then per domain runs sync and `session-start --contract` so the Tier-0 contract enters the transcript. Credentials are ambient or command-scoped, never on disk.
- **`autopush`** — Run by the post-commit hook; by hand only when diagnosing publication debt. It sends only when the repo literally declares `git.autopush: true` — false, absent or malformed is off — and a rejected push is surfaced as divergence, never forced.
- **`boundary`** — Before any publication event; `--history` for a full-archive audit. `--audit-terms` when the boundary starts refusing commits you believe are clean: it turns the check on the local gitignored `.boundary-terms` itself — an entry that occurs in this repo's *own tracked content* is either noise keeping the other legs permanently red, or a leak already committed — and reports by line number, never by term.
- **`bundle`** — When a run-time-bound harness (Cowork, Perplexity) needs its account-level bundle. The output names your private repos, so it lands in a gitignored build directory and is never committed.
- **`calc`** — Ingesting a statement or preparing a return: the tool does every sum over the `computed:` derivations a thing declares — a body table, a frontmatter list, a field across selected things — and `validate` re-checks the same blocks at every commit. Exit 1 on disagreement; `--expr` for an ad-hoc pivot. Grammar: `docs/calculation-reference.md`.
- **`candidates`** — When a pre-commit cue line surprises you: which staged things are reconciliation-cue candidates, and why.
- **`cascade`** — After completing a thing with dependants: "what did I just unblock?"
- **`changelog`** — Framework release prep: drafts the entry from the commit stream since a ref; you set the version and write the one-paragraph summary.
- **`coherence`** — After adding or removing a spec, or on suspected drift between a generated surface and its source. Corpus-general (generated artifacts, managed blocks — including this guide's — stale `stable` labels, dead vocabulary); the framework-only checks switch on at a `.markdownllm` root. Runs in the pre-commit hook, so you rarely type it.
- **`cues`** — When the digest's *Reconciliation cues* line is long and you want the full list, or before a retrospective (it is scan 4's work list); `--raise` when you would rather the floor wrote the open questions than remember to — a tick runs it, and only the verdicts are left for you.
- **`dispatch-payload`** — Only when hand-checking what a scheduled tick will hand a session, or composing the one-line command a host's job entry runs. It refuses to compose a launch with no stop condition. Registering the job stays your act — it is permission-bearing.
- **`docs`** — Framework maintenance after a CLI or spec change: regenerates the derived blocks in `docs/` — this table, and the map's edge list. You edit the authored lines (these bullets, the map's drawings); the blocks you never touch. `--check` is what the hook runs.
- **`doctor`** — New machine, new harness, after a refresh, or "is the floor actually on here?" With `--harness`, support, configuration, currency, trust, runtime and real-event execution are reported as independent facts — a runnable command never counts as an executed lifecycle event.
- **`domain-kernel`** — After a refresh, or when coherence reports a drifted managed block in a domain's AGENTS.md.
- **`estate-check`** — The estate-wide sync question, when you run more than one domain. Coverage `0/n` means the routes are not trusted in this clone, not that the imports are unverifiable.
- **`estate-sync`** — Plain mode at automatic session start; `--require-fresh` when you ask an agent to prove fresh state and want a restricted harness to route approval; `--status` at session end, for publication debt.
- **`eval`** — Regression check after framework or skill changes; `--run` for the framework-vs-bare experiment, which seeds an isolated workspace outside the repo, drives a headless agent, scores trials, and stops the arm if the seed moves. Run it from a terminal where `claude` holds its own credentials — a hosted session's token does not propagate to the child.
- **`external-trust`** — Before the first import read from a configured source, after any `.mcp.json` change, or to revoke a source without editing shared content. The record lives in `.git/`, uncommitted: a second machine grants again.
- **`harness-event`** — Never by hand. The installed project hook calls it to run one ordered lifecycle binding and record hash-bound execution evidence — what `doctor` correlates a real event against.
- **`imports-check`** — "Are my imports still honest?" — after a session in any producing domain, or on suspicion. `stale` means the source moved; `diverged` means the mirror did.
- **`index`** — Suspected index drift, or after bulk edits.
- **`install-hook`** — Once per domain repo at floor adoption, and again to pick up a newer hook body. Pre-commit composes the boundary, validate, coherence and cue legs concurrently against one frozen candidate (the first three block); commit-msg checks the disclosure boundary; post-commit is autopush, off unless declared.
- **`kernel`** — Framework maintenance after any spec change. CI and the hook run `--check` for you.
- **`mcp-serve`** — Stdio you rarely run by hand — the consumer's client spawns it. `--http` when a porch should outlive its callers, loopback-only until the OAuth 2.1 leg; `--token` mints a per-run bearer for tunnelled probes. Serves `exposed: true` things only, after the consumer has reviewed and trusted the exact `.mcp.json` entry.
- **`precommit`** — Never by hand; it is what the pre-commit hook runs. To see one leg's verdict without committing, run that command itself.
- **`provenance`** — Auditing why-trails before relying on a decision, or proving the exact candidate or commit that was assessed (`--view worktree|index|commit`; a commit revision resolves to a full immutable SHA).
- **`publish`** — Deliberate publication after reconciliation. Standing `git.autopush: true` authorises it; otherwise a human instructs this one event and the invocation names that with `--authorize-once` — an agent must never infer or self-grant it.
- **`refresh`** — Bringing a stale domain current with the framework. `--seal` only after you have adopted what it reported; a report never seals on its own.
- **`runtime-probe`** — When `doctor` says the floor's interpreter or dependency resolution is unclear on this machine or in this harness shell. Rarely by hand.
- **`scaffold`** — Creating a new domain: the mechanical half is one command. Omit `--harness` at a keyboard and it asks; headless it refuses with the list — there is no default. `none` proves the substrate does not depend on an adapter. Publication defaults to false; only a literal `--autopush true` enables sends.
- **`session-start`** — A configured adapter runs the ritual for you on an evidenced harness; by hand in any harness without one. `--assert-head <full-sha>` immediately before applying a full-corpus or other long-read result — it refuses if HEAD moved.
- **`tokens`** — Checking session-cost impact after spec edits.
- **`touchpoints`** — Before changing a load-bearing thing, or during an inflection walk: "what did I just put at risk?"
- **`triggers`** — "What needs attention?" without starting a full session; `--estate` after `estate-sync` when the question is "what needs doing across the estate?" It reads the working tree, so an uncommitted edit can fire one — the commit discipline is what makes tree and history agree.
- **`validate`** — Sanity-checking a domain's whole corpus on demand. The hook runs it on every commit against the staged candidate (`--view index`).
- **`watch`** — When a process must run while no session does: it polls the remote ref — never the worktree — and reports when a watched thing reaches a stage your `--role` acts at; `--run` scopes it to one workflow-run. Reads only; arming it is your act, and it wakes an agent rather than doing the work.
- **`worklog`** — Reviewing recent session history — an on-demand view, sessions split on `session-end:` commits; `--write` saves a gitignored local snapshot. Not a committed file.
Requires Python 3.10+ and PyYAML (`tiktoken` optional, for `tokens`).

### Harness adapters

Adapters harden the portable lifecycle; they are not the substrate. A domain
without one still operates through its entry contract and the Git floor. The
registry now contains two binding shapes:

- **Project-bound:** Claude Code and Codex render project artifacts. For an
  existing project, inspect before writing:

```powershell
./tools/mdllm.ps1 doctor . --harness codex
./tools/mdllm.ps1 adapter-install . --harness codex --dry-run
```

- **Run-time bound:** Cowork renders no project artifact; its account-level
  bundle binds when a session activates it. Doctor therefore reports project
  configuration/currency as not applicable. The adapter and bundle build are
  registered and tested, but remote/local live compatibility remains open in
  the Cowork plan; registration is not a compatibility row.

The current project renderers are implemented and covered by unit/integration
tests. The shared launch repair, Claude's ordered neutral-runner migration, and
both recognised root refreshes are complete. The framework root tracks current
`.claude/settings.json` and `.codex/hooks.json` as self-hosted project state;
nested domains were not batch-migrated.

Installing any reviewed diff remains an operator action. The
[official Codex hook documentation](https://developers.openai.com/codex/hooks) names
`/hooks` as a **CLI** inspection/trust command; it was not available in the
observed Desktop chat command palette, so Desktop and CLI trust evidence must
not be conflated. `doctor` reports execution as `untested` until a real
lifecycle event is correlated with harness-owned transcript evidence and a
fresh definition-hash-bound record. The installer never mutates user-global
Codex configuration.

Codex's lifecycle projection is verified on Codex CLI 0.147.0 / Windows 11,
and the Desktop managed shell has separate root and directly opened nested
domain runtime/Git evidence. Gate 7.0 additionally proved the dependency-
probing PowerShell route and the restricted-then-approved strict estate sync,
pre-commit, and publication path in QMS. Each fact keeps its own surface and
build; none is relabelled as global Codex compatibility or machine-readable
trust.

Claude Code's core framework path remains proven in use. Its current projection
uses one handler per lifecycle moment and enters the ordered neutral runner.
The historical two-handler form is recognised as `legacy-v1`; doctor names the
ID and the exact `--refresh-legacy --dry-run` command. Refresh replaces only
the owned `hooks` value span, preserving permissions and every unrelated byte.
Existing `.claude/settings.local.json` remains read-only; competing overlay
hooks, local command tails, malformed JSON, duplicates, and unknown stale
forms all refuse with zero writes.

## Running More Than One Domain

Each domain stays a sealed repo that is comprehensible by reading only itself
plus its quarantined external imports. When domains need each other's output,
the connection runs through three pieces — all operator-wired, none automatic:

- **The exposed face.** A producer opts individual things into its face with
  `exposed: true`; `mdllm mcp-serve` serves exactly that set (content and
  descriptive frontmatter — the internal relationship graph is stripped on
  egress). Nothing crosses by default; publication is an authoring decision.
- **The address book and its local authority.** A consumer's `.mcp.json`
  `mcpServers` map proposes which producers it may read and how to spawn them;
  repository content alone is inert. Review and hash-confirm an entry with
  `mdllm external-trust` in each clone. The uncommitted trust record is bound to
  the exact definition, so a changed command or URL returns to default-deny.
  Discovery is never organic — a domain is reached because it was listed and
  locally authorised.
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
mdllm estate-sync . --require-fresh  # manual sweep: cached state is not accepted as fresh
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

That non-blocking return is correct for automatic lifecycle startup, but it is
too weak when you explicitly ask an agent to prove the state is fresh. Use
`estate-sync --require-fresh` for that manual request. If network or `.git`
access is denied, the command keeps the truthful cached-state report but exits
nonzero, allowing Codex's restricted mode to ask for one-command approval and
retry the exact operation. The repository cannot grant its own sandbox
authority; this mode makes the missing authority mechanically visible.

The mirror runs at session end: `estate-sync --status` reports **publication
debt** — commits that are real on this machine and invisible to the estate.
When a repo explicitly declares `git.autopush: true`, this report is an
**anomaly detector** — any line means an offline session or a rejected push
awaiting your routing. False, absent, and malformed declarations are off; in
that mode the push stays yours and publication debt is expected
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

The honest summary: v3 did not make the system smarter. It made declared
mechanical discrepancies reproducible and blocking at an active commit
boundary, while leaving semantic interpretation probabilistic. When you do
spend attention, more of it can land on judgment instead of bookkeeping.

## Grilling A Session — The Probe Ladder

Sometimes you want to know whether the agent in front of you is actually
constituted as the domain agent, or just sounds like one. Five baseline
sessions (two vendors, three harnesses, four models, 2026-08-18/19) proved
two things: every session economises *somewhere*, and an honest itemised
ledger replicates across vendors when you ask the right way. The asking is
a ladder — each rung extracts a stratum the previous one can't:

1. **The casual probe** — *"Are you actually running as the domain agent?
   Did you follow the startup flow?"* This gets the broad confession or the
   smooth yes. Treat a smooth, unqualified "yes, all loaded" as the tell it
   is: a session that hadn't loaded anything would say exactly the same
   words. What you want is a ledger — file names, what was and wasn't done,
   declared skips.
2. **The forensic probe** — *"Does 'loaded' mean you read it end-to-end?"*
   This is the rung that catches believed compliance: a load command that
   executed but landed truncated produces a sincere overclaim that survives
   rung 1 (observed live: a kernel load that arrived cut, reported as
   "loaded" in good faith). Since the emission carries an integrity trailer
   (line count + sha256), you can ask the agent to account for both.
3. **The walk probe** — *"Did you perform the orientation walk, steps four
   to six?"* Separates relaying the digest from having judged it. The
   strongest sessions audit themselves *before* answering this one; weaker
   ones confess without completing. Either way you learn where this
   session economised — and the evidence says the gap moves every session,
   so hardening against the last session's gap buys nothing here.

Two practices make the ladder work: keep the wording close to verbatim
across sessions (probe precision bounds what the ledger reveals — "loaded?"
hides truncation, "end-to-end?" surfaces it), and demand evidence over
assurances — fingerprints in the output (the stall line applied, the
staleness check's actual findings) outrank any claim of having read
something.
