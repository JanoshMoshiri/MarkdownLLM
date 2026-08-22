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

import re
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml

from .git_transport import git_command, redact
from .yaml_loader import load_yaml

DEFAULT_TIMEOUT = 20  # seconds per network call; a hook that can hang a session start is worse than none
ESTATE_GLOBAL_TIMEOUT = 75


class SyncState(str, Enum):
    """Closed vocabulary for one repository's synchronization outcome."""

    SYNCED = "synced"
    UP_TO_DATE = "up-to-date"
    AHEAD = "ahead"
    DIVERGED = "diverged"
    DIRTY = "dirty"
    LOCAL_ONLY = "local-only"
    NO_UPSTREAM = "no-upstream"
    DETACHED = "detached"
    UNBORN = "unborn"
    IN_OPERATION = "in-operation"
    OFFLINE = "offline"
    AUTH_FAILED = "auth-failed"
    PERMISSION_DENIED = "permission-denied"
    FETCH_FAILED = "fetch-failed"
    PULL_FAILED = "pull-failed"
    BUDGET_EXHAUSTED = "budget-exhausted"

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class SyncResult:
    """Immutable observation returned by :func:`sync_repo`."""

    repo: Path
    state: SyncState
    detail: str = ""
    moved: bool = False

    def __post_init__(self) -> None:
        if self.moved and self.state is not SyncState.SYNCED:
            raise ValueError("only a synced result may report repository movement")


_DEGRADED_SYNC_STATES = frozenset({
    SyncState.OFFLINE,
    SyncState.AUTH_FAILED,
    SyncState.PERMISSION_DENIED,
    SyncState.FETCH_FAILED,
    SyncState.BUDGET_EXHAUSTED,
})


def _git(repo: Path, *args: str, timeout: int = DEFAULT_TIMEOUT,
         token: str | None = None):
    """Run git non-interactively; None on timeout (caller treats as offline).

    ``_git`` remains the sync service's focused test seam.  Construction and
    credential handling belong to the neutral Git transport boundary.
    """
    return git_command(
        repo,
        *args,
        timeout=timeout,
        token=token,
        non_interactive=True,
    )


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
    if ("could not resolve host" in s or "connection refused" in s
            or "failed to connect" in s or "could not connect to server" in s
            or "timed out" in s or "network is unreachable" in s
            or "no route to host" in s):
        return "offline"
    if ("terminal prompts disabled" in s or "authentication" in s
            or "permission denied (publickey)" in s
            or "403" in s or "401" in s):
        return "auth-failed"
    if "permission denied" in s or "access is denied" in s:
        return "permission-denied"
    return "fetch-failed"


def _first_stderr_line(stderr: str, token: str | None = None) -> str:
    for line in (stderr or "").splitlines():
        if line.strip():
            return redact(line.strip(), token)[:120]
    return "no stderr"


