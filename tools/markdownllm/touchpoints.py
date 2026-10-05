"""The Assimilate beat (change-reconciliation.md) as a floor affordance.

Inbound set for one thing: declared edges, structural pointers, provenance
pins, plus the literal-reference grep tier. Human-invoked, never hooked.

`candidates` is the companion the deep dive of 2026-08-04 added
(`inflection-candidates-are-computable`): the cue VERDICT stays human and
`touchpoints` stays invoked-never-hooked — but the cue QUESTION (does anything
reason from what was just modified?) is a mechanical predicate, and the
pre-commit hook asks it in one advisory line. Modified things qualify by
definition-surface/fan-in; additions, deletions, and renames receive their own
truthful duplicate/contradiction/removal/path questions. Never blocks, never
scores, never runs the pass.
"""

from __future__ import annotations

import datetime as dt
import os
import subprocess
from collections import Counter
from pathlib import Path

from .model import ISO_RE, scan
from .repository_view import RepositoryView, RepositoryViewError
from .structural_refs import iter_structural_references, scalar_lexeme


def cmd_touchpoints(args) -> int:
    """The Assimilate beat (change-reconciliation.md) as a floor affordance.

    Given a thing id, report the COMPLETE declared inbound set — every
    `linked_things` edge, the singular structural pointers (`parent`,
    `definition`), and provenance pins (`informed_by`) that point AT it — plus
    the literal textual references a corpus grep reaches. One read answers "what
    did I just put at risk?" instead of a remembered three-step stitch.

    Two deliberate properties:
    (1) Human-invoked, never wired into the pre-commit hook. The Cue stays the
        driver's ("The Driver Names The Inflection"); this makes the blast
        radius impossible to not see, it does not decide a change is
        consequential or initiate the pass.
    (2) Computed fresh from the live corpus, not from the committed
        `relationships`/`provenance` indexes (which can drift) — assimilation
        must be complete AND current.
    The conceptual residue (a thing that reasons about the target without
    naming it) is the irreducible human walk; no mechanical pass reaches it."""
    root = Path(args.path).resolve()
    target = args.id
    corpus, _ = scan(root)
    if target not in corpus.by_id():
        print(f"mdllm: no thing with id `{target}` in {root}")
        return 1

    declared: list[str] = []
    declared_srcs: set[str] = set()
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target:
            continue
        hits: list[str] = []
        for ref in iter_structural_references(t.meta, reverse_only=True):
            if ref.target != target:
                continue
            if ref.field == "linked_things":
                hits.append(f"(linked_things) relation `{ref.relation}`")
            elif ref.field == "informed_by":
                hits.append(f"(provenance) informed_by @{ref.commit or '?'}")
            else:
                hits.append(f"(structural) via `{ref.field}`")
        if hits:
            declared_srcs.add(src)
            for h in hits:
                declared.append(f"{src} -> {target}  {h}")

    literal: list[str] = []
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target or src in declared_srcs:
            continue
        if target in t.body:
            literal.append(src)

    print(f"## Touch points of `{target}` — {root}")
    print(f"({len(declared)} declared edge(s), {len(literal)} literal reference(s))\n")
    print("### Declared edges — the floor guarantees this set is complete")
    for d in sorted(declared) or ["- (none declares an edge to this thing)"]:
        print(d if d.startswith("- ") else f"- {d}")
    print("\n### Literal references — the id appears in another body (grep tier)")
    for src in sorted(literal):
        print(f"- {src}")
    if not literal:
        print("- (none)")
    print("\n### Conceptual residue — the human walk")
    print(f"Walk the set above: does each still hold given the change? Then ask "
          f"what reasons about `{target}` WITHOUT naming it — no mechanical pass "
          f"reaches that tier (change-reconciliation.md -> Walking the Dark Region).")
    if not declared and not literal:
        print(f"\nNothing points at `{target}`: a leaf or fresh thing carries no "
              f"consistency risk (change-reconciliation.md -> the premise).")
    return 0


# Types whose entire function is to be reasoned from — modification is a cue
# candidate regardless of fan-in. Data things qualify by fan-in instead.
# `insight` and `decision` joined at v3.26.1: both meet this set's own
# criterion (an insight exists only to be reasoned from; a decision is
# reasoned-from the moment anything cites it), and the operator felt the
# gap live — porch-bound insights modified with no cue (substrate-currency-sweep).
DEFINITION_SURFACE_TYPES = {"specification", "skill", "guide", "manifesto",
                            "prompt", "workflow-definition", "insight",
                            "decision"}
