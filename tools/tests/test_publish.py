"""Phase 2 of the ``cowork-adapter`` plan: the guarded publication leg.

Ported guard-for-guard from the bootstrap plugin's ``push.sh`` /
``default-branch.sh`` and pinned here so the floor owns them under test:

1. branch READ (mdllm.defaultbranch / origin HEAD), never typed;
2. checkout must be on that branch, and not detached;
3. the remote ref must already exist — publish NEVER creates a branch;
4. fast-forward only — a rejected push refuses, and the refusal says
   never to force;
5. the remote tip is re-read and must equal the local commit.

The fixture remote's default branch is deliberately NOT ``main`` — the
most expensive silent failure this guards against is the main-assumption.

Run: python -m pytest tools/tests/test_publish.py -q
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.git_transport import redact  # noqa: E402
from markdownllm.publish import publish, resolve_default_branch  # noqa: E402


def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True, check=True)


def _commit(repo: Path, name: str) -> None:
    (repo / name).write_text(name + "\n", encoding="utf-8")
    _run(repo, "add", name)
    _run(repo, "commit", "-q", "-m", f"add {name}")


@pytest.fixture()
def estate(tmp_path):
    """A bare origin whose default branch is 'trunk' (not main), a clone."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
    subprocess.run(["git", "-C", str(origin), "symbolic-ref", "HEAD",
                    "refs/heads/trunk"], check=True)

    seed = tmp_path / "seed"
    subprocess.run(["git", "init", "-q", "-b", "trunk", str(seed)], check=True)
    _run(seed, "config", "user.email", "t@t")
    _run(seed, "config", "user.name", "t")
    _commit(seed, "first.txt")
    _run(seed, "remote", "add", "origin", str(origin))
    _run(seed, "push", "-q", "origin", "trunk")

    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)],
                   check=True)
    _run(clone, "config", "user.email", "t@t")
    _run(clone, "config", "user.name", "t")
    (clone / "AGENTS.md").write_text(
        "---\ngit:\n  autopush: true\n---\n\n# Test Domain\n",
        encoding="utf-8",
    )
    return origin, clone


def _origin_heads(origin: Path) -> dict[str, str]:
    out = subprocess.run(["git", "-C", str(origin), "show-ref", "--heads"],
                         capture_output=True, text=True).stdout
    return {line.split()[1].removeprefix("refs/heads/"): line.split()[0]
            for line in out.splitlines() if line.strip()}


# -------------------------------------------------------------- resolution

def test_branch_is_read_from_clone_state_never_guessed(estate):
    origin, clone = estate
    branch, _ = resolve_default_branch(clone)
    assert branch == "trunk"          # the remote's own HEAD, not "main"


def test_recorded_config_wins_over_symref(estate):
    _, clone = estate
    _run(clone, "config", "mdllm.defaultbranch", "trunk")
    branch, _ = resolve_default_branch(clone)
    assert branch == "trunk"


def test_resolution_refuses_rather_than_guesses(estate):
    _, clone = estate
    _run(clone, "remote", "set-head", "origin", "--delete")
    branch, why = resolve_default_branch(clone)
    assert branch is None
    assert "DO NOT assume 'main'" in why


# ------------------------------------------------------------------ guards

def test_publish_pushes_and_verifies(estate, capsys):
    origin, clone = estate
    _commit(clone, "second.txt")
    local = _run(clone, "rev-parse", "HEAD").stdout.strip()

    assert publish(clone) == 0
    out = capsys.readouterr().out
    assert "verified — origin/trunk" in out
    assert _origin_heads(origin)["trunk"] == local


def test_nothing_to_push_is_calm(estate, capsys):
    _, clone = estate
    assert publish(clone) == 0
    assert "nothing to push" in capsys.readouterr().out


