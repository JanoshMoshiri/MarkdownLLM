---
id: codex-cloud-git-boundary-2026-09-27
type: artifact
status: stable
created: 2026-09-27
tags: [codex, cloud, git, authentication, execution-evidence]
linked_things:
  - id: codex-cloud-workspace
    relation: informs
  - id: interface-specification
    relation: informs
---

# Codex Cloud Git boundary — diagnostic and adapter fixture

This record separates two kinds of evidence. The first was observed in a
Codex Cloud environment diagnostic terminal on 2026-09-24. The second is an
isolated Linux integration test of this adapter on 2026-09-27. Neither is a
first working-agent session with the completed adapter.

## Cloud diagnostic terminal

The host supplied the selected private repository checkout. A plain shell
Git command could read the public MarkdownLLM remote. Plain shell Git reads
of the selected private remote and a second private remote failed because Git
had no username in that terminal. The primary host checkout therefore did
not establish an ambient Git credential for other repository operations.
The diagnostic did not test an actual working-agent phase or a push. It did
not test whether a later product version supplies different credentials.

The settings UI selected one primary GitHub repository. Selecting the other
private repository replaced the first selection in the observed environment.
That does not rule out product features unavailable in this account. The
adapter's extra repository clones are therefore explicit, not presumed to
arrive from a connector or a multi-repository mapping.

## Isolated adapter execution

Linux fixtures use real Git remotes and the generated shell bootstrap. The
host-selected primary HEAD, index and tracked files were preserved on fresh
setup and cached maintenance. A public framework clone obtained full history;
the extra read-pinned domain, writable domain and ordinary code repository
were independent clones. Domain hooks and validation ran; the ordinary code
repository retained its own hooks. The credential helper selected an exact
GitHub repository and kept the test token out of argv, Git config and logs.
Missing configured credentials failed in the tested phase. A writable domain
with literal declared autopush published one accepted fixture commit; PR and
manual restraints disabled automatic sends in the other clones. These are
fixture observations, not proof of actual cloud agent delivery or GitHub
permissions.

## Claim boundary

The adapter is built and locally tested. A real Codex Cloud task must still
establish setup and maintenance execution, model-visible Tier-0 receipt,
agent-time Git reads for every private repository, Git hook enforcement,
project lifecycle trust and the chosen publication path. A read probe does
not prove write permission. The public framework release and selected
primary's committed bundle are prerequisites for that live task.
