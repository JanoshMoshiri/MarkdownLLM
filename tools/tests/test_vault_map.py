"""`mdllm vault-map` — the generated map folder beside a folder of domains.

What these pin: every structural reference field becomes a link (not only
`linked_things`), a target resolves to the owning domain first and is
*reported* when it cannot be placed, the open set is the digest's, the map
writes only its own folder and only its own files, and it refuses a place
where a repository would track it.

Run: python -m pytest tools/tests/test_vault_map.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from corpus_harness import (RECENT, _git_commit, _git_repo, _ns,  # noqa: E402
                            _sync_git, thing_text, write)
from markdownllm.vault_map import (DEFAULT_OUT, NOTE_MARK, VIEW_MARK,  # noqa: E402
                                   VaultMapRefused, build_vault_map,
                                   cmd_vault_map)

pytestmark = pytest.mark.gitfs

SHA = "0123456789abcdef0123456789abcdef01234567"


def _thing(root: Path, rel: str, tid: str, extra: str = "", typ: str = "task",
           status: str = "in-progress") -> None:
    write(root, rel, thing_text(
        f"id: {tid}\ntype: {typ}\nstatus: {status}\ncreated: {RECENT}\n{extra}"))


def _vault(tmp_path: Path) -> Path:
    """Two domains: `alpha` references into itself and into `beta`."""
    vault = tmp_path / "vault"
    alpha, beta = vault / "alpha", vault / "beta"
    _thing(alpha, "things/work/x.md", "x", extra=(
        "linked_things:\n  - id: y\n    relation: informs\n"
        "dependencies: [z]\n"
        "parent: only-in-beta\n"
        f"informed_by:\n  - id: y\n    commit: {SHA}\n"
        "blocks: [nowhere]\n"))
    _thing(alpha, "things/work/y.md", "y")
    _thing(alpha, "things/work/z.md", "z", status="completed")
    _thing(beta, "things/notes/only-in-beta.md", "only-in-beta")
    return vault


def _read(vault: Path, *parts: str) -> str:
    return (vault / DEFAULT_OUT).joinpath(*parts).read_text(encoding="utf-8")


def test_every_reference_field_becomes_a_link(tmp_path):
    vault = _vault(tmp_path)
    report = build_vault_map(vault)
    links = _read(vault, "Links", "alpha.md")
    assert "- [[alpha/things/work/x|x]] · task · in-progress" in links
    assert "    - informs → [[alpha/things/work/y|y]]" in links
    assert "    - dependencies → [[alpha/things/work/z|z]]" in links
    assert "    - parent → [[beta/things/notes/only-in-beta|only-in-beta]]" in links
    assert f"    - informed-by → [[alpha/things/work/y|y]] (at `{SHA[:7]}`)" in links
    assert "    - blocks → `nowhere` (not in this vault)" in links
    alpha = next(d for d in report.domains if d.name == "alpha")
    assert (alpha.links, alpha.unresolved) == (5, 1)
    assert links.startswith("---\n" + NOTE_MARK)


def test_a_target_is_placed_by_ownership_or_reported(tmp_path):
    vault = _vault(tmp_path)
    alpha, beta, gamma = vault / "alpha", vault / "beta", vault / "gamma"
    # `shared` is native in beta and gamma: no owner can be named for alpha.
    _thing(beta, "things/shared.md", "shared")
    _thing(gamma, "things/shared.md", "shared")
    # `fact` is native in gamma and mirrored into beta: gamma owns it.
    _thing(gamma, "things/fact.md", "fact")
    _thing(beta, "things/imports/fact.md", "fact", extra=(
        f"source_domain: gamma\nsource_id: fact\nsource_commit: {SHA}\n"))
    # `local` exists in alpha and gamma: alpha's own copy wins for alpha.
    _thing(alpha, "things/local.md", "local")
    _thing(gamma, "things/local.md", "local")
    _thing(alpha, "things/asker.md", "asker",
           extra="dependencies: [shared, fact, local]\n")
    build_vault_map(vault)
    links = _read(vault, "Links", "alpha.md")
    assert "dependencies → `shared` (2 matches in other workspaces)" in links
    assert "dependencies → [[gamma/things/fact|fact]]" in links
    assert "dependencies → [[alpha/things/local|local]]" in links


def test_open_work_is_the_digests_set(tmp_path):
    vault = _vault(tmp_path)
    alpha = vault / "alpha"
    write(alpha, "things/_schema.yaml",
          "schema_version: 1\ntypes:\n  ticket:\n    statuses: [raised, shut]\n"
          "    terminal_statuses: [shut]\n")
    _thing(alpha, "things/t1.md", "t1", typ="ticket", status="raised")
    _thing(alpha, "things/t2.md", "t2", typ="ticket", status="shut")
    _thing(alpha, "things/c1.md", "c1", typ="conflict", status="open")
    _thing(alpha, "things/i1.md", "i1", typ="insight", status="active")
    build_vault_map(vault)
    open_note = _read(vault, "Open work", "alpha.md")
    assert "## Open conflicts (1)" in open_note and "[[alpha/things/c1|c1]]" in open_note
    assert "[[alpha/things/t1|t1]] · ticket · raised" in open_note
    assert "t2" not in open_note      # the type declares `shut` settled
    assert "|z]]" not in open_note    # completed: the universal terminal set
    assert "i1" not in open_note      # knowledge, not a loop
    # x, y and t1 are open loops; c1 is the open conflict.
    assert "| alpha | — | 7 | 4 |" in _read(vault, "Home.md")
    assert "Nothing open." not in open_note


def test_generated_caches_are_not_listed(tmp_path):
    vault = _vault(tmp_path)
    _thing(vault / "alpha", "things/_index/triggers.md", "alpha-triggers",
           typ="index", status="live")
    build_vault_map(vault)
    assert "alpha-triggers" not in _read(vault, "Links", "alpha.md")


def test_a_rerun_replaces_its_own_files_and_keeps_the_operators(tmp_path):
    vault = _vault(tmp_path)
    build_vault_map(vault)
    out = vault / DEFAULT_OUT
    mine = out / "My notes.md"
    mine.write_text("# Mine\n", encoding="utf-8")
    edited = out / "Links" / "alpha.md"
    edited.write_text("# I rewrote this\n", encoding="utf-8")
    # beta leaves the vault: its generated notes describe nothing now.
    for path in sorted((vault / "beta").rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    (vault / "beta").rmdir()
    report = build_vault_map(vault)
    assert mine.read_text(encoding="utf-8") == "# Mine\n"
    assert edited.read_text(encoding="utf-8") == "# I rewrote this\n"
    assert edited in report.kept
    assert not (out / "Links" / "beta.md").exists()
    assert not (out / "Open work" / "beta.md").exists()
    assert {p.name for p in report.removed} == {"beta.md"}


def test_it_never_writes_inside_a_domain(tmp_path):
    vault = _vault(tmp_path)
    before = sorted(p.relative_to(vault).as_posix()
                    for d in ("alpha", "beta") for p in (vault / d).rglob("*"))
    build_vault_map(vault, views="obsidian")
    after = sorted(p.relative_to(vault).as_posix()
                   for d in ("alpha", "beta") for p in (vault / d).rglob("*"))
    assert before == after


def test_view_files_are_a_named_choice_never_a_default(tmp_path):
    vault = _vault(tmp_path)
    build_vault_map(vault)
    assert not (vault / DEFAULT_OUT / "Views").exists()
    assert "Views" not in _read(vault, "Home.md")
    build_vault_map(vault, views="obsidian")
    base = _read(vault, "Views", "Things.base")
    assert base.startswith(VIEW_MARK)
    assert '\'["task"].contains(note.type)\'' in base
    assert f'!file.path.startsWith("{DEFAULT_OUT}")' in base
    assert f"[[{DEFAULT_OUT}/Views/Things.base|Things]]" in _read(vault, "Home.md")
    # Dropping the choice on a rerun removes the generated view with it.
    build_vault_map(vault)
    assert not (vault / DEFAULT_OUT / "Views" / "Things.base").exists()


def test_a_view_survives_the_tools_reformatting_but_an_edit_is_kept(tmp_path):
    """Measured on Obsidian 1.15 (2026-11-10): seconds after first showing a
    view file the tool rewrites it — comments dropped, quoting changed, the
    unknown top-level keys kept. That rewrite must not read as an operator's
    edit, or the view would never refresh again; a real change must."""
    import yaml
    vault = _vault(tmp_path)
    build_vault_map(vault, views="obsidian")
    view = vault / DEFAULT_OUT / "Views" / "Things.base"
    data = yaml.safe_load(view.read_text(encoding="utf-8"))
    # The tool's rewrite: same data, different bytes, keys in another order.
    view.write_text(yaml.safe_dump(data, sort_keys=True, width=4096),
                    encoding="utf-8")
    _thing(vault / "alpha", "things/new.md", "new", typ="memo")
    report = build_vault_map(vault, views="obsidian")
    assert view in report.written
    assert '["memo", "task"]' in view.read_text(encoding="utf-8")
    # The operator adds a column: now it is theirs.
    data = yaml.safe_load(view.read_text(encoding="utf-8"))
    data["views"][0]["order"].append("priority")
    view.write_text(yaml.safe_dump(data, sort_keys=False, width=4096),
                    encoding="utf-8")
    _thing(vault / "alpha", "things/newer.md", "newer", typ="zeta")
    report = build_vault_map(vault, views="obsidian")
    assert view in report.kept
    assert "zeta" not in view.read_text(encoding="utf-8")
    assert "priority" in view.read_text(encoding="utf-8")
    # And dropping --views does not delete a view the operator changed.
    build_vault_map(vault)
    assert view.exists()


def test_recent_changes_come_from_each_domains_own_log(tmp_path):
    vault = _vault(tmp_path)
    _git_repo(vault / "alpha")
    _git_commit(vault / "alpha", "create: x — see [[y]] for why")
    build_vault_map(vault, commits=5)
    changes = _read(vault, "Recent changes", "alpha.md")
    assert "create: x — see [ [y]] for why" in changes   # prose, not a link
    assert not (vault / DEFAULT_OUT / "Recent changes" / "beta.md").exists()
    home = _read(vault, "Home.md")
    assert f"[[{DEFAULT_OUT}/Recent changes/alpha\\|changes]]" in home
    assert home.count("| — |") >= 1      # beta has no log to show
    build_vault_map(vault, commits=0)
    assert not (vault / DEFAULT_OUT / "Recent changes" / "alpha.md").exists()


def test_refuses_where_a_repository_would_track_the_map(tmp_path):
    vault = _vault(tmp_path)
    _sync_git(tmp_path, "init", "-q")          # a repo around the vault
    with pytest.raises(VaultMapRefused, match="would be tracked"):
        build_vault_map(vault)
    assert not (vault / DEFAULT_OUT).exists()
    write(tmp_path, ".gitignore", "vault/\n")  # the nested-repo isolation line
    build_vault_map(vault)
    assert (vault / DEFAULT_OUT / "Home.md").is_file()
    assert _sync_git(tmp_path, "status", "--porcelain").stdout.strip() == "?? .gitignore"


def test_refuses_a_vault_that_is_a_domain_or_holds_none(tmp_path):
    vault = _vault(tmp_path)
    with pytest.raises(VaultMapRefused, match="itself a domain"):
        build_vault_map(vault / "alpha")
    assert not (vault / "alpha" / DEFAULT_OUT).exists()
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(VaultMapRefused, match="no domains found"):
        build_vault_map(empty)
    with pytest.raises(VaultMapRefused, match="plain folder name"):
        build_vault_map(vault, out_name="a/b")


def test_cli_reports_and_exit_codes(tmp_path, capsys):
    vault = _vault(tmp_path)
    args = _ns(vault=str(vault), out=DEFAULT_OUT, views=None, commits=0)
    assert cmd_vault_map(args) == 0
    out = capsys.readouterr().out
    assert "`alpha`: 3 thing(s) · 5 link(s) (1 not resolved) · 2 open" in out
    assert cmd_vault_map(_ns(vault=str(vault / "alpha"), out=DEFAULT_OUT,
                             views=None, commits=0)) == 2
    assert "refused" in capsys.readouterr().out
