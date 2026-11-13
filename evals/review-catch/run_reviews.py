"""Run one arm of the review-catch eval for one trial.

Each review gets a fresh, bare work folder outside the repository holding only
the `tools/` tree at the entry's commit, `CHANGE.diff`, and (``-message`` arms
only) `COMMIT_MESSAGE.txt`. The reviewer never sees the set file, the entry
kind, the defects, the fix commits, or later history. See README.md.

Standard library only. Helpers mirrored from tools/markdownllm/evals.py are
copied, not imported, because that module imports PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

ARMS = ("claude-blind", "codex-blind", "claude-message", "codex-message")
PROMPTS = {"blind": HERE / "prompt-blind.md", "message": HERE / "prompt-message.md"}
MAX_FINDINGS = 5
VOID_STREAK_STOP = 2
RAW_CHARS = 20000
CLAUDE_TOOLS = "Read,Glob,Grep"


def arm_parts(arm: str) -> tuple[str, str]:
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}; one of {', '.join(ARMS)}")
    vendor, variant = arm.split("-", 1)
    return vendor, variant


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_bytes(path: Path) -> bytes:
    """File bytes with CRLF converted to LF: a checkout may convert line endings,
    so prompts and the set are sent and hashed as LF bytes."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def decode(data: bytes | None) -> str:
    return (data or b"").decode("utf-8", errors="replace")


def git(*args: str, repo: Path = REPO) -> bytes:
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {decode(proc.stderr).strip()}")
    return proc.stdout


# ---------------------------------------------------------------- work folder

def _rmtree(path: Path) -> None:
    def onerror(func, p, _exc):
        try:
            os.chmod(p, 0o700)
            func(p)
        except OSError:
            pass
    if path.exists():
        shutil.rmtree(path, onerror=onerror)


def work_base(arm: str, trial: int, root: Path | None = None) -> Path:
    base = Path(root) if root else Path(tempfile.gettempdir()) / "mdllm-review-catch"
    return (base / f"{arm}-t{trial}").resolve()


def build_work_folder(entry: dict, variant: str, folder: Path, repo: Path = REPO) -> Path:
    """Fresh folder: tools/ at the commit, CHANGE.diff, COMMIT_MESSAGE.txt (message arms)."""
    commit = entry["commit"]
    try:
        folder.resolve().relative_to(repo.resolve())
    except ValueError:
        pass
    else:
        raise ValueError("work folder must be outside the repository")
    _rmtree(folder)
    folder.mkdir(parents=True)
    tar_bytes = git("archive", "--format=tar", commit, "tools", repo=repo)
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tf:
        tf.extractall(folder, filter="data")
    diff = git("diff", "--no-color", "--no-ext-diff", f"{commit}^", commit, "--", "tools", repo=repo)
    (folder / "CHANGE.diff").write_bytes(diff)
    if variant == "message":
        msg = git("log", "-1", "--format=%B", commit, repo=repo)
        (folder / "COMMIT_MESSAGE.txt").write_bytes(msg)
    return folder


def _sha_patterns(shas: list[str]) -> list[re.Pattern]:
    pats = []
    for s in shas:
        s = (s or "").lower()
        if len(s) >= 7:
            pats.append(re.compile(rb"(?<![0-9a-fA-F])" + re.escape(s[:7].encode())
                                   + rb"[0-9a-fA-F]{0,33}(?![0-9a-fA-F])", re.I))
    return pats