FAN_IN_THRESHOLD = 3  # inbound edges at which an ordinary thing is "reasoned-from"


def _inbound_counts(corpus) -> Counter:
    """Inbound edge count per target id: linked_things + structural pointers +
    provenance pins — the same edge set touchpoints walks, counted."""
    counts: Counter = Counter()
    for t in corpus.things:
        for ref in iter_structural_references(t.meta, cue_only=True):
            counts[ref.target] += 1
    return counts


def _parse_name_status_z(raw: bytes) -> list[tuple[str, str | None, str]]:
    """Parse ``git diff --name-status -z`` without a line/text boundary.

    With ``-z`` Git emits ``status NUL path NUL`` (and two paths for a
    rename/copy).  Paths may themselves contain tabs or newlines, so neither
    ``splitlines`` nor tab splitting is a valid parser.  Decode with
    ``surrogateescape`` so even non-UTF-8 Git path bytes round-trip through the
    local filesystem boundary rather than being replaced.
    """
    fields = raw.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()
    changes: list[tuple[str, str | None, str]] = []
    cursor = 0
    while cursor < len(fields):
        try:
            status_text = fields[cursor].decode("ascii")
        except UnicodeDecodeError:
            break
        cursor += 1
        if not status_text:
            continue
        state = status_text[0]
        path_count = 2 if state in {"R", "C"} else 1
        if cursor + path_count > len(fields):
            break
        paths = [field.decode("utf-8", errors="surrogateescape")
                 for field in fields[cursor:cursor + path_count]]
        cursor += path_count
        if state == "R":
            old_rel, rel = paths
            if old_rel.endswith(".md") or rel.endswith(".md"):
                changes.append((state, old_rel, rel))
        elif state in {"A", "M", "D"}:
            rel = paths[0]
            if rel.endswith(".md"):
                changes.append((state, rel if state == "D" else None, rel))
    return changes


