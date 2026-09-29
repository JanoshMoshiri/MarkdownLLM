"""Render and inspect reusable hosted-workspace files through adapter ports."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

from . import adapters
from .bundle_service import framework_source_findings
from .cloud_bootstrap import assert_recorded_manifest, canonical_remote, existing_domain, git, load_config, primary_spec, validate_config
from .cloud_workspace import prepare_workspace
from .cloud_repositories import layout, probe, status
from .harness_ports import CloudWorkspacePort
from .model import parse_frontmatter
from .sync import cmd_estate_sync


def derive_config(source: Path, domain: Path, workspace: str, kind="domain") -> dict:
    if Path(git(domain, "rev-parse", "--show-toplevel")).resolve() != domain:
        raise ValueError("name the domain repository root")
    if kind == "domain":
        meta, _, problem = parse_frontmatter((domain / "AGENTS.md").read_text(encoding="utf-8"))
        if problem or not meta or meta.get("framework_root") != "../..":
            raise ValueError("this profile requires a nested domain with framework_root: ../..")
    return {
        "schema_version": 2,
        "framework_repo": canonical_remote(git(source, "config", "--get", "remote.origin.url")),
        "framework_commit": git(source, "rev-parse", "HEAD"),
        "workspace_directory": workspace,
        "primary": {"repo": canonical_remote(git(domain, "config", "--get", "remote.origin.url")),
                    "kind": kind, "credential_env": None, "boundary_terms_env": None},
        "repositories": [],
    }


def write_artifacts(out: Path, rendered: dict[str, bytes], *, check=False) -> None:
    targets = []
    for relative, data in rendered.items():
        rel = PurePosixPath(relative)
        windows = PureWindowsPath(relative)
        if (rel.is_absolute() or windows.drive or ".." in rel.parts
                or "\\" in relative or not rel.parts):
            raise ValueError("adapter returned an escaping artifact path")
        target = out / relative
        if out.resolve() not in target.resolve().parents:
            raise ValueError("adapter returned an escaping artifact path")
        if target.resolve() != target.absolute():
            raise ValueError(f"refusing symlink artifact path {target}")
        if target.exists() and (not target.is_file() or target.read_bytes() != data):
            raise ValueError(f"{target} differs; render into a fresh output directory and review the diff")
        if check and not target.is_file():
            raise ValueError(f"missing generated artifact {target}")
        targets.append((target, data))
    if not check:
        # All collisions are checked before the first write. Never overwrite
        # existing bytes; exclusive creation also catches concurrent writers.
        for target, data in targets:
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(data)


def cmd_cloud(args) -> int:
    source = Path(__file__).resolve().parents[2]
    domain = Path(args.path).resolve()
    try:
        if args.operation in {"probe", "status", "start"}:
            config_path = Path(args.config) if args.config else domain / ".codex/cloud/environment.json"
            config = load_config(config_path)
            root = existing_domain(config, domain)
            if source != root or git(root, "rev-parse", "HEAD") != config["framework_commit"]:
                raise ValueError("run this command from the workspace's pinned framework")
            assert_recorded_manifest(root, config)
            if args.operation == "probe":
                return probe(config, domain)
            if args.operation == "status":
                return status(config, domain)
            selected = getattr(args, "repository", None) or domain.name
            matches = [(entry, path) for entry, path in layout(config, domain) if entry["name"] == selected]
            if not matches:
                raise ValueError("repository is not in this workspace manifest")
            entry, path = matches[0]
            if entry["kind"] != "domain":
                raise ValueError("ordinary code repositories use their own AGENTS.md; select a domain with --repository")
            if git(domain, "config", "--local", "--get", "mdllm.sync") != "observe":
                raise ValueError("primary checkout has no host HEAD restraint; rerun cloud preparation")
            # Observe the host-selected primary without moving it; normal
            # ff-only sync applies to extra branch-following repositories.
            cmd_estate_sync(argparse.Namespace(
                paths=[str(root), *(str(p) for _, p in layout(config, domain))],
                status=False, require_fresh=False, timeout=20))
            # This is deliberately an agent-invoked operation, never setup.
            # stdout is inherited so the whole Tier-0 contract reaches its caller.
            executable = [sys.executable, str(source / "tools/mdllm.py")]
            for index, (label, command) in enumerate((
                    ("Tier-0 contract", ["session-start", str(path), "--contract"]),
                    ("full triggers (judge non-evaluable conditions)", ["triggers", str(path)]),
                    ("imports coverage (report could-not-check)", ["imports-check", str(path)]))):
                print(f"----- {entry['name']}: {label} -----", flush=True)
                result = subprocess.run([*executable, *command], check=False).returncode
                if result and index == 0:
                    return result
                if result:
                    print(f"{entry['name']}: {label} incomplete (exit {result}); inspect before relying on it")
            return 0
        if args.operation == "prepare":
            if not args.config:
                raise ValueError("prepare requires --config")
            return prepare_workspace(domain, Path(args.config), maintenance=args.maintenance)
        if not args.harness:
            raise ValueError("configure/check requires --harness")
        adapter = adapters.get(args.harness)
        if not isinstance(adapter, CloudWorkspacePort):
            raise ValueError(f"{args.harness} has no hosted-workspace port")
        preview = bool(getattr(args, "preview", False))
        findings = framework_source_findings(source, source,
                                             require_published=not preview)
        if findings:
            raise ValueError("; ".join(findings))
        if args.config:
            config = load_config(Path(args.config))
            if config["framework_commit"] != git(source, "rev-parse", "HEAD"):
                raise ValueError("render/check must run from the manifest's exact framework commit")
            derived = derive_config(source, domain, config["workspace_directory"], primary_spec(config)["kind"])
            if (config["framework_repo"] != derived["framework_repo"]
                    or primary_spec(config)["repo"] != derived["primary"]["repo"]):
                raise ValueError("manifest repositories differ from the local source/domain")
        else:
            kind = getattr(args, "primary_kind", "domain")
            workspace = args.workspace_directory or ("/workspace/MarkdownLLM/domain" if kind == "domain"
                                                      else "/workspace/MarkdownLLM/repositories")
            config = derive_config(source, domain, workspace, kind)
        # Validate the same strict data before rendering or writing anything.
        # The standalone reader accepts JSON; use its object validator here too.
        validate_config(config)
        rendered = adapter.cloud_artifacts(source, config)
        out = Path(args.out).resolve() if args.out else source / ".bundle-build" / (args.harness + "-cloud") / domain.name
        if preview:
            if source / ".bundle-build" not in out.parents:
                raise ValueError("unpublished previews must remain in the private .bundle-build directory")
            rendered["RELEASE-REQUIRED.txt"] = (
                "PREVIEW: the framework pin may not be published. Do not install or enable "
                "this bundle until a release is authorised and a normal configure build succeeds.\n"
            ).encode()
        if out == source or (source in out.parents and not (
                source / ".bundle-build" in out.parents or domain == out)):
            raise ValueError("private output belongs in .bundle-build or the owning domain repository")
        write_artifacts(out, rendered, check=args.operation == "check")
        print(f"Hosted workspace files {'checked' if args.operation == 'check' else 'rendered'}: {out}")
        print(json.dumps(dict(adapter.cloud_settings(config)), indent=2))
        print("PREVIEW ONLY; release verification is still required." if preview else "Published source pin verified against cached origin refs.")
        print("Files must be committed to the primary repository and available on its default branch "
              "before enabling setup. No external environment was changed.")
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f"cloud: {exc}")
        return 2
