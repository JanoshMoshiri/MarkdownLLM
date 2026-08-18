"""Estate git sync — fetch + fast-forward across the machine axis.

Mechanises the `session-start:estate-sync` hard hook (orchestration.md) and
git-workflow.md -> The Machine Axis: orientation reads committed state, and in
a multi-machine estate committed state partly lives on the remote — so sync
runs BEFORE orientation, and `cmd_session_start` stays read-only.

Doctrine, by construction:
- **ff-only.** A fast-forward is transport of state already real elsewhere.
  Anything else is `divergence-is-an-unrouted-decision`: reported, never
  resolved. The sync walk itself never pushes, never merges, never resets —
  the push side is `autopush` below (post-commit hook), which is the same
  transport argument run in reverse and under the same doctrine: bounded,
  never forcing, divergence surfaced never resolved.
- **Bounded, degrading, never blocking.** GIT_TERMINAL_PROMPT=0 + per-repo
  timeout; offline/auth failure degrades to an advisory state and the session
  proceeds. A REQUIRED network call at session start is forbidden; this is a
  bounded attempt.
- **Discovery is legitimate here — estate-check's guardrail does not
  transfer.** estate-check refuses discovery because its objects are membrane
  reads and a registry would become a producer->consumer map. This walk's
  objects are repos and their own remotes: it reveals nothing `ls` doesn't
  and touches no membrane. Batching-never-an-index still binds: stdout-only,
  ephemeral, nothing persisted.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

DEFAULT_TIMEOUT = 20  # seconds per network call; a hook that can hang a session start is worse than none
ESTATE_GLOBAL_TIMEOUT = 75


def _git(repo: Path, *args: str, timeout: int = DEFAULT_TIMEOUT):
    """Run git non-interactively; None on timeout (caller treats as offline)."""
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"  # never prompt — degrade instead
    env.setdefault("GCM_INTERACTIVE", "never")
    try:
        return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                              text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None


def discover_repos(root: Path) -> list[Path]:
    """Root repo + immediate children of domain/ and domains/ that are repos."""
    repos = []
    if (root / ".git").exists():
        repos.append(root)
    for holder in ("domain", "domains"):
        d = root / holder
        if d.is_dir():
            for child in sorted(d.iterdir()):
                if child.is_dir() and (child / ".git").exists():
                    repos.append(child)
    return repos


def _counts(repo: Path) -> tuple[int, int] | None:
    """(ahead, behind) vs @{upstream} from cached tracking refs — no network."""
    r = _git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
    if r is None or r.returncode != 0:
        return None
    try:
        a, b = r.stdout.split()
        return int(a), int(b)
    except ValueError:
        return None


def _classify_fetch_failure(stderr: str) -> str:
    """Name the cause only where the evidence names it. The else branch used
    to return `offline` — a definite cause for a failure it never diagnosed —
    which read a proxy's 403 as a network outage (`a-403-is-not-an-outage`,
    QMS porch 2026-08-06; the null-result primitive: never return the shape
    of an answer to a question you could not answer). An undiagnosed failure
    now says so, and carries its evidence in the detail at the call sites."""
    s = stderr.lower()
    if ("terminal prompts disabled" in s or "authentication" in s
            or "permission denied" in s or "403" in s or "401" in s):
        return "auth-failed"
    if ("could not resolve host" in s or "connection refused" in s
            or "failed to connect" in s or "could not connect to server" in s
            or "timed out" in s or "network is unreachable" in s
            or "no route to host" in s):
        return "offline"
    return "fetch-failed"


def _first_stderr_line(stderr: str) -> str:
    for line in (stderr or "").splitlines():
        if line.strip():
            return line.strip()[:120]
    return "no stderr"


def sync_repo(repo: Path, fetch: bool = True, timeout: int = DEFAULT_TIMEOUT,
              deadline: float | None = None) -> dict:
    """One repo's sync outcome: {'repo', 'state', 'detail', 'moved'}.

    States: synced / up-to-date / ahead / diverged / dirty / local-only /
    no-upstream / detached / unborn / in-operation / offline / auth-failed /
    fetch-failed / pull-failed / budget-exhausted. Only 'synced' moves the
    tree; everything else reports.
    """
    out = {"repo": repo, "state": "up-to-date", "detail": "", "moved": False}

    remotes = _git(repo, "remote")
    if remotes is None or not remotes.stdout.strip():
        out["state"] = "local-only"
        return out

    gitdir_r = _git(repo, "rev-parse", "--git-dir")
    gitdir = repo / (gitdir_r.stdout.strip() if gitdir_r and gitdir_r.returncode == 0 else ".git")
    if any((gitdir / f).exists() for f in ("MERGE_HEAD", "rebase-merge", "rebase-apply")):
        out["state"] = "in-operation"
        out["detail"] = "merge/rebase in progress — skipped"
        return out

    if (r := _git(repo, "rev-parse", "--verify", "-q", "HEAD")) is None or r.returncode != 0:
        out["state"] = "unborn"
        return out
    if (r := _git(repo, "symbolic-ref", "-q", "--short", "HEAD")) is None or r.returncode != 0:
        out["state"] = "detached"
        out["detail"] = "detached HEAD — skipped"
        return out

    if fetch:
        remaining = ((deadline - time.monotonic())
                     if deadline is not None else float(timeout))
        if remaining <= 0:
            f = None
            out["state"] = "budget-exhausted"
            out["detail"] = ("global estate deadline exhausted before fetch "
                             "— orienting from last-fetched state")
        else:
            f = _git(repo, "fetch", "--quiet",
                     timeout=min(float(timeout), remaining))
        if f is None and out["state"] != "budget-exhausted":
            if deadline is not None and time.monotonic() >= deadline:
                out["state"] = "budget-exhausted"
                out["detail"] = ("global estate deadline exhausted during "
                                 "fetch — orienting from last-fetched state")
            else:
                out["state"] = "offline"
                out["detail"] = ("fetch timed out — orienting from "
                                 "last-fetched state")
        elif f is not None and f.returncode != 0:
            out["state"] = _classify_fetch_failure(f.stderr)
            out["detail"] = "orienting from last-fetched state"
            if out["state"] == "fetch-failed":
                out["detail"] = (f"undiagnosed ({_first_stderr_line(f.stderr)}) — "
                                 f"orienting from last-fetched state")

    counts = _counts(repo)
    if counts is None:
        if out["state"] in (
                "offline", "auth-failed", "fetch-failed", "budget-exhausted"):
            return out
        out["state"] = "no-upstream"
        return out
    ahead, behind = counts
    cached = " (cached)" if out["state"] in (
        "offline", "auth-failed", "fetch-failed", "budget-exhausted") else ""
    degraded = out["state"] if cached else None

    dirty = _git(repo, "status", "--porcelain")
    is_dirty = bool(dirty and dirty.stdout.strip())

    if ahead and behind:
        out["state"] = "diverged"
        out["detail"] = f"+{ahead} local / +{behind} remote{cached} — a decision is owed, not a merge"
    elif behind:
        if is_dirty:
            out["state"] = "dirty"
            out["detail"] = f"+{behind} remote{cached} — pull skipped, working tree not clean"
        elif degraded:
            reason = ("global estate deadline exhausted"
                      if degraded == "budget-exhausted" else "fetch failed")
            out["detail"] = (f"+{behind} remote (cached) — pull skipped, "
                             f"{reason}")
        else:
            remaining = ((deadline - time.monotonic())
                         if deadline is not None else float(timeout))
            if remaining <= 0:
                p = None
                out["state"] = "budget-exhausted"
                out["detail"] = (f"+{behind} remote (cached) — pull skipped, "
                                 "global estate deadline exhausted")
            else:
                p = _git(repo, "pull", "--ff-only", "--quiet",
                         timeout=min(float(timeout), remaining))
            if p is not None and p.returncode == 0:
                out["state"] = "synced"
                out["detail"] = f"+{behind}"
                out["moved"] = True
            elif out["state"] != "budget-exhausted":
                out["state"] = "pull-failed"
                err = (p.stderr.strip().splitlines() or ["?"])[-1] if p else "timeout"
                out["detail"] = err
    elif ahead:
        out["state"] = "ahead" if not degraded else out["state"]
        out["detail"] = f"+{ahead} (unpushed){cached}"
    elif is_dirty:
        # Up to date with the remote but uncommitted work in the tree — not
        # sync's problem to fix, but worth a word at session start.
        out["detail"] = "working tree not clean"
    return out


def _autopush_enabled(repo: Path) -> bool:
    """`git.autopush` from the repo's AGENTS.md frontmatter — absence is ON
    (estate-cadence-cluster Phase 1, operator ruling 2026-08-04: the opt-out
    set is the small one). Only an explicit `autopush: false` opts out; a
    missing AGENTS.md, missing git block, or unparseable frontmatter all mean
    the default applies."""
    agents = repo / "AGENTS.md"
    if not agents.is_file():
        return True
    try:
        import re
        import yaml
        text = agents.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
        if not m:
            return True
        fm = yaml.safe_load(m.group(1)) or {}
        git_cfg = fm.get("git") or {}
        return git_cfg.get("autopush") is not False
    except Exception:
        return True


def autopush_repo(repo: Path, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """The post-commit publication leg: push the current branch to its
    upstream — transport of already-committed, floor-validated state.

    States: off / local-only / detached / unborn / no-upstream / published /
    rejected / offline / auth-failed. Never forces (structurally: --force is
    not in this function's vocabulary), never blocks (the caller exits 0
    regardless), never resolves a rejection — a rejected push is DIVERGED on
    the push side, an unrouted decision the operator routes."""
    out = {"repo": repo, "state": "published", "detail": ""}
    if not _autopush_enabled(repo):
        out["state"] = "off"
        return out
    remotes = _git(repo, "remote")
    if remotes is None or not remotes.stdout.strip():
        out["state"] = "local-only"  # legitimate standing state; estate-sync reports it
        return out
    if (r := _git(repo, "rev-parse", "--verify", "-q", "HEAD")) is None or r.returncode != 0:
        out["state"] = "unborn"
        return out
    br = _git(repo, "symbolic-ref", "-q", "--short", "HEAD")
    if br is None or br.returncode != 0:
        out["state"] = "detached"
        return out
    branch = br.stdout.strip()
    upstream = _git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if upstream is None or upstream.returncode != 0:
        out["state"] = "no-upstream"
        out["detail"] = (f"branch `{branch}` has no upstream — set one "
                         f"(`git push -u origin {branch}`) or declare `git: autopush: false`")
        return out
    p = _git(repo, "push", "--porcelain", timeout=timeout)
    if p is None:
        out["state"] = "offline"
        out["detail"] = "push timed out — commit stands as publication debt (`mdllm estate-sync --status`)"
        return out
    if p.returncode == 0:
        out["detail"] = f"{branch} -> {upstream.stdout.strip()}"
        return out
    stderr = p.stderr.lower() + p.stdout.lower()
    if "non-fast-forward" in stderr or "rejected" in stderr or "fetch first" in stderr:
        out["state"] = "rejected"
        out["detail"] = ("remote moved — DIVERGED on the push side: a decision is owed, "
                         "not a merge. Commit stands as publication debt; never forced.")
    else:
        out["state"] = _classify_fetch_failure(p.stderr)
        out["detail"] = "could not publish — commit stands as publication debt (`mdllm estate-sync --status`)"
        if out["state"] == "fetch-failed":
            out["detail"] = (f"undiagnosed ({_first_stderr_line(p.stderr)}) — "
                             f"commit stands as publication debt (`mdllm estate-sync --status`)")
    return out


def cmd_autopush(args) -> int:
    """Hook entry: one advisory line at most, exit 0 always — a post-commit
    surface must never fail the commit it follows."""
    repo = Path(args.path).resolve()
    res = autopush_repo(repo, timeout=args.timeout)
    state = res["state"]
    if state in ("off", "local-only", "unborn", "detached"):
        return 0  # silent: opted out or nothing to transport; estate-sync owns the standing report
    if state == "published":
        print(f"autopush: published {res['detail']}")
    else:
        print(f"autopush: {state.upper()} — {res['detail']}")
    return 0


_LABEL = {
    "synced": "synced", "up-to-date": "up-to-date", "ahead": "ahead",
    "diverged": "DIVERGED", "dirty": "dirty", "local-only": "local-only",
    "no-upstream": "no-upstream", "detached": "detached", "unborn": "unborn",
    "in-operation": "in-operation", "offline": "offline",
    "auth-failed": "auth-failed", "pull-failed": "pull-failed",
    "fetch-failed": "fetch-failed",
    "budget-exhausted": "budget-exhausted",
}


def cmd_estate_sync(args) -> int:
    root = Path(args.paths[0] if args.paths else ".").resolve()
    if args.paths and len(args.paths) > 1:
        repos = [Path(p).resolve() for p in args.paths]
    else:
        repos = discover_repos(root)
    if not repos:
        print(f"estate-sync: no git repos under {root}")
        return 0

    fetch = not args.status
    title = "Publication Debt" if args.status else "Estate Sync"
    print(f"## {title} — {root.name} ({len(repos)} repo(s))\n")
    deadline = (time.monotonic() + ESTATE_GLOBAL_TIMEOUT) if fetch else None
    results = [sync_repo(r, fetch=fetch, timeout=args.timeout,
                         deadline=deadline) for r in repos]
    debt = 0
    for res in results:
        name = res["repo"].name
        label = _LABEL.get(res["state"], res["state"])
        line = f"- `{name}`: {label}"
        if res["detail"]:
            line += f" — {res['detail']}" if res["state"] != "synced" else f" ({res['detail']})"
        if args.status and res["state"] not in ("ahead", "diverged", "dirty"):
            continue  # debt view: only what the estate cannot see yet
        print(line)
        if args.status:
            debt += 1
    if args.status:
        if debt == 0:
            print("- nothing unpublished — the estate sees everything committed here")
        print("\nUnder autopush (the default) every line above is an anomaly — route it, "
              "don't just push it. Where `git: autopush: false`, publication stays yours: "
              "review `git log`, then push per repo when satisfied.")
        return 0

    moved = [res["repo"] for res in results if res["moved"]]
    diverged = [res["repo"].name for res in results if res["state"] == "diverged"]
    if moved:
        roots = " ".join(str(m) for m in moved)
        print(f"\n{len(moved)} repo(s) moved — consider `mdllm estate-check {roots}` "
              f"to re-check the membrane (pulled source commits can flip imports stale/diverged).")
    if diverged:
        print(f"\nDIVERGED: {', '.join(diverged)} — route each as a decision "
              f"(git-workflow.md -> The Machine Axis); never auto-merge.")
    print("\nThis is a batch of per-repo reads — ephemeral, never an index. Sync before orienting.")
    return 0
