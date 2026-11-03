"""`mdllm watch` — the doorbell, as floor rather than as shell.

Two agent instances take turns working one thing to completion. The turn
itself is already substrate-native: it is a `status` field the floor
validates, in a repository both clones sync through. What git does not do is
*wake* the other side. That gap has been filled, in one live domain, by three
bash watchers polling `git ls-remote`.

This is those watchers, in the floor. It adds no transport and moves no
domain content over a wire: it reads the same ref the clones already pull,
and the only thing crossing the network is the question *has the head moved*.

**Why the floor and not a script.** The shell version runs in one session's
shell. A domain running two model families takes its turns from two
harnesses, and the second reaches the floor through `mdllm.ps1`, not bash —
so half the loop could not ring its own doorbell. That is a portability fact,
not a preference (`portability-claims-need-execution-tests`).

**The five decisions below are inherited, each paid for by a defect in the
domain that found them first.** They are not re-derived here; they are
carried, with the failure each prevents named at its site, because a rule
whose reason is lost is a rule the next author deletes.

**What this never does.** It never writes, never commits, never resolves a
divergence, and never advances a turn. It reads a ref, reports a change, and
exits. The turn stays the agent's act and the ruling stays the human's.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from .git_transport import command_token, git_command, redact
from .model import RESERVED_STATUSES, Corpus, scan
from .repository_view import RepositoryView, RepositoryViewError
from .seat import read_seat
from .workflow_actors import declared_actors, stages_for_actor

__all__ = [
    "WatchConfig",
    "lock_path_for",
    "InstanceLock",
    "WatchError",
    "BoardChange",
    "read_board",
    "resolve_remote_head",
    "diff_board",
    "state_path_for",
    "cmd_watch",
]


# Losing more than this many board entries in one poll is treated as a bad
# read rather than as a mass deletion. The sibling recorded a list endpoint
# returning fifteen rows then seven under a success status; a corpus scan can
# do the same thing for a less exotic reason (a partial fetch, a tree read
# against a half-written object).
BAD_READ_LOSS = 2

DEFAULT_INTERVAL = 60.0
POLL_TIMEOUT = 30.0
FETCH_TIMEOUT = 120.0
LOCAL_TIMEOUT = 20.0   # rev-parse / merge-base / rev-list: local reads, never the network


class WatchError(RuntimeError):
    """A condition that must stop the watcher before it starts.

    Raised only at arming time. Once the loop is running, failures are
    *emitted* rather than raised — a blind watcher is a finding, and a
    watcher that exits on a failed poll is indistinguishable from a quiet
    estate, which is the exact failure this command exists to prevent.
    """


@dataclass(frozen=True)
class WatchConfig:
    root: Path
    role: str
    definition_id: str
    remote: str = "origin"
    branch: str = "main"
    field_name: str = "status"
    interval: float = DEFAULT_INTERVAL
    exit_on_wake: bool = False
    once: bool = False
    state_file: Path | None = None
    # The scope: a workflow-run id. When set, the board is only the things
    # that declare they realise this run. The run and `definition_id` are two
    # different definitions by design — the run is the vertical (a subject
    # through its layers), the definition is the horizontal (the turn).
    run_id: str | None = None


@dataclass
class BoardChange:
    """One thing's field moving between two board reads."""

    thing_id: str
    was: str | None
    now: str
    wakes: bool

    def line(self, role: str) -> str:
        if self.wakes:
            return (f"{role.upper()} UP: {self.thing_id} is at "
                    f"'{self.now}' (was {self.was or '(new)'}).")
        return f"moved: {self.thing_id} {self.was or '(new)'} -> {self.now}"


@dataclass
class _Gone:
    thing_id: str
    was: str

    def line(self) -> str:
        return (f"GONE: {self.thing_id} left the board (was {self.was}) — "
                "deleted, renamed, or moved off this definition or run. If "
                "work on it is in flight, stop and check.")


