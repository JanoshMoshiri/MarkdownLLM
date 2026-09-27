"""An explicit cloud workspace, not a second domain or publication engine.

The host owns the primary checkout. Extra repositories remain independent;
the existing domain floor and publication policy retain their authority.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

from .cloud_bootstrap import auth_options, canonical_remote, git, install_credentials, primary_spec, run


def layout(config: dict, primary: Path) -> list[tuple[dict, Path]]:
    entry = dict(primary_spec(config), name=primary.name, access="write", publication="pr")
    result = [(entry, primary)]
    root = primary.parent.parent
    for spec in config.get("repositories", []):
        folder = "domains" if spec["kind"] == "domain" else "repositories"
        target = root / folder / spec["name"]
        if target.absolute() != target.resolve():
            raise ValueError("repository paths must not have symlink ancestors")
        result.append((spec, target))
    return result


def check_clone(path: Path, entry: dict) -> None:
    if (path.absolute() != path.resolve() or not (path / ".git").is_dir()
            or Path(git(path, "rev-parse", "--show-toplevel")).resolve() != path):
        raise ValueError(f"{entry['name']}: expected an independent repository, not a symlink or worktree")
    if canonical_remote(git(path, "config", "--get", "remote.origin.url")) != entry["repo"]:
        raise ValueError(f"{entry['name']}: origin differs from the declared repository")


def complete_history(path: Path, entry: dict, *, primary=False) -> None:
    auth_options(entry)  # A configured credential must exist in this phase.
    origin = subprocess.run(["git", "-C", str(path), "config", "--get", "remote.origin.url"],
                            capture_output=True, text=True, check=False)
    if primary and origin.returncode == 1:
        git(path, "remote", "add", "origin", entry["repo"])
        print(f"{entry['name']}: restored missing origin from the explicit manifest")
    check_clone(path, entry)
    install_credentials(path, entry)
    if git(path, "rev-parse", "--is-shallow-repository") == "true":
        git(path, *auth_options(entry), "fetch", "--quiet", "--unshallow", "origin")
        if git(path, "rev-parse", "--is-shallow-repository") != "false":
            raise ValueError(f"{entry['name']}: history remains shallow; preparation is incomplete")


def assemble_extra(root: Path, entry: dict, path: Path, *, maintenance: bool) -> None:
    # The published substrate must already exclude both repo classes. Never
    # edit its tracked .gitignore or commit an operator's repositories into it.
    git(root, "check-ignore", "--no-index", "--", path.relative_to(root).as_posix() + "/AGENTS.md")
    revision = entry["revision"]
    branch = revision.get("branch")
    if branch:
        git(root, "check-ref-format", "--branch", branch)
    if not path.exists():
        options = auth_options(entry)  # Fail missing credentials before writing.
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="mdllm-cloud-clone-", dir=path.parent) as temporary:
            checkout = Path(temporary) / "checkout"
            run(["git", *options, "clone", "--quiet", "--no-checkout", "--", entry["repo"], str(checkout)])
            if branch:
                git(checkout, "checkout", "--quiet", branch)
            else:
                pin = revision["commit"]
                git(checkout, *options, "fetch", "--quiet", "origin", pin)
                git(checkout, "checkout", "--quiet", "--detach", pin)
            if path.exists():
                raise ValueError(f"{entry['name']}: destination appeared during clone; refusing replacement")
            checkout.rename(path)
    check_clone(path, entry)
    if git(path, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"{entry['name']}: cached repository has drafts; preserve them before rebuilding")
    complete_history(path, entry)
    if branch:
        if git(path, "rev-parse", "--abbrev-ref", "HEAD") != branch:
            raise ValueError(f"{entry['name']}: cached branch differs; refusing checkout")
        if maintenance:
            git(path, *auth_options(entry), "fetch", "--quiet", "origin")
            # Fast-forward only. Local commits are kept; divergence is a stop.
            git(path, "merge", "--ff-only", "--no-edit", f"refs/remotes/origin/{branch}")
    elif git(path, "rev-parse", "HEAD") != revision["commit"]:
        raise ValueError(f"{entry['name']}: cached pin differs; refusing reset")


def provision_boundary(path: Path, entry: dict) -> None:
    variable = entry.get("boundary_terms_env")
    if not variable:
        if not (path / ".boundary-terms").is_file():
            print(f"{entry['name']}: disclosure vocabulary not provisioned; no boundary coverage claimed")
        return
    value = os.environ.get(variable)
    if not value or not value.strip():
        raise ValueError(f"{entry['name']}: required boundary variable {variable} is unavailable")
    target = path / ".boundary-terms"
    git(path, "check-ignore", "--", ".boundary-terms")
    if target.is_symlink():
        raise ValueError("refusing symlink boundary vocabulary")
    data = value.encode("utf-8")
    if target.exists():
        if target.read_bytes() != data:
            raise ValueError(f"{entry['name']}: boundary vocabulary differs; review the existing file")
        return
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)


def probe(config: dict, primary: Path) -> int:
    """Read-only authentication test. Success never asserts write permission."""
    failed = False
    for entry, path in layout(config, primary):
        try:
            check_clone(path, entry)
            run(["git", "-C", str(path), *auth_options(entry), "ls-remote", "origin", "HEAD"], timeout=30)
            print(f"{entry['name']}: remote read succeeded (write permission not tested)")
        except (OSError, ValueError, subprocess.SubprocessError):
            failed = True
            print(f"{entry['name']}: remote read unavailable; check network and this phase's credentials")
    return int(failed)


def status(config: dict, primary: Path) -> int:
    """Local status only. Never turn missing upstream data into 'no debt'."""
    from .sync import publication_policy
    attention = False
    for entry, path in layout(config, primary):
        try:
            check_clone(path, entry)
            head = git(path, "rev-parse", "HEAD")
            branch = git(path, "rev-parse", "--abbrev-ref", "HEAD")
            dirty = bool(git(path, "status", "--porcelain", "--untracked-files=all"))
            shallow = git(path, "rev-parse", "--is-shallow-repository") == "true"
            policy = publication_policy(path)
            print(f"{entry['name']}: {entry['kind']}, {entry['access']}, {branch}@{head[:12]}, "
                  f"drafts={dirty}, shallow={shallow}, automatic publication={policy.enabled}")
            if path == primary:
                print("  host-managed result: review the selected repository's Codex diff/PR; not a multi-repo receipt")
            variable = entry.get("credential_env")
            print(f"  credentials: {variable} {'available' if os.environ.get(variable) else 'unavailable'} in this phase"
                  if variable else "  credentials: native Git, availability unverified (use cloud probe)")
            if entry["access"] == "read" and "commit" in entry.get("revision", {}):
                changed = head != entry["revision"]["commit"]
                print("  read-only intent, pinned reference: " + ("HEAD CHANGED" if changed else "pin unchanged"))
                attention |= dirty or shallow or changed
                continue
            if path == primary:
                print("  host PR state: inspect in Codex; this local command cannot verify it")
                attention |= dirty or shallow
                continue
            try:
                counts = git(path, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
                ahead, behind = (int(n) for n in counts.split())
                print(f"  cached upstream: {ahead} ahead / {behind} behind; remote freshness not checked")
                attention |= bool(ahead or behind)
            except (ValueError, subprocess.SubprocessError):
                print("  publication debt UNKNOWN: no usable upstream comparison")
                attention = True
            attention |= dirty or shallow
        except (OSError, ValueError, subprocess.SubprocessError):
            print(f"{entry['name']}: unavailable; no clean-state or publication claim")
            attention = True
    return int(attention)
