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
"""

from __future__ import annotations

import datetime as dt
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


def reckon_report(root: Path, corpus, *, today: dt.date | None = None,
                  imports: bool = False, workflows: bool = False) -> dict:
    """Every attention item's disposition candidate, banded, with evidence."""
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
            if due:
                items.append(Item("insight", t.id, "settled",
                                  "read the stated condition: met → dispose; not → re-date",
                                  f"keep-active {age}d; reason: "
                                  f"{reason or '(none stated — give one or dispose)'}"))
            continue
        if cited == 0:
            if due:
                items.append(Item("insight", t.id, "settled", "dismiss or consolidate",
                                  f"active {age}d, nothing live cites it"))
            continue
        if age >= 2 * INTERVALS["insight"] and _settles_when(m) is None:
            items.append(Item("insight", t.id, "settled",
                              "promote into the operating layer, or state why it stays",
                              f"active {age}d, cited by {cited} live thing(s) and never promoted"))

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
            if due:
                items.append(Item("conflict", t.id, "settled",
                                  "read what would resolve it: happened → rule; not → re-date",
                                  f"held {age}d; reason: {reason}"))
            continue
        stale = idle is not None and idle >= INTERVALS["conflict"]
        if not (stale or due):
            continue
        cited = live_inbound.get(t.id, 0)
        where = f"open {age}d, untouched {idle if idle is not None else '?'}d"
        if cited:
            items.append(Item("conflict", t.id, "residue", "rule: choose a side, or hold with a reason",
                              f"{where}, in circulation ({cited} live thing(s) link it)"))
        else:
            items.append(Item("conflict", t.id, "settled", "rule, link from live work, or hold",
                              f"{where}, nothing live links it"))

    # ---- cues -------------------------------------------------------------
    for t in corpus.things:
        m = t.meta
        if t.id and str(m.get("type")) == "cue" and str(m.get("status")) == "open":
            created = _date(m.get("created"))
            age = (today - created).days if created else 0
            items.append(Item("cue", t.id, "settled", "answer by citation, or walk",
                              f"open {age}d on `{m.get('subject')}`"))

    # ---- fired triggers ---------------------------------------------------
    try:
        from .triggers import TriggerOutcome, evaluate_results
        results = evaluate_results(root)
    except Exception as exc:  # the trigger engine says what it cannot read
        results = ()
        notes.append(f"triggers could not be evaluated: {type(exc).__name__}")
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
        if (thing is not None and cond_day is not None and idle is not None
                and (today - idle * dt.timedelta(days=1)) > cond_day):
            items.append(Item("trigger", label, "settled", "re-date or disarm",
                              f"fired ({r.trigger_type}); the thing moved "
                              f"{(today - cond_day).days - idle}d after the condition "
                              "— was it acted on?"))
        else:
            items.append(Item("trigger", label, "settled", "act, re-date or disarm",
                              f"fired ({r.trigger_type}): {r.reason}"))

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
        if sw is not None and due:
            items.append(Item("work", t.id, "residue", "cancel, pause or continue",
                              f"past its `settles_when` ({sw}); status {m.get('status')}"))
            continue
        if idle is None or idle < INTERVALS["work"]:
            continue
        parent = m.get("parent")
        parent_thing = by_id.get(str(parent)) if parent else None
        if parent_thing is not None and str(parent_thing.meta.get("status")) == "cancelled":
            items.append(Item("work", t.id, "residue", "cancel or re-parent",
                              f"untouched {idle}d; its parent `{parent}` is cancelled"))
            continue
        ticked = sum(1 for b in boxes if b.lower() == "x")
        status = str(m.get("status"))
        if status == "not-started":
            proposal = "start, or say when"
        elif status in {"paused", "blocked"}:
            proposal = "unblock, or say what it waits on"
        else:
            proposal = "pause, or say what it waits on"
        items.append(Item("work", t.id, "settled", proposal,
                          f"{status} and untouched {idle}d"
                          + (f"; {ticked}/{len(boxes)} boxes ticked" if boxes else "")))

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
                lines[i] = f"{key}: {value}"
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
            # insights included, so walks can be read against it.
            if not is_new and typ in _DEFINITION_SURFACES:
                surfaces.add(cur)
    return {"days": days, "created": dict(created), "disposed": disposed,
            "surface_changes": len(surfaces), "walks": len(walks)}


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


def cmd_reckon(args) -> int:
    """Reads, and with --apply writes the mechanical band; exit 0 always."""
    root = Path(args.path).resolve()
    try:
        corpus, _ = scan(root)
    except Exception as exc:
        print(f"mdllm: reckon cannot scan {root}: {exc}")
        return 2
    rates_only = bool(getattr(args, "rates", False))
    rep = reckon_report(root, corpus, imports=bool(getattr(args, "imports", False)),
                        workflows=not rates_only)
    if rates_only:
        print(rate_line(rep, rates(root, corpus)))
        return 0
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
    return 0
