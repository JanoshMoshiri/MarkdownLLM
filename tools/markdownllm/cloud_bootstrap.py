"""Dependency-free transport for an existing hosted checkout.

This file is also distributed verbatim as bootstrap.py. It must run before
the framework or PyYAML exists; the pinned framework owns everything after
transport. Configuration is strict JSON so no second YAML parser is needed.
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import shlex
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
    if isinstance(config, dict) and type(config.get("schema_version")) is int and config["schema_version"] == 2:
        validate_estate_config(config)
        return
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


def repository_url(value) -> None:
    if not isinstance(value, str) or not re.fullmatch(
            r"https://github\.com/[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+\.git", value):
        raise ValueError("repository must be a credential-free GitHub HTTPS URL")
    if value.rsplit("/", 1)[1].removesuffix(".git") in {"", ".", "..", ".git"}:
        raise ValueError("invalid repository name")


def validate_credential_name(value) -> None:
    if value is not None and (not isinstance(value, str) or not re.fullmatch(
            r"[A-Z_][A-Z0-9_]{0,127}", value)):
        raise ValueError("credential/boundary configuration names an environment variable, never its value")


def validate_estate_config(config: dict) -> None:
    if set(config) != {"schema_version", "framework_repo", "framework_commit",
                       "workspace_directory", "primary", "repositories"}:
        raise ValueError("environment.json has missing or unknown fields")
    repository_url(config["framework_repo"])
    if not isinstance(config["framework_commit"], str) or not re.fullmatch(r"[0-9a-f]{40}", config["framework_commit"]):
        raise ValueError("framework_commit must be a full lowercase commit SHA")
    workspace = config["workspace_directory"]
    if not isinstance(workspace, str):
        raise ValueError("workspace_directory must be a string")
    path = PurePosixPath(workspace)
    if (not path.is_absolute() or len(path.parts) < 4 or ".." in path.parts
            or path.name not in {"domain", "domains", "repositories"}
            or str(path) != workspace):
        raise ValueError("workspace_directory must end in domain(s) or repositories beneath the framework")
    primary = config["primary"]
    base_fields = {"repo", "kind", "credential_env", "boundary_terms_env"}
    if not isinstance(primary, dict) or set(primary) != base_fields:
        raise ValueError("primary has missing or unknown fields")
    entries = config["repositories"]
    if not isinstance(entries, list):
        raise ValueError("repositories must be a list")
    names = {primary["repo"].rsplit("/", 1)[-1].removesuffix(".git")} if isinstance(primary["repo"], str) else set()
    urls = set()
    for entry in [primary, *entries]:
        required = base_fields if entry is primary else base_fields | {"name", "revision", "access", "publication"}
        if not isinstance(entry, dict) or set(entry) != required:
            raise ValueError("repository entry has missing or unknown fields")
        repository_url(entry["repo"])
        if entry["repo"].lower() in urls:
            raise ValueError("duplicate repository")
        urls.add(entry["repo"].lower())
        if entry["kind"] not in {"domain", "repository"}:
            raise ValueError("kind must be domain or repository")
        for field in ("credential_env", "boundary_terms_env"):
            validate_credential_name(entry[field])
        if entry["kind"] != "domain" and entry["boundary_terms_env"] is not None:
            raise ValueError("boundary_terms_env belongs only to a domain")
        if entry is primary:
            if (path.name == "repositories") != (entry["kind"] == "repository"):
                raise ValueError("workspace_directory does not match primary kind")
            continue
        name = entry["name"]
        if (not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", name)
                or name.lower() in {n.lower() for n in names}):
            raise ValueError("repository names must be safe, unique directory names")
        names.add(name)
        revision = entry["revision"]
        if not isinstance(revision, dict) or len(revision) != 1 or not set(revision) <= {"commit", "branch"}:
            raise ValueError("revision must name exactly one commit or branch")
        value = next(iter(revision.values()))
        if not isinstance(value, str):
            raise ValueError("revision must be a string")
        if "commit" in revision and not re.fullmatch(r"[0-9a-f]{40}", value):
            raise ValueError("revision.commit must be a full lowercase SHA")
        if "branch" in revision and (not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9/_.-]*", value)
                or any(s in value for s in ("..", "//", ".lock")) or value.endswith(("/", "."))):
            raise ValueError("invalid revision.branch")
        if entry["access"] not in {"read", "write"} or entry["publication"] not in {"manual", "declared"}:
            raise ValueError("invalid access or publication policy")
        if entry["access"] == "write" and "branch" not in revision:
            raise ValueError("writable repositories require an explicit branch")
        if entry["publication"] == "declared" and (entry["access"] != "write" or entry["kind"] != "domain"):
            raise ValueError("declared publication requires a writable domain; it cannot grant authority")


def primary_spec(config: dict) -> dict:
    if config["schema_version"] == 2:
        return config["primary"]
    return dict(repo=config["domain_repo"], kind="domain", credential_env=None,
                boundary_terms_env=None)


def manifest_digest(config: dict) -> str:
    return hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()


def assert_recorded_manifest(root: Path, config: dict) -> None:
    if config["schema_version"] != 2:
        return
    recorded = subprocess.run(["git", "-C", str(root), "config", "--local",
                               "--get", "mdllm.cloud.manifest"],
                              capture_output=True, text=True, check=False)
    if recorded.returncode != 0 or recorded.stdout.strip() != manifest_digest(config):
        raise ValueError("workspace manifest differs from the prepared cache; review and reset it")


def credential_helper(variable: str, url: str) -> str:
    validate_credential_name(variable)
    repository_url(url)
    return "!" + shlex.join([sys.executable, str(Path(__file__).resolve()),
                            "credential", variable, url])


def credential_response(variable: str, url: str, operation: str) -> int:
    """Git credential protocol: only this HTTPS repository, never store/erase.

    Configuration contains the variable NAME only. Git consumes the response;
    bootstrap logs never receive it. No token is persisted or placed in argv.
    """
    validate_credential_name(variable)
    repository_url(url)
    if operation != "get":
        return 0
    request = dict(line.rstrip("\n").split("=", 1) for line in sys.stdin
                   if "=" in line)
    expected = url.removeprefix("https://github.com/").removesuffix(".git")
    if (request.get("protocol") != "https" or request.get("host") != "github.com"
            or request.get("path", "").removesuffix(".git") != expected):
        return 0
    token = os.environ.get(variable, "")
    if token and not any(c in token for c in "\r\n\0"):
        print("username=x-access-token\npassword=" + token)
    return 0


def auth_options(entry: dict) -> list[str]:
    variable = entry.get("credential_env")
    if not variable:
        return []  # Native Git credentials, if the host actually supplies them.
    if not os.environ.get(variable):
        raise ValueError(f"credential environment variable {variable} is unavailable in this phase")
    return ["-c", "credential.helper=", "-c", "credential.useHttpPath=true",
            "-c", "credential.helper=" + credential_helper(variable, entry["repo"])]


def install_credentials(repo: Path, entry: dict) -> None:
    variable = entry.get("credential_env")
    if not variable:
        return
    helper = credential_helper(variable, entry["repo"])
    old = subprocess.run(["git", "-C", str(repo), "config", "--local", "--get-all", "credential.helper"],
                         capture_output=True, text=True, check=False)
    if old.returncode not in (0, 1) or (old.returncode == 0 and old.stdout.splitlines() != ["", helper]):
        raise ValueError("operator-owned credential helper exists; refusing to overwrite it")
    if old.returncode == 1:
        git(repo, "config", "--local", "--add", "credential.helper", "")
        git(repo, "config", "--local", "--add", "credential.helper", helper)
    git(repo, "config", "--local", "credential.useHttpPath", "true")


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
    primary = primary_spec(config)
    origin = subprocess.run(["git", "-C", str(domain), "config", "--get", "remote.origin.url"],
                            capture_output=True, text=True, check=False)
    if origin.returncode == 1 and config["schema_version"] == 2:
        pass  # Preparation may restore the explicitly declared origin, never guess it.
    elif origin.returncode != 0 or canonical_remote(origin.stdout.strip()) != primary["repo"]:
        raise ValueError("checkout origin differs from domain_repo")
    expected_name = primary["repo"].rsplit("/", 1)[1].removesuffix(".git")
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
            # The floor reads history and structural pins: a depth-one source
            # is not a valid framework, even if the selected tree is complete.
            git(checkout, "fetch", "--quiet", "origin", pin)
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
    if config["schema_version"] == 2:
        digest = manifest_digest(config)
        recorded = subprocess.run(["git", "-C", str(root), "config", "--local", "--get", "mdllm.cloud.manifest"],
                                  capture_output=True, text=True, check=False)
        if recorded.returncode == 0 and recorded.stdout.strip() != digest:
            raise ValueError("cached workspace configuration changed; review and reset the environment cache")
        if recorded.returncode not in (0, 1):
            raise ValueError("cached workspace manifest could not be read")
        git(root, "config", "--local", "mdllm.cloud.manifest", digest)
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
        if len(sys.argv) == 5 and sys.argv[1] == "credential":
            return credential_response(sys.argv[2], sys.argv[3], sys.argv[4])
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
