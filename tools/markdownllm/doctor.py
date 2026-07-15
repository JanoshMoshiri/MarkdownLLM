"""Environment probe — floor prerequisites, hook execution, version drift.

The one sanctioned aggregator: it imports library functions from its sibling
modules (never their `cmd_*` entry points) to answer "can the floor run
here, and is anything stale?".
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .model import parse_frontmatter
from .repo import _version_lt
from .scaffold import HOOK_BODY, MDLLM_ENTRY

def _upstream_sentinel_version(root: Path):
    """Read the framework version from the *cached* upstream copy of
    `.markdownllm` — git's remote-tracking objects, with no network call
    (orchestration.md → session-start:version-check upward leg). Tries the
    current branch's configured upstream first, then origin/main / origin/HEAD.
    Returns the version string, or None when no fetched copy is available."""
    refs = []
    up = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
                        cwd=root, capture_output=True, text=True)
    if up.returncode == 0 and up.stdout.strip():
        refs.append(up.stdout.strip())
    refs += ["origin/main", "origin/HEAD"]
    for ref in refs:
        show = subprocess.run(["git", "show", f"{ref}:.markdownllm"],
                              cwd=root, capture_output=True, text=True)
        if show.returncode == 0 and show.stdout.strip():
            try:
                data = yaml.safe_load(show.stdout) or {}
            except yaml.YAMLError:
                continue
            v = data.get("version")
            if v is not None:
                return str(v)
    return None


def cmd_doctor(args) -> int:
    """Probe the environment the floor depends on. A floor/portability claim
    is verified only by executing the capability in the target environment
    (insight: portability-claims-need-execution-tests) — so the hook check
    *runs* the hook rather than checking the file exists. Exit 1 when the
    floor cannot run here (degraded mode: run `mdllm validate` manually
    before each commit, and say so)."""
    import shutil
    root = Path(args.path).resolve()
    lines: list[str] = []
    floor_ok = True

    def report(status: str, label: str):
        lines.append(f"  {status:4s}  {label}")

    # interpreter + libraries (if we got this far, python and yaml exist)
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        report("OK", f"python {py}")
    else:
        report("FAIL", f"python {py} — floor requires 3.10+")
        floor_ok = False
    report("OK", f"pyyaml {getattr(yaml, '__version__', '?')}")
    try:
        import tiktoken
        report("OK", f"tiktoken {getattr(tiktoken, '__version__', '?')} — token counts are measured")
    except ImportError:
        report("--", "tiktoken absent — `tokens` falls back to a chars/3.8 heuristic (fine)")

    # git + identity
    git = shutil.which("git")
    if not git:
        report("FAIL", "git not on PATH — the floor and the state machine need git")
        print(f"## Doctor Report — {root}\n" + "\n".join(lines))
        print("\nVerdict: DEGRADED — no git, no floor.")
        return 1
    gv = subprocess.run(["git", "--version"], capture_output=True, text=True)
    report("OK", gv.stdout.strip())
    for key in ("user.name", "user.email"):
        cfg = subprocess.run(["git", "config", key], cwd=root,
                             capture_output=True, text=True)
        if cfg.returncode == 0 and cfg.stdout.strip():
            report("OK", f"git {key} = {cfg.stdout.strip()}")
        else:
            report("WARN", f"git {key} unset — commits will fail until configured")

    # repo + hook (executed, not just resolved)
    inside = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                            capture_output=True, text=True)
    if inside.returncode != 0:
        report("FAIL", "not a git repository — `git init` first")
        floor_ok = False
    else:
        git_dir = (root / inside.stdout.strip()).resolve()
        hook = git_dir / "hooks" / "pre-commit"
        if not hook.is_file():
            report("FAIL", "pre-commit hook not installed — run `mdllm install-hook .`")
            floor_ok = False
        else:
            # Body freshness: the installed hook is a copy frozen at install
            # time. A domain that sealed to a newer framework but never re-ran
            # install-hook keeps an older HOOK_BODY — the version sentinel then
            # claims an enforcement level the hook does not actually run (e.g.
            # `coherence` missing). Compare the copy against what install-hook
            # would write now. Advisory, not fatal: the hook still runs
            # `validate`, so the floor is active — just not current.
            import os
            try:
                rel = Path(os.path.relpath(MDLLM_ENTRY, root)).as_posix()
            except ValueError:
                rel = MDLLM_ENTRY.as_posix()
            installed = hook.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            if installed != HOOK_BODY.format(rel=rel).replace("\r\n", "\n").strip():
                report("WARN", "pre-commit hook body is STALE vs the current mdllm "
                               "HOOK_BODY — re-run `mdllm install-hook` to pick up "
                               "newer checks (the sentinel may claim enforcement the "
                               "hook does not run)")
            run = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=root,
                                 capture_output=True, text=True)
            if "is not a git command" in (run.stderr or ""):
                report("WARN", "git < 2.36 — cannot execution-test the hook "
                               "(file present; make one commit to verify)")
            elif run.returncode == 0:
                report("OK", "pre-commit hook EXECUTES (validation currently clean)")
            elif run.returncode == 1 and "Validation" in (run.stdout or run.stderr or ""):
                report("OK", "pre-commit hook EXECUTES (validation currently has Errors "
                             "— it would block a commit, which is the point)")
            else:
                report("FAIL", f"pre-commit hook present but failed to execute "
                               f"(exit {run.returncode}) — resolution is not verification")
                floor_ok = False

    # framework / domain version drift
    sentinel = root / ".markdownllm"
    if sentinel.is_file():
        data = yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}
        local_v = str(data.get("version"))
        report("OK", f"framework root — sentinel version {local_v}")
        # Upstream leg (advisory, cached, non-blocking): compare the local
        # sentinel against the *already-fetched* upstream copy. No live fetch —
        # `git show` reads objects git already has (orchestration.md → upward
        # leg). Never flips floor_ok: this coordinates humans, not integrity.
        upstream_v = _upstream_sentinel_version(root)
        if upstream_v is None:
            report("--", "upstream version unknown — no fetched remote-tracking "
                         "copy of .markdownllm (run `git fetch`, then `mdllm doctor`)")
        elif upstream_v == local_v:
            report("OK", f"framework current with published upstream {upstream_v} "
                         f"(as of last fetch)")
        elif _version_lt(local_v, upstream_v):
            report("WARN", f"local framework is {local_v}; published upstream is "
                           f"{upstream_v} (as of last fetch) — consider pulling. "
                           f"Advisory only; does not block.")
        else:
            report("OK", f"local framework {local_v} is ahead of published upstream "
                         f"{upstream_v} (unpushed work) — as of last fetch")
    else:
        agents = root / "AGENTS.md"
        meta = None
        if agents.is_file():
            meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        fr = (meta or {}).get("framework_root")
        if fr:
            fsent = (root / fr / ".markdownllm").resolve()
            if fsent.is_file():
                fdata = yaml.safe_load(fsent.read_text(encoding="utf-8")) or {}
                fv, seen = str(fdata.get("version")), str(meta.get("framework_version_seen"))
                if fv == seen:
                    report("OK", f"domain current with framework {fv}")
                else:
                    report("WARN", f"domain last saw framework {seen}; framework is {fv} "
                                   f"— run the domain-refresh process")
            else:
                report("FAIL", f"framework_root `{fr}` does not resolve to a framework "
                               f"(.markdownllm not found at {fsent})")
                floor_ok = False
        else:
            report("--", "no .markdownllm and no framework_root in AGENTS.md — "
                         "neither a framework root nor a wired domain")

    # domain-kernel freshness + harness adapter (advisory; existence != currency)
    agents_p = root / "AGENTS.md"
    if agents_p.is_file():
        import json
        atext = agents_p.read_text(encoding="utf-8")
        ameta, _, _ = parse_frontmatter(atext)
        present, drifted = domain_kernel_status(
            atext, build_domain_kernel_blocks(root, ameta or {}))
        if not present:
            report("--", "AGENTS.md has no domain-kernel managed blocks "
                         "(opt-in; the entry file runs by interpretation)")
        elif drifted:
            report("WARN", f"domain-kernel blocks STALE ({', '.join(drifted)}) — "
                           f"run `mdllm domain-kernel .` and commit")
        else:
            report("OK", f"domain-kernel in sync ({len(present)} blocks)")
        has_ss = False
        settings = root / ".claude" / "settings.json"
        if settings.is_file():
            try:
                has_ss = "SessionStart" in (json.loads(
                    settings.read_text(encoding="utf-8")).get("hooks") or {})
            except (ValueError, OSError):
                has_ss = False
        report("OK" if has_ss else "--",
               "SessionStart adapter installed (.claude/settings.json)" if has_ss
               else "no SessionStart adapter — session-start runs by interpretation "
                    "(opt-in: adapters/claude-code.settings.example.json)")

    print(f"## Doctor Report — {root}\n")
    print("\n".join(lines))
    print(f"\nVerdict: {'FLOOR ACTIVE' if floor_ok else 'DEGRADED'} — "
          + ("mechanical validation is enforced at the commit boundary."
             if floor_ok else
             "run `mdllm validate` manually before each commit, and say so."))
    return 0 if floor_ok else 1
