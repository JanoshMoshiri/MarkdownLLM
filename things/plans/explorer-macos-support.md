---
id: explorer-macos-support
type: plan
status: not-started
version: 1.0
created: 2026-08-28
priority: medium
tags: [explorer, macos, packaging, portability, notarization]
linked_things:
  - id: explorer-publication-readiness
    relation: complements
    notes: "Same shape of blocker at the end: Windows needs Authenticode, macOS needs Apple notarization. Neither is a code change."
  - id: explorer-ui-increment-2026-08
    relation: references
  - id: an-attestation-bound-to-a-whole-tree-hash-is-terminal-by-construction
    relation: informs
    notes: "This increment seals its own evidence bundle. The ordering is mandatory, not advisory, and the last increment lost four cycles rediscovering that."
  - id: an-explanation-committed-to-a-specification-outlives-the-doubt-that-made-it
    relation: informs
    notes: "This work is written blind on a platform the authoring seat cannot execute. Every causal claim about macOS behaviour will be inferred rather than reproduced, which is exactly the condition that produced a false explanation last time."
  - id: a-test-anchored-in-source-text-fails-loudly-on-drift-and-silently-on-ambiguity
    relation: informs
    notes: "The macOS layer mirrors the Windows mutation anchors. Mirrored anchors multiply the fragments each one must remain unique against."
---

# Explorer on macOS

The operator needs the Explorer running on a Mac. This plan records what that
actually costs, measured rather than estimated, so the decision to start it is
made against numbers.

## The finding that shapes everything

**The application almost certainly already runs on macOS.** This was checked,
not assumed:

- The core runtime depends on **PyYAML alone**.
- There are **no** Windows-only imports outside the optional desktop launcher,
  and no core module imports that launcher.
- Only three platform branches exist in the whole runtime, and each already has
  a working non-Windows path.
- The wheel is `py3-none-any` — platform-independent by construction.

So the work is not "port the Explorer". It is "give macOS the native layer
Windows already has", plus one genuine security fix.

## Measured size

| | Lines |
|---|---|
| Whole product (code, tests, tools, browser assets) | 9,766 |
| The Windows-native layer inside it | 1,458 (≈15%) |
| The 0.3.0 interface increment, for calibration | 2,347 insertions across 43 files |

**macOS is roughly 60% the size of the 0.3.0 increment.** Of the 1,458 lines,
about 500 are genuinely new thinking and about 900 are translation:

- `windows_app.py` (418) — the real work. Menu-bar item instead of a tray icon,
  single instance by file lock instead of a named mutex.
- `verify_windows_installer.py` (368) — mirror in structure, different in
  substance: no registry, so `~/Applications`, LaunchServices and the quarantine
  attribute instead.
- `explorer.nsi` (203) — gets *simpler*. A DMG is a disk image holding an `.app`
  and a symlink to `/Applications`.
- `build.ps1` (163) — becomes a shell script; PyInstaller already produces
  `.app` bundles.
- `test_windows_app.py` (187) — mirror.
- icons, launcher shim, spec (119) — near-identical.

Plus about 28 specification and traceability rows, mirroring `FR-RUN-004/005/006`
and the `ST-WIN-*` family.

## The security fix, which is owed regardless

`_opened_final_path` returns `None` on anything that is not Windows. On Windows
it re-checks, *after the file handle is open*, that what actually opened is still
inside the source — the check that closes the gap between validating a path and
reading it. On macOS that check is currently skipped, so `NFR-SAFE-002B` claims
a confinement strength that platform does not have.

The macOS equivalent is `fcntl(fd, F_GETPATH)`. Roughly fifteen lines plus
tests. **This should be done whether or not the native app is built**, because
the requirement already makes the claim.

## What makes macOS harder than Windows, despite being smaller

**Notarization is mandatory in practice.** An unsigned Windows `.exe` warns;
an unnotarized macOS `.app` downloaded from the internet simply will not open.
It requires Apple Developer Program membership, then `codesign` →
`notarytool submit` → `stapler staple`. So unlike Windows, there is no
"ship it with a warning" fallback for the native bundle.

**The wheel route sidesteps this entirely.** `pip install` is not Gatekeeper's
business. A Mac user comfortable with Python has a working Explorer today with
no bundle, no membership and no notarization.

**Nothing here can be executed from the Windows seat.** The Windows layer was
built fast because it could be run and re-run locally. macOS work is written
blind and verified only by the operator, which slows the loop regardless of how
few lines it is. The right shape is therefore one uninterrupted arc ending in a
single testable artefact and an explicit list of what to try — not a
question-and-answer cadence, since questions cannot resolve what only a Mac can
answer.

The one genuine unknown is `pystray` on macOS, which needs an `NSApplication`
run loop on the main thread. That is where surprises are expected.

## Decisions owed before starting

1. **Wheel route only, or full `.app` + DMG + notarization?** They are different
   projects: the first is already done, the second is the 60% above.
2. **If native: is the Apple Developer membership being obtained?** Without it
   the bundle cannot ship at all, so building it first would be building
   something nobody can open.

## Phases, if the native route is chosen

- [ ] Confirm the wheel runs on macOS (operator, minutes — settles the premise).
- [ ] `F_GETPATH` confinement parity, with tests. Owed regardless.
- [ ] Menu-bar launcher: single instance, Open/Exit, no console, browser open.
- [ ] `.app` bundle and DMG via the existing PyInstaller route; `.icns` icons.
- [ ] macOS lifecycle verifier mirroring the Windows one.
- [ ] Requirements, test specification, traceability and acceptance journeys.
- [ ] Signed and notarized release, gated on Apple Developer membership.
