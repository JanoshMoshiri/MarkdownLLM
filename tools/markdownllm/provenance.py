"""Provenance-chain checks (provenance.md).

Pinned commits must be reachable, pinned inputs present, external things
verified before anything rests on them; drift since a pin is surfaced as Info.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

from .model import Finding, SEV_ERROR, SEV_INFO, SEV_WARNING, scan

def cmd_provenance(args) -> int:
    """Mechanical checks for provenance chains (provenance.md)."""
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    by_id = corpus.by_id()
    findings: list[Finding] = []
    today = dt.date.today()

    def commit_exists(sha: str) -> bool:
        return subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                              cwd=root, capture_output=True).returncode == 0

    def exists_at(sha: str, thing_id: str) -> bool:
        out = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha],
                             cwd=root, capture_output=True, text=True)
        return out.returncode == 0 and any(
            p.endswith(f"{thing_id}.md") for p in out.stdout.splitlines())

    for t in corpus.things:
        name = t.id or t.path.name
        for i, pin in enumerate(t.meta.get("informed_by") or []):
            if not isinstance(pin, dict) or not pin.get("id") or not pin.get("commit"):
                findings.append(Finding(SEV_ERROR, name,
                                f"`informed_by[{i}]` must have `id` and `commit`"))
                continue
            pid, sha = str(pin["id"]), str(pin["commit"])
            src = by_id.get(pid)
            if not commit_exists(sha):
                # The pinned commit is not reachable in this repository. The tool
                # cannot know *why* — the history it referenced may have been
                # rewritten (rebase/squash/filter re-hashes every commit), or the
                # pin may never have been a valid commit here — so it reports only
                # the observable fact and never asserts a cause. Severity is
                # decided by whether the reasoning chain still holds: if the cited
                # input is present in the corpus the decision can still be traced,
                # so this is a non-blocking Warning to re-pin; only when the input
                # is *also* absent is the chain genuinely broken.
                if src is not None:
                    findings.append(Finding(SEV_WARNING, name,
                                    f"pinned commit `{sha}` for `{pid}` is not "
                                    f"reachable in this repository; the cited input "
                                    f"is still in the corpus — re-pin to a current "
                                    f"commit"))
                else:
                    findings.append(Finding(SEV_ERROR, name,
                                    f"pinned commit `{sha}` is not reachable and "
                                    f"input `{pid}` is not in the corpus — "
                                    f"provenance chain is broken"))
                continue
            if src is None and not exists_at(sha, pid):
                findings.append(Finding(SEV_ERROR, name,
                                f"pinned input `{pid}` not found (current corpus "
                                f"or at {sha})"))
            if src is not None:
                if (str(src.meta.get("origin")) == "external"
                        and src.meta.get("verified") is not True):
                    findings.append(Finding(SEV_ERROR, name,
                                    f"pins UNVERIFIED external thing `{pid}` — "
                                    f"quarantine rule violated"))
                rel = src.path.relative_to(root).as_posix()
                log = subprocess.run(["git", "log", "--oneline", f"{sha}..HEAD",
                                      "--", rel], cwd=root, capture_output=True,
                                     text=True)
                if log.returncode == 0 and log.stdout.strip():
                    n = len(log.stdout.strip().splitlines())
                    findings.append(Finding(SEV_INFO, name,
                                    f"input `{pid}` changed in {n} commit(s) since "
                                    f"pin {sha} — decision may be dated"))

        if str(t.meta.get("origin")) == "external" and t.meta.get("verified") is not True:
            created = t.meta.get("created")
            age = ""
            if isinstance(created, (dt.date, dt.datetime)):
                c = created.date() if isinstance(created, dt.datetime) else created
                days = (today - c).days
                age = f" ({days}d old)"
                sev = SEV_INFO if days > 30 else None
            else:
                sev = SEV_INFO
            if sev:
                findings.append(Finding(sev, t.id or t.path.name,
                                f"external thing still unverified{age}"))

    errors = [x for x in findings if x.severity == SEV_ERROR]
    print(f"## Provenance Report — {root}\n")
    if not findings:
        print("No provenance issues found.")
    for title, group in (("Errors", errors),
                         ("Warnings", [x for x in findings if x.severity == SEV_WARNING]),
                         ("Info", [x for x in findings if x.severity == SEV_INFO])):
        if group:
            print(f"### {title}")
            for x in group:
                print(f"- **{x.thing}**: {x.message}")
            print()
    return 1 if errors else 0
