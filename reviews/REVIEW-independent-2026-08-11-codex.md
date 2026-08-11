---
id: independent-review-2026-08-11-codex
type: artifact
status: stable
version: 1.0
created: 2026-08-11
origin: synthesised
tags: [independent-review, codex, architecture, deterministic-floor, full-corpus]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: challenges
    notes: "Tests the manifesto's determinism, universality, transparency, prompt, and git-as-truth claims against the complete implementation and corpus."
  - id: hook-enforcement-has-three-anchors
    relation: challenges
    notes: "Reproduces an index/worktree mismatch at the git-fs anchor: the pre-commit hook can pass bytes other than those Git will commit."
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "The managed-shell and nested-fallback findings independently support the designed-for versus verified-on distinction."
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Cold-reads the Codex challenge and the Phase 2C in-flight adapter boundary; the capture addendum records the subsequent extraction commits."
---

# Independent Full-Corpus Review — Codex, 2026-08-11

**Reviewer:** OpenAI Codex, arriving without authorship history or prior participation in defining the framework.

**Commission:** Read every tracked file, beginning with the manifesto, and provide a fresh code, architecture, epistemic, and product review. The operator initially required the findings to remain session-only, then explicitly instructed that the completed report be captured in full as a framework review record.

**Disposition at capture:** The review is a stable historical record; its findings are not yet accepted, rejected, or routed. No response plan or implementation authorization is implied. The report between the markers below is preserved verbatim from the session response, including its machine-local file links and the repository state described at that moment.

<!-- verbatim-review-begins -->

I’ve finished the independent review. My blunt assessment is: MarkdownLLM is a serious and unusually coherent agent substrate, not merely a prompt collection. Its central idea is sound and valuable—surround stochastic reasoning with deterministic structure, validation, state, and history.

But it is not deterministic end-to-end, and one foundational implementation mismatch currently prevents the “deterministic floor” from guaranteeing the state Git actually commits. I would keep building it, but I would fix the transaction model before widening the feature surface or strengthening the public claims.

## Findings

### 1. Critical: the pre-commit floor validates the worktree, not the commit candidate

Git commits the index. The hook invokes `validate` against ordinary filesystem paths, and the scanner reads those paths from the worktree: [hook](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/scaffold.py:28), [scanner](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/model.py:294).

I reproduced this directly:

1. I staged a `thing.md` containing an invalid status.
2. I repaired only the worktree version, leaving the invalid blob staged.
3. I ran the installed pre-commit hook.
4. It exited successfully.

The inverse is also possible: a valid staged version can be blocked by an unrelated invalid worktree version.

This means the floor does not currently validate the state transition it claims to guard. It validates a neighbouring state.

The fix should be architectural, not another hook condition: introduce a repository-view abstraction capable of reading from:

- `INDEX` for pre-commit validation.
- A pinned `COMMIT` for stable analysis and serving.
- `WORKTREE` only for explicit draft/edit operations.

A pre-commit run can obtain the candidate tree with `git write-tree` or read index blobs through Git plumbing. Add a regression test that performs a real commit and inspects the resulting blob.

### 2. High: there is no consistent snapshot for an agent’s read

Nearly every command scans a mutable directory. During this review, several other commits landed and Phase 2C began modifying the working tree. A sufficiently long analysis can therefore read some files before a commit and other files after it.

That is incompatible with Git being the state machine. Git already gives you immutable snapshots, but the read layer mostly bypasses them.

This same architectural gap underlies several other problems:

- Pre-commit sees the wrong state.
- MCP can serve working-copy bytes under a committed provenance pin.
- Workflow transition validation cannot reliably compare old and new state.
- A long agent session cannot prove which corpus it reasoned over.
- Multi-agent work relies on advisory convention rather than optimistic concurrency.

I would have every session and significant tool result name a base commit. Before writing, check whether `HEAD` still equals that base or explicitly reconcile the intervening commits. Full-corpus reads should default to committed bytes.

### 3. High: autopush fails open on an irreversible operation

[`_autopush_enabled`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/sync.py:183) returns `True` when:

- `AGENTS.md` is missing.
- Frontmatter is absent.
- YAML is malformed.
- The Git section is absent.
- Parsing raises any exception.

The scaffolded AGENTS template does not explicitly declare an autopush choice, so a new domain becomes publication-enabled by absence. It initially has no remote, but adding one later activates automatic publication.

That conflicts directly with the framework’s standing principle that irreversible operations—things that send—belong to the human and explicit structure. Missing or unreadable structure should never become permission to publish.

