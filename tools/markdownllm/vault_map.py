"""`mdllm vault-map` — a generated map folder for markdown-vault tools.

A folder of domains opened in a vault tool shows every record as a note, but
not what the substrate knows about them. Structural references live in
frontmatter as ids (`linked_things`, `dependencies`, `informed_by` …), which
vault tools do not read as links, so their backlink panes and graphs miss
every one; "what is open" is computed from declared terminal statuses, which
no vault tool knows; and the event stream is the commit log, which none of
them shows. This command restates those three facts as plain notes, in a
folder of its own beside the domains:

    <vault>/<out>/Home.md                    the domains, with counts
    <vault>/<out>/Links/<domain>.md          every thing, its references as links
    <vault>/<out>/Open work/<domain>.md      the digest's forward set
    <vault>/<out>/Recent changes/<domain>.md the newest commits

It is a projection, never a source: it reads the domains and writes only its
own folder; every file it writes carries a generated mark, a rerun replaces
marked files and removes marked ones that no longer apply, and a file without
the mark — one the operator wrote or edited — is left alone. It refuses to
write where a git repository would track the result, so a map can never
dirty a domain.

The notes are plain markdown with path-qualified wikilinks, readable by any
tool that follows them. Tool-specific view files are a separate, named
choice (`--views`), never a default: the substrate does not pick a surface
(`the-substrate-picks-no-surface-2026-11-10` — make it more reachable from a vault
tool without claiming one). The notes are outward text, so they follow the
2026-10-20 wording ruling — *workspace* where the specs say domain, *your
workspaces* where they say estate; this module's own names and its CLI
messages stay in the spec vocabulary. Links are written with the full vault path
because note names repeat across domains (pointer mirrors, shared ids) and a
bare name can open the wrong note; this touches generated notes only — how
records themselves spell a link is not this command's decision.

The pattern is one operator's hand-built map (a per-domain relationship note
generated from `linked_things`, in use since 2026-11-06), generalised: every
structural reference field from the registry rather than one, resolution
that says *why* a target did not resolve, and the open set from the same
function the session-start digest renders.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from .model import scan
from .session import open_loops
from .yaml_loader import load_yaml
from .structural_refs import (REFERENCE_FIELDS, StructuralReference,
                              iter_structural_references)

DEFAULT_OUT = "00 Workspace Map"
VIEW_KINDS = ("obsidian",)
NOTE_MARK = "generated_by: mdllm vault-map"
VIEW_MARK = "generated_by: mdllm vault-map"
_SAFE_NAME = re.compile(r"^[^\\/:*?\"<>|\[\]#^]+$")
_SAFE_TYPE = re.compile(r"^[A-Za-z0-9_.-]+$")


@dataclass(frozen=True)
class Entry:
    """One thing as the map shows it."""
    domain: str
    id: str
    vpath: str          # vault-relative, posix, no suffix — the link target
    folder: str         # parent directory, relative to its domain
    typ: str
    status: str
    mirror: bool        # a cross-domain import: another domain owns the fact
    refs: tuple[StructuralReference, ...]


@dataclass
class DomainMap:
    name: str
    root: Path
    entries: list[Entry] = field(default_factory=list)
    open_ids: tuple[list, list, list] = ((), (), ())
    unreadable: int = 0     # files the scan could not parse
    links: int = 0
    unresolved: int = 0


@dataclass
class Report:
    out: Path
    domains: list[DomainMap] = field(default_factory=list)
    written: list[Path] = field(default_factory=list)
    kept: list[Path] = field(default_factory=list)
    removed: list[Path] = field(default_factory=list)


class VaultMapRefused(Exception):
    """The map cannot be written here; the message says why and what to do."""


def discover_domains(vault: Path, out_name: str) -> list[Path]:
    """Immediate children that hold a `things/` directory."""
    return [child for child in sorted(vault.iterdir())
            if child.is_dir() and not child.name.startswith(".")
            and child.name != out_name and (child / "things").is_dir()]


def _read_domain(vault: Path, root: Path) -> DomainMap:
    dm = DomainMap(name=root.name, root=root)
    try:
        corpus, findings = scan(root)
    except Exception:
        dm.unreadable = -1  # the scan itself failed; said on the home note
        return dm
    dm.unreadable = sum(1 for f in findings if f.severity == "Error")
    dm.open_ids = open_loops(corpus)
    for t in corpus.things:
        if not t.id:
            continue
        try:
            rel = t.path.resolve().relative_to(root.resolve())
            vrel = t.path.resolve().relative_to(vault.resolve())
        except ValueError:
            continue
        if "_index" in rel.parts:
            continue  # generated caches: not records, and they restate every id
        dm.entries.append(Entry(
            domain=root.name, id=t.id, vpath=vrel.with_suffix("").as_posix(),
            folder=rel.parent.as_posix(), typ=str(t.meta.get("type", "")),
            status=str(t.meta.get("status", "")),
            mirror="source_domain" in t.meta,
            refs=tuple(iter_structural_references(t.meta))))
    dm.entries.sort(key=lambda e: (e.folder, e.id, e.vpath))
    return dm


class Resolver:
    """Where an id lives in this vault. The owning domain first, then the one
    native copy elsewhere; anything else is reported, never guessed."""

    def __init__(self, domains: list[DomainMap]):
        self._local: dict[str, dict[str, Entry]] = {}
        self._all: dict[str, list[Entry]] = {}
        for dm in domains:
            local = self._local.setdefault(dm.name, {})
            for e in sorted(dm.entries, key=lambda e: (e.mirror, e.vpath)):
                local.setdefault(e.id, e)
                self._all.setdefault(e.id, []).append(e)

    def find(self, thing_id: str, domain: str) -> tuple[str | None, str]:
        hit = self._local.get(domain, {}).get(thing_id)
        if hit is not None:
            return hit.vpath, ""
        found = self._all.get(thing_id, [])
        natives = [e for e in found if not e.mirror] or found
        if len(natives) == 1:
            return natives[0].vpath, ""
        if not natives:
            return None, "not in this vault"
        return None, f"{len(natives)} matches in other workspaces"

    def link(self, thing_id: str, domain: str) -> tuple[str, bool]:
        target, why = self.find(thing_id, domain)
        if target is None:
            return f"`{thing_id}` ({why})", False
        return f"[[{target}|{thing_id}]]", True


def _header(title: str, stamp: str, source: str) -> list[str]:
    return ["---", NOTE_MARK, f"generated: {stamp}", "---", "", f"# {title}", "",
            f"Generated by `mdllm vault-map` from {source}. Rerun the command "
            "to refresh; edits here are replaced.", ""]


def _links_note(dm: DomainMap, resolver: Resolver, stamp: str) -> str:
    fields = ", ".join(f"`{spec.field}`" for spec in REFERENCE_FIELDS)
    lines = _header(f"Links: {dm.name}", stamp,
                    f"each thing's structural references ({fields})")
    folder = None
    for e in dm.entries:
        if e.folder != folder:
            folder = e.folder
            lines += ["", f"## {folder}", ""]
        lines.append(f"- [[{e.vpath}|{e.id}]] · {e.typ} · {e.status}")
        for ref in e.refs:
            shown, ok = resolver.link(ref.target, dm.name)
            dm.links += 1
            dm.unresolved += 0 if ok else 1
            pin = f" (at `{ref.commit[:7]}`)" if ref.commit else ""
            lines.append(f"    - {ref.relation} → {shown}{pin}")
    if not dm.entries:
        lines.append("No things found.")
    return "\n".join(lines) + "\n"


def _open_note(dm: DomainMap, resolver: Resolver, stamp: str) -> str:
    conflicts, loops, watched = dm.open_ids
    lines = _header(f"Open work: {dm.name}", stamp,
                    "the set the session-start digest calls open — work "
                    "whose status its type does not declare settled")

    def section(title: str, rows: list[str]) -> None:
        if rows:
            lines.extend([f"## {title} ({len(rows)})", "", *rows, ""])

    section("Open conflicts",
            [f"- {resolver.link(c, dm.name)[0]}" for c in sorted(conflicts)])
    section("Open loops",
            [f"- {resolver.link(i, dm.name)[0]} · {t} · {s}"
             for i, t, s in sorted(loops)])
    section("Watched — another workspace's or the world's state",
            [f"- {resolver.link(i, dm.name)[0]} · {t} · {s}"
             for i, t, s in sorted(watched)])
    if not (conflicts or loops or watched):
        lines.append("Nothing open.")
    return "\n".join(lines) + "\n"


def _recent_commits(root: Path, count: int) -> list[tuple[str, str, str]] | None:
    """(short sha, day, subject), newest first; None where there is no log."""
    if count <= 0 or not (root / ".git").exists():
        return None
    try:
        r = subprocess.run(
            ["git", "log", f"-n{count}", "--date=short",
             "--format=%h%x1f%ad%x1f%s%x1e"],
            cwd=root, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    rows = []
    # Records end on \x1e, not a newline: a subject may carry a bare carriage
    # return, which splitlines() would cut in two.
    for record in r.stdout.decode("utf-8", "replace").split("\x1e"):
        parts = record.strip("\r\n").split("\x1f")
        if len(parts) == 3:
            rows.append((parts[0], parts[1], " ".join(parts[2].split())))
    return rows


def _changes_note(dm: DomainMap, commits: list, stamp: str) -> str:
    lines = _header(f"Recent changes: {dm.name}", stamp,
                    f"the newest {len(commits)} commit(s) in this workspace's "
                    "git history")
    for sha, day, subject in commits:
        # A subject is prose, not a link: `[[` in one must not become one.
        lines.append(f"- {day} · `{sha}` · {subject.replace('[[', '[ [')}")
    return "\n".join(lines) + "\n"


def _cell(target: str, label: str) -> str:
    return f"[[{target}\\|{label}]]"  # the pipe is escaped inside a table


def _home_note(report: Report, out_name: str, views: str | None,
               has_changes: set[str], stamp: str) -> str:
    lines = _header("Your workspaces", stamp,
                    f"the {len(report.domains)} workspace(s) in this folder")
    lines += ["| Workspace | Front page | Things | Open | Links | Open work | Changes |",
              "|---|---|---|---|---|---|---|"]
    for dm in report.domains:
        conflicts, loops, _watched = dm.open_ids
        front = (_cell(f"{dm.name}/AGENTS", "AGENTS")
                 if (dm.root / "AGENTS.md").is_file() else "—")
        changes = (_cell(f"{out_name}/Recent changes/{dm.name}", "changes")
                   if dm.name in has_changes else "—")
        lines.append(
            f"| {dm.name} | {front} | {len(dm.entries)} "
            f"| {len(conflicts) + len(loops)} "
            f"| {_cell(f'{out_name}/Links/{dm.name}', 'links')} "
            f"| {_cell(f'{out_name}/Open work/{dm.name}', 'open')} | {changes} |")
    lines.append("")
    if views == "obsidian":
        lines += [f"**Views:** [[{out_name}/Views/Things.base|Things]] — every "
                  "thing, grouped by type, status or workspace. A view you change is "
                  "kept on a rerun.", ""]
    broken = [dm for dm in report.domains if dm.unreadable]
    if broken:
        lines.append("**Could not read:** " + "; ".join(
            f"{dm.name} ({'the whole workspace' if dm.unreadable < 0 else str(dm.unreadable) + ' file(s)'})"
            for dm in broken) + " — `mdllm validate` in that workspace says why.")
        lines.append("")
    lines += [
        "**Good to know**",
        "- This folder is generated and sits outside every workspace's git "
        "repository. A rerun replaces generated notes and leaves anything "
        "you wrote here alone.",
        "- Things record their links in frontmatter by id, which vault tools "
        "do not treat as links. The Links notes restate them, so backlinks "
        "work; a graph view shows each Links note as a hub, not thing-to-thing "
        "edges.",
        "- Editing a workspace's file here changes the real file. It is committed, "
        "checked and published only when a session in that workspace commits it.",
    ]
    return "\n".join(lines) + "\n"


def _view_digest(data: dict) -> str:
    """A view file's content as data, minus its own generated keys."""
    body = {k: v for k, v in data.items()
            if k not in ("generated_by", "generated_hash")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False,
                                     default=str).encode("utf-8")).hexdigest()[:16]


