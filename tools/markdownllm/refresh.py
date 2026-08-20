"""Floor-only domain refresh — the mechanical half of domain-refresh.md.

Reports the version delta and unseen CHANGELOG entries; regenerates the
domain-kernel managed blocks as the migration rail; `--seal` bumps
`framework_version_seen` after the agent confirms semantic adoption.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from .yaml_loader import load_version_sentinel

from .domain_kernel import (apply_domain_kernel, build_domain_kernel_blocks,
                            domain_kernel_status)
from .model import parse_frontmatter
from .repo import version_lt

def _changelog_versions_since(changelog: Path, seen: str) -> list[str]:
    """Heading lines (`## [x.y.z] - date`) in CHANGELOG.md newer than `seen`."""
    if not changelog.is_file():
        return []
    out = []
    for line in changelog.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## \[([0-9][^\]]*)\] - (.+)$", line.strip())
        if m and (not seen or version_lt(seen, m.group(1))):
            out.append(f"v{m.group(1)} ({m.group(2)})")
    return out


def cmd_refresh(args) -> int:
    """Floor-only domain refresh (review #7, Option A): the MECHANICAL half of
    domain-refresh.md. Reports the version delta and the CHANGELOG entries the
    domain has not yet seen, so the agent does the SEMANTIC adoption rather than
    diffing by hand. With --seal, bumps `framework_version_seen` AFTER the agent
    confirms adoption. Never rewrites domain skills — that is semantic, and
    stays the agent's job (the floor/agent split)."""
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    if not agents.is_file():
        sys.exit(f"mdllm: {domain} has no AGENTS.md — not a domain")
    try:
        text = agents.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        sys.exit(f"mdllm: refresh cannot read AGENTS.md as UTF-8 — {exc}")
    meta, _, agents_error = parse_frontmatter(text, source=agents)
    if agents_error:
        sys.exit(f"mdllm: refresh refused invalid AGENTS.md frontmatter — "
                 f"{agents_error}")
    fr = (meta or {}).get("framework_root")
    if not fr:
        sys.exit("mdllm: AGENTS.md has no framework_root — not a wired domain")
    froot = (domain / fr).resolve()
    sentinel = froot / ".markdownllm"
    if not sentinel.is_file():
        sys.exit(f"mdllm: framework_root `{fr}` does not resolve to a framework "
                 f"(.markdownllm not found at {sentinel})")
    try:
        sentinel_data = load_version_sentinel(
            sentinel.read_text(encoding="utf-8"), source=sentinel)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        sys.exit(f"mdllm: refresh refused invalid/unreadable {sentinel} — {exc}")
    fv = str(sentinel_data.get("version"))
    seen = str(meta.get("framework_version_seen", "")) if meta else ""

    print(f"## Domain Refresh — {domain.name}\n")
    print(f"  framework_root : {froot}")
    print(f"  framework      : {fv}")
    print(f"  last seen      : {seen or '<unset — treat as fully stale>'}")

    if seen == fv:
        print("\nUp to date. Nothing to refresh.")
        return 0

    deltas = _changelog_versions_since(froot / 'CHANGELOG.md', seen)
    if deltas:
        print("\n  Versions not yet absorbed (semantic adoption is the agent's job):")
        for d in deltas:
            print(f"    - {d}")
        print("\n  Read those CHANGELOG entries + foundational spec versions, adopt new "
              "capabilities into domain skills/AGENTS.md, then re-run with --seal.")
    else:
        print("\n  Framework is ahead but no newer CHANGELOG entries parsed — verify by hand.")

    # Migration rail: regenerate the domain-kernel managed blocks so framework
    # improvements to the generated operative sections land as part of absorbing
    # the new version. Mechanical and idempotent — only the managed blocks change.
    present, _ = domain_kernel_status(text, build_domain_kernel_blocks(domain, meta or {}))
    if present:
        new_ag, written, _ = apply_domain_kernel(
            text, build_domain_kernel_blocks(domain, meta or {}))
        if new_ag != text:
            agents.write_text(new_ag, encoding="utf-8", newline="\n")
            text = new_ag  # keep --seal's regex operating on the fresh text
            print(f"\n  regenerated domain-kernel blocks: {', '.join(written)} "
                  f"(commit AGENTS.md)")
        else:
            print("\n  domain-kernel blocks already in sync.")

    if args.seal:
        if "framework_version_seen:" in text:
            new = re.sub(r"(?m)^(framework_version_seen:).*$",
                         rf"\g<1> {fv}", text, count=1)
        else:
            new = re.sub(r"(?m)^(framework_root:.*)$",
                         rf"\1\nframework_version_seen: {fv}", text, count=1)
        agents.write_text(new, encoding="utf-8", newline="\n")
        print(f"\nsealed: framework_version_seen → {fv} "
              f"(commit the domain AGENTS.md to record the refresh)")
    return 0