@dataclass
class _Note:
    """A write on a thing at one of this role's stages that did not move the
    turn — a note left on a ticket its addressee holds.

    Until 2026-11-02 this was invisible by design: the board was
    `{thing_id: status}` and `diff_board` skipped `was == now`, so one message
    per turn was floor behaviour and the double-send question was answered
    *no* until a live run showed the need. The first live run that needed it
    handed a ticket to a seat whose next act was the operator's, and the fact
    that seat was waiting for arrived as a note that rang nothing. The
    operator's ruling: the note is an interrupt
    (`a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`).
    """

    thing_id: str
    status: str
    authors: list[tuple[str, str]]
    own: bool
    addressed: bool

    def line(self, role: str, seat_name: str) -> str:
        who = (", ".join(sorted({a[0] or a[1] for a in self.authors}))
               or "an author the record does not show")
        if not self.addressed:
            return (f"body [{role}]: {self.thing_id} changed at '{self.status}' "
                    f"— the holder's own write, not your turn")
        if self.own:
            return (f"noted [{role}]: {self.thing_id} changed at '{self.status}' "
                    f"by this seat (`{seat_name}`) — your own write, not a ring")
        tail = ("" if seat_name else " (seat undeclared, so the watch cannot tell "
                "whether it was yours: `mdllm seat . --set <actor>`)")
        return (f"{role.upper()} UP: a note landed on {self.thing_id} while it is "
                f"addressed to you ('{self.status}') — written by {who} without "
                f"moving the turn; reread it before continuing "
                f"(a-note-on-a-held-ticket-rings-its-addressee-2026-11-02){tail}")


@dataclass
class _LoopState:
    """Everything that must survive a restart.

    A restart must not re-baseline. A change that landed while the watcher was
    down has to be *reported*, not absorbed — otherwise the one event the
    channel exists to carry is the one it silently eats.
    """

    board: dict[str, str] = field(default_factory=dict)
    # What each board thing *said* at the last read — a digest of its bytes,
    # so a write that leaves the status alone is still a change the watch
    # can see (the note).
    content: dict[str, str] = field(default_factory=dict)
    last_head: str | None = None
    seen: bool = False
    # The local tip this watch last rang its own role for — a turn that
    # never left. Once per tip: an agent that has not yet acted is not rung
    # every poll; one that commits again without publishing is rung again.
    woke_unpublished: str | None = None


def state_path_for(config: WatchConfig) -> Path:
    """Per-role, per-definition state — never shared between two watchers.

    Two watchers sharing one state file is not a theoretical hazard: the
    sibling found eight orphaned instances racing on one, each absorbing the
    others' events, so the live watcher saw nothing change and stayed silent.
    Everything keyed here is keyed on both the role and the definition.

    It lives under `.git/` because it is per-clone, never committed, and it
    disappears with the clone it describes.
    """
    if config.state_file is not None:
        return Path(config.state_file)
    slug = f"{config.definition_id}.{config.role}"
    if config.run_id:
        # A third key. Two reviewers on two runs in one clone are two
        # watchers, and they must not share a state file any more than two
        # roles may — the same collision, one axis over.
        slug = f"{slug}.{config.run_id}"
    slug = slug.replace("/", "-")
    return config.root / ".git" / "mdllm-watch" / f"{slug}.json"


def lock_path_for(config: WatchConfig) -> Path:
    """The single-instance guard, keyed exactly as the state file is."""
    return state_path_for(config).with_suffix(".pid")


def _process_alive(pid: int) -> bool:
    """Is this pid a live process?

    Deliberately not `os.kill(pid, 0)` on Windows. Python's `os.kill` there
    does not implement signal 0 as a liveness probe — it routes to
    TerminateProcess, so the "check" would kill the very process it was asking
    about. The Win32 path opens a query-only handle instead.
    """
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        try:
            code = ctypes.c_ulong()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return code.value == STILL_ACTIVE
            return True
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # Alive, owned by someone else. Not ours to take.
        return True
    return True


