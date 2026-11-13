#!/usr/bin/env python3
"""Mine the review-catch candidate set from this repo's own history.

Read-only on git. Standard library only.

Default run: writes candidates.json and candidates.md next to this file.
--freeze [--items N] --trim-controls [--set-out PATH] [--force]: reads
candidates.json, writes set.json (all items, or the first N by sha, each with
one size-matched control). frozen_at is printed, not stored, so the printed
sha256 depends only on the set's content.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SINCE = "2026-07-01"
SHARE_MIN = 0.60
SIZE_MIN = 10
SIZE_MAX = 600
SEED = 20261113
FIX_RE = re.compile(r"^fix(\(|:|\+|!| )", re.IGNORECASE)
LOOSE_FIX_RE = re.compile(r"^fix", re.IGNORECASE)
REFACTOR_RE = re.compile(r"^refactor", re.IGNORECASE)
KEYWORDS = ["review", "codex", "cold", "ci", "test", "smoke", "first", "live", "operator", "use"]
KW_RES = {k: re.compile(r"\b" + re.escape(k) + r"\b", re.IGNORECASE) for k in KEYWORDS}

RULES = {
    "fix_subject_regex": r"^fix(\(|:|\+|!| ) (case-insensitive)",
    "since_author_date": SINCE,
    "scope": "tools/**/*.py excluding tools/tests/",
    "blame": "git blame -M -C --porcelain -L <old ranges> F^ -- <file>",
    "filter_moved_lines": "an old-side line of F whose stripped text (non-empty) equals the stripped text of "
                          "any line F adds in any scope file is ignored before blame",
    "filter_blank_lines": "old-side lines that are blank or whitespace-only are ignored before blame",
    "filter_refactor": "an introducing commit whose subject matches ^refactor (case-insensitive) is rejected; "
                       "such commits are also excluded from controls",
    "min_share": SHARE_MIN,
    "changed_lines_min": SIZE_MIN,
    "changed_lines_max": SIZE_MAX,
    "changed_lines_basis": "added+removed vs first parent, --no-renames, scope files only",
    "controls": "subject not a fix (tight regex), not ^refactor, not a merge, in date and size range, "
                "zero blamed lines from any fix on the UNFILTERED tallies (before the moved/blank filters); "
                "items use the filtered tallies",
    "freeze_controls": "walk chosen items by ascending sha; each takes the unused control with the closest "
                       "changed_lines (ties: lower sha); one control per item",
    "keywords": KEYWORDS,
    "freeze_seed": SEED,
}


def git(*args, check=True):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace")))
    return p.stdout.decode("utf-8", errors="replace")


def repo_root():
    p = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.decode("utf-8", "replace").strip()


REPO = repo_root()


def in_scope(path):
    return path.startswith("tools/") and path.endswith(".py") and not path.startswith("tools/tests/")


def load_commits():
    """All commits reachable from HEAD with scope numstat vs their (single) parent."""
    out = git("log", "--no-renames", "--numstat", "--format=%x01%H%x02%P%x02%an%x02%ae%x02%aI%x02%s", "HEAD")
    commits = {}
    order = []
    for block in out.split("\x01")[1:]:
        head, _, rest = block.partition("\n")
        sha, parents, an, ae, date, subj = head.split("\x02", 5)
        parents = parents.split()
        files, changed = [], 0
        for line in rest.splitlines():
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            a, d, path = parts
            if not in_scope(path):
                continue
            files.append(path)
            if a != "-":
                changed += int(a)
            if d != "-":
                changed += int(d)
        commits[sha] = {
            "commit": sha, "parents": parents, "author_name": an, "author_email": ae,
            "date": date, "subject": subj, "files": sorted(set(files)), "changed_lines": changed,
        }
        order.append(sha)
    return commits, order


HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@")


def parse_diff(fix, path):
    """Return (removed [(old_line_no, text)], added [text], pure_addition_hunks)."""
    out = git("diff", "--no-renames", "-U0", fix + "^", fix, "--", path)
    removed, added, pure = [], [], 0
    old_no = None
    in_hunk = False
    for line in out.split("\n"):
        m = HUNK_RE.match(line)
        if m:
            in_hunk = True
            old_no = int(m.group(1))
            if (1 if m.group(2) is None else int(m.group(2))) == 0:
                pure += 1
            continue
        if not in_hunk:
            continue
        if line.startswith("-"):
            removed.append((old_no, line[1:]))
            old_no += 1
        elif line.startswith("+"):
            added.append(line[1:])
    return removed, added, pure


def blame_lines(fix, path, ranges):
    """Return [(sha, orig_path, orig_line, final_line)] for every blamed line."""
    args = ["blame", "-M", "-C", "--porcelain"]
    for a, b in ranges:
        args += ["-L", "%d,%d" % (a, b)]
    args += [fix + "^", "--", path]
    out = git(*args)
    result = []
    cur_sha = cur_orig = cur_final = cur_file = None
    last_file = {}
    for line in out.split("\n"):
        if line.startswith("\t"):
            result.append((cur_sha, cur_file, cur_orig, cur_final))
            continue
        parts = line.split(" ")
        if len(parts) in (3, 4) and re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            cur_sha, cur_orig, cur_final = parts[0], int(parts[1]), int(parts[2])
            cur_file = last_file.get(cur_sha)  # 3-field header continues a group
            continue
        if line.startswith("filename "):
            cur_file = line[len("filename "):]
            last_file[cur_sha] = cur_file
    return result


def merge_ranges(lines):
    lines = sorted(set(lines))
    out = []
    for n in lines:
        if out and n <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], n)
        else:
            out.append([n, n])
    return out


def parse_date(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def record(c, kind, defects):
    # No author fields: who wrote a commit is read from git by its id when a
    # report needs it, and is never copied into a published file.
    return {
        "commit": c["commit"],
        "date": c["date"], "subject": c["subject"][:140], "files": c["files"],
        "changed_lines": c["changed_lines"], "kind": kind, "defects": defects,
    }


def match_controls(items, controls):
    """Greedy size match: items by ascending sha, closest unused control, ties lower sha.

    Greedy in a fixed order, so the pairing for the first N items is a prefix
    of the pairing for all items."""
    pool = sorted(controls, key=lambda e: e["commit"])
    used = set()
    pairs = []
    for it in sorted(items, key=lambda e: e["commit"]):
        best = None
        for c in pool:
            if c["commit"] in used:
                continue
            key = (abs(c["changed_lines"] - it["changed_lines"]), c["commit"])
            if best is None or key < best[0]:
                best = (key, c)
        if best is None:
            raise SystemExit("not enough controls to match %d items" % len(items))
        used.add(best[1]["commit"])
        pairs.append((it, best[1]))
    return pairs


def mine():
    head = git("rev-parse", "HEAD").strip()
    commits, order = load_commits()
    since_ok = lambda c: c["date"][:10] >= SINCE

    fixes, merges_skipped, dropped_by_subject = [], 0, []
    for sha in order:
        c = commits[sha]
        if not since_ok(c):
            continue
        if LOOSE_FIX_RE.match(c["subject"]) and not FIX_RE.match(c["subject"]):
            dropped_by_subject.append({"commit": sha, "subject": c["subject"][:140],
                                       "touches_scope": bool(c["files"])})
            continue
        if not FIX_RE.match(c["subject"]) or not c["files"]:
            continue
        if len(c["parents"]) > 1:
            merges_skipped += 1
            continue
        if len(c["parents"]) == 0:
            continue
        fixes.append(sha)

    blamed_any = set()  # unfiltered: any line of any fix, before the moved/blank filters
    rejected = []
    entries = {}
    stats = Counter()
    for f in fixes:
        fc = commits[f]
        per_file = {}
        added_all = set()
        for path in fc["files"]:
            removed, added, pure = parse_diff(f, path)
            per_file[path] = removed
            added_all.update(t.strip() for t in added if t.strip())
            stats["pure_addition_hunks"] += pure
        old_total = ign_moved = ign_blank = 0
        lines = []
        for path, removed in per_file.items():
            keep = []
            if removed:
                # blame every old-side line once; a line's blame does not depend
                # on which other -L ranges are asked for, so filter afterwards
                raw = blame_lines(f, path, [tuple(r) for r in merge_ranges([n for n, _ in removed])])
                blamed_any.update(b[0] for b in raw)
            for no, text in removed:
                old_total += 1
                s = text.strip()
                if not s:
                    ign_blank += 1
                elif s in added_all:
                    ign_moved += 1
                else:
                    keep.append(no)
            if keep:
                stats["blamed_ranges"] += len(merge_ranges(keep))
                ks = set(keep)
                lines += [b[:3] for b in raw if b[3] in ks]
        stats["old_side_lines"] += old_total
        stats["ignored_moved"] += ign_moved
        stats["ignored_blank"] += ign_blank
        filt = {"old_side_lines": old_total, "ignored_moved": ign_moved, "ignored_blank": ign_blank,
                "blamed_lines": len(lines)}
        tally = Counter(sha for sha, _, _ in lines)

        def reject(reason):
            rejected.append({"fix": f, "subject": fc["subject"][:140], "reason": reason, **filt})

        if old_total == 0:
            reject("no blamed lines (pure additions)")
            continue
        if not lines:
            reject("only moved or blank lines")
            continue
        top, n = tally.most_common(1)[0]
        share = n / len(lines)
        if share < SHARE_MIN:
            reject("no commit holds >= 60% of blamed lines")
            continue
        c = commits.get(top)
        if c is None:
            reject("introducing commit not reachable from HEAD")
            continue
        if top == f:
            reject("introducing commit is the fix itself")
            continue
        if not since_ok(c):
            reject("introducing commit before 2026-07-01")
            continue
        if len(c["parents"]) == 0:
            reject("introducing commit is a root commit")
            continue
        if len(c["parents"]) > 1:
            reject("introducing commit is a merge")
            continue
        if REFACTOR_RE.match(c["subject"]):
            reject("introducing commit is a refactor")
            continue
        if not (SIZE_MIN <= c["changed_lines"] <= SIZE_MAX):
            reject("introducing commit size outside 10..600 changed lines")
            continue
        msg = git("log", "-1", "--format=%B", f)
        kws = [k for k in KEYWORDS if KW_RES[k].search(msg)]
        by_file = defaultdict(list)
        for sha, opath, oline in lines:
            if sha == top:
                by_file[opath].append(oline)
        days = (parse_date(fc["date"]) - parse_date(c["date"])).total_seconds() / 86400
        e = entries.setdefault(top, record(c, "item", []))
        for opath in sorted(by_file, key=lambda p: (p is None, p or "")):
            e["defects"].append({
                "fix": f, "fix_date": fc["date"], "fix_subject": fc["subject"][:140],
                "file": opath, "ranges": merge_ranges(by_file[opath]),
                "share": round(share, 4), "days_to_fix": round(days, 2),
                "found_by_keywords": kws, "fix_line_filter": filt,
            })

    controls = []
    for sha in order:
        c = commits[sha]
        if FIX_RE.match(c["subject"]) or REFACTOR_RE.match(c["subject"]):
            continue
        if not since_ok(c) or len(c["parents"]) != 1:
            continue
        if not (SIZE_MIN <= c["changed_lines"] <= SIZE_MAX):
            continue
        if sha in blamed_any:
            continue
        controls.append(record(c, "control", []))

    items = sorted(entries.values(), key=lambda e: e["commit"])
    controls.sort(key=lambda e: e["commit"])
    preview = [{"item": it["commit"], "item_changed_lines": it["changed_lines"],
                "control": co["commit"], "control_changed_lines": co["changed_lines"]}
               for it, co in match_controls(items, controls)] if len(controls) >= len(items) else []
    data = {
        "schema": 1, "repo_head": head,
        "mined_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "rules": RULES, "entries": items + controls, "rejected": rejected,
        "dropped_by_subject_match": dropped_by_subject,
        "freeze_preview": preview,
        "counts": {
            "fix_commits_considered": len(fixes), "fix_merges_skipped": merges_skipped,
            "dropped_by_subject_match": len(dropped_by_subject),
            "accepted_fixes": len(fixes) - len(rejected), "rejected_fixes": len(rejected),
            "items": len(items), "defects": sum(len(e["defects"]) for e in items),
            "controls": len(controls),
            "pure_addition_hunks": stats["pure_addition_hunks"],
            "old_side_lines": stats["old_side_lines"], "ignored_moved": stats["ignored_moved"],
            "ignored_blank": stats["ignored_blank"], "blamed_ranges": stats["blamed_ranges"],
        },
    }
    return data


def md_escape(s):
    return s.replace("|", "\\|")


def write_md(data, path):
    items = [e for e in data["entries"] if e["kind"] == "item"]
    controls = [e for e in data["entries"] if e["kind"] == "control"]
    cnt = data["counts"]
    L = ["# Review-catch candidates", "",
         "Repo head `%s`, mined %s." % (data["repo_head"], data["mined_at"]), "",
         "## Rules", ""]
    for k, v in data["rules"].items():
        L.append("- **%s**: %s" % (k, md_escape(", ".join(v) if isinstance(v, list) else str(v))))
    L += ["", "## Counts", ""]
    for k, v in cnt.items():
        L.append("- %s: %d" % (k, v))
    L += ["", "## Rejections", "", "| reason | count |", "|---|---|"]
    for r, n in Counter(x["reason"] for x in data["rejected"]).most_common():
        L.append("| %s | %d |" % (r, n))
    L += ["", "## What a --freeze would select today", "",
          "All items, each with its size-matched control (no set.json written).", "",
          "| item | item lines | control | control lines |", "|---|---|---|---|"]
    for p in data["freeze_preview"]:
        L.append("| `%s` | %d | `%s` | %d |" % (p["item"][:10], p["item_changed_lines"],
                                               p["control"][:10], p["control_changed_lines"]))
    L += ["", "## Items", "",
          "| commit | date | lines | subject | fix | file | ranges | share | days | moved/blank ignored | keywords |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in items:
        for i, d in enumerate(e["defects"]):
            head = ("`%s` | %s | %d | %s" % (e["commit"][:10], e["date"][:10],
                                              e["changed_lines"], md_escape(e["subject"][:80]))
                    if i == 0 else " | | |")
            flt = d["fix_line_filter"]
            L.append("| %s | `%s` %s | %s | %s | %.2f | %.1f | %d/%d | %s |" % (
                head, d["fix"][:10], md_escape(d["fix_subject"][:70]), d["file"],
                ", ".join("%d-%d" % tuple(r) for r in d["ranges"]), d["share"], d["days_to_fix"],
                flt["ignored_moved"], flt["ignored_blank"], ", ".join(d["found_by_keywords"])))
    L += ["", "## Controls", "", "| commit | date | lines | subject |", "|---|---|---|---|"]
    for e in controls:
        L.append("| `%s` | %s | %d | %s |" % (e["commit"][:10], e["date"][:10],
                                             e["changed_lines"], md_escape(e["subject"][:100])))
    L += ["", "## Rejected fixes", "", "| fix | reason | old-side | moved | blank | blamed |",
          "|---|---|---|---|---|---|"]
    for r in data["rejected"]:
        L.append("| `%s` | %s | %d | %d | %d | %d |" % (r["fix"][:10], r["reason"], r["old_side_lines"],
                                                       r["ignored_moved"], r["ignored_blank"], r["blamed_lines"]))
    L += ["", "## Dropped by the tighter fix-subject match", "", "| commit | touches scope | subject |",
          "|---|---|---|"]
    for d in data["dropped_by_subject_match"]:
        L.append("| `%s` | %s | %s |" % (d["commit"][:10], "yes" if d["touches_scope"] else "no",
                                         md_escape(d["subject"][:100])))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def freeze(n_items, force, out_path):
    if os.path.exists(out_path) and not force:
        sys.exit("set.json exists; pass --force to overwrite")
    with open(os.path.join(HERE, "candidates.json"), encoding="utf-8") as fh:
        cand = json.load(fh)
    items = sorted((e for e in cand["entries"] if e["kind"] == "item"), key=lambda e: e["commit"])
    controls = [e for e in cand["entries"] if e["kind"] == "control"]
    if n_items is not None:
        if n_items > len(items):
            sys.exit("asked for %d items; only %d available" % (n_items, len(items)))
        items = items[:n_items]
    pairs = match_controls(items, controls)
    chosen = [it for it, _ in pairs] + [co for _, co in pairs]
    order = list(range(len(chosen)))
    random.Random(SEED).shuffle(order)
    entries = []
    for new_idx, src in enumerate(order):
        entries.append({"id": "r%03d" % (new_idx + 1), **chosen[src]})
    keys = {tuple(e.keys()) for e in entries}
    if len(keys) != 1:
        sys.exit("internal error: entries do not share one key set: %r" % keys)
    data = {
        "schema": 1, "repo_head": cand["repo_head"],
        "selection": {"items": len(items), "controls": len(pairs),
                      "items_order": "sha ascending" + ("" if n_items is None else ", first %d" % n_items),
                      "controls": RULES["freeze_controls"], "id_shuffle_seed": SEED,
                      "candidates_mined_at": cand["mined_at"]},
        "entries": entries,
    }
    blob = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(blob)
    # frozen_at is printed, not stored, so the file's hash depends only on its content
    print("wrote %s (%d entries: %d items, %d controls)" % (out_path, len(entries), len(items), len(pairs)))
    print("frozen_at %s" % dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    print("sha256 %s" % hashlib.sha256(blob).hexdigest())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--items", type=int)
    ap.add_argument("--trim-controls", action="store_true",
                    help="required with --freeze: one size-matched control per item")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--set-out", default=os.path.join(HERE, "set.json"),
                    help="where --freeze writes the set (default: set.json next to this script)")
    a = ap.parse_args()
    if a.freeze:
        if not a.trim_controls:
            ap.error("--freeze needs --trim-controls")
        freeze(a.items, a.force, a.set_out)
        return
    data = mine()
    with open(os.path.join(HERE, "candidates.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    write_md(data, os.path.join(HERE, "candidates.md"))
    c = data["counts"]
    print("fixes considered %d (merges skipped %d, dropped by subject match %d): accepted %d, rejected %d"
          % (c["fix_commits_considered"], c["fix_merges_skipped"], c["dropped_by_subject_match"],
             c["accepted_fixes"], c["rejected_fixes"]))
    for r, n in Counter(x["reason"] for x in data["rejected"]).most_common():
        print("  rejected: %-60s %d" % (r, n))
    print("items %d (defects %d), controls %d; old-side lines %d, ignored moved %d, blank %d"
          % (c["items"], c["defects"], c["controls"], c["old_side_lines"], c["ignored_moved"], c["ignored_blank"]))


if __name__ == "__main__":
    main()
