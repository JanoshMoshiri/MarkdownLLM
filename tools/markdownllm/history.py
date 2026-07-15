"""Git-stream views: the CHANGELOG draft and the on-demand worklog.

Both read the commit stream — the backward record — and render it; neither
is a committed artifact (the committed WORKLOG was retired in v3.17).
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .model import parse_frontmatter, scan

def cmd_changelog(args) -> int:
    """Draft a CHANGELOG entry from structured commit messages since a ref."""
    root = Path(args.path).resolve()
    rng = f"{args.since}..HEAD" if args.since else "HEAD"
    out = subprocess.run(["git", "log", "--format=%s", rng], cwd=root,
                         capture_output=True, text=True, check=True).stdout
    groups: dict[str, list[str]] = {}
    for line in out.strip().splitlines():
        prefix = line.split(":", 1)[0].strip() if ":" in line else "other"
        groups.setdefault(prefix, []).append(line)
    order = ["framework", "create", "update", "insight", "retrospective",
             "session-end", "measure", "validate", "fix", "docs", "chore", "other"]
    print(f"## [x.y.z] - {dt.date.today().isoformat()}\n")
    print("<!-- drafted by `mdllm changelog`; set the version, write the one-paragraph")
    print("     summary, prune noise — then commit. `git log` holds the detail. -->\n")
    for key in sorted(groups, key=lambda k: order.index(k) if k in order else 99):
        print(f"**{key}:**")
        for line in groups[key]:
            print(f"- {line}")
        print()
    return 0


def cmd_worklog(args) -> int:
    """Print an **on-demand** session-grouped view of the commit stream — NOT a
    committed artifact. The commit stream is the backward record (a committed
    WORKLOG was generated *from* git and committed *back into* it — circular
    duplication, retired in v3.17; `orient-and-reconciliation-are-the-corpus-two-
    sides`). Sessions are delimited by `session-end:` commits; the narrative detail
    is the commit messages themselves. Default prints to stdout; `--write` saves a
    local (gitignored) snapshot. CHANGELOG stays the external per-version record."""
    root = Path(args.path).resolve()
    # Identity comes from the repo this runs in, not hard-coded framework values:
    # the WORKLOG is generated in the framework and in domain repos alike. Read the
    # local AGENTS.md frontmatter for the system name; fall back to the folder name.
    name = root.name
    agents = root / "AGENTS.md"
    if agents.is_file():
        ameta, _b, _e = parse_frontmatter(agents.read_text(encoding="utf-8"))
        if isinstance(ameta, dict) and isinstance(ameta.get("name"), str) and ameta["name"].strip():
            name = ameta["name"].strip()
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")
    worklog_id = f"{slug}-worklog" if slug else "worklog"
    fmt = "%H%x1f%ad%x1f%s"
    # Decode git output as UTF-8 explicitly: text=True would use the locale
    # codepage (cp1252 on Windows), which mangles em-dashes in commit subjects.
    out = subprocess.run(["git", "log", "--reverse", "--date=short",
                          f"--format={fmt}", "HEAD"], cwd=root,
                         capture_output=True, encoding="utf-8", errors="replace",
                         check=True).stdout
    commits = [tuple(line.split("\x1f", 2)) for line in out.strip().splitlines() if line]
    if not commits:
        print("mdllm: no commits — nothing to generate")
        return 0

    sessions: list[list[tuple]] = []
    cur: list[tuple] = []
    for c in commits:
        cur.append(c)
        if c[2].startswith("session-end"):
            sessions.append(cur)
            cur = []
    if cur:
        sessions.append(cur)

    # Auto-link to a local manifesto thing if the repo has one (the framework
    # does; most domains don't). Hard-coding a framework-only id here would
    # dangle — and fail validation as an unknown reference — in a domain repo.
    corpus, _ = scan(root)
    manifesto = next((t.id for t in corpus.things
                      if str(t.meta.get("type")) == "manifesto" and t.id), None)

    L = ["---", f"id: {worklog_id}", "type: artifact", "status: evolving",
         f"created: {commits[0][1]}"]
    if manifesto:
        L += ["linked_things:", f"  - id: {manifesto}", "    relation: documents"]
    L += ["---", "",
          f"# {name} Work Log", "",
          "> An on-demand view of the commit stream (`mdllm worklog`) — NOT committed.",
          "> Sessions are delimited by `session-end:` commits; full detail is in `git log`.",
          ""]
    for sess in reversed(sessions):
        first_d, last_d = sess[0][1], sess[-1][1]
        closed = sess[-1][2].startswith("session-end")
        title = sess[-1][2] if closed else "in progress"
        label = first_d if first_d == last_d else f"{first_d} → {last_d}"
        L += [f"## {label} — {title}", ""]
        for h, _d, s in (sess[:-1] if closed else sess):
            L.append(f"- `{h[:9]}` {s}")
        L.append("")
    content = "\n".join(L).rstrip() + "\n"
    if args.write:
        (root / "WORKLOG.md").write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote WORKLOG.md — {len(sessions)} sessions from {len(commits)} commits")
    else:
        print(content)
    return 0
