"""`mdllm watch` — the doorbell.

The behaviour worth pinning is not "it polls". It is the set of refusals and
the diff semantics, because every one of them corresponds to a way the shell
version of this failed in the domain that wrote it first:

* a watcher armed against a role nothing declares, or against stage values
  the watched field can never take, must refuse **at arming time** — a
  watcher that could never wake is indistinguishable from a quiet estate;
* the *previous* value discriminates a turn from a creation;
* state persists before a wake, and a restart resumes rather than
  re-baselines;
* a board that shrinks implausibly is a bad read, not a mass deletion;
* a failed poll is an emitted event, never silence.

Network is never touched: `resolve_remote_head` and `_fetch` are the only
seams that would, and the loop tests stub them.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import watch as watch_mod  # noqa: E402
from markdownllm.watch import (  # noqa: E402
    BoardChange,
    WatchConfig,
    WatchError,
    diff_board,
    state_path_for,
)

from corpus_harness import _sync_git, thing_text, write  # noqa: E402


DEFINITION = {
    "id": "spec-loop",
    "type": "workflow-definition",
    "status": "draft",
    "created": "2026-09-19",
    "stages": [
        {"id": "draft", "to": ["review"], "actor": "writer"},
        {"id": "review", "to": ["draft", "cleared"], "actor": "reviewer"},
        {"id": "cleared", "to": ["ruling"], "actor": "writer"},
        {"id": "ruling", "to": ["approved"], "actor": "cto"},
        {"id": "approved", "to": []},
    ],
}


def _write(root: Path, meta: dict) -> None:
    write(root, f"things/{meta['id']}.md",
          thing_text(yaml.safe_dump(meta, sort_keys=False)))


def _schema(root: Path) -> None:
    write(root, "_schema.yaml", yaml.safe_dump({
        "schema_version": 1,
        "domain": "watch-fixture",
        "types": {"design-spec": {
            "statuses": ["draft", "review", "cleared", "ruling", "approved"],
            "terminal_statuses": ["approved"],
        }},
    }, sort_keys=False))


def _spec(thing_id: str, status: str) -> dict:
    return {"id": thing_id, "type": "design-spec", "status": status,
            "created": "2026-09-19"}


@pytest.fixture
def board(tmp_path: Path) -> Path:
    _schema(tmp_path)
    _write(tmp_path, DEFINITION)
    _write(tmp_path, _spec("m04-design", "draft"))
    return tmp_path


def _config(root: Path, **kw) -> WatchConfig:
    base = dict(root=root, role="reviewer", definition_id="spec-loop",
                once=True, interval=0.0,
                state_file=root / ".watch-state.json")
    base.update(kw)
    return WatchConfig(**base)


class _Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _args(root: Path, **kw):
    base = dict(path=str(root), role="reviewer", definition="spec-loop",
                field="status", remote="origin", branch="main",
                interval=0.0, exit_on_wake=False, once=True,
                state=str(root / ".watch-state.json"))
    base.update(kw)
    return _Args(**base)


class TestArmingRefusals:
    """Every refusal here is a watcher that would otherwise never wake."""

    def test_unknown_definition_id_refuses(self, board, capsys):
        assert watch_mod.cmd_watch(_args(board, definition="nope")) == 2
        assert "no thing with id `nope`" in capsys.readouterr().out

    def test_a_non_definition_refuses(self, board, capsys):
        assert watch_mod.cmd_watch(_args(board, definition="m04-design")) == 2
        assert "not a workflow-definition" in capsys.readouterr().out

    def test_a_role_no_stage_declares_refuses_and_names_the_declared_set(
            self, board, capsys):
        assert watch_mod.cmd_watch(_args(board, role="builder")) == 2
        out = capsys.readouterr().out
        assert "actor: builder" in out
        assert "cto" in out and "reviewer" in out and "writer" in out

    def test_a_definition_with_no_actors_refuses(self, tmp_path, capsys):
        _schema(tmp_path)
        _write(tmp_path, {**DEFINITION,
                          "stages": [{"id": "draft", "to": []}]})
        _write(tmp_path, _spec("m04-design", "draft"))
        assert watch_mod.cmd_watch(_args(tmp_path)) == 2
        assert "declares no `stages[].actor`" in capsys.readouterr().out

    def test_stage_ids_the_field_can_never_take_refuse(self, tmp_path, capsys):
        """The engineering-loop mismatch, caught at arming.

        A definition whose stage is `reviewing` while the watched field's
        vocabulary says `review` produces a watcher that polls forever in
        silence. That is the exact failure mode the loop fears most, so it is
        a startup error rather than a runtime quiet.
        """
        _schema(tmp_path)
        _write(tmp_path, {**DEFINITION, "stages": [
            {"id": "drafting", "to": ["reviewing"], "actor": "writer"},
            {"id": "reviewing", "to": [], "actor": "reviewer"},
        ]})
        _write(tmp_path, _spec("m04-design", "draft"))
        assert watch_mod.cmd_watch(_args(tmp_path)) == 2
        out = capsys.readouterr().out
        assert "could never wake" in out
        assert "reviewing" in out

    def test_a_well_armed_watcher_reports_what_it_will_wake_on(
            self, board, capsys, monkeypatch):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (None, "offline"))
        watch_mod.cmd_watch(_args(board))
        out = capsys.readouterr().out
        assert "as [reviewer]" in out
        assert "['review']" in out


class TestDiffSemantics:
    def test_the_previous_value_discriminates_a_turn_from_a_creation(self):
        changes, _ = diff_board({}, {"s": "review"}, {"review"})
        assert changes == [BoardChange("s", None, "review", True)]
        assert "(new)" in changes[0].line("reviewer")

    def test_a_return_to_a_stage_this_role_does_not_act_at_is_not_a_turn(self):
        changes, _ = diff_board({"s": "review"}, {"s": "draft"}, {"review"})
        assert [c.wakes for c in changes] == [False]
        assert changes[0].line("reviewer").startswith("moved:")

    def test_an_unchanged_board_yields_nothing(self):
        assert diff_board({"s": "review"}, {"s": "review"}, {"review"}) == ([], [])

    def test_a_thing_leaving_the_board_is_reported(self):
        _, gone = diff_board({"s": "review"}, {}, {"review"})
        assert [g.thing_id for g in gone] == ["s"]
        assert "GONE" in gone[0].line()


class TestStateIsolation:
    def test_state_is_keyed_by_role_and_definition(self, tmp_path):
        a = state_path_for(_config(tmp_path, role="writer", state_file=None))
        b = state_path_for(_config(tmp_path, role="reviewer", state_file=None))
        assert a != b
        assert ".git" in a.parts and "writer" in a.name and "reviewer" in b.name

    def test_an_explicit_state_file_wins(self, tmp_path):
        target = tmp_path / "custom.json"
        assert state_path_for(_config(tmp_path, state_file=target)) == target


class TestLoopBehaviour:
    """The loop, with the two network seams stubbed."""

    @pytest.fixture(autouse=True)
    def _no_network(self, monkeypatch):
        monkeypatch.setattr(watch_mod, "_fetch", lambda c: None)

    def _head(self, monkeypatch, sha):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (sha, None))

    def _commit_view_over_worktree(self, monkeypatch, root):
        """Read the worktree while claiming to be a commit view.

        The loop's contract is that it reads an immutable view; these tests
        exercise the *diff and state* half, so the view seam is stubbed to the
        worktree rather than building real commits for each fixture.
        """
        from markdownllm.repository_view import RepositoryView
        monkeypatch.setattr(RepositoryView, "commit",
                            classmethod(lambda cls, r, rev: cls.worktree(r)))

    def test_a_failed_poll_is_emitted_not_silent(self, board, capsys, monkeypatch):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (None, "Repository not found"))
        assert watch_mod.cmd_watch(_args(board)) == 1
        out = capsys.readouterr().out
        assert "WATCHER BLIND" in out and "Repository not found" in out

    def test_first_poll_baselines_and_does_not_wake(
            self, board, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        assert watch_mod.cmd_watch(_args(board, exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "baseline: 1 thing(s)" in out
        assert "REVIEWER UP" not in out

    def test_a_turn_wakes_after_the_baseline(self, board, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))          # baseline
        capsys.readouterr()

        _write(board, _spec("m04-design", "review"))
        self._head(monkeypatch, "b" * 40)
        assert watch_mod.cmd_watch(_args(board, exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "REVIEWER UP: m04-design is at 'review' (was draft)" in out

    def test_an_unmoved_head_costs_no_board_read(
            self, board, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        capsys.readouterr()

        def _explode(cls, r, rev):  # pragma: no cover - must not be reached
            raise AssertionError("unchanged head must not trigger a tree read")
        from markdownllm.repository_view import RepositoryView
        monkeypatch.setattr(RepositoryView, "commit", classmethod(_explode))
        assert watch_mod.cmd_watch(_args(board)) == 0

    def test_state_persists_before_the_wake_so_a_restart_does_not_repeat(
            self, board, capsys, monkeypatch):
        """The infinite re-wake loop the sibling's first version shipped."""
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        _write(board, _spec("m04-design", "review"))
        self._head(monkeypatch, "b" * 40)
        watch_mod.cmd_watch(_args(board, exit_on_wake=True))
        capsys.readouterr()

        # Same head, restarted watcher: the turn was already recorded.
        assert watch_mod.cmd_watch(_args(board, exit_on_wake=True)) == 0
        assert "REVIEWER UP" not in capsys.readouterr().out

    def test_a_change_landing_while_down_is_reported_not_absorbed(
            self, board, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        capsys.readouterr()

        # The watcher is "down" here; the board moves anyway.
        _write(board, _spec("m04-design", "review"))
        self._head(monkeypatch, "c" * 40)
        watch_mod.cmd_watch(_args(board, exit_on_wake=True))
        out = capsys.readouterr().out
        assert "resumed [reviewer]" in out
        assert "REVIEWER UP" in out

    def test_an_implausible_shrink_is_a_bad_read(
            self, board, capsys, monkeypatch):
        for n in range(4):
            _write(board, _spec(f"spec-{n}", "draft"))
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        capsys.readouterr()

        for n in range(4):
            (board / "things" / f"spec-{n}.md").unlink()
        self._head(monkeypatch, "d" * 40)
        assert watch_mod.cmd_watch(_args(board)) == 1
        assert "BAD READ ignored" in capsys.readouterr().out

    def test_a_one_thing_board_emptying_is_a_departure_not_a_bad_read(
            self, board, capsys, monkeypatch):
        """Changed on 2026-09-22 when the scope landed.

        This test once asserted the opposite: any populated→empty read was a
        bad read. That was true of a board that is a whole corpus. A
        run-scoped board is often one thing, and that thing leaving is the
        event the watch exists to report. The bad-read guard is the
        threshold (`test_an_implausible_shrink_is_a_bad_read`), not emptiness.
        """
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        capsys.readouterr()

        (board / "things" / "m04-design.md").unlink()
        self._head(monkeypatch, "e" * 40)
        assert watch_mod.cmd_watch(_args(board, exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "GONE: m04-design" in out
        assert "bad read" not in out

    def test_the_definition_is_not_on_its_own_board(
            self, board, capsys, monkeypatch):
        """A reserved type's status is a lifecycle, never a turn.

        `spec-loop` is a workflow-definition at `status: draft`, and `draft`
        is one of its own stage ids. Without the reserved-type exclusion it
        appears on the board it defines — and every later diff counts it.
        """
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        assert "baseline: 1 thing(s)" in capsys.readouterr().out

    def test_watch_never_writes_to_the_corpus(self, board, monkeypatch):
        before = {p: p.read_bytes()
                  for p in (board / "things").rglob("*.md")}
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        after = {p: p.read_bytes() for p in (board / "things").rglob("*.md")}
        assert before == after


class TestRealRemoteTurn:
    """The one path the stubs above cannot reach.

    Every test in `TestLoopBehaviour` replaces `RepositoryView.commit` with a
    worktree read, so the loop's diff and state semantics are pinned but its
    actual reading surface is not. This class builds a bare remote and two
    clones and takes one real turn across them — the shape the loop runs in,
    where the two instances share nothing but the ref.
    """

    STAGES = [
        {"id": "draft", "to": ["review"], "actor": "writer"},
        {"id": "review", "to": ["draft", "cleared"], "actor": "reviewer"},
        {"id": "cleared", "to": ["ruling"], "actor": "writer"},
        {"id": "ruling", "to": ["approved"], "actor": "cto"},
        {"id": "approved", "to": []},
    ]

    @pytest.fixture
    def clones(self, tmp_path):
        bare = tmp_path / "origin.git"
        _sync_git(tmp_path, "init", "-q", "--bare", str(bare))
        _sync_git(tmp_path, "--git-dir", str(bare),
                  "symbolic-ref", "HEAD", "refs/heads/main")
        writer = tmp_path / "writer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(writer))
        _sync_git(writer, "checkout", "-q", "-b", "main")
        _schema(writer)
        _write(writer, {**DEFINITION, "stages": self.STAGES})
        _write(writer, _spec("m04-design", "draft"))
        _sync_git(writer, "add", "-A")
        _sync_git(writer, "commit", "-q", "-m", "create: the board")
        _sync_git(writer, "push", "-q", "-u", "origin", "main")

        reviewer = tmp_path / "reviewer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(reviewer))
        _sync_git(reviewer, "checkout", "-q", "-b", "main", "origin/main")
        return writer, reviewer

    def _watch(self, root, role, **kw):
        return watch_mod.cmd_watch(_args(root, role=role, **kw))

    def test_a_turn_crosses_two_clones_through_the_ref_alone(
            self, clones, capsys):
        writer, reviewer = clones

        assert self._watch(reviewer, "reviewer") == 0
        assert "baseline: 1 thing(s)" in capsys.readouterr().out

        # Nothing has moved: the cheap poll must not report a turn.
        assert self._watch(reviewer, "reviewer", exit_on_wake=True) == 0
        assert "REVIEWER UP" not in capsys.readouterr().out

        # The writer hands over, in the commit that completes the work.
        spec = writer / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8")
                        .replace("status: draft", "status: review"),
                        encoding="utf-8")
        _sync_git(writer, "commit", "-qam", "handover: m04-design -> review")
        _sync_git(writer, "push", "-q", "origin", "main")

        assert self._watch(reviewer, "reviewer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "REVIEWER UP: m04-design is at 'review' (was draft)" in out

    def test_the_other_role_does_not_wake_on_this_turn(self, clones, capsys):
        """Role isolation across the same board — v1.9's two-watchers rule."""
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()

        spec = writer / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8")
                        .replace("status: draft", "status: review"),
                        encoding="utf-8")
        _sync_git(writer, "commit", "-qam", "handover: m04-design -> review")
        _sync_git(writer, "push", "-q", "origin", "main")

        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP" not in out
        assert "moved: m04-design draft -> review" in out

    def test_an_unpushed_handover_is_not_a_turn(self, clones, capsys):
        """`git-workflow.md`: the turn is real on the remote, not on commit.

        The writer commits and does *not* push. Every local indication says it
        handed over; the reviewer must see nothing, because nothing published.
        """
        writer, reviewer = clones
        assert self._watch(reviewer, "reviewer") == 0
        capsys.readouterr()

        spec = writer / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8")
                        .replace("status: draft", "status: review"),
                        encoding="utf-8")
        _sync_git(writer, "commit", "-qam", "handover (unpublished)")

        assert self._watch(reviewer, "reviewer", exit_on_wake=True) == 0
        assert "REVIEWER UP" not in capsys.readouterr().out


class TestRunScope:
    """A watch watches a run — the vertical axis, so two streams of one loop
    stop hearing each other's doorbell.

    The fan-out defect this pins was found in the field on 2026-09-21: two
    reviewers armed against one definition both woke on either stream's
    turn. The scope is the `workflow-run`, read through the one membership
    edge the spec names (`linked_things: {relation: implements}`) — never
    `informed_by`, which is provenance and can legitimately point elsewhere.
    """

    LIFECYCLE = {
        "id": "lifecycle",
        "type": "workflow-definition",
        "status": "stable",
        "created": "2026-09-01",
        "stages": [
            {"id": "requirement", "to": ["design"]},
            {"id": "design", "to": ["test"]},
            {"id": "test", "to": []},
        ],
    }

    @staticmethod
    def _run(run_id: str) -> dict:
        return {"id": run_id, "type": "workflow-run", "status": "active",
                "created": "2026-09-12", "definition": "lifecycle",
                "current_stage": "design"}

    @staticmethod
    def _member(thing_id: str, run_id: str, status: str,
                relation: str = "implements") -> dict:
        return {**_spec(thing_id, status),
                "linked_things": [{"id": run_id, "relation": relation}]}

    @pytest.fixture
    def streams(self, tmp_path: Path) -> Path:
        _schema(tmp_path)
        _write(tmp_path, DEFINITION)
        _write(tmp_path, self.LIFECYCLE)
        _write(tmp_path, self._run("run-a"))
        _write(tmp_path, self._run("run-b"))
        _write(tmp_path, self._member("a-design", "run-a", "draft"))
        _write(tmp_path, self._member("b-design", "run-b", "draft"))
        return tmp_path

    @pytest.fixture(autouse=True)
    def _no_network(self, monkeypatch):
        monkeypatch.setattr(watch_mod, "_fetch", lambda c: None)
        from markdownllm.repository_view import RepositoryView
        monkeypatch.setattr(RepositoryView, "commit",
                            classmethod(lambda cls, r, rev: cls.worktree(r)))

    def _head(self, monkeypatch, sha):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (sha, None))

    def _args_for(self, root, run, **kw):
        return _args(root, run=run,
                     state=str(root / f".watch-{run or 'all'}.json"), **kw)

    # -- arming ------------------------------------------------------------

    def test_an_unknown_run_refuses(self, streams, capsys):
        assert watch_mod.cmd_watch(self._args_for(streams, "run-z")) == 2
        assert "no thing with id `run-z`" in capsys.readouterr().out

    def test_a_thing_that_is_not_a_run_refuses(self, streams, capsys):
        assert watch_mod.cmd_watch(self._args_for(streams, "a-design")) == 2
        assert "not a workflow-run" in capsys.readouterr().out

    def test_the_run_need_not_instance_the_watched_definition(
            self, streams, capsys, monkeypatch):
        """The run is the vertical; the definition is the horizontal.

        `run-a` instances `lifecycle`, not `spec-loop`, and that is the
        normal case — a watch reads the loop's stages for the run's
        members. Refusing here would refuse the topology the scope exists
        for.
        """
        self._head(monkeypatch, "a" * 40)
        assert watch_mod.cmd_watch(self._args_for(streams, "run-a")) == 0
        assert "scoped to run `run-a`" in capsys.readouterr().out

    # -- scope -------------------------------------------------------------

    def test_the_board_is_only_the_runs_members(
            self, streams, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, "run-a"))
        assert "baseline: 1 thing(s)" in capsys.readouterr().out

    def test_an_unscoped_watch_still_sees_every_stream(
            self, streams, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, None))
        out = capsys.readouterr().out
        assert "baseline: 2 thing(s)" in out
        assert "unscoped" in out

    def test_two_reviewers_on_two_runs_wake_only_on_their_own(
            self, streams, capsys, monkeypatch):
        """The defect itself, as a test."""
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, "run-a"))
        watch_mod.cmd_watch(self._args_for(streams, "run-b"))
        capsys.readouterr()

        _write(streams, self._member("b-design", "run-b", "review"))
        self._head(monkeypatch, "b" * 40)

        assert watch_mod.cmd_watch(
            self._args_for(streams, "run-a", exit_on_wake=True)) == 0
        assert "REVIEWER UP" not in capsys.readouterr().out

        assert watch_mod.cmd_watch(
            self._args_for(streams, "run-b", exit_on_wake=True)) == 0
        assert "REVIEWER UP: b-design is at 'review'" in capsys.readouterr().out

    def test_membership_is_implements_never_informed_by(
            self, streams, capsys, monkeypatch):
        """Provenance is not membership.

        A thing that names the run in `informed_by` but does not declare it
        realises the run is not on the run's board. The ruling is that a
        thing made under one run can be the realisation of another.
        """
        _write(streams, {**_spec("c-design", "draft"),
                         "informed_by": [{"id": "run-a",
                                          "commit": "f" * 40}]})
        _write(streams, self._member("d-design", "run-a", "draft",
                                     relation="references"))
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, "run-a"))
        assert "baseline: 1 thing(s)" in capsys.readouterr().out

    def test_a_thing_leaving_its_run_is_gone_for_that_watch(
            self, streams, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, "run-a"))
        capsys.readouterr()

        # a-design now realises run-b instead: off run-a's board.
        _write(streams, self._member("a-design", "run-b", "draft"))
        self._head(monkeypatch, "b" * 40)
        assert watch_mod.cmd_watch(
            self._args_for(streams, "run-a", exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "GONE: a-design" in out
        assert "or run" in out

    # -- isolation ---------------------------------------------------------

    def test_state_is_keyed_by_run_as_well(self, tmp_path):
        a = state_path_for(_config(tmp_path, run_id="run-a", state_file=None))
        b = state_path_for(_config(tmp_path, run_id="run-b", state_file=None))
        none = state_path_for(_config(tmp_path, state_file=None))
        assert len({a, b, none}) == 3
        assert "run-a" in a.name and "run-b" in b.name

    def test_watch_still_never_writes_to_the_corpus(
            self, streams, monkeypatch):
        before = {p: p.read_bytes()
                  for p in (streams / "things").rglob("*.md")}
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(streams, "run-a"))
        after = {p: p.read_bytes() for p in (streams / "things").rglob("*.md")}
        assert before == after

class TestSingleInstance:
    """One watcher per (definition, role), per clone.

    Keying the state file per role stops two *different* roles colliding. It
    does not stop two instances of the *same* role, and that is the failure
    the sibling loop actually hit — eight orphaned watchers racing on one
    state file, each absorbing the others' events, so the live one saw nothing
    change and stayed silent. These pin the second guarantee.
    """

    def test_a_second_instance_of_the_same_role_refuses(self, board, capsys):
        lock_file = watch_mod.lock_path_for(_config(board))
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text(str(os.getppid()), encoding="utf-8")

        assert watch_mod.cmd_watch(_args(board)) == 3
        out = capsys.readouterr().out
        assert "not starting a second" in out
        assert str(os.getppid()) in out

    def test_the_refusal_is_not_exit_zero(self, board, capsys):
        """Exit 3, never 0.

        A harness bound to `--exit-on-wake` re-invokes on exit. Returning 0
        for a double-arm refusal would read as "your turn" and wake an agent
        for a doorbell that never rang.
        """
        lock_file = watch_mod.lock_path_for(_config(board))
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text(str(os.getppid()), encoding="utf-8")
        assert watch_mod.cmd_watch(_args(board, exit_on_wake=True)) == 3

    def test_a_stale_lock_is_taken_not_obeyed(self, board, capsys, monkeypatch):
        """A watcher killed without cleanup must not lock its role out."""
        lock_file = watch_mod.lock_path_for(_config(board))
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text("999999999", encoding="utf-8")  # long dead
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (None, "offline"))
        assert watch_mod.cmd_watch(_args(board)) == 1
        assert "not starting a second" not in capsys.readouterr().out

    def test_a_corrupt_lock_does_not_block(self, board, monkeypatch):
        lock_file = watch_mod.lock_path_for(_config(board))
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        lock_file.write_text("not-a-pid", encoding="utf-8")
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (None, "offline"))
        assert watch_mod.cmd_watch(_args(board)) == 1

    def test_the_lock_is_released_on_exit(self, board, monkeypatch):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (None, "offline"))
        watch_mod.cmd_watch(_args(board))
        assert not watch_mod.lock_path_for(_config(board)).exists()

    def test_two_roles_never_share_a_lock(self, tmp_path):
        a = watch_mod.lock_path_for(
            _config(tmp_path, role="writer", state_file=None))
        b = watch_mod.lock_path_for(
            _config(tmp_path, role="reviewer", state_file=None))
        assert a != b

    def test_liveness_never_terminates_the_process_it_probes(self):
        """The Windows trap, pinned.

        `os.kill(pid, 0)` is a liveness probe on POSIX. On Windows, Python's
        `os.kill` routes to TerminateProcess for any signal that is not a
        CTRL_* event — so the obvious implementation would kill the very
        process it was asking about. This asserts our own live pid reads as
        alive and is still here afterwards.
        """
        assert watch_mod._process_alive(os.getpid()) is True
        assert watch_mod._process_alive(os.getpid()) is True  # still alive

    def test_a_dead_pid_reads_as_dead(self):
        assert watch_mod._process_alive(999999999) is False

    def test_a_nonsense_pid_reads_as_dead(self):
        assert watch_mod._process_alive(0) is False
        assert watch_mod._process_alive(-1) is False


