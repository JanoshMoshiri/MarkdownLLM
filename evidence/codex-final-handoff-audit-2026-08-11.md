---
id: codex-final-handoff-audit-2026-08-11
type: artifact
status: stable
created: 2026-08-11
origin: synthesised
exposed: false
tags: [harness, adapters, codex, acceptance, phase-2c, evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Final Codex acceptance record for Claude's Phase 1 repair and Phase 2C extraction; the failed conditions are an explicit Claude return package."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Separates successful target-shell runtime execution from a test fixture that still relies on the source harness's PATH."
---

# Codex Final Handoff Audit — Phase A/0–2 (2026-08-11)

This is the independent final-gate review of Claude commits `cce3b70` and
`6996309`, run in the Codex desktop managed shell before any Phase 3–5 work.
It creates no project `.codex/` state and does not alter a live domain. This is
internal implementation evidence; no other domain needs to rest on it
(`exposed: false`).

The Codex hook contract was rechecked on 2026-08-11 against the official
[Codex hooks documentation](https://learn.chatgpt.com/docs/hooks). Static
shape tests earn designed-for only; Phase 6 remains the first point at which a
Codex lifecycle adapter can earn verified-on.

## Verdict

**Final handoff rejected; Phases 3–5 remain stopped.** The shared runtime
repair works in the target shell, but final acceptance conditions 3, 4, and 6
fail, and the Phase 1 cross-harness acceptance suite is not green.

| Final condition | Result | Evidence |
|---|---|---|
| 1. Agent-neutral canonical prose | accepted | Phase A remains complete; this handoff introduced no contrary address. |
| 2. Claude bytes and regression boundary | accepted narrowly | Golden and estate fixtures are unchanged; the focused Claude adapter/golden/ports boundary passed 29 tests. |
| 3. Neutral modules contain no vendor assumptions, mechanically enforced | failed | The lexical gate passes, but it does not enforce the additional adapter methods scaffold and doctor actually call. |
| 4. Codex can implement the ports without learning Claude | failed | A conforming Render/Inspect adapter lacks three undeclared methods required by neutral consumers. |
| 5. Root and nested runtime/commit probes pass | implementation passed; acceptance fixture failed | All real probes pass, while one runtime test assumes a PyYAML-capable PATH interpreter absent in Codex. |
| 6. No hidden Claude ordering or least-common-denominator abstraction | failed | The effective shared interface is the concrete Claude adapter rather than the declared narrow ports; inspection also hides ambiguous managed groups. |

## Runtime evidence that passed

- Framework root: repository `.venv/Scripts/python.exe` resolved, PyYAML
  loaded, and the floor command executed (`command-executed: OK`).
- Directly opened live nested domain with no domain venv: the framework-root
  venv resolved and the floor command executed.
- Fresh nested Git repo with no domain venv: `install-hook` wrote the checked-in
  resolver, its automatic execution test passed, and a real
  `git hook run pre-commit` passed.
- An independent masked-PATH probe supplied failing `python`, `python3`, `py`,
  and `dirname` candidates; the nested hook still selected the framework venv
  and passed. The repair no longer depends on `dirname` or PATH Python.

The focused A/0–2 gate reported **38 passed, 1 failed**. The failure is
`test_probe_reports_command_executed_as_its_own_fact`: its broken entry lives
under pytest's temporary root, so runtime correctly derives that location as
the framework root; there is no venv there, and Codex's PATH Python cannot load
PyYAML. The test then incorrectly requires `resolved` to be non-null. Repair
the fixture with a controlled floor-capable candidate or mock at the candidate
boundary; do not weaken the production resolver.

## Blocking adapter-boundary findings

### Undeclared service-facing interface

`RenderPort` and `InspectPort` declare `capabilities`, `render`, and `inspect`.
The neutral consumers additionally call:

- `scaffold.py`: `shortcut_sources` and `scaffold_guidance`;
- `doctor.py`: `doctor_line`.

The architecture fitness test only verifies Render/Inspect conformance. A
minimal second adapter can therefore pass the declared gate, register
successfully, and then fail at runtime in scaffold and doctor. Codex must not
copy dummy Claude methods to accommodate that hidden interface. Make every
service dependency an explicit narrow port, or make shared services consume
only the existing ports; exercise a port-only fake through the real services.

### Claude inspection is not yet safe currency evidence

The current inspector can report an artifact current while:

- a managed token changes by prefix, such as `--quiet` to `--quietly`;
- an extra command is appended inside the managed PostToolUse group;
- a second group repeats the managed matcher and overwrites the first result;
- only an operator-owned hook event exists, yet the managed fragment is marked
  present.

These are not formatting differences. They are stale, extended, absent, or
ambiguous states and must remain distinct before inspection can feed Phase 3
diagnostics or Phase 5 merge/refusal decisions. Require token-boundary-safe
extensions, check exact managed hook counts, report duplicate candidate groups
as findings, and derive `present` only from a genuinely located managed
fragment.

## Claude-owned return package

1. Make shortcut projection, scaffold presentation, and diagnostic consumption
   explicit interfaces—or remove those requirements from neutral consumers.
2. Strengthen architecture fitness with a minimal non-Claude adapter that
   implements only declared contracts and is exercised through scaffold and
   doctor.
3. Correct Claude managed-fragment discovery and currency for token mutations,
   extra commands, duplicate matching groups, and operator-only hook events;
   add all four regression cases.
4. Make the `command_executed` runtime test independent of a PyYAML-capable
   PATH interpreter, and strengthen the PowerShell parity test so every
   candidate branch is pinned.
5. Rerun the focused handoff suite and complete full suite in the Codex managed
   shell, then return the clean commit for final acceptance.

Until that package returns, Codex Phases 3–5 are not authorised. The port and
inspection defects belong at the shared/Claude extraction boundary, not in a
Codex adapter workaround.
