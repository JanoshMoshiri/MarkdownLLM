"""Bundle rendering service — Phase 3 of the ``cowork-adapter`` plan.

``mdllm bundle --harness <name>`` renders that harness's estate-level
distribution bundle through the ``BundlePort``. The service owns what is
neutral: gathering the estate config (the domain list derived from the
local clones' remotes — never authored; the identity from git config)
and writing the rendered bytes. The adapter owns the content.

The output is PRIVATE by construction — a rendered bundle carries the
operator's repository names — so it lands in a gitignored build
directory and must never be committed to the framework repo. The
templates the adapter renders from are public and name no repository.

``--hash`` prints the canonical mechanism hash only: the run-time
currency anchor an installed bundle compares its build stamp against.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from . import adapters as harness_adapters
from .harness_ports import BundlePort

_REMOTE_FORMS = [
    re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?/?$"),
    re.compile(r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$"),
    re.compile(r"^ssh://git@github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$"),
]


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def owner_repo(url: str) -> str | None:
    for form in _REMOTE_FORMS:
        match = form.match(url.strip())
        if match:
            return f"{match.group('owner')}/{match.group('repo')}"
    return None


def derive_estate_config(root: Path) -> tuple[dict[str, str], list[str]]:
    """The estate as the filesystem states it — derived, never authored.

    Domains: every git repo under ``domain/`` or ``domains/`` whose origin
    is a recognised GitHub remote. Identity: the framework clone's git
    config (falling back to global). Notes report what was skipped so a
    derivation can never silently narrow."""
    notes: list[str] = []
    domains: list[str] = []
    for container in ("domain", "domains"):
        base = root / container
        if not base.is_dir():
            continue
        for child in sorted(base.iterdir()):
            if not (child / ".git").exists():
                continue
            url = _git(child, "remote", "get-url", "origin")
            if not url:
                notes.append(f"skipped {container}/{child.name}: no origin "
                             "remote (local-only repo)")
                continue
            entry = owner_repo(url)
            if entry is None:
                notes.append(f"skipped {container}/{child.name}: origin is "
                             f"not a recognised GitHub remote ({url})")
                continue
            domains.append(entry)

    config: dict[str, str] = {
        "GIT_NAME": _git(root, "config", "user.name")
                    or _git(root, "config", "--global", "user.name"),
        "GIT_EMAIL": _git(root, "config", "user.email")
                     or _git(root, "config", "--global", "user.email"),
        "DOMAINS": " ".join(domains),
    }
    fw_url = _git(root, "remote", "get-url", "origin")
    fw_entry = owner_repo(fw_url) if fw_url else None
    if fw_entry:
        config["FRAMEWORK_REPO"] = fw_entry
    else:
        notes.append("framework origin is not a recognised GitHub remote — "
                     "set FRAMEWORK_REPO in the built config by hand")
    return config, notes


def cmd_bundle(args) -> int:
    root = Path(getattr(args, "root", ".")).resolve()
    adapter = harness_adapters.get(args.harness)
    if not isinstance(adapter, BundlePort):
        print(f"mdllm: harness {args.harness!r} has no bundle port — "
              "it distributes through project artifacts, not a bundle")
        return 2

    templates_root = Path(__file__).resolve().parents[2] / "templates"

    if getattr(args, "hash", False):
        print(adapter.bundle_hash(templates_root))
        return 0

    config, notes = derive_estate_config(root)
    for note in notes:
        print(f"  note: {note}")
    if not config.get("DOMAINS"):
        print("mdllm: no domains derived — nothing under domain/ or "
              "domains/ carries a recognised GitHub origin. A bundle with "
              "an empty estate would assemble nothing; aborting.")
        return 2
    if not (config.get("GIT_NAME") and config.get("GIT_EMAIL")):
        print("mdllm: no git identity (user.name/user.email) found in this "
              "clone or globally — set one before building; every commit "
              "the bundle's sessions make is authored with it.")
        return 2

    version = ""
    sentinel = root / ".markdownllm"
    if sentinel.is_file():
        for line in sentinel.read_text(encoding="utf-8").splitlines():
            if line.startswith("version:"):
                version = line.split(":", 1)[1].strip()
                break
    config["FRAMEWORK_VERSION"] = version or "unknown"

    try:
        rendered = adapter.bundle(templates_root, config)
    except ValueError as exc:
        # An adapter refuses to render a bundle its harness would reject.
        # Failing here is the point: the alternative is a clean build and
        # an install failure, where the operator is furthest from the fix.
        print(f"mdllm: {exc}")
        return 2
    out = Path(args.out) if getattr(args, "out", None) else (
        root / ".bundle-build" / args.harness)
    for rel, content in sorted(rendered.items()):
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        print(f"  wrote {target.relative_to(out.parent) if out in target.parents or target == out else target}")

    print(f"\nbundle: {len(rendered)} file(s) -> {out}")
    print("bundle: this output is PRIVATE (it names your repositories). "
          "It is gitignored here; install it in the harness and never "
          "commit it to the framework repo.")
    print(f"bundle: mechanism hash {adapter.bundle_hash(templates_root)} "
          "(stamped into the build; the bundle re-checks it against the "
          "framework it clones at run time)")
    return 0