def cmd_candidates(args) -> int:
    """Advisory, exit 0 always: classify every staged Markdown state.

    Additions ask about duplicate ownership/latent contradiction; deletions
    ask where their dependants go; renames ask about path and identity;
    modifications qualify by definition-surface or fan-in.  Exposure is named
    independently because add/change/delete all alter the served face.
    """
    root = Path(args.path).resolve()
    try:
        r = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "-z", "-M"],
            cwd=root, capture_output=True, timeout=20)
    except Exception:
        return 0
    if r.returncode != 0:
        return 0
    changes = _parse_name_status_z(r.stdout)
    if not changes:
        return 0

    mode = getattr(args, "view", "worktree")
    try:
        view = (RepositoryView.index(root) if mode == "index"
                else RepositoryView.worktree(root))
    except RepositoryViewError:
        return 0  # advisory only; validation reports an unavailable index
    corpus, _ = scan(root, view)
    by_path = {t.path.resolve(): t for t in corpus.things}
    prior_by_path = {}
    if any(state in {"M", "D", "R"} for state, _, _ in changes):
        try:
            prior, _ = scan(root, RepositoryView.commit(root))
            prior_by_path = {t.path.resolve(): t for t in prior.things}
        except RepositoryViewError:
            pass  # unborn/no HEAD: there can be no committed deletion
    inbound = None  # computed lazily — most commits touch no reasoned-from thing
    lines: list[str] = []
    for state, old_rel, rel in changes:
        t = by_path.get((root / rel).resolve())
        prior_rel = old_rel if old_rel else (rel if state == "M" else None)
        old = (prior_by_path.get((root / prior_rel).resolve())
               if prior_rel else None)
        if state == "D":
            if old is None or not old.id:
                lines.append(f"cue: deleted `{rel}` — inspect whether the removed "
                             "identity had conceptual or literal consumers.")
                continue
            if old.meta.get("exposed") is True:
                lines.append(f"porch: `{old.id}` was exposed — this deletion "
                             "withdraws it from consumers on their next imports-check.")
            lines.append(f"cue: `{old.id}` is deleted — route its inbound, provenance, "
                         "and conceptual dependants before accepting removal; "
                         "inspect the prior commit's inbound set before it disappears.")
            continue

        # A Git modification can still be a semantic remove/add operation:
        # frontmatter may disappear, appear, or change identity while the path
        # remains stable.  These are exactly the states an A/M/D/R cue must not
        # let fall silent.
        if state in {"M", "R"} and old and old.id and (t is None or not t.id):
            if old.meta.get("exposed") is True:
                lines.append(f"porch: `{old.id}` was exposed — this change withdraws "
                             "it from consumers on their next imports-check.")
            removal = ("removing its thing frontmatter" if state == "M"
                       else f"moving `{old_rel}` outside the Markdown corpus")
            lines.append(f"cue: `{old.id}` is deleted as a thing by {removal} — "
                         "route its inbound, provenance, and conceptual dependants "
                         "before accepting removal.")
            continue
        if t is None or not t.id:
            continue
        if str(t.meta.get("type")) == "cue":
            continue  # a cue IS the answer to a cue question; asking one of it recurses
        semantic_addition = state == "M" and (old is None or not old.id)
        identity_change = bool(
            state == "M" and old and old.id and old.id != t.id)
        any_identity_change = bool(
            state in {"M", "R"} and old and old.id and old.id != t.id)
        if state == "A":
            lines.append(f"cue: `{t.id}` is new — check duplicate ownership, latent "
                         "contradiction, and whether existing things should link to it; "
                         f"`mdllm touchpoints {t.id}`")
        elif semantic_addition:
            lines.append(f"cue: `{t.id}` is new as a thing at existing path `{rel}` — "
                         "check duplicate ownership, latent contradiction, and whether "
                         "existing things should link to it.")
        elif identity_change:
            lines.append(f"cue: modification changes identity `{old.id}` -> `{t.id}` "
                         f"at `{rel}` — treat it as a removal plus an addition and "
                         "reconcile both.")
        elif state == "R":
            if old and old.id == t.id:
                lines.append(f"cue: `{t.id}` moved `{old_rel}` -> `{rel}` with identity "
                             "stable — check literal/path consumers and loading routes.")
            else:
                old_id = old.id if old and old.id else old_rel
                lines.append(f"cue: rename changes identity `{old_id}` -> `{t.id}` — "
                             "treat it as a removal plus an addition and reconcile both.")

        old_exposed = bool(old and old.meta.get("exposed") is True)
        new_exposed = t.meta.get("exposed") is True
        if any_identity_change and old_exposed:
            lines.append(f"porch: `{old.id}` was exposed — its identity removal "
                         "withdraws it from consumers on their next imports-check.")
        elif old_exposed and not new_exposed:
            lines.append(f"porch: `{old.id}` was exposed — this {state.lower()} "
                         "withdraws it from consumers on their next imports-check.")
        if new_exposed:
            if state == "A" or semantic_addition or any_identity_change:
                verb = "addition publishes"
            elif old_exposed:
                verb = "change publishes"
            else:
                verb = "change begins publishing"
            lines.append(f"porch: `{t.id}` is exposed — this {verb}; "
                         f"consumers' pins go stale on their next imports-check.")
        if state in {"A", "R"} or semantic_addition or identity_change:
            continue  # these states already received truthful cue questions
        typ = t.meta.get("type")
        if typ in DEFINITION_SURFACE_TYPES:
            reason = f"definition surface (`{typ}`)"
        else:
            if inbound is None:
                inbound = _inbound_counts(corpus)
            n = inbound.get(t.id, 0)
            if n < FAN_IN_THRESHOLD:
                continue
            reason = f"{n} inbound edge(s)"
        lines.append(f"cue: `{t.id}` is reasoned-from ({reason}) — inflection? "
                     f"`mdllm touchpoints {t.id}`")
    if lines:
        print("-- change-reconciliation advisories (never blocking) --")
        for ln in lines:
            print(ln)
    return 0


# ------------------------------------------------------------------- cues
# The cue carrier (unattended-cue-carrier-2026-09-12; change-reconciliation.md
# → The Cue Persists). `candidates` asks the cue question at the commit
# boundary and the answer goes to stdout — at 3am, to nobody. This reads the
# same question back off the commit stream so it waits in every session-start
# digest until a human answers it with a `type: cue` thing. Two halves, one
# heading:
#   unanswered — cue things still `open`;
#   unraised   — reasoned-from things (the predicate `candidates` uses:
#                definition-surface type or fan-in) modified since the
#                baseline that no cue thing covers.
# A cue covers its subject's modifications at and before its `raised_at`
# commit — by position in the walk; by `created` date when the pin lies
# outside the window. The floor computes and reports. It never raises a cue
# and never answers one.

CUE_WINDOW_DAYS = 30  # the baseline for a domain that has never written a retrospective


