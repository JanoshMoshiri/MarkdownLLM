"""Disclosure-boundary check (boundary-disclosure-check plan).

A repo declares, in a LOCAL gitignored file (`.boundary-terms`), terms that
must never cross its disclosure boundary — client names, personal names,
internal identifiers. The floor blocks any commit whose staged content,
staged filenames, or commit message contains one.

The invariant this module must never violate: the framework ships the
CAPABILITY, never the VOCABULARY. No terms, no hashed terms (short-string
hashes are dictionary-recoverable), no match counts in committed artifacts.
Findings print to the console only. Enforcement is local by construction —
where no terms file exists (every fresh clone, all CI), the check no-ops
silently. Unlike every other floor check, this one must NOT be hardened
rightward into CI: the knowledge it checks against is exactly the knowledge
that must not be published.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .repository_view import RepositoryView, RepositoryViewError

TERMS_FILE = ".boundary-terms"


def load_terms(root: Path) -> list[tuple[str, str | None]] | None:
    """Parse the local terms file. Returns None when absent (=> no-op).

    Line format: `term`, or `term ==> approved replacement`, `#` comments.
    Terms match case-insensitively as literal substrings.
    """
    path = root / TERMS_FILE
    if not path.is_file():
        return None
    terms: list[tuple[str, str | None]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==>" in line:
            term, _, repl = line.partition("==>")
            terms.append((term.strip(), repl.strip() or None))
        else:
            terms.append((line, None))
    return terms


def scan_text(text: str, terms: list[tuple[str, str | None]],
              label: str) -> list[str]:
    """Return console-ready finding lines for every term match in `text`.
    `label` locates the surface (a filename, 'commit message', a rev)."""
    findings: list[str] = []
    for n, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for term, repl in terms:
            if term.lower() in low:
                hint = f" — use {repl!r}" if repl else ""
                findings.append(
                    f"{label}:{n}: contains boundary term {term!r}{hint}")
    return findings


def _git(root: Path, args: list[str]) -> str:
    out = subprocess.run(["git", *args], cwd=root, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return out.stdout if out.returncode == 0 and out.stdout else ""


def self_guard(root: Path, view: RepositoryView | None = None) -> str | None:
    """The terms file must never itself be tracked — the mechanism protecting
    the boundary must not become the leak."""
    candidate = view or RepositoryView.index(root)
    if candidate.exists(TERMS_FILE):
        return (f"{TERMS_FILE} is TRACKED — it must stay local. "
                f"`git rm --cached {TERMS_FILE}` and add it to .gitignore.")
    return None


def _empty_tree(root: Path) -> str:
    made = subprocess.run(
        ["git", "mktree"], cwd=root, input="", capture_output=True,
        text=True, encoding="utf-8", errors="replace")
    if made.returncode != 0 or not made.stdout.strip():
        raise RepositoryViewError("could not construct Git's empty tree")
    return made.stdout.strip()


def staged_findings(
        root: Path, terms: list[tuple[str, str | None]],
        view: RepositoryView | None = None) -> list[str]:
    """Scan staged ADDITIONS (the boundary is the crossing, not the archive)
    plus staged filenames."""
    findings: list[str] = []
    candidate = view or RepositoryView.index(root)
    assert candidate.tree_sha is not None
    head = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=root,
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    base = head.stdout.strip() if head.returncode == 0 else _empty_tree(root)
    diff_prefix = [base, candidate.tree_sha, "--"]
    for name in _git(root, ["diff", "--name-only", *diff_prefix]).splitlines():
        low = name.lower()
        for term, repl in terms:
            if term.lower() in low:
                hint = f" — use {repl!r}" if repl else ""
                findings.append(
                    f"{name}: filename contains boundary term {term!r}{hint}")
    diff = _git(root, ["diff", "--unified=0", "--no-color", *diff_prefix])
    current = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            low = line.lower()
            for term, repl in terms:
                if term.lower() in low:
                    hint = f" — use {repl!r}" if repl else ""
                    findings.append(f"{current}: staged addition contains "
                                    f"boundary term {term!r}{hint}")
    return findings


def history_findings(root: Path,
                     terms: list[tuple[str, str | None]]) -> list[str]:
    """Full-archive audit: every commit message and every blob at every rev.
    Console-only, for the operator's pre-publication ritual."""
    findings: list[str] = []
    msgs = _git(root, ["log", "--all", "--format=%h%x00%B%x01"])
    for entry in msgs.split("\x01"):
        if "\x00" not in entry:
            continue
        sha, _, body = entry.partition("\x00")
        findings.extend(scan_text(body, terms, f"commit {sha.strip()}"))
    revs = _git(root, ["rev-list", "--all"]).split()
    for term, repl in terms:
        hits = subprocess.run(
            ["git", "grep", "-il", "-F", term, *revs],
            cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        locs = [l for l in hits.stdout.splitlines() if l.strip()]
        if locs:
            hint = f" — use {repl!r}" if repl else ""
            findings.append(f"history: term {term!r} appears in "
                            f"{len(locs)} rev:path location(s){hint} "
                            f"(first: {locs[0]})")
    return findings


def cmd_boundary(args) -> int:
    root = Path(args.path).resolve()
    terms = load_terms(root)
    quiet = getattr(args, "quiet", False)
    if terms is None:
        if not quiet:
            print(f"boundary: no {TERMS_FILE} — skipped (capability present, "
                  f"vocabulary is local-only)")
        return 0
    findings: list[str] = []
    if getattr(args, "message", None):
        try:
            guard = self_guard(root)
        except RepositoryViewError as exc:
            print(f"boundary: BLOCKED — staged candidate could not be frozen: {exc}")
            return 1
        if guard:
            findings.append(guard)
        text = Path(args.message).read_text(encoding="utf-8", errors="replace")
        findings.extend(scan_text(text, terms, "commit message"))
    elif getattr(args, "history", False):
        try:
            guard = self_guard(root)
        except RepositoryViewError as exc:
            print(f"boundary: BLOCKED — staged candidate could not be frozen: {exc}")
            return 1
        if guard:
            findings.append(guard)
        findings.extend(history_findings(root, terms))
    else:
        try:
            view = RepositoryView.index(root)
            guard = self_guard(root, view)
            if guard:
                findings.append(guard)
            findings.extend(staged_findings(root, terms, view))
        except RepositoryViewError as exc:
            print(f"boundary: BLOCKED — staged candidate could not be frozen: {exc}")
            return 1
    if findings:
        print("boundary: BLOCKED — content crosses the disclosure boundary:")
        for f in findings:
            print(f"  - {f}")
        print(f"  (false positive? edit {TERMS_FILE} — local, never committed)")
        return 1
    if not quiet:
        print("boundary: clean")
    return 0
