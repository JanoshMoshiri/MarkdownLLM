# MarkdownLLM adapter for OpenClaw

This package binds explicitly designated OpenClaw agents to the MarkdownLLM
session-start lifecycle. OpenClaw keeps ownership of agents, sessions and
conversation history. MarkdownLLM keeps ownership of domain discovery, Git
state, validation and workflow state.

The initial public release is version 0.1.0. Compatibility is bounded to
OpenClaw 2026.9.3 while the Plugin SDK remains experimental.

## Requirements

- Node.js 24 or later.
- OpenClaw 2026.9.3. Later OpenClaw releases are not claimed compatible until
  this package has been retested and its bounded ranges updated.
- A MarkdownLLM checkout containing the domain entry and framework root.
- A trusted MarkdownLLM launcher available as an argv-safe executable path.

## Installation

For a local source-checkout verification:

```bash
cd integrations/openclaw
npm ci
npm test
npm pack
openclaw plugins install npm-pack:/absolute/path/to/markdownllm-openclaw-adapter-0.1.0.tgz --force --accept-capabilities
```

Use the documented `npm-pack:` prefix. It exercises OpenClaw's managed npm
project and lockfile verification; installing the same file as a raw archive
does not prove the registry-shaped installation path.

Install the pinned public package:

```bash
openclaw plugins install @markdownllm/openclaw-adapter@0.1.0 --pin
```

Review the package and its native plugin code before installation: an OpenClaw
plugin executes inside the Gateway process.

## Configuration

Before any lifecycle step runs, MarkdownLLM verifies that the resolved workspace
contains a domain `AGENTS.md`, that its relative `framework_root` (or the
specified ancestor fallback) reaches a valid `.markdownllm` sentinel and
`kernel.md`, and that the entry declares a domain name. A refusal is injected
as failed advisory context; it never certifies or runs the ordered startup.

Register each MarkdownLLM domain against one OpenClaw agent. Each agent's
configured workspace must be the entry for exactly one domain; domain ids and
agent ids are unique.

Merge this shape into `openclaw.json`:

```json5
{
  agents: {
    entries: {
      engineering: {
        workspace: "/domains/engineering"
      }
    }
  },
  channels: {
    telegram: {
      actions: { createForumTopic: true }
    }
  },
  plugins: {
    entries: {
      markdownllm: {
        enabled: true,
        hooks: { allowConversationAccess: true },
        config: {
          domains: {
            engineering: {
              agentId: "engineering",
              topicName: "Engineering"
            }
          },
          command: "mdllm",
          commandArgs: [],
          timeoutMs: 115000
        }
      }
    }
  }
}
```

`actions.createForumTopic` is an explicit host permission. Without literal
`true`, `/domain open` can find existing routes but will not create a
Telegram topic.

## Telegram domain commands

The owner-only command surface is:

```text
/domain
/domain list
/domain open engineering
```

`/domain` shows the domain, agent, workspace and Telegram topic bound to the
current conversation. `/domain list` shows registered domains and whether
each already has a topic in the current Telegram supergroup.

`/domain open engineering` verifies the Engineering agent workspace and its
`AGENTS.md` before creating anything. It then reuses an existing routed topic
or creates a new forum topic, persists that topic's `agentId` through
OpenClaw's config mutation API, and returns the topic link. Opening the link and
sending the first message causes the existing lifecycle hook to run
session-start inside the Engineering workspace.

The command never changes the current agent's working directory and never
rebinds the current QMS or other domain session. There is deliberately no
`/domain bind` operator command: selection happens by opening the isolated
domain topic whose route already points at the correct agent and workspace.

OpenClaw 2026.9.3 requires the explicit `allowConversationAccess` consent for
all external `before_prompt_build` hooks. The adapter ignores raw conversation
content, but the host permission still applies to the hook category. Without
it, OpenClaw loads only the four non-conversation lifecycle hooks and blocks
the context projection.

The adapter invokes the configured mdllm executable directly with argument
arrays. It never invokes a shell and never edits OpenClaw session storage.
The default command is mdllm. commandArgs can prefix the lifecycle arguments
when the floor is launched through an interpreter; for example, configure the
Python executable as command and the absolute tools/mdllm.py path as the first
commandArgs item. Paths are passed as argv values, so spaces do not require
shell quoting.

Verify the installed runtime:

```bash
openclaw plugins enable markdownllm --accept-capabilities
openclaw plugins inspect markdownllm --runtime --json
openclaw plugins doctor
```