def _cue_baseline(corpus) -> tuple[dt.date, str]:
    """The date the walk starts from: the newest retrospective's period end
    (scan 4 answered everything before it), else a fixed window."""
    newest: dt.date | None = None
    for t in corpus.things:
        if str(t.meta.get("type")) != "retrospective":
            continue
        for fld in ("period_end", "created"):
            v = t.meta.get(fld)
            if isinstance(v, dt.datetime):
                v = v.date()
            elif isinstance(v, str) and ISO_RE.match(v):
                v = dt.date.fromisoformat(v[:10])
            if isinstance(v, dt.date):
                newest = max(newest, v) if newest else v
                break
    if newest is not None:
        return newest, "the newest retrospective"
    return (dt.date.today() - dt.timedelta(days=CUE_WINDOW_DAYS),
            f"{CUE_WINDOW_DAYS} days — no retrospective yet")


def _modifications_since(root: Path, since: dt.date):
    """One git walk: ``[(sha, date, [paths modified])]`` newest-first.

    Modifications only — an addition is new on a clean slate (no dependants
    yet), and a deletion's dependants already dangle into a validate Error;
    neither needs a carrier to stay loud.  Returns None when git cannot be
    read, so the caller can say so rather than report an empty set as clean.
    """
    try:
        # Explicit midnight: git reads a bare `--since=YYYY-MM-DD` as that date
        # at the CURRENT time of day, so on the retrospective's own day the
        # walk silently skipped every commit that followed it (found 2026-09-13,
        # the day the baseline moved to today).
        r = subprocess.run(
            ["git", "log", "--format=%x1e%H%x00%cs", "--name-status", "-M",
             f"--since={since.isoformat()}T00:00:00", "--", "."],
            cwd=root, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=60)
    except Exception:
        return None
    if r.returncode != 0 or r.stdout is None:
        return None
    walk: list[tuple[str, dt.date, list[str], list[str]]] = []
    for record in r.stdout.split("\x1e"):
        header, _, body = record.partition("\n")
        if "\x00" not in header:
            continue
        sha, _, day = header.strip().partition("\x00")
        try:
            when = dt.date.fromisoformat(day.strip())
        except ValueError:
            continue
        modified: list[str] = []
        added: list[str] = []
        for line in body.splitlines():
            if "\t" not in line:
                continue
            state, _, rest = line.partition("\t")
            if state.startswith("M"):
                modified.append(rest)
            elif state.startswith("A"):
                added.append(rest)  # a cue's birth commit — see _covers
        walk.append((sha.strip().lower(), when, modified, added))
    return walk


def _reasoned_from_reason(t, inbound: Counter) -> str | None:
    """Why a thing is reasoned-from, or None — the same predicate `candidates`
    applies at the boundary, so the two surfaces cannot disagree."""
    typ = str(t.meta.get("type"))
    if typ in DEFINITION_SURFACE_TYPES:
        return f"definition surface (`{typ}`)"
    n = inbound.get(t.id, 0)
    if n >= FAN_IN_THRESHOLD:
        return f"{n} inbound edge(s)"
    return None


def cues_report(root: Path, corpus, since: dt.date | None = None) -> dict:
    """The two halves the digest and `mdllm cues` both print, computed once."""
    if since is not None:
        baseline, why = since, "--since"
    else:
        baseline, why = _cue_baseline(corpus)
    walk = _modifications_since(root, baseline)

    open_cues: list[dict] = []
    by_subject: dict[str, list[dict]] = {}
    for t in corpus.things:
        if str(t.meta.get("type")) != "cue" or not t.id:
            continue
        subj = t.meta.get("subject")
        pin = t.meta.get("raised_at")
        created = t.meta.get("created")
        if isinstance(created, dt.datetime):
            created = created.date()
        elif isinstance(created, str) and ISO_RE.match(created):
            created = dt.date.fromisoformat(created[:10])
        elif not isinstance(created, dt.date):
            created = None
        try:
            rel_path = t.path.resolve().relative_to(root).as_posix()
        except ValueError:
            rel_path = ""
        entry = {
            "id": t.id,
            "subject": str(subj) if subj else "",
            "status": str(t.meta.get("status")),
            "raised_at": (scalar_lexeme(pin).lower()
                          if isinstance(pin, (str, int)) and not isinstance(pin, bool)
                          else ""),
            "created": created,
            "raised_by": str(t.meta.get("raised_by") or ""),
            "path": rel_path,
        }
        if entry["status"] == "open":
            open_cues.append(entry)
        if entry["subject"]:
            by_subject.setdefault(entry["subject"], []).append(entry)

    unraised: list[dict] = []
    if walk:
        order = {sha: i for i, (sha, _, _, _) in enumerate(walk)}
        # A cue raised IN the same commit as the change it is for cannot pin
        # that commit (it does not exist yet); it pins the parent, and the
        # commit that added the cue file is covered by construction.
        birth: dict[str, int] = {}
        for i, (_, _, _, added) in enumerate(walk):
            for rel in added:
                birth.setdefault(rel, i)
        for cues in by_subject.values():
            for c in cues:
                pin = c["raised_at"]
                c["pos"] = (next((order[s] for s in order if s.startswith(pin)), None)
                            if pin else None)
                c["birth"] = birth.get(c["path"])
        by_path = {t.path.resolve(): t for t in corpus.things if t.id}
        inbound: Counter | None = None
        touched: dict[str, dict] = {}
        for i, (sha, day, paths, _) in enumerate(walk):
            for rel in paths:
                t = by_path.get((root / rel).resolve())
                if t is None or str(t.meta.get("type")) == "cue":
                    continue
                if inbound is None:
                    inbound = _inbound_counts(corpus)
                reason = _reasoned_from_reason(t, inbound)
                if reason is None:
                    continue
                if any(_covers(c, i, day) for c in by_subject.get(t.id, [])):
                    continue
                rec = touched.get(t.id)
                if rec is None:
                    rec = touched[t.id] = {"subject": t.id, "reason": reason,
                                           "commits": 0, "latest": day,
                                           "latest_sha": sha, "earliest": day}
                rec["commits"] += 1
                rec["earliest"] = min(rec["earliest"], day)
        unraised = sorted(touched.values(),
                          key=lambda r: (-r["commits"], r["subject"]))
    return {"baseline": baseline, "baseline_why": why,
            "walk_ok": walk is not None,
            "open": sorted(open_cues, key=lambda e: e["id"]),
            "unraised": unraised}


