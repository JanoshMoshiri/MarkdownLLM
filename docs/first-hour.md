---
id: first-hour-guide
type: guide
status: evolving
version: 1.6
created: 2026-06-12
linked_things:
  - id: operator-guide
    relation: complements
    notes: "This guide covers arrival; the operator-guide covers the steady state"
  - id: domain-specification-guide
    relation: references
  - id: framework-map
    relation: references
  - id: framework-discovery-specification
    relation: references
  - id: explorer-publication-position
    relation: derived-from
    notes: "v1.5 offers Explorer as an optional visual orientation path, never as a prerequisite or agent route."
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: derived-from
    notes: "v1.6 names the eventual guided route while retaining the current published first-hour path until acceptance."
---

# The First Hour

## Who This Is For

You have never used this framework. You have an agent harness that can read
files, write files, and run commands, sixty minutes, and a healthy suspicion
of 850-line guides. Named products differ in how they discover entry files and
bind lifecycle events; the compatibility table records what has actually been
exercised rather than treating a product list as proof.

Almost everything else in this repository is written for your agent to read.
This document and the `operator-guide.md` are the two written for you — this
one for your first hour, the operator's guide for every hour after that. You
do not need to read any specification to finish this page.

## What This Is, In Three Sentences

You describe a domain — anything you want to track and reason about over
time — and your agent builds it as a folder of markdown files with structured
YAML headers, in its own git repository. A supported entry route delivers the
domain contract; the agent reasons within that structure and updates it as your
situation changes — git records the accepted state. A small Python tool
(`tools/mdllm.py`) plus a set of current, runnable git hooks deterministically
checks structural invariants and blocks commits with mechanical Errors. The
agent remains a probabilistic interpreter responsible for meaning.

## Minutes 0–10: Install, Then a Look Around

