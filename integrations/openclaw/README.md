# MarkdownLLM adapter for OpenClaw

This package binds explicitly designated OpenClaw agents to the MarkdownLLM
session-start lifecycle. OpenClaw keeps ownership of agents, sessions and
conversation history. MarkdownLLM keeps ownership of domain discovery, Git
state, validation and workflow state.

The package is under active development and is not yet released. Compatibility
is currently bounded to OpenClaw 2026.9.3 while the Plugin SDK remains
experimental.

## Configuration

Configure the plugin with an explicit list of OpenClaw agent ids. Each selected
agent's configured OpenClaw workspace must be the entry for exactly one
MarkdownLLM domain.

The adapter invokes the configured mdllm executable directly with argument
arrays. It never invokes a shell and never edits OpenClaw session storage.
The default command is mdllm. commandArgs can prefix the lifecycle arguments
when the floor is launched through an interpreter; for example, configure the
Python executable as command and the absolute tools/mdllm.py path as the first
commandArgs item. Paths are passed as argv values, so spaces do not require
shell quoting.

## Standing watch bridge

The package also builds the `markdownllm-openclaw-watch` command. It runs the
framework-owned `mdllm watch --exit-on-wake` process, targets one explicit
OpenClaw `agentId` and canonical `sessionKey` when the watch exits 0, waits
for that turn to finish, then rearms the watch. Exit codes 1, 2 and 3 never wake
an agent. An OpenClaw failure stops the bridge without an automatic retry
because transport loss can be ambiguous and replaying a turn can duplicate
work.

Both child commands use argv arrays with `shell: false`. On Windows, point
`--mdllm-command` at Python with `--mdllm-arg` naming `tools/mdllm.py`,
and point `--openclaw-command` at Node with `--openclaw-arg` naming
OpenClaw's `openclaw.mjs` entry.
