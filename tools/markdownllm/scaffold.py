"""Domain birth and the pre-commit hook — the `pre-domain-scaffold:isolate`
hard hook, mechanised, plus `install-hook`.

`MDLLM_ENTRY` is the public entry shim (`tools/mdllm.py`) — the path every
installed hook and generated settings file must reference; the package is an
implementation detail behind it.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

from .boundary import TERMS_FILE
from .domain_kernel import apply_domain_kernel, build_domain_kernel_blocks
from .model import ID_RE, parse_frontmatter

MDLLM_ENTRY = Path(__file__).resolve().parents[1] / "mdllm.py"

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
# Prefer a repository-local environment when it exists. This keeps the
# deterministic floor available in managed shells (including Codex) whose
# bundled Python is deliberately absent from PATH or has no third-party
# packages. The two paths cover POSIX and Windows virtual environments.
for c in "$ROOT/.venv/bin/python" "$ROOT/.venv/Scripts/python.exe" python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  echo "mdllm: validation floor unavailable (python or $MDLLM not found) — commit blocked."
  echo "Install Python 3.10+ with PyYAML, or re-run install-hook from the framework root."
  exit 1
fi
# Disclosure boundary first: cheapest check, clearest message. Reads the LOCAL
# gitignored .boundary-terms; absent (every fresh clone, all CI) => silent no-op.
"$PY" "$MDLLM" boundary "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: staged content crosses the disclosure boundary — commit blocked."
  exit 1
}}
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
# Change-reconciliation advisories (estate-cadence-cluster Phase 1+4): the cue
# question (modified thing that is reasoned-from) and the serve-side notice
# (modified thing that is exposed). Advisory only — never blocks the commit.
"$PY" "$MDLLM" candidates "$ROOT" || true
"""

# The publication leg (estate-cadence-cluster Phase 1): after a commit lands
# and the floor has validated it, publish it — transport of already-committed,
# already-validated state, the mirror of estate-sync's fast-forwards. Opt-out
# per repo via `git: autopush: false` in AGENTS.md frontmatter; absence = on.
# All outcome handling (rejected = DIVERGED surfaced never resolved, offline =
# publication debt, no --force ever) lives in `mdllm autopush`; the hook only
# invokes it and always exits 0 — a post-commit surface must never fail the
# commit it follows.
POST_COMMIT_HOOK_BODY = """#!/bin/sh
# mdllm post-commit: autopush publication leg (estate-cadence-cluster Phase 1)
ROOT="$(git rev-parse --show-toplevel)"
MDLLM="$ROOT/{rel}"
PY=""
for c in "$ROOT/.venv/bin/python" "$ROOT/.venv/Scripts/python.exe" python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: publication stays manual; estate-sync --status reports the debt
fi
"$PY" "$MDLLM" autopush "$ROOT" || true
exit 0
"""

