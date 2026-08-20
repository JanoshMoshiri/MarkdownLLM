"""The session-start ritual, mechanically emitted.

The mechanical half of the session-start ritual, printed to stdout for a
registered harness lifecycle binding to inject. This is
the HARDENING that moves the `session-start:version-check` hook's anchor from
its `interpretation` default to `harness-session` where an adapter binds it: a
weak (or distracted) model receives the ritual at t=0 instead of having to
recall it from a buried entry file. Optional — the AGENTS.md prose stays the
interpretation floor where no adapter is installed. Read-only; safe on every
session.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import os
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
    conflicts, loops, watched = [], [], []
    for t in corpus.things:
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "conflict" and status == "open":
            conflicts.append(t.id)
        elif typ not in _ORIENT_KNOWLEDGE_TYPES and not is_terminal(corpus.schema, t.meta):
            # Watched, not owned (v3.27.0): a mirror's status is the SOURCE's
            # state restated — this domain cannot advance, close, or edit it,
            # so it is not a loop here. Exclusion, not hiding: it gets its own
            # line. The distortion scaled with how well a domain consumed
            # (58% -> 81% of the count in one estate's measured session).
            if str(t.meta.get("origin")) == "external":
                watched.append((t.id, typ, status))
            else:
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
    if watched:
        lines.append(f"- **Watched ({len(watched)}):** external things — the world's or a "
                     f"source's state, not this domain's work (`mdllm imports-check` "
                     f"reads their freshness) —")
        for tid, typ, status in sorted(watched)[:8]:
            lines.append(f"    - `{tid}` ({typ}, {status})")
        if len(watched) > 8:
            lines.append(f"    - …and {len(watched) - 8} more.")
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
        cwd=domain, capture_output=True, text=True,
        encoding="utf-8", errors="replace")
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
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
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





def _kernel_path() -> Path:
    from .scaffold import MDLLM_ENTRY

    return MDLLM_ENTRY.resolve().parents[1] / "kernel.md"


def _kernel_reference(domain: Path) -> str:
    """The path a reader in `domain` can actually open to reach the kernel.

    The kernel is framework state, so a domain-relative `kernel.md` resolves
    to a file that does not exist and the first read fails (field report
    2026-08-13). AGENTS.md already says `{framework_root}/kernel.md`; this
    renders the same fact resolved.
    """
    kernel = _kernel_path()
    try:
        return Path(os.path.relpath(kernel, domain.resolve())).as_posix()
    except ValueError:            # different drive — no relative path exists
        return kernel.as_posix()


def _kernel_integrity(text: str) -> tuple[int, str]:
    """Line count + short digest of the kernel as emitted, so "did it land
    whole" is checkable in-context (the trailer) and on disk (the
    attestation) instead of being a memory claim — the Terra failure mode:
    a load that *executed* but landed truncated produced sincere believed
    compliance that survived a casual grilling (2026-08-19). Normalised to
    `\\n` so the mark survives checkout line-ending differences."""
    normal = text.replace("\r\n", "\n")
    lines = normal.count("\n") + (0 if normal.endswith("\n") else 1)
    return lines, hashlib.sha256(normal.encode("utf-8")).hexdigest()[:12]


_KERNEL_TRAILER = ("[kernel emitted whole — {lines} lines, sha256 {digest}. "
                   "This trailer is the integrity mark: if it is missing, or "
                   "a [truncated] / [contract elided: marker appears in the "
                   "kernel above, the channel cut the emission — read "
                   "`{ref}` in full before acting.]")


def _kernel_emission(domain: Path) -> tuple[list[str], str]:
    """The operative kernel emitted inline, plus the attestation state:
    `whole:<sha12>:<lines>`, `elided`, or `absent`.

    Emission, not instruction — the five-run baseline (2026-08-18/19, two
    vendors, three harnesses, four models): emitted content is read,
    instructed content is economised. Only channels that can carry the
    kernel whole call this; the hook/runner channel defers loudly instead
    (see cmd_session_start), because truncation marked is not landing.
    """
    ref = _kernel_reference(domain)
    kernel = _kernel_path()
    if not kernel.is_file():
        return (["## The operative kernel — MISSING", "",
                 f"`{ref}` does not exist — regenerate it at the framework "
                 f"root (`mdllm kernel`) and re-run; the ritual below is "
                 f"ungoverned without it.", ""], "absent")
    text = kernel.read_text(encoding="utf-8")
    lines, digest = _kernel_integrity(text)
    if len(text) > CONTRACT_SECTION_CHARACTERS:
        return ([f"## The operative kernel — `{ref}`", "",
                 _elide(text, CONTRACT_SECTION_CHARACTERS, ref), ""],
                "elided")
    return ([f"## The operative kernel — `{ref}` (emitted)", "", text,
             _KERNEL_TRAILER.format(lines=lines, digest=digest, ref=ref),
             ""], f"whole:{digest}:{lines}")


# Contract emission bounds. The Tier-0 contract is inherently large (an
# operative kernel plus a domain entry file), so these are generous — but
# they are real: an unbounded emitter fails exactly once, on the domain
# whose entry file grew pathological (Gate 6R: protect every budget, or the
# failure moves to the unprotected one). Per-section, with marked elision
# naming the on-disk path; total output is bounded by construction because
# every unbounded input passes through a bounded section.
CONTRACT_SECTION_CHARACTERS = 48_000


def _elide(text: str, limit: int, read_path: str) -> str:
    if len(text) <= limit:
        return text
    return (text[:limit]
            + f"\n\n[contract elided: {len(text) - limit:,} of {len(text):,} "
              f"characters withheld by the emission bound — read "
              f"`{read_path}` in full before acting past this point]")


def _emit_contract(domain: Path) -> list[str]:
    """The Tier-0 contract CONTENT, emitted — injection, not instruction.

    In harnesses with entry-file discovery, AGENTS.md is in context before
    the first action and this emission is redundant (harmlessly so). In a
    harness with none — where a bootstrap assembles the workspace after the
    session has started — an instruction to *go read* the contract loses to
    the live request, and the session gate's attestation would otherwise
    vouch for an emission of ritual, not contract. This emits the contract
    itself: the operative kernel, the entry file, and a reading list derived
    from the filesystem at emission time, which therefore cannot be short
    (the 2026-08-08 field failure: an authored handoff list omitted what the
    domain's own text named, invisibly — the list was the instrument the
    load was checked against).
    """
    from .domain_kernel import routed_prompts, routed_skills

    out = ["# MarkdownLLM — Tier-0 Contract (emitted)", "",
           "This is the contract itself, not a pointer at it. Everything "
           "below is in your context now; the derived list at the end names "
           "what remains on disk for you to read at the moments it states.",
           ""]

    kernel_ref = _kernel_reference(domain)
    kernel = _kernel_path()
    if kernel.is_file():
        text = kernel.read_text(encoding="utf-8")
        out += [f"## The operative kernel — `{kernel_ref}`", "",
                _elide(text, CONTRACT_SECTION_CHARACTERS, kernel_ref)]
        if len(text) <= CONTRACT_SECTION_CHARACTERS:
            lines_n, digest = _kernel_integrity(text)
            out.append(_KERNEL_TRAILER.format(
                lines=lines_n, digest=digest, ref=kernel_ref))
        out.append("")
    else:
        out += ["## The operative kernel — MISSING", "",
                f"`{kernel_ref}` does not exist — regenerate it at the "
                "framework root (`mdllm kernel`) and re-run. The contract "
                "is incomplete without it and this emission says so rather "
                "than papering over it.", ""]

    agents = domain / "AGENTS.md"
    if agents.is_file():
        out += ["## The entry file — `AGENTS.md`", "",
                _elide(agents.read_text(encoding="utf-8"),
                       CONTRACT_SECTION_CHARACTERS, "AGENTS.md"), ""]
    else:
        out += ["## The entry file — MISSING", "",
                "No `AGENTS.md` at this root: nothing governs this position, "
                "and work here is work outside any domain contract.", ""]

    skills = routed_skills(domain)
    prompts = routed_prompts(domain)
    out += ["## Derived reading list (from the filesystem at emission time)",
            ""]
    if skills:
        out.append("**Domain skills** — the specification and write skills "
                   "are required reading before any write (kernel rule, not "
                   "discretionary); read/workflow skills per session intent:")
        out += [f"- `skills/{s}`" for s in skills]
        out.append("")
    if prompts:
        out.append("**Domain prompts** — the entry file's Session Start "
                   "block names when each runs:")
        out += [f"- `prompts/{p}`" for p in prompts]
        out.append("")
    if not skills and not prompts:
        out.append("_(no `skills/` or `prompts/` files at this root — "
                   "nothing further to route)_")
        out.append("")
    return out


def _write_contract_copy(domain: Path, text: str) -> str | None:
    """Write the full contract emission inside the git dir and return a
    domain-relative reference, or None (best-effort — emission never fails
    on its receipt copy)."""
    try:
        gd = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=domain,
                            capture_output=True, text=True)
        if gd.returncode != 0 or not gd.stdout.strip():
            return None
        target = ((domain / gd.stdout.strip()).resolve()
                  / "mdllm-contract-emission.md")
        target.write_text(text + "\n", encoding="utf-8")
        try:
            return Path(os.path.relpath(target, domain.resolve())).as_posix()
        except ValueError:
            return target.as_posix()
    except Exception:
        return None


def _record_session_attestation(domain: Path, *,
                                contract_emitted: bool = False,
                                kernel_state: str = "") -> None:
    """Record that the Tier-0 contract entered this session, per clone.

    Running session-start IS the mechanical proxy for the contract entering
    the session — this command's output is the contract's operative surface.
    Stored inside the git dir so it is uncommittable by construction;
    `mdllm validate` enforces freshness where the domain declares
    `options: {session_gate: warn|strict}`.

    **Every emitting path must call this.** The attestation attests to
    *emission*, not to a rendering format. When a second rendering existed and
    only one path attested, the gate fired against the harness integration
    that satisfies its own intent — a hook-opened session could never clear
    the gate it was designed to satisfy (field report 2026-08-13). One
    rendering remains today; the rule outlives it.

    Best-effort: orientation must never fail on it, and the gate reports
    absence itself.
    """
    try:
        gd = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=domain,
                            capture_output=True, text=True)
        if gd.returncode == 0 and gd.stdout.strip():
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=domain,
                                  capture_output=True, text=True)
            sha = head.stdout.strip() if head.returncode == 0 else "unknown"
            stamp = dt.datetime.now(dt.timezone.utc).isoformat()
            # A third token records that the contract CONTENT was emitted,
            # not only the ritual — the distinction the gate's claim rests on
            # in harnesses with no entry-file injection. The gate reads only
            # token 0 (freshness), so old two-token attestations stay valid;
            # this token is evidence for humans and Phase 5 records.
            tail = " contract" if contract_emitted else ""
            # A kernel token records what the emitter DID with the kernel:
            # whole:<sha12>:<lines> (landed, checkable), elided (bounded —
            # did not land whole), deferred (hook channel, by design), or
            # absent. The gate keeps reading token 0 for freshness (old
            # attestations stay valid) and additionally surfaces `elided`
            # as a Warning — the remote Cowork evidence (2026-08-19) showed
            # a truncated emission clearing a timestamp-only gate.
            mark = f" kernel={kernel_state}" if kernel_state else ""
            ((domain / gd.stdout.strip()).resolve() / "mdllm-attest").write_text(
                f"{stamp} {sha}{tail}{mark}\n", encoding="utf-8")
    except Exception:
        pass










def _fired_by_thing(domain: Path):
    """{thing_id: [condition, ...]} for every trigger the floor evaluated as
    fired, plus the upcoming/horizon/skipped buckets. The floor already
    computes this; session-start simply stopped asking — which is why the
    most urgent thing in a domain could be absent from the one output the
    operator always reads. `upcoming` (≤30d look-aheads) is carried
    SEPARATELY and must never be folded into `fired` — the v3.29.0 conflation
    made a quiet domain read as a domain under pressure."""
    try:
        from .triggers import evaluate
        hits, upcoming, horizon, skipped = evaluate(domain)
    except Exception:
        return {}, [], [], []
    fired: dict[str, list[str]] = {}
    for h in hits:
        tid, _, rest = h.partition(": ")
        # Drop the `-> action` tail: the action is the *derivation*, retrievable
        # via --why. The line here says what matured, not what to do about it.
        fired.setdefault(tid.strip(), []).append(rest.split(" -> ")[0].strip())
    return fired, upcoming, horizon, skipped












def cmd_session_start(args) -> int:
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    meta = {}
    if agents.is_file():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        meta = meta or {}

    # --contract: inject the Tier-0 contract content ahead of orientation.
    # Ordering is the point — the contract governs how the orientation below
    # is read and acted on, so it enters context first. Never part of the
    # hook lifecycle bindings (their output budget is two orders of magnitude
    # too small); this mode exists for bootstraps and adapterless harnesses
    # where nothing injects the entry file.
    emit_contract = bool(getattr(args, "contract", False))

    # The kernel is EMITTED, not instructed, on every channel that can carry
    # it whole — the five-run baseline (session-start-hardening Phase 0):
    # emitted content is read; instructed content is economised. The one
    # channel that cannot is the hook/runner path (2,200-character budget,
    # two orders of magnitude below the kernel); the runner marks itself via
    # MDLLM_LIFECYCLE_CHANNEL and gets a loud, checkable deferral instead —
    # a partial kernel, even with elision marked, recreates the
    # believed-loaded failure (truncation marked is not landing).
    runner_channel = bool(os.environ.get("MDLLM_LIFECYCLE_CHANNEL"))
    out: list[str] = []
    kernel_state = ""
    if emit_contract:
        out += _emit_contract(domain)
        _, kernel_state = _kernel_emission(domain)
    elif runner_channel:
        kernel_state = "deferred"
    else:
        block, kernel_state = _kernel_emission(domain)
        out += block

    kernel_ref = _kernel_reference(domain)
    if emit_contract or kernel_state.startswith("whole"):
        step1 = (f"1. Load `{kernel_ref}` (operative kernel). Already "
                 f"emitted above — loaded; do not re-read.")
    elif kernel_state == "deferred":
        kernel_file = _kernel_path()
        if kernel_file.is_file():
            lines_n, digest = _kernel_integrity(
                kernel_file.read_text(encoding="utf-8"))
            step1 = (f"1. **Kernel NOT emitted** (hook channel budget) — "
                     f"read `{kernel_ref}` END TO END before acting on "
                     f"anything below: {lines_n} lines, sha256 {digest}. "
                     f"A read that cannot account for both did not land "
                     f"whole.")
        else:
            step1 = (f"1. Load `{kernel_ref}` (operative kernel) — MISSING; "
                     f"regenerate at the framework root (`mdllm kernel`).")
    elif kernel_state == "elided":
        step1 = (f"1. The kernel above was ELIDED at the emission bound — "
                 f"read `{kernel_ref}` in full past the elision mark before "
                 f"acting.")
    else:  # absent
        step1 = (f"1. Load `{kernel_ref}` (operative kernel) — MISSING; "
                 f"regenerate at the framework root (`mdllm kernel`).")

    out += ["# MarkdownLLM — Session Start (run before the user's first request)", "",
           "The live request will pull you toward itself; do these first, then await intent:",
           step1,
           "2. Act on the version + velocity (backward) and open-loops (forward) status below.",
           "3. Surface the fired triggers below to the user; judge the ones the "
           "floor could not evaluate.", ""]

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
            elif version_tuple(seen) != version_tuple(fv):
                out.append(f"- **Version: MISMATCH** — framework v{fv}; domain last saw "
                           f"v{seen}. Validate the domain, then `mdllm refresh .` → adopt "
                           f"→ `--seal`.")
            else:
                out.append(f"- **Version: in sync** (framework v{fv}).")

    # Enforcement state before content state: if the floor is not actually
    # installed, everything below it is unenforced. Quiet when healthy.
    floor = _floor_status(domain)
    if floor:
        out.append(floor)

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

    # Retrospective cadence, computed once and emitted below at its own
    # position.
    retrospective_due: list[str] = []
    try:
        from .model import scan as _scan
        from .validation import retrospective_findings as _retro
        _corpus, _ = _scan(domain)
        retrospective_due = [f.message for f in _retro(domain, _corpus)]
    except Exception:
        retrospective_due = []  # advisory only — session start never fails on it

    out.extend(_orient_forward(domain))

    # Trigger evaluation, mechanically — session start is the primary
    # evaluation point (trigger-specification.md); until v3.24.0 this emitter
    # only *instructed* the agent to evaluate, so the most urgent thing in a
    # domain could be absent from the one output the operator always reads
    # (2026-08-01 estate sweep). Fired hits verbatim from the same evaluator
    # `mdllm triggers` runs; horizon and not-evaluable compressed to counts —
    # quiet when healthy, one line when not.
    fired, upcoming, horizon, skipped = _fired_by_thing(domain)
    if fired:
        out.append(f"- **Triggers fired ({sum(len(v) for v in fired.values())}):**")
        for tid in sorted(fired):
            for reason in fired[tid]:
                out.append(f"    - `{tid}`: {reason}")
    else:
        out.append("- **Triggers:** none currently true.")
    if upcoming:
        # Look-aheads are a separate bucket by construction — labelling them
        # "fired" is how a quiet domain reads as a domain under pressure
        # (2026-08-08 field evidence; the fix is the label, not the listing).
        out.append(f"- **Upcoming (within 30d — not yet fired) "
                   f"({len(upcoming)}):**")
        for _, line in sorted(upcoming):
            tid, _, rest = line.partition(": ")
            out.append(f"    - `{tid.strip()}`: {rest.split(' -> ')[0].strip()}")
    tail = []
    if horizon:
        tail.append(f"{len(horizon)} beyond the 30-day horizon")
    if skipped:
        tail.append(f"{len(skipped)} not mechanically evaluable — yours to judge")
    if tail:
        out.append(f"    ({'; '.join(tail)} — `mdllm triggers .` for the full evaluation)")

    # Retrospective cadence at the moment it can be acted on (estate-cadence-
    # cluster Phase 2): the v3.24.0 sensor fired only in `validate` — mid-commit,
    # the moment of least receptivity — so the debt reached the operator through
    # feel instead of the floor (change-reconciliation.md routes every missed
    # cue to the retrospective; a net-beneath-the-net with no clock is down
    # exactly when the cue-missing rate is highest). Same check, surfaced at
    # t=0. Quiet when healthy — young and dormant domains stay silent.
    for message in retrospective_due:
        out.append(f"- **Retrospective cadence:** {message}")

    _record_session_attestation(domain, contract_emitted=emit_contract,
                                kernel_state=kernel_state)

    text = "\n".join(out)
    if emit_contract:
        # Receipt path (cowork-remote-phase5-evidence-2026-08-19 F1/F2): a
        # harness may preview-truncate a large emission in its transcript
        # display — 76.4 KB became a ~2 KB preview and receipt required
        # manual recovery. The full emission is therefore also written to
        # disk (inside the git dir: uncommittable by construction) and named
        # in-band, so recovery is one file read on any harness — Read is
        # every harness's native full-content channel.
        copy_ref = _write_contract_copy(domain, text)
        if copy_ref:
            text += ("\n\n[receipt: this emission is also on disk at "
                     f"`{copy_ref}` — if any [truncated] or [contract "
                     "elided: marker appears above, read that file in full "
                     "instead of trusting the preview]")
    print(text)
    return 0