def sync_repo(repo: Path, fetch: bool = True, timeout: int = DEFAULT_TIMEOUT,
              deadline: float | None = None,
              token: str | None = None) -> SyncResult:
    """Return one immutable, typed repository synchronization observation.

    ``token`` is optional command-scoped authentication. Callers serving
    ephemeral containers may pass the token they already hold; local callers
    leave it ``None`` and use ambient Git authentication.

    States: synced / up-to-date / ahead / diverged / dirty / local-only /
    no-upstream / detached / unborn / in-operation / offline / auth-failed /
    permission-denied / fetch-failed / pull-failed / budget-exhausted. Only
    'synced' moves the tree; everything else reports.
    """
    state = SyncState.UP_TO_DATE
    detail = ""
    moved = False

    def result() -> SyncResult:
        return SyncResult(repo=repo, state=state, detail=detail, moved=moved)

    remotes = _git(repo, "remote")
    if remotes is None or remotes.returncode != 0:
        # `git remote` failing to run is not evidence of "no remote
        # configured": rendering it LOCAL_ONLY diagnosed a broken or
        # timed-out environment as a deliberately unpublished repo — the
        # same empty value for two different questions
        # (substrate-totality-residue sibling).
        state = SyncState.FETCH_FAILED
        detail = "`git remote` could not run — remote configuration unknown"
        return result()
    if not remotes.stdout.strip():
        state = SyncState.LOCAL_ONLY
        return result()

    gitdir_r = _git(repo, "rev-parse", "--git-dir")
    gitdir = repo / (gitdir_r.stdout.strip() if gitdir_r and gitdir_r.returncode == 0 else ".git")
    if any((gitdir / f).exists() for f in ("MERGE_HEAD", "rebase-merge", "rebase-apply")):
        state = SyncState.IN_OPERATION
        detail = "merge/rebase in progress — skipped"
        return result()

    if (r := _git(repo, "rev-parse", "--verify", "-q", "HEAD")) is None or r.returncode != 0:
        state = SyncState.UNBORN
        return result()
    if (r := _git(repo, "symbolic-ref", "-q", "--short", "HEAD")) is None or r.returncode != 0:
        state = SyncState.DETACHED
        detail = "detached HEAD — skipped"
        return result()

    if fetch:
        remaining = ((deadline - time.monotonic())
                     if deadline is not None else float(timeout))
        if remaining <= 0:
            f = None
            state = SyncState.BUDGET_EXHAUSTED
            detail = ("global estate deadline exhausted before fetch "
                      "— orienting from last-fetched state")
        else:
            f = _git(repo, "fetch", "--quiet",
                     timeout=min(float(timeout), remaining), token=token)
        if f is None and state is not SyncState.BUDGET_EXHAUSTED:
            if deadline is not None and time.monotonic() >= deadline:
                state = SyncState.BUDGET_EXHAUSTED
                detail = ("global estate deadline exhausted during "
                          "fetch — orienting from last-fetched state")
            else:
                state = SyncState.OFFLINE
                detail = ("fetch timed out — orienting from "
                          "last-fetched state")
        elif f is not None and f.returncode != 0:
            state = SyncState(_classify_fetch_failure(f.stderr))
            detail = "orienting from last-fetched state"
            if state is SyncState.FETCH_FAILED:
                detail = (
                    f"undiagnosed ({_first_stderr_line(f.stderr, token)}) — "
                    "orienting from last-fetched state")
            elif state is SyncState.PERMISSION_DENIED:
                detail = (
                    "permission denied "
                    f"({_first_stderr_line(f.stderr, token)}) — "
                    "orienting from last-fetched state")

    counts = _counts(repo)
    if counts is None:
        if state in _DEGRADED_SYNC_STATES:
            return result()
        state = SyncState.NO_UPSTREAM
        return result()
    ahead, behind = counts
    cached = " (cached)" if state in _DEGRADED_SYNC_STATES else ""
    degraded = state if cached else None

    dirty = _git(repo, "status", "--porcelain")
    is_dirty = bool(dirty and dirty.stdout.strip())

    if ahead and behind:
        state = SyncState.DIVERGED
        detail = (f"+{ahead} local / +{behind} remote{cached} — "
                  "a decision is owed, not a merge")
    elif behind:
        if is_dirty:
            state = SyncState.DIRTY
            detail = (f"+{behind} remote{cached} — pull skipped, "
                      "working tree not clean")
        elif degraded:
            reason = ("global estate deadline exhausted"
                      if degraded is SyncState.BUDGET_EXHAUSTED
                      else "fetch failed")
            detail = (f"+{behind} remote (cached) — pull skipped, "
                      f"{reason}")
        else:
            remaining = ((deadline - time.monotonic())
                         if deadline is not None else float(timeout))
            if remaining <= 0:
                p = None
                state = SyncState.BUDGET_EXHAUSTED
                detail = (f"+{behind} remote (cached) — pull skipped, "
                          "global estate deadline exhausted")
            else:
                p = _git(repo, "pull", "--ff-only", "--quiet",
                         timeout=min(float(timeout), remaining), token=token)
            if p is not None and p.returncode == 0:
                state = SyncState.SYNCED
                detail = f"+{behind}"
                moved = True
            elif state is not SyncState.BUDGET_EXHAUSTED:
                state = SyncState.PULL_FAILED
                err = ((p.stderr.strip().splitlines() or ["?"])[-1]
                       if p else "timeout")
                detail = redact(err, token)
    elif ahead:
        if not degraded:
            state = SyncState.AHEAD
        detail = f"+{ahead} (unpushed){cached}"
    elif is_dirty:
        # Up to date with the remote but uncommitted work in the tree — not
        # sync's problem to fix, but worth a word at session start.
        if not degraded:
            state = SyncState.DIRTY
        detail = f"working tree not clean{cached}"
    return result()


class PublicationPolicyState(str, Enum):
    """Why the post-commit publication leg is enabled or disabled."""

    LITERAL_TRUE = "literal-true"
    LITERAL_FALSE = "literal-false"
    ABSENT = "absent"
    MALFORMED = "malformed"
    UNREADABLE = "unreadable"


@dataclass(frozen=True)
class PublicationPolicy:
    """One typed, inspectable reading of ``AGENTS.md`` publication authority."""

    enabled: bool
    state: PublicationPolicyState
    reason: str


