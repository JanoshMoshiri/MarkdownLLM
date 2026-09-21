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

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from .git_transport import command_token, git_command, redact
from .model import RESERVED_STATUSES, Corpus, scan
from .repository_view import RepositoryView, RepositoryViewError
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
class _LoopState:
    """Everything that must survive a restart.

    A restart must not re-baseline. A change that landed while the watcher was
    down has to be *reported*, not absorbed — otherwise the one event the
    channel exists to carry is the one it silently eats.
    """

    board: dict[str, str] = field(default_factory=dict)
    last_head: str | None = None
    seen: bool = False


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
    return _LoopState(
        board={str(k): str(v) for k, v in board.items()},
        last_head=raw.get("last_head") or None,
        seen=bool(raw.get("seen")),
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
            "last_head": state.last_head,
            "seen": state.seen,
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

        woke = False
        if not state.seen:
            print(f"baseline: {len(board)} thing(s) on the board at {head[:8]}")
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

        state.board = board
        state.last_head = head
        state.seen = True
        _save_state(state_path, state)

        if woke and config.exit_on_wake:
            return 0
        if config.once:
            return 0
        time.sleep(config.interval)
