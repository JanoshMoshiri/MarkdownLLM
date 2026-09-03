---
id: explorer-extraction-and-hosting
type: plan
status: cancelled
version: 1.2
created: 2026-08-27
priority: medium
exposed: false
tags: [explorer, extraction, hosting, architecture, distribution, vercel, local-connector]
linked_things:
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: derived-from
    notes: "The local-first Desktop direction replaces this hosted-Explorer hypothesis."
  - id: explorer-publication-position
    relation: derived-from
  - id: interface-specification
    relation: references
  - id: markdownllm-explorer-windows-distribution
    relation: references
  - id: code-architect-governs-substrate-code
    relation: references
---

# Extract and host MarkdownLLM Explorer

## Disposition — 2026-09-03

**Cancelled as the preferred product path.** The operator chose a local-first MarkdownLLM Desktop
and deferred remote access until a later paired mobile client can prove its boundary against a
live local application. The read-only Explorer and this plan remain historical evidence; no
source move, hosted control plane or cloud resource is authorised. Any future remote design starts
from the Desktop's accepted local boundary rather than resuming this plan by inertia.

## Intent

After the local Windows preview has produced real operating evidence, move
Explorer out of the framework release surface and decide how it should be
owned, hosted and delivered. This is a future architecture and migration
exercise, not a relocation of files disguised as clean-up.

## Preferred architecture hypothesis

The leading shape to prove is a **hosted web/control plane with a local,
read-only data plane**:

- Explorer becomes a separately owned product repository with its own release,
  protocol, security and migration lifecycle.
- Vercel hosts the web interface, login, account preferences, device pairing
  and ordinary control-plane APIs.
- A thin local connector retains the existing Python filesystem, Git and
  eligibility logic. It remains the authority over the selected substrate and
  opens an authenticated outbound connection; the hosted service receives no
  ambient authority over a device.
- Browser requests remain bounded Explorer operations — estate overview, tree,
  search, collection, document and commit history — expressed through a
  versioned protocol. The connector never accepts an arbitrary absolute path
  or unrestricted file-read instruction from the cloud.
- Synchronisation is query-on-demand plus revision invalidation. The connector
  sends bounded manifests, revisions and requested DTOs rather than uploading
  the entire estate. Raw substrate content is transient and is not retained by
  the hosted service by default.
- The realtime relay is a replaceable transport adapter. Vercel is the first
  deployment candidate, not a dependency of the Explorer core; reconnection,
  resumption and durable session state must survive a provider swap.

This is a hypothesis to characterise against a real device and estate, not an
authority to start migration. A browser-only filesystem mode and a remote-Git
mode remain useful reduced-capability alternatives, but neither is assumed to
provide full parity with immediate local dirty state and native Git history.

## Sequence

### 0. Close the local evidence loop

- Complete `explorer-publication-readiness`: selected review corrections,
  immutable technical evidence and operator-owned UAT.
- Keep the accepted local Explorer as the behavioural and safety oracle for
  the hosted work. Extraction must not rewrite the requirements retrospectively.

### 1. Establish independent product ownership

- Create one Explorer product repository containing the web application, local
  connector, versioned protocol, contract tests and architectural decisions.
- Move history and release ownership deliberately; do not copy a snapshot and
  abandon the rationale or evidence chain.
- Preserve the current core/application dependency direction while replacing
  loopback HTTP and Windows presentation with new outer adapters.

### 2. Run the risk-first hybrid spike

Prove one account, one paired device and one real estate through the smallest
end-to-end slice:

- overview, tree, document and Git-history queries;
- a local uncommitted change becoming visible through revision invalidation;
- disconnect, reconnect and state resumption without a stale or mixed view;
- explicit device revocation;
- no raw content at rest in the cloud; and
- a hostile-request oracle proving that the hosted side cannot escape the
  connector's source boundary, exclusions or bounded operations.

The spike decides whether the proposed trust and transport boundary is real.
It does not optimise the UI or begin broad migration.

### 3. Fix the production contracts

- Authentication, device pairing, per-device keys, revocation and tenant
  isolation.
- Protocol compatibility and connector update policy, including the supported
  old/new version window and safe refusal when versions cannot interoperate.
- Reconnect, replay, ordering, deduplication and terminal failure states.
- Content exposure, encryption, retention, telemetry and deletion policy.
- Relay deployment and durable state, kept behind a provider-neutral port.
- Signed connector distribution and an update path that changes less often
  than the centrally deployed UI.

### 4. Migrate and cut over

- Re-run the local acceptance journeys against the hybrid product and add the
  new pairing, reconnection, tenancy and cloud-compromise journeys.
- Publish the separate product only from a pinned, verified candidate.
- Deprecate the in-repository preview only after the hosted route preserves its
  observable behaviour and read-only safety boundary.

## Questions to resolve

- Repository and package ownership, version cadence and release governance.
- Whether Vercel's live-connection path satisfies the measured relay boundary
  or the web/control plane should use a separately hosted relay adapter.
- Authentication, authorisation, device revocation and tenant isolation when
  bounded substrate content crosses a network boundary.
- Whether end-to-end encryption is required in addition to transport security,
  and which metadata the control plane may retain.
- Connector update delivery, signing, protocol compatibility, telemetry and
  support expectations.
- The reduced capability and browser support promised by any zero-install
  browser-filesystem or remote-Git mode.
- Migration of history, documentation, issue tracking and public release links.
- Cutover and deprecation path for the in-repository preview.

## Invariants

- The local filesystem and its Git repositories remain the source of truth.
- The connector is read-only in this plan. Cloud-to-local edits, commands and
  arbitrary code execution require a separate future decision and threat model.
- The connector applies source ownership, exclusion, path, output and resource
  limits locally even if the hosted service is faulty or hostile.
- The whole estate is not retained in the cloud by default merely because its
  files are small or textual.
- Account configuration stores device identity and preferences, not reusable
  server-side authority over an absolute local path.
- The transport and host remain outer adapters; the Explorer core does not
  depend on Vercel, a particular relay or an authentication vendor.

## Non-goals for the current release

- Do not move Explorer now.
- Do not expose the current loopback service to a network.
- Do not add local write-back while establishing the read-only hosted boundary.
- Do not make future extraction a blocker to a truthful preview release.

## Exit condition

An accepted design and captured hybrid spike name the product boundary, trust
model, versioned protocol, deployment path, connector lifecycle, migration
sequence and evidence required for cutover. They demonstrate live local change
visibility without whole-estate cloud custody and prove that a hostile hosted
request cannot cross the connector's read-only source boundary. Only then
should source move or the local preview be deprecated.
