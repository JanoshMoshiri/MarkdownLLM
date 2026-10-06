"""`mdllm workflows` — workflows emerge from use; the work is the run
(workflows-emerge-from-use-2026-10-07; `workflow-state.md` → Carrier Binding,
Workflows Emerge From Use).

Three reads over one walk of the commit stream:

- **Bindings.** A `workflow-definition` may declare `carrier: {type, map}`:
  every thing of that type is a run of it, its stage read from its `status`
  through the map (identity where the map is silent). For each definition the
  report lists its runs by stage — carrier-derived or explicit — and its
  *departures*: status moves on carrier things, since the definition last
  changed, whose stages the definition's edges do not connect. A departure is
  reported, never refused.
- **Emergence** (`--emergent`). Per domain type, the status transitions things
  actually made. A candidate is a type whose observed graph has at least
  three stages, enough transitions across enough days and things, and no
  live binding; moves a thing made all on one day are bookkeeping and do not
  count; reserved types and generic lifecycles are not workflows. Evidence
  attached. Where nothing repeats, the answer is none.
- **Draft** (`--emergent --draft`). Writes each candidate as a
  `workflow-definition` marked `origin: inferred`, bound to its carrier, its
  edges from what was observed, its terminal stages from the type's terminal
  statuses, and per stage the acts the commit stream shows on the way in —
  the skeleton the agent completes. Never overwrites.

The floor detects, assembles and writes the skeleton; the agent writes the
steps and marks the gates; the operator rules only on departures from what
they authored. Read-only except `--draft`; exit 0 always.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .model import (RESERVED_STATUSES, SEV_ERROR, SEV_WARNING, Finding,
                    origin_is_external, scan, terminal_statuses_for)

# --------------------------------------------------------------- thresholds
# What "keeps being done" means, as numbers a reader can move. A candidate
# needs a graph of MIN_STAGES stages, MIN_TRANSITIONS counted moves spread
# over MIN_DAYS distinct days and MIN_THINGS things. Moved by evidence, not
# by taste (the first live read is in the plan).
MIN_STAGES = 3
MIN_TRANSITIONS = 8
MIN_DAYS = 3
MIN_THINGS = 2
MIN_EDGE = 2          # an observed move must recur to become a declared edge

# Statuses that describe a thing's own lifecycle rather than steps of work.
# A type whose observed statuses all sit here is a lifecycle, not a workflow.
GENERIC_STATUSES = {
    "not-started", "in-progress", "completed", "cancelled", "blocked", "paused",
    "active", "inactive", "open", "closed", "resolved", "done", "draft",
    "current", "superseded", "deprecated", "archived", "evolving", "stable",
    "made", "answered", "promoted", "dismissed", "abandoned", "dormant", "live",
}

_FILE_RE = re.compile(r"^diff --git a/(.*?) b/(.*?)$")
_RENAME_FROM = re.compile(r"^rename from (.*)$")
_RENAME_TO = re.compile(r"^rename to (.*)$")
_MINUS_STATUS = re.compile(r"^-status:\s*(\S+)")
_PLUS_STATUS = re.compile(r"^\+status:\s*(\S+)")
_PLUS_TYPE = re.compile(r"^\+type:\s*(\S+)")
_PLUS_ID = re.compile(r"^\+id:\s*(\S+)")
_PREFIX = re.compile(r"^([a-z][a-z0-9-]{1,24}):")


# ----------------------------------------------------------------- history

@dataclass
class Move:
    path: str
    thing_id: str | None
    thing_type: str | None
    old: str
    new: str
    day: dt.date
    act: str | None      # the commit subject's prefix — the enacted act


@dataclass
class History:
    moves: list[Move] = field(default_factory=list)
    readable: bool = True


def read_history(root: Path) -> History:
    """Every status move a thing made under things/, oldest first, from one
    `git log -p` walk. A file's birth is not a move. Renames carry identity."""
    try:
        r = subprocess.run(
            ["git", "log", "-p", "-M", "--reverse", "--format=%x1e%cs%x00%s",
             "--", "things"], cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=300)
    except Exception:
        return History(readable=False)
    if r.returncode != 0:
        return History(readable=False)
    type_of: dict[str, str] = {}
    id_of: dict[str, str] = {}
    status_of: dict[str, str] = {}
    moves: list[Move] = []
    for rec in r.stdout.split("\x1e")[1:]:
        header, _, body = rec.partition("\n")
        day_s, _, subject = header.partition("\x00")
        try:
            day = dt.date.fromisoformat(day_s.strip())
        except ValueError:
            continue
        pm = _PREFIX.match(subject.strip().lower())
        act = pm.group(1) if pm else None
        cur: str | None = None
        rename_from: str | None = None
        old_s = new_s = new_t = new_i = None

        def flush():
            if cur is None or "/_index/" in f"/{cur}" or cur.endswith("_schema.yaml"):
                return
            if new_t and cur not in type_of:
                type_of[cur] = new_t
            if new_i and cur not in id_of:
                id_of[cur] = new_i
            if new_s is None:
                return
            before = old_s if old_s is not None else status_of.get(cur)
            if before is not None and before != new_s:
                moves.append(Move(cur, id_of.get(cur), type_of.get(cur),
                                  before, new_s, day, act))
            status_of[cur] = new_s

        for line in body.splitlines():
            fm = _FILE_RE.match(line)
            if fm:
                flush()
                cur = fm.group(2)
                old_s = new_s = new_t = new_i = None
                rename_from = None
                continue
            if cur is None:
                continue
            m = _RENAME_FROM.match(line)
            if m:
                rename_from = m.group(1)
                continue
            m = _RENAME_TO.match(line)
            if m and rename_from:
                for table in (type_of, id_of, status_of):
                    if rename_from in table:
                        table[m.group(1)] = table.pop(rename_from)
                continue
            if line.startswith("---") or line.startswith("+++"):
                continue
            m = _MINUS_STATUS.match(line)
            if m:
                old_s = m.group(1)
                continue
            m = _PLUS_STATUS.match(line)
            if m:
                new_s = m.group(1)
                continue
            m = _PLUS_TYPE.match(line)
            if m and new_t is None:
                new_t = m.group(1)
                continue
            m = _PLUS_ID.match(line)
            if m and new_i is None:
                new_i = m.group(1)
        flush()
    # Types and ids learnt late (a file whose frontmatter was added after
    # birth) are back-filled onto its earlier moves.
    for mv in moves:
        if mv.thing_type is None:
            mv.thing_type = type_of.get(mv.path)
        if mv.thing_id is None:
            mv.thing_id = id_of.get(mv.path)
    return History(moves=moves)