Require explicit `autopush: true`. Treat absent, malformed, and unknown as off or degraded, and have `doctor` report the reason. The post-commit hook may remain advisory, but authorization should fail closed.

### 4. High: scaffold and hook installation are not transactional

The scaffold flow stages `.gitignore` in the outer repository and then runs an ordinary `git commit`: [scaffold isolation](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/scaffold.py:310).

If the operator already has unrelated staged changes, that commit will include them. `git add .gitignore` does not constrain `git commit` to that file.

There are related hazards:

- A later failure leaves an outer isolation commit plus a partially born domain.
- [`install_hook`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/scaffold.py:121) overwrites existing `pre-commit`, `commit-msg`, and `post-commit` hooks without chaining or backup.
- It assumes `.git` is a directory and ignores Git worktrees, gitfiles, and `core.hooksPath`.
- Installing the framework can therefore destroy an unrelated hook system.

Preflight the outer index and refuse or isolate the commit when unrelated staged content exists. Resolve the actual hooks directory through Git. Preserve existing hooks through a dispatcher, managed fragment, or explicit operator-approved replacement.

### 5. High: MCP provenance can assert a commit that did not produce the served content

The MCP server constructs payload content from the live scanned `Thing`, but obtains `source_commit` from the last commit that touched its path: [MCP payload](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/mcp_server.py:140).

If the file is dirty, a consumer receives uncommitted bytes stamped with an older commit. The reference triple is then false. It also uses abbreviated hashes, which are weak identifiers for long-lived, cross-repository provenance.

Serve the blob from the exact full commit named in the reference triple. Alternatively, refuse dirty exposed things or mark them explicitly:

```text
source_state: uncommitted
base_commit: <full SHA>
content_sha256: <hash>
```

The manifest, deliverable, and imported copy should all refer to the same immutable bytes.

### 6. High: the declared graph is implemented by several drifting field lists

[`touchpoints`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/touchpoints.py:25) says it reports the “COMPLETE declared inbound set,” but it examines only:

- `linked_things`
- `parent`
- `definition`
- `informed_by`

It omits declared structural relationships such as `dependencies`, `blocks`, `parties`, and any future schema-owned pointers. Validation, indexes, cascade, MCP egress, and touchpoints each maintain related but different lists.

That makes completeness claims unstable by construction.

Define one canonical structural-reference iterator or registry and make validation, indexes, touchpoints, cascade, and MCP consume it.

A neighbouring issue is more conceptual: [change-reconciliation](C:/Users/Jamos/Projects/MarkdownLLM/change-reconciliation.md:48) says a fresh thing carries no consistency risk, while [`candidates`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/touchpoints.py:129) considers only staged `M` modifications.

A new thing can absolutely contradict existing knowledge. A deleted thing can invalidate conceptual assumptions even when declared references remain clean. Candidate handling needs `A`, `M`, `D`, and rename semantics, with different cue questions for each.

### 7. High: duplicate YAML keys are silently accepted

The parser uses `yaml.safe_load`, which follows last-value-wins behaviour for duplicate keys: [parser](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/model.py:237).

The current corpus contains a concrete example that validates cleanly:

- [`source_domain` appears twice](C:/Users/Jamos/Projects/MarkdownLLM/things/insights/divergence-is-an-unrouted-decision.md:11).

Today that duplication is harmless because the values agree. The same behaviour could silently discard one of two conflicting statuses, origins, dependency lists, or publication settings.

A definition-driven framework should reject duplicate mapping keys before constructing the Python dictionary. Use one strict YAML loader everywhere, including schemas, fixtures, AGENTS frontmatter, and thing frontmatter.

### 8. High: the evaluation harness can return success for failed evidence

Several independent gaps exist in [evals.py](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/evals.py:21):

- Scan findings are discarded at line 30.
- `validates_clean` invokes only three validation functions, not the complete validation command.
- The headless agent’s process return code is not made part of the trial result.
- An agent-reported error is printed but does not necessarily fail the trial.
- The command returns `0` after Stage 2 even when assertions failed: [final return](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/evals.py:377).
- Second-resolution run IDs can collide under concurrent or repeated execution.

This means the JSON evidence may be informative, but the command is not yet a trustworthy CI/evidence boundary.

Return non-zero when any trial, session, agent invocation, validation, or assertion fails. Record the exact framework commit, fixture hash, CLI version, model identifier, execution surface, and complete validation result.

The repository is admirably honest that its first model-size fixture saturated and that the stronger efficiency claim remains open. Keep that caution.

### 9. High for financial domains: calculation enforcement has three loopholes

