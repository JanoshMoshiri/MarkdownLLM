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

    def test_an_emptied_board_is_a_bad_read_not_an_empty_estate(
            self, board, capsys, monkeypatch):
        self._head(monkeypatch, "a" * 40)
        self._commit_view_over_worktree(monkeypatch, board)
        watch_mod.cmd_watch(_args(board))
        capsys.readouterr()

        (board / "things" / "m04-design.md").unlink()
        self._head(monkeypatch, "e" * 40)
        assert watch_mod.cmd_watch(_args(board)) == 1
        assert "bad read" in capsys.readouterr().out

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
