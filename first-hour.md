---
id: first-hour-guide
type: guide
status: draft
version: 1.0
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
---

# The First Hour

## Who This Is For

You have never used this framework. You have an agent harness (Claude Code,
Copilot, Cursor, Codex — anything that reads files, writes files, and runs
commands), sixty minutes, and a healthy suspicion of 850-line guides.

Almost everything else in this repository is written for your agent to read.
This document and the `operator-guide.md` are the two written for you — this
one for your first hour, the operator's guide for every hour after that. You
do not need to read any specification to finish this page.

## What This Is, In Three Sentences

You describe a domain — anything you want to track and reason about over
time — and your agent builds it as a folder of markdown files with structured
YAML headers, in its own git repository. From then on, the agent reads those
files at the start of every session, reasons within the structure they
declare, and updates them as your situation changes — git is the memory.
A small Python tool (`tools/mdllm.py`) plus a git pre-commit hook mechanically
blocks structurally broken changes, so the agent's reliability is spent on
reasoning, not bookkeeping.

## Minutes 0–10: Prerequisites and a Look Around

You need: `git`, Python 3.10+, and PyYAML (`pip install pyyaml`). Clone the
framework repository and open it — but before involving the agent, look at
two things yourself:

1. **One real thing.** Open
   `examples/life-manager/things/task-choose-worktop.md`. That is the entire
   atom of the system: YAML frontmatter (identity, status, dates, links — what
   the machine reads) above a markdown body (context and reasoning — what the
   agent reads). Every domain is just files shaped like this.
2. **The example's `AGENTS.md`.** Open `examples/life-manager/AGENTS.md` and
   skim the headings only. This is the file an agent reads on arrival: what
   the domain is, what types exist, what to do on startup. Your domain will
   get one of these, written for you.

Skip the README's full depth and skip `domain-specification-guide.md`
entirely — that one is your *agent's* reading, not yours.

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
  stays yours. Red flag worth catching in hour one: domain files appearing
  in the *framework's* `git log`.
- **You get a seed thing or two**, not an empty shell. Ask for one if you
  don't get one.

When it's done, open the domain folder as its own workspace. From now on you
talk to *that* agent, in that workspace; the framework workspace is only for
framework work.

## Minutes 45–55: Install the Floor and Watch It Catch Something

From the framework folder:

```
python tools/mdllm.py install-hook <path-to-your-domain>
python tools/mdllm.py validate <path-to-your-domain>
```

Then break something on purpose: open any thing in your domain, change its
`status:` to `banana`, and run validate again. You get an Error naming the
file, the field, and the legal values — and with the hook installed, that
Error would have *blocked the commit*. Revert it.

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
stream). Then stop. That loop — talk, files change, git remembers — is the
whole system; everything else is refinement.

## What to Read Next

- **`operator-guide.md`** — the steady state: what the tooling carries for
  you, the six recurring scenarios, what remains irreducibly your job.
- **`framework-map.md`** — one visual page of how the specs relate, for when
  you're curious what's underneath.
- Nothing else. The specifications are your agent's operating manual; read
  them when you *want* to, not because you must.

## Honest Footnotes for Hour One

- **Discovery varies by harness.** Auto-discovery of `AGENTS.md` is measured
  on Claude Code; other harnesses are designed-for but not all verified-on.
  The pasted bootstrap line above works everywhere.
- **The floor needs Python.** If the hook can't run on some machine (no
  Python, sandboxed git), you are in degraded mode: ask the agent to run
  `mdllm validate` manually before each commit and say so out loud.
- **If validation blocks a legitimate change**, the schema is wrong, not
  you: extend `things/_schema.yaml` with the agent rather than fighting the
  finding.