The calculator says “Decimal, never float,” but YAML has already parsed unquoted numeric scalars before [`to_decimal`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/calc.py:93) receives them. Converting the resulting float through `str` avoids exposing the binary expansion, but it cannot recover decimal precision already discarded by YAML.

Two more consequential gaps exist:

- A non-evaluable expression remains only a warning even under `computed: strict`: [validation](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/validation.py:644). A typo can therefore disable a supposedly blocking calculation.
- Cross-corpus calculations exclude unverified external things and record a context note, but commit validation does not surface those notes when the remaining result agrees. A total can validate cleanly while omitting quarantined inputs.

In strict mode, unevaluable computation should be an error. For exact financial values, parse numeric source lexemes directly or require quoted decimal values. Any exclusion that changes a declared aggregate’s input set should appear in validation output.

### 10. Medium-high: workflow transition legality is classified as semantic when it is mechanical

A workflow definition contains machine-readable adjacency lists. Git contains the prior `current_stage`. Yet [workflow-state.md](C:/Users/Jamos/Projects/MarkdownLLM/workflow-state.md:139) explicitly delegates transition legality to the agent, and validation checks only membership: [validator](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/validation.py:236).

A move from `draft` directly to `done` can validate even when the definition permits only `draft → review → done`.

Whether the work deserves to advance is semantic. Whether `old_stage → new_stage` is a declared edge is mechanical. The floor should enforce the latter from the candidate index against the parent commit.

### 11. Medium-high: trigger evaluation can crash or fire incorrectly

In [triggers.py](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/triggers.py:118):

- A malformed stale threshold reaches `int(thresh)` and can crash the command instead of producing a validation finding.
- `subtasks_complete` ignores subtask IDs absent from the corpus. If every named subtask is missing, `all(empty)` is true and the trigger fires.
- Unknown threshold conditions fall through silently.
- Several history-dependent conditions are delegated to the agent even though Git history is already available.

Compile and validate trigger declarations before evaluation. An evaluator should return explicit `fired`, `not-fired`, `unevaluable`, or `invalid` results; malformed declarations should never become exceptions or silence.

### 12. Medium: session attestation records a SHA but never checks it

Session start writes a timestamp and `HEAD` SHA: [attestation writer](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/session.py:722). Validation reads only the timestamp: [gate](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/validation.py:721).

A Tier-0 contract can change immediately after session start and the attestation remains accepted until its time window expires. The test also contains a vacuous assertion: [`assert _gate(...) == [] or True`](C:/Users/Jamos/Projects/MarkdownLLM/tools/tests/test_mdllm.py:3082).

Pin the contract content rather than requiring `HEAD` equality, since ordinary work legitimately advances HEAD. Hash the relevant AGENTS/kernel/spec set or record its commit and invalidate only when those surfaces change.

### 13. Medium-high: external integrations need an explicit trust boundary

[`imports-check`](C:/Users/Jamos/Projects/MarkdownLLM/tools/markdownllm/imports_check.py:30) treats `.mcp.json` as an address book and can:

- Execute an arbitrary configured command.
- Make requests to any HTTP or HTTPS URL.
- Send configured headers.
- Read unbounded response bodies.

Operator wiring lowers the risk, but a repository-local configuration file can still become an execution surface when a project is opened or automated. Require a human trust decision or a local hash attestation before executing repository-provided commands. Constrain URLs or make remote-network authorization explicit.

The minimal stdio client also sends `initialize` and immediately sends resource requests without the normal initialized notification, which may fail against stricter MCP servers.

The provenance spec correctly recognizes external things as durable prompt-injection risks. Metadata quarantine is valuable, but it is not content isolation: an agent still reads the body. External bodies should be visibly delimited and treated as quoted data, never as instructions.

### 14. Medium: examples and birth surfaces sometimes claim enforcement they do not provide

The compliance example says metadata such as `access_control` “enforces” least privilege and that Git provides an access audit trail: [example](C:/Users/Jamos/Projects/MarkdownLLM/examples/compliance-patterns/things/example-gdpr-compliant-data-handling.md:52).

Those fields declare a desired control; the framework does not implement authorization, access logging, residency enforcement, or retention deletion. The legal rules shown—UK-only processing and a universal seven-year hold—are context-dependent, not GDPR invariants.

Teach three distinct fields:

- `declared_policy`
- `enforcement_mechanism`
- `evidence_of_operation`

Label legal examples synthetic and non-authoritative.

There are smaller birth-surface defects too:

