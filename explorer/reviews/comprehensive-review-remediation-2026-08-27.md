---
id: markdownllm-explorer-comprehensive-review-remediation-2026-08-27
type: artifact
status: evolving
version: 1.0
created: 2026-08-27
origin: synthesised
exposed: false
confidence: high
tags: [explorer, review-remediation, acceptance, windows, publication, signing]
linked_things:
  - id: markdownllm-explorer-comprehensive-review-2026-08-27
    relation: extends
  - id: explorer-publication-readiness
    relation: documents
  - id: code-architect-governs-substrate-code
    relation: implements
---

# MarkdownLLM Explorer — Comprehensive Review Remediation

## Verdict

The reviewed product and architecture corrections are implemented, and the
operator's product acceptance is recorded. The Explorer source candidate is
materially stronger and its portable/browser evidence is green. **Public
Windows publication is not yet ready.** The remaining gate is the separately
authorised Authenticode release step followed by a native lifecycle run on the
signed bytes.

This is not a disguised product-test failure. The unsigned identity-isolated
installer completed install and active upgrade, then Windows Smart App Control
blocked the generated unsigned `Uninstall.exe` before process start. Code
Integrity event 3077 names policy
`0283ac0f-fff1-49ae-ada1-8a933130cad6`. The release path now signs the frozen
application, generated uninstaller and setup, but this repository has no code
signing certificate or authority to use one.

## Review boundary

- Significant-read base: `commit:016150e76f1ae69aefd41331f9da1aa7fed471e6`.
- Final Explorer subject: `sha256:faab2f2cd91daea6dd0d39e358d506795d8e085a69cda7e6a1021820b74628ad`.
- Unsigned release candidate:
  `MarkdownLLM-Explorer-Installer-0.2.0.exe`, 10,509,386 bytes,
  SHA-256 `a963d146e40e9813c522b2f87bb67dde4e48a3aa14f3d5a3516b3dd27ddf4c27`.
- Code Architect's requirements → model → design → decomposition → build →
  acceptance loop remained the review spine.
- The operator's existing Explorer installation was not upgraded, removed or
  otherwise used as disposable test state.

## Finding dispositions

| Original finding | Disposition | Evidence |
|---|---|---|
| Stale evidence seal | Corrected. The ledger is bound to the current subject and represents the remaining gate as failed rather than retaining a stale pass. | `evidence-index.json`, `traceability-result.json` |
| Active upgrade/uninstall race | Corrected in source. The secondary process acknowledges the primary PID and waits on its process handle; setup aborts before deletion on non-zero. Upgrade uses the new payload as a private shutdown helper so an older installed binary cannot reintroduce the race. | Windows unit tests, packaging architecture test, partial native run |
| One-adapter swap claim | Corrected. Independent controlled swaps cover HTTP server, Git reader, filesystem reader and Markdown renderer with exactly one outer adapter plus composition changed. | `adapter-swap.json` |
| Skills/Memory deep-link restoration | Corrected and browser-replayed. Refresh, Back and Forward retain the collection shell, selected item, source, mode and reader. | `browser-runtime.json` |
| Design/code drift | Reconciled. Capability header, cursor shape, file opening, context naming, lifecycle and UI module ownership now agree. | design and contract suite |
| Directory-depth inconsistency | Corrected to one inclusive boundary with deterministic partial state across tree, search, counts, Skills and Memory. | adapter/core contracts |
| Browser coordinator growth | Partially decomposed for this release: routing, theme and overlays are owned modules. Source/tree/collection/search orchestration remains one explicit controller and is deferred to the separate-hosting tranche before another feature tranche. | architecture tests and hosting plan |
| Accessible commit-title spacing | Corrected. | browser/component tests |
| Ambiguous Explorer test cwd | Corrected in the README. | documentation tests/review |
| Narrow static no-write fitness check | Broadened across path, `os`, `shutil` and write-capable open modes. | architecture suite |

## Acceptance and evidence

| Gate | Result |
|---|---:|
| Operator product/UAT dispositions | **30 accepted, 0 pending** |
| Explorer pytest | **114 passed, 0 failed/skipped** |
| Mutation programme | **16 killed, 0 survived** |
| Scale profile | **20 runs; all five route categories pass** |
| Clean wheel install | **pass** — arbitrary cwd, offline runtime and active-request interrupt |
| Browser/UI | **pass** — route restoration, safety, themes, responsive and accessibility checks |
| Trace ledger | **56/63 technical pass; 7 failed** |
| Signed Windows lifecycle | **blocked** — the same seven requirements depend on it |

The trace verifier has no evidence errors and no unresolved mutants. Its seven
failed requirements are `FR-RUN-001`, `FR-RUN-004`, `FR-RUN-005`,
`FR-RUN-006`, `NFR-SAFE-001C`, `NFR-OFF-001` and `NFR-PORT-001`; each consumes
the signed Windows installer evidence. No unrelated failure is hidden by the
blocker.

## Publication gate

The build now accepts `SignToolPath`, `SignCertificateThumbprint` and an HTTPS
`TimestampUrl` only as a complete set. It uses SHA-256 file digests and an RFC
3161 SHA-256 timestamp, signs the frozen application before packaging, then
uses NSIS `!uninstfinalize` for the generated uninstaller and `!finalize` for
setup. Partial signing configuration fails before construction.

To close the review:

1. provide an authorised Authenticode certificate and timestamp service;
2. run the documented signed build;
3. execute the full active install, upgrade and uninstall verifier on the
   signed release installer;
4. reseal the evidence ledger and record the signed installer hash;
5. make the framework version/changelog decision, then publish under separate
   operator authority.

Until then, the truthful release claim is **operator-accepted Windows preview
candidate, publication blocked on signing and signed-byte verification**.
