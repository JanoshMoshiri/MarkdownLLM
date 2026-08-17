---
id: an-interface-is-what-its-consumers-call-not-what-it-declares
type: insight
status: active
version: 1.0
created: 2026-08-17
session: 2026-08-11
source: both
confidence: high
origin: stated
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: derived-from
    notes: "The v1.6 final-gate rejection: Claude's extraction passed the lexical fitness gate and declared-port conformance while scaffold and doctor called three undeclared Claude methods."
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: complements
    notes: "Why the author could not see it: one agent wrote both the adapter and its consumers, so every call-site felt like the contract. The gap was structural to the seat, not a lapse."
  - id: portability-claims-need-execution-tests
    relation: complements
    notes: "Same epistemics one level up: a declared contract is a claim; only an implementer that has ONLY the declaration, executed through the real consumers, is evidence."
---

# An interface is what its consumers call, not what it declares

## What happened

Phase 2C extracted the Claude adapter behind two declared ports (`RenderPort`,
`InspectPort`) and added an architecture fitness gate: a lexical scan proving
neutral modules contained no vendor vocabulary, plus a conformance check that
every registered adapter satisfied the declared protocols. Both were green.

The Codex final-gate audit rejected the handoff anyway. Scaffold called
`shortcut_sources` and `scaffold_guidance`; doctor called `doctor_line`. None
were declared on any port. A second adapter could satisfy every declared
protocol, register successfully, and crash both shared services at runtime.
The *effective* interface was the concrete Claude adapter; the declared ports
were a subset that no consumer actually lived within.

## The rule

**The interface a service depends on is the set of attributes it dereferences,
and no gate that inspects declarations can see it.** A lexical scan checks
vocabulary; a protocol-conformance check verifies the adapter against the
declaration; neither checks the declaration against the call-sites. The gap
between declared and effective interface is exactly where a second implementer
fails — and the first implementer cannot feel it, because their one concrete
class satisfies both by construction.

The mechanical fix is a **minimal implementer of only the declaration, driven
through the real consumers**: a port-only fake, registered, then run through
the production scaffold and doctor end-to-end. Any undeclared dereference
crashes the test at the exact call-site that leaked. After the v1.6 repair,
every service capability became a declared narrow port (`ShortcutPort`,
`ScaffoldNoticePort`, `DiagnosticPresentationPort`), consumers gained
isinstance gates so capability-absence is an answer rather than an error, and
the fake became a standing regression test.

## Where it generalises

Any boundary this framework declares and then consumes from the same hand:
domain schemas consumed by generated indexes, exposed faces consumed by
importing domains, prompt contracts consumed by bindings. Wherever declaration
and consumption are authored together, the declaration is untested until
something that has *only* the declaration is executed against the real
consumer. Deploy the fake-through-real-services pattern at any such seam when
a second implementer is expected.
