# MarkdownLLM

*Records your agent keeps in markdown and git — where nothing a later session relies on changes silently.*

[The guides as a site](https://janoshmoshiri.github.io/MarkdownLLM/) · [First hour](docs/first-hour.md) · [Glossary](docs/glossary.md) · [Limitations](docs/limitations.md)

## What it is

Every agent session starts from scratch, so you hand the agent its context
back — and after hundreds of sessions the hard question stops being *how do I
retrieve this* and becomes *is any of it still true*. Other systems let a model
settle that on its own, or re-check a memory when it is next read: Zep
time-stamps facts and invalidates the old ones, GitHub Copilot re-verifies a
memory against the branch, Letta's background pass consolidates without asking,
Karpathy's LLM wiki has a lint step, Hermes keeps a short memory page the agent
rewrites itself.

**MarkdownLLM refuses to let a model settle that question silently.**

- A **workspace** is a folder of plain markdown records in git, each with typed
  frontmatter the workspace declares for itself.
- A deterministic checker — the **floor** — runs at every commit and refuses
  broken structure, broken links and anything the workspace's schema does not
  allow.
- A change to something other records rely on raises a recorded question over
  everything that depends on it. The agent works through it, you rule on what
  the agent may not settle, and the ruling is committed. The history is the git
  log, not a retention window.

Most of the parts are old and borrowed — the [glossary](docs/glossary.md) gives
each word its plain name and its prior art. What is specific is the assembly.

## Who it is for, and who it isn't

For anyone keeping records an agent will reason from for longer than anyone
will remember writing them: a regulated quality system, a set of procedures, a
body of decisions, a personal finance ledger. No expertise is needed at the
door — what the framework asks of you is the standing to say "this is true in
my workspace", and the floor supplies the record-keeping discipline.

It is the wrong tool for high-volume transactional data, many concurrent
writers, sub-second answers, relational queries, or more than about 1,000
active records in one workspace. For one person, one project and memory that
only needs to last weeks, a `CLAUDE.md` and a notes folder is cheaper —
[limitations](docs/limitations.md) says exactly where the line is.

## What a session looks like

```text
you    › /orient
agent  › Rules and today's state loaded. Two things matter: the refund policy
         changed last week, and the Q3 report is due in nine days.
you    › Raise the refund approval limit to £400.
agent  › Edited the rule. The commit was refused: seven records rely on it.
         I walked them — five still hold, I revised one (a worked example), and
         one needs you: does the new limit apply to refunds already queued?
you    › No, queued refunds keep the old limit.
agent  › Recorded your ruling and committed the change, its walk and the answer.
you    › /end-session
```

## What a record looks like

```markdown
---
id: refund-approval-limit
type: rule              # the workspace's own types, declared in _schema.yaml
status: current
created: 2026-04-01
linked_things:
  - id: finance-policy-2026
    relation: derived-from
---

# Refund approval limit

Support may refund up to £250 without a manager. Above that, the refund
waits for the finance lead's approval.
```

## How it's laid out

```text
MarkdownLLM/                 the framework: specifications, the mdllm tool, the floor
└── domains/
    └── your-workspace/      its own git repository, ignored by the framework's
        ├── AGENTS.md        the agent's entry contract
        ├── skills/          how to read, write and run this workspace
        └── things/          the records
```

The framework and each workspace version independently. You create workspaces
from the framework folder, then open a workspace's own folder in your agent tool
and work there.

## Get started

You need git, Python 3.10 or later, and an agent tool that can read and write
files — Claude Code, Codex or Cowork today.

<!-- generated:install -->

The newest release is **3.50.0**, commit `f100b16b3c9d`. Fetch exactly
that commit, check the installer's bytes, then run it:

```bash
# macOS / Linux
RELEASE_COMMIT=f100b16b3c9d9b780decd69e146c91001aa3bd08
INSTALLER_SHA256=cf9ec80117912db8077ae92e10eb718c53f3d49b42485538fdd8b54354eeb7c6
git init MarkdownLLM
git -C MarkdownLLM config core.autocrlf false
git -C MarkdownLLM remote add origin https://github.com/JanoshMoshiri/MarkdownLLM.git
git -C MarkdownLLM fetch --depth 1 origin "$RELEASE_COMMIT:refs/remotes/origin/verified-release"
git -C MarkdownLLM checkout --detach "$RELEASE_COMMIT"
test "$(git -C MarkdownLLM rev-parse HEAD)" = "$RELEASE_COMMIT"
cd MarkdownLLM
printf '%s  install.sh\n' "$INSTALLER_SHA256" | sha256sum -c -
./install.sh
```

```powershell
# Windows (PowerShell 7+)
$ReleaseCommit = 'f100b16b3c9d9b780decd69e146c91001aa3bd08'
$InstallerSha256 = 'ae3444fc655e04ff55a06eb8d412af40904bb6164e55e5d1c3a9913ff156be01'
git init MarkdownLLM
git -C MarkdownLLM config core.autocrlf false
git -C MarkdownLLM remote add origin https://github.com/JanoshMoshiri/MarkdownLLM.git
git -C MarkdownLLM fetch --depth 1 origin "${ReleaseCommit}:refs/remotes/origin/verified-release"
git -C MarkdownLLM checkout --detach $ReleaseCommit
if ((git -C MarkdownLLM rev-parse HEAD) -ne $ReleaseCommit) { throw 'release commit mismatch' }
Set-Location MarkdownLLM
if ((Get-FileHash ./install.ps1 -Algorithm SHA256).Hash.ToLowerInvariant() -ne $InstallerSha256) { throw 'installer hash mismatch' }
./install.ps1
```

<!-- /generated:install -->

The installer checks prerequisites, installs PyYAML 6.0.3 and the git hooks, and
verifies the result with `mdllm doctor`. The pin above is written by `mdllm
docs` from the newest `release:` commit and checked at every commit, so it moves
with each release. The trust roots are this repository's identity and TLS, git,
and the package sources the installer offers to use with your consent; releases
are not yet signed.

Then open the `MarkdownLLM` folder in your agent tool and say what you want:

> "I want a workspace for tracking architectural decisions across our services —
> each decision with its context, the options, the choice and its consequences."

The agent proposes a structure and builds it; you open the new workspace's
folder and work there. In Claude Code, start each session with `/orient` and
end it with `/end-session`. **[The first hour](docs/first-hour.md)** is the paced
walkthrough, including the floor refusing a deliberate mistake.

## Which agent tools work

The contract is plain files plus git, so it is portable by design — but whether
a product finds the entry file and runs the hooks is measured per product, not
assumed.

| Tool | Status | Evidence |
|---|---|---|
| Claude Code | Verified: entry file, lifecycle hooks, adapter-free floor; `/orient` accepted on 2.1.283 | [root dispatch](evidence/claude-phase6-no-adapter-and-root-2026-08-16.md) · [no-adapter probe](evidence/claude-no-adapter-entry-probe-2026-08-17.md) · [session start](things/plans/session-start-hardening.md) |
| Codex CLI | Verified on 0.147.0, Windows 11 | [live dispatch](evidence/codex-cli-live-dispatch-2026-08-14.md) · [acceptance](evidence/codex-phase6-post-6r-acceptance-2026-08-16.md) |
| Codex desktop | Verified on the named builds, framework and nested workspaces | [operator acceptance](evidence/codex-gate-7-0b-qms-operator-acceptance-2026-08-18.md) |
| Codex Cloud | Framework half shipped; live acceptance paused | [adapter](adapters/codex-cloud.md) |
| Cowork | Adapter registered; live verification open | [remote evidence](evidence/cowork-remote-phase5-evidence-2026-08-19.md) |
| OpenClaw | Adapter built and accepted locally; package not yet published | [integration](integrations/openclaw/README.md) |
| Copilot, Cursor, Windsurf, Gemini CLI | Designed for; no execution record yet | — |

Nothing without filesystem access — a chat window, a bare API call — can run
it. On Windows run the tool as `tools/mdllm.ps1`, elsewhere as
`sh tools/mdllm.sh`. Per-tool setup is in the [operator guide](docs/operator-guide.md).

## What is claimed, and what isn't

- **Shown:** typed records validated at every commit; a change to what other
  records rely on refused until a recorded question names every dependant,
  and that question held open at each session start until it is answered;
  decisions pinned to the commits they rest on; a workspace's whole history
  readable in git. The framework runs itself this way.
- **A hypothesis, not a result:** that this structure lets a smaller model match
  a larger one without it. One evaluation pointed that way and then saturated;
  the [eval record](things/artifacts/eval-record-2026.md) has the honest reading,
  and no conclusion is drawn until a harder test runs.
- **Not yet shown:** use by anyone outside the author's own workspaces, and
  coherence held over months measured against a plain notes folder.

## Read next

| | |
|---|---|
| [First hour](docs/first-hour.md) | install, create a workspace, one whole session |
| [Glossary](docs/glossary.md) | every coined word, its plain name, its prior art |
| [Limitations](docs/limitations.md) | when not to use this, and what the other memory systems do |
| [Operator guide](docs/operator-guide.md) | the steady state: what the tooling carries for you, the toolbox |
| [Several workspaces](docs/estate-mechanics.md) | sync, publication and change across repositories |
| [Framework map](docs/framework-map.md) | the specifications and how they connect |
| [AGENTS.md](AGENTS.md) | the agent's entry contract — the spec catalog and the principles live there |
| [CHANGELOG](CHANGELOG.md) · [reviews](reviews/) · [evidence](evidence/) | what shipped, what was reviewed, what was verified |

## FAQ

**Why not just a `CLAUDE.md` and a notes folder?** Often you should —
[limitations](docs/limitations.md) says when. The folder fails one specific way:
when a rule changes, nothing knows which notes relied on it, and the agent reads
whichever it opens. Here the commit is refused until a recorded question names
every note that relied on the rule; the agent walks them, you rule on what it
may not settle, and the question stays open at every session start until it
is answered.

**Do I need to understand the specs?** No. They are written for the agent. You
need to know your own workspace.

**Why markdown and git?** Agents and people can both read and diff them, and
git keeps every accepted change with its reason.

**Why "MarkdownLLM"?** Markup pointed text at a parser; markdown pointed it back
at a person; the LLM is the first machine that reads it on human terms.

**Is it production-ready?** It runs daily across more than a dozen private
workspaces — regulated compliance, finance and life operations among them — on
several machines. Each specification carries its own maturity (`draft`,
`evolving`, `stable`); `examples/` are small validated demonstrations, not
production load.

## Contributing · Licence

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licence — see [LICENSE](LICENSE).
Copyright (c) 2026 Janosh Moshiri.
