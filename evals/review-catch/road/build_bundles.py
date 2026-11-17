"""Build the review-catch road's per-entry git bundles and their manifest.

Each entry of ../set.json gets one bundle holding exactly the entry commit and
its ancestry, advertised as HEAD and nothing else: no branch, no tag, no
remote. A reviewer who clones it sees the repository as it stood at that
commit and cannot reach the later fix.

Why HEAD and not a named ref: `git clone` of a bundle checks out the bundle's
HEAD and fetches only refs/heads/*, so a bundle of refs/review-catch-tmp/<id>
clones to an empty repository. The bundle is therefore cut from a throwaway
bare "shim" repository whose objects are borrowed from this repository
(objects/info/alternates) and whose only state is a detached HEAD at the
entry commit. This repository's refs are never touched.

Steps (Windows side; the leak check runs inside the distro):
  python build_bundles.py build [OUT_DIR]
      writes OUT_DIR/<id>.bundle and OUT_DIR/checks.tsv
      (id, commit, fix commits or "-", expected commit count)
  copy OUT_DIR to /srv/review-road/bundles/ in the review-road distro (root-only:
  dir 700, files 600; `run_reviews.py --install` resets those permissions),
  run leak_check.sh there, save its stdout as a results TSV, then
  python build_bundles.py manifest RESULTS_TSV [OUT_DIR]
      writes bundles.json next to this script

OUT_DIR defaults to %LOCALAPPDATA%/review-road/bundles.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SET = HERE.parent / "set.json"
REPO = HERE.parents[2]
MANIFEST = HERE / "bundles.json"
DEFAULT_OUT = Path(os.environ.get("LOCALAPPDATA", ".")) / "review-road" / "bundles"


def git(*args, git_dir=None):
    cmd = ["git"] + (["--git-dir", str(git_dir)] if git_dir else ["-C", str(REPO)])
    return subprocess.run(cmd + list(args), check=True, capture_output=True,
                          text=True).stdout.strip()


def entries():
    data = json.loads(SET.read_text(encoding="utf-8"))
    return sorted(data["entries"], key=lambda e: e["id"])


def fixes(entry):
    return sorted({d["fix"] for d in entry.get("defects", [])})


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    objects = (REPO / ".git" / "objects").as_posix()
    rows = []
    for e in entries():
        sha = git("rev-parse", "--verify", e["commit"] + "^{commit}")
        assert sha == e["commit"], (e["id"], sha)
        with tempfile.TemporaryDirectory() as tmp:
            shim = Path(tmp) / "shim.git"
            subprocess.run(["git", "init", "--bare", "--quiet", str(shim)], check=True)
            (shim / "objects" / "info" / "alternates").write_bytes(objects.encode() + b"\n")
            (shim / "HEAD").write_bytes(sha.encode() + b"\n")
            assert git("for-each-ref", git_dir=shim) == ""
            bundle = out / f"{e['id']}.bundle"
            git("bundle", "create", str(bundle), "HEAD", git_dir=shim)
        heads = git("bundle", "list-heads", str(bundle))
        assert heads == f"{sha} HEAD", (e["id"], heads)
        count = git("rev-list", "--count", sha)
        rows.append("\t".join([e["id"], sha, ",".join(fixes(e)) or "-", count]))
        print(e["id"], sha[:12], count, "commits", bundle.stat().st_size, "bytes")
    (out / "checks.tsv").write_bytes(("\n".join(rows) + "\n").encode())


def manifest(results_tsv, out):
    results = {}
    for line in Path(results_tsv).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rid, verdict, commits, digest, failures = (line.split("\t") + [""])[:5]
            results[rid] = (verdict, int(commits or 0), digest,
                            [f for f in failures.split("; ") if f])
    items = []
    for e in entries():
        verdict, commits, digest, failures = results.get(
            e["id"], ("fail", 0, "", ["no leak-check result"]))
        local = sha256(out / f"{e['id']}.bundle")
        if digest != local:
            failures = failures + ["bundle in distro differs from the one built"]
        items.append({"id": e["id"], "commit": e["commit"], "bundle_sha256": local,
                      "commits_in_bundle": commits,
                      "leak_check": "pass" if verdict == "pass" and not failures else "fail",
                      "failures": failures})
    set_sha = hashlib.sha256(SET.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    doc = {"set_sha256": set_sha, "bundles": items}
    MANIFEST.write_bytes((json.dumps(doc, indent=2) + "\n").encode())
    passed = sum(i["leak_check"] == "pass" for i in items)
    print(f"{passed}/{len(items)} passed; wrote {MANIFEST.name}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        build(Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUT)
    elif len(sys.argv) >= 3 and sys.argv[1] == "manifest":
        manifest(sys.argv[2], Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OUT)
    else:
        sys.exit(__doc__)
