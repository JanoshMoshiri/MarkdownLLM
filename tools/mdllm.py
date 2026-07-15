#!/usr/bin/env python3
"""mdllm — the MarkdownLLM deterministic floor.

Mechanical validation and maintenance for MarkdownLLM domains. The division of
labour (validate.thing.md v2.0): this tool guarantees the mechanical checks
(structural, referential, schema); the LLM keeps the semantic ones (Level 4).

Subcommands:
  validate [path]      Levels 1-3 mechanical validation. Exit 1 on Errors.
                       Example domains under <path>/examples/ are validated
                       as their own corpora in the same run.
  triggers [path]      Evaluate time/dependency/threshold trigger conditions;
                       relationship triggers (and blocked_duration) are listed
                       as not mechanically evaluable — left to the agent.
  index    [path] check|rebuild [--signal triggers|schema|relationships]
  touchpoints <id> [path]  Assimilate beat (change-reconciliation): the declared
                       inbound set + literal references for one thing — "what did
                       I just put at risk?". Human-invoked, never hooked; live.
  cascade  <id> [path] Post-completion cascade (write.thing.md): the declared
                       downstream set a thing's completion unblocks — "what did I
                       just unblock?". Mirror of touchpoints; reports, never applies.
  coherence [path]     Dark-region checks: generated-artifact (kernel/index)
                       freshness, foundational_specs<->filesystem, stale labels.
                       Corpus-general; framework-only checks switch on at a root
                       with .markdownllm. Runs in the pre-commit hook.
  tokens   [path]      Measure spec token costs by loading tier.
  doctor   [path]      Probe the environment: floor prerequisites, hook
                       execution (not just presence), framework version drift.
  scaffold <path>      Deterministic domain birth: instantiated templates,
                       nested git repo, outer .gitignore isolation, hook,
                       first commit. The semantic half stays with the agent.
  install-hook [path]  Install a git pre-commit hook running `validate`.

Requires: Python 3.10+, PyYAML. tiktoken optional (tokens falls back to heuristic).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("mdllm: PyYAML is required (pip install pyyaml)")

from markdownllm.model import (
    RESERVED_STATUSES, DEFAULT_STATUSES, TERMINAL_STATUSES, CORE_FIELDS,
    DEFAULT_EXCLUDES, NON_THING_FILES, ID_RE, ISO_RE,
    SEV_ERROR, SEV_WARNING, SEV_INFO,
    Thing, Finding, Corpus, parse_frontmatter, load_schema, scan,
)


from markdownllm.validation import (
    valid_statuses_for, validate_level1, validate_level2, version_tuple,
    check_version_sync, validate_level3, validate_corpus, example_corpora,
    cmd_validate,
)


from markdownllm.triggers import cmd_triggers
from markdownllm.repo import git_short_sha, framework_version, _version_lt, TIERS

from markdownllm.indexes import (
    INDEX_FILES, build_index_body, index_drift_findings, cmd_index,
)

from markdownllm.touchpoints import cmd_touchpoints

from markdownllm.cascade import cmd_cascade

from markdownllm.tokens import cmd_tokens

from markdownllm.provenance import cmd_provenance

from markdownllm.history import cmd_changelog, cmd_worklog


from markdownllm.refresh import _changelog_versions_since, cmd_refresh


HOOK_BODY = """#!/bin/sh
# mdllm pre-commit: deterministic validation floor (transformation plan Phase 1)
# Portable: repo root and interpreter are resolved at run time, mdllm.py via a
# path relative to the repo root — so the same hook works wherever this repo is
# checked out or mounted (Windows, WSL, CI, sandboxed agent harnesses).
ROOT="$(git rev-parse --show-toplevel)"
MDLLM="$ROOT/{rel}"
# Candidates are executed, not just resolved: on Windows, the Microsoft Store
# ships alias stubs named python/python3 that command -v happily finds but
# that only print an install hint and exit nonzero.
PY=""
for c in python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  echo "mdllm: validation floor unavailable (python or $MDLLM not found) — commit blocked."
  echo "Install Python 3.10+ with PyYAML, or re-run install-hook from the framework root."
  exit 1
