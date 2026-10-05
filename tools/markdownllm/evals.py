"""The eval harness — golden-scenario fixtures against domain state.

Stage 1: deterministic assertions against an existing corpus. Stage 2
(--run): seed an isolated workspace and drive fresh headless agents (single
prompt or a longitudinal `sessions:` chain), asserting after each session.
evals/results/ is the committed evidence mirror.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from decimal import Decimal
from pathlib import Path

import yaml

from .calc import CalcError, to_decimal
from .yaml_loader import load_version_sentinel, load_yaml_mapping

from .model import Corpus, SEV_ERROR, SEV_INFO, SEV_WARNING, scan
from .validation import validation_reports


def _full_validation_errors(root: Path) -> list:
    """The exact Error set behind ``mdllm validate``, without reformatting."""
    return [finding
            for _, _, findings in validation_reports(root)
            for finding in findings if finding.severity == SEV_ERROR]


def _validation_summary(root: Path) -> dict[str, int]:
    """Count the complete validation boundary without dropping scan findings."""
    counts = {SEV_ERROR: 0, SEV_WARNING: 0, SEV_INFO: 0}
    for _, _, findings in validation_reports(root):
        for finding in findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
    return {
        "errors": counts[SEV_ERROR],
        "warnings": counts[SEV_WARNING],
        "info": counts[SEV_INFO],
    }


def _validation_control_failure(assertions: list[dict],
                                summary: dict[str, int]) -> bool:
    """Whether validation needs its own trial-level control failure.

    An explicit ``validates_clean`` assertion already represents the same
    complete boundary and must not be double-counted.  Without that assertion,
    validation remains an unconditional integrity leg of an agent-run trial.
    """
    declared = any("validates_clean" in item
                   for item in assertions if isinstance(item, dict))
    return bool(summary.get("errors")) and not declared


def _run_id(model: str, condition: str, trial: int) -> str:
    """Collision-resistant, path-safe evidence identity.

    Second-resolution ids collided during repeated/concurrent trials.  Time is
    retained for operator readability; a UUID suffix supplies identity.
    """
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    safe_model = re.sub(r"[^A-Za-z0-9._-]+", "-", str(model)).strip("-") or "model"
    return f"{stamp}-{safe_model}-{condition}-t{trial}-{uuid.uuid4().hex[:10]}"


def _git_value(root: Path, *args: str) -> str | None:
    out = subprocess.run(["git", *args], cwd=root, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


def _agent_failure(proc, stdout_meta: object) -> str | None:
    """Return the invocation failure reason; success is ``None``.

    Process, transport and agent-reported success are separate facts.  An eval
    trial cannot be green when any one of them is red or unreadable.
    """
    if proc.returncode != 0:
        return f"process exited {proc.returncode}"
    if not isinstance(stdout_meta, dict):
        return "agent stdout is not a JSON object"
    if stdout_meta.get("is_error"):
        return f"agent reported error ({stdout_meta.get('subtype') or 'unspecified'})"
    if stdout_meta.get("subtype") not in (None, "success"):
        return f"agent subtype is {stdout_meta.get('subtype')!r}, not success"
    return None


def _command_version(executable: str) -> str:
    """Return an observed harness build string, or an explicit unknown.

    A successful agent trial without the executable build is not reproducible
    evidence.  Version probing is deliberately bounded and never promotes the
    framework version into a vendor-build claim.
    """
    try:
        proc = subprocess.run(
            [executable, "--version"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unknown ({type(exc).__name__})"
    text = (proc.stdout or proc.stderr or "").strip()
    if proc.returncode != 0 or not text:
        return f"unknown (version command exited {proc.returncode})"
    return text.splitlines()[0].strip()


def _eval_run_dir(root: Path, run_id: str) -> Path:
    """Resolve an isolated workspace and refuse a source-tree descendant."""
    base = Path(os.environ.get(
        "MDLLM_EVAL_RUN_ROOT",
        str(Path(tempfile.gettempdir()) / "mdllm-evals"))).resolve()
    candidate = (base / run_id).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return candidate
    raise ValueError(
        "eval workspace must be outside the framework/source repository; "
        "set MDLLM_EVAL_RUN_ROOT to an isolated directory")


CONDITIONS = ("framework", "bare", "bare-coached")

# What the framework arm is allowed to see of the framework checkout. The
# full root contains evals/ — every fixture's expected figures and the
# generators that print them — so granting it was granting the answer key
# (cold review, 2026-10-05). The view carries the operating layer only.
FRAMEWORK_VIEW_INCLUDE = (
    ".markdownllm", "AGENTS.md", "CLAUDE.md", "kernel.md",
    "thing.md", "orchestration.md", "read.thing.md", "write.thing.md",
    "validate.thing.md", "git-workflow.md", "provenance.md",
    "change-reconciliation.md", "trigger-specification.md",
    "docs/calculation-reference.md",
    "tools/mdllm.py", "tools/mdllm.ps1", "tools/markdownllm",
)
FRAMEWORK_VIEW_EXCLUDE_DIRS = ("__pycache__", "tests")
ANSWER_KEY_PATTERNS = (r"evals[\\/]", r"polar_station_htc", r"-longitudinal\.yaml",
                       r"sleeping-bag-fac\.yaml", r"vat-quarter-basic\.yaml")


def _tree_fingerprint(base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        if any(part in FRAMEWORK_VIEW_EXCLUDE_DIRS for part in path.relative_to(base).parts):
            continue
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_framework_view(root: Path, run_root: Path) -> Path:
    """Materialise the pruned framework the framework arm is granted.

    `MDLLM_EVAL_FRAMEWORK_DIR` names a prepared view instead. The view is
    rebuilt per command invocation and shared read-only by its trials; its
    fingerprint is checked after every trial (the same guard the seed has).
    """
    import shutil
    override = os.environ.get("MDLLM_EVAL_FRAMEWORK_DIR")
    if override:
        view = Path(override).resolve()
        if not view.is_dir():
            sys.exit(f"mdllm: MDLLM_EVAL_FRAMEWORK_DIR is not a directory: {view}")
        if (view / "evals").exists():
            sys.exit("mdllm: MDLLM_EVAL_FRAMEWORK_DIR contains evals/ — that is "
                     "the answer key; prune it")
        return view
    view = run_root / f"framework-view-{uuid.uuid4().hex[:8]}"
    view.mkdir(parents=True)
    for rel in FRAMEWORK_VIEW_INCLUDE:
        src = root / rel
        dst = view / rel
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                *FRAMEWORK_VIEW_EXCLUDE_DIRS))
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return view


def _answer_key_hits(text: str) -> list[str]:
    return sorted({m.group(0) for pat in ANSWER_KEY_PATTERNS
                   for m in re.finditer(pat, text or "")})


def _git_dirty(run_dir: Path) -> bool:
    out = subprocess.run(["git", "status", "--porcelain"], cwd=run_dir,
                         capture_output=True, text=True, encoding="utf-8")
    return bool(out.stdout.strip())


def _reset_to_committed(run_dir: Path) -> None:
    """Committed state is the carrier between sessions, by construction."""
    subprocess.run(["git", "reset", "-q", "--hard"], cwd=run_dir, check=True)
    subprocess.run(["git", "clean", "-fdq"], cwd=run_dir, check=True)


def _seed_fingerprint(seed: Path) -> str:
    """One digest over the seed tree's bytes — the run's input identity.

    Hashes every file's workspace-relative path and content, so an edit,
    an addition and a deletion all move the digest, committed or not.
    Git is deliberately not consulted: the 2026-07 contamination was
    *committed* to the framework repo, so a HEAD comparison would have
    moved with it and agreed with the damage.
    """
    digest = hashlib.sha256()
    for path in sorted(p for p in seed.rglob("*") if p.is_file()):
        digest.update(path.relative_to(seed).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _results_exit_code(results: list[dict]) -> int:
    return 1 if any(r.get("failed", 0) for r in results) else 0

def check_assertions(fixture: dict, domain_root: Path) -> tuple[int, int, list[str]]:
    """Stage 1: deterministic assertions against a domain's current state."""
    records = check_assertions_detailed(fixture, domain_root)
    passed = sum(1 for r in records if r["passed"])
    return passed, len(records) - passed, [r["line"] for r in records]