class InstanceLock:
    """One watcher per (definition, role), per clone.

    The state file is keyed per role, which stops two *different* roles
    colliding. It does not stop two instances of the *same* role, and that is
    the failure the sibling loop actually hit: eight orphaned watchers racing
    on one state file, each absorbing the others' events, so the live one saw
    nothing change and stayed silent. State isolation and single-instance are
    two guarantees, not one.

    A lock whose process is gone is stale and is taken. A watcher killed
    without cleanup must not lock its own role out forever.
    """

    def __init__(self, path: Path):
        self.path = path
        self.held = False

    def holder(self) -> int | None:
        """The live pid holding this lock, or None if free or stale."""
        try:
            raw = self.path.read_text(encoding="utf-8").strip()
        except OSError:
            return None
        try:
            pid = int(raw)
        except ValueError:
            return None
        if pid == os.getpid():
            return None
        return pid if _process_alive(pid) else None

    def acquire(self) -> int | None:
        """Take the lock, or return the live pid that already holds it."""
        other = self.holder()
        if other is not None:
            return other
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(str(os.getpid()), encoding="utf-8")
            self.held = True
        except OSError:
            # A clone whose .git is read-only still deserves a watcher; it
            # just cannot be guarded. Better an unguarded watch than none.
            pass
        return None

    def release(self) -> None:
        if not self.held:
            return
        try:
            if self.path.read_text(encoding="utf-8").strip() == str(os.getpid()):
                self.path.unlink()
        except OSError:
            pass
        self.held = False

    def __enter__(self) -> "InstanceLock":
        return self

    def __exit__(self, *exc) -> None:
        self.release()


def _load_state(path: Path) -> _LoopState:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _LoopState()
    board = raw.get("board")
    if not isinstance(board, dict):
        return _LoopState()
    content = raw.get("content")
    return _LoopState(
        board={str(k): str(v) for k, v in board.items()},
        content=({str(k): str(v) for k, v in content.items()}
                 if isinstance(content, dict) else {}),
        last_head=raw.get("last_head") or None,
        seen=bool(raw.get("seen")),
        woke_unpublished=raw.get("woke_unpublished") or None,
    )


