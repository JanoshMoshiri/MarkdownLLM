"""estate-sync and autopush (sync.py) — the machine axis and its
publication leg. Lifted from test_mdllm.py along its banners (sprint 2, F6;
floor-structure-residue item 4)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from corpus_harness import _ns, _sync_git, thing_text, write  # noqa: E402


# ---------------------------------------------------------------------------
# estate-sync (sync.py) — the machine axis: ff-only transport, divergence
# reported never resolved, discovery of repos (not membranes), publication debt
# ---------------------------------------------------------------------------

def _seed_pair(tmp_path, name="d"):
    """A 'remote' repo and a clone of it — the two-machine estate in miniature."""
    src = tmp_path / f"{name}-src"
    src.mkdir()
    _sync_git(src, "init", "-q")
    (src / "a.txt").write_text("one\n", encoding="utf-8")
    _sync_git(src, "add", "-A")
    _sync_git(src, "commit", "-q", "-m", "c1")
    clone = tmp_path / name
    _sync_git(tmp_path, "clone", "-q", str(src), str(clone))
    return src, clone


def test_estate_sync_classifies_transport_without_inventing_authentication():
    from markdownllm.sync import _classify_fetch_failure
    cases = (
        ("fatal: Failed to connect to github.com port 443: "
         "Could not connect to server", "offline"),
        ("warning: unable to access 'C:/Users/example/.config/git/ignore': "
         "Permission denied\n"
         "fatal: Failed to connect to github.com port 443: "
         "Could not connect to server", "offline"),
        ("fatal: unable to access remote: Could not resolve host: github.com",
         "offline"),
        ("fatal: Authentication failed for "
         "'https://github.com/example/repo.git/'", "auth-failed"),
        ("error: cannot open .git/FETCH_HEAD: Permission denied",
         "permission-denied"),
        ("fatal: unexpected transport response", "fetch-failed"),
    )
    for stderr, expected in cases:
        assert _classify_fetch_failure(stderr) == expected


def test_estate_sync_discovery_walks_root_and_domain_children(tmp_path):
    from markdownllm.sync import discover_repos
    _sync_git(tmp_path, "init", "-q")
    (tmp_path / "domain").mkdir()
    (tmp_path / "outside").mkdir()
    src, _ = _seed_pair(tmp_path / "outside", "x")
    clone = tmp_path / "domain" / "x"
    _sync_git(tmp_path, "clone", "-q", str(src), str(clone))
    (tmp_path / "domain" / "not-a-repo").mkdir()
    repos = discover_repos(tmp_path)
    assert repos == [tmp_path, clone]


def test_estate_sync_fast_forwards_when_remote_ahead(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    src, clone = _seed_pair(tmp_path)
    (src / "a.txt").write_text("two\n", encoding="utf-8")
    _sync_git(src, "commit", "-q", "-am", "c2")
    res = sync_repo(clone)
    assert res.state is SyncState.SYNCED
    assert res.moved and "+1" in res.detail
    assert (clone / "a.txt").read_text(encoding="utf-8") == "two\n"


def test_estate_sync_reports_ahead_never_pushes(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    src, clone = _seed_pair(tmp_path)
    (clone / "b.txt").write_text("local\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "local work")
    res = sync_repo(clone)
    assert res.state is SyncState.AHEAD
    assert "unpushed" in res.detail
    # the remote must NOT have received the commit
    log = _sync_git(src, "log", "--oneline")
    assert "local work" not in log.stdout


def test_estate_sync_divergence_reported_never_resolved(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    src, clone = _seed_pair(tmp_path)
    (src / "a.txt").write_text("remote2\n", encoding="utf-8")
    _sync_git(src, "commit", "-q", "-am", "remote c2")
    (clone / "b.txt").write_text("local\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "local c2")
    res = sync_repo(clone)
    assert res.state is SyncState.DIVERGED and not res.moved
    assert "+1 local / +1 remote" in res.detail
    # no merge commit was created
    log = _sync_git(clone, "log", "--oneline")
    assert len(log.stdout.strip().splitlines()) == 2


def test_estate_sync_dirty_tree_skips_pull(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    src, clone = _seed_pair(tmp_path)
    (src / "a.txt").write_text("remote2\n", encoding="utf-8")
    _sync_git(src, "commit", "-q", "-am", "remote c2")
    (clone / "a.txt").write_text("uncommitted local edit\n", encoding="utf-8")
    res = sync_repo(clone)
    assert res.state is SyncState.DIRTY and not res.moved
    # the uncommitted edit survives untouched
    assert (clone / "a.txt").read_text(encoding="utf-8") == "uncommitted local edit\n"


def test_estate_sync_degraded_dirty_tree_keeps_cached_marker(
        tmp_path, monkeypatch):
    import subprocess
    from markdownllm import sync as sync_mod
    _src, clone = _seed_pair(tmp_path)
    (clone / "a.txt").write_text("uncommitted local edit\n", encoding="utf-8")
    original = sync_mod._git

    def offline_fetch(repo, *args, **kwargs):
        if args[:2] == ("fetch", "--quiet"):
            return subprocess.CompletedProcess(
                args, 1, "", "fatal: Failed to connect to github.com")
        return original(repo, *args, **kwargs)

    monkeypatch.setattr(sync_mod, "_git", offline_fetch)
    res = sync_mod.sync_repo(clone)

    assert res.state is sync_mod.SyncState.OFFLINE
    assert res.detail == "working tree not clean (cached)"


def test_estate_sync_local_only_repo_is_legitimate(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    solo = tmp_path / "solo"
    solo.mkdir()
    _sync_git(solo, "init", "-q")
    (solo / "a.txt").write_text("x\n", encoding="utf-8")
    _sync_git(solo, "add", "-A")
    _sync_git(solo, "commit", "-q", "-m", "c1")
    res = sync_repo(solo)
    assert res.state is SyncState.LOCAL_ONLY


def test_estate_sync_status_mode_reports_debt_without_network(tmp_path, capsys):
    import mdllm
    src, clone = _seed_pair(tmp_path)
    (clone / "b.txt").write_text("local\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "unpublished")
    rc = mdllm.cmd_estate_sync(_ns(paths=[str(clone)], status=True, timeout=20))
    out = capsys.readouterr().out
    assert rc == 0 and "Publication Debt" in out
    assert "ahead" in out and "+1 (unpushed)" in out


def test_estate_sync_require_fresh_splits_manual_gate_from_lifecycle_fallback(
        tmp_path, monkeypatch, capsys):
    from markdownllm import sync as sync_mod
    repo = tmp_path / "repo"
    repo.mkdir()
    current = [sync_mod.SyncResult(
        repo=repo,
        state=sync_mod.SyncState.PERMISSION_DENIED,
        detail="orienting from last-fetched state",
    )]
    monkeypatch.setattr(sync_mod, "discover_repos", lambda _root: [repo])
    monkeypatch.setattr(
        sync_mod, "sync_repo", lambda *_args, **_kw: current[0])

    lifecycle_rc = sync_mod.cmd_estate_sync(_ns(
        paths=[str(repo)], status=False, require_fresh=False, timeout=20))
    lifecycle_out = capsys.readouterr().out
    strict_rc = sync_mod.cmd_estate_sync(_ns(
        paths=[str(repo)], status=False, require_fresh=True, timeout=20))
    strict_out = capsys.readouterr().out
    current[0] = sync_mod.SyncResult(
        repo=repo,
        state=sync_mod.SyncState.UP_TO_DATE,
    )
    fresh_rc = sync_mod.cmd_estate_sync(_ns(
        paths=[str(repo)], status=False, require_fresh=True, timeout=20))
    fresh_out = capsys.readouterr().out

    assert lifecycle_rc == 0
    assert "permission-denied" in lifecycle_out
    assert strict_rc == 1
    assert "Fresh sync incomplete: repo=permission-denied" in strict_out
    assert "one-command network/filesystem approval" in strict_out
    assert fresh_rc == 0
    assert "up-to-date" in fresh_out
    assert "Fresh sync incomplete" not in fresh_out


def test_estate_sync_in_progress_merge_is_skipped(tmp_path):
    from markdownllm.sync import SyncState, sync_repo
    src, clone = _seed_pair(tmp_path)
    gitdir = clone / ".git"
    (gitdir / "MERGE_HEAD").write_text("0" * 40 + "\n", encoding="utf-8")
    res = sync_repo(clone)
    assert res.state is SyncState.IN_OPERATION and not res.moved


def test_estate_sync_global_deadline_skips_remote_and_reads_cached_state(
        tmp_path, monkeypatch):
    from markdownllm import sync as sync_mod
    src, clone = _seed_pair(tmp_path)
    calls = []
    original = sync_mod._git

    def observed(repo, *args, **kwargs):
        calls.append(args)
        return original(repo, *args, **kwargs)

    monkeypatch.setattr(sync_mod, "_git", observed)
    res = sync_mod.sync_repo(
        clone, deadline=sync_mod.time.monotonic() - 1)

    assert res.state is sync_mod.SyncState.BUDGET_EXHAUSTED
    assert "last-fetched state" in res.detail
    assert not any(args and args[0] in ("fetch", "pull") for args in calls)


def test_estate_sync_clamps_fetch_to_remaining_global_budget(
        tmp_path, monkeypatch):
    from markdownllm import sync as sync_mod
    _, clone = _seed_pair(tmp_path)
    observed = []
    original = sync_mod._git

    def timed(repo, *args, **kwargs):
        if args and args[0] == "fetch":
            observed.append(kwargs["timeout"])
        return original(repo, *args, **kwargs)

    monkeypatch.setattr(sync_mod, "_git", timed)
    sync_mod.sync_repo(
        clone, timeout=20, deadline=sync_mod.time.monotonic() + 2)

    assert len(observed) == 1
    assert 0 < observed[0] <= 2



# ---------------------------------------------------------------------------
# autopush (sync.py) — the publication leg: transport of committed state,
# explicit opt-in, no --force ever, rejection surfaced never resolved
# (estate-cadence-cluster Phase 1)
# ---------------------------------------------------------------------------

def _seed_bare_pair(tmp_path, name="d"):
    """A bare 'remote' and a working clone — the push-side estate in miniature."""
    bare = tmp_path / f"{name}-remote.git"
    _sync_git(tmp_path, "init", "-q", "--bare", str(bare))
    clone = tmp_path / name
    _sync_git(tmp_path, "clone", "-q", str(bare), str(clone))
    (clone / "AGENTS.md").write_text(
        "---\nname: X\ngit:\n  autopush: true\n---\n# X\n", encoding="utf-8")
    (clone / "a.txt").write_text("one\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "c1")
    _sync_git(clone, "push", "-q", "-u", "origin", "HEAD")
    return bare, clone


def test_autopush_publishes_committed_state(tmp_path):
    from markdownllm.sync import autopush_repo
    bare, clone = _seed_bare_pair(tmp_path)
    (clone / "b.txt").write_text("two\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "local work")
    res = autopush_repo(clone)
    assert res["state"] == "published"
    log = _sync_git(tmp_path, "--git-dir", str(bare), "log", "--oneline")
    assert "local work" in log.stdout


def test_autopush_absence_of_config_is_off(tmp_path):
    from markdownllm.sync import _autopush_enabled
    bare, clone = _seed_bare_pair(tmp_path)
    (clone / "AGENTS.md").unlink()
    assert _autopush_enabled(clone) is False  # no AGENTS.md at all
    (clone / "AGENTS.md").write_text(
        "---\nname: X\ngit:\n  autocommit: true\n---\n# X\n", encoding="utf-8")
    assert _autopush_enabled(clone) is False  # git block without the key


def test_autopush_explicit_false_opts_out_and_pushes_nothing(tmp_path):
    from markdownllm.sync import autopush_repo
    bare, clone = _seed_bare_pair(tmp_path)
    (clone / "AGENTS.md").write_text(
        "---\nname: X\ngit:\n  autopush: false\n---\n# X\n", encoding="utf-8")
    _sync_git(clone, "add", "-A")
    _sync_git(clone, "commit", "-q", "-m", "opted out")
    res = autopush_repo(clone)
    assert res["state"] == "off"
    log = _sync_git(tmp_path, "--git-dir", str(bare), "log", "--oneline")
    assert "opted out" not in log.stdout


def test_autopush_local_only_is_silent_state(tmp_path):
    from markdownllm.sync import autopush_repo
    repo = tmp_path / "solo"
    repo.mkdir()
    _sync_git(repo, "init", "-q")
    (repo / "AGENTS.md").write_text(
        "---\nname: X\ngit:\n  autopush: true\n---\n# X\n", encoding="utf-8")
    (repo / "a.txt").write_text("x\n", encoding="utf-8")
    _sync_git(repo, "add", "-A")
    _sync_git(repo, "commit", "-q", "-m", "c1")
    res = autopush_repo(repo)
    assert res["state"] == "local-only"


def test_autopush_rejection_is_surfaced_never_forced(tmp_path):
    from markdownllm.sync import autopush_repo
    bare, clone_a = _seed_bare_pair(tmp_path, "a")
    clone_b = tmp_path / "b"
    _sync_git(tmp_path, "clone", "-q", str(bare), str(clone_b))
    # A advances the remote past B
    (clone_a / "a.txt").write_text("from-a\n", encoding="utf-8")
    _sync_git(clone_a, "commit", "-q", "-am", "a moves")
    _sync_git(clone_a, "push", "-q")
    # B commits without fetching — push must be rejected, remote must keep A's move
    (clone_b / "a.txt").write_text("from-b\n", encoding="utf-8")
    _sync_git(clone_b, "commit", "-q", "-am", "b diverges")
    res = autopush_repo(clone_b)
    assert res["state"] == "rejected"
    assert "decision" in res["detail"]
    log = _sync_git(tmp_path, "--git-dir", str(bare), "log", "--oneline")
    assert "a moves" in log.stdout and "b diverges" not in log.stdout


def test_autopush_cmd_always_exits_zero(tmp_path, capsys):
    from markdownllm.sync import cmd_autopush
    import argparse
    bare, clone_a = _seed_bare_pair(tmp_path, "a")
    clone_b = tmp_path / "b"
    _sync_git(tmp_path, "clone", "-q", str(bare), str(clone_b))
    (clone_a / "a.txt").write_text("from-a\n", encoding="utf-8")
    _sync_git(clone_a, "commit", "-q", "-am", "a moves")
    _sync_git(clone_a, "push", "-q")
    (clone_b / "a.txt").write_text("from-b\n", encoding="utf-8")
    _sync_git(clone_b, "commit", "-q", "-am", "b diverges")
    args = argparse.Namespace(path=str(clone_b), timeout=20)
    assert cmd_autopush(args) == 0  # a post-commit surface never fails the commit
    out = capsys.readouterr().out
    assert "REJECTED" in out


