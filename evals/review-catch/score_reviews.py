"""Score review-catch result files against the frozen set. See README.md.

Standard library only. Prints markdown.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
from pathlib import Path

HIT_WIDEN = 5
NEAR_LINES = 30


def lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def norm_path(p: str) -> str:
    p = (p or "").strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def gap(ls: int, le: int, a: int, b: int) -> int:
    """Lines between finding range [ls, le] and defect range [a, b]; 0 if they overlap."""
    lo, hi = min(ls, le), max(ls, le)
    return max(0, a - hi, lo - b)


def classify(finding: dict, defect: dict) -> str:
    """'hit' (same file, range widened by 5 overlaps), 'near' (same file within 30), or 'miss'."""
    if norm_path(finding.get("file", "")) != norm_path(defect["file"]):
        return "miss"
    g = min(gap(finding["line_start"], finding["line_end"], a, b) for a, b in defect["ranges"])
    if g <= HIT_WIDEN:
        return "hit"
    if g <= NEAR_LINES:
        return "near"
    return "miss"


def majority(hits: int, trials: int) -> bool:
    return trials > 0 and hits * 2 > trials


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p on the discordant counts b, c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def near_key(set_sha: str, result_sha: str, entry: str, fi: int, di: int) -> str:
    return hashlib.sha256(f"{set_sha}|{result_sha}|{entry}|{fi}|{di}".encode()).hexdigest()[:12]


# ---------------------------------------------------------------- loading

def load_results(paths: list[str], set_sha: str) -> tuple[dict, list[str]]:
    """Group usable result files by (arm, model, prompt sha). Returns (groups, skipped notes)."""
    files: list[Path] = []
    for p in paths:
        q = Path(p)
        files.extend(sorted(q.glob("*.json")) if q.is_dir() else [q])
    groups: dict = {}
    skipped = []
    for f in files:
        try:
            data_bytes = f.read_bytes()
            r = json.loads(data_bytes.decode("utf-8", errors="replace"))
        except (OSError, ValueError) as exc:
            skipped.append(f"{f.name}: unreadable ({exc})")
            continue
        if not isinstance(r, dict) or "arm" not in r or "reviews" not in r:
            skipped.append(f"{f.name}: not a review-catch result")
            continue
        if not r.get("complete"):
            skipped.append(f"{f.name}: incomplete ({r.get('stopped') or 'complete is false'})")
            continue
        if r.get("set_sha256") != set_sha:
            skipped.append(f"{f.name}: set sha256 {str(r.get('set_sha256'))[:12]} != {set_sha[:12]}")
            continue
        key = (r["arm"], r.get("model_requested"), str(r.get("prompt_sha256")))
        g = groups.setdefault(key, {})
        if r.get("trial") in g:
            skipped.append(f"{f.name}: duplicate trial {r.get('trial')} for {label(key)} "
                           f"(kept {g[r['trial']]['_file']})")
            continue
        r["_file"] = f.name
        r["_sha"] = hashlib.sha256(data_bytes).hexdigest()
        g[r["trial"]] = r
    return groups, skipped


def label(key: tuple) -> str:
    arm, model, psha = key
    return f"{arm} / {model} / prompt {psha[:8]}"


# ---------------------------------------------------------------- scoring

def defects_of(set_data: dict) -> list[dict]:
    out = []
    for e in set_data["entries"]:
        for i, d in enumerate(e.get("defects") or []):
            out.append({"id": f"{e['id']}#{i}", "entry": e["id"], "index": i, **d})
    return out


def score_group(set_data: dict, set_sha: str, trials: dict, rulings: dict) -> dict:
    """Per trial, per defect: caught or not. Near misses collected for ruling."""
    entries = {e["id"]: e for e in set_data["entries"]}
    defects = defects_of(set_data)
    per_trial = {}
    near = []
    warnings = []
    for t, r in sorted(trials.items()):
        reviews = {rv["entry"]: rv for rv in r["reviews"]}
        missing = [e for e in entries if e not in reviews]
        if missing:
            warnings.append(f"trial {t} ({r['_file']}) did not review {len(missing)} entries; "
                            "their defects count as not caught")
        caught = {}
        for d in defects:
            rv = reviews.get(d["entry"])
            hit = False
            for fi, f in enumerate((rv or {}).get("findings") or []):
                c = classify(f, d)
                if c == "near":
                    k = near_key(set_sha, r["_sha"], d["entry"], fi, d["index"])
                    ruling = rulings.get(k)
                    if ruling == "hit":
                        c = "hit"
                    elif ruling is None:
                        near.append({"key": k, "claim": f["claim"], "file": norm_path(f["file"]),
                                     "finding_lines": [f["line_start"], f["line_end"]],
                                     "defect_file": norm_path(d["file"]), "defect_lines": d["ranges"],
                                     "_where": {"result": r["_file"], "arm": r["arm"],
                                                "model": r.get("model_requested"), "trial": t,
                                                "entry": d["entry"], "finding": fi, "defect": d["id"]}})
                if c == "hit":
                    hit = True
            caught[d["id"]] = hit
        items = [e for e in entries.values() if e["kind"] == "item"]
        controls = [e for e in entries.values() if e["kind"] == "control"]
        nf = lambda e: len((reviews.get(e["id"]) or {}).get("findings") or [])
        per_trial[t] = {
            "caught": caught,
            "findings_per_entry": (sum(nf(e) for e in entries.values()) / len(entries)) if entries else 0,
            "findings_per_item": (sum(nf(e) for e in items) / len(items)) if items else 0,
            "controls_flagged": (sum(1 for e in controls if nf(e) > 0) / len(controls)) if controls else None,
            "findings_per_control": (sum(nf(e) for e in controls) / len(controls)) if controls else None,
            "void": sum(1 for rv in r["reviews"] if rv.get("void")),
        }
    n = len(per_trial)
    freq = {d["id"]: sum(1 for pt in per_trial.values() if pt["caught"][d["id"]]) for d in defects}
    maj = {d: majority(c, n) for d, c in freq.items()}
    return {"defects": defects, "per_trial": per_trial, "freq": freq, "majority": maj,
            "trials": n, "near": near, "warnings": warnings}


def _rate(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.1%}"


def report_group(key: tuple, s: dict) -> list[str]:
    defects, n = s["defects"], s["trials"]
    out = [f"## {label(key)}", "", f"Trials: {n}. Defects: {len(defects)}.", ""]
    for w in s["warnings"]:
        out.append(f"- warning: {w}")
    out += ["", "| trial | catch rate | review/codex-found | other | findings/entry | "
            "controls with ≥1 finding | findings/control | void |",
            "|---|---|---|---|---|---|---|---|"]
    rc = [d for d in defects if {"review", "codex"} & set(d.get("found_by_keywords") or [])]
    other = [d for d in defects if d not in rc]
    for t, pt in sorted(s["per_trial"].items()):
        c = pt["caught"]
        rate = lambda ds: (sum(c[d["id"]] for d in ds) / len(ds)) if ds else None
        fpc = pt["findings_per_control"]
        fpc_s = "n/a" if fpc is None else f"{fpc:.2f}"
        out.append(f"| {t} | {_rate(rate(defects))} ({sum(c.values())}/{len(defects)}) | "
                   f"{_rate(rate(rc))} | {_rate(rate(other))} | {pt['findings_per_entry']:.2f} | "
                   f"{_rate(pt['controls_flagged'])} | {fpc_s} | {pt['void']} |")
    pooled = lambda ds: (sum(s["freq"][d["id"]] for d in ds) / (len(ds) * n)) if ds and n else None
    out += ["", f"Pooled catch rate: {_rate(pooled(defects))}; review/codex-found defects "
            f"({len(rc)}): {_rate(pooled(rc))}; other ({len(other)}): {_rate(pooled(other))}.",
            f"Defects caught in a majority of trials: "
            f"{sum(s['majority'].values())}/{len(defects)} "
            f"({_rate(sum(s['majority'].values()) / len(defects) if defects else None)}).", "",
            "| defect | file | lines | keywords | caught/trials |", "|---|---|---|---|---|"]
    for d in defects:
        out.append(f"| {d['id']} | {d['file']} | {d['ranges']} | "
                   f"{','.join(d.get('found_by_keywords') or [])} | {s['freq'][d['id']]}/{n} |")
    out.append("")
    return out


def paired(ka: tuple, sa: dict, kb: tuple, sb: dict) -> list[str]:
    ids = [d["id"] for d in sa["defects"]]
    a = b = both = neither = 0
    for i in ids:
        x, y = sa["majority"][i], sb["majority"][i]
        both += x and y
        a += x and not y
        b += y and not x
        neither += not x and not y
    n = len(ids)
    return [f"### {label(ka)}  vs  {label(kb)}", "",
            "| A only | B only | both | neither | union catch rate | exact McNemar p |",
            "|---|---|---|---|---|---|",
            f"| {a} | {b} | {both} | {neither} | {_rate((a + b + both) / n if n else None)} | "
            f"{mcnemar_exact(a, b):.4g} |", ""]


def read_rulings(path: Path | None) -> dict:
    if not path:
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^`?([0-9a-f]{12})`?\s*:\s*(hit|miss)\s*$", line, re.I)
        if not m:
            raise ValueError(f"bad ruling line: {line!r} (want 'key: hit|miss')")
        out[m.group(1).lower()] = m.group(2).lower()
    return out


def emit_near(path: Path, near: list[dict], set_sha: str) -> None:
    items = list(near)
    random.Random(set_sha).shuffle(items)
    lines = ["# Near misses to rule on", "",
             "For each, decide whether the finding names the defect. Copy the ruling lines into a",
             "rulings file as `key: hit` or `key: miss` and pass it with --near-rulings.", ""]
    for it in items:
        lines += [f"## {it['key']}", "",
                  f"- finding: `{it['file']}` lines {it['finding_lines'][0]}-{it['finding_lines'][1]}",
                  f"- claim: {it['claim']}",
                  f"- defect: `{it['defect_file']}` lines {it['defect_lines']}", "",
                  f"    {it['key']}: ", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    key_path = path.with_name(path.stem + ".key.json")
    key_path.write_text(json.dumps({it["key"]: it["_where"] for it in items}, indent=2),
                        encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--set", required=True)
    ap.add_argument("--results", required=True, nargs="+", help="result files or directories")
    ap.add_argument("--near-rulings", default=None)
    ap.add_argument("--emit-near", default=None)
    args = ap.parse_args(argv)
    set_bytes = lf_bytes(Path(args.set))
    set_sha = hashlib.sha256(set_bytes).hexdigest()
    set_data = json.loads(set_bytes.decode("utf-8", errors="replace"))
    groups, skipped = load_results(args.results, set_sha)
    rulings = read_rulings(Path(args.near_rulings) if args.near_rulings else None)
    out = [f"# Review-catch score — set {set_sha[:12]} (repo_head {str(set_data.get('repo_head'))[:12]})", ""]
    if skipped:
        out += ["Skipped result files:", ""] + [f"- {s}" for s in skipped] + [""]
    arm_prompts: dict = {}
    for arm, _, psha in groups:
        arm_prompts.setdefault(arm, set()).add(psha)
    for arm, ps in arm_prompts.items():
        if len(ps) > 1:
            out.append(f"- note: arm {arm} has {len(ps)} prompt hashes; they are reported separately, never pooled")
    scores = {k: score_group(set_data, set_sha, v, rulings) for k, v in sorted(groups.items(),
                                                                               key=lambda kv: str(kv[0]))}
    if not scores:
        out.append("No usable result files.")
    for k, s in scores.items():
        out += report_group(k, s)
    keys = list(scores)
    if len(keys) >= 2:
        out += ["## Paired (majority-of-trials catch)", ""]
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                out += paired(keys[i], scores[keys[i]], keys[j], scores[keys[j]])
    near = [n for s in scores.values() for n in s["near"]]
    out.append(f"Unruled near misses: {len(near)}" + (f"; {len(rulings)} rulings applied" if rulings else ""))
    if args.emit_near:
        emit_near(Path(args.emit_near), near, set_sha)
        out.append(f"Near misses written to {args.emit_near} (key file beside it).")
    sys.stdout.buffer.write(("\n".join(out) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