def _save_state(path: Path, state: _LoopState) -> None:
    """Persist before waking, never after.

    The sibling's first version exited from inside its diff loop, so the poll
    that woke the reviewer never persisted what it had seen and every restart
    re-detected the same change — an infinite wake loop. The ordering here is
    the fix and is load-bearing: record, then signal.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "board": state.board,
            "content": state.content,
            "last_head": state.last_head,
            "seen": state.seen,
            "woke_unpublished": state.woke_unpublished,
        }, indent=2, sort_keys=True), encoding="utf-8")
    except OSError:
        # A watcher that cannot persist still watches; it just re-reports on
        # restart. Losing the doorbell over a read-only temp dir would be a
        # worse trade than a duplicate line.
        pass


def resolve_remote_head(config: WatchConfig) -> tuple[str | None, str | None]:
    """One ref read: the whole cost of learning that nothing moved.

    Returns ``(head, error)``. A ref is a single value that is either fetched
    or not, which is why this is cheaper *and* safer than reading a board over
    the wire — there is no partial success to mistake for an empty estate.
    """
    token = command_token()
    result = git_command(
        config.root, "ls-remote", config.remote,
        f"refs/heads/{config.branch}",
        token=token, timeout=POLL_TIMEOUT, non_interactive=True,
    )
    if result is None:
        return None, f"ls-remote timed out after {POLL_TIMEOUT:.0f}s"
    if result.returncode != 0:
        detail = redact((result.stderr or "").strip(), token).splitlines()
        return None, (detail[0] if detail else "ls-remote failed")
    line = (result.stdout or "").strip().splitlines()
    if not line:
        return None, (f"{config.remote} has no refs/heads/{config.branch}")
    return line[0].split()[0], None


def _fetch(config: WatchConfig) -> str | None:
    token = command_token()
    result = git_command(
        config.root, "fetch", config.remote, config.branch,
        token=token, timeout=FETCH_TIMEOUT, non_interactive=True,
    )
    if result is None:
        return f"fetch timed out after {FETCH_TIMEOUT:.0f}s"
    if result.returncode != 0:
        detail = redact((result.stderr or "").strip(), token).splitlines()
        return detail[0] if detail else "fetch failed"
    return None


def _local_ref(root: Path, ref: str) -> str | None:
    r = git_command(root, "rev-parse", "--verify", "-q", ref, timeout=LOCAL_TIMEOUT)
    if r is None or r.returncode != 0:
        return None
    return r.stdout.strip() or None


def _object_known(root: Path, sha: str) -> bool:
    r = git_command(root, "cat-file", "-e", f"{sha}^{{commit}}", timeout=LOCAL_TIMEOUT)
    return r is not None and r.returncode == 0


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    r = git_command(root, "merge-base", "--is-ancestor", ancestor, descendant,
                    timeout=LOCAL_TIMEOUT)
    return r is not None and r.returncode == 0


def local_publication_state(config: WatchConfig,
                            remote_head: str) -> tuple[str, str | None]:
    """Where this clone's own branch stands against the ref it watches.

    `published` (equal), `behind`, `unpublished` (local ahead: a turn that
    never left), `diverged` (both moved), `absent` (no local branch of that
    name), or `unknown` (the remote head is not in this clone's objects yet,
    so ancestry cannot be read — never guessed as divergence). The one local
    read the watch makes, and it reads refs, never the worktree. It exists
    for the one failure the remote ref cannot show: a commit that succeeded
    while its push was rejected leaves this side holding every local sign of
    a handover and the other side seeing nothing
    (loop-turns-self-heal-2026-09-23).
    """
    local = _local_ref(config.root, f"refs/heads/{config.branch}")
    if local is None:
        return "absent", None
    if local == remote_head:
        return "published", local
    if not _object_known(config.root, remote_head):
        return "unknown", local
    if _is_ancestor(config.root, remote_head, local):
        return "unpublished", local
    if _is_ancestor(config.root, local, remote_head):
        return "behind", local
    return "diverged", local


def _unpublished_authors(config: WatchConfig, head: str,
                         local: str) -> list[tuple[str, str]]:
    """(name, email) of each commit the remote lacks, newest first. One git
    spawn over the unpublished range only."""
    r = git_command(config.root, "log", "--format=%an%x1f%ae", f"{head}..{local}",
                    timeout=LOCAL_TIMEOUT)
    if r is None or r.returncode != 0:
        return []
    out = []
    for line in (r.stdout or "").splitlines():
        name, _, email = line.partition("\x1f")
        if name.strip() or email.strip():
            out.append((name.strip(), email.strip().lower()))
    return out


def _own_commits(authors: list[tuple[str, str]], seat: dict) -> list[tuple[str, str]]:
    """The commits a declared seat made: author name equals the seat's name,
    or author email equals the identity the seat declaration set."""
    if not seat.get("name"):
        return list(authors)
    name = seat["name"].strip().lower()
    email = (seat.get("user_email") or "").strip().lower()
    return [a for a in authors
            if a[0].strip().lower() == name or (email and a[1] == email)]


def _self_wake(config: WatchConfig, head: str, state: _LoopState,
               state_path: Path) -> bool:
    """Ring this role for its own turn that never left — once per local tip.

    The floor reports and never resolves: the pull, the merge and the push
    are the agent's, and a merge it cannot make cleanly is filed to the seat.
    Record, then signal: the state is saved before the line is printed, so a
    restart does not ring twice for one tip.
    """
    kind, local = local_publication_state(config, head)
    if kind in ("unpublished", "diverged"):
        if state.woke_unpublished == local:
            return False
        authors = _unpublished_authors(config, head, local)
        ahead = str(len(authors)) if authors else "?"
        state.woke_unpublished = local
        _save_state(state_path, state)
        moved = " and the remote moved under it" if kind == "diverged" else ""
        # Whose turn never left? In a shared checkout the branch is ahead
        # whenever ANY party committed without publishing, and the four false
        # wakes on record (in-a-shared-checkout-ahead-of-origin-says-nothing-
        # about-whose-turn-it-is) each exited a watch for someone else's
        # commit, leaving the next real turn with no watch running. The seat
        # is the author the record can now tell apart (the-seat Phase 1): a
        # declared seat is rung only for its own commits; another party's are
        # reported once per tip and never ring. An undeclared seat is rung as
        # before, told why the watch cannot narrow it.
        seat = read_seat(config.root)
        own = _own_commits(authors, seat)
        if seat["name"] and authors and not own:
            names = ", ".join(sorted({a for a, _ in authors})) or "unknown"
            print(f"not your turn [{config.role}]: local {config.branch} is "
                  f"{ahead} commit(s) ahead of {config.remote}/{config.branch}"
                  f"{moved} ({kind}), none of them this seat's (`{seat['name']}`); "
                  f"authored by {names}. A shared checkout holds another party's "
                  f"unpublished work — a routing question for the operator, not a "
                  f"turn for you to repair; this watch stays armed "
                  f"(in-a-shared-checkout-ahead-of-origin-says-nothing-about-whose-"
                  f"turn-it-is)")
            return False
        whose = ""
        if seat["name"] and authors:
            whose = (f" {len(own)} of them this seat's (`{seat['name']}`);"
                     if len(own) != len(authors) else "")
        elif not seat["name"]:
            whose = (" (seat undeclared, so the watch cannot tell whose: "
                     "`mdllm seat . --set <actor>`)")
        print(f"{config.role.upper()} UP: your last turn never left — local "
              f"{config.branch} is {ahead} commit(s) ahead of "
              f"{config.remote}/{config.branch}{moved} ({kind}).{whose} Pull, merge, "
              f"push again; a merge you cannot make cleanly goes to the seat, "
              f"not to a guess. (loop-turns-self-heal-2026-09-23)")
        return True
    if state.woke_unpublished is not None and kind in ("published", "behind"):
        state.woke_unpublished = None
        _save_state(state_path, state)
        print(f"published [{config.role}]: the turn that had not left is on "
              f"{config.remote}/{config.branch} now")
    return False


def _realises(meta: dict, run_id: str) -> bool:
    """Does this thing declare itself the realisation of ``run_id``?

    Membership is the edge `linked_things: {id: <run>, relation: implements}`
    and no other (`workflow-state.md` → Activation and Fulfilment →
    Membership; ruled in `run-membership-is-realisation-2026-09-22`). It is
    deliberately not `informed_by`: that says where a thing *came from*, and
    a thing produced under one run can be the realisation of another.
    """
    for link in meta.get("linked_things") or []:
        if not isinstance(link, dict):
            continue
        if link.get("id") == run_id and link.get("relation") == "implements":
            return True
    return False


def read_board(
    corpus: Corpus, config: WatchConfig, stage_ids: set[str],
) -> dict[str, str]:
    """The things currently sitting at one of this definition's stages.

    Deliberately read from an immutable commit view, never the worktree. The
    worktree is whatever the local session is mid-edit on, and a turn read
    from it is a turn that has not happened yet — the distinction between a
    draft and the estate's state.

    **Reserved types are never on a status-keyed board.** A reserved type's
    status vocabulary is the tool's own lifecycle, and it collides: a
    `workflow-definition` sitting at `draft` would otherwise appear on the
    board of a loop whose first stage is also called `draft` — including its
    own. A tool-owned lifecycle is never a domain's turn token, so the two
    are separated here rather than left to every definition to avoid by
    choosing non-colliding stage names.
    """
    board: dict[str, str] = {}
    watching_status = config.field_name == "status"
    for thing in corpus.things:
        if not thing.id:
            continue
        if watching_status and str(thing.meta.get("type")) in RESERVED_STATUSES:
            continue
        if config.run_id and not _realises(thing.meta, config.run_id):
            continue
        value = thing.meta.get(config.field_name)
        if isinstance(value, str) and value in stage_ids:
            board[thing.id] = value
    return board


def read_content(
    corpus: Corpus, board: dict[str, str],
) -> tuple[dict[str, str], dict[str, Path]]:
    """A digest of each board thing's bytes, and where it lives — read from
    the same commit view as the board, never the worktree."""
    content: dict[str, str] = {}
    paths: dict[str, Path] = {}
    for thing in corpus.things:
        if thing.id not in board:
            continue
        raw = thing.source_text if thing.source_text is not None else thing.body
        content[thing.id] = hashlib.sha1(raw.encode("utf-8", "replace")).hexdigest()
        paths[thing.id] = thing.path
    return content, paths


def diff_notes(
    previous_board: dict[str, str], board: dict[str, str],
    previous_content: dict[str, str], content: dict[str, str],
    wake_stages: set[str],
) -> list[tuple[str, str, bool]]:
    """(thing_id, status, addressed) for each thing whose bytes changed while
    its status did not. `addressed` is whether that status is one this role
    acts at — the note that rings — as against the holder's own write at a
    stage that is not this role's, which does not."""
    out: list[tuple[str, str, bool]] = []
    for thing_id, now in sorted(board.items()):
        if previous_board.get(thing_id) != now:
            continue
        before = previous_content.get(thing_id)
        if before is None or before == content.get(thing_id):
            continue
        out.append((thing_id, now, now in wake_stages))
    return out


