"""Guarded publication — Phase 2 of the ``cowork-adapter`` plan.

``mdllm publish <repo>`` pushes the current commit to the repo's REAL
default branch with every guard that stops a guessed branch name from
doing damage. Ported guard-for-guard from the bootstrap plugin's
``push.sh``/``default-branch.sh`` (v0.4.0), which proved the mechanics in
the field; the floor owns them now so they are tested, versioned with the
framework, and available to every harness.

Why this exists: ``git push origin HEAD:refs/heads/mian`` does not fail.
It creates a branch called ``mian`` on the remote, reports success, and
the work becomes invisible — to the operator, to CI, and to the next
session. Prose cannot prevent that reliably; a refusal-first command can.

Authority and guards, in order:

0. Publication is authorized by literal ``git.autopush: true`` or an explicit
   one-shot operator instruction (``--authorize-once``).  False, absent,
   malformed, and unreadable policy refuse before any remote contact.
1. The branch name is READ — ``mdllm.defaultbranch`` git config (recorded
   at assembly from the remote's own HEAD) or ``refs/remotes/origin/HEAD``
   (set by clone) — never typed, never guessed, no fallback to ``main``.
2. The local checkout must be ON that branch (and not detached).
3. The branch must ALREADY exist on the remote. This command never
   creates a remote branch; a missing ref is a stop, not an invitation.
4. Plain fast-forward push — no ``--force``, no ``--force-with-lease``.
5. The remote tip is re-read afterwards and must equal the local commit.

Two credential modes, one command:

- **ambient** (default): the environment's own git credentials — a local
  clone with a credential helper, SSH, or an already-authenticated CI.
- **env-scoped**: when ``GH_PAT`` (or ``MDLLM_GIT_TOKEN``) is set, it is
  supplied through a command-scoped HTTP header — never written to disk,
  never placed in ``.git/config`` or a URL, and redacted from every line
  this module prints. This is the ephemeral-container mode, where ambient
  credentials do not exist by design and the post-commit autopush leg
  honestly fails.

Exit codes: 0 = pushed and verified (or nothing to push); 2 = usage;
3 = a guard refused — read the message, never route around it.
"""

from __future__ import annotations

from pathlib import Path

from .git_transport import command_token, git_command, redact


def resolve_default_branch(repo: Path) -> tuple[str | None, str]:
    """The repo's real default branch, READ — or (None, why-not).

    Resolution order: ``mdllm.defaultbranch`` (recorded from the remote's
    own HEAD at assembly) then ``refs/remotes/origin/HEAD`` (set by
    clone). There is deliberately NO guess: a wrong branch name is worse
    than a hard stop.
    """
    recorded = git_command(repo, "config", "--get", "mdllm.defaultbranch")
    branch = recorded.stdout.strip()
    if not branch:
        symref = git_command(repo, "symbolic-ref", "--short",
                             "refs/remotes/origin/HEAD")
        branch = symref.stdout.strip().removeprefix("origin/")
    if not branch:
        return None, (
            "neither mdllm.defaultbranch (git config) nor "
            "refs/remotes/origin/HEAD is set. DO NOT assume 'main' or "
            "'master'. Re-derive from the remote "
            "(`git remote set-head origin --auto`) or ask the operator "
            "which branch is authoritative, then record it: "
            "`git config mdllm.defaultbranch <branch>`")
    verify = git_command(repo, "show-ref", "--verify", "--quiet",
                         f"refs/remotes/origin/{branch}")
    if verify.returncode != 0:
        return None, (
            f"resolved {branch!r} but refs/remotes/origin/{branch} does "
            "not exist locally — refusing to act on a name the remote "
            "state does not corroborate")
    return branch, ""


