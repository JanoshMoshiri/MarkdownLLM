---
id: first-hour-guide
type: guide
status: evolving
version: 1.8
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
    notes: "v1.5 offered Explorer as an optional visual route; v1.8 drops it while Explorer is parked."
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: derived-from
    notes: "v1.6 named the eventual guided route while retaining the published first-hour path."
  - id: harness-native-onramp-supersedes-desktop
    relation: derived-from
    notes: "v1.7 recorded Desktop frozen and named the harness-native onramp; that onramp is paused, and v1.8 says so."
  - id: the-onramp-is-the-operators-own-sentence
    relation: references
    notes: "The domain-expert newcomer — ten minutes, four ideas — is the guide still to be written."
  - id: documentation-rulings-2026-10-20
    relation: implements
    notes: "v1.8 is package 5: workspace wording, the generated install pin, and an hour that ends in one whole session — /orient, real work, a refused commit walked, /end-session."
---

# The First Hour

## Who This Is For

You have never used this framework. You have an agent tool that can read
files, write files and run commands — Claude Code, Codex or Cowork — sixty
minutes, and a healthy suspicion of long guides. By the end of the hour you will
have a [workspace](glossary.md#workspace) of your own, you will have watched the
[floor](glossary.md#floor) refuse a mistake, and you will have run one whole
session from start to close.

Almost everything else in this repository is written for your agent to read.
This page and the [operator guide](operator-guide.md) are written for you. When
a word gets in the way, the [glossary](glossary.md) has its plain name; if you
are still deciding whether to use this at all, [limitations](limitations.md)
says when a notes folder would serve you better.

## What This Is, In Three Sentences

You describe something you want to track and reason about over time, and your
agent builds it as a workspace: a folder of markdown records with structured
headers, in its own git repository. A small tool, `mdllm`, runs at every commit
and refuses anything that breaks the workspace's declared structure. The agent
reasons about meaning, and the questions it may not settle on its own come to
you.

## Minutes 0–10: Install, Then a Look Around

Follow [Get started](../README.md#get-started) in the README: it fetches the
newest release by its exact commit, checks the installer's SHA-256, and runs it.
Do not pipe a moving branch into a shell. The installer finishes on an
`mdllm doctor` report that should read **FLOOR ACTIVE**.

Below, `mdllm <command>` means the repository's tool: on Windows run
`./tools/mdllm.ps1 <command>`, elsewhere `sh tools/mdllm.sh <command>`.

Before involving the agent, look at two files yourself:

1. **One real record.** Open
   `examples/life-manager/things/task-choose-worktop.md`. That is the whole
   unit of the system: a header of structured fields (identity, status, dates,
   links — what the tool checks) above a plain body (context and reasoning —
   what the agent reads). Every workspace is files shaped like this. The
   framework calls each one a [*thing*](glossary.md#thing).
2. **The example's entry file.** Skim the headings of
   `examples/life-manager/AGENTS.md`. This is what the agent reads on arrival:
   what the workspace is, which record types exist, what to do first. Yours
   will be written for you.

Skip `domain-specification-guide.md` — that one is your agent's reading.

## Minutes 10–15: Confirm the Agent Found the Framework

Open the `MarkdownLLM` folder in your agent tool and ask:

> What is this repository, and what would you do here on my behalf?

A correctly oriented agent answers in the framework's terms — workspaces,
records, skills, the floor. If it answers generically ("this appears to be a
documentation project"), your tool did not find `AGENTS.md` on its own. That
happens; it is a property of the tool, not of the framework. One pasted line
fixes it:

> Read AGENTS.md at the repository root and follow its startup instructions
> before anything else.

## Minutes 15–40: Create a Real Workspace

Pick something real but small — expense tracking, a hiring pipeline, your
allotment. Real, because an invented subject teaches you nothing about the fit;
small, because the structure grows with use by design. Say what you want in one
honest paragraph:

> I want a workspace for tracking my freelance clients: each client, the
> projects I run for them, invoices and whether they're paid. I care most about
> never losing track of an unpaid invoice.

What should happen, and what you do:

- **The agent proposes** record types, skills and a folder structure, and asks
  you to confirm. Rename the types into *your* words and cut anything you do not
  recognise as yours. You know the subject; it knows the structure.
- **The agent builds it as its own repository.** The workspace gets its own git
  history, and the framework ignores its folder. The mechanical half is one
  command the agent should reach for: `mdllm scaffold <path> --harness
  <selection>` (`claude`, `codex`, `cowork`, `all` or `none` — omit it and it
  asks). A red flag worth catching now: the workspace's files appearing in the
  *framework's* `git log`.
- **You get a seed record or two**, not an empty shell. Ask for one if you
  don't.

When it is done, open the workspace's own folder in your agent tool. From now on
you work there; the framework folder is only for creating workspaces and
changing the framework itself.

## Minutes 40–45: Watch the Floor Catch Something

`scaffold` installed git hooks in your workspace: the floor runs before every
commit. Prove it bites — open any record, change its `status:` to `banana`, and
run

```
mdllm validate .
```

You get an Error naming the file, the field and the legal values; with the hooks
installed, that same Error would have refused the commit. Revert it.

That is the framework's core bargain. Everything mechanical — structure,
references, vocabularies — is checked by code at the commit. Neither the agent
nor you spot-checks it by eye. What stays yours and the agent's is what code
cannot check: whether a status is *true*, whether a link *means* something,
whether the text still matches the world.

## Minutes 45–60: One Whole Session

This is what every working session looks like from here on. In Claude Code the
start and the end are typed commands; in another tool, say "orient" and "end the
session" and the agent runs the same steps.

1. **Start: `/orient`.** The agent is handed the framework's rules and your
   workspace's current state whole, then tells you in plain words what matters
   today — what changed, what is due, what is stuck. It should read like a
   colleague catching you up, not a dashboard. ([orient](glossary.md#orient))
2. **Work by talking.** "Add the client I signed yesterday, invoice due at the
   end of the month." The agent writes the records and commits as it goes; `git
   log` in the workspace shows each step.
3. **Change something other records rely on.** Ask for a rule to change — "our
   payment terms are 14 days now, not 30" — where the rule lives in the
   workspace's skills or a record others link to. Where the tool runs the commit
   gate (Claude Code does), the agent cannot commit that change until it has read
   every record that depends on it. It tells you which still hold, which it
   revised, and asks you only what it may not settle — "do existing invoices keep
   30 days?" Your answer is committed with the change. That refusal is the point:
   nothing a later session relies on changes silently. ([walk](glossary.md#walk))
4. **End: `/end-session`.** The close: anything worth keeping becomes a lesson
   on record, up to ten open items are decided, and the ones only you can rule on
   come to you as one question with options. The session ends in a commit;
   nothing is left uncommitted. ([the close](glossary.md#the-close))

That loop — orient, talk, rule, close — is the whole system. Everything else is
refinement.

## What to Read Next

- **[Operator guide](operator-guide.md)** — the steady state: what the tooling
  carries for you, the eight recurring scenarios, what remains your job.
- **[Glossary](glossary.md)** — keep it open; every coined word has a row.
- **[Framework map](framework-map.md)** — how the specifications relate, for
  when you are curious what is underneath.

The specifications are your agent's operating manual; read them when you want
to, not because you must.

## Honest Footnotes for Hour One

- **The person this framework most needs to reach is not yet written for.** This
  guide assumes a terminal and a healthy suspicion. A guide for someone who will
  never open a terminal would be ten minutes and four ideas: the agent writes
  things down in files you can read; nothing is real until it is committed, and
  you can always see what changed; the agent proposes, and some things only you
  can rule on; what you rule on accumulates. The route that would serve them —
  your agent doing this hour's setup for you — is planned and paused
  (`operator-seat-and-harness-native-onramp`).
- **Finding the entry file varies by tool.** Claude Code and the named Codex
  builds have execution records; Copilot, Cursor, Windsurf and Gemini are
  designed for but not yet exercised. The pasted bootstrap line works in any
  tool that can read files, but it is manual, not proof of auto-loading.
- **The floor needs Python.** If the hooks cannot run on some machine (no Python,
  sandboxed git), you are in degraded mode: ask the agent to run `mdllm
  validate` before each commit and say so out loud. `mdllm doctor <path>
  --harness <name>` checks whether the hooks actually *run*, not just exist.
- **Your workspace is born without permission to publish.** Its `AGENTS.md`
  declares `git.autopush: false`. If automatic pushing is what you want, choose
  it at birth (`mdllm scaffold <path> --autopush true`) or change the
  declaration later, and add the remote yourself.
- **Some words should never reach a commit.** `scaffold` gave your workspace a
  local `.boundary-terms` file, never committed. List client names or personal
  identifiers there and the hooks refuse any commit that would carry them.
- **If validation blocks a legitimate change**, the schema is wrong, not you:
  extend `things/_schema.yaml` with the agent rather than fighting the finding.
