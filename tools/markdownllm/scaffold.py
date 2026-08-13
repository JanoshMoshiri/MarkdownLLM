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

from . import adapters as harness_adapters
from .adapter_install import portable_artifact_parts
from .boundary import TERMS_FILE
from .harness_ports import (
    HarnessContext, RenderPort, ScaffoldNoticePort, ShortcutPort,
)
from .runtime import SH_RESOLVE, execution_test_hook
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
# Interpreter resolution (one owner: markdownllm/runtime.py — the comment
# there explains the candidate order and why the probe imports the floor's
# real dependency rather than just proving an interpreter exists).
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  echo "mdllm: validation floor unavailable (no interpreter with PyYAML, or $MDLLM not found) — commit blocked."
  echo "Run \\`mdllm runtime-probe .\\` (or \\`python <framework>/tools/mdllm.py runtime-probe .\\`) for a per-candidate report."
  exit 1
fi
# Disclosure boundary first: cheapest check, clearest message. Reads the LOCAL
# gitignored .boundary-terms; absent (every fresh clone, all CI) => silent no-op.
mdllm_python "$MDLLM" boundary "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: staged content crosses the disclosure boundary — commit blocked."
  exit 1
}}
mdllm_python "$MDLLM" validate "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: validation Errors — commit blocked. Fix or run with --no-verify (discouraged)."
  exit 1
}}
# Coherence: generated-artifact freshness (kernel/index drift) + spec-catalog
# integrity. Self-scoping — at a domain root (no .markdownllm) only the general
# checks run, so the same hook is correct in the framework and in every domain.
mdllm_python "$MDLLM" coherence "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: coherence Errors — a generated artifact (kernel/index) or the spec catalog is stale. Regenerate and re-commit, or --no-verify (discouraged)."
  exit 1
}}
# Change-reconciliation advisories (estate-cadence-cluster Phase 1+4): the cue
# question (modified thing that is reasoned-from) and the serve-side notice
# (modified thing that is exposed). Advisory only — never blocks the commit.
mdllm_python "$MDLLM" candidates "$ROOT" || true
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
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: publication stays manual; estate-sync --status reports the debt
fi
mdllm_python "$MDLLM" autopush "$ROOT" || true
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
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: the pre-commit hook already reported/blocked
fi
mdllm_python "$MDLLM" boundary "$ROOT" --message "$1" --quiet || {{
  echo ""
  echo "mdllm: the commit MESSAGE crosses the disclosure boundary — commit blocked."
  exit 1
}}
"""

# Interpreter resolution has ONE owner (runtime.py); substituted here once so
# every consumer — install_hook's writes, doctor's currency comparison — sees
# the same final bytes. Only {rel} remains for per-repo formatting, so the
# fragment's shell braces (${MDLLM%/*/*}) are doubled to survive .format().
_SH_RESOLVE_ESCAPED = SH_RESOLVE.replace("{", "{{").replace("}", "}}")
HOOK_BODY = HOOK_BODY.replace("{resolve}", _SH_RESOLVE_ESCAPED)
POST_COMMIT_HOOK_BODY = POST_COMMIT_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)
COMMIT_MSG_HOOK_BODY = COMMIT_MSG_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)


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
    # The execution test fires a real pre-commit, which is a full validate.
    # On a large domain that is minutes, and chaining it in a harness silently
    # blew a 120s tool timeout and read as a hang (field report 2026-08-13).
    # Skipping is opt-in and downgrades the claim honestly: installed is a
    # weaker fact than runs, and the report must say which one it has.
    if getattr(args, "no_test", False):
        print("execution test: SKIPPED (--no-test) — the hook is installed but "
              "unproven; it will first fire at the next real commit")
        return 0
    # Execution-test the hook we just wrote (vendor-harness-adapter-foundation
    # Phase 1): installed is a weaker fact than runs. Where git cannot fire it
    # (`git hook run` < 2.36), report untested rather than implying success.
    result = execution_test_hook(root)
    if not result["supported"]:
        print("execution test: UNTESTED — this git predates `git hook run` "
              "(2.36); the hook will first fire at the next real commit")
        return 0
    if result["passed"]:
        print("execution test: pre-commit ran and passed")
        return 0
    print("execution test: pre-commit ran and FAILED — the floor is wired but "
          "blocking; its output follows:")
    if result.get("detail"):
        print(result["detail"])
    return 1


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
        sys.exit("mdllm: framework and target have no relative path; refusing "
                 "to embed an absolute machine-specific adapter command")

    # Resolve the complete outer projection before creating the target.  This
    # makes an unknown selection or a cross-adapter path collision a true
    # preflight failure rather than a half-scaffolded domain.
    selected_names = harness_adapters.selection(
        getattr(args, "harness", None))
    selected_adapters = tuple(harness_adapters.get(n) for n in selected_names)
    ctx = HarnessContext(framework_root_rel=rel_fw)
    adapter_shortcuts: list[tuple[str, Path]] = []
    adapter_artifacts: list[tuple[str, bytes]] = []
    projected: dict[tuple[str, ...], tuple[str, bool]] = {}

    def claim_projection(
            relpath: str, owner: str, *, directory: bool = False) -> str:
        """Reserve a portable target path before scaffold creates anything.

        The projection is case-folded and separator-normalised even off
        Windows.  A scaffold committed on one platform must not contain two
        paths which become the same path when cloned on another.  Core
        directories reserve their whole namespace from adapter output.
        """
        if not isinstance(relpath, str):
            sys.exit(f"mdllm: {owner!r} projected non-string path {relpath!r}")
        try:
            # Scaffold accepts either separator spelling as adapter input but
            # reserves and writes one POSIX projection.  That lets a Windows-
            # shaped path collide visibly with its portable spelling instead
            # of becoming a second file after clone.
            parts = portable_artifact_parts(relpath.replace("\\", "/"))
        except ValueError:
            sys.exit(f"mdllm: {owner!r} projected unsafe path {relpath!r}")
        key = tuple(part.casefold() for part in parts)
        for previous_key, (previous_owner, previous_directory) in projected.items():
            same = key == previous_key
            within_previous = (previous_directory
                               and key[:len(previous_key)] == previous_key)
            owns_previous_parent = (directory
                                    and previous_key[:len(key)] == key)
            # Two file projections also cannot stand in an ancestor relation:
            # the first would need to be both a file and a directory.
            file_prefix = (not directory and not previous_directory
                           and (key[:len(previous_key)] == previous_key
                                or previous_key[:len(key)] == key))
            if same or within_previous or owns_previous_parent or file_prefix:
                sys.exit(
                    f"mdllm: adapter projection collision at {relpath!r}: "
                    f"{previous_owner} and {owner}")
        projected[key] = (owner, directory)
        return "/".join(parts)

    # Reserve every path the harness-neutral scaffold owns before asking an
    # adapter for its projection.  Directory reservations cover all generated
    # skills/prompts and the git metadata namespace, including paths added to
    # those core sets by future template evolution.
    for core_path in ("things", "skills", ".git"):
        claim_projection(core_path, "scaffold:core", directory=True)
    if (templates / "prompts").is_dir():
        claim_projection("prompts", "scaffold:core", directory=True)
    for core_path in ("AGENTS.md",):
        claim_projection(core_path, "scaffold:core")
    boundary_template = templates / "boundary-terms.template"
    if boundary_template.is_file():
        claim_projection(TERMS_FILE, "scaffold:core")
        claim_projection(".gitignore", "scaffold:core")

    for adapter in selected_adapters:
        if isinstance(adapter, ShortcutPort):
            for relpath, src in adapter.shortcut_sources(templates).items():
                normalised = claim_projection(
                    relpath, f"{adapter.name}:shortcuts")
                adapter_shortcuts.append((normalised, src))
        if isinstance(adapter, RenderPort):
            for relpath, data in adapter.render(ctx).items():
                normalised = claim_projection(relpath, f"{adapter.name}:render")
                adapter_artifacts.append((normalised, data))

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

    # Deliberate-ritual shortcut projections (inert until the operator invokes
    # them). WHERE each file belongs is the adapter's knowledge; the placeholder
    # substitution and the writes stay here with every other template. The
    # auto-firing lifecycle adapter stays opt-in (hint printed below).
    # Every adapter capability is a declared port, tested with isinstance —
    # an adapter without shortcuts simply projects none (v1.6).
    for relpath, src in adapter_shortcuts:
        dst = target / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(instantiate(src.read_text(encoding="utf-8")),
                       encoding="utf-8", newline="\n")
        written.append(relpath)

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

    # Lifecycle adapter: render the default harness's managed artifacts so a
    # new domain is hardened out of the box — startup context and post-write
    # feedback per the inward lifecycle bindings. The adapter owns the vendor
    # format; the bytes are written verbatim here. Still optional in spirit:
    # delete the artifacts and the domain kernel drives both by interpretation.
    # Scaffold writes directly (it runs as the tool, not through a
    # permissions-gated editor).
    for relpath, data in adapter_artifacts:
        dst = target / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        written.append(relpath)

    # Disclosure boundary (boundary-disclosure-check plan): a domain is born
    # with its own LOCAL terms file — per-repo boundaries; a domain's disclosure
    # surface is its own — and a .gitignore that keeps it local BEFORE the
    # `git add -A` first commit, so the vocabulary never enters any repo,
    # including the domain's own.
    bt_template = boundary_template
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
    for adapter in selected_adapters:
        if isinstance(adapter, ScaffoldNoticePort):
            print(adapter.scaffold_guidance())
    if broken:
        print("\nBIRTH SEQUENCE INCOMPLETE — the isolation invariant did not "
              "fully hold; fix the FAIL lines before using the domain.")
    return 1 if broken else 0