- The sanitised evidence template places comments before `---`, so the frontmatter parser ignores it; it also uses an artifact status inconsistent with the framework’s artifact vocabulary: [template](C:/Users/Jamos/Projects/MarkdownLLM/evidence/sanitised-validation-record.md.template:1).
- Example skills reference a nonexistent `../thing.md`.
- Scaffolded skill `applies_to` globs point at a nested domain-name directory even though the domain is normally opened at its own root.
- The insight template suggests relations not present in the scaffold schema’s starting vocabulary.

Templates deserve their own validation corpus because they are where future domains inherit defects.

### 15. Medium: installation and hook supply-chain hardening is below the framework’s trust ambition

The README recommends piping the moving `main` branch directly into `bash` or PowerShell. Dependencies and several action references are not cryptographically pinned.

For a framework that installs executable Git hooks and may automatically push committed domain data, this is a meaningful supply-chain boundary. Prefer versioned release artifacts, checksums/signatures, pinned dependencies, and immutable CI action SHAs.

## The central conceptual correction

The framework should not describe itself as deterministic without naming the layer.

| Layer | Current reality |
|---|---|
| File format and schema | Largely deterministic, with duplicate-key and template gaps |
| Structural validation | Strong against the worktree, not yet against the commit candidate |
| State-transition legality | Partial; several machine-readable transitions remain agent-owned |
| Agent interpretation | Stochastic and harness/model-dependent |
| Semantic correctness | Human/agent judgement supported by evidence |
| External truth and outcomes | Never established by structure alone |

The strongest honest description is:

> A deterministic state and validation substrate around probabilistic reasoning.

That is not a retreat. It is a sharper and more defensible proposition than “deterministic AI.”

Several manifesto claims should be narrowed:

- Self-hosting proves reflexivity and serious dogfooding, not universality.
- Markdown definitions and executable code are not literally the same artifact. The LLM remains a stochastic translation/interpreter layer.
- Definitions are still prompts in the broad technical sense; their advantage is that they are modular, persistent, typed, versioned, and shared—not that prompting disappeared.
- Git is recorded and accepted state, not truth. It can preserve false claims, bypassed validation, rewritten history, and incomplete reasoning.
- Inspectable files provide strong transparency, but commit history is not a complete reasoning trace.
- “Everything is a thing” is a useful ontology for domain knowledge, but the repository necessarily contains code, configuration, templates, evidence, and release surfaces that are not ordinary things.

