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


def self_guard(root: Path) -> str | None:
    """The terms file must never itself be tracked — the mechanism protecting
    the boundary must not become the leak."""
    if _git(root, ["ls-files", "--", TERMS_FILE]).strip():
        return (f"{TERMS_FILE} is TRACKED — it must stay local. "
                f"`git rm --cached {TERMS_FILE}` and add it to .gitignore.")
    return None


def staged_findings(root: Path,
                    terms: list[tuple[str, str | None]]) -> list[str]:
    """Scan staged ADDITIONS (the boundary is the crossing, not the archive)
    plus staged filenames."""
    findings: list[str] = []
    for name in _git(root, ["diff", "--cached", "--name-only"]).splitlines():
        low = name.lower()
        for term, repl in terms:
            if term.lower() in low:
                hint = f" — use {repl!r}" if repl else ""
                findings.append(
                    f"{name}: filename contains boundary term {term!r}{hint}")
    diff = _git(root, ["diff", "--cached", "--unified=0", "--no-color"])
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
    guard = self_guard(root)
    if guard:
        findings.append(guard)
    if getattr(args, "message", None):
        text = Path(args.message).read_text(encoding="utf-8", errors="replace")
        findings.extend(scan_text(text, terms, "commit message"))
    elif getattr(args, "history", False):
        findings.extend(history_findings(root, terms))
    else:
        findings.extend(staged_findings(root, terms))
    if findings:
        print("boundary: BLOCKED — content crosses the disclosure boundary:")
        for f in findings:
            print(f"  - {f}")
        print(f"  (false positive? edit {TERMS_FILE} — local, never committed)")
        return 1
    if not quiet:
        print("boundary: clean")
    return 0