def _obsidian_things_view(out_name: str, types: list[str]) -> str:
    """One table view over every thing. Written in the tool's own canonical
    spelling (a bare `type`, not `note.type`, in `order` and `groupBy`):
    the tool rewrites a view file in that form seconds after first showing
    it, and a file that already reads that way comes back as the same data
    (measured on Obsidian 1.15, 2026-11-10 — the rewrite drops YAML comments
    and keeps unknown top-level keys, which is why the mark is a key)."""

    def view(name: str, group_by: str | None, only: str | None = None) -> list[str]:
        lines = ["  - type: table", f"    name: {name}"]
        if group_by:
            lines += ["    groupBy:", f"      property: {group_by}",
                      "      direction: ASC"]
        if only:
            lines += ["    filters:", "      and:", f"        - '{only}'"]
        return lines + ["    order:", "      - file.name", "      - type",
                        "      - status", "      - formula.domain",
                        "      - created"]

    lines = [
        "filters:",
        "  and:",
        "    - 'file.ext == \"md\"'",
        f"    - '!file.path.startsWith(\"{out_name}\")'",
        "    - '!file.path.contains(\"/_index/\")'",
        f"    - '{json.dumps(types)}.contains(note.type)'",
        "formulas:",
        "  domain: 'file.path.split(\"/\")[0]'",
        "properties:",
        "  formula.domain:",
        "    displayName: Workspace",
        "  note.type:",
        "    displayName: Type",
        "  note.status:",
        "    displayName: Status",
        "views:",
        *view("By type", "type"),
        *view("By status", "status"),
        *view("By workspace", "formula.domain"),
        *view("Skills", None, only='note.type == "skill"'),
    ]
    body = "\n".join(lines) + "\n"
    return (f"{VIEW_MARK}\ngenerated_hash: {_view_digest(load_yaml(body))}\n"
            + body)


