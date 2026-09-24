"""Dependency-free transport for an existing hosted checkout.

This file is also distributed verbatim as bootstrap.py. It must run before
the framework or PyYAML exists; the pinned framework owns everything after
transport. Configuration is strict JSON so no second YAML parser is needed.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate configuration key: {key}")
        result[key] = value
    return result


def load_config(path: Path) -> dict:
    config = json.loads(path.read_text(encoding="utf-8"),
                        object_pairs_hook=unique_object)
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    fields = {"schema_version", "framework_repo", "framework_commit",
              "domain_repo", "workspace_directory", "publication"}
    if not isinstance(config, dict) or set(config) != fields:
        raise ValueError("environment.json has missing or unknown fields")
    if type(config["schema_version"]) is not int or config["schema_version"] != 1:
        raise ValueError("unsupported environment schema_version")
    for key in fields - {"schema_version"}:
        if not isinstance(config[key], str):
            raise ValueError(f"{key} must be a string")
    for key in ("framework_repo", "domain_repo"):
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git",
                            config[key]):
            raise ValueError(f"{key} must be a credential-free GitHub HTTPS URL")
    if not re.fullmatch(r"[0-9a-f]{40}", config["framework_commit"]):
        raise ValueError("framework_commit must be a full lowercase commit SHA")
    workspace = PurePosixPath(config["workspace_directory"])
    if (not workspace.is_absolute() or ".." in workspace.parts
            or len(workspace.parts) < 4
            or workspace.name not in {"domain", "domains"}
            or str(workspace) != config["workspace_directory"]):
        raise ValueError("workspace_directory must be an absolute nested domain(s) directory")
    if config["publication"] != "pr":
        raise ValueError("this hosted profile supports publication: pr only")


def run(command: list[str], *, cwd: Path | None = None,
        timeout: int = 180) -> str:
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=timeout)
    if result.returncode:
        # Do not echo ambient Git credentials or proxy error pages.
        raise ValueError(f"{Path(command[0]).name} {command[1]} failed "
                         f"(exit {result.returncode}); inspect the command locally")
    return result.stdout.strip()


def git(root: Path, *args: str) -> str:
    return run(["git", "-C", str(root), *args])


def canonical_remote(value: str) -> str:
    match = re.fullmatch(r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/]+/[^/]+?)(?:\.git)?/?", value)
    return f"https://github.com/{match[1]}.git" if match else value


def existing_domain(config: dict, domain: Path) -> Path:
    """Check exact ownership and layout before touching a parent directory."""
    domain = domain.absolute()
    if domain != domain.resolve() or not (domain / ".git").is_dir():
        raise ValueError("hosted domain must be a real independent clone, without symlink ancestors")
    if Path(git(domain, "rev-parse", "--show-toplevel")).resolve() != domain:
        raise ValueError("domain path is not its repository root")
    if domain.parent.as_posix() != config["workspace_directory"]:
        raise ValueError("checkout is outside workspace_directory; correct the environment setting")
    if canonical_remote(git(domain, "config", "--get", "remote.origin.url")) != config["domain_repo"]:
        raise ValueError("checkout origin differs from domain_repo")
    expected_name = config["domain_repo"].rsplit("/", 1)[1].removesuffix(".git")
    if domain.name != expected_name:
        raise ValueError("checkout directory differs from the repository name")
    return domain.parent.parent


def materialise(config: dict, domain: Path) -> Path:
    """Surround the existing clone without moving or checking it out."""
    root = existing_domain(config, domain)
    pin = config["framework_commit"]
    if (root / ".git").exists():
        if not (root / ".git").is_dir() or git(root, "rev-parse", "HEAD") != pin:
            raise ValueError("cached framework differs from the pin; reset the environment cache")
        if canonical_remote(git(root, "config", "--get", "remote.origin.url")) != config["framework_repo"]:
            raise ValueError("cached framework origin differs from framework_repo")
        if git(root, "status", "--porcelain", "--untracked-files=normal"):
            raise ValueError("cached framework has changes; inspect it before resetting the cache")
    else:
        # Only the host-created domain container may already occupy this root.
        if set(p.name for p in root.iterdir()) != {domain.parent.name}:
            raise ValueError("framework destination contains unrelated files; refusing to overwrite")
        with tempfile.TemporaryDirectory(prefix="mdllm-bootstrap-", dir=root.parent) as temp:
            checkout = Path(temp) / "framework"
            checkout.mkdir()
            git(checkout, "init", "--quiet")
            git(checkout, "remote", "add", "origin", config["framework_repo"])
            git(checkout, "fetch", "--quiet", "--depth", "1", "origin", pin)
            if git(checkout, "rev-parse", "FETCH_HEAD") != pin:
                raise ValueError("fetched framework does not match the requested pin")
            git(checkout, "checkout", "--quiet", "--detach", pin)
            required = (".markdownllm", "kernel.md", "tools/mdllm.py",
                        "tools/markdownllm/cloud_workspace.py")
            if any(not (checkout / p).is_file() for p in required):
                raise ValueError("pinned source does not contain the hosted workspace floor")
            relative = domain.relative_to(root).as_posix()
            if git(checkout, "ls-files", "--", domain.parent.name):
                raise ValueError("framework tracks the domain container")
            git(checkout, "check-ignore", "--no-index", "--", relative + "/AGENTS.md")
            entries = list(checkout.iterdir())
            if any((root / p.name).exists() for p in entries):
                raise ValueError("framework source collides with existing workspace content")
            moved = []
            try:
                for source in entries:
                    destination = root / source.name
                    source.rename(destination)
                    moved.append((source, destination))
            except BaseException:
                for source, destination in reversed(moved):
                    destination.rename(source)
                raise
    git(root, "check-ignore", "--no-index", "--",
        domain.relative_to(root).as_posix() + "/AGENTS.md")
    if (root / "tools/markdownllm/cloud_bootstrap.py").read_text(encoding="utf-8") != Path(__file__).read_text(encoding="utf-8"):
        raise ValueError("bootstrap differs from pinned source; regenerate the complete bundle")
    return root


def ensure_runtime(root: Path) -> Path:
    environment = root / ".venv"
    if environment.is_symlink():
        raise ValueError("framework .venv must not be a symlink")
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not environment.exists():
        run([sys.executable, "-m", "venv", str(environment)])
    if not python.is_file():
        raise ValueError("existing framework .venv has no interpreter")
    probe = [str(python), "-c",
             "import yaml; assert yaml.__version__ == '6.0.3'"]
    try:
        run(probe)
    except ValueError:
        run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
             "PyYAML==6.0.3"])
        run(probe)
    return python


def main() -> int:
    try:
        mode = sys.argv[1] if len(sys.argv) == 2 else "setup" if len(sys.argv) == 1 else ""
        if mode not in {"setup", "maintenance"}:
            raise ValueError("usage: bootstrap.py [setup|maintenance]")
        config_path = Path(__file__).resolve().with_name("environment.json")
        config = load_config(config_path)
        domain = Path(run(["git", "rev-parse", "--show-toplevel"]))
        root = materialise(config, domain)
        python = ensure_runtime(root)
        command = [str(python), str(root / "tools/mdllm.py"), "cloud", "prepare",
                   str(domain), "--config", str(config_path)]
        if mode == "maintenance":
            command.append("--maintenance")
        return subprocess.run(command, cwd=domain, check=False).returncode
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"workspace bootstrap: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