fi
"$PY" "$MDLLM" validate "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: validation Errors — commit blocked. Fix or run with --no-verify (discouraged)."
  exit 1
}}
# Coherence: generated-artifact freshness (kernel/index drift) + spec-catalog
# integrity. Self-scoping — at a domain root (no .markdownllm) only the general
# checks run, so the same hook is correct in the framework and in every domain.
"$PY" "$MDLLM" coherence "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: coherence Errors — a generated artifact (kernel/index) or the spec catalog is stale. Regenerate and re-commit, or --no-verify (discouraged)."
  exit 1
}}
"""


from markdownllm.evals import (
    check_assertions, seed_run_dir, eval_report, _resolve_claude_cli, cmd_eval,
)
from markdownllm.kernel_gen import (
    KERNEL_RE, _token_counter, build_kernel, cmd_kernel,
)
from markdownllm.domain_kernel import (
    DOMAIN_KERNEL_BLOCKS, apply_domain_kernel, build_domain_kernel_blocks,
    cmd_domain_kernel, domain_kernel_status,
)

# ---------------------------------------------------------------- session start
#
# The mechanical half of the session-start ritual, emitted to stdout for a harness
# SessionStart hook to inject (Claude Code; Copilot in VS Code agent mode — both
# inject `additionalContext` at session start). This is the HARDENING for the
# `session-start:version-check` hook whose anchor is `harness-session`: a weak (or
# distracted) model receives the ritual at t=0 instead of having to recall it from
# a buried entry file. Optional — the AGENTS.md prose stays the interpretation
# floor where no adapter is installed. Read-only; safe on every session.


def _velocity_signal(domain: Path) -> str:
    things = domain / "things"
    if not things.is_dir():
        return "no `things/` directory yet."
    last = subprocess.run(["git", "log", "-1", "--format=%cr|%s", "--", "things"],
                          cwd=domain, capture_output=True, text=True)
    if last.returncode != 0 or not last.stdout.strip():
        return "no committed history over `things/` yet."
    when, _, subj = last.stdout.strip().partition("|")
    cnt = subprocess.run(["git", "rev-list", "--count", "--since=30.days", "HEAD",
                          "--", "things"], cwd=domain, capture_output=True, text=True)
    n = cnt.stdout.strip() if cnt.returncode == 0 else "?"
    return (f"last `things/` change {when} (\"{subj.strip()}\"); {n} commit(s) in 30d. "
            f"Read `git log -- things/` for the full picture.")


# Types that sit at a non-terminal status as a steady state (knowledge/reference),
# so they are NOT "open work" — excluded from the forward orientation view.
_ORIENT_KNOWLEDGE_TYPES = {"specification", "guide", "manifesto", "insight",
                           "retrospective", "index", "continuity-brief", "prompt",
                           "workflow-definition", "decision", "artifact"}


def _orient_forward(domain: Path) -> list[str]:
    """The forward half of orientation — the open loops the next session inherits,
    computed from the thing graph. Orient is the session-memory counterpart to
    change-reconciliation's work-content state: backward orientation is the commit
    stream (velocity), this is its forward complement (what is still open). Replaces
    the hand-maintained continuity brief (dissolve-continuity-into-reconciliation)."""
    try:
        corpus, _ = scan(domain)
    except Exception:
        return []
    conflicts, loops = [], []
    for t in corpus.things:
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "conflict" and status == "open":
            conflicts.append(t.id)
        elif typ not in _ORIENT_KNOWLEDGE_TYPES and status not in TERMINAL_STATUSES:
            loops.append((t.id, typ, status))
    lines: list[str] = []
    if conflicts:
        lines.append("- **Open conflicts (%d):** %s — resolve or carry forward."
                     % (len(conflicts), ", ".join(f"`{c}`" for c in sorted(conflicts))))
    if loops:
        lines.append(f"- **Open loops ({len(loops)}):** forward work still in flight —")
        for tid, typ, status in sorted(loops)[:15]:
            lines.append(f"    - `{tid}` ({typ}, {status})")
        if len(loops) > 15:
            lines.append(f"    - …and {len(loops) - 15} more (`mdllm validate` lists all).")
    return lines


def cmd_session_start(args) -> int:
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    meta = {}
    if agents.is_file():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        meta = meta or {}

    out = ["# MarkdownLLM — Session Start (run before the user's first request)", "",
           "The live request will pull you toward itself; do these first, then await intent:",
           "1. Load `kernel.md` (operative kernel).",
           "2. Act on the version + velocity (backward) and open-loops (forward) status below.",
           "3. Evaluate triggers and surface what needs the user.", ""]

    fr = meta.get("framework_root")
    if (domain / ".markdownllm").is_file():
        # This IS a framework root (it carries the sentinel), not a downstream
        # domain — `framework_root: .` points at itself, so the domain
        # version-check does not apply.
        fv = str((yaml.safe_load((domain / ".markdownllm").read_text(encoding="utf-8"))
                  or {}).get("version"))
        out.append(f"- **Version:** framework root (v{fv}) — not a downstream domain; "
                   f"no refresh applies.")
    elif not fr:
        out.append("- **Version:** n/a — no `framework_root` in AGENTS.md.")
    else:
        sentinel = (domain / fr).resolve() / ".markdownllm"
        if not sentinel.is_file():
            out.append(f"- **Version:** unknown — `framework_root` `{fr}` has no .markdownllm.")
        else:
            fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}).get("version"))
            seen = str(meta.get("framework_version_seen", ""))
            if not seen:
                out.append(f"- **Version: STALE** — framework v{fv}; domain has no "
                           f"`framework_version_seen`. Run `mdllm refresh .` and adopt.")
            elif version_tuple(seen) != version_tuple(fv):
                out.append(f"- **Version: MISMATCH** — framework v{fv}; domain last saw "
                           f"v{seen}. Validate the domain, then `mdllm refresh .` → adopt "
                           f"→ `--seal`.")
            else:
                out.append(f"- **Version: in sync** (framework v{fv}).")

    out.append(f"- **Velocity:** {_velocity_signal(domain)}")

    if agents.is_file():
        _, drifted = domain_kernel_status(
            agents.read_text(encoding="utf-8"),
            build_domain_kernel_blocks(domain, meta))
        if drifted:
            out.append(f"- **Domain kernel: DRIFT** in {', '.join(drifted)} — run "
                       f"`mdllm domain-kernel .` and commit.")

    out.extend(_orient_forward(domain))

    print("\n".join(out))
    return 0


def _changed_files_recent(root: Path, window: int) -> set[str] | None:
    """Repo-relative POSIX paths changed in the last `window` commits, or None
    if `root` is not inside a git repo (the check then skips, like provenance).
    Returns all tracked files when there are 0–1 commits (nothing to diff against
    yet — and on the first commit there is no HEAD)."""
    cnt = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root,
                         capture_output=True, text=True)
    if cnt.returncode != 0:
        return None
    n = int(cnt.stdout.strip()) if cnt.stdout.strip().isdigit() else 0
    if n <= 1:
        out = subprocess.run(["git", "ls-files"], cwd=root,
                             capture_output=True, text=True)
    else:
        out = subprocess.run(["git", "diff", "--name-only",
                              f"HEAD~{min(window, n - 1)}", "HEAD"],
                             cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        return set()
    return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}


def coherence_findings(root: Path, window: int) -> list[Finding]:
    """Mechanical checks over the 'dark region' a hand-walk currently guards
    (AGENTS.md -> Walking the Dark Region). Corpus-general by design: the
    stable-staleness, unused-vocabulary, and derived-index-drift checks run on
    ANY corpus, so a domain inherits them through the same pre-commit hook; the
    foundational-spec / TIERS / kernel-drift checks switch on only at a framework
    root (where `.markdownllm` is present). None of this is judgment — staleness
    and unused vocabulary are Info *proxies*; the semantic calls (is it *really*
    stable; is that empty type intended) stay the agent's."""
    corpus, _ = scan(root)
    findings: list[Finding] = []

    # --- general: stable-staleness (Info) --------------------------------
    changed = _changed_files_recent(root, window)
    if changed is not None:
        for t in corpus.things:
            if str(t.meta.get("status")) != "stable":
                continue
            rel = t.path.relative_to(root).as_posix()
            if rel in changed:
                findings.append(Finding(SEV_INFO, t.id or rel,
                    f"marked `stable` but changed within the last {window} "
                    f"commits — confirm the label still reflects reality"))

    # --- general: unused declared vocabulary (Info) ----------------------
    # A domain's _schema.yaml is its own spec of its types; a declared type that
    # no thing uses is dead vocabulary worth surfacing — but only Info, since the
    # framework explicitly allows foreseen-but-undeployed types.
    if corpus.schema:
        declared = set(corpus.schema.get("types") or {})
        used = {str(t.meta.get("type")) for t in corpus.things}
        for typ in sorted(declared - used):
            findings.append(Finding(SEV_INFO, "_schema.yaml",
                f"declared type `{typ}` is used by no thing — dead vocabulary?"))

    # --- general: derived-index drift (Error, deployed indexes only) -----
    findings.extend(index_drift_findings(root, corpus))

    # --- general: domain-kernel drift (Error, kernel-shaped AGENTS.md only) ---
    # Opt-in by construction: only domains whose AGENTS.md carries managed
    # `<!-- generated:NAME -->` blocks are checked. Same builder as
    # `mdllm domain-kernel`, so the check cannot disagree with the generator.
    agents = root / "AGENTS.md"
    if agents.is_file():
        atext = agents.read_text(encoding="utf-8")
        ameta, _, aerr = parse_frontmatter(atext)
        if not aerr:
            _, dk_drifted = domain_kernel_status(
                atext, build_domain_kernel_blocks(root, ameta or {}))
            for name in dk_drifted:
                findings.append(Finding(SEV_ERROR, "AGENTS.md",
                    f"domain-kernel block `{name}` drifted from a fresh build — "
                    f"run `mdllm domain-kernel .` and commit the result"))

    # --- framework root only ---------------------------------------------
    if (root / ".markdownllm").is_file():
        data = yaml.safe_load((root / ".markdownllm").read_text(encoding="utf-8")) or {}
        specs = data.get("foundational_specs") or []

        # foundational_specs <-> filesystem. `kernel` skips a missing spec
        # silently; here a listed-but-absent spec is an Error.
        for name in specs:
            if not (root / name).is_file():
                findings.append(Finding(SEV_ERROR, "foundational_specs",
                    f"`{name}` listed in .markdownllm but not present on disk"))

        # TIERS <-> foundational_specs: every foundational spec has a tier entry
        # in the loading map. A missing one means tier routing drifted from the
        # catalog — the dark-region class with the worst track record.
        tier_files = ({f for files in TIERS.values() for f in files}
                      - {"AGENTS.md", "kernel.md"})
        for name in specs:
            if name not in tier_files:
                findings.append(Finding(SEV_WARNING, "TIERS",
                    f"foundational spec `{name}` has no entry in the TIERS map "
                    f"(tools/mdllm.py) — tier routing drifted from the catalog"))

        # ...and the mirror (directional graph reads come in inbound/outbound
        # pairs): every TIERS entry must be in the catalog. A file routed by
        # tier but absent from .markdownllm is loadable-but-uncatalogued —
        # the reverse drift the one-directional check was blind to (review 6,
        # finding 6: thing-lifecycle.md sat exactly there).
        for name in sorted(tier_files):
            if name not in specs:
                findings.append(Finding(SEV_WARNING, "TIERS",
                    f"`{name}` is in the TIERS map (tools/mdllm.py) but not in "
                    f".markdownllm foundational_specs — loading map drifted "
                    f"from the catalog"))

        # Example staleness: an example's framework_version_seen pins the
        # framework version it was last walked against; a pin behind the
        # sentinel means the example teaches an old shape (review 6: both
        # examples sat at 3.4.0 for thirteen minor versions, invisibly).
        # Same-builder — the sentinel is the only version source — and no
        # suppression list: the only way to quiet it is the walk + re-pin.
        fw_version = str(data.get("version", ""))
        for ex in sorted((root / "examples").glob("*/AGENTS.md")):
            emeta, _, _ = parse_frontmatter(ex.read_text(encoding="utf-8"))
            seen = str(emeta.get("framework_version_seen", ""))
            if fw_version and seen and seen != fw_version:
                findings.append(Finding(SEV_WARNING, f"examples/{ex.parent.name}",
                    f"pinned at framework_version_seen {seen} but the framework "
                    f"is {fw_version} — walk the example against the current "
                    f"shape, then re-pin"))

        # kernel drift, via the shared builder (cannot disagree with what
        # `mdllm kernel` would write — same source).
        kpath = root / "kernel.md"
        kbody, _, _, _ = build_kernel(root, specs, _token_counter())
        if not kpath.exists():
            findings.append(Finding(SEV_ERROR, "kernel.md",
                "missing — run `mdllm kernel` to generate it"))
        else:
            _, ex_body, _ = parse_frontmatter(kpath.read_text(encoding="utf-8"))
            if ex_body.strip() != kbody.strip():
                findings.append(Finding(SEV_ERROR, "kernel.md",
                    "DRIFT — spec kernel blocks changed since kernel.md was "
                    "generated; run `mdllm kernel` and commit the result"))

        # framework-map subcommand count <-> the actual CLI surface. The map's
        # own "Keeping This Map Honest" note already pins View 3 to `mdllm
        # --help`; this makes that pin mechanical so the hand-drawn count can't
        # silently drift when a subcommand lands — the exact repeat-offender the
        # 2026-06d retrospective said to make checkable. Truth = the subparser
        # registration calls in this file, one per subcommand.
        fmap = root / "docs" / "framework-map.md"
        if fmap.is_file():
            actual = len(re.findall(r"sub\.add_parser\(",
                                    Path(__file__).read_text(encoding="utf-8")))
            stated = re.search(r"(\d+)\s+mechanical subcommands",
                               fmap.read_text(encoding="utf-8"))
            if stated and int(stated.group(1)) != actual:
                findings.append(Finding(SEV_WARNING, "framework-map.md",
                    f"says {stated.group(1)} mechanical subcommands but the CLI "
                    f"defines {actual} — update the count and View 3 in the same "
                    f"commit the subcommand landed"))

    return findings