def _note_authors(config: WatchConfig, since: str | None, head: str,
                  path: Path) -> list[tuple[str, str]]:
    """(name, email) of each commit between the last read and this one that
    touched `path`, newest first. Empty when git cannot say — and an unknown
    author is rung, never assumed to be this seat."""
    if not since:
        return []
    try:
        rel = Path(path).resolve().relative_to(config.root.resolve()).as_posix()
    except ValueError:
        rel = Path(path).as_posix()
    r = git_command(config.root, "log", "--format=%an%x1f%ae", f"{since}..{head}",
                    "--", rel, timeout=LOCAL_TIMEOUT)
    if r is None or r.returncode != 0:
        return []
    out = []
    for line in (r.stdout or "").splitlines():
        name, _, email = line.partition("\x1f")
        if name.strip() or email.strip():
            out.append((name.strip(), email.strip().lower()))
    return out


def diff_board(
    previous: dict[str, str], current: dict[str, str], wake_stages: set[str],
) -> tuple[list[BoardChange], list[_Gone]]:
    """What moved, and which of it is this role's turn.

    The *previous* value is the discriminator, not the current one. A thing
    arriving at `draft` is an author creating it; `review -> draft` is a
    reviewer sending it back. Those are different events and only one of them
    is a turn.
    """
    changes: list[BoardChange] = []
    for thing_id, now in sorted(current.items()):
        was = previous.get(thing_id)
        if was == now:
            continue
        changes.append(BoardChange(
            thing_id=thing_id, was=was, now=now, wakes=now in wake_stages))
    gone = [_Gone(thing_id=t, was=v)
            for t, v in sorted(previous.items()) if t not in current]
    return changes, gone


