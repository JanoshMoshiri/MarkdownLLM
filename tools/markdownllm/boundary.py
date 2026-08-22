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


def load_located_terms(
        root: Path) -> list[tuple[int, str, str | None]] | None:
    """`load_terms`, but each entry carries the 1-based line it was read from.

    The line number is what lets `--audit-terms` name an offending entry
    without printing it: the operator opens the local file at that line. See
    `term_audit_findings`.
    """
    path = root / TERMS_FILE
    if not path.is_file():
        return None
    terms: list[tuple[int, str, str | None]] = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==>" in line:
            term, _, repl = line.partition("==>")
            terms.append((n, term.strip(), repl.strip() or None))
        else:
            terms.append((n, line, None))
    return terms


def load_terms(root: Path) -> list[tuple[str, str | None]] | None:
    """Parse the local terms file. Returns None when absent (=> no-op).

    Line format: `term`, or `term ==> approved replacement`, `#` comments.
    Terms match case-insensitively as literal substrings.
    """
    located = load_located_terms(root)
    if located is None:
        return None
    return [(term, repl) for _n, term, repl in located]


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


def term_audit_findings(root: Path,
                        located: list[tuple[int, str, str | None]]) -> list[str]:
    """Entries that occur in this repository's OWN tracked content.

    A term in a repo's own tracked tree is not a private identifier. Either it
    is noise — and it is making the staged and history legs permanently red,
    which trains the operator to ignore them — or it is a leak that is already
    committed. Both are actionable, which is what makes this a check and not a
    warning.

    Why an invariant and not a state-once-and-derive promotion: the list this
    reasons over must never be committed, so the floor cannot own it. It can
    own a property OF it. (`a-control-that-must-stay-local-has-no-floor`.)

    Reports by **line number in the local file, never by term.** The staged and
    message legs print a term because they are refusing a specific edit and the
    operator needs to see which word to change. This leg is different: a hit
    means the word is already in tracked content, so naming it in output adds
    exposure without adding information the operator cannot get by opening the
    file at the line named.
    """
    findings: list[str] = []
    for lineno, term, _repl in located:
        hits = subprocess.run(
            ["git", "grep", "-I", "-l", "-i", "-F", "-e", term, "HEAD"],
            cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        if hits.returncode not in (0, 1):
            findings.append(
                f"{TERMS_FILE}:{lineno}: could not be audited — `git grep` "
                f"failed (rc {hits.returncode}); this is 'could not look', "
                f"not 'clean'")
            continue
        paths = [l.split(":", 1)[1] for l in hits.stdout.splitlines()
                 if ":" in l]
        if paths:
            findings.append(
                f"{TERMS_FILE}:{lineno}: this entry occurs in "
                f"{len(paths)} tracked file(s) — first: {paths[0]}. Either "
                f"noise (remove it) or an already-committed leak (act on it). "
                f"The term is deliberately not printed.")
    return findings


def cmd_boundary(args) -> int:
    root = Path(args.path).resolve()
    located = load_located_terms(root)
    terms = None if located is None else [(t, r) for _n, t, r in located]
    quiet = getattr(args, "quiet", False)
    if terms is None:
        if not quiet:
            print(f"boundary: no {TERMS_FILE} — skipped (capability present, "
                  f"vocabulary is local-only)")
        return 0
    findings: list[str] = []
    if getattr(args, "audit_terms", False):
        guard = self_guard(root)
        if guard:
            findings.append(guard)
        findings.extend(term_audit_findings(root, located))
        if findings:
            print(f"boundary: {len(findings)} terms-file finding(s) — "
                  f"each entry below is either noise or an already-committed "
                  f"leak:")
            for f in findings:
                print(f"  - {f}")
            return 1
        if not quiet:
            print(f"boundary: terms file clean ({len(located)} entries, none "
                  f"present in tracked content)")
        return 0
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
