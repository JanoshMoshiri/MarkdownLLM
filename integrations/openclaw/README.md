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
