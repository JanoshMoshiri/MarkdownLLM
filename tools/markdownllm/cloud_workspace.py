"""Prepare a host-owned checkout using the existing deterministic floor.

No clone, branch change, pull, entry-file rewrite or lifecycle attestation.
Setup logs are not evidence that the working agent received the contract.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .cloud_bootstrap import existing_domain, git, load_config
from .model import parse_frontmatter
from .scaffold import cmd_install_hook
from .validation import validation_reports
from .model import SEV_ERROR


def prepare_workspace(domain: Path, config_path: Path, *, maintenance=False) -> int:
    config = load_config(config_path)
    root = existing_domain(config, domain)
    if Path(__file__).resolve().parents[2] != root:
        raise ValueError("prepare must run from the pinned framework in this workspace")
    if git(root, "rev-parse", "HEAD") != config["framework_commit"]:
        raise ValueError("framework pin changed; reset the environment cache")
    meta, _, problem = parse_frontmatter(
        (domain / "AGENTS.md").read_text(encoding="utf-8"), source=domain / "AGENTS.md")
    if problem or not meta or meta.get("framework_root") != "../..":
        raise ValueError("domain AGENTS.md must declare framework_root: ../..")
    # This clone-local restraint can only reduce standing publication authority.
    # It persists through cached branch checkouts without changing AGENTS.md.
    git(domain, "config", "--local", "mdllm.publication", config["publication"])
    before = (git(domain, "rev-parse", "HEAD"), git(domain, "write-tree"),
              git(domain, "status", "--porcelain", "--untracked-files=all"))
    result = cmd_install_hook(argparse.Namespace(path=str(domain), no_test=True))
    if result:
        return result
    # The first real agent must emit Tier 0. Do not forge a session receipt
    # merely to make a setup-phase execution test pass the strict session gate.
    for _, _, findings in validation_reports(domain):
        for finding in findings:
            deferred = finding.thing == "_session-gate"
            print(f"{'AGENT START REQUIRED' if deferred else finding.severity}: "
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
          "Publication: PR (automatic push disabled for this clone).")
    print("Setup output is not session delivery. The working agent must run "
          "the entry contract's estate-sync and session-start --contract, "
          "consume Tier 0, then load the routed domain skills. "
          "Project lifecycle trust/execution remain separately observed.")
    return result