The inspection must report `status: "loaded"`, `hookCount: 5`, a
`before_prompt_build` typed hook and no diagnostics. Restart the Gateway after
plugin code changes.

## Standing watch bridge

The package also builds the `markdownllm-openclaw-watch` command. It runs the
framework-owned `mdllm watch --exit-on-wake` process, targets one explicit
OpenClaw `agentId` and canonical `sessionKey` when the watch exits 0, waits
for that turn to finish, then rearms the watch. Exit codes 1, 2 and 3 never wake
an agent. An OpenClaw failure stops the bridge without an automatic retry
because transport loss can be ambiguous and replaying a turn can duplicate
work.

The bridge relays MarkdownLLM watch output to its own console and includes a
bounded copy in the exact-session wake as labelled observed data. An
unpublished or diverged local turn therefore carries the framework's
reconciliation observation to the responsible domain agent while Git
resolution remains outside the adapter.

Both child commands use argv arrays with `shell: false`. On Windows, point
`--mdllm-command` at Python with `--mdllm-arg` naming `tools/mdllm.py`,
and point `--openclaw-command` at Node with `--openclaw-arg` naming
OpenClaw's `openclaw.mjs` entry.

The bridge exit contract is:

- 0: a turn ran successfully and the watch may rearm;
- 1: the MarkdownLLM watch failed;
- 2: the watch refused to arm or arguments were invalid;
- 3: another watcher already owns the same standing watch;
- 4: the OpenClaw turn failed or its acceptance is ambiguous;
- 5: a child process could not be launched.

Codes 1 through 5 stop the bridge. Ambiguous OpenClaw failures are never
replayed automatically.

## Trust and security

- The plugin is native Gateway code. Install only a reviewed artifact from a
  trusted publisher.
- Register only trusted `domains` and keep each domain on a unique agent and
  workspace. The lifecycle adapter rejects every agent not present in that
  registry.
- Domain opening is owner-only and requires `operator.admin` authority.
- Point `command` and `commandArgs` only at a trusted MarkdownLLM checkout.
- Lifecycle subprocesses use argv arrays with `shell: false`, a bounded timeout
  and a bounded output buffer.
- MarkdownLLM admission verifies the domain entry, relative or ancestor
  framework discovery, sentinel, kernel, domain name and framework version
  before session-start commands run.
- Context is additive. The plugin does not replace the system prompt, create
  ordinary sessions, edit OpenClaw's session database or read transcripts.
- The watch bridge treats watch output as labelled observed data and wakes only
  the configured canonical agent/session key.
- OpenClaw's normal plugin allow/deny policy and hook permissions remain
  authoritative.

## Removal

Stop any `markdownllm-openclaw-watch` process, then run:

```bash
openclaw plugins disable markdownllm
openclaw plugins uninstall markdownllm
```

Removal deletes OpenClaw's managed plugin copy and configuration through the
host's supported lifecycle. It does not delete the MarkdownLLM checkout,
domain state, Git history or workflow state.

## Troubleshooting

### `before_prompt_build` is blocked

Set:

```bash
openclaw config set plugins.entries.markdownllm.hooks.allowConversationAccess true --strict-json
```

Then inspect the runtime again. A healthy 2026.9.3 load has five typed hooks.

### `openclaw plugins validate` rejects the entry

OpenClaw 2026.9.3's authoring validator accepts tool and feature authoring
metadata, but this adapter is a supported hook-only compatibility plugin. Use
managed installation, `plugins inspect --runtime --json` and `plugins doctor`
for the host-native hook proof.

### Session-start is unavailable

Check that the selected agent workspace is the MarkdownLLM domain entry and
that `command` plus `commandArgs` launch the framework CLI without a shell.
The adapter emits a failed advisory envelope and does not certify the domain
when admission or lifecycle execution fails.

### The standing watch stops

Read the exit code above. Correct the underlying watch, Git or Gateway
condition and restart deliberately. Do not blindly replay exit code 4.

## Development

```bash
npm ci
npm test
npm run test:install
npm pack --dry-run --json
```

`test:install` creates and removes a disposable OpenClaw profile, installs the
actual npm tarball, grants the required hook consent, inspects all five hooks,
runs Plugin Doctor and uninstalls the package. CI executes this on Windows and
Ubuntu.

See `CONTRIBUTING.md` and `CHANGELOG.md`. The package is MIT licensed.