def _is_ours(path: Path) -> bool:
    """A note is ours while it carries the mark. A view file is ours while it
    carries the mark AND still holds the data we wrote: the tool's own
    reformatting keeps both, an operator's change to the view breaks the
    hash — so a customised view is kept, never overwritten."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    if path.suffix == ".md":
        return text.startswith("---") and NOTE_MARK in text[:400]
    try:
        data = load_yaml(text, source=path)
    except Exception:
        return False
    return (isinstance(data, dict)
            and data.get("generated_by") == "mdllm vault-map"
            and data.get("generated_hash") == _view_digest(data))


def _write_owned(path: Path, text: str, report: Report) -> None:
    if path.exists() and not _is_ours(path):
        report.kept.append(path)  # the operator's file, or their edit of ours
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    report.written.append(path)


def _tracked_by_git(vault: Path, out: Path) -> bool:
    """True when a git repository containing the vault would track `out`."""
    try:
        inside = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                cwd=vault, capture_output=True, timeout=30)
        if inside.returncode != 0:
            return False
        ignored = subprocess.run(["git", "check-ignore", "-q", str(out)],
                                 cwd=vault, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return ignored.returncode != 0


def build_vault_map(vault: Path, out_name: str = DEFAULT_OUT,
                    views: str | None = None, commits: int = 30) -> Report:
    vault = Path(vault).resolve()
    if not vault.is_dir():
        raise VaultMapRefused(f"{vault} is not a folder")
    if not _SAFE_NAME.match(out_name) or out_name.startswith("."):
        raise VaultMapRefused(
            f"--out {out_name!r} is not a plain folder name a link can carry")
    if (vault / "things").is_dir():
        raise VaultMapRefused(
            f"{vault} is itself a domain — the map would be written inside "
            "its repository. Point this at the folder that holds the domains.")
    roots = discover_domains(vault, out_name)
    if not roots:
        raise VaultMapRefused(
            f"no domains found in {vault} — expected subfolders that each "
            "hold a `things/` directory")
    out = vault / out_name
    if _tracked_by_git(vault, out):
        raise VaultMapRefused(
            f"{out} would be tracked by the git repository around it — a "
            "generated view must not enter a record. Add the folder to that "
            "repository's .gitignore, or choose another location.")

    report = Report(out=out)
    report.domains = [_read_domain(vault, root) for root in roots]
    resolver = Resolver(report.domains)
    stamp = dt.date.today().isoformat()
    has_changes: set[str] = set()
    for dm in report.domains:
        _write_owned(out / "Links" / f"{dm.name}.md",
                     _links_note(dm, resolver, stamp), report)
        _write_owned(out / "Open work" / f"{dm.name}.md",
                     _open_note(dm, resolver, stamp), report)
        log = _recent_commits(dm.root, commits)
        if log:
            has_changes.add(dm.name)
            _write_owned(out / "Recent changes" / f"{dm.name}.md",
                         _changes_note(dm, log, stamp), report)
    if views == "obsidian":
        types = sorted({e.typ for dm in report.domains for e in dm.entries
                        if _SAFE_TYPE.match(e.typ)})
        _write_owned(out / "Views" / "Things.base",
                     _obsidian_things_view(out_name, types), report)
    _write_owned(out / "Home.md",
                 _home_note(report, out_name, views, has_changes, stamp), report)

    # A marked file this run did not produce describes a domain, a log or a
    # view that is no longer there. Unmarked files are never touched.
    current = set(report.written) | set(report.kept)
    for path in sorted(out.rglob("*")):
        if (path.is_file() and path.suffix in (".md", ".base")
                and path not in current and _is_ours(path)):
            path.unlink()
            report.removed.append(path)
    return report


def cmd_vault_map(args) -> int:
    try:
        report = build_vault_map(Path(args.vault), out_name=args.out,
                                 views=args.views, commits=args.commits)
    except VaultMapRefused as refused:
        print(f"mdllm vault-map: refused — {refused}")
        return 2
    print(f"## Vault map — {report.out}")
    for dm in report.domains:
        conflicts, loops, _watched = dm.open_ids
        missing = f" ({dm.unresolved} not resolved)" if dm.unresolved else ""
        print(f"- `{dm.name}`: {len(dm.entries)} thing(s) · {dm.links} "
              f"link(s){missing} · {len(conflicts) + len(loops)} open")
    print(f"\nwrote {len(report.written)} file(s)"
          + (f", kept {len(report.kept)} without the generated mark"
             if report.kept else "")
          + (f", removed {len(report.removed)} stale" if report.removed else ""))
    for path in report.kept:
        print(f"  kept: {path.relative_to(report.out).as_posix()}")
    return 0