class TestSelfHeal:
    """`loop-turns-self-heal-2026-09-23`: a turn that never left wakes its own
    side. The ref cannot show it — `test_an_unpushed_handover_is_not_a_turn`
    pins that the other side sees nothing — so the watch reads its own
    clone's branch against the ref, and rings this role once per local tip.
    The floor rings; the merge stays the agent's.
    """

    STAGES = TestRealRemoteTurn.STAGES

    @pytest.fixture
    def clones(self, tmp_path):
        bare = tmp_path / "origin.git"
        _sync_git(tmp_path, "init", "-q", "--bare", str(bare))
        _sync_git(tmp_path, "--git-dir", str(bare),
                  "symbolic-ref", "HEAD", "refs/heads/main")
        writer = tmp_path / "writer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(writer))
        _sync_git(writer, "checkout", "-q", "-b", "main")
        _schema(writer)
        _write(writer, {**DEFINITION, "stages": self.STAGES})
        _write(writer, _spec("m04-design", "draft"))
        _sync_git(writer, "add", "-A")
        _sync_git(writer, "commit", "-q", "-m", "create: the board")
        _sync_git(writer, "push", "-q", "-u", "origin", "main")
        reviewer = tmp_path / "reviewer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(reviewer))
        _sync_git(reviewer, "checkout", "-q", "-b", "main", "origin/main")
        return writer, reviewer

    def _watch(self, root, role, **kw):
        return watch_mod.cmd_watch(_args(root, role=role, **kw))

    def _handover_unpublished(self, writer, msg="handover (unpublished)"):
        spec = writer / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8")
                        .replace("status: draft", "status: review"),
                        encoding="utf-8")
        _sync_git(writer, "commit", "-qam", msg)

    def test_an_unpushed_handover_wakes_its_own_side(self, clones, capsys):
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()

        self._handover_unpublished(writer)

        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP: your last turn never left" in out
        assert "1 commit(s) ahead of origin/main (unpublished)" in out
        assert "Pull, merge, push again" in out
        # And still nothing on the other side: the ref did not move.
        assert self._watch(reviewer, "reviewer") == 0
        capsys.readouterr()
        assert self._watch(reviewer, "reviewer", exit_on_wake=True) == 0
        assert "REVIEWER UP" not in capsys.readouterr().out

    def test_the_wake_is_once_per_local_tip(self, clones, capsys):
        writer, _ = clones
        assert self._watch(writer, "writer") == 0
        self._handover_unpublished(writer)
        assert self._watch(writer, "writer") == 0
        assert "WRITER UP: your last turn never left" in capsys.readouterr().out

        # Same tip, next poll: the agent has been told; do not ring again.
        assert self._watch(writer, "writer") == 0
        assert "WRITER UP" not in capsys.readouterr().out

        # A further unpublished commit is a new tip: ring again.
        (writer / "things" / "note.md").write_text(
            "---\nid: note\ntype: design-spec\nstatus: draft\ncreated: 2026-09-23\n---\n\n# n\n",
            encoding="utf-8")
        _sync_git(writer, "add", "-A")
        _sync_git(writer, "commit", "-qm", "another unpublished commit")
        assert self._watch(writer, "writer") == 0
        assert "2 commit(s) ahead of origin/main" in capsys.readouterr().out

    def test_a_diverged_clone_is_told_the_remote_moved(self, clones, capsys):
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        self._handover_unpublished(writer)
        capsys.readouterr()

        # The other side publishes meanwhile: the writer's push would now be
        # rejected — exactly the field failure.
        (reviewer / "things" / "r-note.md").write_text(
            "---\nid: r-note\ntype: design-spec\nstatus: draft\ncreated: 2026-09-23\n---\n\n# r\n",
            encoding="utf-8")
        _sync_git(reviewer, "add", "-A")
        _sync_git(reviewer, "commit", "-qm", "reviewer publishes")
        _sync_git(reviewer, "push", "-q", "origin", "main")

        assert self._watch(writer, "writer") == 0
        out = capsys.readouterr().out
        assert "WRITER UP: your last turn never left" in out
        assert "the remote moved under it (diverged)" in out

    def test_publication_clears_the_debt_and_says_so(self, clones, capsys):
        writer, _ = clones
        assert self._watch(writer, "writer") == 0
        self._handover_unpublished(writer)
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()

        _sync_git(writer, "push", "-q", "origin", "main")
        assert self._watch(writer, "writer") == 0
        out = capsys.readouterr().out
        assert "published [writer]: the turn that had not left is on origin/main now" in out
        assert "WRITER UP" not in out

    def test_the_watch_still_never_writes_or_merges(self, clones):
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        self._handover_unpublished(writer)
        before = _sync_git(writer, "rev-parse", "HEAD").stdout.strip()
        remote = _sync_git(writer, "rev-parse", "origin/main").stdout.strip()
        assert self._watch(writer, "writer") == 0
        assert _sync_git(writer, "rev-parse", "HEAD").stdout.strip() == before
        assert _sync_git(writer, "rev-parse", "origin/main").stdout.strip() == remote
        # The corpus is untouched (the fixture keeps its state file in the clone root).
        assert _sync_git(writer, "status", "--porcelain", "--", "things").stdout.strip() == ""

    # ---- the seat-aware self-wake (the-seat; 2026-10-30) ---------------------
    # `in-a-shared-checkout-ahead-of-origin-says-nothing-about-whose-turn-it-is`:
    # the Claude seat was woken four times for commits that were Codex's or the
    # dispatcher's, and each false wake exited a watch that nobody re-armed. A
    # declared seat is rung only for its own commits.

    def _commit_as(self, root, name, email, msg):
        spec = root / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8")
                        .replace("status: draft", "status: review"),
                        encoding="utf-8")
        env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email,
               "GIT_COMMITTER_NAME": name, "GIT_COMMITTER_EMAIL": email}
        import subprocess
        subprocess.run(["git", "commit", "-qam", msg], cwd=root, check=True, env=env)

    def test_another_partys_unpublished_commit_does_not_wake_a_declared_seat(
            self, clones, capsys):
        from markdownllm.seat import set_seat
        writer, _ = clones
        set_seat(writer, "writer", "claude-code")
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()
        self._commit_as(writer, "codex", "codex@seat.local", "codex's turn, unpublished")
        # exit_on_wake: a ring would return 0 from the wake; `once` returns 0
        # quietly, so the text is the evidence.
        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP" not in out
        assert "not your turn [writer]" in out
        assert "none of them this seat's (`writer`)" in out and "authored by codex" in out
        assert "this watch stays armed" in out
        # Once per tip, like the ring it replaces.
        assert self._watch(writer, "writer") == 0
        assert "not your turn" not in capsys.readouterr().out

    def test_the_seats_own_unpublished_commit_still_wakes_it(self, clones, capsys):
        from markdownllm.seat import set_seat
        writer, _ = clones
        set_seat(writer, "writer", "claude-code")
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()
        self._commit_as(writer, "writer", "writer@seat.local", "my turn, unpublished")
        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP: your last turn never left" in out
        assert "seat undeclared" not in out and "not your turn" not in out

    def test_an_undeclared_seat_is_rung_as_before_and_told_why(self, clones, capsys):
        writer, _ = clones
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()
        self._commit_as(writer, "somebody", "somebody@example.invalid", "unpublished")
        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP: your last turn never left" in out
        assert "seat undeclared, so the watch cannot tell whose" in out


