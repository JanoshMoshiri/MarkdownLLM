"""Repository transaction boundaries introduced by the substrate review."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm import assemble as assemble_mod  # noqa: E402
from markdownllm import git_transport as transport_mod  # noqa: E402
from markdownllm import publish as publish_mod  # noqa: E402
from markdownllm import hook_contract  # noqa: E402
from markdownllm import scaffold as scaffold_mod  # noqa: E402
from markdownllm import sync as sync_mod  # noqa: E402
from markdownllm import runtime as runtime_mod  # noqa: E402
from markdownllm.hook_contract import HookByteContract  # noqa: E402
from markdownllm.repository_transaction import (  # noqa: E402
    RepositoryTransaction, RepositoryTransactionError,
)
from markdownllm import repository_transaction as transaction_mod  # noqa: E402
from markdownllm.repository_view import (  # noqa: E402
    FROZEN_INDEX_ROOT_ENV, FROZEN_INDEX_TREE_ENV, RepositoryView,
    RepositoryViewError,
)


for _key in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_key, "transaction-tests")
for _key in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_key, "transaction-tests@local")


def _git(root: Path, *args: str, check: bool = True):
    return subprocess.run(["git", "-C", str(root), *args], check=check,
                          capture_output=True, text=True)


def _repo(root: Path, *, commit: bool = False) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    if commit:
        (root / "seed.txt").write_text("seed\n", encoding="utf-8")
        _git(root, "add", "seed.txt")
        _git(root, "commit", "-q", "-m", "seed")
    return root


def test_install_hook_honours_core_hooks_path_and_is_uninstallable(tmp_path):
    repo = _repo(tmp_path / "repo")
    _git(repo, "config", "core.hooksPath", ".operator-hooks")

    scaffold_mod.install_hook(repo)

    hooks = hook_contract.resolve_hooks_dir(repo)
    assert hooks == (repo / ".operator-hooks").resolve()
    assert {p.name for p in hooks.iterdir()} == {
        "pre-commit", "commit-msg", "post-commit"}

    removed_from = scaffold_mod.uninstall_hook(repo)
    assert removed_from == hooks
    assert not any((hooks / name).exists() for name in (
        "pre-commit", "commit-msg", "post-commit"))


def test_install_hook_refuses_foreign_hook_without_partial_writes(tmp_path):
    repo = _repo(tmp_path / "repo")
    hooks = repo / ".operator-hooks"
    hooks.mkdir()
    _git(repo, "config", "core.hooksPath", ".operator-hooks")
    operator_bytes = b"#!/bin/sh\n# operator-owned\n\xff\n"
    (hooks / "pre-commit").write_bytes(operator_bytes)

    with pytest.raises(SystemExit, match="refusing to replace existing operator hook"):
        scaffold_mod.install_hook(repo)

    assert (hooks / "pre-commit").read_bytes() == operator_bytes
    assert not (hooks / "commit-msg").exists()
    assert not (hooks / "post-commit").exists()


def test_install_hook_resolves_gitfile_worktree_hooks(tmp_path):
    main = _repo(tmp_path / "main", commit=True)
    linked = tmp_path / "linked"
    _git(main, "worktree", "add", "-q", "-b", "linked-test", str(linked))
    assert (linked / ".git").is_file()

    scaffold_mod.install_hook(linked)

    hooks = hook_contract.resolve_hooks_dir(linked)
    reported = _git(linked, "rev-parse", "--path-format=absolute",
                    "--git-path", "hooks").stdout.strip()
    assert hooks == Path(reported).resolve()
    assert (hooks / "pre-commit").is_file()
    installed = (hooks / "pre-commit").read_text(encoding="utf-8")
    assert f'MDLLM_ROUTE="{hook_contract.MDLLM_ENTRY.as_posix()}"' in installed
    assert 'MDLLM="$ROOT/C:' not in installed
    scaffold_mod.uninstall_hook(linked)


def test_install_hook_rollback_never_overwrites_concurrent_operator_edit(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo")
    scaffold_mod.install_hook(repo)
    hooks = hook_contract.resolve_hooks_dir(repo)
    operator = b"#!/bin/sh\n# concurrent operator edit\nexit 7\n"
    original_replace = Path.replace

    def fail_second_replace(path, target):
        target = Path(target)
        if target.name == "commit-msg":
            (hooks / "pre-commit").write_bytes(operator)
            raise OSError("injected second-hook replace failure")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_second_replace)
    with pytest.raises(scaffold_mod.HookTransactionError,
                       match="rollback conflicts"):
        scaffold_mod.install_hook(repo)

    assert (hooks / "pre-commit").read_bytes() == operator
    # The failed and not-yet-applied legs retain their exact prior mdllm bytes.
    rel = hook_contract.hook_mdllm_route(repo)
    assert (hooks / "commit-msg").read_bytes() == (
        hook_contract.COMMIT_MSG_HOOK_BODY.format(rel=rel).encode("utf-8"))
    assert (hooks / "post-commit").read_bytes() == (
        hook_contract.POST_COMMIT_HOOK_BODY.format(rel=rel).encode("utf-8"))


def test_install_hook_rechecks_each_snapshot_before_first_replace(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo")
    scaffold_mod.install_hook(repo)
    hooks = hook_contract.resolve_hooks_dir(repo)
    operator = b"#!/bin/sh\n# changed while payloads staged\nexit 3\n"
    original_stage = scaffold_mod._stage_hook
    staged_count = {"value": 0}

    def mutate_after_staging(path, payload, mode):
        result = original_stage(path, payload, mode)
        staged_count["value"] += 1
        if staged_count["value"] == 3:
            (hooks / "pre-commit").write_bytes(operator)
        return result

    monkeypatch.setattr(scaffold_mod, "_stage_hook", mutate_after_staging)
    with pytest.raises(scaffold_mod.HookTransactionConflict,
                       match="changed while hook payloads were staged"):
        scaffold_mod.install_hook(repo)

    assert (hooks / "pre-commit").read_bytes() == operator


def test_uninstall_rollback_never_overwrites_concurrent_recreation(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo")
    scaffold_mod.install_hook(repo)
    hooks = hook_contract.resolve_hooks_dir(repo)
    operator = b"#!/bin/sh\n# recreated after unlink\nexit 9\n"
    original_unlink = Path.unlink

    def fail_second_unlink(path, *args, **kwargs):
        if path.name == "commit-msg":
            (hooks / "pre-commit").write_bytes(operator)
            raise OSError("injected second-hook unlink failure")
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", fail_second_unlink)
    with pytest.raises(scaffold_mod.HookTransactionError,
                       match="rollback conflicts"):
        scaffold_mod.uninstall_hook(repo)

    assert (hooks / "pre-commit").read_bytes() == operator
    assert (hooks / "commit-msg").is_file()
    assert (hooks / "post-commit").is_file()


def test_old_git_fallback_executes_only_attested_hook_bytes(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo")
    hooks = repo / ".git" / "hooks"
    hook = hooks / "pre-commit"
    payload = b"#!/bin/sh\nexit 0\n"
    hook.write_bytes(payload)
    hook.chmod(hook.stat().st_mode | 0o111)
    monkeypatch.setattr(runtime_mod, "git_supports_hook_run", lambda _root: False)

    result = runtime_mod.run_git_hook(
        repo, "pre-commit", expected_bytes=payload)
    if not result["supported"]:
        pytest.skip(result["detail"])
    assert result["executed"] is True
    assert result["passed"] is True
    assert result["via"] == "direct-compatible"

    hook.write_bytes(b"#!/bin/sh\nexit 91\n")
    refused = runtime_mod.run_git_hook(
        repo, "pre-commit", expected_bytes=payload)
    assert refused["supported"] is False
    assert refused["executed"] is False
    assert "bytes changed" in refused["detail"]


def test_exact_transaction_carries_managed_hook_bytes_to_old_git_fallback(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo", commit=True)
    hook = repo / ".git" / "hooks" / "pre-commit"
    payload = b"#!/bin/sh\necho ran > .hook-ran\n"
    hook.write_bytes(payload)
    hook.chmod(hook.stat().st_mode | 0o111)
    monkeypatch.setattr(runtime_mod, "git_supports_hook_run", lambda _root: False)

    candidate = repo / "candidate.txt"
    candidate.write_text("candidate\n", encoding="utf-8")
    transaction = RepositoryTransaction.begin(
        repo,
        hook_contract=HookByteContract.from_mapping({"pre-commit": payload}),
    )
    try:
        result = transaction.commit_exact(
            (candidate.name,), "test: exact old-Git hook contract")
    except RepositoryTransactionError as exc:
        if "cannot be executed safely" in str(exc):
            pytest.skip(str(exc))
        raise

    assert result.committed_paths == (candidate.name,)
    assert (repo / ".hook-ran").read_text(encoding="utf-8").strip() == "ran"


def test_repository_index_view_honours_validated_hook_tree_pin(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo", commit=True)
    candidate = repo / "candidate.txt"
    candidate.write_text("first candidate\n", encoding="utf-8")
    _git(repo, "add", candidate.name)
    frozen = _git(repo, "write-tree").stdout.strip()
    monkeypatch.setenv(FROZEN_INDEX_TREE_ENV, frozen)
    monkeypatch.setenv(FROZEN_INDEX_ROOT_ENV, str(repo.resolve()))

    candidate.write_text("later candidate\n", encoding="utf-8")
    _git(repo, "add", candidate.name)
    view = RepositoryView.index(repo)

    assert view.tree_sha == frozen
    assert view.read_text(candidate.name) == "first candidate\n"
    monkeypatch.setenv(FROZEN_INDEX_ROOT_ENV, str(tmp_path.resolve()))
    with pytest.raises(RepositoryViewError, match="root does not match"):
        RepositoryView.index(repo)


def test_real_hook_blocks_index_mutation_between_subchecks(
        tmp_path, monkeypatch):
    repo = _repo(tmp_path / "repo", commit=True)
    candidate = repo / "candidate.txt"
    candidate.write_text("one frozen candidate\n", encoding="utf-8")
    _git(repo, "add", candidate.name)

    fake_root = tmp_path / "fake-framework"
    fake_entry = fake_root / "tools" / "mdllm.py"
    fake_entry.parent.mkdir(parents=True)
    log = tmp_path / "subchecks.log"
    project_tools = Path(__file__).resolve().parents[1]
    fake_entry.write_text(
        "import os, pathlib, subprocess, sys\n"
        f"sys.path.insert(0, {str(project_tools)!r})\n"
        "from markdownllm.repository_view import RepositoryView\n"
        "command = sys.argv[1]\n"
        "root = pathlib.Path(sys.argv[2]).resolve()\n"
        "if command == 'precommit':\n"
        "    # The hook now invokes the real coordinator, which re-spawns\n"
        "    # THIS entry (argv[0]) for each leg — so the instrumentation\n"
        "    # below still observes every leg, now concurrently.\n"
        "    from types import SimpleNamespace\n"
        "    from markdownllm.precommit import cmd_precommit\n"
        "    raise SystemExit(cmd_precommit(SimpleNamespace(path=str(root))))\n"
        "view = RepositoryView.index(root)\n"
        "value = view.read_text('candidate.txt').strip()\n"
        f"log = pathlib.Path({str(log)!r})\n"
        "with log.open('a', encoding='utf-8') as handle:\n"
        "    handle.write(f'{command}|{view.tree_sha}|{value}\\n')\n"
        "if command == 'validate':\n"
        "    (root / 'candidate.txt').write_text('mutated mid-floor\\n', encoding='utf-8')\n"
        "    subprocess.run(['git', 'add', 'candidate.txt'], cwd=root, check=True)\n"
        "raise SystemExit(0)\n",
        encoding="utf-8", newline="\n")
    monkeypatch.setattr(hook_contract, "MDLLM_ENTRY", fake_entry)
    scaffold_mod.install_hook(repo)
    # Give the emitted portable resolver a repo-local POSIX candidate which
    # delegates to this test runner's known floor-capable interpreter. This is
    # a test fixture, not an ambient PATH assumption (especially under Git sh
    # on Windows, where native PATH conversion is deliberately inconsistent).
    interpreter = repo / ".venv" / "bin" / "python"
    interpreter.parent.mkdir(parents=True)
    interpreter.write_text(
        f'#!/bin/sh\nexec "{Path(sys.executable).as_posix()}" "$@"\n',
        encoding="utf-8", newline="\n")
    interpreter.chmod(interpreter.stat().st_mode | 0o111)

    result = subprocess.run(
        ["git", "hook", "run", "pre-commit"], cwd=repo,
        capture_output=True, text=True, encoding="utf-8", errors="replace")

    assert result.returncode != 0
    assert "staged index changed while the floor was running" in (
        result.stdout + result.stderr)
    rows = [line.split("|", 2) for line in log.read_text(
        encoding="utf-8").splitlines()]
    # The legs run CONCURRENTLY since the precommit coordinator (floor-
    # sprint-1 F11), so execution order is nondeterministic; the invariant
    # is that all four legs ran and every one observed the SAME frozen
    # candidate despite the mid-floor mutation.
    assert sorted(row[0] for row in rows) == [
        "boundary", "candidates", "coherence", "validate"]
    assert len({row[1] for row in rows}) == 1
    assert {row[2] for row in rows} == {"one frozen candidate"}
    assert _git(repo, "show", f":{candidate.name}").stdout == "mutated mid-floor\n"


def test_scaffold_outer_commit_is_exact_and_preserves_unrelated_index(tmp_path):
    outer = _repo(tmp_path / "outer", commit=True)
    unrelated = outer / "unrelated.txt"
    unrelated.write_text("operator work\n", encoding="utf-8")
    _git(outer, "add", "unrelated.txt")

    target = outer / "new-domain"
    rc = scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness=None))

    assert rc == 0
    committed = {
        line.strip() for line in _git(
            outer, "show", "--pretty=format:", "--name-only", "HEAD"
        ).stdout.splitlines() if line.strip()
    }
    staged = {
        line.strip() for line in _git(
            outer, "diff", "--cached", "--name-only"
        ).stdout.splitlines() if line.strip()
    }
    assert committed == {".gitignore"}
    assert staged == {"unrelated.txt"}
    assert _git(outer, "check-ignore", "-q", "new-domain/",
                check=False).returncode == 0


def test_scaffold_dirty_gitignore_refuses_before_target_write(tmp_path):
    outer = _repo(tmp_path / "outer")
    gitignore = outer / ".gitignore"
    gitignore.write_bytes(b"existing/\r\n")
    _git(outer, "add", ".gitignore")
    _git(outer, "commit", "-q", "-m", "seed ignore")
    gitignore.write_bytes(b"existing/\r\noperator-draft/\r\n")
    before = gitignore.read_bytes()
    target = outer / "new-domain"

    with pytest.raises(SystemExit, match="has existing changes"):
        scaffold_mod.cmd_scaffold(
            SimpleNamespace(path=str(target), harness=None))

    assert not target.exists()
    assert gitignore.read_bytes() == before


def test_scaffold_failed_outer_commit_rolls_back_exactly(tmp_path):
    outer = _repo(tmp_path / "outer")
    gitignore = outer / ".gitignore"
    gitignore.write_bytes(b"existing/\r\n")
    (outer / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(outer, "add", ".gitignore", "seed.txt")
    _git(outer, "commit", "-q", "-m", "seed")
    original = gitignore.read_bytes()
    (outer / "operator-draft.txt").write_text("draft\n", encoding="utf-8")
    _git(outer, "add", "operator-draft.txt")
    hook = outer / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\necho operator refusal >&2\nexit 1\n",
                    encoding="utf-8", newline="\n")
    hook.chmod(hook.stat().st_mode | 0o111)
    target = outer / "domains" / "new-domain"

    with pytest.raises(SystemExit, match="all pre-birth writes were rolled back"):
        scaffold_mod.cmd_scaffold(
            SimpleNamespace(path=str(target), harness=None))

    assert gitignore.read_bytes() == original
    assert not target.exists()
    assert not target.parent.exists()
    staged = _git(outer, "diff", "--cached", "--name-only").stdout.splitlines()
    assert staged == ["operator-draft.txt"]


def test_failed_outer_isolation_rollback_preserves_concurrent_gitignore_edit(
        tmp_path, monkeypatch):
    outer = _repo(tmp_path / "outer", commit=True)
    target = outer / "new-domain"
    isolation = scaffold_mod._preflight_outer_isolation(target)
    concurrent = {"bytes": b""}

    def fail_after_operator_edit(self, paths, message):
        gi = outer / ".gitignore"
        concurrent["bytes"] = gi.read_bytes() + b"# operator concurrent edit\n"
        gi.write_bytes(concurrent["bytes"])
        raise RepositoryTransactionError("injected isolation commit failure")

    monkeypatch.setattr(RepositoryTransaction, "commit_exact",
                        fail_after_operator_edit)
    with pytest.raises(SystemExit, match="partial state was preserved"):
        scaffold_mod._initialise_and_isolate(target, isolation)

    assert (outer / ".gitignore").read_bytes() == concurrent["bytes"]
    assert (target / ".git").is_dir()
    assert _git(outer, "log", "-1", "--format=%s").stdout.strip() == "seed"


def _outer_with_operator_index(tmp_path: Path) -> tuple[Path, Path, Path]:
    outer = _repo(tmp_path / "outer", commit=True)
    operator = outer / "operator-draft.txt"
    operator.write_text("operator draft\n", encoding="utf-8")
    _git(outer, "add", operator.name)
    target = outer / "new-domain"
    return outer, target, operator


def _assert_outer_isolation_and_operator_index(
        outer: Path, target: Path, operator: Path) -> None:
    committed = _git(
        outer, "show", "--pretty=format:", "--name-only", "HEAD"
    ).stdout.splitlines()
    assert committed == [".gitignore"]
    assert _git(outer, "diff", "--cached", "--name-only").stdout.splitlines() == [
        operator.name]
    assert _git(outer, "check-ignore", "-q", "--", f"{target.name}/",
                check=False).returncode == 0


def test_scaffold_render_failure_after_isolation_is_truthfully_recoverable(
        tmp_path, monkeypatch, capsys):
    outer, target, operator = _outer_with_operator_index(tmp_path)
    original_write_text = Path.write_text

    def fail_first_domain_render(path, *args, **kwargs):
        if path == target / "AGENTS.md":
            raise OSError("injected render failure")
        return original_write_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_first_domain_render)
    rc = scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness="none"))
    output = capsys.readouterr().out

    assert rc == 1
    assert "stage: domain rendering" in output
    assert "outer isolation commit was erased" in output
    assert "RECOVERY" in output
    assert (target / ".git").is_dir()
    assert _git(target, "rev-parse", "--verify", "-q", "HEAD",
                check=False).returncode != 0
    _assert_outer_isolation_and_operator_index(outer, target, operator)


def test_scaffold_hook_failure_retains_complete_render_and_outer_isolation(
        tmp_path, monkeypatch, capsys):
    outer, target, operator = _outer_with_operator_index(tmp_path)

    def refuse_hook(_target):
        raise SystemExit("injected hook ownership conflict")

    monkeypatch.setattr(scaffold_mod, "install_hook", refuse_hook)
    rc = scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness="none"))
    output = capsys.readouterr().out

    assert rc == 1
    assert "stage: hook installation" in output
    assert "mdllm install-hook" in output
    assert (target / "AGENTS.md").is_file()
    assert _git(target, "rev-parse", "--verify", "-q", "HEAD",
                check=False).returncode != 0
    _assert_outer_isolation_and_operator_index(outer, target, operator)


def test_scaffold_domain_add_failure_preserves_outer_and_unrelated_state(
        tmp_path, monkeypatch, capsys):
    outer, target, operator = _outer_with_operator_index(tmp_path)
    original_run = transaction_mod._run

    def fail_domain_add(root, *args, **kwargs):
        if Path(root).resolve() == target.resolve() and args[:1] == ("add",):
            return subprocess.CompletedProcess(
                ["git", *args], 1, "", "injected exact domain add failure")
        return original_run(root, *args, **kwargs)

    monkeypatch.setattr(transaction_mod, "_run", fail_domain_add)
    rc = scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness="none"))
    output = capsys.readouterr().out

    assert rc == 1
    assert "exact paths could not be staged" in output
    assert "recoverable" in output
    assert _git(target, "rev-parse", "--verify", "-q", "HEAD",
                check=False).returncode != 0
    assert (target / ".git" / "hooks" / "pre-commit").is_file()
    assert "AGENTS.md" in _git(
        target, "status", "--short", "--untracked-files=all").stdout
    _assert_outer_isolation_and_operator_index(outer, target, operator)


def test_scaffold_first_commit_object_failure_is_recoverable_and_exact(
        tmp_path, monkeypatch, capsys):
    outer, target, operator = _outer_with_operator_index(tmp_path)
    original_run = transaction_mod._run

    def fail_domain_commit_tree(root, *args, **kwargs):
        if (Path(root).resolve() == target.resolve()
                and args[:1] == ("commit-tree",)):
            return subprocess.CompletedProcess(
                ["git", *args], 1, "", "injected commit object failure")
        return original_run(root, *args, **kwargs)

    monkeypatch.setattr(transaction_mod, "_run", fail_domain_commit_tree)
    # This test owns commit-object failure, not hook behavior. Hook execution
    # is covered independently above and in runtime tests.
    monkeypatch.setattr(RepositoryTransaction, "_run_hook",
                        lambda self, name, args, env: None)
    rc = scaffold_mod.cmd_scaffold(
        SimpleNamespace(path=str(target), harness="none"))
    output = capsys.readouterr().out

    assert rc == 1
    assert "commit object could not be created" in output
    assert "isolation state remains intact" in output
    assert _git(target, "rev-parse", "--verify", "-q", "HEAD",
                check=False).returncode != 0
    assert _git(target, "diff", "--cached", "--name-only").stdout == ""
    _assert_outer_isolation_and_operator_index(outer, target, operator)


@pytest.mark.parametrize("agents_text", [
    None,
    "# no frontmatter\n",
    "---\ngit: [broken\n---\n",
    "---\nname: x\n---\n",
    "---\ngit:\n  autocommit: true\n---\n",
    "---\ngit:\n  autopush: false\n---\n",
    "---\ngit:\n  autopush: 'true'\n---\n",
    "---\ngit:\n  autopush: false\n  autopush: true\n---\n",
])
def test_autopush_ambiguous_or_absent_authority_is_off(tmp_path, agents_text):
    if agents_text is not None:
        (tmp_path / "AGENTS.md").write_text(agents_text, encoding="utf-8")
    assert sync_mod._autopush_enabled(tmp_path) is False


def test_autopush_requires_literal_true_and_templates_default_off(tmp_path):
    (tmp_path / "AGENTS.md").write_text(
        "---\ngit:\n  autopush: true\n---\n", encoding="utf-8")
    assert sync_mod._autopush_enabled(tmp_path) is True
    assert sync_mod._autopush_enabled(Path(__file__).resolve().parents[2]) is False
    template = (Path(__file__).resolve().parents[2]
                / "templates" / "AGENTS.md.template").read_text(encoding="utf-8")
    assert "autopush: false" in template


def test_sync_git_token_is_command_scoped_not_persisted(tmp_path, monkeypatch):
    observed = {}

    def run(command, **kwargs):
        observed["command"] = command
        observed["env"] = kwargs["env"]
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(transport_mod.subprocess, "run", run)
    token = "github_pat_COMMAND_SCOPED_SECRET"
    result = sync_mod._git(tmp_path, "fetch", "--quiet", token=token)

    assert result.returncode == 0
    rendered = " ".join(observed["command"])
    assert "http.extraheader=Authorization: Basic" in rendered
    assert token not in rendered
    assert token not in observed["env"].values()


def test_sync_repo_passes_token_to_fetch_and_redacts_failure(
        tmp_path, monkeypatch):
    token = "github_pat_SYNC_SECRET"
    fetch_tokens = []

    def completed(args, rc=0, stdout="", stderr=""):
        return subprocess.CompletedProcess(args, rc, stdout, stderr)

    def fake_git(_repo, *args, **kwargs):
        if args == ("remote",):
            return completed(args, stdout="origin\n")
        if args == ("rev-parse", "--git-dir"):
            return completed(args, stdout=".git\n")
        if args == ("rev-parse", "--verify", "-q", "HEAD"):
            return completed(args, stdout="abc\n")
        if args == ("symbolic-ref", "-q", "--short", "HEAD"):
            return completed(args, stdout="main\n")
        if args == ("fetch", "--quiet"):
            fetch_tokens.append(kwargs.get("token"))
            return completed(args, rc=1, stderr=f"fatal: undiagnosed {token}")
        if args == ("rev-list", "--left-right", "--count",
                    "HEAD...@{upstream}"):
            return completed(args, stdout="0 0\n")
        if args == ("status", "--porcelain"):
            return completed(args)
        raise AssertionError(args)

    monkeypatch.setattr(sync_mod, "_git", fake_git)
    result = sync_mod.sync_repo(tmp_path, token=token)

    assert fetch_tokens == [token]
    assert result.state is sync_mod.SyncState.FETCH_FAILED
    assert token not in result.detail
    assert "[REDACTED]" in result.detail


def test_sync_result_is_frozen_and_rejects_impossible_movement(tmp_path):
    result = sync_mod.SyncResult(
        repo=tmp_path,
        state=sync_mod.SyncState.UP_TO_DATE,
    )

    with pytest.raises(FrozenInstanceError):
        result.detail = "changed"
    with pytest.raises(ValueError, match="only a synced result"):
        sync_mod.SyncResult(
            repo=tmp_path,
            state=sync_mod.SyncState.DIRTY,
            moved=True,
        )


def test_git_transport_has_one_neutral_owner():
    assert sync_mod.git_command is transport_mod.git_command
    assert assemble_mod.git_command is transport_mod.git_command
    assert publish_mod.git_command is transport_mod.git_command
    assert sync_mod.redact is transport_mod.redact
    assert assemble_mod.redact is transport_mod.redact
    assert publish_mod.redact is transport_mod.redact
