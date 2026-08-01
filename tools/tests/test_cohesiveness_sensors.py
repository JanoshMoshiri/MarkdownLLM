"""Self-tests for the cohesiveness sensors (cohesiveness-sensors plan, Phase 2).

Each sensor watches a definition surface for divergence from usage — the
self-describing axis. These tests pin: structural trigger completeness,
quarantine age, retrospective cadence, template residue, and index anchor
integrity. Run: python -m pytest tools/tests -q
"""

import datetime as dt
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402

from test_mdllm import thing_text, write, all_findings, messages  # noqa: E402


# ------------------------------------------------- trigger completeness


def test_relationship_trigger_with_nothing_to_key_on_warns(tmp_path):
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: relationship
    action: chase it
"""))
    msgs = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert any("can never fire" in m for m in msgs)


def test_relationship_trigger_complete_is_quiet(tmp_path):
    write(tmp_path, "things/b.md", thing_text("""\
id: b
type: task
status: in-progress
created: 2026-06-01
"""))
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: relationship
    on: status_changed
    watch: [b]
    action: chase it
"""))
    msgs = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert not any("can never fire" in m for m in msgs)


def test_relationship_trigger_with_condition_prose_is_quiet(tmp_path):
    # Watching the world rather than a thing (condition prose, no watch) is a
    # legitimate observed pattern — the agent judges it; no warning.
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: relationship
    on: external_decision
    condition: "A CR is raised against the coding scheme"
    action: fold it in
"""))
    msgs = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert not any("never fire" in m for m in msgs)


def test_yaml_on_key_normalized_and_dependency_fires(tmp_path):
    # YAML 1.1 parses a bare `on:` key as boolean True; before normalization
    # this made every dependency trigger silently unfireable.
    write(tmp_path, "things/b.md", thing_text("""\
id: b
type: task
status: completed
created: 2026-06-01
"""))
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: dependency
    on: status_changed_to
    watch: [b]
    value: completed
    action: start the next phase
"""))
    meta, _, _ = mdllm.parse_frontmatter((tmp_path / "things/a.md").read_text(encoding="utf-8"))
    assert meta["triggers"][0].get("on") == "status_changed_to"
    hits, _, _ = mdllm.evaluate(tmp_path)
    assert any("all watched (b) are `completed`" in h for h in hits)


def test_shapeless_dependency_trigger_is_skipped_not_silent(tmp_path):
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: dependency
    action: unblock
"""))
    _, _, skipped = mdllm.evaluate(tmp_path)
    assert any("never fires as declared" in s for s in skipped)


def test_dependency_trigger_without_watch_value_warns(tmp_path):
    write(tmp_path, "things/a.md", thing_text("""\
id: a
type: task
status: in-progress
created: 2026-06-01
triggers:
  - type: dependency
    action: unblock
"""))
    msgs = messages(all_findings(tmp_path), mdllm.SEV_WARNING)
    assert any("can never fire" in m for m in msgs)


# ------------------------------------------------- quarantine age


def _corpus(root):
    corpus, _ = mdllm.scan(root)
    return corpus


def test_external_unverified_over_30d_is_info(tmp_path):
    old = (dt.date.today() - dt.timedelta(days=45)).isoformat()
    write(tmp_path, "things/x.md", thing_text(f"""\
id: x
type: task
status: in-progress
created: {old}
origin: external
verified: false
"""))
    found = mdllm.quarantine_findings(tmp_path, _corpus(tmp_path))
    infos = [f for f in found if f.severity == mdllm.SEV_INFO]
    assert any("unverified for 45 days" in f.message for f in infos)


def test_external_unverified_under_30d_is_quiet(tmp_path):
    recent = (dt.date.today() - dt.timedelta(days=10)).isoformat()
    write(tmp_path, "things/x.md", thing_text(f"""\
id: x
type: task
status: in-progress
created: {recent}
origin: external
verified: false
"""))
    found = mdllm.quarantine_findings(tmp_path, _corpus(tmp_path))
    assert not [f for f in found if f.severity == mdllm.SEV_INFO]


# ------------------------------------------------- retrospective cadence


def _git(root, *args, date=None):
    env = None
    if date:
        import os
        env = dict(os.environ, GIT_AUTHOR_DATE=f"{date}T12:00:00",
                   GIT_COMMITTER_DATE=f"{date}T12:00:00")
    subprocess.run(["git", *args], cwd=root, check=True,
                   capture_output=True, env=env)


def _aged_active_repo(tmp_path):
    """A repo whose things/ history began 100 days ago and committed 5 days
    ago — old enough and active enough for the cadence check to apply."""
    born = (dt.date.today() - dt.timedelta(days=100)).isoformat()
    recent = (dt.date.today() - dt.timedelta(days=5)).isoformat()
    write(tmp_path, "things/a.md", thing_text(f"""\
id: a
type: task
status: in-progress
created: {born}
"""))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "create: a", date=born)
    write(tmp_path, "things/b.md", thing_text(f"""\