def cmd_coherence(args) -> int:
    root = Path(args.path).resolve()
    findings = coherence_findings(root, args.window)
    errors = [x for x in findings if x.severity == SEV_ERROR]
    warnings = [x for x in findings if x.severity == SEV_WARNING]
    infos = [x for x in findings if x.severity == SEV_INFO]
    if not args.quiet or errors:
        is_fw = (root / ".markdownllm").is_file()
        print(f"## Coherence Report — {root}")
        print(f"scope: {'framework root (+ catalog/kernel checks)' if is_fw else 'corpus (general checks only)'}\n")
        if not findings:
            print("No coherence issues found.")
        for title, group in (("Errors (must fix)", errors),
                             ("Warnings (should fix)", warnings),
                             ("Info (worth knowing)", infos)):
            if group:
                print(f"### {title}")
                for x in group:
                    print(f"- **{x.thing}**: {x.message}")
                print()
    return 1 if errors else 0




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
                rel = Path(os.path.relpath(Path(__file__).resolve(), root)).as_posix()
            except ValueError:
                rel = Path(__file__).resolve().as_posix()
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


def install_hook(root: Path) -> str:
    """Write the pre-commit validation hook into `root`'s git repo.
    Returns the mdllm path the hook will use (for reporting)."""
    git_dir = root / ".git"
    if not git_dir.is_dir():
        sys.exit(f"mdllm: {root} is not a git repository root")
    mdllm = Path(__file__).resolve()
    hook = git_dir / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    try:
        import os
        rel = Path(os.path.relpath(mdllm, root)).as_posix()
    except ValueError:  # e.g. different drives on Windows — no relative path exists
        rel = mdllm.as_posix()
    hook.write_text(HOOK_BODY.format(rel=rel), encoding="utf-8", newline="\n")
    try:
        hook.chmod(hook.stat().st_mode | 0o111)
    except OSError:
        pass  # Windows: executability is not a file-mode concern
    return rel


