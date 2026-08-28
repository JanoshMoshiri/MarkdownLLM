"""Trigger evaluation — time, dependency, threshold, and import conditions.

Relationship triggers and `blocked_duration` need change history the floor
does not keep; they are reported as not-mechanically-evaluable rather than
silently skipped. Import triggers key on the state imports-check computes —
a live face read, crossed lazily at most once per run. Includes the deadline
horizon scan over every non-terminal date-bearing thing. (The tenth review
caught this docstring and the CLI help claiming three families while the
code below evaluates four — an agent reading --help would re-derive import
states by reasoning, duplicating a floor check.)
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .model import ISO_RE, Corpus, is_terminal, scan

_DATE_IN_TEXT = re.compile(r"(\d{4}-\d{2}-\d{2})")

# A `git log --name-only` walk interleaves date lines with path lines; the
# date shape tells them apart without needing a NUL/control delimiter.
_ISO_DAY = re.compile(r"\d{4}-\d{2}-\d{2}")

# Import states meaning the floor could not SEE the source at all — distinct
# from the states it read and can match against. A trigger may legitimately
# watch FOR one of these values; only unavailability the trigger did not ask
# about becomes unevaluable (substrate-totality-residue #1).
_IMPORT_UNAVAILABLE = frozenset(
    {"unreachable", "no-address-book-entry", "incomplete"})


def _git_touch_map(root: Path) -> dict[str, "dt.date"]:
    """{repo-relative posix path: date of its most recent commit} in ONE git
    pass. The per-path alternative (`git log -1 -- <path>` per stale trigger)
    cost a subprocess each — ~0.6s apiece on Windows — and scaled with the
    trigger count; sixteen of them were most of session-start's git time."""
    out = subprocess.run(["git", "log", "--format=%cs", "--name-only"],
                         cwd=root, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if out.returncode != 0:
        return {}
    seen: dict[str, dt.date] = {}
    cur: dt.date | None = None
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if _ISO_DAY.fullmatch(line):
            cur = dt.date.fromisoformat(line)
        elif cur is not None:
            seen.setdefault(line, cur)  # log is newest-first: first wins
    return seen

# The self-answering pattern (session-start-hardening Phase 3): an armed
# future-dated trigger whose ACTION text already answers its own condition
# — "do not re-ask", "already issued", "both remedies are spent". Left
# armed, it fires on its own answer. Six triggers wore this at once in one
# live domain (2026-08-18). A heuristic cue, not a verdict: the
# disarm/re-condition judgement stays the agent's.
_SELF_ANSWERING = re.compile(
    r"(?:do\s+not|don'?t)\s+re-?ask"
    r"|already\s+(?:answered|issued|discharged|resolved|sent)"
    r"|remed(?:y|ies)\s+(?:is|are)\s+spent", re.I)


def _embedded_date(cond):
    """First ISO date appearing anywhere in a free-text condition, or None."""
    if not isinstance(cond, str):
        return None
    m = _DATE_IN_TEXT.search(cond)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


# Lazy membrane reads for `type: import` triggers — crossed at most once per
# evaluation run, and only if such a trigger exists. Cleared at the start of
# every evaluate() so each run reads live state.
_MEMBRANE_CACHE: dict = {}


class TriggerOutcome(str, Enum):
    """The exhaustive mechanical result for one declared trigger."""

    FIRED = "fired"
    NOT_FIRED = "not-fired"
    UNEVALUABLE = "unevaluable"
    INVALID = "invalid"


@dataclass(frozen=True)
class TriggerResult:
    """One trigger declaration reduced to exactly one explicit outcome.

    ``messages`` retains the established CLI wording.  It may contain more
    than one line when one declaration watches several imports, but the
    declaration still has one outcome.  ``timing`` is populated only for a
    valid future condition and lets the compatibility projection keep the
    existing upcoming/horizon sections without confusing either with fired.
    """

    thing_id: str
    trigger_index: int
    trigger_type: str
    condition: Any
    action: Any
    outcome: TriggerOutcome
    reason: str
    messages: tuple[str, ...] = ()
    timing: str | None = None
    days_until: int | None = None
    advisories: tuple[str, ...] = ()


@dataclass(frozen=True)
class TriggerEvaluation:
    """Total trigger results plus the deadline attention surface."""

    results: tuple[TriggerResult, ...]
    deadline_fired: tuple[str, ...] = ()
    deadline_upcoming: tuple[tuple[int, str], ...] = ()
    deadline_horizon: tuple[tuple[int, str], ...] = ()

    def legacy(self) -> tuple[list[str], list[tuple[int, str]],
                              list[tuple[int, str]], list[str], list[str]]:
        """Project typed results onto the long-standing five CLI buckets."""
        fired: list[str] = []
        upcoming: list[tuple[int, str]] = []
        horizon: list[tuple[int, str]] = []
        skipped: list[str] = []
        advisories: list[str] = []
        for result in self.results:
            if result.outcome is TriggerOutcome.FIRED:
                fired.extend(result.messages)
            elif result.outcome is TriggerOutcome.NOT_FIRED:
                if result.timing == "upcoming" and result.days_until is not None:
                    upcoming.extend((result.days_until, line)
                                    for line in result.messages)
                elif result.timing == "horizon" and result.days_until is not None:
                    horizon.extend((result.days_until, line)
                                   for line in result.messages)
            else:
                skipped.extend(result.messages or (
                    f"{result.thing_id}: {result.outcome.value} "
                    f"trigger[{result.trigger_index}] - {result.reason}",
                ))
            advisories.extend(result.advisories)
        fired.extend(self.deadline_fired)
        upcoming.extend(self.deadline_upcoming)
        horizon.extend(self.deadline_horizon)
        return fired, upcoming, horizon, skipped, advisories


def _import_states(root: Path) -> dict | None:
    key = ("states", str(root))
    if key not in _MEMBRANE_CACHE:
        try:
            from .imports_check import imports_freshness
            _MEMBRANE_CACHE[key] = {r["id"]: r["state"]
                                    for r in imports_freshness(root)}
        except Exception:
            _MEMBRANE_CACHE[key] = None
    return _MEMBRANE_CACHE[key]


def _porch_coverage(root: Path) -> list | None:
    key = ("porch", str(root))
    if key not in _MEMBRANE_CACHE:
        try:
            from .imports_check import face_coverage
            _MEMBRANE_CACHE[key] = face_coverage(root)
        except Exception:
            _MEMBRANE_CACHE[key] = None
    return _MEMBRANE_CACHE[key]


def _evaluate_typed_impl(root: Path,
                         corpus: Corpus | None = None) -> TriggerEvaluation:
    """Evaluate every declaration to one typed result without input throws.

    `fired` holds only conditions that are TRUE NOW (a date reached, a
    dependency satisfied, a threshold crossed) — including a matured free-text
    date whose carrier has settled, explicitly labelled with its TERMINAL
    carrier so the obligation cannot go dark the day it fires (estate
    synthesis 2026-08, F6 defect 2). `upcoming` holds conditions
    maturing within 30 days — look-aheads, deliberately a separate bucket:
    v3.29.0 and earlier mixed both into one `hits` list that session-start
    labelled "Triggers fired", so a quiet domain with a busy fortnight ahead
    read as a domain under pressure (2026-08-08 field evidence, two domains).
    `horizon` is beyond 30 days; `skipped` is not-mechanically-evaluable;
    `selfanswer` is the heuristic cue for armed future triggers whose action
    text already answers the condition (see _SELF_ANSWERING)."""
    _MEMBRANE_CACHE.clear()
    if corpus is None:
        corpus, _ = scan(root)
    today = dt.date.today()
    by_id = corpus.by_id()
    hits: list[str] = []
    upcoming: list[tuple[int, str]] = []
    skipped: list[str] = []
    horizon: list[tuple[int, str]] = []
    selfanswer: list[str] = []
    results: list[TriggerResult] = []

    def as_date(v):
        if isinstance(v, dt.datetime):
            return v.date()
        if isinstance(v, dt.date):
            return v
        if isinstance(v, str) and ISO_RE.match(v):
            try:
                return dt.date.fromisoformat(v[:10])
            except ValueError:
                return None
        return None

    touch_map: dict[str, dt.date] | None = None

    def last_activity(path: Path) -> dt.date | None:
        # Staleness keys on the commit stream, not mtime: mtime is clone-local
        # noise (a fresh checkout resets it, a stray touch renews it) while
        # git history is the domain's actual activity record (review 5 drift
        # item; thing-lifecycle's last_active-from-git is the same fact).
        # mtime is the fallback for untracked files / no git. The map is one
        # `git log --name-only` walk built lazily on the first stale trigger.
        nonlocal touch_map
        if touch_map is None:
            touch_map = _git_touch_map(root)
        try:
            rel = path.resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            rel = None
        if rel is not None and rel in touch_map:
            return touch_map[rel]
        try:
            return dt.date.fromtimestamp(path.stat().st_mtime)
        except OSError:
            return None

    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        status = str(meta.get("status", ""))
        declarations = meta.get("triggers")
        if declarations is None:
            continue
        if not isinstance(declarations, list):
            reason = "`triggers` must be a list of declarations"
            results.append(TriggerResult(
                str(name), -1, "<collection>", None, None,
                TriggerOutcome.INVALID, reason,
                (f"{name}: invalid trigger collection - {reason}",),
            ))
            continue
        for trigger_index, tr in enumerate(declarations):
            if not isinstance(tr, dict):
                reason = "declaration must be a mapping"
                results.append(TriggerResult(
                    str(name), trigger_index, "<invalid>", None, None,
                    TriggerOutcome.INVALID, reason,
                    (f"{name}: invalid trigger[{trigger_index}] - {reason}",),
                ))
                continue
            ttype, cond, action = tr.get("type"), tr.get("condition"), tr.get("action")
            start_hits = len(hits)
            start_upcoming = len(upcoming)
            start_horizon = len(horizon)
            start_skipped = len(skipped)
            start_selfanswer = len(selfanswer)
            forced: TriggerOutcome | None = None
            reason = "condition is currently false"

            if not isinstance(ttype, str) or not ttype.strip():
                forced = TriggerOutcome.INVALID
                reason = "trigger type is missing or is not a string"
                skipped.append(f"{name}: invalid trigger[{trigger_index}] - {reason}")
            elif action is None or (isinstance(action, str) and not action.strip()):
                forced = TriggerOutcome.INVALID
                reason = "trigger action is missing or empty"
                skipped.append(f"{name}: invalid trigger[{trigger_index}] - {reason}")
            elif ttype in ("time", "date"):
                # `date` is accepted as an alias of `time` — domains write it
                # naturally, and it is one character of drift away from a
                # silently dead control (estate audit FW-1).
                if not isinstance(cond, str) or not cond.strip():
                    forced = TriggerOutcome.INVALID
                    reason = "time trigger condition is missing or is not text"
                    skipped.append(f"{name}: invalid time trigger - {reason}")
                elif cond == "due_date_passed":
                    raw_due = meta.get("due_date")
                    due = as_date(raw_due)
                    if due is None:
                        forced = TriggerOutcome.INVALID
                        reason = ("`due_date_passed` requires a valid `due_date`; "
                                  f"found {raw_due!r}")
                        skipped.append(f"{name}: invalid due-date trigger - {reason}")
                    elif due < today and not is_terminal(corpus.schema, meta):
                        reason = f"due_date {due} passed {(today - due).days}d ago"
                        hits.append(f"{name}: due_date {due} passed "
                                    f"({(today - due).days}d ago) -> {action}")
                    elif due < today:
                        # Deliberate silence, unlike the matured free-text
                        # date branch below: a due_date belongs to the work
                        # itself, so the carrier settling IS the deadline
                        # satisfied — nothing outlives it to surface.
                        reason = f"due_date {due} passed but the thing is terminal"
                    else:
                        reason = f"due_date {due} has not passed"
                elif cond == "review_date_reached":
                    raw_review = meta.get("review_date")
                    rd = as_date(raw_review)
                    if rd is None:
                        forced = TriggerOutcome.INVALID
                        reason = ("`review_date_reached` requires a valid `review_date`; "
                                  f"found {raw_review!r}")
                        skipped.append(f"{name}: invalid review-date trigger - {reason}")
                    elif rd <= today:
                        reason = f"review_date {rd} has been reached"
                        hits.append(f"{name}: review_date {rd} reached -> {action}")
                    else:
                        reason = f"review_date {rd} has not been reached"
                elif cond == "stale":
                    raw_threshold = tr.get("threshold", "30d")
                    match = (None if isinstance(raw_threshold, bool) else
                             re.fullmatch(r"\s*(\d+)\s*d?\s*",
                                          str(raw_threshold), re.I))
                    if match is None:
                        forced = TriggerOutcome.INVALID
                        reason = (f"stale threshold {raw_threshold!r} is invalid; "
                                  "use a non-negative day duration such as `30d`")
                        skipped.append(f"{name}: invalid stale trigger - {reason}")
                    else:
                        threshold_days = int(match.group(1))
                        last = last_activity(t.path)
                        if last is None:
                            forced = TriggerOutcome.UNEVALUABLE
                            reason = "last activity is unavailable from Git and the filesystem"
                            skipped.append(f"{name}: stale trigger {reason}")
                        else:
                            age = (today - last).days
                            reason = (f"last activity was {age}d ago; threshold is "
                                      f"{threshold_days}d")
                            if age > threshold_days:
                                hits.append(f"{name}: unmodified {age}d "
                                            f"(threshold {threshold_days}d) -> {action}")
                else:
                    # Free-text time condition. Recover a date if the condition
                    # names one; otherwise say so instead of falling through
                    # silently (the else below is on TYPE, so it never fires
                    # here — the no-silent-default law, same bug class as the
                    # `relationship` branch one screen down).
                    d = _embedded_date(cond)
                    if (d is not None and d > today and action
                            and _SELF_ANSWERING.search(str(action))):
                        selfanswer.append(
                            f"{name}: armed for {d} while its action text "
                            f"already answers the condition — disarm or "
                            f"re-condition")
                    if d is None:
                        forced = TriggerOutcome.UNEVALUABLE
                        reason = (f"time condition {cond!r} names no parseable "
                                  "date and requires agent judgement")
                        skipped.append(f"{name}: time condition {cond!r} names no "
                                       f"parseable date - left to the agent")
                    elif d <= today and not is_terminal(corpus.schema, meta):
                        reason = f"date {d} has been reached"
                        hits.append(f"{name}: time condition {cond!r} - date {d} "
                                    f"reached ({(today - d).days}d ago) -> {action}")
                    elif d <= today:
                        # A matured obligation on a settled carrier. Until
                        # v3.36.x this branch set a reason and appended to NO
                        # bucket, so the obligation vanished from `mdllm
                        # triggers` and the session-start digest on the day it
                        # fired — while the same carrier's FUTURE dates kept
                        # reporting as upcoming/horizon below (estate synthesis
                        # 2026-08 F6 defect 2, read out of this source by an
                        # operating domain: a dated obligation goes dark when
                        # its carrier settles). No-silent-default: it surfaces
                        # in the fired bucket, labelled with its terminal
                        # carrier; whether the obligation transfers to a live
                        # carrier, dies with this one, or disarms is the
                        # agent's judgement — possible only when it is seen.
                        reason = (f"date {d} reached on a terminal carrier "
                                  f"(status `{status}`) — surfaced, not dropped")
                        hits.append(f"{name}: time condition {cond!r} - date {d} "
                                    f"reached ({(today - d).days}d ago) on "
                                    f"TERMINAL carrier (status `{status}`) "
                                    f"-> {action}")
                    elif (d - today).days <= 30:
                        reason = f"date {d} is {(d - today).days}d away"
                        upcoming.append(((d - today).days,
                                         f"{name}: time condition {cond!r} - fires in "
                                         f"{(d - today).days}d ({d}) -> {action}"))
                    else:
                        reason = f"date {d} is {(d - today).days}d away"
                        horizon.append(((d - today).days,
                                        f"{name}: time condition {cond!r} fires {d} "
                                        f"({(d - today).days}d out)"))
            elif ttype == "dependency":
                raw_watch = tr.get("watch")
                watch = (raw_watch if isinstance(raw_watch, list)
                         else [raw_watch] if raw_watch is not None else [])
                value = tr.get("value")
                bad_watch = [w for w in watch
                             if not isinstance(w, str) or not w.strip()]
                missing = [w for w in watch
                           if isinstance(w, str) and w not in by_id]
                event = tr.get("on")
                if bad_watch:
                    forced = TriggerOutcome.INVALID
                    reason = f"dependency watch contains invalid ids: {bad_watch!r}"
                    skipped.append(f"{name}: invalid dependency trigger - {reason}")
                elif missing:
                    forced = TriggerOutcome.INVALID
                    reason = ("dependency trigger watches absent thing(s): "
                              + ", ".join(f"`{w}`" for w in missing))
                    skipped.append(f"{name}: invalid dependency trigger - {reason}")
                elif event == "status_changed_to":
                    if not watch:
                        forced = TriggerOutcome.INVALID
                        reason = "dependency trigger has an empty `watch` set"
                        skipped.append(f"{name}: invalid dependency trigger - {reason}")
                    elif value is None or isinstance(value, (list, dict)):
                        forced = TriggerOutcome.INVALID
                        reason = "`status_changed_to` requires one scalar `value`"
                        skipped.append(f"{name}: invalid dependency trigger - {reason}")
                    else:
                        states = [str(by_id[w].meta.get("status")) for w in watch]
                        reason = (f"watched states are {dict(zip(watch, states))}; "
                                  f"required `{value}`")
                        if all(s == str(value) for s in states):
                            hits.append(f"{name}: all watched ({', '.join(watch)}) are "
                                        f"`{value}` -> {action}")
                elif event in ("priority_changed", "any_modification") and watch:
                    forced = TriggerOutcome.UNEVALUABLE
                    reason = f"dependency event `{event}` needs change history"
                    skipped.append(f"{name}: dependency trigger `{event}` needs "
                                   "change history - left to the agent")
                elif tr.get("condition"):
                    forced = TriggerOutcome.UNEVALUABLE
                    reason = (f"dependency prose condition {tr.get('condition')!r} "
                              "requires agent judgement")
                    skipped.append(f"{name}: dependency trigger with prose "
                                   f"condition {tr.get('condition')!r} — "
                                   f"left to the agent")
                else:
                    forced = TriggerOutcome.INVALID
                    reason = ("dependency trigger is not in the evaluable shape "
                              "(`on: status_changed_to` + non-empty `watch` + `value`)")
                    skipped.append(f"{name}: dependency trigger not in the "
                                   f"evaluable shape (`on: status_changed_to` "
                                   f"+ `watch` + `value`) — never fires as "
                                   f"declared")
            elif ttype == "threshold":
                if cond == "subtasks_complete":
                    links = meta.get("linked_things")
                    if links is not None and not isinstance(links, list):
                        forced = TriggerOutcome.INVALID
                        reason = "`linked_things` is not a list, so subtasks are invalid"
                        skipped.append(f"{name}: invalid subtasks trigger - {reason}")
                        links = []
                    subs = [e.get("id") for e in (links or [])
                            if isinstance(e, dict) and e.get("relation") == "subtask"]
                    bad_subs = [s for s in subs
                                if not isinstance(s, str) or not s.strip()]
                    missing_subs = [s for s in subs
                                    if isinstance(s, str) and s not in by_id]
                    if forced is TriggerOutcome.INVALID:
                        pass
                    elif not subs:
                        forced = TriggerOutcome.INVALID
                        reason = ("`subtasks_complete` has no declared subtasks; "
                                  "an empty set is not completion")
                        skipped.append(f"{name}: invalid subtasks trigger - {reason}")
                    elif bad_subs:
                        forced = TriggerOutcome.INVALID
                        reason = f"subtask links contain invalid ids: {bad_subs!r}"
                        skipped.append(f"{name}: invalid subtasks trigger - {reason}")
                    elif missing_subs:
                        forced = TriggerOutcome.INVALID
                        reason = ("subtask link(s) are absent: "
                                  + ", ".join(f"`{s}`" for s in missing_subs))
                        skipped.append(f"{name}: invalid subtasks trigger - {reason}")
                    else:
                        incomplete = [s for s in subs
                                      if not is_terminal(corpus.schema, by_id[s].meta)]
                        reason = ("all declared subtasks are terminal" if not incomplete
                                  else "non-terminal subtasks: "
                                  + ", ".join(f"`{s}`" for s in incomplete))
                    if forced is None and not incomplete:
                        hits.append(f"{name}: all subtasks complete -> {action}")
                elif cond == "blocked_duration":
                    raw_threshold = tr.get("threshold")
                    match = (None if isinstance(raw_threshold, bool) else
                             re.fullmatch(r"\s*(\d+)\s*d?\s*",
                                          str(raw_threshold), re.I)
                             if raw_threshold is not None else None)
                    if match is None:
                        forced = TriggerOutcome.INVALID
                        reason = (f"blocked_duration threshold {raw_threshold!r} is "
                                  "invalid; use a day duration such as `7d`")
                        skipped.append(f"{name}: invalid threshold trigger - {reason}")
                    else:
                        forced = TriggerOutcome.UNEVALUABLE
                        reason = ("`blocked_duration` needs status history "
                                  f"to test its {int(match.group(1))}d threshold")
                        skipped.append(f"{name}: `blocked_duration` needs status history "
                                       f"(evaluate via git log) — left to the agent")
                else:
                    forced = TriggerOutcome.INVALID
                    reason = f"unknown threshold condition {cond!r}"
                    skipped.append(f"{name}: invalid threshold trigger - {reason}")
            elif ttype == "relationship":
                # Watching another thing's field change needs event history the
                # floor doesn't keep — same honesty line as blocked_duration,
                # not silence (review 6, finding 3: the no-silent-default law
                # violated in miniature by the tool that enforces it).
                raw_watch = tr.get("watch")
                watch = (raw_watch if isinstance(raw_watch, list)
                         else [raw_watch] if raw_watch is not None else [])
                bad_watch = [w for w in watch
                             if not isinstance(w, str) or not w.strip()]
                missing = [w for w in watch
                           if isinstance(w, str) and w not in by_id]
                if bad_watch:
                    forced = TriggerOutcome.INVALID
                    reason = f"relationship watch contains invalid ids: {bad_watch!r}"
                    skipped.append(f"{name}: invalid relationship trigger - {reason}")
                elif missing:
                    forced = TriggerOutcome.INVALID
                    reason = ("relationship trigger watches absent thing(s): "
                              + ", ".join(f"`{w}`" for w in missing))
                    skipped.append(f"{name}: invalid relationship trigger - {reason}")
                    # Keep the established CLI cue as a second line while the
                    # typed result makes the stronger invalidity explicit.
                    skipped.append(f"{name}: `relationship` trigger "
                                   f"(on: {tr.get('on', '?')}, "
                                   f"watch: {tr.get('watch', '?')}) needs "
                                   "change history — left to the agent")
                elif not watch and not tr.get("condition"):
                    forced = TriggerOutcome.INVALID
                    reason = "relationship trigger has neither `watch` nor `condition`"
                    skipped.append(f"{name}: invalid relationship trigger - {reason}")
                else:
                    forced = TriggerOutcome.UNEVALUABLE
                    reason = "relationship change detection needs history or agent judgement"
                    skipped.append(f"{name}: `relationship` trigger "
                                   f"(on: {tr.get('on', '?')}, watch: {tr.get('watch', '?')}) "
                                   f"needs change history — left to the agent")
            elif ttype == "import":
                # Keyed to the state imports-check computes — a live,
                # consumer-side face read (trigger-specification.md ->
                # Import-based). Lazy: the membrane is crossed at most once
                # per evaluation run, and only if an import trigger exists.
                icond = tr.get("condition") or "state_is"
                if icond == "state_is":
                    states = _import_states(root)
                    if states is None:
                        forced = TriggerOutcome.UNEVALUABLE
                        reason = "imports machinery is unavailable, so state is unknown"
                        skipped.append(f"{name}: import trigger — imports "
                                       f"machinery unavailable, state unknown")
                    else:
                        raw_watch = tr.get("watch")
                        watch = (raw_watch if isinstance(raw_watch, list)
                                 else [raw_watch] if raw_watch is not None
                                 else list(states))
                        raw_values = tr.get("value", ["stale", "diverged", "withdrawn"])
                        values = (raw_values if isinstance(raw_values, list)
                                  else [raw_values])
                        bad_watch = [w for w in watch
                                     if not isinstance(w, str) or not w.strip()]
                        bad_values = [v for v in values
                                      if not isinstance(v, str) or not v.strip()]
                        unknown = [w for w in watch
                                   if isinstance(w, str) and w not in states]
                        if not watch:
                            forced = TriggerOutcome.INVALID
                            reason = ("import trigger has an empty watch set; no "
                                      "imports exist or were selected")
                            skipped.append(f"{name}: invalid import trigger - {reason}")
                        elif bad_watch:
                            forced = TriggerOutcome.INVALID
                            reason = f"import watch contains invalid ids: {bad_watch!r}"
                            skipped.append(f"{name}: invalid import trigger - {reason}")
                        elif not values or bad_values:
                            forced = TriggerOutcome.INVALID
                            reason = "import `value` must contain one or more state names"
                            skipped.append(f"{name}: invalid import trigger - {reason}")
                        elif unknown:
                            forced = TriggerOutcome.INVALID
                            reason = ("import trigger watches absent import(s): "
                                      + ", ".join(f"`{w}`" for w in unknown))
                            for w in unknown:
                                skipped.append(f"{name}: import trigger watches `{w}` "
                                               f"but no such import exists here")
                        else:
                            route_invalid = {w: states[w] for w in watch
                                             if states[w] ==
                                             "unevaluable-invalid-config"}
                            unevaluable = {w: states[w] for w in watch
                                           if str(states[w]).startswith("unevaluable-")
                                           and w not in route_invalid}
                            # Unavailability the trigger did not ask about is
                            # not a state mismatch: `unreachable` /
                            # `no-address-book-entry` / `incomplete` mean the
                            # floor never read the watched state, so falling
                            # through to the match test minted a confident
                            # `not-fired` from a state it could not see. A
                            # trigger watching FOR one of these values keeps
                            # it as a match candidate — only the unasked-for
                            # case degrades (substrate-totality-residue #1;
                            # the porch branch is the sibling specification).
                            unevaluable.update(
                                {w: states[w] for w in watch
                                 if states[w] in _IMPORT_UNAVAILABLE
                                 and states[w] not in values
                                 and w not in route_invalid})
                            if route_invalid:
                                forced = TriggerOutcome.INVALID
                                reason = ("route configuration is invalid for "
                                          + ", ".join(f"`{w}`" for w in route_invalid))
                                for w in route_invalid:
                                    skipped.append(f"{name}: import `{w}` route "
                                                   "configuration is invalid — "
                                                   "left unevaluable")
                            elif unevaluable:
                                forced = TriggerOutcome.UNEVALUABLE
                                reason = ("one or more watched import routes cannot "
                                          "be evaluated")
                                for w, state in unevaluable.items():
                                    if state == "unevaluable-untrusted":
                                        route_reason = ("route is untrusted "
                                                        "and was not executed")
                                    elif state in _IMPORT_UNAVAILABLE:
                                        route_reason = (f"is {state} — its "
                                                        f"watched state could "
                                                        f"not be read")
                                    else:
                                        route_reason = "route is unevaluable"
                                    skipped.append(f"{name}: import `{w}` {route_reason} — "
                                                   f"left unevaluable")
                            else:
                                fired = {w: states[w] for w in watch
                                         if states[w] in values}
                                reason = ("matching imports: "
                                          + ", ".join(f"`{w}`={s}" for w, s in fired.items())
                                          if fired else "no watched import state matches "
                                          + repr(values))
                                for w, state in fired.items():
                                    hits.append(f"{name}: import `{w}` is {state} -> {action}")
                elif icond == "porch_offers_unimported":
                    cov = _porch_coverage(root)
                    if cov is None:
                        forced = TriggerOutcome.UNEVALUABLE
                        reason = "face coverage is unavailable"
                        skipped.append(f"{name}: import trigger — face "
                                       f"coverage unavailable")
                    else:
                        src_filter = tr.get("source")
                        if src_filter is not None and not isinstance(src_filter, str):
                            forced = TriggerOutcome.INVALID
                            reason = "porch trigger `source` must be a server name"
                            skipped.append(f"{name}: invalid porch trigger - {reason}")
                        else:
                            selected = [c for c in cov if isinstance(c, dict)
                                        and (not src_filter or
                                             c.get("source") == src_filter)]
                            malformed = [c for c in cov if not isinstance(c, dict)]
                            if malformed:
                                forced = TriggerOutcome.INVALID
                                reason = "face coverage returned malformed entries"
                                skipped.append(f"{name}: invalid porch result - {reason}")
                            elif not selected:
                                forced = TriggerOutcome.INVALID
                                reason = (f"no face named `{src_filter}` exists"
                                          if src_filter else
                                          "no faces exist; an empty set is not success")
                                skipped.append(f"{name}: invalid porch trigger - {reason}")
                            else:
                                invalid_rows = [c for c in selected if c.get("state") ==
                                                "unevaluable-invalid-config"]
                                unknown_rows = [c for c in selected if c.get("state") in
                                                ("unreachable", "unevaluable-untrusted")]
                                if invalid_rows:
                                    forced = TriggerOutcome.INVALID
                                    reason = "one or more selected face routes are invalid"
                                    for c in invalid_rows:
                                        skipped.append(f"{name}: face `{c.get('source')}` route "
                                                       f"configuration is invalid — offering "
                                                       f"unevaluable")
                                elif unknown_rows:
                                    forced = TriggerOutcome.UNEVALUABLE
                                    reason = ("one or more selected faces are unreachable "
                                              "or untrusted; partial coverage cannot fire")
                                    for c in unknown_rows:
                                        if c.get("state") == "unreachable":
                                            skipped.append(f"{name}: face `{c.get('source')}` "
                                                           f"unreachable — offering unknown")
                                        else:
                                            skipped.append(f"{name}: face `{c.get('source')}` "
                                                           f"route is untrusted and was not "
                                                           f"executed — offering unevaluable")
                                else:
                                    malformed_counts = [c for c in selected
                                                        if not isinstance(c.get("imported"), int)
                                                        or not isinstance(c.get("offered"),
                                                                          (int, type(None)))]
                                    if malformed_counts:
                                        forced = TriggerOutcome.INVALID
                                        reason = "face coverage counts are malformed"
                                        skipped.append(f"{name}: invalid porch result - {reason}")
                                    else:
                                        fired_rows = [c for c in selected
                                                      if (c.get("offered") or 0) >
                                                      c.get("imported", 0)]
                                        reason = ("one or more faces offer unimported things"
                                                  if fired_rows else
                                                  "all selected face offerings are imported")
                                        for c in fired_rows:
                                            hits.append(f"{name}: face `{c['source']}` offers "
                                                        f"{c['offered']}, imported "
                                                        f"{c['imported']} -> {action}")
                else:
                    forced = TriggerOutcome.INVALID
                    reason = f"unknown import trigger condition {icond!r}"
                    skipped.append(f"{name}: import trigger condition "
                                   f"{icond!r} is not one the floor knows "
                                   f"(state_is, porch_offers_unimported)")
            else:
                forced = TriggerOutcome.INVALID
                reason = f"unrecognised trigger type `{ttype}`"
                skipped.append(f"{name}: unrecognised trigger type `{ttype}` — "
                               f"not evaluated")

            new_hits = tuple(hits[start_hits:])
            new_upcoming = tuple(upcoming[start_upcoming:])
            new_horizon = tuple(horizon[start_horizon:])
            new_skipped = tuple(skipped[start_skipped:])
            if forced is not None:
                outcome = forced
            elif new_hits:
                outcome = TriggerOutcome.FIRED
            elif new_skipped:
                # Defensive default: any intentionally non-mechanical branch
                # should set ``forced`` above.  If a future branch forgets,
                # silence is still impossible and the honest result is
                # unevaluable rather than a fabricated false.
                outcome = TriggerOutcome.UNEVALUABLE
                reason = new_skipped[0]
            else:
                outcome = TriggerOutcome.NOT_FIRED

            timing = None
            days_until = None
            messages: tuple[str, ...]
            if outcome is TriggerOutcome.FIRED:
                messages = new_hits
            elif outcome in (TriggerOutcome.INVALID,
                              TriggerOutcome.UNEVALUABLE):
                messages = new_skipped
            elif new_upcoming:
                timing = "upcoming"
                days_until = new_upcoming[0][0]
                messages = tuple(line for _, line in new_upcoming)
            elif new_horizon:
                timing = "horizon"
                days_until = new_horizon[0][0]
                messages = tuple(line for _, line in new_horizon)
            else:
                messages = ()
            results.append(TriggerResult(
                thing_id=str(name), trigger_index=trigger_index,
                trigger_type=str(ttype), condition=cond, action=action,
                outcome=outcome, reason=reason, messages=messages,
                timing=timing, days_until=days_until,
                advisories=tuple(selfanswer[start_selfanswer:]),
            ))

    # Deadline scan: every non-terminal date-bearing thing, triggers or not.
    # OVERDUE is never suppressed by a declared trigger — the more carefully
    # authored thing must not get less warning (estate audit FW-1).
    deadline_fired: list[str] = []
    deadline_upcoming: list[tuple[int, str]] = []
    deadline_horizon: list[tuple[int, str]] = []
    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        due = as_date(meta.get("due_date"))
        if due and not is_terminal(corpus.schema, meta):
            days = (due - today).days
            if days < 0:
                note = "" if meta.get("triggers") else ", no trigger declared"
                deadline_fired.append(
                    f"{name}: OVERDUE by {-days}d (due {due}{note})")
            elif 0 <= days <= 30:
                deadline_upcoming.append(
                    (days, f"{name}: due in {days}d ({due})"))
            elif days > 30:
                deadline_horizon.append(
                    (days, f"{name}: due {due} ({days}d out)"))

    return TriggerEvaluation(
        results=tuple(results), deadline_fired=tuple(deadline_fired),
        deadline_upcoming=tuple(deadline_upcoming),
        deadline_horizon=tuple(deadline_horizon),
    )


def evaluate_typed(root: Path,
                   corpus: Corpus | None = None) -> TriggerEvaluation:
    """Total public boundary: malformed input becomes ``invalid``, never an exception.

    ``corpus`` lets a caller that already scanned the same worktree share the
    scan; session-start's four consumers each rescanning the corpus was most
    of its budget overrun."""
    try:
        return _evaluate_typed_impl(Path(root).resolve(), corpus)
    except Exception as exc:
        reason = ("trigger evaluation failed safely: "
                  f"{type(exc).__name__}: {exc}")
        return TriggerEvaluation(results=(TriggerResult(
            thing_id="_trigger-evaluation", trigger_index=-1,
            trigger_type="<domain>", condition=None, action=None,
            outcome=TriggerOutcome.INVALID, reason=reason,
            messages=(f"_trigger-evaluation: invalid - {reason}",),
        ),))


def evaluate_results(root: Path) -> tuple[TriggerResult, ...]:
    """Return the exhaustive per-declaration result surface."""
    return evaluate_typed(root).results


def evaluate(root: Path,
             corpus: Corpus | None = None) -> tuple[list[str], list[tuple[int, str]],
                                                    list[tuple[int, str]], list[str],
                                                    list[str]]:
    """Backward-compatible five-bucket projection used by the existing CLI."""
    return evaluate_typed(root, corpus).legacy()


def _print_evaluation(hits, upcoming, horizon, skipped,
                      selfanswer=()) -> None:
    if hits:
        for h in hits:
            print(f"- {h}")
    else:
        print("No trigger conditions currently true.")
    if upcoming:
        print("\n### Upcoming (within 30 days — not yet fired)")
        for _, line in sorted(upcoming):
            print(f"- {line}")
    if horizon:
        print("\n### Horizon (beyond 30 days)")
        for _, line in sorted(horizon):
            print(f"- {line}")
    if skipped:
        print("\n### Not mechanically evaluable")
        for s in skipped:
            print(f"- {s}")
    if selfanswer:
        print("\n### Self-answering armed triggers (heuristic)")
        for s in selfanswer:
            print(f"- {s}")


def cmd_triggers(args) -> int:
    root = Path(args.path).resolve()
    today = dt.date.today()

    if getattr(args, "estate", False):
        # Operator-axis batch over per-domain evaluations — the estate
        # attention sweep. Roots come from the same local-clone walk
        # estate-sync uses (repos-not-membranes: a filesystem fact, not an
        # estate manifest). Ephemeral roll-up, never an index. Run after
        # `estate-sync` — the sweep is only as honest as the clones are
        # fresh (an-unpulled-checkout-orients-on-a-past-domain).
        from .sync import discover_repos
        repos = discover_repos(root)
        if not repos:
            print(f"triggers --estate: no local clones under {root}")
            return 0
        print(f"## Estate Trigger Sweep — {len(repos)} local clone(s) walked "
              f"({today})\nA filesystem fact, not an estate manifest; "
              f"sync before sweeping.\n")
        total_hits = 0
        rollup = []
        for repo in repos:
            hits, upcoming, horizon, skipped, selfanswer = evaluate(repo)
            # Retrospective debt joins the sweep (estate-cadence-cluster
            # Phase 2): per-domain the v3.24.0 sensor fires as scatter across
            # thirteen validates; here it lands as one picture in the one
            # sweep the operator's estate loop already reads. Quiet when
            # healthy — the sensor's own young/dormant gates hold.
            # A failed computation must not render identically to "no debt
            # owed" — the swallow made an error read as health
            # (substrate-totality-residue sibling). None = could not compute;
            # "" = computed, quiet.
            retro: str | None = ""
            try:
                from .model import scan as _scan
                from .validation import retrospective_findings as _retro
                _corpus, _ = _scan(repo)
                rf = _retro(repo, _corpus)
                if rf:
                    retro = rf[0].message.split(" — ")[0].split(" (")[0]
            except Exception as exc:
                retro = None
                print(f"(retrospective state unavailable for {repo.name}: "
                      f"{type(exc).__name__})")
            rollup.append((repo.name, len(hits), len(upcoming), len(skipped), retro))
            total_hits += len(hits)
            print(f"### {repo.name}")
            _print_evaluation(hits, upcoming, horizon, skipped, selfanswer)
            print()
        print("### Roll-up")
        overdue = 0
        unknown_retro = 0
        for name, nh, nu, ns, retro in rollup:
            line = (f"- {name}: {nh} fired, {nu} upcoming (≤30d), "
                    f"{ns} not mechanically evaluable")
            if retro is None:
                line += " — retrospective state UNKNOWN (computation failed)"
                unknown_retro += 1
            elif retro:
                line += f" — RETROSPECTIVE DEBT: {retro}"
                overdue += 1
            print(line)
        tailbits = [f"{total_hits} trigger(s) fired across the walk"]
        if overdue:
            tailbits.append(f"{overdue} domain(s) owe a retrospective")
        if unknown_retro:
            tailbits.append(f"{unknown_retro} domain(s) with unknown "
                            f"retrospective state")
        print(f"\n{'; '.join(tailbits)}. Ephemeral — never an index.")
        return 0

    hits, upcoming, horizon, skipped, selfanswer = evaluate(root)
    print(f"## Trigger Evaluation — {root}  ({today})\n")
    _print_evaluation(hits, upcoming, horizon, skipped, selfanswer)
    return 0