def _resolve_definition(config: WatchConfig) -> tuple[dict, set[str], set[str]]:
    """Arm-time resolution: the definition, its stage set, and this role's.

    Every refusal below is a watcher that would otherwise have run forever
    without ever waking — the silent failure mode, which is worse than a loud
    one because a hung watcher and a quiet estate look identical.
    """
    corpus, _ = scan(config.root, RepositoryView.worktree(config.root))
    definition = corpus.by_id().get(config.definition_id)
    if definition is None:
        raise WatchError(
            f"no thing with id `{config.definition_id}` in {config.root}")
    if str(definition.meta.get("type")) != "workflow-definition":
        raise WatchError(
            f"`{config.definition_id}` is a "
            f"`{definition.meta.get('type')}`, not a workflow-definition")

    if config.run_id:
        # The scope must be a run that exists. Deliberately *not* checked:
        # that the run instances `definition_id`. It usually will not — the
        # run is the vertical (a lifecycle, a subject through its layers) and
        # the definition is the horizontal (the turn on one artefact), and a
        # watch reads the horizontal's stages for the vertical's members.
        run = corpus.by_id().get(config.run_id)
        if run is None:
            raise WatchError(
                f"no thing with id `{config.run_id}` in {config.root} to "
                "scope to")
        if str(run.meta.get("type")) != "workflow-run":
            raise WatchError(
                f"`{config.run_id}` is a `{run.meta.get('type')}`, not a "
                "workflow-run — a watch is scoped to a run, never to a thing")

    stage_ids = {
        str(stage["id"])
        for stage in definition.meta.get("stages") or []
        if isinstance(stage, dict) and isinstance(stage.get("id"), str)
    }
    if not stage_ids:
        raise WatchError(
            f"`{config.definition_id}` declares no stages to watch")

    actors = declared_actors(definition.meta)
    if not actors:
        raise WatchError(
            f"`{config.definition_id}` declares no `stages[].actor`, so there "
            "is no role to watch for — declare who acts at each stage "
            "(workflow-state.md)")
    wake_stages = set(stages_for_actor(definition.meta, config.role))
    if not wake_stages:
        raise WatchError(
            f"`{config.definition_id}` declares no stage with "
            f"`actor: {config.role}` — declared actors are "
            f"{sorted(actors)}")

    # The guard that turns a never-waking watcher into a startup error. It
    # compares the role's wake values against the *declared* status
    # vocabulary, never against the values things currently hold: a reviewer
    # arms precisely when nothing is at `review` yet, so an observed-value
    # guard would refuse the normal case and fire only on the abnormal one.
    #
    # What it does catch is a definition whose stage ids and the watched
    # field's vocabulary disagree — `reviewing` against a vocabulary that
    # says `review`. That watcher polls forever in silence, which is
    # indistinguishable from a healthy estate: the mirror of
    # `a-check-that-always-fires-teaches-the-operator-to-ignore-it`, a check
    # that can never fire.
    declarable = _declarable_statuses(corpus, config.field_name)
    if declarable and not (wake_stages & declarable):
        raise WatchError(
            f"no declared `{config.field_name}` vocabulary contains "
            f"{sorted(wake_stages)} — this watcher could never wake. The "
            f"definition's stage ids and the domain's declared statuses "
            f"disagree; reconcile them before arming "
            f"(declared: {sorted(declarable)[:12]})")
    return definition.meta, stage_ids, wake_stages