def cmd_install_hook(args) -> int:
    root = Path(args.path).resolve()
    rel = install_hook(root)
    print(f"installed {root / '.git' / 'hooks' / 'pre-commit'} (mdllm via {rel})")
    return 0


def cmd_scaffold(args) -> int:
    """The pre-domain-scaffold:isolate hard hook, mechanised. Owns the
    deterministic sequence of domain birth: directories, templates with
    mechanical placeholders substituted (name, dates, framework_root,
    framework_version_seen), a nested git repo, the outer repo's .gitignore
    isolation (added and committed BEFORE the domain's first commit, per the
    hard hook's ordering), the pre-commit hook, and the first commit.
    What remains semantic — thing types and vocabularies in _schema.yaml,
    skill content, AGENTS.md sections, the first real things — stays with
    the agent and the human, where it belongs."""
    import os
    fw_root = Path(__file__).resolve().parents[1]
    sentinel = fw_root / ".markdownllm"
    if not sentinel.is_file():
        sys.exit("mdllm: scaffold requires a framework checkout (.markdownllm not found)")
    fw_version = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {})
                     .get("version"))
    target = Path(args.path).resolve()
    name = target.name
    if not ID_RE.match(name):
        sys.exit(f"mdllm: domain folder name must be kebab-case (got {name!r})")
    if target.exists() and any(target.iterdir()):
        sys.exit(f"mdllm: {target} exists and is not empty")
    templates = fw_root / "templates"
    title = " ".join(w.capitalize() for w in name.split("-"))
    today = f"{dt.date.today():%Y-%m-%d}"
    try:
        rel_fw = Path(os.path.relpath(fw_root, target)).as_posix()
    except ValueError:
        rel_fw = fw_root.as_posix()

    def instantiate(text: str) -> str:
        text = (text.replace("[domain]", name)
                    .replace("[Domain Name]", title)
                    .replace("[Domain]", title)
                    .replace("[ISO-date]", today))
        text = re.sub(r"framework_root: \[[^\]]*\]", f"framework_root: {rel_fw}", text)
        text = re.sub(r"framework_version_seen: \[[^\]]*\]",
                      f"framework_version_seen: {fw_version}", text)
        return text

    (target / "things").mkdir(parents=True, exist_ok=True)
    (target / "skills").mkdir(exist_ok=True)
    written: list[str] = []
    (target / "AGENTS.md").write_text(
        instantiate((templates / "AGENTS.md.template").read_text(encoding="utf-8")),
        encoding="utf-8", newline="\n")
    written.append("AGENTS.md")
    (target / "things" / "_schema.yaml").write_text(
        (templates / "_schema.yaml.template").read_text(encoding="utf-8")
        .replace("[domain-name]", name),
        encoding="utf-8", newline="\n")
    written.append("things/_schema.yaml")
    for t in sorted(templates.glob("domain-*.skill.md.template")):
        out_name = t.name.replace("domain-", f"{name}-", 1)
        out_name = out_name[:-len(".template")]
        (target / "skills" / out_name).write_text(
            instantiate(t.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        written.append(f"skills/{out_name}")

    # Fill the domain-kernel managed blocks now that skills exist, so the entry
    # file is born in sync — otherwise the pre-commit coherence check would flag
    # the template's placeholder blocks as drift and block the first commit.
    ag = target / "AGENTS.md"
    ag_text = ag.read_text(encoding="utf-8")
    ag_meta, _, _ = parse_frontmatter(ag_text)
    ag_filled, _, _ = apply_domain_kernel(
        ag_text, build_domain_kernel_blocks(target, ag_meta or {}))
    ag.write_text(ag_filled, encoding="utf-8", newline="\n")

    # Deliberate-ritual slash commands (inert until the operator invokes them) —
    # Claude Code `.claude/commands/` and Copilot `.github/prompts/`. The
    # auto-firing SessionStart/PostToolUse adapter stays opt-in (hint printed below).
    cmd_dir = target / ".claude" / "commands"
    prm_dir = target / ".github" / "prompts"
    if (templates / "commands").is_dir():
        cmd_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted((templates / "commands").glob("*.md")):
            (cmd_dir / src.name).write_text(
                instantiate(src.read_text(encoding="utf-8")),
                encoding="utf-8", newline="\n")
            written.append(f".claude/commands/{src.name}")
    if (templates / "copilot-prompts").is_dir():
        prm_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted((templates / "copilot-prompts").glob("*.prompt.md")):
            (prm_dir / src.name).write_text(
                instantiate(src.read_text(encoding="utf-8")),
                encoding="utf-8", newline="\n")
            written.append(f".github/prompts/{src.name}")

    # Adapter: write .claude/settings.json so a new domain is hardened out of the
    # box — SessionStart injects the ritual, PostToolUse runs the floor on write.
    # One Claude-format file serves Claude Code AND VS Code Copilot (agent mode).
    # Paths key off rel_fw (framework_root). Still optional in spirit: delete it
    # and the domain kernel drives both by interpretation. Scaffold writes it
    # directly (it runs as the tool, not through a permissions-gated editor).
    import json as _json
    settings = target / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(_json.dumps({
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command",
                            "command": f"python {rel_fw}/tools/mdllm.py session-start ."}]}
            ],
            "PostToolUse": [
                {"matcher": "Write|Edit",
                 "hooks": [{"type": "command",
                            "command": f"python {rel_fw}/tools/mdllm.py validate . --quiet"}]}
            ],
        }
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    written.append(".claude/settings.json")

    # Isolation, in the hard hook's order: (1) domain repo exists,
    # (2)+(3) outer repo ignores the domain BEFORE any domain commit,
    # (4) domain's first commit. Step 5 (remote) stays with the human.
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    broken: list[str] = []  # any partial birth = exit 1; this hook's whole
    #                         point is that incomplete sequences cannot pass silently
    outer = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           cwd=target.parent, capture_output=True, text=True)
    isolated_in = None
    if outer.returncode == 0 and outer.stdout.strip():
        outer_root = Path(outer.stdout.strip())
        rel_t = Path(os.path.relpath(target, outer_root)).as_posix() + "/"
        gi = outer_root / ".gitignore"
        existing = gi.read_text(encoding="utf-8") if gi.is_file() else ""
        # Ask git before appending: a blanket rule (e.g. `domain/`) may already
        # isolate the path. A per-domain line — and the commit message naming it —
        # publishes which domains exist in the outer repo's history; domain names
        # are domain state, and domain state never enters the framework repo.
        already_ignored = subprocess.run(
            ["git", "check-ignore", "-q", rel_t],
            cwd=outer_root, capture_output=True).returncode == 0
        if not already_ignored and rel_t.rstrip("/") not in {
                ln.strip().rstrip("/") for ln in existing.splitlines()}:
            gi.write_text(existing.rstrip("\n") + ("\n" if existing else "")
                          + f"{rel_t}\n", encoding="utf-8", newline="\n")
            subprocess.run(["git", "add", ".gitignore"], cwd=outer_root, check=True)
            commit = subprocess.run(
                ["git", "commit", "-q", "-m", f"chore: isolate domain {rel_t} (scaffold)"],
                cwd=outer_root, capture_output=True, text=True)
            if commit.returncode != 0:
                broken.append(f"outer .gitignore updated but commit failed in "
                              f"{outer_root}: {commit.stderr.strip() or commit.stdout.strip()}")
        isolated_in = outer_root

    hook_via = install_hook(target)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    first = subprocess.run(
        ["git", "commit", "-q", "-m", f"scaffold: {name} — framework v{fw_version}"],
        cwd=target, capture_output=True, text=True)
    if first.returncode != 0:
        broken.append(f"first domain commit failed — configure git user.name/"
                      f"user.email, then commit. "
                      f"({first.stderr.strip() or first.stdout.strip()})")

    print(f"## Scaffolded {name} — {target}\n")
    for w in written:
        print(f"  wrote {w}")
    print(f"  git repo initialised; pre-commit hook installed (mdllm via {hook_via})")
    if isolated_in:
        print(f"  isolated: {isolated_in / '.gitignore'} ignores the domain")
    if first.returncode == 0:
        print(f"  first commit made (framework_version_seen: {fw_version})")
    for b in broken:
        print(f"  FAIL  {b}")
    print("\nStill yours (and your agent's) — the semantic half:")
    print("  - AGENTS.md: name, description, principles, thing types")
    print("  - things/_schema.yaml: declare your types and status vocabularies")
    print("  - skills/: fill the four skill bodies with the domain's reasoning")
    print("  - things/: create the first real things")
    print("  - a remote, if the domain should have one")
    print("  - hardened out of the box: .claude/settings.json fires session-start + "
          "post-write validation automatically (Claude Code / VS Code Copilot agent "
          "mode), and /end-session + /retrospective are installed. Delete .claude/ to "
          "fall back to interpretation-only — the domain kernel still drives both.")
    if broken:
        print("\nBIRTH SEQUENCE INCOMPLETE — the isolation invariant did not "
              "fully hold; fix the FAIL lines before using the domain.")
    return 1 if broken else 0