# ---------------------------------------------------------------- binding

def carrier_types(meta: dict) -> tuple[str, ...]:
    """Every type a definition binds — `carrier.type` is a name or a list of
    names: one loop may run through several types (a specification loop over
    requirement, design and test documents)."""
    c = meta.get("carrier")
    raw = c if isinstance(c, (str, list)) else (c.get("type") if isinstance(c, dict) else None)
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        return ()
    return tuple(str(x).strip() for x in raw if isinstance(x, str) and x.strip())


def carrier_of(meta: dict) -> tuple[str | None, dict]:
    """(first carrier type, status→stage map) for a definition, or (None, {}).
    Callers that need every bound type use `carrier_types`."""
    types = carrier_types(meta)
    if not types:
        return None, {}
    c = meta.get("carrier")
    m = c.get("map") if isinstance(c, dict) else None
    return types[0], ({str(k): str(v) for k, v in m.items()}
                      if isinstance(m, dict) else {})


def _stages(meta: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for s in meta.get("stages") or []:
        if isinstance(s, dict) and isinstance(s.get("id"), str):
            to = s.get("to") or []
            out[s["id"]] = [str(x) for x in to] if isinstance(to, list) else []
    return out


def stage_of(def_meta: dict, status) -> str | None:
    """The stage a carrier thing at `status` is at, or None (outside it)."""
    _, mp = carrier_of(def_meta)
    st = mp.get(str(status), str(status))
    return st if st in _stages(def_meta) else None


def _live(meta: dict) -> bool:
    return str(meta.get("status")) != "deprecated"


def carrier_findings(corpus) -> list[Finding]:
    """The floor's half of Carrier Binding: shape, map members, one live
    binding per type, explicit runs of a bound definition."""
    findings: list[Finding] = []
    bound: dict[str, str] = {}
    by_id = {t.id: t for t in corpus.things if t.id}
    for t in corpus.things:
        if str(t.meta.get("type")) != "workflow-definition":
            continue
        raw = t.meta.get("carrier")
        if raw is None:
            continue
        name = t.id or t.path.name
        ctype, mp = carrier_of(t.meta)
        if ctype is None:
            findings.append(Finding(SEV_ERROR, name,
                "`carrier` must name the thing type the work travels through — "
                "`carrier: {type: <type>, map: {<status>: <stage>}}`, or a bare type name"))
            continue
        if isinstance(raw, dict) and raw.get("map") is not None and not isinstance(raw.get("map"), dict):
            findings.append(Finding(SEV_ERROR, name,
                "`carrier.map` must map carrier statuses to stage ids"))
        stages = _stages(t.meta)
        for status, stage in mp.items():
            if stage not in stages:
                findings.append(Finding(SEV_ERROR, name,
                    f"`carrier.map` sends `{status}` to `{stage}`, which is not a "
                    f"stage (stages: {sorted(stages)})"))
        for one in carrier_types(t.meta):
            if one in {"workflow-run", "workflow-definition", "cue", "index"}:
                findings.append(Finding(SEV_ERROR, name,
                    f"`carrier.type` `{one}` is framework machinery, not work"))
            if not _live(t.meta):
                continue
            if one in bound:
                findings.append(Finding(SEV_ERROR, name,
                    f"`{one}` is already the carrier of `{bound[one]}` — one type, "
                    "one binding: a thing cannot be a run of two processes at once "
                    "(an inferred workflow never replaces an authored one)"))
            else:
                bound[one] = name
    for t in corpus.things:
        if str(t.meta.get("type")) != "workflow-run":
            continue
        d = by_id.get(str(t.meta.get("definition")))
        if d is not None and carrier_types(d.meta):
            findings.append(Finding(SEV_WARNING, t.id or t.path.name,
                f"explicit run of `{d.id}`, which is carrier-bound to "
                f"{', '.join(f'`{x}`' for x in carrier_types(d.meta))} — the carrier "
                "things are its runs; this one counts the work twice"))
    return findings


def _last_changed(root: Path, t) -> dt.date | None:
    try:
        rel = t.path.resolve().relative_to(root.resolve()).as_posix()
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel],
                             cwd=root, capture_output=True, text=True,
                             timeout=30).stdout.strip()
        return dt.date.fromisoformat(out) if out else None
    except Exception:
        return None