def check_assertions_detailed(fixture: dict, domain_root: Path) -> list[dict]:
    """One record per assertion: {label, passed, changed, line}.

    `changed` is the fixture's tag (a longitudinal generator marks whether
    the asserted value moved since the previous session); a do-nothing agent
    passes every unchanged assertion, so only the changed set discriminates.

    `domain_root` is the workspace; if the fixture declares `domain_dir`
    (scaffold-style fixtures, where the agent *creates* the domain in a
    subfolder), thing/status/field/link/validates assertions scan that
    subfolder while file/git assertions stay workspace-relative."""
    ws = domain_root
    droot = (ws / fixture["domain_dir"]) if fixture.get("domain_dir") else ws
    corpus, _ = scan(droot) if droot.is_dir() else (Corpus(root=droot), [])
    by_id = corpus.by_id()
    records: list[dict] = []
    current: dict | None = None

    def report(ok: bool, label: str):
        changed = current.get("changed") if isinstance(current, dict) else None
        tag = "" if changed is None else (" [changed]" if changed else " [unchanged]")
        records.append({"label": label, "passed": bool(ok), "changed": changed,
                        "line": f"  {'PASS' if ok else 'FAIL'}  {label}{tag}"})

    for a in fixture.get("assertions") or []:
        current = a
        if "things_of_type" in a:
            tt = a["things_of_type"]
            n = sum(1 for t in corpus.things if str(t.meta.get("type")) == tt["type"])
            report(n >= tt.get("min", 1),
                   f"things of type {tt['type']}: {n} (need >= {tt.get('min', 1)})")
        elif "thing_exists" in a:
            tid = a["thing_exists"]
            report(tid in by_id, f"thing exists: {tid}")
        elif "status" in a:
            s = a["status"]
            t = by_id.get(s["id"])
            actual = str(t.meta.get("status")) if t else "<missing>"
            report(actual == str(s["equals"]),
                   f"status of {s['id']} == {s['equals']} (actual: {actual})")
        elif "field" in a:
            fa = a["field"]
            t = by_id.get(fa["id"])
            actual = t.meta.get(fa["name"]) if t else "<missing>"
            expected = fa["equals"]
            if (isinstance(expected, (int, float, Decimal))
                    and not isinstance(expected, bool)):
                # Compare numeric contracts through the exact-decimal
                # boundary *before* Python float equality.  LexicalFloat is a
                # float-compatible YAML value, so two distinct long lexemes
                # can otherwise compare equal after binary rounding.
                try:
                    ok = to_decimal(actual, "actual") == to_decimal(
                        expected, "expected")
                except (CalcError, TypeError, ValueError):
                    ok = False
            else:
                ok = actual == expected
            report(ok, f"{fa['id']}.{fa['name']} == {expected!r} (actual: {actual!r})")
        elif "link" in a:
            ln = a["link"]
            t = by_id.get(ln["from"])
            ok = bool(t) and any(
                isinstance(e, dict) and e.get("id") == ln["to"]
                and e.get("relation") == ln["relation"]
                for e in t.meta.get("linked_things") or [])
            report(ok, f"link: {ln['from']} --{ln['relation']}--> {ln['to']}")
        elif "validates_clean" in a:
            errs = _full_validation_errors(droot)
            report(not errs, f"validates clean (Errors: {len(errs)})")
        elif "file_exists" in a:
            paths = a["file_exists"]
            paths = [paths] if isinstance(paths, str) else paths
            report(any((ws / p).exists() for p in paths),
                   f"file exists: {' or '.join(paths)}")
        elif "file_contains" in a:
            fc = a["file_contains"]
            f_ = ws / fc["path"]
            ok = f_.is_file() and fc["text"] in f_.read_text(encoding="utf-8")
            report(ok, f"{fc['path']} contains {fc['text']!r}")
        elif "git_repo" in a:
            report((ws / a["git_repo"] / ".git").exists(),
                   f"own git repo: {a['git_repo']}")
        elif "git_commits" in a:
            gc = a["git_commits"]
            tgt = ws / gc["path"]
            n = 0
            if (tgt / ".git").exists():
                out = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                                     cwd=tgt, capture_output=True, text=True)
                if out.returncode == 0 and out.stdout.strip().isdigit():
                    n = int(out.stdout.strip())
            report(n >= gc.get("min", 1),
                   f"git commits in {gc['path']}: {n} (need >= {gc.get('min', 1)})")
        elif "min_things" in a:
            report(len(corpus.things) >= a["min_things"],
                   f"things in domain >= {a['min_things']} (actual: {len(corpus.things)})")
        else:
            report(False, f"unknown assertion: {a}")
    return records