def _covers(cue: dict, position: int, day: dt.date) -> bool:
    """Does this cue cover a modification at `position` (newest-first) on `day`?
    In the commit that added the cue itself (a same-commit raise); on the day
    the cue was created (one ask per subject per day —
    `the-verdict-is-asked-where-the-change-lands-2026-10-05`); else at or
    before its `raised_at` commit when that commit is in the walk; else at or
    before the cue's own `created` date."""
    if cue.get("birth") is not None and position == cue["birth"]:
        return True
    created = cue.get("created")
    if created is not None and day == created:
        return True  # one ask per subject per day: the day's later edits are covered
    pos = cue.get("pos")
    if pos is not None:
        return position >= pos
    return created is not None and day <= created


CUE_RAISED_BODY = """---
id: {cue_id}
type: cue
status: open
version: 1.0
created: {today}
subject: {subject}
raised_at: {sha}
raised_by: "floor — mdllm cues --raise"
verdict:
verdict_reason:
tags: [cue, raised-mechanically]
---

# Cue: `{subject}` was modified — inflection?

## The Change
Raised by the floor on {today}: `{subject}` is reasoned-from ({reason}) and
was modified in {commits} commit(s) since the baseline {baseline} — latest
{latest} (`{sha7}`) — with no cue covering the change. `mdllm touchpoints
{subject}` lists what depends on it; `git log -p {sha7}` shows what moved.
The raise is mechanical (`inflection-candidates-are-computable`); the
verdict never is (`unattended-cue-carrier-2026-09-12`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
Open. Two verdicts, for a human or for the framework agent citing the ruling
that already covers it (`framework-agent-closes-settled-cues-2026-09-13`);
set `verdict`, `verdict_reason` and `status: answered` in one commit:

1. `not-inflection` — the dependants still hold as written; say why.
2. `inflection` — run the four beats (cue → assimilate → walk → seal) and
   name the touch points walked and the commit that sealed them.
"""


def raise_cues(root: Path, rep: dict) -> list[Path]:
    """Write one open `type: cue` thing per unraised subject — the mechanical
    half of the carrier (`inflection-candidates-are-computable`). The verdict
    is left empty: a raise is a question, and only a human, or the framework
    agent citing a ruling, answers it. Never overwrites — a cue already on
    disk today for that subject is kept, whoever raised it."""
    today = dt.date.today().isoformat()
    cues_dir = root / "things" / "cues"
    written: list[Path] = []
    for r in rep["unraised"]:
        cue_id = f"cue-{r['subject']}-{today}"
        path = cues_dir / f"{cue_id}.md"
        if path.exists():
            continue
        cues_dir.mkdir(parents=True, exist_ok=True)
        sha = str(r["latest_sha"])
        path.write_text(CUE_RAISED_BODY.format(
            cue_id=cue_id, today=today, subject=r["subject"], sha=sha,
            sha7=sha[:7], reason=r["reason"], commits=r["commits"],
            baseline=rep["baseline"], latest=r["latest"]),
            encoding="utf-8", newline="\n")
        written.append(path)
    return written