class TestNoteWake:
    """`a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`, on a real
    remote: the note rings the holder when another seat wrote it, stays a
    quiet line when the holder wrote it, and never rings the seat that is
    not the holder. The author is read from the commits between the two
    polls, matched to the declared seat the way the self-wake does."""

    STAGES = TestRealRemoteTurn.STAGES

    @pytest.fixture
    def clones(self, tmp_path):
        bare = tmp_path / "origin.git"
        _sync_git(tmp_path, "init", "-q", "--bare", str(bare))
        _sync_git(tmp_path, "--git-dir", str(bare),
                  "symbolic-ref", "HEAD", "refs/heads/main")
        writer = tmp_path / "writer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(writer))
        _sync_git(writer, "checkout", "-q", "-b", "main")
        _schema(writer)
        _write(writer, {**DEFINITION, "stages": self.STAGES})
        _write(writer, _spec("m04-design", "draft"))
        _sync_git(writer, "add", "-A")
        _sync_git(writer, "commit", "-q", "-m", "create: the board")
        _sync_git(writer, "push", "-q", "-u", "origin", "main")
        reviewer = tmp_path / "reviewer"
        _sync_git(tmp_path, "clone", "-q", str(bare), str(reviewer))
        _sync_git(reviewer, "checkout", "-q", "-b", "main", "origin/main")
        from markdownllm.seat import set_seat
        set_seat(writer, "writer", "claude-code")
        set_seat(reviewer, "reviewer", "codex")
        return writer, reviewer

    def _watch(self, root, role, **kw):
        return watch_mod.cmd_watch(_args(root, role=role, **kw))

    @staticmethod
    def _note(root, seat, text, msg):
        """A write at an unchanged status, committed as the clone's declared
        seat (the harness's `_sync_git` pins its own author, so the seat's
        identity is passed explicitly here, as `set_seat` would have it)."""
        spec = root / "things" / "m04-design.md"
        spec.write_text(spec.read_text(encoding="utf-8") + f"\n{text}\n",
                        encoding="utf-8")
        env = {**os.environ, "GIT_AUTHOR_NAME": seat,
               "GIT_AUTHOR_EMAIL": f"{seat}@seat.local",
               "GIT_COMMITTER_NAME": seat,
               "GIT_COMMITTER_EMAIL": f"{seat}@seat.local"}
        import subprocess
        subprocess.run(["git", "commit", "-qam", msg], cwd=root, check=True, env=env)
        _sync_git(root, "push", "-q", "origin", "main")

    def test_another_seats_note_rings_the_holder_and_nobody_else(
            self, clones, capsys):
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        assert self._watch(reviewer, "reviewer") == 0
        capsys.readouterr()

        # The reviewer writes on the writer's held thing without moving it.
        self._note(reviewer, "reviewer", "Note: the merge landed, you can go ahead.",
                   "note: merged")

        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert ("WRITER UP: a note landed on m04-design while it is addressed "
                "to you ('draft') — written by reviewer") in out
        assert "seat undeclared" not in out
        assert self._watch(reviewer, "reviewer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "REVIEWER UP" not in out
        assert "body [reviewer]: m04-design changed at 'draft'" in out

    def test_the_role_defaults_to_the_declared_seat(self, clones, capsys):
        """Actors are seats: a clone that declared its seat watches as it,
        and `--role` is for a loop whose actor names predate the ruling."""
        writer, reviewer = clones
        assert self._watch(writer, None) == 0
        out = capsys.readouterr().out
        assert "as [writer]" in out
        self._note(reviewer, "reviewer", "Note from the reviewer.", "note")
        assert self._watch(writer, None, exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP: a note landed on m04-design" in out
        assert "--- message: m04-design @" in out and "Note from the reviewer." in out

    def test_a_seat_the_loop_does_not_name_is_refused_with_the_rename_hint(
            self, clones, capsys):
        from markdownllm.seat import set_seat
        writer, _ = clones
        set_seat(writer, "workspace-9", "claude-code")
        assert self._watch(writer, None) == 2
        out = capsys.readouterr().out
        assert "declares no stage with `actor: workspace-9`" in out
        assert "the role came from this clone's seat (`workspace-9`)" in out
        assert "rename them to the seats or pass --role" in out

    def test_no_role_and_no_seat_is_refused(self, clones, capsys):
        from markdownllm.seat import clear_seat
        writer, _ = clones
        clear_seat(writer)
        assert self._watch(writer, None) == 2
        assert "no --role and no declared seat" in capsys.readouterr().out

    def test_the_holders_own_write_does_not_ring_it(self, clones, capsys):
        writer, reviewer = clones
        assert self._watch(writer, "writer") == 0
        capsys.readouterr()

        self._note(writer, "writer", "Progress: half done.", "progress")

        assert self._watch(writer, "writer", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "WRITER UP" not in out
        assert ("noted [writer]: m04-design changed at 'draft' by this seat "
                "(`writer`) — your own write, not a ring") in out


class TestTicketLoop:
    """The ticket — an ad-hoc message with no artefact behind it.

    Ruled 2026-09-30 (`ticket-is-the-ad-hoc-carrier-2026-09-30`): one
    overwritable thing per conversation, whose `status` is the *addressee*
    and whose body is the current message. The watch needed nothing new to
    carry it — these tests pin that the existing contract does. The one open
    question (double-sends) was first settled *no* by evidence here: a
    body-only change at the same status woke nobody. It was reopened and
    answered *yes* on 2026-11-02 by the first live run that needed it
    (`a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`): a write at
    an unchanged status is a note, and it rings the addressee.
    """

    LOOP = {
        "id": "ad-hoc-message-loop",
        "type": "workflow-definition",
        "status": "draft",
        "created": "2026-09-30",
        "stages": [
            {"id": "claude", "to": ["codex", "closed"], "actor": "claude"},
            {"id": "codex", "to": ["claude", "closed"], "actor": "codex"},
            {"id": "closed", "to": []},
        ],
    }

    @staticmethod
    def _ticket(status: str, body: str = "Codex, quickly review X.") -> str:
        meta = {"id": "ticket-claude-codex", "type": "ticket",
                "status": status, "created": "2026-09-30"}
        return thing_text(yaml.safe_dump(meta, sort_keys=False), body=body)

    @pytest.fixture
    def desk(self, tmp_path: Path) -> Path:
        write(tmp_path, "_schema.yaml", yaml.safe_dump({
            "schema_version": 1,
            "domain": "ticket-fixture",
            "types": {"ticket": {
                "statuses": ["claude", "codex", "closed"],
                "terminal_statuses": ["closed"],
            }},
        }, sort_keys=False))
        _write(tmp_path, self.LOOP)
        write(tmp_path, "things/ticket-claude-codex.md", self._ticket("codex"))
        return tmp_path

    @pytest.fixture(autouse=True)
    def _no_network(self, monkeypatch):
        monkeypatch.setattr(watch_mod, "_fetch", lambda c: None)
        from markdownllm.repository_view import RepositoryView
        monkeypatch.setattr(RepositoryView, "commit",
                            classmethod(lambda cls, r, rev: cls.worktree(r)))

    def _head(self, monkeypatch, sha):
        monkeypatch.setattr(watch_mod, "resolve_remote_head",
                            lambda c: (sha, None))

    def _args_for(self, root, role, **kw):
        return _args(root, role=role, definition="ad-hoc-message-loop",
                     state=str(root / f".watch-{role}.json"), **kw)

    def test_both_actors_arm_against_a_domain_declared_ticket(self, desk, capsys):
        for role in ("claude", "codex"):
            assert watch_mod.cmd_watch(self._args_for(desk, role)) != 2, role
        out = capsys.readouterr().out
        assert "as [claude]" in out and "as [codex]" in out

    def test_a_reserved_type_could_never_carry_a_ticket(self, desk, capsys,
                                                         monkeypatch):
        """Why `ticket` must be domain-declared: reserved types are off a
        status-keyed board, so a reserved ticket would never wake anyone."""
        self._head(monkeypatch, "a" * 40)
        write(desk, "things/ticket-claude-codex.md",
              thing_text("id: ticket-claude-codex\ntype: cue\nstatus: codex\n"
                         "created: 2026-09-30\n"))
        watch_mod.cmd_watch(self._args_for(desk, "codex"))
        assert "baseline: 0 thing(s)" in capsys.readouterr().out

    def test_the_addressee_wakes_and_the_sender_does_not(
            self, desk, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(desk, "claude"))
        watch_mod.cmd_watch(self._args_for(desk, "codex"))
        capsys.readouterr()

        # Codex replies: overwrite the body, set status to the next addressee.
        write(desk, "things/ticket-claude-codex.md",
              self._ticket("claude", "Reviewed X — two findings, see below."))
        self._head(monkeypatch, "b" * 40)

        assert watch_mod.cmd_watch(
            self._args_for(desk, "codex", exit_on_wake=True)) == 0
        assert "CODEX UP" not in capsys.readouterr().out
        assert watch_mod.cmd_watch(
            self._args_for(desk, "claude", exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "CLAUDE UP: ticket-claude-codex is at 'claude' (was codex)" in out
        # The message arrives with the wake: the body as committed at the
        # head that rang, so the woken agent reads nothing blind.
        assert "--- message: ticket-claude-codex @ bbbbbbbb ('claude') ---" in out
        assert "Reviewed X — two findings, see below." in out
        assert "--- end of message ---" in out

    def test_a_body_only_change_at_the_same_status_is_a_note_that_rings_the_addressee(
            self, desk, capsys, monkeypatch):
        """The double-send question, reopened and answered on live evidence.

        `diff_board` still keys on `{thing_id: status}` and skips `was ==
        now`; the note is read beside it, from a digest of each board
        thing's bytes. A write that leaves the addressee alone rings the
        addressee — not as a turn (`is at … was …`) but as a note landed on
        a ticket it holds. The sender's own watch sees the holder's write at
        a stage it does not act at, and stays quiet. No git here, so the
        author is unknown, and an unknown author is rung, never assumed to be
        this seat.
        """
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(desk, "codex"))
        watch_mod.cmd_watch(self._args_for(desk, "claude"))
        capsys.readouterr()

        write(desk, "things/ticket-claude-codex.md",
              self._ticket("codex", "Also — and do Y while you are there."))
        self._head(monkeypatch, "b" * 40)
        assert watch_mod.cmd_watch(
            self._args_for(desk, "codex", exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert ("CODEX UP: a note landed on ticket-claude-codex while it is "
                "addressed to you ('codex')") in out
        assert "an author the record does not show" in out
        assert "seat undeclared" in out
        assert "moved:" not in out and "is at" not in out
        assert "--- message: ticket-claude-codex @ bbbbbbbb ('codex') ---" in out
        assert "Also — and do Y while you are there." in out
        # The other side: the holder's ticket changed, not its turn.
        assert watch_mod.cmd_watch(
            self._args_for(desk, "claude", exit_on_wake=True)) == 0
        out = capsys.readouterr().out
        assert "CLAUDE UP" not in out
        assert "body [claude]: ticket-claude-codex changed at 'codex'" in out
        assert "--- message:" not in out

    def test_closing_wakes_nobody_and_the_ticket_leaves_no_board(
            self, desk, capsys, monkeypatch):
        """`closed` is terminal and declares no actor: the conversation ends
        without a doorbell. The ticket stays on the board (its status is a
        stage), so a reopen is a `closed -> <actor>` move, not a creation."""
        self._head(monkeypatch, "a" * 40)
        watch_mod.cmd_watch(self._args_for(desk, "claude"))
        watch_mod.cmd_watch(self._args_for(desk, "codex"))
        capsys.readouterr()

        write(desk, "things/ticket-claude-codex.md",
              self._ticket("closed", "Done; findings landed in design-x."))
        self._head(monkeypatch, "b" * 40)
        for role in ("claude", "codex"):
            assert watch_mod.cmd_watch(
                self._args_for(desk, role, exit_on_wake=True)) == 0
            out = capsys.readouterr().out
            assert f"{role.upper()} UP" not in out
            assert "moved: ticket-claude-codex codex -> closed" in out
            assert "GONE" not in out


class TestTicketTranscript:
    """A ticket's body is one message and its git history is the transcript
    (peer-loops, rule 1). A ticket wake therefore carries the last few
    earlier turns, read from the file's history at the head that rang,
    oldest first, then the message, then a reminder that the body is to be
    replaced, never appended to. Any other thing wakes exactly as before.

    Real commits in one local repository: the history is the thing under
    test, so the commit view is real; only the remote head and the fetch are
    stubbed (the head is this repository's own HEAD)."""

    LOOP = TestTicketLoop.LOOP
    TICKET = "things/ticket-claude-codex.md"

    @pytest.fixture
    def desk(self, tmp_path: Path, monkeypatch) -> Path:
        root = tmp_path / "desk"
        root.mkdir()
        _sync_git(root, "init", "-q")
        write(root, "_schema.yaml", yaml.safe_dump({
            "schema_version": 1,
            "domain": "ticket-fixture",
            "types": {
                "ticket": {"statuses": ["claude", "codex", "closed"],
                           "terminal_statuses": ["closed"]},
                "memo": {"statuses": ["claude", "codex", "closed"],
                         "terminal_statuses": ["closed"]},
            },
        }, sort_keys=False))
        _write(root, self.LOOP)
        _sync_git(root, "add", "-A")
        _sync_git(root, "commit", "-q", "-m", "create: the desk")
        monkeypatch.setattr(watch_mod, "_fetch", lambda c: None)
        monkeypatch.setattr(watch_mod, "_self_wake", lambda *a, **k: False)
        monkeypatch.setattr(
            watch_mod, "resolve_remote_head",
            lambda c: (_sync_git(c.root, "rev-parse", "HEAD").stdout.strip(),
                       None))
        return root

    @staticmethod
    def _turn(root, status, body, author, msg, day,
              rel=TICKET, thing_id="ticket-claude-codex", kind="ticket"):
        """Write the whole thing (one message in the body) and commit it as
        `author` on 2026-11-<day>."""
        meta = {"id": thing_id, "type": kind, "status": status,
                "created": "2026-11-01"}
        write(root, rel, thing_text(yaml.safe_dump(meta, sort_keys=False),
                                    body=body))
        stamp = f"2026-11-{day:02d}T12:00:00+00:00"
        env = {**os.environ, "GIT_AUTHOR_NAME": author,
               "GIT_AUTHOR_EMAIL": f"{author}@seat.local",
               "GIT_COMMITTER_NAME": author,
               "GIT_COMMITTER_EMAIL": f"{author}@seat.local",
               "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        import subprocess
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", msg], cwd=root, check=True,
                       env=env)
        return _sync_git(root, "rev-parse", "HEAD").stdout.strip()

    def _watch(self, root, role, **kw):
        return watch_mod.cmd_watch(_args(
            root, role=role, definition="ad-hoc-message-loop",
            state=str(root.parent / f".watch-{role}.json"), **kw))

    def test_four_earlier_turns_wake_with_the_last_three_oldest_first(
            self, desk, capsys):
        self._turn(desk, "codex", "Turn one: please review X.\n", "claude",
                   "ticket: turn one", 1)
        two = self._turn(desk, "claude", "Turn two: X has two findings.\n",
                         "codex", "ticket: turn two", 2)
        three = self._turn(desk, "codex", "Turn three: both fixed, recheck.\n",
                           "claude", "ticket: turn three", 3)
        four = self._turn(desk, "claude", "Turn four: one still open.\n",
                          "codex", "ticket: turn four", 4)
        assert self._watch(desk, "codex") == 0          # baseline
        capsys.readouterr()
        head = self._turn(desk, "codex", "Turn five: closed the last one.\n",
                          "claude", "ticket: turn five", 5)

        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "CODEX UP: ticket-claude-codex is at 'codex' (was claude)" in out
        assert ("--- earlier turns: ticket-claude-codex (3 shown, oldest "
                "first; `git log -- things/ticket-claude-codex.md` has the "
                "rest) ---") in out
        assert "Turn one" not in out
        h3 = (f"[3 back · codex · 2026-11-02 · {two[:8]} · "
              "ticket: turn two]\nTurn two: X has two findings.")
        h2 = (f"[2 back · claude · 2026-11-03 · {three[:8]} · "
              "ticket: turn three]\nTurn three: both fixed, recheck.")
        h1 = (f"[1 back · codex · 2026-11-04 · {four[:8]} · "
              "ticket: turn four]\nTurn four: one still open.")
        for header in (h3, h2, h1):
            assert header in out
        message = f"--- message: ticket-claude-codex @ {head[:8]} ('codex') ---"
        indexes = [out.index(x) for x in (
            "--- earlier turns:", h3, h2, h1, "--- end of earlier turns ---",
            message, "Turn five: closed the last one.", "--- end of message ---",
            "--- before you reply ---")]
        assert indexes == sorted(indexes)
        assert out.count("Turn five: closed the last one.") == 1
        assert watch_mod.reminder_block() in out

    def test_a_first_turn_has_no_earlier_turns_block(self, desk, capsys):
        assert self._watch(desk, "codex") == 0          # baseline: empty board
        capsys.readouterr()
        self._turn(desk, "codex", "Turn one: please review X.\n", "claude",
                   "ticket: open", 1)
        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "CODEX UP: ticket-claude-codex is at 'codex'" in out
        assert "--- message: ticket-claude-codex @" in out
        assert "--- before you reply ---" in out
        assert "earlier turns" not in out
        assert out.index("--- end of message ---") < out.index(
            "--- before you reply ---")

    def test_a_thing_that_is_not_a_ticket_wakes_as_before(self, desk, capsys):
        memo = dict(rel="things/memo-x.md", thing_id="memo-x", kind="memo")
        self._turn(desk, "codex", "Memo one.\n", "claude", "memo: one", 1,
                   **memo)
        self._turn(desk, "claude", "Memo two.\n", "codex", "memo: two", 2,
                   **memo)
        assert self._watch(desk, "codex") == 0
        capsys.readouterr()
        self._turn(desk, "codex", "Memo three.\n", "claude", "memo: three", 3,
                   **memo)
        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "CODEX UP: memo-x is at 'codex' (was claude)" in out
        assert "--- message: memo-x @" in out and "Memo three." in out
        assert "earlier turns" not in out
        assert "--- before you reply ---" not in out
        assert "Memo two." not in out

    def test_a_long_earlier_turn_is_cut_at_the_cap(self, desk, capsys):
        long_body = "# Long turn\n\n" + "x" * (watch_mod.TURN_CAP + 500) + "\n"
        self._turn(desk, "claude", long_body, "codex", "ticket: long", 1)
        assert self._watch(desk, "codex") == 0
        capsys.readouterr()
        self._turn(desk, "codex", "Short reply.\n", "claude", "ticket: short", 2)
        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        cut = len(long_body.strip("\n")) - watch_mod.TURN_CAP
        assert f"\n[… {cut} more character(s)]\n" in out
        assert "x" * (watch_mod.TURN_CAP + 1) not in out
        assert "(1 shown, oldest first;" in out

    def test_a_status_only_commit_is_not_a_duplicate_turn(self, desk, capsys):
        self._turn(desk, "claude", "Turn A.\n", "codex", "ticket: A", 1)
        self._turn(desk, "codex", "Turn B.\n", "claude", "ticket: B", 2)
        self._turn(desk, "claude", "Turn B.\n", "codex",
                   "ticket: hand back, status only", 3)
        assert self._watch(desk, "codex") == 0
        capsys.readouterr()
        self._turn(desk, "codex", "Turn C.\n", "claude", "ticket: C", 4)
        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert "(2 shown, oldest first;" in out
        assert out.count("Turn B.") == 1
        assert "hand back, status only" in out           # the newest B commit
        assert "ticket: B]" not in out
        assert out.index("Turn A.") < out.index("Turn B.") < out.index("Turn C.")

    def test_a_note_on_a_held_ticket_carries_the_transcript_and_reminder(
            self, desk, capsys):
        self._turn(desk, "claude", "Turn A.\n", "codex", "ticket: A", 1)
        self._turn(desk, "codex", "Turn B.\n", "claude", "ticket: B", 2)
        assert self._watch(desk, "codex") == 0
        capsys.readouterr()
        self._turn(desk, "codex", "Note: and do Y too.\n", "claude",
                   "ticket: note", 3)
        assert self._watch(desk, "codex", exit_on_wake=True) == 0
        out = capsys.readouterr().out
        assert ("CODEX UP: a note landed on ticket-claude-codex while it is "
                "addressed to you ('codex')") in out
        assert "is at" not in out
        assert "--- earlier turns: ticket-claude-codex (2 shown" in out
        assert "[2 back · codex · 2026-11-01" in out
        assert "[1 back · claude · 2026-11-02" in out
        assert out.index("--- end of earlier turns ---") < out.index(
            "--- message: ticket-claude-codex @") < out.index(
            "Note: and do Y too.") < out.index("--- before you reply ---")

    def test_an_unreadable_history_is_emitted_never_raised(self, tmp_path):
        config = WatchConfig(root=tmp_path, role="codex",
                             definition_id="ad-hoc-message-loop")
        out = watch_mod.earlier_turns_block(
            config, "c" * 40, tmp_path / "things" / "t.md", "t", "body")
        assert out == ("earlier turns unavailable: could not read the history "
                       "of t at cccccccc")