def seed_run_dir(root: Path, fixture: dict, run_dir: Path, bare: bool,
                 framework_view: Path | None = None) -> None:
    """Stage 2 workspace: copy the seed into an isolated git repo.

    `bare` is true for both no-framework conditions (bare, bare-coached) —
    what differs between them is the prompt preamble, not the tree."""
    import shutil
    seed = root / fixture["seed"]
    if not seed.is_dir():
        sys.exit(f"mdllm: fixture seed not found: {seed}")
    shutil.copytree(seed, run_dir)
    if bare:
        # The no-framework condition: same data, no operating system.
        for p in ("AGENTS.md", "CLAUDE.md", "things/_schema.yaml"):
            f = run_dir / p
            if f.exists():
                f.unlink()
        skills = run_dir / "skills"
        if skills.is_dir():
            shutil.rmtree(skills)
    elif framework_view is not None:
        # The seed's relative framework_root pointed at the source checkout;
        # in the isolated workspace it resolves to nothing. Point it at the
        # granted view so the agent does not spend turns hunting.
        agents = run_dir / "AGENTS.md"
        if agents.is_file():
            text = agents.read_text(encoding="utf-8")
            new = re.sub(r"^framework_root:.*$",
                         f"framework_root: {framework_view.as_posix()}",
                         text, count=1, flags=re.M)
            if new != text:
                agents.write_text(new, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=run_dir, check=True)
    subprocess.run(["git", "add", "-A"], cwd=run_dir, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=run_dir, check=True)