# ------------------------------------------------------------ mcp-serve
#
# The cross-domain producing side, on MCP (design: docs/plans/mcp-domain-server.md).
# Phase 1: the read-only face over stdio. The split below is the guardrail made
# literal — the SEMANTIC helpers (manifest/list/read/query/deliverable) reuse the
# floor's own `scan()`; the TRANSPORT (a minimal JSON-RPC stdio loop) is thin and
# replaceable. Swapping stdio for Streamable HTTP later touches only the loop.
# Pure stdlib, like the rest of the floor — `mcp` SDK is not a dependency.

MCP_PROTOCOL_VERSION = "2025-11-25"  # echoed back to the client if it offers one
MCP_SERVER_VERSION = "0.1"


class _RpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code, self.message = code, message


def mcp_domain_id(root: Path) -> str:
    # Phase 1: identity is the domain directory name (kebab). A domain that wants
    # to declare its own id can override this later — kept trivial on purpose.
    return root.name


def mcp_exposed_things(corpus: Corpus) -> list[Thing]:
    # Exposure is opt-in: only `exposed: true` things join the face. Nothing
    # crosses by default — the semi-permeable membrane, curated by the producer.
    return [t for t in corpus.things if t.meta.get("exposed") is True and t.id]


def _mcp_summary(t: Thing) -> str:
    for line in t.body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    for line in t.body.splitlines():
        if line.strip():
            return line.strip()
    return ""


# A crossing thing carries its descriptive frontmatter, never the producer's
# internal relationship graph: those ids live in the producer's id-space and are
# foreign / unresolvable to any consumer. Stripped on egress so the graph stays
# reasoning-opaque across the boundary (the bright line). A cross-domain link, if
# ever wanted, is a deliberate source-scoped exposure — never a raw leak of
# foreign ids. (Surfaced by the first road test: the consumer tried to resolve a
# producer-local `linked_things` id and found nothing.)
# The rule is "every relational field", not this list's history: `informed_by`
# (provenance pins) and `parties` (conflict members) carry producer-local ids
# just as much as `linked_things` does — they leaked for two versions because
# the list was built from the road test's symptom, not from the rule (review 6,
# finding 2).
_MCP_INTERNAL_GRAPH = ("linked_things", "dependencies", "blocks", "parent",
                       "definition", "triggers", "informed_by", "parties")


def _mcp_egress_meta(meta: dict) -> dict:
    return {k: v for k, v in meta.items() if k not in _MCP_INTERNAL_GRAPH}


def _mcp_render_thing(t: Thing) -> str:
    import yaml
    fm = yaml.safe_dump(_mcp_egress_meta(t.meta), sort_keys=False, allow_unicode=True)
    return f"---\n{fm}---\n\n{t.body.lstrip(chr(10))}"