def publish(repo: Path, *, authorize_once: bool = False) -> int:
    token = command_token()

    def say(line: str) -> None:
        print(redact(line, token))

    repo = Path(repo).resolve()
    inside = git_command(repo, "rev-parse", "--git-dir")
    if inside.returncode != 0:
        say(f"publish: {repo} is not a git repository")
        return 2

    # -- 0. sending authority must be explicit --------------------------
    # Publication policy remains a sync-owned port.  Generic Git transport is
    # neutral, so this one-way application dependency cannot form a cycle.
    from .sync import publication_policy
    policy = publication_policy(repo)
    if not policy.enabled and not authorize_once:
        say(f"publish: ABORT — publication authority is off: {policy.reason}. "
            "A human may either declare literal git.autopush: true as standing "
            "authority or explicitly instruct this one event and invoke "
            "`mdllm publish --authorize-once`. No remote was contacted.")
        return 3
    if authorize_once and not policy.enabled:
        say("publish: one-shot authority supplied for this invocation; the "
            "repository's standing publication policy remains off.")

    # -- 1. the branch is read, never typed ------------------------------
    branch, why_not = resolve_default_branch(repo)
    if branch is None:
        say(f"publish: ABORT — {why_not}")
        return 3

    local = git_command(repo, "rev-parse", "HEAD")
    if local.returncode != 0:
        say("publish: no commits to publish")
        return 3
    local_sha = local.stdout.strip()

    # -- 2. the checkout must be on that branch --------------------------
    current = git_command(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if current == "HEAD":
        say("publish: ABORT — detached HEAD; check out the default branch "
            f"({branch}) before publishing")
        return 3
    if current != branch:
        say(f"publish: ABORT — checked out on {current!r} but this repo's "
            f"default branch is {branch!r}. Publishing one onto the other "
            "is exactly the mistake this guards. Resolve with the "
            "operator before pushing.")
        return 3

    # -- 3. the branch must already exist on the remote ------------------
    listed = git_command(repo, "ls-remote", "origin", f"refs/heads/{branch}",
                         token=token)
    if listed.returncode != 0:
        say(f"publish: ABORT — could not reach origin to verify "
            f"refs/heads/{branch}: {listed.stderr.strip()}")
        return 3
    remote_sha = next((line.split()[0] for line in
                       listed.stdout.splitlines() if line.strip()), "")
    if not remote_sha:
        say(f"publish: ABORT — refs/heads/{branch} does not exist on "
            "origin. This command never creates remote branches. If the "
            "name is genuinely wrong, re-derive it "
            "(`git remote set-head origin --auto`) or ask the operator "
            "which branch is authoritative.")
        return 3

    if remote_sha == local_sha:
        say(f"publish: origin/{branch} is already at {local_sha[:8]} — "
            "nothing to push.")
        return 0

    # -- 4. plain fast-forward push --------------------------------------
    say(f"publish: -> origin/{branch}  ({remote_sha[:8]} -> {local_sha[:8]})")
    pushed = git_command(repo, "push", "origin", f"HEAD:refs/heads/{branch}",
                         token=token)
    if pushed.returncode != 0:
        say(pushed.stderr.strip() or pushed.stdout.strip())
        say("publish: FAILED — the remote rejected the push. Do not retry "
            "with --force; a rejected publish is divergence, and routing "
            "it is the operator's decision.")
        return 3

    # -- 5. the remote must actually have moved --------------------------
    verify = git_command(repo, "ls-remote", "origin", f"refs/heads/{branch}",
                         token=token)
    verified_sha = next((line.split()[0] for line in
                         verify.stdout.splitlines() if line.strip()), "")
    if verified_sha != local_sha:
        say(f"publish: VERIFY FAILED — origin/{branch} is at "
            f"{verified_sha or '<missing>'}, expected {local_sha}.")
        return 3

    say(f"publish: verified — origin/{branch} is now at {local_sha[:8]}.")
    return 0


def cmd_publish(args) -> int:
    return publish(
        Path(args.path),
        authorize_once=bool(getattr(args, "authorize_once", False)),
    )