@pytest.mark.parametrize("agents", [
    "# no policy\n",
    "---\ngit:\n  autopush: false\n---\n",
    "---\ngit:\n  autopush: 'true'\n---\n",
])
def test_publish_refuses_without_explicit_authority_before_remote_contact(
        estate, capsys, agents):
    origin, clone = estate
    (clone / "AGENTS.md").write_text(agents, encoding="utf-8")
    _commit(clone, "withheld.txt")
    before = _origin_heads(origin)["trunk"]

    assert publish(clone) == 3

    out = capsys.readouterr().out
    assert "publication authority is off" in out
    assert "No remote was contacted" in out
    assert _origin_heads(origin)["trunk"] == before


def test_one_shot_human_authority_publishes_without_changing_policy(
        estate, capsys):
    origin, clone = estate
    (clone / "AGENTS.md").write_text(
        "---\ngit:\n  autopush: false\n---\n", encoding="utf-8")
    _commit(clone, "operator-approved.txt")
    local = _run(clone, "rev-parse", "HEAD").stdout.strip()

    assert publish(clone, authorize_once=True) == 0

    out = capsys.readouterr().out
    assert "one-shot authority supplied" in out
    assert _origin_heads(origin)["trunk"] == local
    assert "autopush: false" in (clone / "AGENTS.md").read_text(encoding="utf-8")


def test_refuses_from_the_wrong_branch(estate, capsys):
    origin, clone = estate
    _run(clone, "checkout", "-q", "-b", "feature")
    _commit(clone, "second.txt")
    assert publish(clone) == 3
    out = capsys.readouterr().out
    assert "checked out on 'feature'" in out
    assert list(_origin_heads(origin)) == ["trunk"]   # nothing created


def test_never_creates_a_remote_branch(estate, capsys):
    """The load-bearing guard: a push toward a missing remote ref would
    CREATE it and report success. publish refuses instead."""
    origin, clone = estate
    _run(clone, "checkout", "-q", "-b", "mian")       # the classic typo
    _run(clone, "config", "mdllm.defaultbranch", "mian")
    # Fake local corroboration for the wrong name so guard 3 is what fires.
    _run(clone, "update-ref", "refs/remotes/origin/mian",
         _run(clone, "rev-parse", "HEAD").stdout.strip())
    _commit(clone, "second.txt")

    assert publish(clone) == 3
    out = capsys.readouterr().out
    assert "never creates remote branches" in out
    assert list(_origin_heads(origin)) == ["trunk"]   # no stray branch


def test_refuses_detached_head(estate, capsys):
    _, clone = estate
    _run(clone, "checkout", "-q", "--detach")
    assert publish(clone) == 3
    assert "detached HEAD" in capsys.readouterr().out


def test_non_fast_forward_refuses_and_never_forces(estate, capsys, tmp_path):
    origin, clone = estate
    # A second clone moves origin ahead...
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(origin), str(other)],
                   check=True)
    _run(other, "config", "user.email", "t@t")
    _run(other, "config", "user.name", "t")
    _commit(other, "theirs.txt")
    _run(other, "push", "-q", "origin", "trunk")
    ahead = _run(other, "rev-parse", "HEAD").stdout.strip()

    # ...while this clone commits divergently without fetching.
    _commit(clone, "ours.txt")
    assert publish(clone) == 3
    out = capsys.readouterr().out
    assert "Do not retry with --force" in out
    assert _origin_heads(origin)["trunk"] == ahead    # remote untouched


def test_not_a_repo_is_usage_error(tmp_path, capsys):
    assert publish(tmp_path / "void") == 2


# --------------------------------------------------------------- redaction

def test_redaction_strips_every_credential_shape():
    token = "github_pat_11AAAA0000bbbbCCCCddddEEEE"
    import base64
    header = base64.b64encode(
        f"x-access-token:{token}".encode()).decode()
    line = f"fatal: auth {token} basic {header} ghp_zzzz9999"
    cleaned = redact(line, token)
    assert token not in cleaned
    assert header not in cleaned
    assert "ghp_zzzz9999" not in cleaned
    assert cleaned.count("[REDACTED]") >= 3