# ------------------------------------------------------------- the gate
# The ask, where the change lands
# (the-verdict-is-asked-where-the-change-lands-2026-10-05). `cues --staged`
# asks the cue question for the commit in hand — off the delta against HEAD,
# not the commit stream — and is the one mode of this command that is not
# advisory: exit 1 says a definition surface changes with no cue on disk,
# and the `pre-commit` lifecycle moment turns that into a harness refusal
# whose text tells the agent to put the question to the operator through the
# harness's native choice prompt. The scope is the definition surfaces only
# — the types that exist to be reasoned from, where "this is how it needs to
# be" lands; data things reasoned from by fan-in stay with `cues` and the
# retrospective's net. Coverage is a cue on disk whose `subject` is the thing
# and that was created today or is itself part of the delta: one ask per
# subject per day. The delta is read from the worktree, not the index,
# because the common `git add -A && git commit` chain stages *after* a
# PreToolUse hook has asked. The floor detects and refuses; it never answers.

UNATTENDED_ENV = "MDLLM_UNATTENDED"   # set by the dispatcher's tick: no human to ask
GATE_DEPENDANTS_SHOWN = 4


def _delta_against_head(root: Path):
    """Staged and unstaged tracked changes against HEAD, or None when git
    cannot say (no HEAD yet, not a repository) — the gate then opens and
    says it could not look rather than minting a refusal."""
    try:
        r = subprocess.run(["git", "diff", "HEAD", "--name-status", "-z", "-M"],
                           cwd=root, capture_output=True, timeout=20)
    except Exception:
        return None
    if r.returncode != 0:
        return None
    return _parse_name_status_z(r.stdout)


def _untracked(root: Path) -> set[str]:
    try:
        r = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "-z"],
                           cwd=root, capture_output=True, timeout=20)
    except Exception:
        return set()
    if r.returncode != 0:
        return set()
    return {p.decode("utf-8", "surrogateescape") for p in r.stdout.split(b"\0") if p}


def _inbound_ids(corpus) -> dict[str, list[str]]:
    """Who depends on whom, by id — the same edge set `_inbound_counts`
    counts, kept as names so the ask can say which dependants wait."""
    out: dict[str, list[str]] = {}
    for t in corpus.things:
        if not t.id:
            continue
        for ref in iter_structural_references(t.meta, cue_only=True):
            out.setdefault(ref.target, []).append(t.id)
    return out


def staged_report(root: Path, corpus, today: dt.date | None = None) -> dict:
    """The gate's question: definition surfaces changed in the commit in
    hand that no cue on disk covers."""
    today = today or dt.date.today()
    delta = _delta_against_head(root)
    if delta is None:
        return {"walk_ok": False, "owed": [], "head": "",
                "unattended": bool(os.environ.get(UNATTENDED_ENV))}
    changed = {rel for state, _, rel in delta if state.startswith("M")}
    in_delta = ({rel for _, _, rel in delta}
                | {old for _, old, _ in delta if old}
                | _untracked(root))
    cues_by_subject: dict[str, list[dict]] = {}
    by_path = {}
    for t in corpus.things:
        if not t.id:
            continue
        by_path[t.path.resolve()] = t
        if str(t.meta.get("type")) != "cue":
            continue
        subj = t.meta.get("subject")
        if not subj:
            continue
        created = t.meta.get("created")
        if isinstance(created, dt.datetime):
            created = created.date()
        elif isinstance(created, str) and ISO_RE.match(created):
            created = dt.date.fromisoformat(created[:10])
        elif not isinstance(created, dt.date):
            created = None
        try:
            rel = t.path.resolve().relative_to(root).as_posix()
        except ValueError:
            rel = ""
        cues_by_subject.setdefault(str(subj), []).append(
            {"created": created, "path": rel})
    inbound: dict[str, list[str]] | None = None
    owed: list[dict] = []
    for rel in sorted(changed):
        t = by_path.get((root / rel).resolve())
        if t is None:
            continue
        typ = str(t.meta.get("type"))
        if typ == "cue" or typ not in DEFINITION_SURFACE_TYPES:
            continue
        if any(c["created"] == today or (c["path"] and c["path"] in in_delta)
               for c in cues_by_subject.get(t.id, [])):
            continue
        if inbound is None:
            inbound = _inbound_ids(corpus)
        owed.append({"subject": t.id, "type": typ, "path": rel,
                     "dependants": sorted(inbound.get(t.id, []))})
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                              capture_output=True, text=True, timeout=20
                              ).stdout.strip().lower()
    except Exception:
        head = ""
    return {"walk_ok": True, "owed": owed, "head": head,
            "unattended": bool(os.environ.get(UNATTENDED_ENV))}