def publication_policy(repo: Path) -> PublicationPolicy:
    """Read the fail-closed publication authority and preserve its reason.

    Only the YAML boolean ``true`` at ``git.autopush`` enables a send.  The
    distinction between false, absent, malformed, and unreadable is retained
    for diagnostics; collapsing all four to ``False`` made a safe refusal
    operationally opaque.
    """
    agents = repo / "AGENTS.md"
    if not agents.is_file():
        return PublicationPolicy(
            False, PublicationPolicyState.ABSENT,
            "AGENTS.md is absent; no publication authority was declared")
    try:
        text = agents.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return PublicationPolicy(
            False, PublicationPolicyState.UNREADABLE,
            f"AGENTS.md cannot be read as UTF-8 ({exc})")

    if not text.startswith("---"):
        return PublicationPolicy(
            False, PublicationPolicyState.ABSENT,
            "AGENTS.md has no YAML frontmatter; git.autopush is absent")
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|\s*$)", text, re.S)
    if not m:
        return PublicationPolicy(
            False, PublicationPolicyState.MALFORMED,
            "AGENTS.md opens YAML frontmatter but does not close it cleanly")
    try:
        fm = load_yaml(m.group(1), source=agents) or {}
    except yaml.YAMLError as exc:
        return PublicationPolicy(
            False, PublicationPolicyState.MALFORMED,
            f"AGENTS.md frontmatter is invalid YAML ({exc})")
    if not isinstance(fm, dict):
        return PublicationPolicy(
            False, PublicationPolicyState.MALFORMED,
            "AGENTS.md frontmatter must be a YAML mapping")
    if "git" not in fm:
        return PublicationPolicy(
            False, PublicationPolicyState.ABSENT,
            "AGENTS.md has no git mapping; git.autopush is absent")
    git_cfg = fm.get("git")
    if not isinstance(git_cfg, dict):
        return PublicationPolicy(
            False, PublicationPolicyState.MALFORMED,
            "AGENTS.md git must be a YAML mapping")
    if "autopush" not in git_cfg:
        return PublicationPolicy(
            False, PublicationPolicyState.ABSENT,
            "AGENTS.md git.autopush is absent")
    value = git_cfg.get("autopush")
    if value is True:
        return PublicationPolicy(
            True, PublicationPolicyState.LITERAL_TRUE,
            "AGENTS.md git.autopush is the YAML boolean true")
    if value is False:
        return PublicationPolicy(
            False, PublicationPolicyState.LITERAL_FALSE,
            "AGENTS.md git.autopush is the YAML boolean false")
    return PublicationPolicy(
        False, PublicationPolicyState.MALFORMED,
        "AGENTS.md git.autopush must be the YAML boolean true or false "
        f"(got {type(value).__name__})")


def _autopush_enabled(repo: Path) -> bool:
    """Compatibility query; new diagnostics consume ``publication_policy``."""
    return publication_policy(repo).enabled