def bindings_report(root: Path, corpus, history: History) -> list[dict]:
    """Per definition: its carrier, runs by stage, departures since it last
    changed."""
    explicit = Counter(str(t.meta.get("definition")) for t in corpus.things
                       if str(t.meta.get("type")) == "workflow-run")
    out: list[dict] = []
    for d in corpus.things:
        if str(d.meta.get("type")) != "workflow-definition" or not d.id:
            continue
        ctypes = set(carrier_types(d.meta))
        ctype = ", ".join(sorted(ctypes)) if ctypes else None
        origin = ("mirror" if origin_is_external(d.meta)
                  else str(d.meta.get("origin") or "stated"))
        row = {"id": d.id, "status": str(d.meta.get("status")),
               "origin": origin,
               "carrier": ctype, "explicit_runs": explicit.get(d.id, 0),
               "by_stage": {}, "outside": 0, "departures": []}
        if ctype:
            stages = _stages(d.meta)
            for t in corpus.things:
                if str(t.meta.get("type")) not in ctypes or origin_is_external(t.meta):
                    continue
                st = stage_of(d.meta, t.meta.get("status"))
                if st is None:
                    row["outside"] += 1
                else:
                    row["by_stage"][st] = row["by_stage"].get(st, 0) + 1
            since = _last_changed(root, d)
            for mv in history.moves:
                if mv.thing_type not in ctypes or (since and mv.day < since):
                    continue
                a, b = stage_of(d.meta, mv.old), stage_of(d.meta, mv.new)
                if a and b and a != b and b not in stages.get(a, []):
                    row["departures"].append(mv)
        out.append(row)
    return out


# --------------------------------------------------------------- emergence

@dataclass
class Candidate:
    carrier: str
    stages: list[str]
    edges: dict[tuple[str, str], int]
    moves: int
    things: int
    days: int
    first: dt.date
    last: dt.date
    paths: list[tuple[str, int]]
    terminal: list[str]
    acts: dict[str, Counter]
    overlaps: list[str]
    same_shape_as: list[str] = field(default_factory=list)


_RESERVED_TYPES = set(RESERVED_STATUSES)
_PATH_SHOWN = 10


def _short_path(chain: list[str]) -> str:
    """A chain as text; a long loop is shown by its head and its count."""
    if len(chain) <= _PATH_SHOWN:
        return " > ".join(chain)
    return " > ".join(chain[:_PATH_SHOWN]) + f" > … ({len(chain)} stage visits)"