def _mcp_thing_commit(root: Path, t: Thing) -> str:
    # The pin is *per-thing*: the last commit that touched this exposed thing,
    # not the domain HEAD — so a freshness check fires only when the consumed
    # thing actually changed, not on any commit to the source. Computed
    # source-side; only the resulting commit crosses, never the file path.
    try:
        rel = t.path.relative_to(root)
    except ValueError:
        rel = t.path
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%h", "--", str(rel)],
                             cwd=root, capture_output=True, text=True, check=True)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def mcp_list_tools() -> list[dict]:
    tools = [
        {"name": "query_things",
         "description": "List this domain's exposed things, optionally filtered by "
                        "type, tag, status, or free text. Browse the face.",
         "inputSchema": {"type": "object", "properties": {
             "type": {"type": "string"}, "tag": {"type": "string"},
             "status": {"type": "string"}, "text": {"type": "string"}}}},
        {"name": "get_deliverable",
         "description": "Fetch one exposed thing as a quarantined external "
                        "deliverable, stamped with its provenance reference triple "
                        "(source_domain, source_id, source_commit).",
         "inputSchema": {"type": "object",
                         "properties": {"id": {"type": "string"}},
                         "required": ["id"]}},
    ]
    return tools


def mcp_query_things(corpus: Corpus, typ=None, tag=None, status=None, text=None) -> list[dict]:
    rows = []
    for t in mcp_exposed_things(corpus):
        m = t.meta
        if typ and str(m.get("type")) != str(typ):
            continue
        if status and str(m.get("status")) != str(status):
            continue
        if tag:
            tags = m.get("tags") or []
            if not (isinstance(tags, list) and tag in tags):
                continue
        if text and text.lower() not in (f"{t.id} {_mcp_summary(t)} {t.body}").lower():
            continue
        rows.append({"id": t.id, "type": m.get("type"),
                     "status": m.get("status"), "summary": _mcp_summary(t)})
    return rows


def mcp_get_deliverable(root: Path, corpus: Corpus, domain_id: str, tid: str) -> dict | None:
    # Allowlist lookup by id — never builds a filesystem path from caller input,
    # so the path-traversal / argument-injection class (the 2026 reference-server
    # CVEs) cannot apply. Only an *exposed* id resolves.
    t = {x.id: x for x in mcp_exposed_things(corpus)}.get(tid)
    if t is None:
        return None
    return {"reference_triple": {"source_domain": domain_id, "source_id": tid,
                                 "source_commit": _mcp_thing_commit(root, t)},
            "frontmatter": _mcp_egress_meta(t.meta), "content": t.body}


def mcp_build_manifest(root: Path, corpus: Corpus, domain_id: str) -> dict:
    # Server Card-shaped (the emerging MCP automatic-discovery convention). Each
    # `knows` entry carries the thing's per-thing `source_commit` so a consumer's
    # freshness check reads current pins from the face in one call.
    things = mcp_exposed_things(corpus)
    return {"name": domain_id, "domain_id": domain_id,
            "head_commit": git_short_sha(root),
            "liveness": "corpus",
            "knows": [{"id": t.id, "type": t.meta.get("type"),
                       "status": t.meta.get("status"), "summary": _mcp_summary(t),
                       "source_commit": _mcp_thing_commit(root, t)}
                      for t in things],
            "can_do": [tool["name"] for tool in mcp_list_tools()],
            "who_i_know": []}  # outbound address book — a later phase


def mcp_list_resources(corpus: Corpus, domain_id: str) -> list[dict]:
    res = [{"uri": f"manifest://{domain_id}", "name": f"{domain_id} manifest",
            "description": "Domain porch: identity, exposed catalog, capabilities.",
            "mimeType": "application/json"}]
    for t in mcp_exposed_things(corpus):
        res.append({"uri": f"thing://{domain_id}/{t.id}", "name": t.id,
                    "description": _mcp_summary(t), "mimeType": "text/markdown"})
    return res


def mcp_read_resource(root: Path, corpus: Corpus, domain_id: str, uri: str) -> dict | None:
    import json
    if uri == f"manifest://{domain_id}":
        return {"uri": uri, "mimeType": "application/json",
                "text": json.dumps(mcp_build_manifest(root, corpus, domain_id),
                                    indent=2, default=str)}
    prefix = f"thing://{domain_id}/"
    if uri.startswith(prefix):
        t = {x.id: x for x in mcp_exposed_things(corpus)}.get(uri[len(prefix):])
        if t is None:
            return None
        return {"uri": uri, "mimeType": "text/markdown", "text": _mcp_render_thing(t)}
    return None


def cmd_mcp_serve(args) -> int:
    import json
    root = Path(args.path).resolve()
    if not root.is_dir():
        sys.exit(f"mdllm: not a directory: {root}")
    corpus, _ = scan(root)
    domain_id = mcp_domain_id(root)

    def log(msg: str) -> None:
        print(f"mcp-serve[{domain_id}]: {msg}", file=sys.stderr, flush=True)

    def emit(obj: dict) -> None:  # transport: one JSON-RPC message per line on stdout
        sys.stdout.write(json.dumps(obj, default=str) + "\n")
        sys.stdout.flush()

    def handle(method: str, params: dict):
        if method.startswith("notifications/"):
            return None  # client-side lifecycle notice — nothing to answer
        if method == "initialize":
            return {"protocolVersion": params.get("protocolVersion", MCP_PROTOCOL_VERSION),
                    "capabilities": {"resources": {}, "tools": {}},
                    "serverInfo": {"name": f"mdllm-domain:{domain_id}",
                                   "version": MCP_SERVER_VERSION}}
        if method == "ping":
            return {}
        if method == "resources/list":
            return {"resources": mcp_list_resources(corpus, domain_id)}
        if method == "resources/read":
            c = mcp_read_resource(root, corpus, domain_id, params.get("uri", ""))
            if c is None:
                raise _RpcError(-32002, f"resource not found or not exposed: {params.get('uri')}")
            return {"contents": [c]}
        if method == "tools/list":
            return {"tools": mcp_list_tools()}
        if method == "tools/call":
            name, a = params.get("name", ""), params.get("arguments") or {}
            if name == "query_things":
                rows = mcp_query_things(corpus, a.get("type"), a.get("tag"),
                                        a.get("status"), a.get("text"))
                return {"content": [{"type": "text", "text": json.dumps(rows, indent=2, default=str)}]}
            if name == "get_deliverable":
                d = mcp_get_deliverable(root, corpus, domain_id, a.get("id", ""))
                if d is None:
                    return {"content": [{"type": "text",
                            "text": f"not found or not exposed: {a.get('id')!r}"}], "isError": True}
                return {"content": [{"type": "text", "text": json.dumps(d, indent=2, default=str)}]}
            return {"content": [{"type": "text", "text": f"unknown tool: {name!r}"}], "isError": True}
        raise _RpcError(-32601, f"method not found: {method}")

    log(f"serving {len(mcp_exposed_things(corpus))} exposed thing(s) over stdio "
        f"(MCP {MCP_PROTOCOL_VERSION})")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log("dropped non-JSON line")
            continue
        method, mid = msg.get("method"), msg.get("id")
        if method is None:  # a response or unknown frame — not ours to answer
            continue
        try:
            result = handle(method, msg.get("params") or {})
            if mid is not None:  # notifications (no id) get no reply
                emit({"jsonrpc": "2.0", "id": mid, "result": result})
        except _RpcError as e:
            if mid is not None:
                emit({"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": e.message}})
        except Exception as e:  # noqa: BLE001 — transport must not die on one bad call
            log(f"error handling {method}: {e}")
            if mid is not None:
                emit({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)}})
    return 0


