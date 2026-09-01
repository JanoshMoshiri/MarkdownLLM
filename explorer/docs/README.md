# MarkdownLLM Explorer documentation

This is the documentation map for MarkdownLLM Explorer. The files in this
folder are the maintained source; GitHub links to `main` show the newest
published versions, while links to an exact commit preserve a historical
release record.

## Start here

- **Mac operator:** [Open Explorer on a Mac](macos-quick-start.md)
- **Windows operator:** [Install Explorer on Windows](installation-guide.md)
- **Any operator:** [Explore a MarkdownLLM estate](user-guide.md)
- **Project overview:** [Explorer README](../README.md)

## Product and engineering reference

- [Requirements](requirements.md) — what Explorer is required to do.
- [Design](design.md) — component boundaries and security model.
- [Test specification](test-specification.md) — verification and acceptance
  journeys.
- [Traceability manifest](../tests/traceability.yaml) — requirement-to-evidence
  mapping used by the verifier.

## Release and platform reference

- [Windows installation guide](installation-guide.md)
- [Mac quick-start guide](macos-quick-start.md)
- [Windows packaging](../packaging/windows/)
- [Mac launcher](../../tools/open-explorer.sh)

The Mac launcher is the current fast handoff, not a signed native `.app`. The
Windows installer remains a preview until the signed native lifecycle has been
verified. Product documentation distinguishes implemented code, executed
evidence and human acceptance rather than treating them as interchangeable.

## Live open-source source

- [MarkdownLLM repository](https://github.com/JanoshMoshiri/MarkdownLLM)
- [Explorer on the published `main` branch](https://github.com/JanoshMoshiri/MarkdownLLM/tree/main/explorer)
- [Explorer documentation on `main`](https://github.com/JanoshMoshiri/MarkdownLLM/tree/main/explorer/docs)

These moving links are useful for everyday reading because they follow the
published branch. Evidence, release notes and controlled references should use
an exact commit URL instead, so later edits cannot change what the record meant.