def autopush_repo(repo: Path, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """The post-commit publication leg: push the current branch to its
    upstream — transport of already-committed, floor-validated state.

    States: off / local-only / detached / unborn / no-upstream / published /
    rejected / offline / auth-failed. Never forces (structurally: --force is
    not in this function's vocabulary), never blocks (the caller exits 0
    regardless), never resolves a rejection — a rejected push is DIVERGED on
    the push side, an unrouted decision the operator routes."""
    out = {"repo": repo, "state": "published", "detail": ""}
    policy = publication_policy(repo)
    if not policy.enabled:
        out["state"] = "off"
        out["detail"] = policy.reason
        return out
    remotes = _git(repo, "remote")
    if remotes is None or remotes.returncode != 0:
        # Same distinction as sync_repo: a failed `git remote` is an unknown
        # publication surface, not a deliberately unpublished repo.
        out["state"] = "failed"
        out["detail"] = "`git remote` could not run — remote configuration unknown"
        return out
    if not remotes.stdout.strip():
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
    # Never delegate publication scope to ambient ``push.default``.  In
    # particular, ``matching`` would publish every matching local branch even
    # though this post-commit hook was authorized by one current commit.  Pin
    # the configured upstream as an exact remote + destination refspec.
    remote = _git(repo, "config", "--get", f"branch.{branch}.remote")
    merge = _git(repo, "config", "--get", f"branch.{branch}.merge")
    if (remote is None or remote.returncode != 0 or not remote.stdout.strip()
            or merge is None or merge.returncode != 0
            or not merge.stdout.strip().startswith("refs/heads/")):
        out["state"] = "no-upstream"
        out["detail"] = (f"branch `{branch}` has no unambiguous branch upstream; "
                         "publication was not attempted")
        return out
    remote_name = remote.stdout.strip()
    merge_ref = merge.stdout.strip()
    p = _git(repo, "push", "--porcelain", "--", remote_name,
             f"HEAD:{merge_ref}", timeout=timeout)
    if p is None:
        out["state"] = "offline"
        out["detail"] = "push timed out — commit stands as publication debt (`mdllm estate-sync --status`)"
        return out
    if p.returncode == 0:
        out["detail"] = f"{branch} -> {remote_name}/{merge_ref.removeprefix('refs/heads/')}"
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
    SyncState.SYNCED: "synced",
    SyncState.UP_TO_DATE: "up-to-date",
    SyncState.AHEAD: "ahead",
    SyncState.DIVERGED: "DIVERGED",
    SyncState.DIRTY: "dirty",
    SyncState.LOCAL_ONLY: "local-only",
    SyncState.NO_UPSTREAM: "no-upstream",
    SyncState.DETACHED: "detached",
    SyncState.UNBORN: "unborn",
    SyncState.IN_OPERATION: "in-operation",
    SyncState.OFFLINE: "offline",
    SyncState.AUTH_FAILED: "auth-failed",
    SyncState.PERMISSION_DENIED: "permission-denied",
    SyncState.PULL_FAILED: "pull-failed",
    SyncState.FETCH_FAILED: "fetch-failed",
    SyncState.BUDGET_EXHAUSTED: "budget-exhausted",
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

    status_only = getattr(args, "status", False)
    require_fresh = getattr(args, "require_fresh", False)
    fetch = not status_only
    title = "Publication Debt" if status_only else "Estate Sync"
    print(f"## {title} — {root.name} ({len(repos)} repo(s))\n")
    deadline = (time.monotonic() + ESTATE_GLOBAL_TIMEOUT) if fetch else None
    # Concurrent per-repo observation: each sync_repo is independent (its own
    # working directory, its own subprocesses, no shared mutable state) and
    # the wall time of a serial walk is the SUM of every repo's network round
    # trip — 14 repos took ~21s serially where the slowest single fetch is
    # ~2s. Results keep the repos' order; the shared deadline still bounds
    # the whole walk.
    from concurrent.futures import ThreadPoolExecutor
    workers = min(8, max(1, len(repos)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(
            lambda r: sync_repo(r, fetch=fetch, timeout=args.timeout,
                                deadline=deadline), repos))
    debt = 0
    for res in results:
        name = res.repo.name
        label = _LABEL[res.state]
        line = f"- `{name}`: {label}"
        if res.detail:
            line += (f" ({res.detail})" if res.state is SyncState.SYNCED
                     else f" — {res.detail}")
        if status_only and res.state not in {
                SyncState.AHEAD, SyncState.DIVERGED, SyncState.DIRTY}:
            continue  # debt view: only what the estate cannot see yet
        print(line)
        if status_only:
            debt += 1
    if status_only:
        if debt == 0:
            print("- nothing unpublished — the estate sees everything committed here")
        print("\nAutopush is fail-closed: only an explicit `git: autopush: true` "
              "publishes after commit. Where it is false, absent, or malformed, "
              "publication stays yours: review `git log`, then push per repo "
              "when satisfied.")
        return 0

    if require_fresh:
        fresh_states = {
            SyncState.SYNCED,
            SyncState.UP_TO_DATE,
            SyncState.AHEAD,
            SyncState.LOCAL_ONLY,
        }
        incomplete = [res for res in results
                      if res.state not in fresh_states]
        if incomplete:
            summary = ", ".join(
                f"{res.repo.name}={_LABEL[res.state]}"
                for res in incomplete)
            print(f"\nFresh sync incomplete: {summary}.")
            print("Cached or unresolved state is not fresh state. In a "
                  "network-restricted harness task, rerun this exact command "
                  "with one-command network/filesystem approval.")
            return 1

    moved = [res.repo for res in results if res.moved]
    diverged = [res.repo.name for res in results
                if res.state is SyncState.DIVERGED]
    if moved:
        roots = " ".join(str(m) for m in moved)
        print(f"\n{len(moved)} repo(s) moved — consider `mdllm estate-check {roots}` "
              f"to re-check the membrane (pulled source commits can flip imports stale/diverged).")
    if diverged:
        print(f"\nDIVERGED: {', '.join(diverged)} — route each as a decision "
              f"(git-workflow.md -> The Machine Axis); never auto-merge.")
    print("\nThis is a batch of per-repo reads — ephemeral, never an index. Sync before orienting.")
    return 0