# ----------------------------------------------------- imports-check (freshness)
#
# Phase 2: re-quarantine-on-drift, the consumer-side standing check. The upward
# version-check generalised from the one privileged source (the framework, the
# vertical/substrate axis) to an arbitrary source_domain (the horizontal/peer
# axis). It reads the source's *exposed face* through MCP — never its git — so the
# freshness signal obeys the same membrane as content: everything the consumer
# learns about the source crosses through the porch. Report-only: detection is
# mechanical, the re-quarantine (flip to stale / verified:false) is the agent's
# disposition (the floor never mutates a domain's things).


def _load_address_book(consumer_root: Path) -> dict:
    # The consumer's `.mcp.json` mcpServers map IS the address book — operator-
    # wired, per trust zone. name -> {command, args}.
    import json
    p = consumer_root / ".mcp.json"
    if not p.is_file():
        return {}
    try:
        return (json.loads(p.read_text(encoding="utf-8")) or {}).get("mcpServers", {}) or {}
    except Exception:
        return {}


def _mcp_client_manifest(command: str, args: list, cwd: Path, source_domain: str,
                         timeout: int = 30) -> dict | None:
    # A minimal MCP stdio *client*: spawn the source's server, read its manifest
    # through the face. Returns the parsed manifest, or None when the source is
    # unreachable (bad command/path, spawn failure, timeout, malformed) — the
    # honest "freshness unknown" answer, never a silent "fresh".
    import json
    reqs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "resources/read",
             "params": {"uri": f"manifest://{source_domain}"}}]
    payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
    try:
        out = subprocess.run([command, *args], input=payload, cwd=str(cwd),
                             capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None
    for line in out.stdout.splitlines():
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == 2 and "result" in msg:
            try:
                return json.loads(msg["result"]["contents"][0]["text"])
            except Exception:
                return None
    return None


def imports_freshness(consumer_root: Path) -> list[dict]:
    corpus, _ = scan(consumer_root)
    book = _load_address_book(consumer_root)
    manifests: dict[str, tuple[str, dict | None]] = {}  # spawn each source once
    results = []
    for t in corpus.things:
        m = t.meta
        if str(m.get("origin")) != "external":
            continue
        sd, sid, pin = m.get("source_domain"), m.get("source_id"), m.get("source_commit")
        if not (sd and sid and pin):
            results.append({"id": t.id, "state": "incomplete",
                            "detail": "missing source_domain/source_id/source_commit"})
            continue
        if sd not in manifests:
            cfg = book.get(sd)
            if not cfg or not cfg.get("command"):
                manifests[sd] = ("no-address", None)
            else:
                man = _mcp_client_manifest(cfg["command"], cfg.get("args", []),
                                           consumer_root, sd)
                manifests[sd] = ("ok", man) if man else ("unreachable", None)
        state, man = manifests[sd]
        row = {"id": t.id, "source": f"{sd}/{sid}", "pin": pin}
        if state == "no-address":
            row["state"] = "no-address-book-entry"
        elif state == "unreachable":
            row["state"] = "unreachable"  # freshness unknown — the honest answer
        else:
            current = next((k.get("source_commit") for k in man.get("knows", [])
                            if k.get("id") == sid), None)
            if current is None:
                row["state"] = "withdrawn"  # no longer exposed by the source
            else:
                row["current"] = current
                row["state"] = "fresh" if current == pin else "stale"
        results.append(row)
    return results


def cmd_imports_check(args) -> int:
    root = Path(args.path).resolve()
    rows = imports_freshness(root)
    if not rows:
        print(f"imports-check: no external imports in {root.name}")
        return 0
    print(f"## Imports Freshness — {root.name}\n")
    order = {"stale": 0, "unreachable": 1, "withdrawn": 2, "no-address-book-entry": 3,
             "incomplete": 4, "fresh": 5}
    for r in sorted(rows, key=lambda r: order.get(r["state"], 9)):
        if r["state"] == "stale":
            print(f"- STALE      {r['id']}  ({r['source']})  pinned {r['pin']} -> now {r['current']}")
            print("             re-quarantine: re-read the source, then flip `verified: false`, `status: stale`")
        elif r["state"] == "fresh":
            print(f"- fresh      {r['id']}  ({r['source']})  @ {r['pin']}")
        elif r["state"] == "unreachable":
            print(f"- UNKNOWN    {r['id']}  ({r['source']})  unreachable — freshness cannot be determined")
        elif r["state"] == "withdrawn":
            print(f"- WITHDRAWN  {r['id']}  ({r['source']})  source no longer exposes `{r['source'].split('/')[-1]}`")
        elif r["state"] == "no-address-book-entry":
            print(f"- NO-ROUTE   {r['id']}  ({r['source']})  no .mcp.json entry for source domain")
        else:
            print(f"- INCOMPLETE {r['id']}  {r.get('detail','')}")
    stale = sum(1 for r in rows if r["state"] == "stale")
    print(f"\n{len(rows)} import(s); {stale} stale. Freshness is advisory — disposition is yours.")
    return 0


# ---------------------------------------------------------------- main


def build_cli() -> argparse.ArgumentParser:
    # Separate from main() so the parser registry is introspectable: generated
    # prose that names a subcommand is tested against THIS, not against the
    # builder that wrote it (a same-builder check is blind to a
    # self-contradictory builder — the phantom `mdllm orient` incident).
    p = argparse.ArgumentParser(prog="mdllm", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Levels 1-3 mechanical validation")
    v.add_argument("path", nargs="?", default=".")
    v.add_argument("--quiet", action="store_true", help="only print on Errors")
    v.set_defaults(fn=cmd_validate)

    t = sub.add_parser("triggers", help="evaluate trigger conditions")
    t.add_argument("path", nargs="?", default=".")
    t.set_defaults(fn=cmd_triggers)

    i = sub.add_parser("index", help="check or rebuild derived indexes")
    i.add_argument("path", nargs="?", default=".")
    i.add_argument("action", choices=["check", "rebuild"])
    i.add_argument("--signal", choices=["triggers", "schema", "relationships", "provenance"])
    i.set_defaults(fn=cmd_index)

    tp = sub.add_parser("touchpoints", help="Assimilate beat: what a thing's change "
                                            "disturbs (declared edges + literal refs)")
    tp.add_argument("id", help="the thing id to assimilate around")
    tp.add_argument("path", nargs="?", default=".")
    tp.set_defaults(fn=cmd_touchpoints)

    cs = sub.add_parser("cascade", help="post-completion cascade: what a thing's "
                                        "completion unblocks downstream (mirror of touchpoints)")
    cs.add_argument("id", help="the thing id that just reached a terminal status")
    cs.add_argument("path", nargs="?", default=".")
    cs.set_defaults(fn=cmd_cascade)

    pv = sub.add_parser("provenance", help="validate provenance chains (provenance.md)")
    pv.add_argument("path", nargs="?", default=".")
    pv.set_defaults(fn=cmd_provenance)

    k = sub.add_parser("tokens", help="measure spec token costs by tier")
    k.add_argument("path", nargs="?", default=".")
    k.set_defaults(fn=cmd_tokens)

    ev = sub.add_parser("eval", help="check a golden-scenario fixture against domain state")
    ev.add_argument("path", nargs="?", default=".")
    ev.add_argument("--fixture")
    ev.add_argument("--run", action="store_true",
                    help="Stage 2: seed workspace + headless agent + assert")
    ev.add_argument("--model", default="haiku")
    ev.add_argument("--trials", type=int, default=1)
    ev.add_argument("--bare", action="store_true",
                    help="no-framework condition: strip AGENTS.md/skills/schema")
    ev.add_argument("--report", action="store_true",
                    help="aggregate evals/runs/*/result.json into per-cell pass rates")
    ev.add_argument("--dry-run", action="store_true")
    ev.add_argument("--timeout", type=int, default=900,
                    help="seconds per trial (default 900)")
    ev.set_defaults(fn=cmd_eval)

    kn = sub.add_parser("kernel", help="generate kernel.md from spec kernel blocks")
    kn.add_argument("path", nargs="?", default=".")
    kn.add_argument("--check", action="store_true",
                    help="drift check: compare kernel.md against a fresh build")
    kn.set_defaults(fn=cmd_kernel)

    dk = sub.add_parser("domain-kernel",
                        help="generate/refresh a domain AGENTS.md's managed operative blocks")
    dk.add_argument("path", nargs="?", default=".")
    dk.add_argument("--check", action="store_true",
                    help="drift check: compare managed blocks against a fresh build")
    dk.set_defaults(fn=cmd_domain_kernel)

    ss = sub.add_parser("session-start",
                        help="emit the session-start ritual (version + velocity) for a "
                             "harness SessionStart hook to inject")
    ss.add_argument("path", nargs="?", default=".")
    ss.set_defaults(fn=cmd_session_start)

    co = sub.add_parser("coherence", help="dark-region checks: generated-artifact "
                                          "freshness, catalog/filesystem, stale labels")
    co.add_argument("path", nargs="?", default=".")
    co.add_argument("--window", type=int, default=15,
                    help="stable-staleness lookback in commits (default 15)")
    co.add_argument("--quiet", action="store_true", help="only print on Errors")
    co.set_defaults(fn=cmd_coherence)

    c = sub.add_parser("changelog", help="draft a CHANGELOG entry from commits")
    c.add_argument("path", nargs="?", default=".")
    c.add_argument("--since", help="ref to start from (e.g. a version tag)")
    c.set_defaults(fn=cmd_changelog)

    wl = sub.add_parser("worklog", help="print a session-grouped view of the commit stream (on-demand; not committed)")
    wl.add_argument("path", nargs="?", default=".")
    wl.add_argument("--write", action="store_true", help="save a local (gitignored) WORKLOG.md snapshot; default prints to stdout")
    wl.set_defaults(fn=cmd_worklog)

    rf = sub.add_parser("refresh", help="floor-only domain refresh: report version "
                                        "delta + unseen CHANGELOG; --seal bumps seen")
    rf.add_argument("path", nargs="?", default=".", help="the domain directory")
    rf.add_argument("--seal", action="store_true",
                    help="after adoption: bump framework_version_seen in domain AGENTS.md")
    rf.set_defaults(fn=cmd_refresh)

    d = sub.add_parser("doctor", help="probe the environment: floor prerequisites, "
                                      "hook execution, framework version drift")
    d.add_argument("path", nargs="?", default=".")
    d.set_defaults(fn=cmd_doctor)

    sc = sub.add_parser("scaffold", help="deterministic domain birth: templates, "
                                         "nested repo, .gitignore isolation, hook, "
                                         "first commit")
    sc.add_argument("path", help="folder to create (its name becomes the domain name)")
    sc.set_defaults(fn=cmd_scaffold)

    h = sub.add_parser("install-hook", help="install git pre-commit validation hook")
    h.add_argument("path", nargs="?", default=".")
    h.set_defaults(fn=cmd_install_hook)
    # Hook body is portable since v3.4.1: root/interpreter resolved at run time.

    ms = sub.add_parser("mcp-serve", help="serve a domain's exposed face over MCP "
                        "(stdio) — the cross-domain producing side (Phase 1: read-only)")
    ms.add_argument("path", help="path to the domain directory to serve")
    ms.set_defaults(fn=cmd_mcp_serve)

    ic = sub.add_parser("imports-check", help="re-quarantine-on-drift: check a "
                        "domain's external imports against their sources' exposed faces")
    ic.add_argument("path", nargs="?", default=".", help="the consumer domain")
    ic.set_defaults(fn=cmd_imports_check)

    return p


def main() -> int:
    # Windows consoles default to a legacy codepage; spec prose is UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = build_cli().parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
