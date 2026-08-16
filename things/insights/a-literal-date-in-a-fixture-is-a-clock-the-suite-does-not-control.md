---
id: a-literal-date-in-a-fixture-is-a-clock-the-suite-does-not-control
type: insight
status: active
version: 1.0
created: 2026-08-16
session: 2026-08-16
source: field
confidence: high
origin: stated
disposition: keep-active
disposition_reason: >-
  A general test-hygiene rule with no live owner: it arose during the adapter
  work but is not about adapters, and inventing an inbound edge from that plan
  would misfile it. It earns a mechanical check eventually — flagging literal
  dates in fixtures that age past a sensor threshold — and belongs to
  mechanical-coherence-checks-backlog when that plan is next opened.
linked_things:
  - id: portability-claims-need-execution-tests
    relation: complements
    notes: "That insight measures the environment a test runs in; this one names the other uncontrolled variable — the date it runs on."
---

# A literal date in a fixture is a clock the suite does not control

## What happened

A floor self-test wrote a fixture with `created: 2026-07-16` and asserted
that the quarantine sensor produced **no** findings. That sensor raises an
Info once an external thing has been unverified for more than 30 days.

The test passed for thirty days. On the thirty-first it failed in CI, with a
diff that displayed the sensor's message as the unexpected value — pointing
the reader at the sensor, which was working exactly as specified. The defect
was in the fixture, and the fixture had not changed.

## The rule

**A fixture dated with a literal is a second clock, running at the same rate
as the real one but frozen at write time.** Any assertion of the form "this
produces no findings" then holds only until the gap between the two clocks
crosses a threshold some sensor keys on. The test does not fail when the code
changes; it fails when the calendar does.

Date fixtures **relative to the run** wherever any check measures elapsed
time — age, staleness, cadence, expiry, retention. A literal date is safe
only where nothing measures duration, and that safety is a property of
today's sensors, not a permanent one.

## Why the failure is worse than an ordinary red

Three properties compound:

1. **The delay separates cause from effect.** The change that introduced the
   bomb is thirty commits back; the diff implicates code touched five minutes
   ago.
2. **It accuses the correct component.** The sensor is named in the failure
   output, so the first instinct is to question the sensor — the one part
   that is behaving properly.
3. **Green proves nothing.** The suite was green every day until it was not,
   so a passing run cannot distinguish "correct" from "not yet expired".

That third property also disqualifies the obvious fix-verification: making
the test green again is exactly what the broken version already did.
Demonstrate the repair by **moving the clock** — this one was re-run with the
date shifted 400 days forward — so the proof is that the fixture no longer
ages into the threshold at all.

## Where it applies beyond tests

Any assertion that pins a *relationship between two dates* while recording
only one of them: an example in documentation showing a "recent" timestamp, a
golden file containing a computed age, a fixture asserting a domain is "in
sync". The general form is that an absolute value was stored where a relative
one was meant.