def staged_text(rep: dict) -> list[str]:
    """The refusal's text — what the agent reads in the tool's own channel.
    Vendor-neutral: the harness adapter names its own prompt tool."""
    if not rep["walk_ok"]:
        return ["## The cue question — could not look",
                "- git has no HEAD to diff against here; the gate opens with "
                "nothing checked"]
    head = ("## The cue question — the commit in hand changes what the domain "
            "reasons from")
    if not rep["owed"]:
        return [head, "- none — every definition surface changed in the commit "
                      "in hand carries its cue"]
    lines = [head]
    for o in rep["owed"]:
        deps = o["dependants"]
        shown = ", ".join(f"`{d}`" for d in deps[:GATE_DEPENDANTS_SHOWN])
        if len(deps) > GATE_DEPENDANTS_SHOWN:
            shown += f", +{len(deps) - GATE_DEPENDANTS_SHOWN} more"
        lines.append(f"- `{o['subject']}` — definition surface (`{o['type']}`); "
                     f"{len(deps)} dependant(s)"
                     + (f": {shown}" if deps else "")
                     + f" (`mdllm touchpoints {o['subject']}`)")
    if rep["unattended"]:
        lines += [
            "",
            "Unattended run: the verdict is not yours "
            "(`unattended-cue-carrier-2026-09-12`). Raise and file: "
            "`mdllm cues . --staged --raise`, then `git add things/cues`, commit "
            "again, and name the cue in your digest as a seat item.",
        ]
    else:
        lines += [
            "",
            "The verdict is the operator's, asked now, where the change lands "
            "(`the-verdict-is-asked-where-the-change-lands-2026-10-05`). Put it "
            "to them through the harness's native choice prompt — one question "
            "per subject, the option you judge right first and marked as "
            "recommended:",
            "  Inflection? — `<subject>` changes in this commit. Does the change "
            "alter a rule, a workflow, or a thing the domain reasons from?",
            "  1. Inflection — walk its dependants before this lands "
            "(`mdllm touchpoints <subject>`); name them in the cue.",
            "  2. Not an inflection — the dependants hold as written; say why.",
            "  3. File to the seat — leave the cue open for the retrospective.",
            "Then `mdllm cues . --staged --raise` (writes the open cue, pinned to "
            "HEAD); for 1 or 2 set `verdict`, `verdict_reason` in the operator's "
            "words and `status: answered`; `git add things/cues`; commit again. "
            "The commit waits until the cue is on disk.",
        ]
    return lines


CUE_STAGED_BODY = """---
id: {cue_id}
type: cue
status: open
version: 1.0
created: {today}
subject: {subject}
raised_at: {sha}
raised_by: "floor — mdllm cues --staged --raise"
verdict:
verdict_reason:
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `{subject}` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on {today}: `{subject}` is a
definition surface (`{typ}`) and changes in the commit this cue rides in,
on top of `{sha7}`. {dependants} `mdllm touchpoints {subject}` lists what
depends on it; `git show` on the carrying commit shows what moved. The raise
is mechanical; the verdict was asked where the change landed
(`the-verdict-is-asked-where-the-change-lands-2026-10-05`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
Open. The operator's pick, in their words, or the framework agent citing the
ruling that already covers it (`framework-agent-closes-settled-cues-2026-09-13`);
set `verdict`, `verdict_reason` and `status: answered` in the carrying commit:

1. `inflection` — run the four beats (cue → assimilate → walk → seal) and
   name the touch points walked and the commit that sealed them.
2. `not-inflection` — the dependants still hold as written; say why.
3. Left open — filed to the seat; answered at the retrospective.
"""


