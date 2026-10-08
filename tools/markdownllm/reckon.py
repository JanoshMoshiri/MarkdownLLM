"""`mdllm reckon` — the reckoning: the release half of the loop
(the-reckoning-is-the-digestion-beat-2026-10-05; `session-memory.md` → The
Reckoning).

Attention items are created at three cadences and, until this command,
disposed of at none (`circulation-is-not-disposition`). The reckoning reads
every attention item in a corpus — active insights, open conflicts, open cues,
fired triggers, imported mirrors, stale non-terminal work — and names its
disposition candidate with the evidence, in three bands:

- **mechanical** — derivable from a field or a git fact; the floor may apply
  it (`--apply`, Phase 2): a `promoted_to` that resolves, a conflict whose one
  party is superseded, a plan with every box ticked, a trigger whose action
  text already answers its condition.
- **settled** — the agent decides by reading the record: dismiss or
  consolidate an insight nothing live cites, rule or hold an aged conflict out
  of circulation, answer a cue by citation, re-pin a stale mirror, re-date a
  trigger its thing has outlived, pause work that stopped.
- **residue** — the operator rules, through the harness's own prompt: a
  conflict still in circulation, a held item whose stated condition may have
  come true, a mirror that diverged in meaning, work to cancel.

Nothing enters without its exit: each kind carries a default interval (below),
and a thing may override it with ``settles_when: YYYY-MM-DD`` — the date after
which the default disposition is proposed. The floor computes and proposes; it
never marks a verdict (Phase 1 is read-only, exit 0 always). A clean reckoning
is an empty residue: green is reachable.

Staleness keys on the commit stream, never mtime, in one git walk — the same
economy validate's conflict-age row and session-start's stall lines use.

A hold carries its next look: a held item leaves the band until its
`settles_when` date, or, without one, until one interval after it was last
changed — a hold the agent just made is not asked again tomorrow
(`--keep` writes the hold and its date in one move). The close
(`--close`, the-reckoning Phase 3) is what a session end owes: the mechanical
band applied, and the backlog chased — ten decisions a day while one stands,
or the band emptied: the oldest residue first, put to the operator through the
harness's own prompt, then workflow items, open cues and fired triggers, then
the longest-waiting of the rest. The commit gate
refuses a `session-end:` commit until the close is met; an unattended run
applies the mechanical band and drafts the rest into its digest.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .model import ISO_RE, TERMINAL_STATUSES, is_terminal, origin_is_external, scan
from .structural_refs import iter_structural_references

# Exit intervals per kind, in days: the default reader for "has this item
# earned its disposition?" A thing's own `settles_when` date overrides.
INTERVALS = {
    "insight": 60,     # active with nothing live citing it → dismiss or consolidate
    "conflict": 30,    # open and untouched → rule, link or hold (belief-revision.md)
    "work": 21,        # non-terminal and untouched → the stall line (session-start)
}
# Knowledge and structure types are not "work": they are reckoned by their own
# rules above, or not at all (a spec is walked, never paused).
_NOT_WORK = {"insight", "cue", "conflict", "decision", "retrospective", "index",
             "prompt", "skill", "specification", "guide", "manifesto",
             "workflow-definition", "example", "artifact", "continuity-brief",
             "dispatch-digest", "import"}
_CHECKBOX = re.compile(r"^\s*- \[( |x|X)\]", re.M)
_SELF_ANSWERED = re.compile(r"already answers", re.I)


@dataclass
class Item:
    kind: str        # insight | conflict | cue | trigger | import | work
    thing_id: str
    band: str        # mechanical | settled | residue
    proposal: str    # the disposition proposed, as a verb phrase
    evidence: str    # why, in one line
    fields: dict = field(default_factory=dict)  # what --apply would set (mechanical only)
    waited: int = 0  # days the item has waited — the close takes the oldest first


def _date(v) -> dt.date | None:
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


def _touch_map(root: Path) -> dict[str, dt.date] | None:
    """{repo-relative posix path: date of its newest commit}, one git walk
    over things/. None when git cannot be read — the caller then says so."""
    try:
        r = subprocess.run(["git", "log", "--format=%x1e%cs", "--name-only",
                            "--", "things"], cwd=root, capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=60)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    touch: dict[str, dt.date] = {}
    for record in r.stdout.split("\x1e"):
        header, _, paths = record.partition("\n")
        try:
            day = dt.date.fromisoformat(header.strip())
        except ValueError:
            continue
        for line in paths.splitlines():
            line = line.strip()
            if line:
                touch.setdefault(line, day)  # newest-first: first wins
    return touch


def _rel(root: Path, t) -> str:
    try:
        return t.path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return ""


def _settles_when(meta) -> dt.date | None:
    return _date(meta.get("settles_when"))


def _due(meta, created: dt.date | None, interval: int, today: dt.date) -> tuple[bool, int]:
    """(past its exit date?, age in days). A declared `settles_when` wins."""
    age = (today - created).days if created else 0
    sw = _settles_when(meta)
    if sw is not None:
        return today >= sw, age
    return age >= interval, age


def _hold_due(meta, idle: int | None, created: dt.date | None, interval: int,
              today: dt.date) -> tuple[bool, int, str]:
    """A hold's next look: its `settles_when`, else one interval after it was
    last changed (a hold made today is not asked again tomorrow), else — git
    unreadable — one interval after it was created. (due?, waited, said)."""
    sw = _settles_when(meta)
    if sw is not None:
        return today >= sw, max(0, (today - sw).days), f"look-again date {sw}"
    if idle is not None:
        return idle >= interval, idle, f"last looked at {idle}d ago"
    age = (today - created).days if created else 0
    return age >= interval, age, f"{age}d old"


def reckon_report(root: Path, corpus, *, today: dt.date | None = None,
                  imports: bool = False, workflows: bool = False,
                  triggers: bool = True,
                  touch: dict | None = None) -> dict:
    """Every attention item's disposition candidate, banded, with evidence.

    A caller that already walked the things/ history passes its `touch` map
    and the reckoning reads no git of its own; session start does exactly
    that, and leaves `triggers` to the digest's own triggers line, so the
    hook's bounded scan and walk counts do not grow (the hook once ran 67s
    against a 60s budget because consumers each rescanned)."""
    today = today or dt.date.today()
    root = Path(root).resolve()
    by_id = {t.id: t for t in corpus.things if t.id}
    # Liveness is graph-keyed, as validate reads it: an inbound edge from a
    # thing whose status is not universally terminal keeps an item in
    # circulation (session-memory.md → Insight Lifecycle Management).
    live_inbound: dict[str, int] = defaultdict(int)
    for t in corpus.things:
        if str(t.meta.get("status")) in TERMINAL_STATUSES:
            continue
        for ref in iter_structural_references(t.meta, validation_only=True):
            live_inbound[ref.target] += 1
    if touch is None:
        touch = _touch_map(root)
    items: list[Item] = []
    notes: list[str] = []
    if touch is None:
        notes.append("git history over things/ could not be read — untouched "
                     "ages are unknown; only field-derived candidates are listed")
        touch = {}

    def untouched_days(t) -> int | None:
        rel = _rel(root, t)
        last = touch.get(rel) if rel else None
        return (today - last).days if last else None

    # ---- insights ---------------------------------------------------------
    # Mirrors (`origin: external`) are reckoned by the workspace that owns
    # them; here they are read, never disposed.
    for t in corpus.things:
        m = t.meta
        if not t.id or str(m.get("type")) != "insight" or str(m.get("status")) != "active":
            continue
        if origin_is_external(m):
            continue
        promoted_to = m.get("promoted_to")
        if isinstance(promoted_to, list):
            promoted_to = promoted_to[0] if promoted_to else None
        if promoted_to and str(promoted_to) in by_id:
            items.append(Item("insight", t.id, "mechanical", "promote",
                              f"`promoted_to` names `{promoted_to}`, which exists; "
                              "status still active",
                              {"status": "promoted"}))
            continue
        due, age = _due(m, _date(m.get("created")), INTERVALS["insight"], today)
        held = str(m.get("disposition", "")) == "keep-active"
        cited = live_inbound.get(t.id, 0)
        if held:
            # A hold states its own exit. Most stated conditions are facts
            # the agent can check in the corpus (a mechanism shipped, a sweep
            # ran, a plan started); it reads them and either disposes or
            # re-dates the hold with `settles_when`. Only a condition the
            # agent cannot read is the operator's — the agent escalates it.
            reason = str(m.get("disposition_reason", "")).strip()
            hold_due, waited, said = _hold_due(
                m, untouched_days(t), _date(m.get("created")), INTERVALS["insight"], today)
            if hold_due:
                items.append(Item("insight", t.id, "settled",
                                  "read the stated condition: met → dispose; not → re-date",
                                  f"keep-active, {said}; reason: "
                                  f"{reason or '(none stated — give one or dispose)'}",
                                  waited=waited))
            continue
        if cited == 0:
            if due:
                items.append(Item("insight", t.id, "settled", "dismiss or consolidate",
                                  f"active {age}d, nothing live cites it", waited=age))
            continue
        if age >= 2 * INTERVALS["insight"] and _settles_when(m) is None:
            items.append(Item("insight", t.id, "settled",
                              "promote into the operating layer, or state why it stays",
                              f"active {age}d, cited by {cited} live thing(s) and never promoted",
                              waited=age))

    # ---- conflicts --------------------------------------------------------
    for t in corpus.things:
        m = t.meta
        if not t.id or str(m.get("type")) != "conflict" or str(m.get("status")) != "open":
            continue
        if origin_is_external(m):
            continue  # a mirrored conflict is its source workspace's to rule
        # belief-revision.md: the two positions sit in `parties`; older
        # conflicts carry them only as `contradicts` links.
        declared = m.get("parties")
        if isinstance(declared, list) and declared:
            parties = [str(p) for p in declared]
        else:
            parties = [str(l.get("id")) for l in (m.get("linked_things") or [])
                       if isinstance(l, dict) and l.get("id")
                       and str(l.get("relation")) in {"contradicts", "supersedes", "superseded-by"}]
        party_things = [by_id[p] for p in parties if p in by_id]
        gone = [p for p in parties if p not in by_id]
        superseded = [p for p in party_things
                      if str(p.meta.get("status")) in {"superseded", "deprecated"}]
        if party_things and len(superseded) == 1 and len(party_things) >= 2:
            survivor = next(p.id for p in party_things if p is not superseded[0])
            items.append(Item("conflict", t.id, "mechanical", "resolve: superseded",
                              f"one party (`{superseded[0].id}`) is {superseded[0].meta.get('status')}; "
                              f"`{survivor}` survives",
                              {"status": "resolved", "resolution": "superseded",
                               "resolved_by": survivor}))
            continue
        if party_things and all(str(p.meta.get("status")) in TERMINAL_STATUSES
                                for p in party_things):
            items.append(Item("conflict", t.id, "mechanical", "resolve: dismissed",
                              "every party is closed out; nothing live holds either position",
                              {"status": "resolved", "resolution": "dismissed"}))
            continue
        if gone and not party_things:
            items.append(Item("conflict", t.id, "settled", "resolve or re-link",
                              f"its parties no longer exist: {', '.join(gone)}"))
            continue
        held = str(m.get("disposition", "")) == "keep-active"
        reason = str(m.get("disposition_reason", "")).strip()
        due, age = _due(m, _date(m.get("created")), INTERVALS["conflict"], today)
        idle = untouched_days(t)
        if held and reason:
            hold_due, waited, said = _hold_due(
                m, idle, _date(m.get("created")), INTERVALS["conflict"], today)
            if hold_due:
                items.append(Item("conflict", t.id, "settled",
                                  "read what would resolve it: happened → rule; not → re-date",
                                  f"held, {said}; reason: {reason}", waited=waited))
            continue
        stale = idle is not None and idle >= INTERVALS["conflict"]
        if not (stale or due):
            continue
        cited = live_inbound.get(t.id, 0)
        where = f"open {age}d, untouched {idle if idle is not None else '?'}d"
        if cited:
            items.append(Item("conflict", t.id, "residue", "rule: choose a side, or hold with a reason",
                              f"{where}, in circulation ({cited} live thing(s) link it)",
                              waited=age))
        else:
            items.append(Item("conflict", t.id, "settled", "rule, link from live work, or hold",
                              f"{where}, nothing live links it", waited=age))

    # ---- cues -------------------------------------------------------------
    for t in corpus.things:
        m = t.meta
        if t.id and str(m.get("type")) == "cue" and str(m.get("status")) == "open":
            created = _date(m.get("created"))
            age = (today - created).days if created else 0
            items.append(Item("cue", t.id, "settled", "answer by citation, or walk",
                              f"open {age}d on `{m.get('subject')}`", waited=age))

    # ---- fired triggers ---------------------------------------------------
    results = ()
    if triggers:
        try:
            from .triggers import TriggerOutcome, evaluate_typed
            results = evaluate_typed(root, corpus=corpus).results
        except Exception as exc:  # the trigger engine says what it cannot read
            results = ()
            notes.append(f"triggers could not be evaluated: {type(exc).__name__}")
    else:
        from .triggers import TriggerOutcome
    for r in results:
        if r.outcome is not TriggerOutcome.FIRED:
            continue
        label = f"{r.thing_id}[{r.trigger_index}]"
        if any(_SELF_ANSWERED.search(a) for a in r.advisories):
            items.append(Item("trigger", label, "mechanical", "disarm",
                              "its action text already answers its condition",
                              {"disarm": r.trigger_index}))
            continue
        thing = by_id.get(r.thing_id)
        cond_day = _date(r.condition) if not isinstance(r.condition, dict) else None
        if cond_day is None and isinstance(r.condition, str):
            found = re.search(r"\d{4}-\d{2}-\d{2}", r.condition)
            cond_day = dt.date.fromisoformat(found.group(0)) if found else None
        idle = untouched_days(thing) if thing is not None else None
        waited = max(0, (today - cond_day).days) if cond_day is not None else 0
        if (thing is not None and cond_day is not None and idle is not None
                and (today - idle * dt.timedelta(days=1)) > cond_day):
            items.append(Item("trigger", label, "settled", "re-date or disarm",
                              f"fired ({r.trigger_type}); the thing moved "
                              f"{(today - cond_day).days - idle}d after the condition "
                              "— was it acted on?", waited=waited))
        else:
            items.append(Item("trigger", label, "settled", "act, re-date or disarm",
                              f"fired ({r.trigger_type}): {r.reason}", waited=waited))

    # ---- imported mirrors (opt-in: reads the membrane) --------------------
    if imports:
        try:
            from .imports_check import imports_freshness
            rows = imports_freshness(root)
        except Exception as exc:
            rows = []
            notes.append(f"imports could not be checked: {type(exc).__name__}")
        for row in rows:
            state = row.get("state")
            iid = str(row.get("id"))
            if state == "stale":
                items.append(Item("import", iid, "settled", "re-read and re-pin",
                                  "the source moved under the pin"))
            elif state == "withdrawn":
                items.append(Item("import", iid, "settled", "retire the mirror",
                                  "no longer exposed by the source"))
            elif state == "diverged":
                items.append(Item("import", iid, "residue", "re-read: meaning changed",
                                  "the mirror no longer matches the face"))
            elif state == "unreachable":
                notes.append(f"import `{iid}`: source unreachable — not reckoned")

    # ---- work -------------------------------------------------------------
    for t in corpus.things:
        m = t.meta
        typ = str(m.get("type"))
        if not t.id or typ in _NOT_WORK or origin_is_external(m):
            continue
        if is_terminal(corpus.schema, m):
            continue
        try:
            body = t.path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            body = ""
        boxes = _CHECKBOX.findall(body)
        if boxes and all(b.lower() == "x" for b in boxes):
            items.append(Item("work", t.id, "mechanical", "complete",
                              f"every box ticked ({len(boxes)}/{len(boxes)}), status {m.get('status')}",
                              {"status": "completed"}))
            continue
        idle = untouched_days(t)
        due, age = _due(m, _date(m.get("created")), INTERVALS["work"], today)
        sw = _settles_when(m)
        if sw is not None:
            # A declared look-again date governs: before it the work is
            # waiting on purpose; after it the agent looks again, and only a
            # cancellation is the operator's.
            if due:
                items.append(Item("work", t.id, "settled",
                                  "look again: continue, re-date, or put cancelling to the operator",
                                  f"past its `settles_when` ({sw}); status {m.get('status')}"
                                  + (f"; it waited on: {m.get('disposition_reason')}"
                                     if m.get("disposition_reason") else ""),
                                  waited=(today - sw).days))
            continue
        if idle is None or idle < INTERVALS["work"]:
            continue
        parent = m.get("parent")
        parent_thing = by_id.get(str(parent)) if parent else None
        if parent_thing is not None and str(parent_thing.meta.get("status")) == "cancelled":
            items.append(Item("work", t.id, "residue", "cancel or re-parent",
                              f"untouched {idle}d; its parent `{parent}` is cancelled",
                              waited=idle))
            continue
        ticked = sum(1 for b in boxes if b.lower() == "x")
        status = str(m.get("status"))
        if status == "not-started":
            proposal = "start, or say when (`--keep`)"
        elif status in {"paused", "blocked"}:
            proposal = "unblock, or say what it waits on (`--keep`)"
        else:
            proposal = "pause, or say what it waits on (`--keep`)"
        items.append(Item("work", t.id, "settled", proposal,
                          f"{status} and untouched {idle}d"
                          + (f"; {ticked}/{len(boxes)} boxes ticked" if boxes else ""),
                          waited=idle))

    # ---- workflows (workflow-state.md → Workflows Emerge From Use) ---------
    # Emergence and dissolution are the two halves of the workspace learning
    # its own process; both are the agent's, organically, and only a
    # departure from what the operator authored is theirs.
    if workflows:
        try:
            from .workflows import (bindings_report, emergent_candidates,
                                    read_history)
            hist = read_history(root)
            for c in emergent_candidates(root, corpus, hist):
                if c.overlaps:
                    items.append(Item("workflow", c.carrier, "settled",
                                      f"bind `{c.overlaps[0]}` to it — carrier and map only, "
                                      "stages and edges untouched",
                                      f"{c.moves} moves by {c.things} things across {c.days} "
                                      f"days travel `{c.carrier}` through "
                                      f"{' · '.join(c.stages)}"))
                else:
                    items.append(Item("workflow", c.carrier, "settled",
                                      "write the emerged workflow (`mdllm workflows "
                                      "--emergent --draft`) and its steps",
                                      f"{c.moves} moves by {c.things} things across {c.days} "
                                      f"days: {' · '.join(c.stages)}"))
            last_move: dict[str, dt.date] = {}
            for mv in hist.moves:
                if mv.thing_type:
                    last_move[mv.thing_type] = max(last_move.get(mv.thing_type, mv.day), mv.day)
            by_id_local = {t.id: t for t in corpus.things if t.id}
            for row in bindings_report(root, corpus, hist):
                if not row["carrier"] or row["origin"] == "mirror":
                    continue
                if row["departures"]:
                    band = "settled" if row["origin"] == "inferred" else "residue"
                    items.append(Item("workflow", row["id"], band,
                                      "revise the workflow, or name the slip"
                                      if band == "settled" else
                                      "rule: has the practice moved, or did the work slip?",
                                      f"{len(row['departures'])} move(s) its edges do not "
                                      "declare, since it last changed"))
                d = by_id_local.get(row["id"])
                if (row["origin"] == "inferred" and row["status"] != "deprecated"
                        and d is not None):
                    from .workflows import carrier_types
                    recent = [last_move.get(x) for x in carrier_types(d.meta)]
                    recent = [x for x in recent if x]
                    idle = (today - max(recent)).days if recent else None
                    if idle is None or idle >= INTERVALS["insight"]:
                        items.append(Item("workflow", row["id"], "mechanical",
                                          "dissolve",
                                          "inferred, and nothing has moved through it "
                                          + (f"for {idle}d" if idle is not None else "on record"),
                                          {"status": "deprecated"}))
        except Exception as exc:
            notes.append(f"workflows could not be read: {type(exc).__name__}")

    bands = {"mechanical": [], "settled": [], "residue": []}
    for it in items:
        bands[it.band].append(it)
    for band in bands.values():
        band.sort(key=lambda i: (i.kind, i.thing_id))
    return {"today": today, "bands": bands, "notes": notes,
            "imports_read": imports}


_BAND_HEAD = {
    "mechanical": "the floor can apply these — derivable from a field or a git fact",
    "settled": "the agent decides, citing the record",
    "residue": "the operator rules, through the harness's own prompt",
}


def render(rep: dict, root: Path) -> list[str]:
    lines = [f"## The reckoning — {root}", f"as of {rep['today']}"]
    if not rep["imports_read"]:
        lines.append("(imported mirrors not read — pass `--imports` to reckon the membrane)")
    total = sum(len(v) for v in rep["bands"].values())
    for band in ("mechanical", "settled", "residue"):
        items = rep["bands"][band]
        if not items:
            continue
        lines.append(f"- **{band.capitalize()} ({len(items)}):** {_BAND_HEAD[band]}:")
        for it in items:
            lines.append(f"    - {it.kind} `{it.thing_id}` → {it.proposal} — {it.evidence}")
    if total == 0:
        lines.append("- none — every attention item is within its interval or already "
                     "disposed; the residue is empty")
    for n in rep["notes"]:
        lines.append(f"- (note) {n}")
    return lines




# ------------------------------------------------------------------ apply
# The mechanical band is a status derivable from a field or a git fact; the
# floor writes that status the way it writes any generated surface — in
# place, same-builder checkable, and the agent commits it (`reckon:`). It
# never writes a verdict of meaning, never touches the settled or residue
# bands, and never disarms a trigger (re-conditioning a declaration stays the
# agent's, `trigger-specification.md`).

_APPLIABLE_KINDS = {"insight", "conflict", "work", "workflow"}


def _set_frontmatter(path: Path, fields: dict) -> bool:
    """Set or add scalar fields in a thing's frontmatter, in place. Returns
    False when the file has no frontmatter block."""
    raw = path.open(encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---", 4)
    if end == -1:
        return False
    head, body = text[4:end], text[end:]
    lines = head.split("\n")
    for key, value in fields.items():
        pat = re.compile(rf"^{re.escape(key)}:.*$")
        for i, ln in enumerate(lines):
            if pat.match(ln):
                # The old value may run on (a folded reason, a list): its
                # continuation lines go with it, or the YAML breaks.
                j = i + 1
                while j < len(lines) and lines[j][:1] in (" ", "\t", "-"):
                    j += 1
                lines[i:j] = [f"{key}: {value}"]
                break
        else:
            lines.append(f"{key}: {value}")
    out = "---\n" + "\n".join(lines) + body
    path.open("w", encoding="utf-8", newline="").write(out.replace("\n", "\r\n") if crlf else out)
    return True


def apply_mechanical(root: Path, corpus, rep: dict) -> list[str]:
    """Apply the mechanical band; return one receipt line per item."""
    by_id = {t.id: t for t in corpus.things if t.id}
    receipts: list[str] = []
    for it in rep["bands"]["mechanical"]:
        if it.kind not in _APPLIABLE_KINDS or not it.fields:
            receipts.append(f"left to the agent: {it.kind} `{it.thing_id}` → {it.proposal}")
            continue
        t = by_id.get(it.thing_id)
        if t is None:
            continue
        if _set_frontmatter(t.path, it.fields):
            receipts.append(f"applied: {it.kind} `{it.thing_id}` → "
                            + ", ".join(f"{k}: {v}" for k, v in it.fields.items())
                            + f" — {it.evidence}")
        else:
            receipts.append(f"could not write: {it.kind} `{it.thing_id}` (no frontmatter block)")
    return receipts


def keep(root: Path, corpus, thing_id: str, reason: str,
         until: dt.date | None = None, today: dt.date | None = None) -> str:
    """The agent's hold, written in one move: the reason and the next look.
    An insight or a conflict is marked `keep-active`; work keeps its status
    and records what it waits on. Without `until`, the next look is one
    interval out for the item's kind. Returns the receipt, or raises
    ValueError when the thing cannot be held."""
    today = today or dt.date.today()
    t = next((x for x in corpus.things if x.id == thing_id), None)
    if t is None:
        raise ValueError(f"no thing `{thing_id}` in this corpus")
    if not reason.strip():
        raise ValueError("a hold states its reason")
    typ = str(t.meta.get("type"))
    if typ in ("insight", "conflict"):
        kind = typ
    elif typ in _NOT_WORK or is_terminal(corpus.schema, t.meta):
        raise ValueError(f"`{thing_id}` is a {typ} at status "
                         f"{t.meta.get('status')} — not an item the reckoning holds")
    else:
        kind = "work"
    until = until or today + dt.timedelta(days=INTERVALS[kind])
    fields = {}
    if kind != "work":
        fields["disposition"] = "keep-active"
    fields["disposition_reason"] = json.dumps(reason.strip(), ensure_ascii=False)
    fields["settles_when"] = until.isoformat()
    if not _set_frontmatter(t.path, fields):
        raise ValueError(f"`{thing_id}` has no frontmatter block")
    return f"held: {kind} `{thing_id}` until {until.isoformat()} — {reason.strip()}"


# ------------------------------------------------------------ disposition
# A change that only records a disposition — a status the reckoning moved, a
# hold and its reason, a look-again date, a trigger re-dated, a version bumped
# alongside — moves no claim anything reasons from, so it owes no walk (the
# walk gate and the cue listing both read this; the-reckoning Phase 3). One
# exception keeps the walk honest: a status that *withdraws* a claim
# (dismissed, superseded, deprecated, cancelled) leaves its dependants
# reasoning from something no longer held, and stays a walk candidate.

DISPOSITION_KEYS = frozenset({
    "status", "version", "disposition", "disposition_reason", "settles_when",
    "promoted_to", "resolution", "resolved_by", "resolved", "completed",
    "triggers"})
WITHDRAWING = frozenset({"dismissed", "superseded", "deprecated", "cancelled",
                         "retired", "withdrawn"})
_TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$")


def without_disposition(text: str) -> str:
    """The text with its disposition fields taken out of the frontmatter, so
    two versions that differ only in disposition compare equal. A
    withdrawing status is kept: withdrawing a claim is not bookkeeping."""
    t = text.replace("\r\n", "\n")
    if not t.startswith("---\n"):
        return t
    end = t.find("\n---", 4)
    if end == -1:
        return t
    out: list[str] = []
    skipping = False
    for ln in t[4:end].split("\n"):
        m = _TOP_KEY.match(ln)
        if m:
            key, value = m.group(1), m.group(2).strip().strip("'\"")
            skipping = key in DISPOSITION_KEYS and not (
                key == "status" and value in WITHDRAWING)
            if skipping:
                continue
        elif skipping and (ln[:1] in (" ", "\t", "-") or not ln.strip()):
            continue
        else:
            skipping = False
        out.append(ln)
    return "---\n" + "\n".join(out) + t[end:]


# A diff line that records a disposition (the rate's walk count and the
# close's count of decisions read diffs, not whole files).
_DISPOSITION_LINE = re.compile(
    r"^\s*(?:-\s+)?(status|version|disposition|disposition_reason|settles_when|"
    r"promoted_to|resolution|resolved_by|resolved|completed|triggers|condition|"
    r"action|note)\s*:")
_DECISION_LINE = re.compile(
    r"^\s*(?:-\s+)?(status|disposition|disposition_reason|settles_when|"
    r"promoted_to|resolution|resolved_by|condition)\s*:")


# ------------------------------------------------------------------ rates
# The rate on the wall: is disposition keeping pace with intake? Read off one
# git walk over things/ for the window — created attention items, status
# moves into a terminal state, definition-surface changes and the walks
# recorded for them. A rate, not a state (`coherence-is-a-maintained-rate-
# not-a-state`).

_ATTENTION = {"insight", "conflict", "cue"}
_DISPOSED = {"promoted", "dismissed", "resolved", "answered", "completed", "cancelled"}
_DEFINITION_SURFACES = {"specification", "skill", "guide", "manifesto", "prompt",
                        "workflow-definition", "insight", "decision"}
_FILE_RE = re.compile(r"^diff --git a/(.*?) b/(.*?)$")
_PLUS_STATUS = re.compile(r"^\+status:\s*(\S+)")
_PLUS_TYPE = re.compile(r"^\+type:\s*(\S+)")


def rates(root: Path, corpus, days: int = 7) -> dict:
    """{created: {kind: n}, disposed: n, surface_changes: n, walks: n, days}
    for the last ``days`` days; None values when git cannot be read."""
    try:
        r = subprocess.run(["git", "log", "-p", f"--since={days}.days",
                            "--format=%x1e%H", "--diff-filter=AM", "--", "things",
                            "*.md"], cwd=root, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
    except Exception:
        return {"days": days, "created": None, "disposed": None,
                "surface_changes": None, "walks": None}
    if r.returncode != 0:
        return {"days": days, "created": None, "disposed": None,
                "surface_changes": None, "walks": None}
    type_by_path = {}
    for t in corpus.things:
        rel = _rel(root, t)
        if rel:
            type_by_path[rel] = str(t.meta.get("type"))
    created: dict[str, int] = defaultdict(int)
    disposed = 0
    surfaces: set[str] = set()
    walks: set[str] = set()
    for rec in r.stdout.split("\x1e")[1:]:
        cur = None
        is_new = False
        counted = False
        plus_type = None
        for line in rec.splitlines():
            fm = _FILE_RE.match(line)
            if fm:
                cur = fm.group(2)
                is_new = False
                counted = False
                plus_type = None
                continue
            if cur is None:
                continue
            if line.startswith("new file mode"):
                is_new = True
                continue
            mt = _PLUS_TYPE.match(line)
            if mt and plus_type is None:
                plus_type = mt.group(1)
            typ = type_by_path.get(cur) or plus_type
            ms = _PLUS_STATUS.match(line)
            # A status moving into a terminal state on an existing file is a
            # disposal; a file born already disposed (a cue answered in the
            # commit that raised it) is intake, not disposal.
            if ms and not is_new and ms.group(1) in _DISPOSED and typ in (_ATTENTION | {"plan"}):
                disposed += 1
            if is_new and not counted and typ in _ATTENTION and plus_type:
                created[typ] += 1
                counted = True
                if typ == "cue":
                    walks.add(cur)
            # A definition surface modified (not born): the gate's scope,
            # insights included, so walks can be read against it. A change
            # that only records a disposition owes no walk, so it is not
            # counted against the walks either.
            if (not is_new and typ in _DEFINITION_SURFACES
                    and line[:1] in ("+", "-")
                    and not line.startswith(("+++", "--- "))
                    and line[1:].strip()
                    and not _DISPOSITION_LINE.match(line[1:])):
                surfaces.add(cur)
    return {"days": days, "created": dict(created), "disposed": disposed,
            "surface_changes": len(surfaces), "walks": len(walks)}


def bands_line(rep: dict) -> str:
    """The digest's line: the bands now, read from session start's own history
    walk — no git of its own. The week's intake and disposal are
    `mdllm reckon --rates`, which reads the diffs."""
    bands = rep["bands"]
    return (f"- **Reckoning:** {len(bands['mechanical'])} mechanical / "
            f"{len(bands['settled'])} settled / {len(bands['residue'])} residue "
            "(fired triggers have their own line) — a session end owes the close "
            "(`mdllm reckon . --close`); `--rates` for the week's intake and disposal")


def rate_line(rep: dict, rt: dict) -> str:
    """One digest line: intake, disposal, walks, bands."""
    if rt.get("created") is None:
        return "- **Reckoning:** rate unknown (git history unreadable); `mdllm reckon` for the bands"
    created = rt["created"]
    intake = sum(created.values())
    parts = ", ".join(f"{n} {k}{'s' if n != 1 else ''}" for k, n in sorted(created.items()))
    bands = rep["bands"]
    return (f"- **Reckoning (last {rt['days']}d):** intake {intake}"
            + (f" ({parts})" if parts else "")
            + f" · disposed {rt['disposed']} · walks {rt['walks']} of "
            f"{rt['surface_changes']} definition-surface change(s) · now "
            f"{len(bands['mechanical'])} mechanical / {len(bands['settled'])} settled / "
            f"{len(bands['residue'])} residue — `mdllm reckon`")


# ------------------------------------------------------------------ the close
# What a session end owes the reckoning (the-reckoning Phase 3). The mechanical
# band applied, and the backlog chased: CLOSE_QUOTA decisions a day while one
# stands, else the band emptied. One queue, never a wall: the oldest residue
# first and at most CLOSE_RESIDUE of it, so the operator meets one native
# prompt per close; then the time-bound kinds — a workflow the work keeps
# travelling, an open cue, a fired trigger — then the longest-waiting of the
# rest. (The first live read found 49 fired triggers in one workspace: a
# kind held to "all, every close" would have been the wall.) A decision is any disposition moved today — committed since
# midnight or in the delta in hand — so the count is the same whether the
# agent commits its decisions as `reckon:` first or with the `session-end:`
# commit. The commit gate reads this for a `session-end:` commit
# (SESSION_END_ENV, set by the lifecycle runner); an unattended run is held to
# the mechanical band only and drafts the rest, deciding nothing.

SESSION_END_ENV = "MDLLM_GATE_SESSION_END"
CLOSE_QUOTA = 10
CLOSE_RESIDUE = 4
CLOSE_SHOWN_AT_GATE = 3
_FIRST = {"workflow": 0, "cue": 1, "trigger": 2}  # the time-bound kinds lead the queue


def decided_today(root: Path, corpus, today: dt.date) -> set[str] | None:
    """Ids of the attention items whose disposition moved today: the diffs of
    today's commits over things/, and the delta in hand against HEAD. A thing
    born today is intake, not a decision. None when git cannot be read."""
    outs: list[str] = []
    for cmd in (["git", "log", "-p", "-U0", "--format=%x1e%H",
                 f"--since={today.isoformat()}T00:00:00", "--", "things"],
                ["git", "diff", "HEAD", "-U0", "--", "things"]):
        try:
            r = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=60)
        except Exception:
            return None
        if r.returncode != 0:
            if cmd[1] == "diff":
                continue  # no HEAD yet: nothing in hand to compare
            return None
        outs.append(r.stdout or "")
    by_rel = {_rel(root, t): t for t in corpus.things if t.id}
    decided: set[str] = set()
    for out in outs:
        cur = None
        is_new = False
        for line in out.splitlines():
            fm = _FILE_RE.match(line)
            if fm:
                cur, is_new = fm.group(2), False
                continue
            if cur is None:
                continue
            if line.startswith("new file mode"):
                is_new = True
                continue
            if is_new or not line.startswith("+") or line.startswith("+++"):
                continue
            mm = _DECISION_LINE.match(line[1:])
            t = by_rel.get(cur) if mm else None
            if t is None:
                continue
            typ = str(t.meta.get("type"))
            if mm.group(1) == "condition" or typ in _ATTENTION or typ not in _NOT_WORK:
                decided.add(t.id)
    return decided


def _dispatcher_drafts(corpus) -> tuple[str, str] | None:
    """The newest dispatch digest that drafted reckoning decisions: (id,
    created). The attended close adopts what still holds, by citation."""
    best = None
    for t in corpus.things:
        if str(t.meta.get("type")) != "dispatch-digest" or not t.id:
            continue
        try:
            body = t.path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "## Reckoning" not in body:
            continue
        created = str(t.meta.get("created") or "")
        if best is None or created > best[1]:
            best = (t.id, created)
    return best


def close_report(root: Path, corpus, rep: dict, *, today: dt.date | None = None,
                 unattended: bool = False) -> dict:
    """What this close owes, and whether it is met."""
    today = today or rep["today"]
    bands = rep["bands"]
    mechanical = list(bands["mechanical"])
    residue = sorted(bands["residue"], key=lambda i: (-i.waited, i.kind, i.thing_id))
    settled = sorted(bands["settled"], key=lambda i: (
        _FIRST.get(i.kind, len(_FIRST)), -i.waited, i.kind, i.thing_id))
    decided = decided_today(root, corpus, today)
    backlog = len(residue) + len(settled)
    if decided is None:
        quota_met = True  # a close that cannot count opens, and says so
    else:
        quota_met = backlog == 0 or len(decided) >= CLOSE_QUOTA
    need = 0 if quota_met else CLOSE_QUOTA - len(decided or ())
    owed_residue = residue[:min(CLOSE_RESIDUE, need)]
    owed_settled = settled[:max(0, need - len(owed_residue))]
    met = not mechanical and (unattended or quota_met)
    return {"today": today, "mechanical": mechanical,
            "owed_residue": owed_residue, "owed_settled": owed_settled,
            "decided": decided, "backlog": backlog,
            "waiting": backlog - len(owed_residue) - len(owed_settled),
            "quota_met": quota_met, "met": met, "unattended": unattended,
            "drafts": _dispatcher_drafts(corpus)}


def _close_item(it: Item) -> str:
    return f"    - {it.kind} `{it.thing_id}` → {it.proposal} — {it.evidence}"


def close_text(cr: dict, *, gate: bool = False) -> list[str]:
    """The close, as the agent reads it — whole from `reckon --close`, as a
    count with the command to run when the commit gate refuses."""
    if cr["met"]:
        dec = cr["decided"]
        return ["## The close — met",
                f"- the mechanical band is applied"
                + ("" if cr["unattended"] else
                   f"; {len(dec or ())} decision(s) today, "
                   f"{cr['backlog']} waiting for later closes")]
    lines = ["## The close — what this session end owes the reckoning"]
    if gate:
        parts = []
        if cr["mechanical"]:
            parts.append(f"{len(cr['mechanical'])} mechanical item(s) pending")
        if not cr["quota_met"] and not cr["unattended"]:
            parts.append(f"{len(cr['decided'] or ())} of {CLOSE_QUOTA} decisions today "
                         f"with {cr['backlog']} waiting")
        lines.append("- " + "; ".join(parts) + ".")
        shown = (cr["mechanical"] + cr["owed_residue"]
                 + cr["owed_settled"])[:CLOSE_SHOWN_AT_GATE]
        lines += [_close_item(i) for i in shown]
        lines.append("- Run `mdllm reckon . --close --apply` for the whole list, decide "
                     "it, and commit again.")
        return lines
    if cr["mechanical"]:
        lines.append(f"- **Mechanical ({len(cr['mechanical'])}):** pending — "
                     "`mdllm reckon . --close --apply` writes them; stage the receipts.")
        lines += [_close_item(i) for i in cr["mechanical"]]
    if cr["unattended"]:
        lines.append("- **Unattended:** apply the mechanical band and commit it as "
                     "`reckon:`; decide nothing else. Under `## Reckoning` in your "
                     "digest, draft a decision for each item below with the record "
                     "you would cite, and file the residue as seat items. The next "
                     "attended close adopts what still holds.")
    if cr["owed_residue"]:
        lines.append(f"- **The residue ({len(cr['owed_residue'])}, oldest first):** "
                     "the operator's — put them in one native choice prompt, one "
                     "question each, the concrete rulings as options and *not now* "
                     "among them; *not now* is an answer: record it as a hold "
                     "(`--keep`) with their words as the reason.")
        lines += [_close_item(i) for i in cr["owed_residue"]]
    if cr["owed_settled"]:
        lines.append(f"- **Settled ({len(cr['owed_settled'])}, time-bound kinds "
                     "first, then the longest-waiting):** "
                     "decide each by citing the record — dispose (set the status "
                     "and its resolution), or hold: `mdllm reckon . --keep <id> "
                     "--reason \"…\"` (next look one interval out; `--until "
                     "YYYY-MM-DD` to say when). A fired trigger: act, re-date its "
                     "condition, or disarm it; a cue: walk it or answer by "
                     "citation; a workflow: write or bind it (`mdllm workflows`).")
        lines += [_close_item(i) for i in cr["owed_settled"]]
    if cr["decided"] is None:
        lines.append("- (note) git could not be read: today's decisions are uncounted "
                     "and the quota is not enforced")
    else:
        lines.append(f"- **Today:** {len(cr['decided'])} decision(s) recorded; a close "
                     f"owes {CLOSE_QUOTA} a day while a backlog stands, or the band "
                     f"emptied. {cr['waiting']} more wait for later closes — "
                     "`--rates` says whether the chase is winning.")
    if cr["drafts"]:
        lines.append(f"- The dispatcher drafted decisions in `{cr['drafts'][0]}` "
                     f"({cr['drafts'][1]}) — adopt by citation what still holds.")
    return lines


def cmd_reckon(args) -> int:
    """Reads, and with --apply writes the mechanical band; with --keep writes
    one hold; with --close says what a session end owes. Exit 0 except a
    hold that cannot be written (2)."""
    root = Path(args.path).resolve()
    try:
        corpus, _ = scan(root)
    except Exception as exc:
        print(f"mdllm: reckon cannot scan {root}: {exc}")
        return 2
    keep_id = getattr(args, "keep", None)
    if keep_id:
        until = None
        raw = getattr(args, "until", None)
        if raw:
            try:
                until = dt.date.fromisoformat(str(raw))
            except ValueError:
                print("mdllm: --until must be a date, YYYY-MM-DD")
                return 2
        try:
            print(keep(root, corpus, keep_id, getattr(args, "reason", None) or "", until))
        except ValueError as exc:
            print(f"mdllm: reckon --keep: {exc}")
            return 2
        return 0
    rates_only = bool(getattr(args, "rates", False))
    imports = bool(getattr(args, "imports", False))
    rep = reckon_report(root, corpus, imports=imports, workflows=not rates_only)
    if rates_only:
        print(rate_line(rep, rates(root, corpus)))
        return 0
    closing = bool(getattr(args, "close", False))
    if not closing:
        for ln in render(rep, root):
            print(ln)
    if getattr(args, "apply", False):
        receipts = apply_mechanical(root, corpus, rep)
        print(f"- **Applied ({sum(1 for r in receipts if r.startswith('applied'))}):** "
              "the mechanical band, in place — commit it as `reckon:` with the "
              "settled band's decisions:")
        for r in receipts:
            print(f"    - {r}")
        if not receipts:
            print("    - nothing to apply")
        if closing and any(r.startswith("applied") for r in receipts):
            corpus, _ = scan(root)
            rep = reckon_report(root, corpus, imports=imports, workflows=True)
    if closing:
        unattended = bool(os.environ.get("MDLLM_UNATTENDED"))
        for ln in close_text(close_report(root, corpus, rep, unattended=unattended)):
            print(ln)
    return 0