Use the [verified release installation](../README.md#getting-started): fetch the
named immutable commit, confirm the checked-out commit and installer SHA-256,
then run the local script. Do not pipe a moving branch into a shell. The
verified sequence provisions the exact PyYAML runtime before invoking the
published installer, installs the hooks, and finishes on a `doctor` report that
should read **FLOOR ACTIVE**. That pre-install matters because the published
v3.32.0 scripts predate the dependency pin now present in the next-release
installers. The README also names the remaining trust roots; release metadata
is not yet signed.

Open the verified checkout; then, before involving the agent, look at two things
yourself:

In the prose below, `mdllm <command>` means this repository's CLI. On Windows
PowerShell use `./tools/mdllm.ps1 <command>`; elsewhere use
`python tools/mdllm.py <command>` only with a Python that can import PyYAML.

1. **One real thing.** Open
   `examples/life-manager/things/task-choose-worktop.md`. That is the entire
   atom of the system: YAML frontmatter (identity, status, dates, links — what
   the machine reads) above a markdown body (context and reasoning — what the
   agent reads). Every domain is just files shaped like this.
2. **The example's `AGENTS.md`.** Open `examples/life-manager/AGENTS.md` and
   skim the headings only. This is the file an agent reads on arrival: what
   the domain is, what types exist, what to do on startup. Your domain will
   get one of these, written for you.

**Optional visual route.** If you have installed the [MarkdownLLM Explorer
Windows preview](../explorer/docs/installation-guide.md), open it now. On a Mac,
ask the framework agent to **open MarkdownLLM Explorer** and it will bootstrap
the portable viewer. Use the substrate and domain lists to look around. It is a
read-only orientation aid, not part of installing the floor and not a
replacement for the agent that will create or change a domain. Nothing in the
rest of this first hour depends on it.

MarkdownLLM Desktop is being built as the eventual guided first-use route—setup, Domains,
Sessions, provider connection and this visual inspection in one local application. It remains an
Engineering Preview under acceptance, so this guide does not silently substitute it for the
published framework installation route yet.

The README is the one-page overview if you want the *why*; skip
`domain-specification-guide.md` entirely — that one is your *agent's* reading,
not yours.

## Minutes 10–15: Confirm the Agent Found the Framework

Open the framework folder as a workspace and ask your agent:

> What is this repository, and what would you do here on my behalf?

A correctly oriented agent answers in terms of `AGENTS.md` — domains, things,
skills, the validation floor. If it answers generically ("this appears to be
a documentation project"), your harness did not auto-discover `AGENTS.md`.
That happens; discovery is a harness property, not a framework property.
The fix is one pasted line:

> Read AGENTS.md at the repository root and follow its startup instructions
> before anything else.

## Minutes 15–45: Scaffold a Real Domain

Pick something real but small — expense tracking, a hiring pipeline, your
allotment. Real, because invented domains teach you nothing about the fit;
small, because the structure grows with use by design. Then say what you
want in one honest paragraph, for example:

> I want a domain for tracking my freelance clients: each client, the
> projects I run for them, invoices and whether they're paid. I care most
> about never losing track of an unpaid invoice.

What should happen next — and what you should do:

- **The agent proposes** thing types, skills, and a folder structure, and
  asks for confirmation. The proposal is yours to shape: rename types to
  *your* words, cut anything you don't recognise as yours. You are the
  domain expert; it is the structure expert.
- **The agent builds in isolation.** A new domain gets its *own* git
  repository, and the domain folder is added to the framework's
  `.gitignore`. This is mandatory, not stylistic — your domain's history
  stays yours. The mechanical half of this is one command
  (`mdllm scaffold <path> --harness <selection>`), which the agent should
  reach for. Select `claude`, `codex`, `cowork`, `all`, or `none`; omitting
  the flag preserves the current Claude compatibility default. `none` keeps
  the entry contract and Git floor but installs no lifecycle adapter, while a
  run-time-bound selection such as Cowork has no project artifact to write.
  Red flag worth catching in hour one: domain files appearing in the
  *framework's* `git log`.
- **You get a seed thing or two**, not an empty shell. Ask for one if you
  don't get one.

When it's done, open the domain folder as its own workspace. From now on you
talk to *that* agent, in that workspace; the framework workspace is only for
framework work.

## Minutes 45–55: Watch the Floor Catch Something

The floor should now be in place — the installer set it up for the framework, and
`scaffold` installed the git hooks inside your new domain (validation before
each commit, a disclosure check on the commit message, publication after).
Prove it bites: open any thing in your domain, change its `status:` to
`banana`, and run

```
mdllm validate <path-to-your-domain>
```

You get an Error naming the file, the field, and the legal values — and with
the hook installed, that same Error would have *blocked the commit*. Revert it.

That sixty-second exercise is the framework's core bargain: everything
mechanical — structure, references, vocabularies — is checked by code at the
commit boundary. The agent never spot-checks those by reasoning, and neither
do you. What stays yours and the agent's is what code cannot check: whether
a status is *truthful*, whether a link is *meaningful*, whether the narrative
still matches reality.

## Minutes 55–60: One Real Session

In your domain workspace, do one piece of real work by talking — "add the
client I signed yesterday, invoice due end of month." Watch what lands in
git: the agent commits as it writes (`git log` in the domain shows the event
stream). Then stop. That loop — talk, files change, git records the accepted
state — is the whole system; unrecorded reasoning is not a complete audit
trace, and everything else is refinement.

## What to Read Next

- **`operator-guide.md`** — the steady state: what the tooling carries for
  you, the seven recurring scenarios, what remains irreducibly your job.
- **`framework-map.md`** — one visual page of how the specs relate, for when
  you're curious what's underneath.
- **Explorer's `user-guide.md`** — the short visual walkthrough if you prefer
  to inspect the estate through the optional Windows preview.
- Nothing else. The specifications are your agent's operating manual; read
  them when you *want* to, not because you must.

## Honest Footnotes for Hour One

- **Discovery varies by harness.** Claude Code's scaffolded `CLAUDE.md` →
  `AGENTS.md` pointer route and named Codex entry/lifecycle surfaces have
  execution records; Copilot, Cursor, Windsurf, and Gemini remain designed-for
  where no framework record exists. The pasted bootstrap line works in a
  file-aware session, but it is manual discovery, not proof of auto-load.
- **The floor needs Python.** If the hook can't run on some machine (no
  Python, sandboxed git), you are in degraded mode: ask the agent to run
  `mdllm validate` manually before each commit and say so out loud.
  `mdllm doctor <path> --harness <name>` checks all of this mechanically —
  including whether the hook actually *executes*, not just exists — and
  tells you which mode you're in.
- **Session-start hardening uses one ordered handler.** Current Claude launches
  matching handlers in parallel, so the historical two-handler projection is
  retained only as recognised migration data. New scaffolds emit one handler
  entering the neutral ordered runner. Existing project permissions and
  settings remain untouched unless their operator reviews and explicitly runs
  `adapter-install --refresh-legacy`; extensions and ambiguity still refuse.
  Copilot lifecycle compatibility remains a separate unverified claim.
- **Your scaffolded domain is born without publication authority.** Its
  AGENTS.md literally declares `git.autopush: false`, and false, absence, or a
  malformed value are all off. If automatic publication is the deliberate
  choice, make it at birth with `mdllm scaffold <path> --autopush true` (or
  change the declaration later) and add the remote explicitly. The post-commit
  hook can then publish each validated commit through `mdllm autopush`; no
  repository gets publication authority by omission.
- **Some words should never reach a commit.** `scaffold` gave your domain a
  local `.boundary-terms` file (never committed, never cloned). List client
  names or personal identifiers there and the commit-msg/pre-commit hooks block
  any commit that would carry them — with no trace of the terms themselves in
  the repository.
- **If validation blocks a legitimate change**, the schema is wrong, not
  you: extend `things/_schema.yaml` with the agent rather than fighting the
  finding.
