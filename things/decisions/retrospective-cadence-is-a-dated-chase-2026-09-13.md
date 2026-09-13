---
id: retrospective-cadence-is-a-dated-chase-2026-09-13
type: decision
status: made
version: 1.0
created: 2026-09-13
decided_by: the framework domain agent, evidence-led, on the operator's explicit delegation in voice, 2026-09-13
confidence: high
origin: inferred
tags: [retrospective, cadence, trigger, dispatcher, automation, seat-protocol, standing-authority]
informed_by:
  - id: retrospective-specification
    commit: 43dc588d461076773ff3a65b66537d2610bb03d5
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    commit: 43dc588d461076773ff3a65b66537d2610bb03d5
  - id: emitted-content-is-read-instructed-content-is-economised
    commit: 43dc588d461076773ff3a65b66537d2610bb03d5
  - id: feels-automatic-is-persistence-of-the-question
    commit: 43dc588d461076773ff3a65b66537d2610bb03d5
  - id: gates-census-ratified-2026-08-28
    commit: e27240d35c954ee43c3b4f5af2998afee51155c6
  - id: dispatch-loop
    commit: 43dc588d461076773ff3a65b66537d2610bb03d5
linked_things:
  - id: retrospective-specification
    relation: extends
    notes: "The time trigger it already states — monthly, with meaningful activity — becomes a dated chase the latest retrospective carries; its 'no obligation on a fixed schedule' sentence is kept and sharpened: a chase with no activity behind it is re-dated, not run."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: implements
    notes: "The razor this passes in exactly one form: the schedule is a thing (a trigger on the retrospective), the tick is dumb, and no scheduler outside the corpus decides."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
    notes: "Why an attended session does not silently run the ritual at t=0: un-pulled judgement at session start does not happen on any tier. The mechanical scans run; the judgement is offered."
  - id: feels-automatic-is-persistence-of-the-question
    relation: implements
    notes: "What the operator wants forgotten-proof is the tidying; the question 'is the retrospective due?' persists as a fired trigger in every digest until the ritual runs or the chase is re-dated."
  - id: closed-loop-operating-state
    relation: implements
    notes: "The unattended half is Phase 4 applied to one ritual: a dispatch run finds the trigger fired, runs the scans under the domain's own contract, drafts the retrospective, files every ruling to the seat."
  - id: framework-agent-closes-settled-cues-2026-09-13
    relation: references
    notes: "The authority under which an attended framework session completes a drafted retrospective's judgement half — promotions on met conditions, cue answers by citation, skill dispositions — leaving conflict rulings and unsettled items to the seat."
  - id: framework-retrospective-2026-09
    relation: references
    notes: "Carries the first chase: 2026-10-13, thirty days from its period_end."
---

# Decision: The Retrospective's Cadence Is A Dated Chase The Session Reads

The operator asked, 2026-09-13: *why wouldn't I automate a retrospective?
Every 30 days it just kicks off… if the session opens on the 30th day or the
31st or the 32nd, the retrospective will just kick off with session start…
the house gets messy because the kids have been playing all day; at the end
of the day I tidy up.* Then: *"you make the decision… lead by the evidence."*
This is that decision, and its evidence is named at each step.

## What the record says

1. **The spec already states the cadence — and refuses a fixed schedule.**
   `retrospective.md` → When To Write One: *triggered by time: when the
   domain crosses a monthly boundary with meaningful activity*; and,
   deliberately, *there is no obligation to write one on a fixed schedule;
   the purpose is reflection, not compliance.* The operator's own image
   agrees with both halves: the house is tidied because the children
   *played*, not because it is six o'clock.
2. **The spec already dates the chase, one radius out.** The estate
   retrospective's cadence is *a dated trigger in the vantage domain — 30
   days… the floor chases the date; the operator judges whether the moment
   has earned the ritual. Human-gated waits: date the chase.* The domain
   form was never written down; the floor's 60-day cadence check stood in
   for it as a late line.
3. **The schedule must be things.**
   `a-dispatch-layer-outside-the-corpus-is-a-second-brain`: cadences live as
   declared triggers, the only artifact outside the corpus is a dumb tick,
   and the dispatch prompt already runs *each fired trigger's bound ritual
   under that repo's own contract*. No scheduler is needed; one exists.
4. **A ritual instructed at t=0 of an attended session is economised.**
   `emitted-content-is-read-instructed-content-is-economised`, five runs
   across three harnesses and four models: the live request wins, and
   un-pulled judgement at session start does not happen. The `orient`
   binding exists because of this. A silent forty-minute ritual before the
   operator's first sentence would be skipped or would derail the session;
   the operator's own opt-out arrives after the collision.
5. **The ritual's outputs are a seat by ratified census.** Option-bearing
   retrospective outputs and conflict resolution are designed operator
   seats; the 13 September ruling gives the framework agent the rest of the
   judgement half where reasoning is settled. An unattended run holds
   neither authority: it raises, drafts, and files.

## The ruling

- **The cadence is a `type: time` trigger the latest retrospective carries**,
  dated thirty days from its `period_end` — the spec's monthly — with
  `action: surface`. The floor evaluates it at every session start and a
  dispatch run finds it fired. The 60-day cadence check stays as the late
  net beneath it.
- **The action gate is activity, not the calendar.** A fired chase with no
  `things/` movement since `period_end` is re-dated by the session that
  reads it, not run. This is the spec's *meaningful activity* clause made
  operative, and it keeps the ritual reflection rather than compliance.
- **Unattended: the dispatcher runs it.** When the trigger has fired, a
  dispatch run performs the ritual under the domain's own contract, writes
  the retrospective as `status: draft`, raises cues for what it modified,
  and files every ruling — conflicts, promotions, dispositions, the
  reflection's verdicts — to the seat. It never answers a cue and never
  completes the retrospective.
- **Attended: the digest offers, and the mechanical scans run first.** The
  fired trigger is the first line the session acts on: index rebuild, the
  cue list, the orphan findings and the conditions to re-read are produced
  immediately; the judgement half is offered as the session's first item,
  and the operator's "not now" defers it without losing it — the trigger
  stays fired. In the framework domain, the judgement half is then the
  agent's under `framework-agent-closes-settled-cues-2026-09-13`, except
  conflict rulings and anything unsettled.
- **Each retrospective arms the next chase and disarms the one it answered.**
  The ritual's last step. A trigger on a terminal carrier keeps firing until
  removed (the evaluator says so in words), so the ritual owns the handover.
- **The number is thirty days.** Not a new constant: it is the spec's
  "monthly" and the estate's existing thirty, applied one radius in. The
  floor's sixty stays what it was, the late line.

## What is not built

- No scheduler outside the corpus. No new floor mechanism: the trigger type,
  the evaluator, the digest line and the dispatch rule all exist.
- No silent auto-run at t=0 of an attended session.
- No change to who rules a conflict.

## Evidence this will be judged on

The next chase fires 2026-10-13. What to read then: whether the session
that meets it runs the mechanical scans and offers the rest (attended), or
whether a dispatch run has drafted it (unattended, once Phase 4 reaches a
ritual); whether the activity gate ever re-dates a chase; and whether a
drafted retrospective is completed within the session that reads it.