# The commit MESSAGE is a surface pre-commit structurally cannot see (git has
# not collected it yet) — and it is where honour-system disclosure failures
# actually live. Same portable preamble as HOOK_BODY; $1 is the message file.
COMMIT_MSG_HOOK_BODY = """#!/bin/sh
# mdllm commit-msg: disclosure-boundary check on the commit message
# (boundary-disclosure-check plan). Local .boundary-terms only; absent => no-op.
ROOT="$(git rev-parse --show-toplevel)"
MDLLM="$ROOT/{rel}"
PY=""
for c in "$ROOT/.venv/bin/python" "$ROOT/.venv/Scripts/python.exe" python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: the pre-commit hook already reported/blocked
fi
"$PY" "$MDLLM" boundary "$ROOT" --message "$1" --quiet || {{
  echo ""
  echo "mdllm: the commit MESSAGE crosses the disclosure boundary — commit blocked."
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

from markdownllm.session import _velocity_signal, _orient_forward, cmd_session_start


from markdownllm.coherence import _changed_files_recent, coherence_findings, cmd_coherence


def install_hook(root: Path) -> str:
    """Write the pre-commit validation hook into `root`'s git repo.
    Returns the mdllm path the hook will use (for reporting)."""
    git_dir = root / ".git"
    if not git_dir.is_dir():
        sys.exit(f"mdllm: {root} is not a git repository root")
    mdllm = MDLLM_ENTRY
    hook = git_dir / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    try:
        import os
        rel = Path(os.path.relpath(mdllm, root)).as_posix()
    except ValueError:  # e.g. different drives on Windows — no relative path exists
        rel = mdllm.as_posix()
    hook.write_text(HOOK_BODY.format(rel=rel), encoding="utf-8", newline="\n")
    msg_hook = git_dir / "hooks" / "commit-msg"
    msg_hook.write_text(COMMIT_MSG_HOOK_BODY.format(rel=rel),
                        encoding="utf-8", newline="\n")
    post_hook = git_dir / "hooks" / "post-commit"
    post_hook.write_text(POST_COMMIT_HOOK_BODY.format(rel=rel),
                         encoding="utf-8", newline="\n")
    for h in (hook, msg_hook, post_hook):
        try:
            h.chmod(h.stat().st_mode | 0o111)
        except OSError:
            pass  # Windows: executability is not a file-mode concern
    return rel


def cmd_install_hook(args) -> int:
    root = Path(args.path).resolve()
    rel = install_hook(root)
    hooks_dir = root / ".git" / "hooks"
    print(f"installed {hooks_dir / 'pre-commit'} + {hooks_dir / 'commit-msg'} "
          f"+ {hooks_dir / 'post-commit'} (mdllm via {rel})")
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
    fw_root = MDLLM_ENTRY.parents[1]
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

    # Reasoning prompts (orchestration.md): the generated session-start block
    # names `evaluate-triggers`, `surface-attention`, `session-orientation`,
    # `domain-velocity` (and the rituals name more) — until v3.24.0 scaffold
    # never delivered them, so every domain was born instructed to run prompts
    # it did not have (2026-08-01 estate sweep). They are things (type: prompt)
    # and land in the domain's own corpus.
    if (templates / "prompts").is_dir():
        pr_dir = target / "prompts"
        pr_dir.mkdir(exist_ok=True)
        for src in sorted((templates / "prompts").glob("*.md")):
            text = instantiate(src.read_text(encoding="utf-8"))
            # The relational graph is stripped on egress (thing.md, `exposed`):
            # a prompt's linked_things point into the FRAMEWORK's id space and
            # would dangle in the domain's separate corpus — same rule the
            # membrane applies to every thing that crosses a boundary.
            text = re.sub(r"(?m)^linked_things:\n(?:[ \t]+.*\n)+", "", text)
            (pr_dir / src.name).write_text(text, encoding="utf-8", newline="\n")
            written.append(f"prompts/{src.name}")

    # Fill the domain-kernel managed blocks now that skills AND prompts exist,
    # so the entry file is born in sync — the tier-routing block routes both
    # from the filesystem, and filling it before prompts/ landed would make
    # the birth commit drift against its own fresh build (the pre-commit
    # coherence check would rightly block it).
    ag = target / "AGENTS.md"
    ag_text = ag.read_text(encoding="utf-8")
    ag_meta, _, _ = parse_frontmatter(ag_text)
    ag_filled, _, _ = apply_domain_kernel(
        ag_text, build_domain_kernel_blocks(target, ag_meta or {}))
    ag.write_text(ag_filled, encoding="utf-8", newline="\n")

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
            # estate-sync BEFORE session-start: orientation reads git log, and
            # the log is only whole after the fetch (hard hook 4 — until
            # v3.24.0 scaffolded domains were born without it).
            "SessionStart": [
                {"hooks": [{"type": "command",
                            "command": f"python {rel_fw}/tools/mdllm.py estate-sync ."},
                           {"type": "command",
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

    # Disclosure boundary (boundary-disclosure-check plan): a domain is born
    # with its own LOCAL terms file — per-repo boundaries; a domain's disclosure
    # surface is its own — and a .gitignore that keeps it local BEFORE the
    # `git add -A` first commit, so the vocabulary never enters any repo,
    # including the domain's own.
    bt_template = templates / "boundary-terms.template"
    if bt_template.is_file():
        (target / TERMS_FILE).write_text(
            bt_template.read_text(encoding="utf-8"),
            encoding="utf-8", newline="\n")
        gi_d = target / ".gitignore"
        gi_existing = gi_d.read_text(encoding="utf-8") if gi_d.is_file() else ""
        if TERMS_FILE not in {ln.strip() for ln in gi_existing.splitlines()}:
            gi_d.write_text(
                gi_existing.rstrip("\n") + ("\n" if gi_existing else "")
                + f"# local disclosure boundary — never committed\n{TERMS_FILE}\n",
                encoding="utf-8", newline="\n")
        written.append(f".gitignore (+ local {TERMS_FILE}, never committed)")

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

    # Private-by-default at birth: register the newborn's NAME in the framework
    # root's own local terms file, so framework commits cannot mention it until
    # the operator deletes the line — making publication an explicit decision
    # rather than a default. Same invariant as the .gitignore step above: which
    # domains exist is domain state, and it reaches the framework repo only as
    # a local, uncommitted fact.
    fw_terms = fw_root / TERMS_FILE
    fw_existing = (fw_terms.read_text(encoding="utf-8")
                   if fw_terms.is_file() else "")
    fw_terms_present = {ln.split("==>")[0].strip().lower()
                        for ln in fw_existing.splitlines()
                        if ln.strip() and not ln.strip().startswith("#")}
    if name.lower() not in fw_terms_present:
        if not fw_existing and bt_template.is_file():
            fw_existing = bt_template.read_text(encoding="utf-8")
        fw_terms.write_text(
            fw_existing.rstrip("\n") + ("\n" if fw_existing else "")
            + f"{name}\n", encoding="utf-8", newline="\n")

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
    print("  - run `mdllm session-start .` before your next commit: this domain "
          "is born with `session_gate: strict` (v3.28.0), so from the second "
          "commit on, the floor requires a fresh session-start attestation — "
          "the birth commit you just saw was the only exempt one")
    print("  - hardened out of the box: .claude/settings.json fires session-start + "
          "post-write validation automatically (Claude Code / VS Code Copilot agent "
          "mode), and /end-session + /retrospective are installed. Delete .claude/ to "
          "fall back to interpretation-only — the domain kernel still drives both.")
    if broken:
        print("\nBIRTH SEQUENCE INCOMPLETE — the isolation invariant did not "
              "fully hold; fix the FAIL lines before using the domain.")
    return 1 if broken else 0
