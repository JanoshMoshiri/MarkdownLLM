"""Config-driven estate assembly — Phase 3 of the ``cowork-adapter`` plan.

``mdllm assemble --config <file> [filters ...]`` rebuilds a working estate
inside an environment that started without one: clone the configured
domains under ``domains/``, resolve each repo's REAL default branch from
its remote's own HEAD (refusing to guess), install the deterministic
floor hook, set the commit identity, verify no credential leaked into any
git config, then run the ordered session lifecycle per domain — sync
before orienting, then ``session-start --contract`` so the Tier-0
contract CONTENT enters the transcript, then the full trigger evaluation
and the imports COVERAGE line that summaries bury. It closes with the
BRANCH MAP and a handoff that says which controls ran mechanically and
which remain interpretation.

This module is harness-neutral by design: nothing here names a vendor.
It is the post-clone half of any bootstrap for an environment with no
entry-file discovery — an ephemeral container, a bare CI runner, a
devcontainer. A vendor bundle's bash layer shrinks to what must precede
the framework (credential intake + framework clone) and then hands off
to this command.

Credentials: ambient by default; ``GH_PAT``/``MDLLM_GIT_TOKEN`` when set
are supplied per-command through a scoped HTTP header (publish.py's
mechanics — never on disk, never in git config, redacted from output).

Exit codes: 0 = every selected domain assembled and oriented;
1 = at least one domain failed (each failure printed in place);
2 = usage (config missing/invalid, no domain matched a filter).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from .publish import command_token, git_command, redact
from .scaffold import cmd_install_hook
from .session import cmd_session_start
from .sync import sync_repo


def parse_config(path: Path) -> tuple[dict[str, str], str]:
    """Flat KEY=VALUE lines; quotes optional; # comments. DOMAINS is a
    whitespace-separated list. Deliberately not bash — both the thin bash
    bootstrap and this module read it with no sourcing and no arrays."""
    if not path.is_file():
        return {}, f"config not found at {path}"
    config: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        config[key.strip()] = value.strip().strip('"').strip("'")
    missing = [k for k in ("GIT_NAME", "GIT_EMAIL", "DOMAINS")
               if not config.get(k)]
    if missing:
        return config, f"config is missing {', '.join(missing)}"
    return config, ""


def clone_url(entry: str) -> str:
    """owner/repo → the GitHub HTTPS form; anything already URL- or
    path-shaped passes through untouched (file://, https://, ssh, a local
    path) — the tests and non-GitHub estates need no special casing."""
    if re.fullmatch(r"[^/\s:]+/[^/\s:]+", entry):
        return f"https://github.com/{entry}.git"
    return entry


def select_domains(entries: list[str], filters: list[str]
                   ) -> tuple[list[str], list[str]]:
    """Case-insensitive substring match on the entry or its basename.
    No filters selects everything."""
    if not filters:
        return list(entries), []
    chosen, misses = [], []
    for term in filters:
        hit = [e for e in entries
               if term.lower() in e.lower()
               or term.lower() in Path(e).name.lower()]
        if hit:
            chosen.extend(h for h in hit if h not in chosen)
        else:
            misses.append(term)
    return chosen, misses


def resolve_remote_head(repo: Path, token: str | None) -> str:
    """The remote's own HEAD, then clone's origin/HEAD. Never a guess."""
    symref = git_command(repo, "ls-remote", "--symref", "origin", "HEAD",
                         token=token)
    for line in symref.stdout.splitlines():
        if line.startswith("ref:"):
            return line.split()[1].removeprefix("refs/heads/")
    local = git_command(repo, "symbolic-ref", "--short",
                        "refs/remotes/origin/HEAD")
    return local.stdout.strip().removeprefix("origin/")


def _ns(**kw) -> argparse.Namespace:
    return argparse.Namespace(**kw)


def assemble_domain(root: Path, entry: str, config: dict[str, str],
                    token: str | None) -> tuple[str, str, str] | None:
    """Clone + floor + identity for one domain; (name, default, checked-out)
    on success, None on failure (reason already printed, redacted)."""
    name = Path(entry).name.removesuffix(".git")
    target = root / "domains" / name

    def say(line: str) -> None:
        print(redact(line, token))

    if target.exists() and (target / ".git").exists():
        say(f"   - {name}: already present — reusing the existing clone")
        result = sync_repo(target, token=token)
        detail = f" — {result['detail']}" if result["detail"] else ""
        say(f"     sync: {result['state']}{detail}")
        if result["state"] in {"dirty", "diverged", "in-operation"}:
            say("     !! unresolved repository state was reported and left "
                "untouched; assembly will not merge, reset, or discard it")
    else:
        say(f"   - {entry} -> domains/{name}")
        (root / "domains").mkdir(exist_ok=True)
        cloned = git_command(root, "clone", "--quiet", clone_url(entry),
                             str(target), token=token)
        if cloned.returncode != 0:
            say(f"     !! FAILED to clone {entry}: "
                f"{cloned.stderr.strip()}")
            return None

    branch = resolve_remote_head(target, token)
    if not branch:
        say(f"     !! FAILED: cannot determine the default branch of "
            f"{entry}. Refusing to assume 'main' or 'master'. Ask the "
            f"operator which branch is authoritative, then: "
            f"git -C domains/{name} config mdllm.defaultbranch <branch>")
        return None
    if git_command(target, "show-ref", "--verify", "--quiet",
                   f"refs/remotes/origin/{branch}").returncode != 0:
        say(f"     !! FAILED: resolved {branch!r} for {entry}, but "
            f"origin/{branch} does not exist")
        return None

    git_command(target, "config", "user.name", config["GIT_NAME"])
    git_command(target, "config", "user.email", config["GIT_EMAIL"])
    git_command(target, "config", "mdllm.defaultbranch", branch)
    git_command(target, "remote", "set-head", "origin", branch)

    if cmd_install_hook(_ns(path=str(target))) != 0:
        say(f"     !! floor hook installation failed for {name} — the "
            "commit boundary is NOT enforced in this clone")

    checked_out = git_command(target, "rev-parse", "--abbrev-ref",
                              "HEAD").stdout.strip()
    if checked_out != branch:
        say(f"     !! WARNING: {name} is checked out on {checked_out!r} "
            f"but its default branch is {branch!r} — do not publish "
            "until resolved with the operator.")
    else:
        say(f"     default branch: {branch}")
    return name, branch, checked_out


def _leak_check(root: Path, names: list[str]) -> bool:
    """No credential may survive in any git config this assembly touched."""
    configs = [root / ".git" / "config"] + [
        root / "domains" / n / ".git" / "config" for n in names]
    for cfg in configs:
        if cfg.is_file() and re.search(
                r"github_pat_|ghp_|x-access-token",
                cfg.read_text(encoding="utf-8", errors="replace")):
            print(f"!! SECURITY: credential material found in {cfg} — "
                  "aborting. Remove it before continuing.")
            return False
    return True


def cmd_assemble(args) -> int:
    root = Path(getattr(args, "root", ".")).resolve()
    token = command_token()

    config, problem = parse_config(Path(args.config))
    if problem:
        print(f"assemble: {problem}")
        return 2

    entries = config["DOMAINS"].split()
    selected, misses = select_domains(entries, list(args.filters or []))
    if misses:
        print(f"assemble: no configured domain matched: {', '.join(misses)}")
        print("Configured domains:")
        for e in entries:
            print(f"  {e}")
        return 2
    if args.filters:
        print(f"==> domain filter active — assembling {len(selected)} "
              f"of {len(entries)}: {' '.join(Path(e).name for e in selected)}")

    print("==> cloning domains + resolving default branches + installing "
          "floor hooks")
    branch_map: list[tuple[str, str, str]] = []
    failures = 0
    for entry in selected:
        row = assemble_domain(root, entry, config, token)
        if row is None:
            failures += 1
        else:
            branch_map.append(row)

    if not _leak_check(root, [n for n, _, _ in branch_map]):
        return 1
    print("==> safety check: no credential in any git config.")

    # -- the ordered lifecycle, per domain, with the contract emitted -----
    for name, _, _ in branch_map:
        target = root / "domains" / name
        print(f"\n=========================  {name}  =========================")
        print("----- estate-sync (sync BEFORE orienting) -----")
        result = sync_repo(target, token=token)
        detail = f" — {result['detail']}" if result["detail"] else ""
        print(f"  {result['state']}{detail}")
        print("----- session-start (the Tier-0 contract is emitted below —"
              " it is IN CONTEXT once printed) -----")
        cmd_session_start(_ns(path=str(target), contract=True))
        print("----- triggers (FULL — including what the floor cannot "
              "evaluate; judging those is yours) -----")
        from .triggers import cmd_triggers
        cmd_triggers(_ns(path=str(target), estate=False))
        print("----- imports-check (COVERAGE is the number that matters: "
              "could-not-check and checked look identical in a summary) "
              "-----")
        from .imports_check import cmd_imports_check
        cmd_imports_check(_ns(path=str(target)))

    # -- branch map + handoff --------------------------------------------
    print("\n=========================  BRANCH MAP  ========================")
    print("The ONLY branch names that may be published to — each read from "
          "its remote's own HEAD, never assumed:")
    for name, branch, checked_out in branch_map:
        marker = ("" if branch == checked_out
                  else "   <-- MISMATCH, do not publish")
        print(f"  {name:<28} default={branch:<16} "
              f"checked-out={checked_out}{marker}")
    print("Recorded per repo as mdllm.defaultbranch; `mdllm publish` reads "
          "it and refuses everything else.")

    mode = "env-scoped credential" if token else "ambient credentials"
    print("\n=========================  HANDOFF  ===========================")
    print("RAN MECHANICALLY (do not repeat, do not re-ask): clone, branch "
          "resolution, floor hooks, identity, leak check, sync, "
          "session-start WITH the Tier-0 contract emitted into this "
          "transcript, full trigger evaluation, imports coverage.")
    print("ENFORCED AT COMMIT: pre-commit validate + coherence. Never "
          "--no-verify; a blocked commit is fixed at its cause.")
    if token:
        print("PUBLICATION (" + mode + "): the post-commit autopush leg "
              "will report AUTH-FAILED on every commit — by design: the "
              "credential is command-scoped and absent from git config. "
              "The publication guarantee does NOT hold here mechanically. "
              "After EVERY commit run:\n"
              "    python tools/mdllm.py publish domains/<name>\n"
              "(with the credential in GH_PAT). A committed-but-unpublished "
              "change is lost when this environment is reclaimed.")
    else:
        print("PUBLICATION (" + mode + "): the post-commit autopush leg "
              "publishes each validated commit unless the repo opts out; "
              "`mdllm estate-sync . --status` before session end reports "
              "any publication debt.")
    print("YOURS, WITH NO BACKSTOP (interpretation — printed because "
          "skipping them is silent): judge every non-evaluable trigger "
          "above; read the skills the emitted contract lists before your "
          "FIRST write (the write skill before ANY write); answer the "
          "exposure question at creation; record directional calls as "
          "decisions AS you make them. If you skip one, say so out loud.")

    if failures:
        print(f"\nassemble: {failures} domain(s) FAILED — see above.")
        return 1
    print("\n==> assembled. Workspace ready.")
    return 0
