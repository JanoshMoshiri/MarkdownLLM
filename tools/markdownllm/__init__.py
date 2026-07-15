"""markdownllm — the MarkdownLLM deterministic floor, as a package.

The public entry point is unchanged: `python tools/mdllm.py <cmd>` (a thin
shim beside this package — that path is a contract cited by every domain's
AGENTS.md and the installed pre-commit hooks). Modules are cut by reason to
change; dependencies flow inward: every module may import `model`, `cli`
imports the command modules, and no command module imports another.
"""