def _declarable_statuses(corpus: Corpus, field_name: str) -> set[str]:
    """Every status value any type in this corpus is permitted to hold.

    Only meaningful for the `status` field. A domain carrying its turn on a
    `workflow-run` cursor watches `current_stage`, whose permitted values are
    the definition's own stage ids by construction — the guard would be
    vacuous, so it stays quiet rather than inventing a vocabulary to check
    against.

    An empty result also means quiet: absence of a declaration is absence of
    evidence, not evidence of a mismatch.
    """
    if field_name != "status":
        return set()
    declared: set[str] = set()
    for statuses in RESERVED_STATUSES.values():
        declared.update(statuses)
    types = ((corpus.schema or {}).get("types") or {})
    for definition in types.values():
        if isinstance(definition, dict) and isinstance(
                definition.get("statuses"), list):
            declared.update(str(s) for s in definition["statuses"])
    return declared


def cmd_watch(args) -> int:
    root = Path(getattr(args, "path", ".") or ".").resolve()
    config = WatchConfig(
        root=root,
        role=args.role,
        definition_id=args.definition,
        remote=getattr(args, "remote", "origin") or "origin",
        branch=getattr(args, "branch", "main") or "main",
        field_name=getattr(args, "field", "status") or "status",
        interval=float(getattr(args, "interval", DEFAULT_INTERVAL)),
        exit_on_wake=bool(getattr(args, "exit_on_wake", False)),
        once=bool(getattr(args, "once", False)),
        state_file=(Path(args.state) if getattr(args, "state", None) else None),
        run_id=(getattr(args, "run", None) or None),
    )

    try:
        _, stage_ids, wake_stages = _resolve_definition(config)
    except WatchError as exc:
        print(f"mdllm watch: {exc}")
        return 2
    except RepositoryViewError as exc:
        print(f"mdllm watch: {exc}")
        return 2

    lock = InstanceLock(lock_path_for(config))
    other = lock.acquire()
    if other is not None:
        # Exit 3, not 0. A harness bound to `--exit-on-wake` re-invokes on
        # exit, so returning 0 here would read as "your turn" and wake an
        # agent for a doorbell that never rang. A refusal to double-arm is
        # its own outcome and gets its own code.
        print(f"mdllm watch: already watching `{config.definition_id}` as "
              f"[{config.role}] in this clone (pid {other}) — not starting a "
              "second. Two instances of one role race on one state file and "
              "absorb each other's events.")
        return 3

    try:
        return _watch_loop(config, stage_ids, wake_stages)
    finally:
        lock.release()