def emergent_candidates(root: Path, corpus, history: History) -> list[Candidate]:
    bound = {x for t in corpus.things
             if str(t.meta.get("type")) == "workflow-definition" and _live(t.meta)
             for x in carrier_types(t.meta)}
    by_type: dict[str, list[Move]] = defaultdict(list)
    for mv in history.moves:
        if mv.thing_type and mv.thing_type not in _RESERVED_TYPES:
            by_type[mv.thing_type].append(mv)
    # Bookkeeping: a thing whose every move happened on one day.
    days_per_path: dict[str, set] = defaultdict(set)
    for mv in history.moves:
        days_per_path[mv.path].add(mv.day)
    unbound_defs = [t for t in corpus.things
                    if str(t.meta.get("type")) == "workflow-definition"
                    and _live(t.meta) and not carrier_types(t.meta)]
    out: list[Candidate] = []
    for typ, mvs in by_type.items():
        if typ in bound:
            continue
        real = [m for m in mvs if len(days_per_path[m.path]) > 1]
        statuses = {m.old for m in real} | {m.new for m in real}
        if not statuses or statuses <= GENERIC_STATUSES:
            continue
        edges = Counter((m.old, m.new) for m in real)
        kept = {e: n for e, n in edges.items() if n >= MIN_EDGE}
        stages = sorted({a for a, _ in kept} | {b for _, b in kept})
        if len(stages) < MIN_STAGES:
            continue
        counted = [m for m in real if (m.old, m.new) in kept]
        things = {m.path for m in counted}
        days = {m.day for m in counted}
        if len(counted) < MIN_TRANSITIONS or len(days) < MIN_DAYS or len(things) < MIN_THINGS:
            continue
        chains: dict[str, list[str]] = defaultdict(list)
        for m in sorted(counted, key=lambda m: m.day):
            ch = chains[m.path]
            if not ch:
                ch.append(m.old)
            if ch[-1] != m.new:
                ch.append(m.new)
        paths = Counter(_short_path(c) for c in chains.values() if len(c) >= 2)
        # Stages in the order the work meets them: the mean position of each
        # stage's first appearance across the chains.
        first_pos: dict[str, list[int]] = defaultdict(list)
        for ch in chains.values():
            seen: set[str] = set()
            for i, s in enumerate(ch):
                if s not in seen:
                    seen.add(s)
                    first_pos[s].append(i)
        stages = sorted(stages, key=lambda s: (sum(first_pos[s]) / len(first_pos[s])
                                               if first_pos.get(s) else 99, s))
        try:
            term = terminal_statuses_for(corpus.schema, typ)
        except Exception:
            term = set()
        outgoing = {a for a, _ in kept}
        terminal = sorted(s for s in stages if s in term or s not in outgoing)
        acts: dict[str, Counter] = defaultdict(Counter)
        for m in counted:
            if m.act:
                acts[m.new][m.act] += 1
        overlaps = []
        for d in unbound_defs:
            ids = set(_stages(d.meta))
            if ids and len(ids & set(stages)) / len(ids | set(stages)) >= 0.5:
                overlaps.append(d.id)
        out.append(Candidate(typ, stages, kept, len(counted), len(things),
                             len(days), min(days), max(days),
                             paths.most_common(3), terminal, dict(acts), overlaps))
    shapes: dict[tuple, list[str]] = defaultdict(list)
    for c in out:
        shapes[tuple(c.stages)].append(c.carrier)
    for c in out:
        c.same_shape_as = [x for x in shapes[tuple(c.stages)] if x != c.carrier]
    return sorted(out, key=lambda c: -c.moves)


