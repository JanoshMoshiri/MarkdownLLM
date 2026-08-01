"""The session-start ritual, mechanically emitted.

The mechanical half of the session-start ritual, printed to stdout for a
harness SessionStart hook to inject (Claude Code; Copilot agent mode). This is
the HARDENING for the `session-start:version-check` hook whose anchor is
`harness-session`: a weak (or distracted) model receives the ritual at t=0
instead of having to recall it from a buried entry file. Optional — the
AGENTS.md prose stays the interpretation floor where no adapter is installed.
Read-only; safe on every session.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .model import is_terminal, parse_frontmatter, scan
from .validation import version_tuple

def _velocity_signal(domain: Path) -> str:
    things = domain / "things"
    if not things.is_dir():
        return "no `things/` directory yet."
    # encoding is explicit: git emits UTF-8, but `text=True` decodes with the
    # locale codepage, which mangles every em-dash and section sign in a commit
    # subject on Windows. The orientation output is the one place a domain's own
    # prose is quoted back at the operator — it must not arrive as mojibake.
    last = subprocess.run(["git", "log", "-1", "--format=%cr|%s", "--", "things"],
                          cwd=domain, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if last.returncode != 0 or not last.stdout.strip():
        return "no committed history over `things/` yet."
    when, _, subj = last.stdout.strip().partition("|")
    cnt = subprocess.run(["git", "rev-list", "--count", "--since=30.days", "HEAD",
                          "--", "things"], cwd=domain, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    n = cnt.stdout.strip() if cnt.returncode == 0 else "?"
    return (f"last `things/` change {when} (\"{subj.strip()}\"); {n} commit(s) in 30d. "
            f"Read `git log -- things/` for the full picture.")


# Types that sit at a non-terminal status as a steady state (knowledge/reference),
# so they are NOT "open work" — excluded from the forward orientation view.
_ORIENT_KNOWLEDGE_TYPES = {"specification", "guide", "manifesto", "insight",
                           "retrospective", "index", "continuity-brief", "prompt",
                           "workflow-definition", "decision", "artifact"}


def _orient_forward(domain: Path) -> list[str]:
    """The forward half of orientation — the open loops the next session inherits,
    computed from the thing graph. Orient is the session-memory counterpart to
    change-reconciliation's work-content state: backward orientation is the commit
    stream (velocity), this is its forward complement (what is still open). Replaces
    the hand-maintained continuity brief (dissolve-continuity-into-reconciliation)."""
    try:
        corpus, _ = scan(domain)
    except Exception:
        return []
    conflicts, loops = [], []
    for t in corpus.things:
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "conflict" and status == "open":
            conflicts.append(t.id)
        elif typ not in _ORIENT_KNOWLEDGE_TYPES and not is_terminal(corpus.schema, t.meta):
            loops.append((t.id, typ, status))
    lines: list[str] = []
    if conflicts:
        lines.append("- **Open conflicts (%d):** %s — resolve or carry forward."
                     % (len(conflicts), ", ".join(f"`{c}`" for c in sorted(conflicts))))
    if loops:
        lines.append(f"- **Open loops ({len(loops)}):** forward work still in flight —")
        for tid, typ, status in sorted(loops)[:15]:
            lines.append(f"    - `{tid}` ({typ}, {status})")
        if len(loops) > 15:
            lines.append(f"    - …and {len(loops) - 15} more (`mdllm validate` lists all).")
    return lines


def _verified_flips_recent(domain: Path) -> list[str]:
    """`verified: true` flips since the last `session-end:` commit (fallback:
    the last 15 commits) — the visibility leg of the quarantine flip
    discipline (verified-flip-enforcement plan). A wrong or rogue flip cannot
    hide when every flip is surfaced where the operator already looks.
    Silent (empty list) when there are none."""
    log = subprocess.run(["git", "log", "--format=%H%x1f%s", "-n", "200"],
                         cwd=domain, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if log.returncode != 0 or not log.stdout.strip():
        return []
    commits = [ln.split("\x1f", 1) for ln in log.stdout.splitlines() if ln]
    base = None
    for h, subj in commits[1:]:  # HEAD itself being a session-end still ends a session
        if subj.startswith("session-end"):
            base = h
            break
    if base is None:
        base = commits[min(15, len(commits) - 1)][0] if len(commits) > 1 else None
    if base is None:
        return []
    flips = subprocess.run(
        ["git", "log", "--format=%h", "--name-only",
         "-G", r"^verified: *[Tt]rue", f"{base}..HEAD"],
        cwd=domain, capture_output=True, text=True)
    if flips.returncode != 0:
        return []
    lines: list[str] = []
    sha = None
    seen: set[str] = set()
    for ln in flips.stdout.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if "/" not in ln and " " not in ln and len(ln) in range(6, 13):
            sha = ln
            continue
        if not ln.endswith(".md") or ln in seen:
            continue
        seen.add(ln)
        f = domain / ln
        if not f.is_file():
            continue  # flipped then deleted/moved — git has the record
        meta, _, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        if not (meta and meta.get("verified") is True
                and str(meta.get("origin")) == "external"):
            continue
        by = meta.get("verified_by")
        by = by.strip() if isinstance(by, str) and by.strip() else "UNATTRIBUTED"
        lines.append(f"    - `{meta.get('id') or ln}` @ {sha} (verified_by: {by})")
    return lines


def _floor_status(root: Path) -> str | None:
    """One line when the mechanical floor is absent or stale; None when healthy.

    Why session-start and not just `doctor`: git hooks live in `.git/hooks/`,
    which is NEVER cloned. A domain that is re-cloned (every fresh agent
    session that clones rather than copies) silently loses its git-fs anchor
    and orients perfectly cleanly the next session — the one command that
    would say so, `doctor`, requires already suspecting it. Surfacing it at
    orientation is what makes the domain aware of its own enforcement state.

    Deliberately cheap — presence and body-freshness only, no `git hook run`
    (that stays doctor's deep probe): this runs on every session start.
    Imports are deferred because scaffold imports this module.
    """
    from .scaffold import COMMIT_MSG_HOOK_BODY, HOOK_BODY, MDLLM_ENTRY
    import os

    inside = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                            capture_output=True, text=True)
    if inside.returncode != 0:
        return None  # not a git repo — scaffold/doctor own that case
    git_dir = (root / inside.stdout.strip()).resolve()
    missing = [n for n in ("pre-commit", "commit-msg")
               if not (git_dir / "hooks" / n).is_file()]
    if missing:
        return (f"- **Floor: NOT INSTALLED** — missing git {', '.join(missing)} "
                f"hook(s). Mechanical validation is NOT enforced at the commit "
                f"boundary (hooks live in .git/hooks and are never cloned). "
                f"Run `mdllm install-hook .`")
    try:
        rel = Path(os.path.relpath(MDLLM_ENTRY, root)).as_posix()
    except ValueError:
        rel = MDLLM_ENTRY.as_posix()
    stale = []
    for name, body in (("pre-commit", HOOK_BODY),
                       ("commit-msg", COMMIT_MSG_HOOK_BODY)):
        installed = (git_dir / "hooks" / name).read_text(
            encoding="utf-8").replace("\r\n", "\n").strip()
        if installed != body.format(rel=rel).replace("\r\n", "\n").strip():
            stale.append(name)
    if stale:
        return (f"- **Floor: STALE** — {', '.join(stale)} hook body predates the "
                f"current framework; it may not run newer checks. Re-run "
                f"`mdllm install-hook .`")
    return None


# --------------------------------------------------------------------------
# PHASE 0 PROTOTYPE — assistant-register plan. Lives behind `--assistant` for
# the test drive ONLY; if the register survives Phase 0 this becomes the single
# default rendering (a `--brief` variant was rejected in the plan: two
# renderings drift). Nothing below fakes judgment the floor lacks — it orders
# by what the mechanics honestly know and hands sequencing to the agent.
# --------------------------------------------------------------------------

_PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}

_REGISTER_SEED = """\
Answer the operator's loop first — *what have I got, what's first, where do
I go* — and answer it in their language. Report domain substance, never your
own preparation. Say nothing where the domain is healthy. Expand, never
smooth, where a human has to decide. Retain the derivation: "show me why"
must always work (`mdllm session-start <path> --why`).

Before the first reply: load `kernel.md`; act on what is below. Do not
narrate having done so."""


def _days_past(reason: str) -> int | None:
    """How stale a fired trigger is, read out of the floor's own phrasing.
    None when the reason names no elapsed time (fires-in-future, or a
    condition with no date at all)."""
    m = re.search(r"OVERDUE by (\d+)d", reason) or re.search(r"\((\d+)d ago\)", reason)
    return int(m.group(1)) if m else None


def _fired_by_thing(domain: Path):
    """{thing_id: [condition, ...]} for every trigger the floor evaluated as
    fired. The floor already computes this; session-start simply stopped
    asking — which is why the most urgent thing in a domain could be absent
    from the one output the operator always reads."""
    try:
        from .triggers import evaluate
        hits, horizon, skipped = evaluate(domain)
    except Exception:
        return {}, [], []
    fired: dict[str, list[str]] = {}
    for h in hits:
        tid, _, rest = h.partition(": ")
        # Drop the `-> action` tail: the action is the *derivation*, retrievable
        # via --why. The line here says what matured, not what to do about it.
        fired.setdefault(tid.strip(), []).append(rest.split(" -> ")[0].strip())
    return fired, horizon, skipped


def _open_work(domain: Path):
    try:
        corpus, _ = scan(domain)
    except Exception:
        return [], [], {}, None
    conflicts, loops = [], []
    for t in corpus.things:
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "conflict" and status == "open":
            conflicts.append(t)
        elif typ not in _ORIENT_KNOWLEDGE_TYPES and not is_terminal(corpus.schema, t.meta):
            loops.append(t)
    return conflicts, loops, {t.id: t for t in corpus.things}, corpus.schema


def _as_date(v):
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except Exception:
        return None


def _rank_open(loops, fired: dict[str, list[str]], schema=None):
    """Mechanical ordering only: fired triggers (most-matured first), then
    due-date proximity, then priority, alphabetical as the final tiebreak.
    Genuine sequencing is the agent's — this just refuses to make the
    operator find the overdue item themselves."""
    today = dt.date.today()
    rows = []
    for t in loops:
        tid = t.id
        reasons = fired.get(tid, [])
        matured = max([d for d in (_days_past(r) for r in reasons) if d is not None],
                      default=None)
        due = _as_date(t.meta.get("due_date"))
        due_days = (due - today).days if due else None
        prio = str(t.meta.get("priority", "")).lower()
        try:
            settled = bool(schema is not None and is_terminal(schema, t.meta))
        except Exception:
            settled = False
        rows.append({
            "id": tid, "type": str(t.meta.get("type")),
            "status": str(t.meta.get("status")), "settled": settled,
            "reasons": reasons, "matured": matured,
            "due": due, "due_days": due_days, "priority": prio,
            "key": (0 if reasons else 1,
                    -(matured if matured is not None else 0),
                    due_days if due_days is not None else 10 ** 6,
                    _PRIORITY_RANK.get(prio, 9),
                    tid),
        })
    rows.sort(key=lambda r: r["key"])
    return rows


def _row_line(r: dict) -> str:
    """One open item, with the mechanical grounds for its position stated —
    never a recommendation, always a fact the operator can check."""
    bits = []
    if r["due_days"] is not None and r["due_days"] < 0:
        bits.append(f"**overdue {-r['due_days']}d** (due {r['due']})")
    elif r["due_days"] is not None and r["due_days"] <= 30:
        bits.append(f"due in {r['due_days']}d ({r['due']})")
    if r["reasons"]:
        n = len(r["reasons"])
        if r["matured"] is not None:
            bits.append(f"{n} trigger{'s' if n > 1 else ''} matured "
                        f"(oldest {r['matured']}d ago)")
        else:
            bits.append(f"{n} trigger{'s' if n > 1 else ''} fired")
    if r["priority"] in ("high", "critical") and not r["reasons"]:
        bits.append(f"{r['priority']} priority")
    if r["type"] == "conflict":
        bits.append("open conflict")
    elif r["settled"]:
        # The thing is closed but its trigger is not — a wait left behind by
        # finished work is the most invisible kind there is.
        bits.append(f"{r['status']}, but the wait is still live")
    tail = " — " + " · ".join(bits) if bits else f" — {r['status']}"
    return f"- `{r['id']}`{tail}"


def _render_assistant(domain: Path, meta: dict, exceptions: list[str],
                      flips: list[str], velocity: str) -> list[str]:
    fired, horizon, skipped = _fired_by_thing(domain)
    conflicts, loops, by_id, schema = _open_work(domain)

    # A fired trigger must reach the operator whatever it is attached to. The
    # open-loop set is NOT the right filter: a trigger declared on a conflict,
    # or on a plan that closed while leaving a wait behind, is exactly the kind
    # the domain most needs surfaced — and filtering by open-loop membership
    # silently swallowed both. (Phase 0, QMS drive: two such triggers vanished.)
    ranked_things = list(loops)
    seen = {t.id for t in loops}
    for tid in fired:
        if tid not in seen and tid in by_id:
            ranked_things.append(by_id[tid])
            seen.add(tid)

    rows = _rank_open(ranked_things, fired, schema)
    attention = [r for r in rows if r["reasons"] or
                 (r["due_days"] is not None and r["due_days"] <= 30)]
    att_ids = {r["id"] for r in attention}
    rest = [r for r in rows if r["id"] not in att_ids]
    conflicts = [c for c in conflicts if c.id not in att_ids]

    out = [f"# {domain.name} — session start", "", _REGISTER_SEED, ""]

    if attention:
        out.append("## Wants attention")
        out += [_row_line(r) for r in attention]
        out.append("")

    if rest:
        out.append(f"## Also open ({len(rest)})")
        out.append("  " + " · ".join(f"`{r['id']}`" for r in rest[:15]))
        if len(rest) > 15:
            out.append(f"  …and {len(rest) - 15} more.")
        out.append("")

    if conflicts:
        out.append(f"## Unresolved conflicts ({len(conflicts)})")
        out.append("  " + " · ".join(f"`{c.id}`" for c in conflicts))
        out.append("")

    # Rule 4 — expand at human-decides moments. This is the one section that
    # gets LONGER, not shorter: a wrong flip is unrecoverable in retrospect,
    # and smooth prose here would buy assent exactly where deliberation is owed.
    if flips:
        out.append(f"## Needs your confirmation ({len(flips)})")
        out.append("External things were marked human-verified since the last "
                   "session. Each one now carries decisions. Confirm each is real:")
        out += flips
        out.append("")

    if exceptions:
        out.append("## Not working as it should")
        out += exceptions
        out.append("")

    out.append("## Backdrop")
    # The full subject line of a session-end commit runs to hundreds of words.
    # Verbatim, it is the single largest block in the orientation and answers
    # none of the operator's four questions; the log is one command away.
    v = velocity
    m = re.match(r'last `things/` change (.+?) \("(.*)"\); (\d+|\?) commit', v, re.S)
    if m:
        when, subj, n = m.group(1), " ".join(m.group(2).split()), m.group(3)
        if len(subj) > 110:
            subj = subj[:110].rsplit(" ", 1)[0] + "…"
        v = f"Last worked {when}: \"{subj}\" · {n} commit(s) in 30d."
    out.append(f"- {v}")
    if horizon:
        out.append(f"- {len(horizon)} item(s) beyond the 30-day horizon.")
    if skipped:
        out.append(f"- {len(skipped)} trigger(s) the floor cannot evaluate — "
                   f"yours to judge.")
    out.append("")
    out.append("_Ask for the derivation of anything here (`--why`), the horizon, "
               "or the triggers left to judgment._")
    return out


def cmd_session_start(args) -> int:
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    meta = {}
    if agents.is_file():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        meta = meta or {}

    assistant = getattr(args, "assistant", False)
    # Exceptions accumulate separately from the legacy line-stream so the
    # assistant renderer can group them under one plain-language heading.
    exceptions: list[str] = []

    out = ["# MarkdownLLM — Session Start (run before the user's first request)", "",
           "The live request will pull you toward itself; do these first, then await intent:",
           "1. Load `kernel.md` (operative kernel).",
           "2. Act on the version + velocity (backward) and open-loops (forward) status below.",
           "3. Evaluate triggers and surface what needs the user.", ""]

    fr = meta.get("framework_root")
    if (domain / ".markdownllm").is_file():
        # This IS a framework root (it carries the sentinel), not a downstream
        # domain — `framework_root: .` points at itself, so the domain
        # version-check does not apply.
        fv = str((yaml.safe_load((domain / ".markdownllm").read_text(encoding="utf-8"))
                  or {}).get("version"))
        out.append(f"- **Version:** framework root (v{fv}) — not a downstream domain; "
                   f"no refresh applies.")
    elif not fr:
        out.append("- **Version:** n/a — no `framework_root` in AGENTS.md.")
    else:
        sentinel = (domain / fr).resolve() / ".markdownllm"
        if not sentinel.is_file():
            out.append(f"- **Version:** unknown — `framework_root` `{fr}` has no .markdownllm.")
        else:
            fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}).get("version"))
            seen = str(meta.get("framework_version_seen", ""))
            if not seen:
                out.append(f"- **Version: STALE** — framework v{fv}; domain has no "
                           f"`framework_version_seen`. Run `mdllm refresh .` and adopt.")
                exceptions.append(f"- This domain has never recorded which framework "
                                  f"version it was built against (now v{fv}). "
                                  f"Run `mdllm refresh .` and adopt.")
            elif version_tuple(seen) != version_tuple(fv):
                out.append(f"- **Version: MISMATCH** — framework v{fv}; domain last saw "
                           f"v{seen}. Validate the domain, then `mdllm refresh .` → adopt "
                           f"→ `--seal`.")
                exceptions.append(f"- The framework moved on (v{seen} → v{fv}) and this "
                                  f"domain hasn't caught up. Validate it, then "
                                  f"`mdllm refresh .` → adopt → `--seal`.")
            else:
                out.append(f"- **Version: in sync** (framework v{fv}).")

    # Enforcement state before content state: if the floor is not actually
    # installed, everything below it is unenforced. Quiet when healthy.
    floor = _floor_status(domain)
    if floor:
        out.append(floor)
        if "NOT INSTALLED" in floor:
            exceptions.append("- Safety checks aren't switched on in this copy of the "
                              "domain, so nothing is stopping a bad commit. "
                              "Run `mdllm install-hook .`")
        else:
            exceptions.append("- The safety checks in this copy are an old version and "
                              "may miss newer problems. Run `mdllm install-hook .`")

    velocity = _velocity_signal(domain)
    out.append(f"- **Velocity:** {velocity}")

    flips = _verified_flips_recent(domain)
    if flips:
        out.append(f"- **Verified flips since last session ({len(flips)}):** "
                   f"external things marked human-verified — confirm each is real:")
        out.extend(flips)

    if agents.is_file():
        _, drifted = domain_kernel_status(
            agents.read_text(encoding="utf-8"),
            build_domain_kernel_blocks(domain, meta))
        if drifted:
            out.append(f"- **Domain kernel: DRIFT** in {', '.join(drifted)} — run "
                       f"`mdllm domain-kernel .` and commit.")
            exceptions.append(f"- The rules copied into this domain's AGENTS.md no "
                              f"longer match the framework ({', '.join(drifted)}). "
                              f"Run `mdllm domain-kernel .` and commit.")

    if assistant:
        print("\n".join(_render_assistant(domain, meta, exceptions, flips, velocity)))
        return 0

    out.extend(_orient_forward(domain))

    print("\n".join(out))
    return 0
