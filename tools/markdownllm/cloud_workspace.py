"""Prepare a host-owned checkout using the existing deterministic floor.

No primary branch change, pull, entry-file rewrite or lifecycle attestation.
Additional repositories are explicitly assembled from the manifest.
Setup logs are not evidence that the working agent received the contract.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .cloud_bootstrap import assert_recorded_manifest, existing_domain, git, load_config
from .model import parse_frontmatter
from .scaffold import cmd_install_hook
from .validation import validation_reports
from .model import SEV_ERROR
from .cloud_repositories import assemble_extra, complete_history, layout, provision_boundary


def prepare_workspace(domain: Path, config_path: Path, *, maintenance=False) -> int:
    config = load_config(config_path)
    root = existing_domain(config, domain)
    if Path(__file__).resolve().parents[2] != root:
        raise ValueError("prepare must run from the pinned framework in this workspace")
    if git(root, "rev-parse", "HEAD") != config["framework_commit"]:
        raise ValueError("framework pin changed; reset the environment cache")
    assert_recorded_manifest(root, config)
    before = (git(domain, "rev-parse", "HEAD"), git(domain, "write-tree"),
              git(domain, "status", "--porcelain", "--untracked-files=all"))
    git(domain, "config", "--local", "mdllm.sync", "observe")
    result = 0
    for entry, repo in layout(config, domain):
        if config["schema_version"] == 2:
            if repo == domain:
                complete_history(repo, entry, primary=True)
            else:
                assemble_extra(root, entry, repo, maintenance=maintenance)
        if entry["publication"] != "declared":
            # Local restraint narrows authority only. A secondary repository
            # has no assumed host PR channel; manual publication stays explicit.
            git(repo, "config", "--local", "mdllm.publication", entry["publication"])
        if entry["kind"] != "domain":
            print(f"{entry['name']}: ordinary repository; existing build/test hooks preserved")
            continue
        meta, _, problem = parse_frontmatter(
            (repo / "AGENTS.md").read_text(encoding="utf-8"), source=repo / "AGENTS.md")
        if problem or not meta or meta.get("framework_root") != "../..":
            raise ValueError("domain AGENTS.md must declare framework_root: ../..")
        provision_boundary(repo, entry)
        result |= cmd_install_hook(argparse.Namespace(path=str(repo), no_test=True))
        # Setup is not model receipt. The first working agent must emit Tier 0.
        for _, _, findings in validation_reports(repo):
            for finding in findings:
                deferred = finding.thing == "_session-gate"
                print(f"{entry['name']}: {'AGENT START REQUIRED' if deferred else finding.severity}: "
                      f"{finding.thing}: {finding.message}")
                if not deferred and finding.severity == SEV_ERROR:
                    result = 1
    after = (git(domain, "rev-parse", "HEAD"), git(domain, "write-tree"),
             git(domain, "status", "--porcelain", "--untracked-files=all"))
    if before != after:
        raise ValueError("domain checkout changed during preparation; inspect before starting work")
    if result:
        print("Workspace preparation failed validation; resolve the Errors before starting work.")
        return result
    print("Workspace prepared; host-selected HEAD and index preserved. "
          "Primary publication: PR (automatic push disabled for this clone). "
          "Additional repositories retain their own explicit publication policies.")
    print("Setup output is not session delivery. The working agent must run "
          "the entry contract's estate-sync and session-start --contract, "
          "consume Tier 0, then load the routed domain skills. "
          "Project lifecycle trust/execution remain separately observed.")
    return result
