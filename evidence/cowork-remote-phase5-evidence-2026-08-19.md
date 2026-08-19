---
id: cowork-remote-phase5-evidence-2026-08-19
type: artifact
status: stable
created: 2026-08-19
tags: [cowork, remote-transport, phase-5, execution-evidence, graded, partial]
linked_things:
  - id: cowork-adapter
    relation: documents
    notes: "The remote transport leg of Phase 5, graded requirement by requirement: PARTIAL. Transport-critical controls all passed first-hand; four findings and one NOT TESTED stop a pass."
  - id: session-start-hardening
    relation: references
    notes: "Findings 1 and 2 route here: the Cowork harness truncated the 76.4 KB contract emission to a ~2 KB preview (the lands-whole constraint, proven on a second harness), and the session gate reads only the attestation timestamp while its remedy text omits the emitting flag."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: supports
    notes: "Finding 5 is this insight meeting a live remote session: the contract in context did not by itself produce contract-compliant behaviour until the operator challenged."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "The truncation, the marker nothing reads, and the false-negative self-test all sat on the harness-bound path and were found only by running it for real."
---

# Cowork remote Phase 5 evidence — 2026-08-19 — graded: PARTIAL

**Two seats, stated plainly.** The packet was collected **first-hand by the
domain agent** inside the live remote session (identifiers read from the live
workspace, not reconstructed), relayed to this framework seat by the operator,
and **independently corroborated from this estate's own clone of the same
repository** for everything that crossed the remote: the full commit chain
`6d94d6e → 9457709 → b6f7919 → f430cab → fa985e4 → 4546c7e9` exists locally in
exactly the claimed order, the graded commit's full hash matches
(`4546c7e96eb0ed20562e51430b318e81c366006e`), the amended insight is on disk
with the applied `disposition_reason`, and the domain still carries
`framework_version_seen: 3.31.0`. Requirements 5–7 therefore rest on this
seat's own reads, not on relay.

## Tested surface

| Fact | Value |
|---|---|
| Domain | the QMS domain, cloned at `domains/` under the remote workspace |
| Transport | remote ephemeral VM (Anthropic cloud sandbox; no device bridge for any repo operation) |
| Plugin build | `markdownllm-bootstrap` v3.31.0; Cowork client build **unknown — not observable in-session, not inferred** |
| Framework | v3.32.0, HEAD `eda847c4f30b89e9c04ea208aa3b76a0ee5c85b9` |
| Domain initial HEAD | `6d94d6e8ad2452f882b6eaf7ee4bbfd625115fad` |
| Bundle mechanism hash | `c060e2b55bb6414cfaeed1f63e7b866b8a48faf51d3cf064e735e65286dde1f5` — stamped and live-recomputed equal |
| Version-string skew | bundle stamped v3.31.0 against framework 3.32.0 with a byte-identical mechanism — mechanism currency and version currency are decoupled; only the former gates STALE |

## The ten requirements, graded independently

| # | Requirement | Grade | Basis |
|---|---|---|---|
| 1 | Skill activation observed, not merely installation | **PASS** | `spin-up-domain` invoked through the Skill tool on the user's phrasing. Explicit invocation — no harness auto-activation observed, and none is claimed. |
| 2 | Contract emission before first write | **PASS, materially qualified** | Mechanically proven by artifact ordering: attestation 2026-08-18T15:39:24Z carrying the `contract` marker; first domain write 20:35:40Z; gap 4h56m. The qualification is Finding 1 — emission is proven, unaided *receipt* is not. |
| 3 | Session-gate attestation fresh, recording contract emission | **PARTIAL** | Freshness: yes, twice over — valid at bootstrap, then expired at exactly 24h mid-session and blocked a real commit (Finding 3, correct behaviour). The contract-recording half is hollow: the marker is written and nothing reads it, and the documented remedy writes an attestation without it (Finding 2). |
| 4 | Real pre-commit floor on a real, truthful domain change | **PASS** | Operator-approved semantic maintenance (a self-contradicting `disposition_reason` corrected); 224 things, 0 Errors at commit; the floor demonstrated blocking twice in the same session; `--no-verify` never used. |
| 5 | Real commit published through `mdllm publish` | **PASS** | `fa985e4f → 4546c7e9`, corroborated from this estate's clone. |
| 6 | Recorded default branch, ff-only, remote tip verified | **PASS** | Branch read from `mdllm.defaultbranch`, never typed; ff-only; verified twice (publisher re-read + independent `ls-remote`). Strengthened by the unplanned test below. |
| 7 | Publication debt clear afterward | **PASS** | `estate-sync --status`: nothing unpublished; corroborated — this estate pulled the same tip. |
| 8 | No observed credential leak | **PASS** | No token on disk or in git config; redaction regexes verified at source. Two inherent, acknowledged exposures: the user's own paste in the transcript, and command-scoped `http.extraheader` values — the sanctioned pattern, confirmed non-persisting. |
| 9 | Runtime currency checking executed | **PASS (current branch only)** | Stamped hash equals live recompute; no STALE line, correctly. Only the current branch of the check is exercised — the stale branch is requirement 10. |
| 10 | Deliberately stale bundle exercised in a fresh session | **NOT TESTED** | The installed bundle is current and was not falsified. The live session cannot retroactively prove this branch. |