def _watch_loop(config: WatchConfig, stage_ids: set[str],
                wake_stages: set[str]) -> int:
    state_path = state_path_for(config)
    state = _load_state(state_path)
    resumed = state.seen

    scope = (f" scoped to run `{config.run_id}`" if config.run_id
             else " (unscoped — every stream on this board)")
    print(f"watching `{config.definition_id}` as [{config.role}]{scope} on "
          f"{config.remote}/{config.branch} every {config.interval:.0f}s; "
          f"waking on {config.field_name} in {sorted(wake_stages)}; "
          "silence means nothing moved")
    if resumed:
        print(f"resumed [{config.role}] from {len(state.board)} known "
              "board entr(ies)")

    failures = 0
    while True:
        head, error = resolve_remote_head(config)
        if head is None:
            failures += 1
            # Emitted, never absorbed. A watcher that goes blind and says
            # nothing is reporting health it cannot see.
            if failures == 1 or failures % 10 == 0:
                print(f"WATCHER BLIND [{config.role}] (poll {failures}): {error}")
            if config.once:
                return 1
            time.sleep(config.interval)
            continue
        if failures:
            print(f"WATCHER RECOVERED [{config.role}] after {failures} "
                  "failed poll(s)")
            failures = 0

        if state.last_head == head:
            # Nothing moved on the ref — the one case where this clone's own
            # turn that never left would otherwise be silence.
            if _self_wake(config, head, state, state_path) and config.exit_on_wake:
                return 0
            if config.once:
                return 0
            time.sleep(config.interval)
            continue

        fetch_error = _fetch(config)
        if fetch_error is not None:
            print(f"WATCHER BLIND [{config.role}]: {fetch_error} "
                  f"at head {head[:8]}")
            if config.once:
                return 1
            time.sleep(config.interval)
            continue

        try:
            view = RepositoryView.commit(config.root, head)
            corpus, _ = scan(config.root, view)
        except RepositoryViewError as exc:
            print(f"WATCHER BLIND [{config.role}]: {exc}")
            if config.once:
                return 1
            time.sleep(config.interval)
            continue

        board = read_board(corpus, config, stage_ids)
        content, paths = read_content(corpus, board)

        # The bad-read guard is the *threshold*, never emptiness on its own.
        # An earlier version also refused any board that went from populated
        # to empty; that was written when a board was a whole corpus. A
        # run-scoped board is often one thing, and that one thing moving to
        # another run empties it legitimately — a departure the next watch
        # sees arrive. Refusing it would silence exactly the event the scope
        # exists to carry. What a bad read looks like is an implausible
        # collapse, and the threshold below already catches that.
        lost = len(state.board) - len(board)
        if state.seen and lost > BAD_READ_LOSS:
            print(f"BAD READ ignored [{config.role}]: board lost {lost} "
                  "entr(ies) in one poll — not diffed")
            if config.once:
                return 1
            time.sleep(config.interval)
            continue

        woke = _self_wake(config, head, state, state_path)
        if not state.seen:
            print(f"baseline: {len(board)} thing(s) on the board at {head[:8]}")
            # Content is baselined with the board. A state file written
            # before content was kept has no digest for a thing, and the
            # first poll after it reports nothing for that thing: a note
            # older than the state is the seat read's to report.
        else:
            changes, gone = diff_board(state.board, board, wake_stages)
            for change in changes:
                print(change.line(config.role))
                woke = woke or change.wakes
            for missing in gone:
                # The analogue of the sibling's vanished line: the event that
                # must stop anything in flight, for any role.
                print(missing.line())
                woke = True
            notes = diff_notes(state.board, board, state.content, content,
                               wake_stages)
            seat = read_seat(config.root) if notes else {}
            for thing_id, status, addressed in notes:
                authors = (_note_authors(config, state.last_head, head,
                                         paths[thing_id])
                           if addressed and thing_id in paths else [])
                # Own only when the seat is declared and every author is it.
                # No author on record is rung: the one event the channel
                # exists to carry is not absorbed on a guess.
                own = (bool(seat.get("name")) and bool(authors)
                       and len(_own_commits(authors, seat)) == len(authors))
                note = _Note(thing_id=thing_id, status=status, authors=authors,
                             own=own, addressed=addressed)
                print(note.line(config.role, seat.get("name", "")))
                woke = woke or (addressed and not own)

        state.board = board
        state.content = content
        state.last_head = head
        state.seen = True
        _save_state(state_path, state)

        if woke and config.exit_on_wake:
            return 0
        if config.once:
            return 0
        time.sleep(config.interval)
