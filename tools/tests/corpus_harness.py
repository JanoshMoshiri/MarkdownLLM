"""Shared corpus-construction and CLI-invocation harness for floor tests.

Extracted from test_mdllm.py (floor-structure-residue item 4, sprint 2) so
the monolith can be decomposed: every test file builds corpora, invokes the
CLI, and reads findings through these helpers instead of importing them from
another test file.
"""

import datetime as _dt
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Fixtures that age must be dated RELATIVE to the run, never literally.
# Several floor sensors key on elapsed time — quarantine fires an Info at
# >30 days unverified — so a hardcoded `created` turns any "no findings"
# assertion into a time bomb: green in review, red in CI weeks later with a
# diff that implicates the code rather than the fixture. One did exactly
# that on 2026-08-16, thirty-one days after the date it was written with.
RECENT = (_dt.date.today() - _dt.timedelta(days=1)).isoformat()

import mdllm  # noqa: E402

# Tests that commit (scaffold's nested repo, hook execution) must not depend
# on the machine's global git identity — CI runners and sandboxes have none.
# (portability-claims-need-execution-tests, applied to the test suite itself.)
for _k in ("GIT_AUTHOR_NAME", "GIT_COMMITTER_NAME"):
    os.environ.setdefault(_k, "floor-tests")
for _k in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL"):
    os.environ.setdefault(_k, "floor-tests@local")


def _git_supports_hook_run() -> bool:
    import re as _re
    import subprocess as _sp
    out = _sp.run(["git", "--version"], capture_output=True, text=True)
    m = _re.search(r"(\d+)\.(\d+)", out.stdout or "")
    return bool(m) and (int(m.group(1)), int(m.group(2))) >= (2, 36)


def thing_text(fm: str, body: str = "# Title\n\nBody text.\n") -> str:
    return f"---\n{fm.strip()}\n---\n\n{body}"


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def scan(root: Path):
    corpus, findings = mdllm.scan(root)
    return corpus, findings


def all_findings(root: Path):
    corpus, findings = scan(root)
    for t in corpus.things:
        findings.extend(mdllm.validate_level1(t, corpus.schema))
    findings.extend(mdllm.validate_level2(corpus))
    findings.extend(mdllm.validate_level3(corpus))
    return findings


def messages(findings, severity=None):
    return [f.message for f in findings if severity in (None, f.severity)]


GOOD = """\
id: alpha
type: task
status: in-progress
created: 2026-06-01
"""


def _ns(**kw):
    from types import SimpleNamespace
    return SimpleNamespace(**kw)


def _git_repo(tmp_path):
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)


def _git_commit(root, msg):
    import subprocess as sp
    sp.run(["git", "add", "-A"], cwd=root, check=True)
    sp.run(["git", "commit", "-q", "-m", msg], cwd=root, check=True)


def _git_short(root):
    import subprocess as sp
    return sp.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                  capture_output=True, text=True).stdout.strip()


def _sync_git(cwd, *args):
    import subprocess
    return subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                           *args], cwd=cwd, capture_output=True, text=True)