The new vendor-port work is already moving toward this more rigorous vocabulary by separating “designed for” from “verified on.” Its Codex constraints match the important parts of the [official hooks documentation](https://learn.chatgpt.com/docs/hooks), especially concurrent matching handlers, trust review, Windows command variants, and PostToolUse feedback semantics.

## What is genuinely excellent

The review above is demanding because the substrate deserves to be taken seriously. Several aspects are unusually strong:

- The mechanical-versus-semantic division is the right foundation.
- The framework is genuinely self-describing, not cosmetically recursive.
- Tiered context loading is practical and recognizes that agent context is a real computational budget.
- The decomposition principle is consistently useful.
- Conflicts, insights, decisions, provenance, retrospectives, and workflow runs are treated as durable state rather than chat residue.
- Derived indexes are correctly viewed as disposable caches, not sources of truth.
- “Deploy when felt” protects the framework from premature abstraction.
- Git history is used creatively as telemetry and event history.
- The historical record preserves failed evaluations, corrections, retractions, and independent reviews. That makes the project substantially more credible than a polished repository containing only successful evidence.
- The code is plain, readable Python rather than an opaque framework stack.
- Regression tests frequently document the failure that caused them to exist.
- The recent Codex port sequence is evidence that the review culture works: an apparently successful framework-root runtime test was correctly narrowed after the untested nested fallback failed, the gate was reopened, and commit `cce3b70` removed the `dirname` dependency, added a command-executed fact, and reconciled the CLI map.

That last point matters. The substrate is not merely claiming belief revision; it demonstrably revises its own claims.

## Current adapter work

I read the in-flight Phase 2C adapter files separately but did not treat them as accepted state. Two issues are already worth carrying into that work:

- Claude command rendering does not quote the framework-relative script path, so paths containing spaces can break.
- Inspector currency treats any command beginning with the expected command string as a harmless extension. Prefix matching needs argument-token boundaries; otherwise a semantically different path or argument can be classified as current.

The overall render/inspect separation, pure renderer, immutable lifecycle bindings, and registry boundary are good decisions.

## Review scope and verification

I began with the manifesto as requested and read every file in the frozen starting repository:

- Baseline commit: `87ec7b938d7e1299accd2c687cff252892f8d5a4`
- 370 tracked files
- Approximately 2.48 MB and 45,107 lines
- All specifications, guides, things, examples, templates, evidence, reviews, eval fixtures/results, Python code, shell/PowerShell code, configuration, and tests

I then read each committed delta through `cce3b70`. The clean reviewed snapshot at `890406e` produced:

- Framework corpus: 168 things, clean
- Compliance example: 6 things, clean
- Life-manager example: 14 things, clean
- Doctor: framework-root floor active
- Coherence: one 26-versus-27 CLI-map warning, subsequently fixed by `cce3b70`

Earlier full-suite runs exposed the managed-shell runtime boundary:

- Baseline: 283 passed, with six genuine scaffold/runtime integration failures and one temporary-test-layout artifact.
- After the first shared-runtime port: 298 passed and eight scaffold/runtime integration failures, all tracing to the external `dirname` dependency in the nested fallback.

Commit `cce3b70` directly addresses that defect and adds stronger tests. I did not certify the complete suite after it because another agent began Phase 2C modifications concurrently and the resulting integration run stopped making progress. I terminated its exact process tree and removed all temporary review directories rather than presenting a dirty moving tree as verified.

I created no review document, modified no repository file, and made no commit. Everything in this report exists only in this session.

## Recommended order

If this were mine, I would proceed in this order:

1. Build `RepositoryView` with committed, index, and worktree modes; make the pre-commit floor index-native.
2. Add pinned read snapshots and optimistic concurrency checks for agent sessions.
3. Make autopush explicitly opt-in and transactionalize scaffold/hook installation.
4. Serve committed MCP bytes under full provenance hashes and harden import trust.
5. Introduce one strict YAML loader and one canonical structural-reference registry.
6. Mechanize workflow transitions and make trigger evaluation total—never crash or fall silent.
7. Make calculation strictness genuinely blocking and repair eval exit semantics.
8. Validate templates as instantiated birth artifacts.
9. Reconcile the manifesto and README language to the guarantees that tests can actually demonstrate.
10. Then resume widening the vendor adapter surface.

My overall conclusion is strongly positive: the idea is worth pursuing, and much of the hard conceptual work is already unusually mature. The next maturation step is not more ontology. It is transaction integrity—ensuring that every deterministic claim refers to one exact immutable state.

<!-- verbatim-review-ends -->

## Capture Addendum — State Advanced After the Review Cutoff

The verbatim report is deliberately not corrected in place. After its cutoff,
the previously in-flight adapter work became committed state:

- `6996309` extracted the Claude implementation behind the accepted adapter
  ports and recorded 321 passing tests in its commit message.
- `b228f57` returned Phase 2C at the Codex acceptance gate.
- `51a88a3` sealed that session while preserving the test-harness portability
  boundary.

Those commits change the chronology, not the evidence captured above. This
review did not independently rerun the complete suite against `6996309` or
accept the Phase 2C handoff after the report was delivered. The adapter
observations therefore need reproduction against current committed state
before disposition; they are not silently declared current or obsolete here.

## Additional Synthesis — Route Seams, Not Fifteen Isolated Patches

The findings look numerous, but they cluster around five architectural seams:

1. **State view:** worktree, index, and commit are currently conflated. A single
   immutable `RepositoryView` boundary addresses the staged-index bypass,
   stable agent reads, transition history, and truthful MCP serving together.
2. **Authority and transaction:** scaffold, hook installation, and autopush
   need one fail-closed model for staged state, existing operator machinery,
   external effects, and partial failure.
3. **Canonical definition:** YAML parsing and graph-field interpretation each
   need one owner. Duplicate loaders and duplicated relationship-field lists
   are definition drift expressed in code.
4. **Evidence semantics:** eval exit codes, calculation exclusions, session
   attestations, and provenance pins must distinguish observed, executed,
   passed, current, and true rather than promoting one fact into another.
5. **Claim vocabulary:** deterministic structure, transaction integrity,
   semantic judgement, empirical truth, and harness verification are different
   guarantees and should remain separately named in code, tests, and prose.

This clustering matters because patching each symptom independently would
repeat the failure mode the framework already understands: local corrections
that grow machinery while leaving the shared cause intact. The review's
primary recommendation is therefore one architectural correction—the state
view—followed by four smaller canonical boundaries, not fifteen unrelated
features.

## Suggested Disposition Method

The next act should be a response record rather than direct implementation.
For each numbered finding: reproduce against the then-current pinned commit;
mark it accepted, narrowed, already-fixed, or rejected with evidence; identify
the shared seam that owns it; and only then sequence changes. The critical
staged-index reproduction deserves first disposition because every other
commit-boundary guarantee depends on its result.
