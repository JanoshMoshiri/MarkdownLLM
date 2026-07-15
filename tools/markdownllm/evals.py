"""The eval harness — golden-scenario fixtures against domain state.

Stage 1: deterministic assertions against an existing corpus. Stage 2
(--run): seed an isolated workspace and drive fresh headless agents (single
prompt or a longitudinal `sessions:` chain), asserting after each session.
evals/results/ is the committed evidence mirror.
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

import yaml

from .model import Corpus, SEV_ERROR, scan
from .validation import validate_level1, validate_level2, validate_level3

def check_assertions(fixture: dict, domain_root: Path) -> tuple[int, int, list[str]]:
    """Stage 1: deterministic assertions against a domain's current state.

    `domain_root` is the workspace; if the fixture declares `domain_dir`
    (scaffold-style fixtures, where the agent *creates* the domain in a
    subfolder), thing/status/field/link/validates assertions scan that
    subfolder while file/git assertions stay workspace-relative."""
    ws = domain_root
    droot = (ws / fixture["domain_dir"]) if fixture.get("domain_dir") else ws
    corpus, _ = scan(droot) if droot.is_dir() else (Corpus(root=droot), [])
    by_id = corpus.by_id()
    passed = failed = 0
    lines: list[str] = []

    def report(ok: bool, label: str):
        nonlocal passed, failed
        passed, failed = passed + ok, failed + (not ok)
        lines.append(f"  {'PASS' if ok else 'FAIL'}  {label}")

    for a in fixture.get("assertions") or []:
        if "thing_exists" in a:
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
            ok = actual == expected
            if not ok and isinstance(expected, (int, float)) and not isinstance(expected, bool):
                # `2500.00` written as the string "2500.00" is semantically
                # correct — coerce before failing a numeric contract.
                try:
                    ok = abs(float(actual) - float(expected)) < 1e-9
                except (TypeError, ValueError):
                    ok = False
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
            findings = []
            for t in corpus.things:
                findings.extend(validate_level1(t, corpus.schema))
            findings.extend(validate_level2(corpus))
            findings.extend(validate_level3(corpus))
            errs = [x for x in findings if x.severity == SEV_ERROR]
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
    return passed, failed, lines


def seed_run_dir(root: Path, fixture: dict, run_dir: Path, bare: bool) -> None:
    """Stage 2 workspace: copy the seed into an isolated git repo."""
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
    cells: dict[tuple[str, str, str], list[dict]] = {}
    for r in results:
        # Legacy runs predate the fixture tag (the 2026-06-11 2x2 was all one
        # fixture); group them under their known name rather than "?".
        fx = str(r.get("fixture", "VAT quarter prep (synthetic, known-correct figures)"))
        cells.setdefault((fx, str(r.get("model")), str(r.get("condition"))), []).append(r)
    print(f"## Eval Report — {len(results)} trials, {len(cells)} cells\n")
    print("| fixture | model | condition | trials | fully passing | assertion pass rate "
          "| mean wall s | mean cost $ |")
    print("|---|---|---|---|---|---|---|---|")
    for (fx, model, cond), rs in sorted(cells.items()):
        full = sum(1 for r in rs if r.get("failed") == 0)
        p = sum(r.get("passed", 0) for r in rs)
        f_ = sum(r.get("failed", 0) for r in rs)
        rate = f"{p}/{p + f_} ({p / (p + f_):.0%})" if p + f_ else "—"
        walls = [r["wall_s"] for r in rs if r.get("wall_s") is not None]
        costs = [r["cost_usd"] for r in rs if r.get("cost_usd") is not None]
        mw = f"{sum(walls) / len(walls):.0f}" if walls else "—"
        mc = f"{sum(costs) / len(costs):.3f}" if costs else "—"
        fx_short = fx if len(fx) <= 40 else fx[:37] + "..."
        print(f"| {fx_short} | {model} | {cond} | {len(rs)} | {full}/{len(rs)} | {rate} "
              f"| {mw} | {mc} |")
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
    fixture = yaml.safe_load(Path(args.fixture).read_text(encoding="utf-8"))
    sentinel = root / ".markdownllm"
    if sentinel.is_file():
        # Fixtures must not hardcode the framework version (it breaks on the
        # next release) — `{framework_version}` resolves from the sentinel.
        fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {})
                 .get("version"))

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
    import json as _json
    results = []

    def record(run_id: str, run_dir: Path, res: dict) -> None:
        """Run dirs are gitignored workspaces; evals/results/ is the committed
        evidence mirror — the claim and the data travel together."""
        results.append(res)
        payload = _json.dumps(res, indent=2)
        (run_dir / "result.json").write_text(payload, encoding="utf-8")
        res_dir = root / "evals" / "results"
        res_dir.mkdir(parents=True, exist_ok=True)
        (res_dir / f"{run_id}.json").write_text(payload, encoding="utf-8")

    for trial in range(1, args.trials + 1):
        run_id = (f"{dt.datetime.now():%Y%m%d-%H%M%S}-"
                  f"{args.model}-{'bare' if args.bare else 'fw'}-t{trial}")
        run_dir = root / "evals" / "runs" / run_id
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        seed_run_dir(root, fixture, run_dir, args.bare)
        print(f"## Trial {trial}/{args.trials} — {run_id}"
              + (f" ({len(sessions)} sessions)" if len(sessions) > 1 else ""))
        t_passed = t_failed = 0
        sess_records: list[dict] = []
        aborted = False
        for si, sess in enumerate(sessions, 1):
            sname = str(sess.get("name", f"s{si}"))
            prompt = sess["prompt"]
            if args.bare:
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
            if not args.bare:
                # The seed's framework_root resolves to the framework checkout;
                # the bare condition must NOT see it — that's the control.
                cmd += ["--add-dir", str(root)]
            if args.dry_run:
                print(f"  [{sname}] workspace: {run_dir}")
                print(f"  [{sname}] would run (cwd=workspace): {' '.join(cmd[:2])} "
                      f"<prompt {len(prompt)} chars> {' '.join(cmd[3:])}")
                continue
            import shutil as _sh
            exe = _sh.which("claude")
            if not exe:
                sys.exit("mdllm: `claude` CLI not on PATH — install "
                         "@anthropic-ai/claude-code or use --dry-run")
            cmd[0] = _resolve_claude_cli(exe)
            t0 = dt.datetime.now()
            try:
                proc = subprocess.run(cmd, cwd=run_dir, capture_output=True, text=True,
                                      timeout=args.timeout, encoding="utf-8")
            except subprocess.TimeoutExpired:
                wall = (dt.datetime.now() - t0).total_seconds()
                n_asserts = len(sess.get("assertions") or [])
                # Downstream sessions depend on this one's end state — the
                # chain is unresumable, so their assertions fail with it.
                rest = sum(len(s.get("assertions") or []) for s in sessions[si:])
                print(f"  [{sname}] TIMEOUT after {wall:.0f}s — session 0/{n_asserts}"
                      + (f", chain aborted ({rest} downstream assertions failed)"
                         if rest else ""))
                sess_records.append({"name": sname, "passed": 0, "failed": n_asserts,
                                     "wall_s": round(wall), "cost_usd": None,
                                     "turns": None, "timeout": True})
                t_failed += n_asserts + rest
                aborted = True
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
            try:
                meta = _json.loads(proc.stdout)
                cost, turns = meta.get("total_cost_usd"), meta.get("num_turns")
                if meta.get("is_error") or meta.get("subtype") not in (None, "success"):
                    print(f"  [{sname}] AGENT ERROR ({meta.get('subtype')}): "
                          f"{str(meta.get('result'))[:200]}")
            except (ValueError, TypeError):
                pass
            passed, failed, lines = check_assertions(sfx, run_dir)
            if len(sessions) > 1:
                print(f"  --- session {si}/{len(sessions)}: {sname} ---")
            print("\n".join(lines))
            print(f"  [{sname}] {passed}/{passed + failed} · {wall:.0f}s "
                  f"· cost {cost} · turns {turns}")
            t_passed += passed
            t_failed += failed
            sess_records.append({"name": sname, "passed": passed, "failed": failed,
                                 "wall_s": round(wall), "cost_usd": cost,
                                 "turns": turns})
        if args.dry_run:
            continue
        walls = [s["wall_s"] for s in sess_records if s.get("wall_s") is not None]
        costs = [s["cost_usd"] for s in sess_records if s.get("cost_usd") is not None]
        turns_ = [s["turns"] for s in sess_records if s.get("turns") is not None]
        res = {"run_id": run_id, "fixture": name, "model": args.model,
               "condition": "bare" if args.bare else "framework",
               "passed": t_passed, "failed": t_failed,
               "wall_s": sum(walls) if walls else None,
               "cost_usd": round(sum(costs), 6) if costs else None,
               "turns": sum(turns_) if turns_ else None}
        if len(sessions) > 1:
            res["sessions"] = sess_records
        if aborted:
            res["timeout"] = True
        print(f"  trial score {t_passed}/{t_passed + t_failed}\n")
        record(run_id, run_dir, res)
    if results:
        ok = sum(1 for r in results if r["failed"] == 0)
        print(f"### {name}: {ok}/{len(results)} trials fully passing "
              f"({args.model}, {'bare' if args.bare else 'framework'})")
    return 0