def assert_no_leak(folder: Path, variant: str, entry: dict, set_data: dict) -> None:
    """Refuse to launch unless the folder holds exactly the allowed inputs and
    no entry id, kind, commit/fix/repo-head sha appears in any of its files."""
    allowed = {"tools", "CHANGE.diff"} | ({"COMMIT_MESSAGE.txt"} if variant == "message" else set())
    names = {p.name for p in folder.iterdir()}
    problems = []
    if names != allowed:
        problems.append(f"top level is {sorted(names)}, expected {sorted(allowed)}")
    shas = [entry["commit"], set_data.get("repo_head", "")]
    shas += [d.get("fix", "") for d in entry.get("defects", [])]
    sha_pats = _sha_patterns(shas)
    id_pats = [re.compile(rb"(?<![A-Za-z0-9_])" + re.escape(str(e["id"]).encode()) + rb"(?![A-Za-z0-9_])")
               for e in set_data.get("entries", [])]
    for p in folder.rglob("*"):
        rel = p.relative_to(folder).as_posix()
        if p.name == ".git" or p.name.lower() in ("set.json", "candidates.json", "candidates.md"):
            problems.append(f"forbidden path {rel}")
            continue
        if not p.is_file():
            continue
        data = p.read_bytes()
        for pat in sha_pats:
            m = pat.search(data)
            if m:
                problems.append(f"{rel}: commit/fix/head sha prefix {m.group(0)[:12].decode()}")
        for pat in id_pats:
            m = pat.search(data)
            if m:
                problems.append(f"{rel}: entry id {m.group(0).decode()}")
    if problems:
        raise AssertionError("leak check failed:\n  " + "\n  ".join(problems[:20]))


# ---------------------------------------------------------------- executables

def resolve_claude(exe: str) -> str:
    """Mirror of evals._resolve_claude_cli: bypass the npm .cmd shim."""
    p = Path(exe)
    if p.suffix.lower() in (".cmd", ".bat"):
        real = p.parent / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
        if real.is_file():
            return str(real)
    return exe


def resolve_codex(exe: str) -> list[str]:
    """Bypass the npm .cmd shim: run node on the package's codex.js."""
    p = Path(exe)
    if p.suffix.lower() in (".cmd", ".bat"):
        js = p.parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
        node = p.parent / "node.exe"
        node_exe = str(node) if node.is_file() else shutil.which("node")
        if js.is_file() and node_exe:
            return [node_exe, str(js)]
    return [exe]


def find_exe(vendor: str) -> list[str]:
    exe = shutil.which(vendor)
    if not exe:
        sys.exit(f"run_reviews: `{vendor}` is not on PATH")
    return [resolve_claude(exe)] if vendor == "claude" else resolve_codex(exe)