id: b
type: task
status: in-progress
created: {recent}
"""))
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "create: b", date=recent)


def test_no_retrospective_in_active_old_domain_is_info(tmp_path):
    _aged_active_repo(tmp_path)
    found = mdllm.retrospective_findings(tmp_path, _corpus(tmp_path))
    assert len(found) == 1 and found[0].severity == mdllm.SEV_INFO
    assert "no retrospective has ever been written" in found[0].message


def test_recent_retrospective_is_quiet(tmp_path):
    _aged_active_repo(tmp_path)
    recent = (dt.date.today() - dt.timedelta(days=20)).isoformat()
    write(tmp_path, "things/retrospectives/r.md", thing_text(f"""\
id: r
type: retrospective
status: complete
created: {recent}
"""))
    assert mdllm.retrospective_findings(tmp_path, _corpus(tmp_path)) == []


def test_young_domain_is_quiet(tmp_path):
    recent = (dt.date.today() - dt.timedelta(days=5)).isoformat()
    write(tmp_path, "things/a.md", thing_text(f"""\
id: a
type: task
status: in-progress
created: {recent}
"""))
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "create: a", date=recent)
    assert mdllm.retrospective_findings(tmp_path, _corpus(tmp_path)) == []


# ------------------------------------------------- template residue


def _fake_framework(tmp_path):
    fw = tmp_path / "fw"
    write(fw, ".markdownllm", "framework: MarkdownLLM\nversion: 9.9.9\n")
    write(fw, "templates/domain-read.thing.skill.md.template", """\
---
id: [domain]-read-thing-skill
type: skill
status: draft
created: [ISO-date]
---

# Read Skill

[List and briefly describe the main thing types you instantiate]
[If your domain uses specialized reasoning frameworks, document them here]
[Walk through a concrete example]
""")
    write(fw, "templates/AGENTS.md.template", """\
---
framework_root: [framework-root]
---
# [Domain Name]

[1-2 sentences: the vision and primary capability of this domain]
[List and briefly describe the main thing types]
[Describe the principles]
""")
    return fw


def test_stub_skill_flagged(tmp_path):
    _fake_framework(tmp_path)
    dom = tmp_path / "dom"
    write(dom, "AGENTS.md", "---\nframework_root: ../fw\n---\n# Dom\n")
    write(dom, "skills/dom-read.thing.skill.md", thing_text("""\
id: dom-read-thing-skill
type: skill
status: draft
created: 2026-06-01
""", body="""\
# Read Skill

[List and briefly describe the main thing types you instantiate]
[If your domain uses specialized reasoning frameworks, document them here]
[Walk through a concrete example]
"""))
    found = mdllm.coherence_findings(dom, 15)
    assert any("scaffolded, never authored" in f.message for f in found
               if f.severity == mdllm.SEV_INFO)


def test_authored_skill_with_incidental_bracket_is_quiet(tmp_path):
    _fake_framework(tmp_path)
    dom = tmp_path / "dom"
    write(dom, "AGENTS.md", "---\nframework_root: ../fw\n---\n# Dom\n"
                            "Real principles, fully authored entry file.\n")
    write(dom, "skills/dom-read.thing.skill.md", thing_text("""\
id: dom-read-thing-skill
type: skill
status: stable
created: 2026-06-01
""", body="""\
# Read Skill

Fully authored content with one legitimate example template the skill
provides to its own users: [Walk through a concrete example] is quoted here
as an illustration, not residue.
"""))
    found = mdllm.coherence_findings(dom, 15)
    assert not any("scaffolded, never authored" in f.message for f in found)


def test_unfilled_agents_md_flagged(tmp_path):
    _fake_framework(tmp_path)
    dom = tmp_path / "dom"
    write(dom, "AGENTS.md", """\
---
framework_root: ../fw
---
# Dom

[1-2 sentences: the vision and primary capability of this domain]
[List and briefly describe the main thing types]
[Describe the principles]
""")
    found = mdllm.coherence_findings(dom, 15)
    assert any(f.thing == "AGENTS.md" and "never authored" in f.message
               for f in found)


# ------------------------------------------------- index anchor integrity


def test_index_dangling_anchor_warns(tmp_path):
    write(tmp_path, ".markdownllm", "framework: MarkdownLLM\nversion: 9.9.9\n")
    write(tmp_path, "things/_index/schema.md", """\
---
id: t-schema-index
type: index
status: live
index_of: schema
created: 2026-06-01
generated: 2026-06-01T00:00:00
generated_from: HEAD@deadbeef1
coverage: 0
framework_version: 1.0.0
---

# Schema Registry — t

| field | things using it |
|---|---|
""")
    _git(tmp_path, "init", "-q")
    corpus = _corpus(tmp_path)
    found = mdllm.index_drift_findings(tmp_path, corpus)
    warnings = [f.message for f in found if f.severity == mdllm.SEV_WARNING]
    assert any("no longer resolves" in m for m in warnings)
    assert any("stamped at framework 1.0.0" in m for m in warnings)
