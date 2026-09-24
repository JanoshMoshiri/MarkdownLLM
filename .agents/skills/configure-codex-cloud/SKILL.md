---
name: configure-codex-cloud
description: Configure or update a MarkdownLLM domain's GitHub-backed Codex Cloud environment from versioned bootstrap files. Use for requests such as set engineering up for Codex Cloud. This configures the Codex settings UI, not the OpenAI Agents API.
---

# Configure a MarkdownLLM cloud environment

Resolve the named domain from the local estate; read its AGENTS.md and routed
skills before domain writes. Read the framework's `adapters/codex-cloud.md`.
Use the domain's declared framework runtime; on Windows use tools/mdllm.ps1.

Run `mdllm cloud configure <domain> --harness codex` from a clean, published
framework checkout. It produces a private bundle with a manifest, bootstrap,
settings guide and this skill. For updates render to a fresh output directory
and review the diff; the renderer refuses to overwrite different existing files.
Commit reviewed artifacts to the owning domain, observing its publication
policy. The selected default branch must contain them before cloud setup runs.
An unavailable framework pin is a release dependency, not permission to push
the public framework. Never substitute a moving branch for the full pin.

Read generated `.codex/cloud/SETUP.md` and `environment.json`. If the user's
request includes configuring Codex, use the available browser tool and its
instructions to find/create the matching repository environment, set exactly
the generated workspace base, Manual setup and maintenance commands, then save
and read back the fields. Preserve unrelated secrets, variables and policies.
Changing the pin requires a cache reset; report that it affects a shared cache.
If no browser is available, leave the bundle and exact settings for the operator.
GitHub login and repository authorisation are user actions when the UI requires
them. Do not invent APIs, reuse browser session tokens, or claim a save succeeded
without observing it.

If launch is requested, start a task in that environment using the available
product route. Verify setup completion, the domain's unchanged selected HEAD,
Git floor installation, the clone-local PR restraint and model-visible Tier-0
delivery. Distinguish local fixture tests, cloud setup logs, project-hook trust
and actual agent delivery. Report any untested part explicitly.