def raise_staged_cues(root: Path, rep: dict) -> list[Path]:
    """Write one open cue per owed subject, pinned to HEAD (the parent of the
    commit the cue will ride in). Never overwrites a cue already on disk
    today for that subject. The verdict is left empty."""
    today = dt.date.today().isoformat()
    cues_dir = root / "things" / "cues"
    written: list[Path] = []
    for o in rep["owed"]:
        cue_id = f"cue-{o['subject']}-{today}"
        path = cues_dir / f"{cue_id}.md"
        if path.exists():
            continue
        cues_dir.mkdir(parents=True, exist_ok=True)
        sha = rep["head"] or "HEAD"
        deps = o["dependants"]
        dependants = (f"{len(deps)} thing(s) depend on it: "
                      + ", ".join(f"`{d}`" for d in deps[:GATE_DEPENDANTS_SHOWN])
                      + (f", +{len(deps) - GATE_DEPENDANTS_SHOWN} more" if len(deps) > GATE_DEPENDANTS_SHOWN else "")
                      + "." if deps else "Nothing links to it yet.")
        path.write_text(CUE_STAGED_BODY.format(
            cue_id=cue_id, today=today, subject=o["subject"], sha=sha,
            sha7=sha[:7], typ=o["type"], dependants=dependants),
            encoding="utf-8", newline="\n")
        written.append(path)
    return written


def _cmd_cues_staged(args, root: Path, corpus) -> int:
    rep = staged_report(root, corpus)
    for ln in staged_text(rep):
        print(ln)
    if not rep["owed"]:
        if getattr(args, "raise_", False) and rep["walk_ok"]:
            print("- nothing to raise")
        return 0
    if getattr(args, "raise_", False):
        written = raise_staged_cues(root, rep)
        print(f"- **Raised ({len(written)}):** open cue thing(s) written, pinned to "
              f"HEAD — the verdict is still owed on each; `git add things/cues` "
              f"and commit them with the change:")
        for p in written:
            print(f"    - {p.relative_to(root).as_posix()}")
        if len(written) < len(rep["owed"]):
            print("    - (a cue already on disk today for a subject was kept, "
                  "not overwritten)")
        return 0
    return 1


def cmd_cues(args) -> int:
    """Advisory, exit 0 always: the cue question, read back off the commit
    stream and held until answered. Reports; with `--raise` writes the open
    cue for each unraised modification — never the verdict. The one
    exception is `--staged`, the gate's question for the commit in hand,
    which exits 1 while a definition surface changes with no cue on disk."""
    root = Path(args.path).resolve()
    try:
        corpus, _ = scan(root)
    except Exception as exc:
        print(f"mdllm: cues cannot scan {root}: {exc}")
        return 2
    if getattr(args, "staged", False):
        return _cmd_cues_staged(args, root, corpus)
    since = None
    raw = getattr(args, "since", None)
    if raw:
        try:
            since = dt.date.fromisoformat(str(raw))
        except ValueError:
            print("mdllm: --since must be a date, YYYY-MM-DD")
            return 2
    rep = cues_report(root, corpus, since)
    print(f"## Reconciliation cues — {root}")
    print(f"baseline: {rep['baseline']} ({rep['baseline_why']})")
    if not rep["walk_ok"]:
        print("- (no git history readable here — the unraised half cannot be "
              "computed; only open cue things are listed)")
    if rep["open"]:
        print(f"- **Unanswered ({len(rep['open'])}):** open cue things — a human "
              f"verdict is owed on each (`verdict` + `verdict_reason`, "
              f"`status: answered`):")
        for c in rep["open"]:
            who = f" by {c['raised_by']}" if c["raised_by"] else ""
            print(f"    - `{c['id']}` on `{c['subject']}` — raised "
                  f"{c['created'] or '?'}{who}")
    if rep["unraised"]:
        print(f"- **Unraised ({len(rep['unraised'])}):** reasoned-from things "
              f"modified since the baseline with no cue covering the change — "
              f"raise one (`templates/cue.md.template`) and answer it, or it "
              f"is answered at the retrospective:")
        for r in rep["unraised"]:
            print(f"    - `{r['subject']}` — {r['reason']}; modified in "
                  f"{r['commits']} commit(s), latest {r['latest']} "
                  f"({r['latest_sha'][:7]}); `mdllm touchpoints {r['subject']}`")
    if not rep["open"] and not rep["unraised"]:
        print("- none — every reasoned-from modification since the baseline is "
              "covered, and no cue is open.")
    if getattr(args, "raise_", False):
        if rep["unraised"]:
            written = raise_cues(root, rep)
            print(f"- **Raised ({len(written)}):** open cue thing(s) written — the "
                  f"verdict is still owed on each; rebuild the indexes "
                  f"(`mdllm index . rebuild`) and commit them together:")
            for p in written:
                print(f"    - {p.relative_to(root).as_posix()}")
            if len(written) < len(rep["unraised"]):
                print("    - (a cue already on disk today for a subject was kept, "
                      "not overwritten)")
        else:
            print("- nothing to raise")
    return 0