## Findings, routed to their owners

- **F1 (HIGH) — emission did not survive the harness unaided.** The 76.4 KB
  bootstrap emission was truncated to a ~2 KB preview, remainder persisted to a
  file; the contract reached agent context only because the agent went and read
  that file. An agent trusting the preview would have proceeded contract-less
  while the attestation still said `contract` — the artifact records emission
  by the tool, not receipt by the agent. **Routed to `session-start-hardening`
  Phase 2**, whose lands-whole-or-loudly-absent constraint this is, now proven
  on a second harness.
- **F2 (HIGH) — the gate's remedy does not do what its message says.** Plain
  `session-start` emitted no contract (5.7 KB output, zero contract lines),
  wrote a marker-less attestation, and the gate accepted it: the gate parses
  the timestamp only and never reads the marker it writes. The emitting flag
  (`--contract`) is absent from the remedy text; the gate is a freshness check
  wearing a contract-emission claim. **Routed to `session-start-hardening`
  Phase 2.** F1 and F2 compound: the marker exists, and nothing reads it.
- **F3 (MEDIUM, works as designed) — a working-day session outlives its
  attestation.** Recorded as an operational property, not a defect: any Cowork
  session crossing 24h will be blocked mid-flight, and the documented remedy
  currently leaves the clone in the weaker F2 state.
- **F4 (MEDIUM) — bootstrap's floor self-test reports the inverse of the
  truth.** It printed "the commit boundary is NOT enforced" when the non-zero
  exit *was* the boundary working (session gate legitimately unsatisfied at
  that instant). It must distinguish "hook did not execute" from "hook executed
  and correctly refused". **Routed to `cowork-adapter` Phase 3.**
- **F5 (HIGH, behavioural) — emission alone did not produce compliance.** With
  the contract in context, the agent ran no orientation, velocity, or
  attention, and read none of the four domain skills until the operator asked.
  No write had occurred, so nothing was breached — but the adapter may claim
  only that emitting the contract yields an agent that *can* comply. **Bounds
  `cowork-adapter` Phase 6 claims**; live confirmation of
  `emitted-content-is-read-instructed-content-is-economised`.

## Unplanned test passed — the guarded publisher under real divergence

Mid-session another writer pushed `9457709` to the same repository (this
estate's own concurrent session, it turns out — visible in the local log).
`mdllm publish` refused, did not force, did not retarget, surfaced the
divergence; routing was taken as an operator decision; after rebase,
publication succeeded and verified. The guard held against a condition nobody
staged.

## Still unproven, exactly

1. **Contract receipt unaided** — retest after the Phase 2 lands-whole fix;
   receipt must not require manual file recovery.
2. **The `contract` marker meaning anything** — the gate must read what it
   writes, or the claim narrows to freshness.
3. **Stale-bundle behaviour** — install a known-older bundle, open a fresh
   Cowork session, observe the STALE warning fire. The named next test.
4. **Cowork client build identifier** — record when observable.
5. **`harness-session` hook execution** — configuration present; nothing could
   fire it in a clone created after session start. Execution unobserved.

## Verdict

**REMOTE LEG PARTIAL.** Every transport-critical control passed first-hand and
survived independent corroboration from a second clone. Short of PASS on four
findings (F1, F2, F4, F5) and one NOT TESTED (stale bundle). The local leg
(Phase 4's gate session) remains separately owed and takes the same packet
standard.

Housekeeping recorded, owner the operator: revoke the test token now that the
leg is done; the domain's `framework_version_seen: 3.31.0` against framework
3.32.0 is an owed refresh, a change-control event in that domain.