def draft_text(c: Candidate, today: dt.date) -> tuple[str, str]:
    """(id, file text) for a candidate's inferred workflow-definition."""
    wid = f"{c.carrier}-workflow"
    stage_lines = []
    for s in c.stages:
        to = sorted({b for (a, b) in c.edges if a == s})
        stage_lines.append(f"  - id: {s}\n    to: [{', '.join(to)}]")
    confidence = "high" if c.things >= 5 and c.moves >= 20 else "medium"
    edge_rows = "\n".join(f"| `{a}` → `{b}` | {n} |" for (a, b), n
                          in sorted(c.edges.items(), key=lambda kv: -kv[1]))
    path_rows = "\n".join(f"- `{p}` — {n} thing(s)" for p, n in c.paths)
    stage_body = []
    for s in c.stages:
        acts = ", ".join(f"`{a}:` ×{n}" for a, n in c.acts.get(s, Counter()).most_common(4))
        stage_body.append(
            f"### `{s}`\n"
            f"- **Seen on the way in:** {acts or 'no recurring commit act'}\n"
            f"- **Do:** _(the agent writes this from the record)_\n"
            f"- **Produce:** _(the agent writes this from the record)_\n"
            f"- **Check before moving on:** _(the agent writes this from the record)_\n")
    text = f"""---
id: {wid}
type: workflow-definition
status: evolving
version: 1.0
created: {today.isoformat()}
origin: inferred
confidence: {confidence}
tags: [workflow, inferred, emerged]
carrier:
  type: {c.carrier}
stages:
{chr(10).join(stage_lines)}
---

# Workflow: `{c.carrier}` (emerged from use)

Written by the floor from the record (`mdllm workflows --emergent --draft`,
`workflow-state.md` → Workflows Emerge From Use): {c.moves} status moves by
{c.things} things across {c.days} days, {c.first} to {c.last}. Every
`{c.carrier}` is a run of this workflow; its stage is its status. The agent
completes each stage's steps from the record and marks any stage at which a
person approves or rules as theirs; it never removes such a stage.

## Evidence

| Observed move | Count |
|---|---|
{edge_rows}

Most travelled paths:
{path_rows}

## Stages

{chr(10).join(stage_body)}"""
    return wid, text


# --------------------------------------------------------------------- cli

def cmd_workflows(args) -> int:
    root = Path(args.path).resolve()
    try:
        corpus, _ = scan(root)
    except Exception as exc:
        print(f"mdllm: workflows cannot scan {root}: {exc}")
        return 2
    history = read_history(root)
    print(f"## Workflows — {root}")
    if not history.readable:
        print("- (git history unreadable here — departures and emergence cannot be read)")
    rows = bindings_report(root, corpus, history)
    if rows:
        print(f"- **Defined ({len(rows)}):**")
        for r in rows:
            kind = {"inferred": "inferred", "mirror": "mirror — its source's to run"}.get(
                r["origin"], "authored")
            label = f"`{r['id']}` ({r['status']}, {kind})"
            if r["carrier"]:
                spread = ", ".join(f"{s} {n}" for s, n in r["by_stage"].items()) or "none at a stage"
                line = (f"    - {label} — carrier `{r['carrier']}`: runs by stage: {spread}"
                        + (f"; {r['outside']} outside it" if r["outside"] else ""))
                if r["departures"]:
                    line += f"; **{len(r['departures'])} departure(s)**"
                print(line)
                for mv in r["departures"][:5]:
                    print(f"        - `{mv.thing_id or mv.path}`: `{mv.old}` → `{mv.new}` on {mv.day}"
                          f" — {'revise the workflow, or name the slip' if r['origin'] == 'inferred' else 'the operator rules: it is their workflow'}")
            else:
                print(f"    - {label} — no carrier; {r['explicit_runs']} explicit run(s)")
    else:
        print("- **Defined:** none")
    if getattr(args, "emergent", False):
        cands = emergent_candidates(root, corpus, history)
        if not cands:
            print("- **Emergent:** none — no unbound type keeps travelling a path of "
                  f"{MIN_STAGES}+ stages across {MIN_DAYS}+ days; that is the honest "
                  "answer where nothing repeats")
        else:
            print(f"- **Emergent ({len(cands)}):** paths the record supports as a workflow:")
            for c in cands:
                print(f"    - `{c.carrier}` — stages {' · '.join(c.stages)}; {c.moves} moves, "
                      f"{c.things} things, {c.days} days ({c.first} → {c.last})"
                      + (f"; same shape as {', '.join(f'`{x}`' for x in c.same_shape_as)}" if c.same_shape_as else "")
                      + (f"; an unbound definition overlaps: {', '.join(f'`{x}`' for x in c.overlaps)} — bind it rather than write another" if c.overlaps else ""))
                for p, n in c.paths[:2]:
                    print(f"        - path `{p}` ×{n}")
            if getattr(args, "draft", False):
                today = dt.date.today()
                wdir = root / "things" / "workflows"
                for c in cands:
                    if c.overlaps:
                        print(f"    - not drafted `{c.carrier}`: bind `{c.overlaps[0]}` instead")
                        continue
                    wid, text = draft_text(c, today)
                    path = wdir / f"{wid}.md"
                    if path.exists() or any(t.id == wid for t in corpus.things):
                        print(f"    - kept `{wid}`: already on disk")
                        continue
                    wdir.mkdir(parents=True, exist_ok=True)
                    path.write_text(text, encoding="utf-8", newline="\n")
                    print(f"    - **drafted** {path.relative_to(root).as_posix()} — complete each "
                          "stage's steps and mark the gates, then commit")
    return 0