def harness_build(base_cmd: list[str]) -> str:
    try:
        proc = subprocess.run([*base_cmd, "--version"], capture_output=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unknown ({type(exc).__name__})"
    text = (decode(proc.stdout) or decode(proc.stderr)).strip()
    if proc.returncode != 0 or not text:
        return f"unknown (version command exited {proc.returncode})"
    return text.splitlines()[0].strip()


def claude_command(base: list[str], model: str, prompt: str) -> list[str]:
    return [*base, "-p", prompt,
            "--model", model,
            "--output-format", "stream-json", "--verbose",
            "--safe-mode",
            "--restricted",
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--tools", CLAUDE_TOOLS,
            "--allowedTools", CLAUDE_TOOLS,
            "--permission-prompts", "none"]


def codex_command(base: list[str], model: str, folder: Path, last_file: Path) -> list[str]:
    # Prompt arrives on stdin ("-"), so no multi-line argument crosses a shell.
    return [*base, "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox", "read-only",
            "--model", model,
            "--cd", str(folder),
            "--color", "never",
            "--json",
            "--output-last-message", str(last_file),
            "-"]


# ---------------------------------------------------------------- launching

def kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.kill()


def launch(cmd: list[str], cwd: Path, stdin: bytes | None, timeout: int) -> dict:
    t0 = dt.datetime.now(dt.timezone.utc)
    proc = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        out, err = proc.communicate(stdin, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_tree(proc)
        out, err = proc.communicate()
    t1 = dt.datetime.now(dt.timezone.utc)
    return {"stdout": decode(out), "stderr": decode(err), "exit_code": proc.returncode,
            "timed_out": timed_out, "started": t0.isoformat(timespec="seconds"),
            "ended": t1.isoformat(timespec="seconds"),
            "seconds": round((t1 - t0).total_seconds(), 1)}


def _jsonl(text: str) -> list[dict]:
    events = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if isinstance(ev, dict):
            events.append(ev)
    return events


def _outside(raw: str, folder: Path) -> bool:
    p = Path(raw)
    if not p.is_absolute():
        p = folder / p
    try:
        p.resolve().relative_to(folder.resolve())
        return False
    except (ValueError, OSError):
        return True


DOTDOT = re.compile(r"(^|[\\/])\.\.([\\/]|$)")


def _absolute_pattern(pat: str) -> bool:
    p = pat.strip()
    return bool(re.match(r"^[A-Za-z]:[\\/]|^[\\/]|^~", p))


def claude_reach(name: str, inp: dict, folder: Path) -> list[str]:
    """Reaches outside the folder in one Claude tool call. A path (file_path,
    path) resolving outside, or a Glob `pattern` / Grep `glob` that is absolute
    or has a `..` segment. Grep's `pattern` is a content regex, not a path."""
    out = []
    for key in ("file_path", "path", "notebook_path"):
        raw = inp.get(key)
        if raw and (_outside(str(raw), folder) or DOTDOT.search(str(raw))):
            out.append(f"{name} {key}={raw}")
    globs = []
    if name == "Glob" and inp.get("pattern"):
        globs.append(("pattern", str(inp["pattern"])))
    if inp.get("glob"):
        globs.append(("glob", str(inp["glob"])))
    for key, g in globs:
        if _absolute_pattern(g) or DOTDOT.search(g):
            out.append(f"{name} {key}={g}")
    return out


# A shell wrapper Codex puts around the real command (e.g. an absolute path to
# pwsh.exe followed by -Command). Unwrapped before the reach check, so the
# wrapper's own absolute path is not read as a reach.
_SHELL = r"(?:pwsh|powershell|cmd|bash|sh|zsh)(?:\.exe)?"
SHELL_WRAP = re.compile(
    r"""^\s*(?:"(?:[^"]*[\\/])?""" + _SHELL + r'''"|'(?:[^']*[\\/])?''' + _SHELL
    + r"""'|(?:[^"'\s]*[\\/])?""" + _SHELL + r""")\s+"""
    r"""(?:-(?:NoProfile|NoLogo|NonInteractive)\s+|-(?:ExecutionPolicy|WindowStyle)\s+\S+\s+)*"""
    r"""(?:-Command|-c|-lc|/c|/C)\s+""", re.I)
TOKEN = re.compile(r'"([^"]*)"|\'([^\']*)\'|(\S+)')
GIT_CALL = re.compile(
    r"""(?:^|[;&|(\n{]|\b(?:xargs|iex|Invoke-Expression|Start-Process|exec|env|call)\s+)"""
    r"""\s*["']?(?:[^"'\s;&|]*[\\/])?git(?:\.exe)?(?=["'\s;&|)]|$)""", re.I)


def _unwrap(command) -> str:
    if isinstance(command, list):
        parts = [str(c) for c in command]
        if parts and re.search(r"(?:^|[\\/])(?:pwsh|powershell|cmd|bash|sh|zsh)(?:\.exe)?$",
                               parts[0], re.I) and len(parts) >= 2:
            return parts[-1]
        return " ".join(parts)
    text = str(command)
    m = SHELL_WRAP.match(text)
    if m:
        text = text[m.end():].strip()
        if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
            text = text[1:-1]
    return text


def _norm(p: str) -> str:
    p = p.replace("\\", "/").rstrip("/").lower()
    m = re.match(r"^/([a-z])(/|$)", p)
    if m:  # /c/Users/... -> c:/Users/...
        p = f"{m.group(1)}:/" + p[3:]
    return p


def codex_reach(command, folder: Path) -> list[str]:
    """Why one Codex shell command reaches outside the folder (empty if it does not).
    Conservative: when unsure, flag."""
    text = _unwrap(command)
    base = _norm(str(folder.resolve()))
    under = lambda p: _norm(p) == base or _norm(p).startswith(base + "/")
    reasons = []
    if GIT_CALL.search(text):
        reasons.append("invokes git")
    for m in re.finditer(r"\$HOME\b|\$\{HOME\}|%USERPROFILE%|%HOMEPATH%|\$env:", text, re.I):
        reasons.append(f"home/env reference {m.group(0)}")
    for t in TOKEN.finditer(text):
        tok = next(g for g in t.groups() if g is not None)
        tok = tok.strip().rstrip(";,)|&")
        if not tok:
            continue
        if tok.startswith("~"):
            reasons.append(f"home path {tok}")
        if DOTDOT.search(tok):
            reasons.append(f"parent segment in {tok}")
        if tok.startswith("\\\\") or tok.startswith("//"):
            reasons.append(f"UNC path {tok}")
            continue
        for d in re.finditer(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]", tok):
            path = tok[d.start():]
            if not under(path):
                reasons.append(f"absolute path {path}")
        if re.match(r"^/[A-Za-z]", tok) and not under(tok):
            reasons.append(f"absolute path {tok}")
    return reasons


def parse_claude(run: dict, folder: Path) -> dict:
    """stream-json: the `result` event carries the final text, cost and modelUsage."""
    events = _jsonl(run["stdout"])
    result = next((e for e in reversed(events) if e.get("type") == "result"), None)
    tools, outside = [], []
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        for block in (ev.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                inp = block.get("input") or {}
                name = str(block.get("name"))
                tools.append(name)
                outside.extend(claude_reach(name, inp if isinstance(inp, dict) else {}, folder))
    rec = {"final_message": None, "cost_usd": None, "tokens": None, "turns": None,
           "models_observed": [], "agent_error": None, "tool_counts": {}, "outside_reach": outside}
    for t in tools:
        rec["tool_counts"][t] = rec["tool_counts"].get(t, 0) + 1
    if result is None:
        rec["agent_error"] = "no result event"
        return rec
    rec["final_message"] = result.get("result") if isinstance(result.get("result"), str) else None
    rec["cost_usd"] = result.get("total_cost_usd")
    rec["turns"] = result.get("num_turns")
    rec["tokens"] = result.get("usage")
    if isinstance(result.get("modelUsage"), dict):
        rec["models_observed"] = sorted(str(k) for k in result["modelUsage"])
    if result.get("is_error") or result.get("subtype") not in (None, "success"):
        rec["agent_error"] = f"is_error={result.get('is_error')} subtype={result.get('subtype')}"
    return rec


def _find_models(obj, found: set) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "model" and isinstance(v, str):
                found.add(v)
            else:
                _find_models(v, found)
    elif isinstance(obj, list):
        for v in obj:
            _find_models(v, found)


def parse_codex(run: dict, folder: Path, last_file: Path) -> dict:
    events = _jsonl(run["stdout"])
    rec = {"final_message": None, "cost_usd": None, "tokens": None, "turns": None,
           "models_observed": [], "agent_error": None, "tool_counts": {}, "commands": [],
           "outside_reach": []}
    tokens: dict = {}
    turns = 0
    last_agent_msg = None
    models: set = set()
    seen_cmds: set = set()
    for ev in events:
        _find_models(ev, models)
        kind = ev.get("type")
        any_item = ev.get("item")
        if isinstance(any_item, dict) and any_item.get("type") == "command_execution" \
                and any_item.get("command"):
            cmd = any_item["command"]
            key = (any_item.get("id"), json.dumps(cmd))
            if key not in seen_cmds:
                seen_cmds.add(key)
                for why in codex_reach(cmd, folder):
                    rec["outside_reach"].append(f"{why} :: {str(cmd)[:200]}")
        if kind == "turn.completed":
            turns += 1
            for k, v in (ev.get("usage") or {}).items():
                if isinstance(v, int):
                    tokens[k] = tokens.get(k, 0) + v
        elif kind in ("turn.failed", "error"):
            rec["agent_error"] = json.dumps(ev)[:500]
        item = ev.get("item") if kind == "item.completed" else None
        if isinstance(item, dict):
            itype = str(item.get("type"))
            rec["tool_counts"][itype] = rec["tool_counts"].get(itype, 0) + 1
            if itype == "agent_message" and isinstance(item.get("text"), str):
                last_agent_msg = item["text"]
            if itype == "command_execution" and item.get("command"):
                rec["commands"].append(str(item["command"])[:300])
    rec["tokens"] = tokens or None
    rec["turns"] = turns or None
    rec["models_observed"] = sorted(models)
    if last_file.is_file():
        rec["final_message"] = decode(last_file.read_bytes())
    if not rec["final_message"]:
        rec["final_message"] = last_agent_msg
    return rec


# ---------------------------------------------------------------- reply parsing

def extract_findings(text: str | None) -> dict:
    """The last JSON object in the reply must be {"findings": [...]}.

    Returns {"ok", "findings" (first five), "offered", "reason", "trailing_text"}.
    """
    out = {"ok": False, "findings": [], "offered": 0, "reason": None, "trailing_text": False}
    if not text or not text.strip():
        out["reason"] = "empty reply"
        return out
    dec = json.JSONDecoder()
    best = None  # (end, -start, obj)
    for m in re.finditer(r"\{", text):
        try:
            obj, end = dec.raw_decode(text, m.start())
        except ValueError:
            continue
        cand = (end, -m.start(), obj)
        if best is None or cand[:2] > best[:2]:
            best = cand
    if best is None:
        out["reason"] = "no JSON object in reply"
        return out
    end, _, obj = best
    tail = text[end:].strip()
    out["trailing_text"] = bool(tail.strip("`").strip())
    if not isinstance(obj, dict) or not isinstance(obj.get("findings"), list):
        out["reason"] = "last JSON object is not {\"findings\": [...]}"
        return out
    findings = obj["findings"]
    out["offered"] = len(findings)
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            out["reason"] = f"finding {i} is not an object"
            return out
        if not isinstance(f.get("file"), str) or not f["file"].strip():
            out["reason"] = f"finding {i} lacks a file"
            return out
        for k in ("line_start", "line_end"):
            if not isinstance(f.get(k), int) or isinstance(f.get(k), bool):
                out["reason"] = f"finding {i} {k} is not an integer"
                return out
        if not isinstance(f.get("claim"), str) or not f["claim"].strip():
            out["reason"] = f"finding {i} lacks a claim"
            return out
    out["findings"] = [{"file": f["file"], "line_start": f["line_start"], "line_end": f["line_end"],
                        "claim": f["claim"], "confidence": f.get("confidence")}
                       for f in findings[:MAX_FINDINGS]]
    out["ok"] = True
    return out


# ---------------------------------------------------------------- one review

def review_once(vendor: str, base: list[str], model: str, prompt: str, folder: Path,
                out_dir: Path, timeout: int, launcher=launch) -> dict:
    if vendor == "claude":
        cmd = claude_command(base, model, prompt)
        run = launcher(cmd, folder, None, timeout)
        parsed = parse_claude(run, folder)
    else:
        last_file = out_dir / f"{folder.name}.last.txt"
        if last_file.exists():
            last_file.unlink()
        cmd = codex_command(base, model, folder, last_file)
        run = launcher(cmd, folder, prompt.encode("utf-8"), timeout)
        parsed = parse_codex(run, folder, last_file)
        if last_file.exists():
            last_file.unlink()
    ext = extract_findings(parsed.get("final_message"))
    void = None
    reach = parsed.get("outside_reach") or []
    if reach:
        void = "reached outside the work folder"
    elif run["timed_out"]:
        void = f"timeout after {timeout}s"
    elif not ext["ok"]:
        void = (f"exit {run['exit_code']}, no parsable reply: {ext['reason']}"
                if run["exit_code"] != 0 else f"unparsable reply: {ext['reason']}")
    raw = parsed.get("final_message")
    if raw is None and void:
        raw = (run["stdout"][-RAW_CHARS // 2:] + "\n--- stderr ---\n" + run["stderr"][-RAW_CHARS // 2:])
    rec = {"started": run["started"], "ended": run["ended"], "seconds": run["seconds"],
           "exit_code": run["exit_code"], "timed_out": run["timed_out"],
           "cost_usd": parsed.get("cost_usd"), "tokens": parsed.get("tokens"),
           "turns": parsed.get("turns"), "models_observed": parsed.get("models_observed") or [],
           "agent_error": parsed.get("agent_error"), "tool_counts": parsed.get("tool_counts"),
           "findings": ext["findings"] if not void else [], "findings_offered": ext["offered"],
           "trailing_text": ext["trailing_text"],
           "raw_final_message": (raw or "")[:RAW_CHARS],
           "void": bool(void), "void_reason": void, "outside_reach": reach}
    if vendor == "codex":
        rec["commands"] = parsed.get("commands") or []
    return rec


# ---------------------------------------------------------------- the arm

def load_set(path: Path) -> tuple[dict, str]:
    data = lf_bytes(path)
    s = json.loads(decode(data))
    if s.get("schema") != 1 or not isinstance(s.get("entries"), list):
        raise ValueError(f"{path}: not a schema-1 review set")
    return s, sha256_bytes(data)


def ordered_entries(set_data: dict, trial: int, only: list[str] | None) -> list[dict]:
    entries = list(set_data["entries"])
    random.Random(trial).shuffle(entries)
    if only:
        known = {e["id"] for e in entries}
        missing = [x for x in only if x not in known]
        if missing:
            raise ValueError(f"unknown entries: {', '.join(missing)}")
        entries = [e for e in entries if e["id"] in only]
    return entries


def write_result(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def run_arm(args, launcher=launch, base_cmd: list[str] | None = None,
            work_root: Path | None = None, repo: Path = REPO) -> int:
    vendor, variant = arm_parts(args.arm)
    set_path = Path(args.set).resolve()
    set_data, set_sha = load_set(set_path)
    prompt_path = PROMPTS[variant]
    prompt_bytes = lf_bytes(prompt_path)
    prompt = decode(prompt_bytes)
    only = [x.strip() for x in args.entries.split(",") if x.strip()] if args.entries else None
    entries = ordered_entries(set_data, args.trial, only)
    base_dir = work_base(args.arm, args.trial, work_root)
    out_tmp = base_dir.parent / f"{base_dir.name}-out"

    if args.dry_run:
        base = base_cmd or ["claude" if vendor == "claude" else "codex"]
        for e in entries:
            folder = build_work_folder(e, variant, base_dir / e["id"], repo=repo)
            assert_no_leak(folder, variant, e, set_data)
            if vendor == "claude":
                cmd = claude_command(base, args.model, "<PROMPT>")
                stdin_note = ""
            else:
                cmd = codex_command(base, args.model, folder, out_tmp / f"{e['id']}.last.txt")
                stdin_note = f"   < {prompt_path.name}"
            print(f"[{e['id']}] work folder: {folder}  (leak check passed)")
            print(f"[{e['id']}] cwd={folder}")
            print("  " + subprocess.list2cmdline(cmd) + stdin_note
                  + (f"   (<PROMPT> = text of {prompt_path.name})" if vendor == "claude" else ""))
        print(f"dry run: {len(entries)} work folders built, nothing launched")
        return 0

    base = base_cmd or find_exe(vendor)
    build = harness_build(base)
    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = (repo / out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_tmp.mkdir(parents=True, exist_ok=True)
    result_path = out_dir / f"{utc_stamp()}-{args.arm}-t{args.trial}.json"
    payload = {"schema": 1, "arm": args.arm, "vendor": vendor, "model_requested": args.model,
               "models_observed": [], "harness_build": build,
               "prompt_file": prompt_path.name, "prompt_sha256": sha256_bytes(prompt_bytes),
               "set_sha256": set_sha, "hashes_over": "LF-normalised bytes (CRLF -> LF)",
               "repo_head": set_data.get("repo_head"),
               "trial": args.trial, "entries_filter": only, "timeout_s": args.timeout,
               "started": now_iso(), "ended": None, "complete": False, "stopped": None,
               "reviews": [], "totals": {}}

    def totals() -> dict:
        return compute_totals(payload["reviews"])

    def finish(code: int) -> int:
        print_summary(payload, result_path)
        _rmtree(base_dir)
        return code

    streak = 0
    print(f"{args.arm} t{args.trial} [{args.model}] - {len(entries)} reviews -> {result_path}")
    write_result(result_path, payload)
    for e in entries:
        attempts = []
        rec = None
        for attempt in (1, 2):
            folder = build_work_folder(e, variant, base_dir / e["id"], repo=repo)
            assert_no_leak(folder, variant, e, set_data)
            rec = review_once(vendor, base, args.model, prompt, folder, out_tmp, args.timeout, launcher)
            _rmtree(folder)
            if rec["void"]:
                streak += 1
                attempts.append({"void_reason": rec["void_reason"], "exit_code": rec["exit_code"],
                                 "seconds": rec["seconds"], "cost_usd": rec["cost_usd"],
                                 "tokens": rec["tokens"], "outside_reach": rec["outside_reach"],
                                 "commands": rec.get("commands"),
                                 "raw_final_message": rec["raw_final_message"]})
                print(f"  [{e['id']}] VOID (attempt {attempt}): {rec['void_reason']}")
                if streak >= VOID_STREAK_STOP:
                    break
            else:
                streak = 0
                break
        rec = {"entry": e["id"], **rec, "retries": len(attempts) if not rec["void"] else len(attempts) - 1,
               "void_attempts": attempts if not rec["void"] else attempts[:-1]}
        payload["reviews"].append(rec)
        payload["models_observed"] = sorted({m for r in payload["reviews"] for m in r["models_observed"]})
        payload["totals"] = totals()
        write_result(result_path, payload)
        if not rec["void"]:
            print(f"  [{e['id']}] {len(rec['findings'])} kept / {rec['findings_offered']} offered, "
                  f"{rec['seconds']}s, cost {rec['cost_usd']}")
        if streak >= VOID_STREAK_STOP:
            payload["stopped"] = (f"two consecutive voided reviews (last: {e['id']}: "
                                  f"{rec['void_reason']}) - a stopped arm is not a run")
            payload["ended"] = now_iso()
            write_result(result_path, payload)
            print(f"STOPPED: {payload['stopped']}", file=sys.stderr)
            return finish(2)
    payload["complete"] = True
    payload["ended"] = now_iso()
    payload["totals"] = totals()
    write_result(result_path, payload)
    return finish(0)


def _add_tokens(acc: dict, usage) -> None:
    if isinstance(usage, dict):
        for k, v in usage.items():
            if isinstance(v, int) and not isinstance(v, bool):
                acc[k] = acc.get(k, 0) + v


def compute_totals(reviews: list[dict]) -> dict:
    """Totals over reviews, voided attempts included in seconds, cost and tokens."""
    seconds, costs, tokens = 0.0, [], {}
    for r in reviews:
        seconds += r.get("seconds") or 0
        if isinstance(r.get("cost_usd"), (int, float)):
            costs.append(r["cost_usd"])
        _add_tokens(tokens, r.get("tokens"))
        for a in r.get("void_attempts") or []:
            seconds += a.get("seconds") or 0
            if isinstance(a.get("cost_usd"), (int, float)):
                costs.append(a["cost_usd"])
            _add_tokens(tokens, a.get("tokens"))
    return {"reviews": len(reviews), "void": sum(1 for r in reviews if r["void"]),
            "retries": sum(r.get("retries", 0) for r in reviews),
            "findings_kept": sum(len(r["findings"]) for r in reviews),
            "findings_offered": sum(r["findings_offered"] for r in reviews),
            "cost_usd": round(sum(costs), 6) if costs else None,
            "tokens": tokens or None,
            "seconds": round(seconds, 1)}


def print_summary(payload: dict, result_path: Path) -> None:
    """One line per review, then the totals: readable after a smoke."""
    print("")
    print(f"summary {payload['arm']} t{payload['trial']} [{payload['model_requested']}]"
          f" - {'complete' if payload['complete'] else 'NOT complete'}")
    for r in payload["reviews"]:
        state = f"VOID ({r['void_reason']})" if r["void"] else "ok"
        retry = f", {r.get('retries')} retry" if r.get("retries") else ""
        print(f"  {r['entry']}: {r['seconds']}s, {len(r['findings'])} findings kept, {state}{retry}")
    t = compute_totals(payload["reviews"])
    cost = "unknown" if t["cost_usd"] is None else f"${t['cost_usd']:.4f}"
    tokens = ("unknown" if not t["tokens"]
              else ", ".join(f"{k} {v}" for k, v in sorted(t["tokens"].items())))
    print(f"totals: {t['reviews']} reviews, {t['void']} void, {t['retries']} retries, "
          f"{t['seconds']}s, cost {cost}, tokens {tokens}")
    print(f"result: {result_path}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--set", required=True)
    ap.add_argument("--arm", required=True, choices=ARMS)
    ap.add_argument("--model", required=True, help="full model id; never defaulted")
    ap.add_argument("--trial", required=True, type=int)
    ap.add_argument("--out", default="evals/results/review-catch")
    ap.add_argument("--entries", default=None, help="comma-separated entry ids")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if not args.model.strip():
        ap.error("--model must be a non-empty model id")
    return run_arm(args)


if __name__ == "__main__":
    sys.exit(main())
