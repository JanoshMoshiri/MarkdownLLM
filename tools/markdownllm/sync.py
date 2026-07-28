"""Estate git sync — fetch + fast-forward across the machine axis.

Mechanises the `session-start:estate-sync` hard hook (orchestration.md) and
git-workflow.md -> The Machine Axis: orientation reads committed state, and in
a multi-machine estate committed state partly lives on the remote — so sync
runs BEFORE orientation, and `cmd_session_start` stays read-only.

Doctrine, by construction:
- **ff-only.** A fast-forward is transport of state already real elsewhere.
  Anything else is `divergence-is-an-unrouted-decision`: reported, never
  resolved. Never push, never merge, never reset.
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
from pathlib import Path

DEFAULT_TIMEOUT = 20  # seconds per network call; a hook that can hang a session start is worse than none


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
    s = stderr.lower()
    if "terminal prompts disabled" in s or "authentication" in s or "permission denied" in s:
        return "auth-failed"
    return "offline"


def sync_repo(repo: Path, fetch: bool = True, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """One repo's sync outcome: {'repo', 'state', 'detail', 'moved'}.

    States: synced / up-to-date / ahead / diverged / dirty / local-only /
    no-upstream / detached / unborn / in-operation / offline / auth-failed /
    pull-failed. Only 'synced' moves the tree; everything else reports.
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
        f = _git(repo, "fetch", "--quiet", timeout=timeout)
        if f is None:
            out["state"] = "offline"
            out["detail"] = "fetch timed out — orienting from last-fetched state"
        elif f.returncode != 0:
            out["state"] = _classify_fetch_failure(f.stderr)
            out["detail"] = "orienting from last-fetched state"

    counts = _counts(repo)
    if counts is None:
        if out["state"] in ("offline", "auth-failed"):
            return out
        out["state"] = "no-upstream"
        return out
    ahead, behind = counts
    cached = " (cached)" if out["state"] in ("offline", "auth-failed") else ""
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
            out["detail"] = f"+{behind} remote (cached) — pull skipped, fetch failed"
        else:
            p = _git(repo, "pull", "--ff-only", "--quiet", timeout=timeout)
            if p is not None and p.returncode == 0:
                out["state"] = "synced"
                out["detail"] = f"+{behind}"
                out["moved"] = True
            else:
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


_LABEL = {
    "synced": "synced", "up-to-date": "up-to-date", "ahead": "ahead",
    "diverged": "DIVERGED", "dirty": "dirty", "local-only": "local-only",
    "no-upstream": "no-upstream", "detached": "detached", "unborn": "unborn",
    "in-operation": "in-operation", "offline": "offline",
    "auth-failed": "auth-failed", "pull-failed": "pull-failed",
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
    results = [sync_repo(r, fetch=fetch, timeout=args.timeout) for r in repos]
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
        print("\nPublication is yours: review `git log`, then push per repo when satisfied.")
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