def eval_report(root: Path) -> int:
    """Aggregate evals/results/*.json (the committed evidence mirror; legacy
    fallback: evals/runs/*/result.json) into per-cell pass rates."""
    import json as _json
    results = []
    res_dir = root / "evals" / "results"
    paths = sorted(res_dir.glob("*.json")) if res_dir.is_dir() else []
    if not paths:
        runs_dir = root / "evals" / "runs"
        paths = sorted(runs_dir.glob("*/result.json")) if runs_dir.is_dir() else []
    for rj in paths:
        try:
            results.append(_json.loads(rj.read_text(encoding="utf-8")))
        except ValueError:
            print(f"  skipping unparseable {rj}")
    if not results:
        print(f"No run results under {runs_dir}")
        return 1
    cells: dict[tuple[str, str, str, str], list[dict]] = {}
    for r in results:
        # Legacy runs predate the fixture tag (the 2026-06-11 2x2 was all one
        # fixture); group them under their known name rather than "?".
        fx = str(r.get("fixture", "VAT quarter prep (synthetic, known-correct figures)"))
        # A regenerated fixture is a different fixture: group by its bytes.
        sha = str(r.get("fixture_sha256") or "legacy")[:8]
        cells.setdefault((fx, sha, str(r.get("model")), str(r.get("condition"))),
                         []).append(r)
    print(f"## Eval Report — {len(results)} trials, {len(cells)} cells\n")
    print("| fixture | fixture sha | model | condition | trials | fully passing | "
          "assertion pass rate | changed-set pass rate | voided | mean wall s | mean cost $ |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for (fx, sha, model, cond), rs in sorted(cells.items()):
        full = sum(1 for r in rs if r.get("failed") == 0 and not r.get("voided"))
        voided = sum(1 for r in rs if r.get("voided"))
        p = sum(r.get("passed", 0) for r in rs)
        f_ = sum(r.get("failed", 0) for r in rs)
        rate = f"{p}/{p + f_} ({p / (p + f_):.0%})" if p + f_ else "—"
        cp = sum((s.get("changed") or {}).get("passed", 0)
                 for r in rs for s in r.get("sessions") or [])
        ct = sum((s.get("changed") or {}).get("total", 0)
                 for r in rs for s in r.get("sessions") or [])
        crate = f"{cp}/{ct} ({cp / ct:.0%})" if ct else "—"
        walls = [r["wall_s"] for r in rs if r.get("wall_s") is not None]
        costs = [r["cost_usd"] for r in rs if r.get("cost_usd") is not None]
        mw = f"{sum(walls) / len(walls):.0f}" if walls else "—"
        mc = f"{sum(costs) / len(costs):.3f}" if costs else "—"
        fx_short = fx if len(fx) <= 40 else fx[:37] + "..."
        print(f"| {fx_short} | {sha} | {model} | {cond} | {len(rs)} | {full}/{len(rs)} "
              f"| {rate} | {crate} | {voided} | {mw} | {mc} |")
    # Per-session view for longitudinal cells: where in the chain drift enters
    # is the finding, and the aggregate cannot show it.
    longi = {k: rs for k, rs in cells.items() if any(r.get("sessions") for r in rs)}
    if longi:
        print("\n### Per session (longitudinal cells)\n")
        print("| fixture sha | model | condition | session | trials passing | "
              "changed-set | unchanged-set | left uncommitted |")
        print("|---|---|---|---|---|---|---|---|")
        for (fx, sha, model, cond), rs in sorted(longi.items()):
            names: list[str] = []
            for r in rs:
                for s in r.get("sessions") or []:
                    if s["name"] not in names:
                        names.append(s["name"])
            for sn in names:
                ss = [s for r in rs for s in r.get("sessions") or [] if s["name"] == sn]
                sp = sum(1 for s in ss if s.get("failed") == 0)
                cp = sum((s.get("changed") or {}).get("passed", 0) for s in ss)
                ct = sum((s.get("changed") or {}).get("total", 0) for s in ss)
                up = sum((s.get("unchanged") or {}).get("passed", 0) for s in ss)
                ut = sum((s.get("unchanged") or {}).get("total", 0) for s in ss)
                dirty = sum(1 for s in ss if s.get("uncommitted_at_end"))
                print(f"| {sha} | {model} | {cond} | {sn} | {sp}/{len(ss)} | "
                      f"{f'{cp}/{ct}' if ct else '—'} | {f'{up}/{ut}' if ut else '—'} "
                      f"| {dirty} |")
    return 0


def _resolve_claude_cli(exe: str) -> str:
    """On Windows, npm installs `claude` as a .CMD shim around a real .exe;
    running the shim via subprocess routes through cmd.exe, whose argument
    quoting mangles flags containing `(`, `)`, `*` (e.g. `Bash(git:*)`,
    `--permission-mode acceptEdits`). Resolve to the underlying binary."""
    p = Path(exe)
    if p.suffix.lower() in (".cmd", ".bat"):
        real = (p.parent / "node_modules" / "@anthropic-ai" / "claude-code"
                / "bin" / "claude.exe")
        if real.is_file():
            return str(real)
    return exe


def cmd_eval(args) -> int:
    """Stage 1 (default): assert a fixture against an existing domain's state.
    Stage 2 (--run): seed an isolated workspace, run a fresh headless agent on
    the fixture's prompt — or, for a longitudinal fixture (`sessions:`), a
    chain of fresh agents against the same workspace, assertions checked after
    each session. See evals/README.md."""
    root = Path(args.path).resolve()
    if args.report:
        return eval_report(root)
    if not args.fixture:
        sys.exit("mdllm: eval requires --fixture (or --report)")
    fixture_path = Path(args.fixture).resolve()
    try:
        fixture_bytes = fixture_path.read_bytes()
    except OSError as exc:
        sys.exit(f"mdllm: eval cannot read fixture {fixture_path} — {exc}")
    fixture_hash = hashlib.sha256(fixture_bytes).hexdigest()
    try:
        fixture = load_yaml_mapping(fixture_bytes, source=fixture_path)
    except (UnicodeError, yaml.YAMLError) as exc:
        sys.exit(f"mdllm: eval refused invalid fixture {fixture_path} — {exc}")
    sentinel = root / ".markdownllm"
    sentinel_data = None
    if sentinel.is_file():
        # Fixtures must not hardcode the framework version (it breaks on the
        # next release) — `{framework_version}` resolves from the sentinel.
        try:
            sentinel_data = load_version_sentinel(
                sentinel.read_text(encoding="utf-8"), source=sentinel)
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            sys.exit(f"mdllm: eval refused invalid/unreadable {sentinel} — {exc}")
        fv = str(sentinel_data.get("version"))

        def _subst(o):
            if isinstance(o, str):
                return o.replace("{framework_version}", fv)
            if isinstance(o, list):
                return [_subst(x) for x in o]
            if isinstance(o, dict):
                return {k: _subst(v) for k, v in o.items()}
            return o
        fixture = _subst(fixture)
    name = fixture.get("name", args.fixture)
    framework_commit = _git_value(root, "rev-parse", "HEAD")
    framework_version = None
    if sentinel_data is not None:
        framework_version = str(sentinel_data.get("version") or "") or None

    # A longitudinal fixture declares `sessions:` — a list of {name, prompt,
    # assertions} — instead of one top-level prompt/assertions pair. Each
    # session is a FRESH headless agent (`claude -p`, no conversation memory)
    # against the SAME workspace, so the only carrier between sessions is
    # committed state: exactly the drift-resistance property under test.
    sessions = fixture.get("sessions")
    if sessions:
        for i, s in enumerate(sessions, 1):
            if "prompt" not in s:
                sys.exit(f"mdllm: sessions[{i}] missing `prompt`")

    if not args.run:
        print(f"## Eval: {name} — {root}\n")
        target = fixture
        if sessions:
            # Against an existing domain, the end-state contract is the final
            # session's assertions — earlier sessions describe intermediate
            # states that no longer exist.
            last = sessions[-1]
            print(f"(longitudinal fixture — checking final session "
                  f"'{last.get('name', len(sessions))}' assertions)\n")
            target = {"assertions": last.get("assertions")}
            if fixture.get("domain_dir"):
                target["domain_dir"] = fixture["domain_dir"]
        passed, failed, lines = check_assertions(target, root)
        print("\n".join(lines))
        print(f"\n{passed} passed, {failed} failed")
        return 1 if failed else 0

    # ---- Stage 2: agent-in-the-loop -------------------------------------
    if "seed" not in fixture or not (sessions or "prompt" in fixture):
        sys.exit("mdllm: --run requires `seed` and `prompt` (or `sessions`) "
                 "in the fixture")
    if not sessions:
        sessions = [{"name": "main", "prompt": fixture["prompt"],
                     "assertions": fixture.get("assertions")}]
    bare_preamble = fixture.get("bare_preamble",
                                "You are in a directory of markdown files with YAML "
                                "frontmatter representing business records.")
    condition = args.condition or ("bare" if getattr(args, "bare", False) else "framework")
    if condition not in CONDITIONS:
        sys.exit(f"mdllm: unknown condition {condition!r}")
    is_bare = condition != "framework"
    if condition == "bare-coached":
        coached = fixture.get("coached_preamble")
        if not coached:
            sys.exit("mdllm: --condition bare-coached needs `coached_preamble` in "
                     "the fixture (the seed's domain guidance as plain prompt text)")
        bare_preamble = coached
    results = []
    claude_exe: str | None = None
    harness_build = "not executed (dry run)"
    if not args.dry_run:
        import shutil as _sh
        exe = _sh.which("claude")
        if not exe:
            sys.exit("mdllm: `claude` CLI not on PATH — install "
                     "@anthropic-ai/claude-code or use --dry-run")
        claude_exe = _resolve_claude_cli(exe)
        harness_build = _command_version(claude_exe)

    def record(run_id: str, run_dir: Path, res: dict) -> None:
        """Run dirs are gitignored workspaces; evals/results/ is the committed
        evidence mirror — the claim and the data travel together."""
        results.append(res)
        payload = json.dumps(res, indent=2)
        (run_dir / "result.json").write_text(payload, encoding="utf-8")
        res_dir = root / "evals" / "results"
        res_dir.mkdir(parents=True, exist_ok=True)
        (res_dir / f"{run_id}.json").write_text(payload, encoding="utf-8")

    # The seed is the one input every trial shares.  An agent granted
    # --add-dir <framework> can reach it and Bash(git:*) can commit the
    # reach; workspace isolation moved the *copy* out of the repo but did
    # not withdraw that grant, because the framework condition is defined
    # by it.  So the seed is watched rather than walled
    # (isolation-must-contain-writes-not-just-reads).
    seed_dir = (root / fixture["seed"]) if fixture.get("seed") else None
    seed_before = (_seed_fingerprint(seed_dir)
                   if seed_dir and seed_dir.is_dir() else None)

    # The framework arm is granted a pruned VIEW of the checkout, never the
    # root: the root holds evals/ (expected figures, generators) — the answer
    # key. The view is fingerprinted like the seed and checked after every
    # trial, because --add-dir plus Bash(git:*) can write into it.
    framework_view: Path | None = None
    view_before: str | None = None
    if not is_bare and not args.dry_run:
        try:
            run_root = _eval_run_dir(root, "x").parent
        except ValueError as exc:
            sys.exit(f"mdllm: {exc}")
        run_root.mkdir(parents=True, exist_ok=True)
        framework_view = build_framework_view(root, run_root)
        view_before = _tree_fingerprint(framework_view)

    condition_tag = {"framework": "fw", "bare": "bare", "bare-coached": "coached"}[condition]
    for trial in range(1, args.trials + 1):
        run_id = _run_id(args.model, condition_tag, trial)
        # Isolation means outside the source repository, not merely under an
        # ignored folder.  The 2026-07 longitudinal run proved that an agent in
        # evals/runs can walk upward and edit the canonical seed.  Operators may
        # pin a sandbox root; the OS temp directory is the default.
        try:
            run_dir = _eval_run_dir(root, run_id)
        except ValueError as exc:
            sys.exit(f"mdllm: {exc}")
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        seed_run_dir(root, fixture, run_dir, is_bare, framework_view)
        print(f"## Trial {trial}/{args.trials} — {run_id}"
              + (f" ({len(sessions)} sessions)" if len(sessions) > 1 else ""))
        t_passed = t_failed = 0
        sess_records: list[dict] = []
        aborted = False
        abort_reason: str | None = None
        voided: str | None = None
        models_observed: set[str] = set()
        for si, sess in enumerate(sessions, 1):
            sname = str(sess.get("name", f"s{si}"))
            prompt = sess["prompt"]
            if is_bare:
                prompt = bare_preamble + "\n\n" + prompt
            # Per-session assertion view; file/git assertions stay
            # workspace-relative via the fixture's domain_dir, same as Stage 1.
            sfx = {"assertions": sess.get("assertions") or []}
            if fixture.get("domain_dir"):
                sfx["domain_dir"] = fixture["domain_dir"]
            cmd = ["claude", "-p", prompt, "--model", args.model,
                   "--output-format", "json", "--permission-mode", "acceptEdits",
                   "--allowedTools", fixture.get("allowed_tools",
                                                 "Edit Write Read Glob Grep Bash(git:*)")]
            if not is_bare:
                # The framework condition is defined by this grant; the bare
                # conditions must NOT see it — that's the control.
                cmd += ["--add-dir", str(framework_view or "<framework-view>")]
            if args.dry_run:
                print(f"  [{sname}] workspace: {run_dir}")
                print(f"  [{sname}] would run (cwd=workspace): {' '.join(cmd[:2])} "
                      f"<prompt {len(prompt)} chars> {' '.join(cmd[3:])}")
                continue
            if si > 1:
                # Sessions share one working tree; without this, uncommitted
                # edits carry as well as committed ones and the "committed
                # state is the only carrier" claim is untested.
                _reset_to_committed(run_dir)
            assert claude_exe is not None
            cmd[0] = claude_exe
            t0 = dt.datetime.now()
            try:
                proc = subprocess.run(cmd, cwd=run_dir, capture_output=True, text=True,
                                      timeout=args.timeout, encoding="utf-8")
            except subprocess.TimeoutExpired:
                wall = (dt.datetime.now() - t0).total_seconds()
                n_asserts = len(sess.get("assertions") or [])
                validation_root = ((run_dir / fixture["domain_dir"])
                                   if fixture.get("domain_dir") else run_dir)
                validation_summary = _validation_summary(validation_root)
                # Downstream sessions depend on this one's end state — the
                # chain is unresumable, so their assertions fail with it.
                rest = sum(len(s.get("assertions") or []) for s in sessions[si:])
                print(f"  [{sname}] TIMEOUT after {wall:.0f}s — session 0/{n_asserts}"
                      + (f", chain aborted ({rest} downstream assertions failed)"
                         if rest else ""))
                sess_records.append({"name": sname, "passed": 0,
                                     "failed": n_asserts + 1,
                                     "wall_s": round(wall), "cost_usd": None,
                                     "turns": None, "timeout": True,
                                     "process_returncode": None,
                                     "agent_failure": "timeout",
                                     "validation_errors":
                                         validation_summary["errors"],
                                     "validation_summary": validation_summary,
                                     "assertion_result": {
                                         "passed": 0,
                                         "failed": n_asserts,
                                         "not_run_downstream": rest,
                                     }})
                t_failed += n_asserts + rest + 1
                aborted = True
                abort_reason = "timeout"
                break
            wall = (dt.datetime.now() - t0).total_seconds()
            # Always persist the agent's raw output — a 2-second 1-turn
            # "trial" is indistinguishable from a real one without it.
            suffix = "" if len(sessions) == 1 else f"-{si}-{sname}"
            (run_dir / f"agent-stdout{suffix}.json").write_text(
                proc.stdout or "", encoding="utf-8")
            if proc.stderr:
                (run_dir / f"agent-stderr{suffix}.txt").write_text(
                    proc.stderr, encoding="utf-8")
            cost = turns = None
            meta = None
            try:
                meta = json.loads(proc.stdout)
                if isinstance(meta, dict):
                    cost = meta.get("total_cost_usd")
                    turns = meta.get("num_turns")
                    usage = meta.get("modelUsage")
                    if isinstance(usage, dict):
                        models_observed.update(str(k) for k in usage)
            except (ValueError, TypeError):
                meta = None
            agent_failure = _agent_failure(proc, meta)
            if agent_failure:
                print(f"  [{sname}] AGENT FAILURE: {agent_failure}")
            key_hits = _answer_key_hits((proc.stdout or "") + (proc.stderr or ""))
            if key_hits and not voided:
                voided = f"answer-key reference in session {sname}: {key_hits}"
                print(f"  [{sname}] VOIDED — {voided}")
            uncommitted = _git_dirty(run_dir)
            records = check_assertions_detailed(sfx, run_dir)
            passed = sum(1 for r in records if r["passed"])
            failed = len(records) - passed
            lines = [r["line"] for r in records]
            failures = [r["label"] for r in records if not r["passed"]]
            changed = {"passed": sum(1 for r in records if r["changed"] is True and r["passed"]),
                       "total": sum(1 for r in records if r["changed"] is True)}
            unchanged = {"passed": sum(1 for r in records if r["changed"] is False and r["passed"]),
                         "total": sum(1 for r in records if r["changed"] is False)}
            assertion_result = {"passed": passed, "failed": failed}
            validation_root = ((run_dir / fixture["domain_dir"])
                               if fixture.get("domain_dir") else run_dir)
            validation_summary = _validation_summary(validation_root)
            if _validation_control_failure(
                    sfx.get("assertions") or [], validation_summary):
                failed += 1
                lines.append(
                    "  FAIL  complete validation boundary: "
                    f"{validation_summary['errors']} Error(s)")
            if agent_failure:
                failed += 1  # control failure is separate from state assertions
                lines.insert(0, f"  FAIL  agent invocation: {agent_failure}")
            if len(sessions) > 1:
                print(f"  --- session {si}/{len(sessions)}: {sname} ---")
            print("\n".join(lines))
            print(f"  [{sname}] {passed}/{passed + failed}"
                  + (f" · changed {changed['passed']}/{changed['total']}" if changed["total"] else "")
                  + f" · {wall:.0f}s · cost {cost} · turns {turns}"
                  + (" · LEFT UNCOMMITTED" if uncommitted else ""))
            t_passed += passed
            t_failed += failed
            sess_records.append({"name": sname, "passed": passed, "failed": failed,
                                 "wall_s": round(wall), "cost_usd": cost,
                                 "turns": turns,
                                 "process_returncode": proc.returncode,
                                 "agent_failure": agent_failure,
                                 "validation_errors":
                                     validation_summary["errors"],
                                 "validation_summary": validation_summary,
                                 "assertion_result": assertion_result,
                                 "failures": failures,
                                 "changed": changed, "unchanged": unchanged,
                                 "uncommitted_at_end": uncommitted,
                                 "answer_key_hits": key_hits})
            if agent_failure:
                # Later sessions depend on a trustworthy state transition.  Do
                # not convert a failed invocation into a longitudinal success.
                rest = sum(len(s.get("assertions") or [])
                           for s in sessions[si:])
                t_failed += rest
                aborted = True
                abort_reason = agent_failure
                break
        if args.dry_run:
            continue
        seed_mutated = False
        if seed_before is not None:
            seed_after = _seed_fingerprint(seed_dir)
            seed_mutated = seed_after != seed_before
        view_mutated = False
        if framework_view is not None and view_before is not None:
            view_mutated = _tree_fingerprint(framework_view) != view_before
            if view_mutated and not voided:
                voided = "framework view mutated during the trial"
        if voided:
            t_failed += 1
        walls = [s["wall_s"] for s in sess_records if s.get("wall_s") is not None]
        costs = [s["cost_usd"] for s in sess_records if s.get("cost_usd") is not None]
        turns_ = [s["turns"] for s in sess_records if s.get("turns") is not None]
        res = {"run_id": run_id, "fixture": name, "model": args.model,
               "models_observed": sorted(models_observed),
               "condition": condition,
               "passed": t_passed, "failed": t_failed,
               "voided": voided,
               "seed_sha256": seed_before,
               "seed_mutated": seed_mutated,
               "framework_view": (str(framework_view) if framework_view else None),
               "framework_view_sha256": view_before,
               "framework_view_mutated": view_mutated,
               "framework_root_granted": False,
               "wall_s": sum(walls) if walls else None,
               "cost_usd": round(sum(costs), 6) if costs else None,
               "turns": sum(turns_) if turns_ else None,
               "framework_commit": framework_commit,
               "framework_version": framework_version,
               "fixture_sha256": fixture_hash,
               "fixture_path": fixture_path.name,
               "execution_surface": "claude-cli",
               "harness": "Claude Code CLI",
               "harness_build": harness_build,
               "tool_version": framework_version,
               "reasoning_effort": "CLI default (not explicitly configured)",
               "reasoning_effort_requested": fixture.get("reasoning_effort"),
               "process_status": [s.get("process_returncode")
                                  for s in sess_records],
               "validation_errors": sum(s.get("validation_errors", 0)
                                        for s in sess_records),
               "validation_summary": {
                   key: sum((s.get("validation_summary") or {}).get(key, 0)
                            for s in sess_records)
                   for key in ("errors", "warnings", "info")
               },
               "assertion_result": {
                   "passed": sum((s.get("assertion_result") or {}).get(
                       "passed", 0) for s in sess_records),
                   "failed": sum((s.get("assertion_result") or {}).get(
                       "failed", 0) for s in sess_records),
                   "not_run_downstream": sum(
                       (s.get("assertion_result") or {}).get(
                           "not_run_downstream", 0) for s in sess_records),
               }}
        if len(sessions) > 1:
            res["sessions"] = sess_records
        if aborted:
            res["aborted"] = True
            res["abort_reason"] = abort_reason
            if abort_reason == "timeout":
                res["timeout"] = True
        print(f"  trial score {t_passed}/{t_passed + t_failed}"
              + (f" — VOIDED: {voided}" if voided else "") + "\n")
        record(run_id, run_dir, res)
        if view_mutated:
            print(f"!!! FRAMEWORK VIEW MUTATED during {run_id} — {framework_view}")
            print("    The framework arm's granted directory changed under the trial;"
                  " later trials would be seeded from a moved operating layer. Stopping.")
            return 1
        if seed_mutated:
            # In 2026-07 this went undetected and every subsequent trial
            # was seeded from the perturbed inputs, voiding a whole arm.
            # Refuse to seed another trial from bytes an agent moved.
            print(f"!!! SEED MUTATED during {run_id} — {seed_dir}")
            print("    This trial's inputs are no longer the inputs it "
                  "was seeded from, and every later trial would inherit "
                  "the change. Results from this trial on are not "
                  "comparable with the arm.")
            print("    Restore the seed (`git -C <framework> checkout -- "
                  f"{fixture['seed']}`), confirm it is clean, then re-run.")
            return 1
    if results:
        ok = sum(1 for r in results if r["failed"] == 0 and not r.get("voided"))
        nv = sum(1 for r in results if r.get("voided"))
        print(f"### {name}: {ok}/{len(results)} trials fully passing "
              f"({args.model}, {condition})" + (f", {nv} voided" if nv else ""))
    return _results_exit_code(results)
