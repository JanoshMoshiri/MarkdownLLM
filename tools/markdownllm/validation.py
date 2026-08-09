"""Levels 1-3 mechanical validation — the floor's core contract.

Level 1: per-thing structure (required fields, status vocabulary, ISO dates,
relational field shapes). Level 2: corpus-wide referential integrity (unknown
ids, terminal-status invariant, workflow-run cursors, cycles, insight/conflict
circulation). Level 3: schema conformance (declared types, required fields,
relation and field vocabularies). Plus the framework version-sentinel sync
check and example-corpus discovery that `validate` and the pre-commit hook
run over.
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

import yaml

from .model import (
    RESERVED_STATUSES, DEFAULT_STATUSES, TERMINAL_STATUSES, CORE_FIELDS,
    is_terminal, terminal_statuses_for,
    ID_RE, ISO_RE, SEV_ERROR, SEV_WARNING, SEV_INFO,
    Thing, Finding, Corpus, parse_frontmatter, scan,
)

def valid_statuses_for(typ: str, schema: dict | None) -> tuple[list[str] | None, bool]:
    """Returns (allowed_statuses, declared). declared=False means default vocabulary."""
    if typ in RESERVED_STATUSES:
        return RESERVED_STATUSES[typ], True
    if schema:
        tdef = (schema.get("types") or {}).get(typ)
        if isinstance(tdef, dict) and isinstance(tdef.get("statuses"), list):
            return [str(s) for s in tdef["statuses"]], True
    return DEFAULT_STATUSES, False


def validate_level1(t: Thing, schema: dict | None) -> list[Finding]:
    f: list[Finding] = []
    name = t.id or str(t.path.name)
    meta = t.meta

    for fld in ("id", "type", "status", "created"):
        if not meta.get(fld):
            f.append(Finding(SEV_ERROR, name, f"missing required field `{fld}`"))

    if t.id:
        if not ID_RE.match(t.id):
            f.append(Finding(SEV_WARNING, name, f"`id` not lowercase-hyphenated: {t.id!r}"))
        check_filename = ((schema or {}).get("options") or {}).get("id_filename_match", True)
        if check_filename and t.path.stem != t.id and t.path.name not in ("continuity.md",):
            f.append(Finding(SEV_WARNING, name, f"`id` does not match filename `{t.path.name}`"))

    typ, status = str(meta.get("type", "")), meta.get("status")
    if typ and status is not None:
        allowed, declared = valid_statuses_for(typ, schema)
        if str(status) not in allowed:
            sev = SEV_ERROR if declared else SEV_WARNING
            f.append(Finding(sev, name,
                     f"status `{status}` not in {'declared' if declared else 'default'} "
                     f"vocabulary for type `{typ}`: {allowed}"))

    for fld in ("created", "due_date", "review_date"):
        v = meta.get(fld)
        if v is not None and not (isinstance(v, (dt.date, dt.datetime)) or
                                  (isinstance(v, str) and ISO_RE.match(v))):
            sev = SEV_ERROR if fld == "created" else SEV_WARNING
            f.append(Finding(sev, name, f"`{fld}` is not ISO 8601: {v!r}"))

    lt = meta.get("linked_things")
    if lt is not None:
        if not isinstance(lt, list):
            f.append(Finding(SEV_ERROR, name, "`linked_things` is not a list"))
        else:
            for i, entry in enumerate(lt):
                if not isinstance(entry, dict) or "id" not in entry or "relation" not in entry:
                    f.append(Finding(SEV_ERROR, name,
                             f"`linked_things[{i}]` must be an object with `id` and `relation`"))

    for fld in ("dependencies", "blocks"):
        v = meta.get(fld)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) for x in v)):
            f.append(Finding(SEV_ERROR, name, f"`{fld}` must be an array of id strings"))

    trig = meta.get("triggers")
    if trig is not None:
        if not isinstance(trig, list):
            f.append(Finding(SEV_ERROR, name, "`triggers` is not a list"))
        else:
            for i, tr in enumerate(trig):
                if not isinstance(tr, dict) or "type" not in tr or "action" not in tr:
                    f.append(Finding(SEV_ERROR, name,
                             f"`triggers[{i}]` must have `type` and `action`"))
                    continue
                # Structural completeness (cohesiveness-sensors plan): a trigger
                # that gives the floor nothing to evaluate AND the agent nothing
                # to judge is declared but can never fire — for anyone. `watch`
                # is the floor's substrate; `condition` prose is the agent's (a
                # relationship trigger watching the world rather than a thing is
                # a legitimate, observed pattern — it must stay quiet). Only the
                # nothing-at-all case warns. Same-builder: these fields are
                # exactly what triggers.py reads.
                ttype = tr.get("type")
                if (ttype == "relationship"
                        and not tr.get("watch") and not tr.get("condition")):
                    f.append(Finding(SEV_WARNING, name,
                             f"`triggers[{i}]` is a `relationship` trigger with "
                             f"neither `watch` nor `condition` — nothing for the "
                             f"floor to evaluate or the agent to judge; it can "
                             f"never fire. Fill one, or route it to another "
                             f"species (trigger-specification.md)"))
                elif (ttype == "dependency" and not tr.get("condition")
                        and not (tr.get("watch") and tr.get("value"))):
                    f.append(Finding(SEV_WARNING, name,
                             f"`triggers[{i}]` is a `dependency` trigger without "
                             f"`watch`/`value` — as declared it can never fire "
                             f"(the evaluator needs both, with "
                             f"`on: status_changed_to`)"))

    if not t.body.strip():
        f.append(Finding(SEV_WARNING, name, "empty markdown body"))
    elif not t.body.lstrip().startswith("#"):
        f.append(Finding(SEV_WARNING, name, "body does not start with a `#` title heading"))
    return f


def validate_level2(corpus: Corpus) -> list[Finding]:
    f: list[Finding] = []
    ids: dict[str, list[Thing]] = {}
    for t in corpus.things:
        if t.id:
            ids.setdefault(t.id, []).append(t)
    for tid, ts in ids.items():
        if len(ts) > 1:
            paths = ", ".join(str(t.path.relative_to(corpus.root)) for t in ts)
            f.append(Finding(SEV_ERROR, tid, f"duplicate id across files: {paths}"))
    known = set(ids)

    referenced: set[str] = set()
    # `referenced_by_live` is the inbound-edge set restricted to edges whose
    # SOURCE is non-terminal — the graph signal for "still in circulation" that
    # replaces continuity-brief presence as the liveness test (dissolve-continuity-
    # into-reconciliation plan, Phase B). A thing nothing live points back to has
    # fallen out of session memory.
    referenced_by_live: set[str] = set()
    for t in corpus.things:
        name = t.id or t.path.name
        meta = t.meta
        # NOTE: deliberately the universal set, not is_terminal(). "Settled"
        # and "dead" are different questions. A signed SOP at
        # `approved-current`, or an oversight view at `current`, is settled
        # work AND a live referrer — an insight it links to has not fallen
        # out of session memory. Only genuinely closed-out states
        # (superseded, cancelled, dismissed...) stop a thing conferring
        # liveness. Using the per-type set here made this check fire on five
        # healthy insights the moment a domain declared its vocabulary.
        src_live = str(meta.get("status")) not in TERMINAL_STATUSES
        refs: list[tuple[str, str]] = []
        for entry in meta.get("linked_things") or []:
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                refs.append(("linked_things", entry["id"]))
        for fld in ("dependencies", "blocks", "parties"):
            for rid in meta.get(fld) or []:
                if isinstance(rid, str):
                    refs.append((fld, rid))
        if isinstance(meta.get("parent"), str):
            refs.append(("parent", meta["parent"]))
        if isinstance(meta.get("definition"), str):
            refs.append(("definition", meta["definition"]))
        for tr in meta.get("triggers") or []:
            if isinstance(tr, dict):
                watch = tr.get("watch")
                for rid in (watch if isinstance(watch, list) else [watch] if watch else []):
                    if isinstance(rid, str):
                        refs.append(("triggers.watch", rid))
        for fld, rid in refs:
            referenced.add(rid)
            if src_live:
                referenced_by_live.add(rid)
            if rid not in known:
                f.append(Finding(SEV_ERROR, name, f"`{fld}` references unknown id `{rid}`"))

        # terminal-status invariant: a finished thing cannot depend on unfinished
        # work (detect-conflicts rule #1, mechanised). Terminal deps (completed,
        # cancelled, met, ...) count as resolved; dangling deps are caught above.
        if is_terminal(corpus.schema, meta):
            for dep in meta.get("dependencies") or []:
                if not isinstance(dep, str):
                    continue
                dt = ids.get(dep, [None])[0]
                if dt and not is_terminal(corpus.schema, dt.meta):
                    f.append(Finding(SEV_ERROR, name,
                             f"is `{meta.get('status')}` but dependency `{dep}` is "
                             f"`{dt.meta.get('status')}` (not terminal) — a finished "
                             f"thing cannot depend on unfinished work"))

        # bidirectional: A blocks B => B depends on A (or links A)
        for blocked in meta.get("blocks") or []:
            target = ids.get(blocked, [None])[0]
            if target:
                deps = target.meta.get("dependencies") or []
                linked = [e.get("id") for e in target.meta.get("linked_things") or []
                          if isinstance(e, dict)]
                if t.id not in deps and t.id not in linked:
                    f.append(Finding(SEV_WARNING, name,
                             f"blocks `{blocked}` but it lists no inverse dependency/link"))

        # contradicts requires a conflict thing listing both parties
        for entry in meta.get("linked_things") or []:
            if isinstance(entry, dict) and entry.get("relation") == "contradicts":
                other = entry.get("id")
                if str(meta.get("type")) == "conflict":
                    continue
                has_conflict = any(
                    str(c.meta.get("type")) == "conflict"
                    and t.id in (c.meta.get("parties") or [])
                    and other in (c.meta.get("parties") or [])
                    for c in corpus.things)
                if not has_conflict:
                    f.append(Finding(SEV_ERROR, name,
                             f"`contradicts: {other}` without a `type: conflict` thing "
                             f"listing both parties"))
            if isinstance(entry, dict) and entry.get("relation") == "supersedes":
                other_t = ids.get(entry.get("id"), [None])[0]
                if other_t:
                    back = any(isinstance(e, dict) and e.get("id") == t.id
                               and e.get("relation") == "superseded-by"
                               for e in other_t.meta.get("linked_things") or [])
                    deprecated = str(other_t.meta.get("status")) == "deprecated"
                    if not back and not deprecated:
                        f.append(Finding(SEV_WARNING, name,
                                 f"supersedes `{entry.get('id')}` but target has no "
                                 f"`superseded-by` link and is not deprecated"))

    # workflow-run cursor integrity (workflow-state.md): a run points at its
    # definition via the structural `definition` field, and `current_stage` must
    # be a stage that definition declares. Pure referential integrity — the
    # floor's job, same class as "linked_things targets must exist". (Transition
    # *legality* across the loop graph stays the agent's Layer-2 judgment.)
    for t in corpus.things:
        if str(t.meta.get("type")) != "workflow-run":
            continue
        name = t.id or t.path.name
        defn_id, cur = t.meta.get("definition"), t.meta.get("current_stage")
        if not isinstance(defn_id, str):
            f.append(Finding(SEV_ERROR, name,
                     "workflow-run missing `definition` (the workflow-definition it instances)"))
            continue
        if cur is None:
            f.append(Finding(SEV_ERROR, name, "workflow-run missing `current_stage`"))
        target = ids.get(defn_id, [None])[0]
        if target is None:
            continue  # unknown id already reported by the referential check above
        if str(target.meta.get("type")) != "workflow-definition":
            f.append(Finding(SEV_ERROR, name,
                     f"`definition` `{defn_id}` is not a workflow-definition"))
            continue
        stage_ids = {s["id"] for s in target.meta.get("stages") or []
                     if isinstance(s, dict) and isinstance(s.get("id"), str)}
        if cur is not None and str(cur) not in stage_ids:
            f.append(Finding(SEV_ERROR, name,
                     f"`current_stage` `{cur}` is not a stage in `{defn_id}` "
                     f"(stages: {sorted(stage_ids)})"))

    # circular dependencies
    graph = {t.id: [d for d in (t.meta.get("dependencies") or []) if isinstance(d, str)]
             for t in corpus.things if t.id}
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> list[str] | None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                return stack + [node, nxt]
            if state.get(nxt, 0) == 0 and nxt in graph:
                cycle = visit(nxt, stack + [node])
                if cycle:
                    return cycle
        state[node] = 2
        return None

    for node in graph:
        if state.get(node, 0) == 0:
            cycle = visit(node, [])
            if cycle:
                f.append(Finding(SEV_ERROR, cycle[0],
                         "circular dependency: " + " -> ".join(cycle)))
                break

    # orphans (Info). `prompt` is exempt alongside the generated types: prompts
    # are instruction things, referenced by NAME from kernel blocks and
    # bindings, never by graph edge — and their linked_things are stripped on
    # scaffold egress by design, so flagging them would fire on every newborn.
    for t in corpus.things:
        meta = t.meta
        if str(meta.get("type")) in ("continuity-brief", "index", "prompt"):
            continue
        has_rel = bool(meta.get("linked_things") or meta.get("dependencies")
                       or meta.get("blocks") or meta.get("parent") or meta.get("triggers"))
        if not has_rel and t.id not in referenced:
            f.append(Finding(SEV_INFO, t.id or t.path.name,
                     "orphaned — no relationships, triggers, or inbound references"))

    # Insight / conflict circulation (session-memory.md → Insight Lifecycle
    # Management). Liveness is GRAPH-keyed, not file-keyed: an `active` insight or
    # `open` conflict is "in circulation" iff some NON-TERMINAL thing has an
    # inbound edge to it (`referenced_by_live`). One that nothing live points back
    # to has fallen out of session memory — promote it (its lesson shipped),
    # dismiss it, or link it from live work. This replaces the old "present in
    # continuity.md" proxy (dissolve-continuity-into-reconciliation, Phase B):
    # file-presence liveness was brittle — a backward-log cleanup could orphan a
    # standing insight, and an insight with only OUTBOUND edges has discharged
    # itself (a promotion candidate), which the inbound test surfaces by design.
    for t in corpus.things:
        if not t.id or t.id not in known:
            continue
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "insight" and status == "active" and t.id not in referenced_by_live:
            # A standing-razor or parked insight is genuinely live with no active
            # dependant; `disposition: keep-active` is the deliberate reckoning that
            # exempts it (the brake the backlog itself demanded — Phase C). The
            # stated reason is the whole point, so keep-active without one is nudged.
            if str(t.meta.get("disposition", "")) == "keep-active":
                if not str(t.meta.get("disposition_reason", "")).strip():
                    f.append(Finding(SEV_INFO, t.id,
                             "insight marked keep-active but has no "
                             "`disposition_reason` — state why it stays live"))
            else:
                f.append(Finding(SEV_INFO, t.id,
                         "active insight with no inbound edge from a live thing — "
                         "orphaned from session memory; promote, dismiss, link it "
                         "from live work, or mark `disposition: keep-active`"))
        elif typ == "conflict" and status == "open" and t.id not in referenced_by_live:
            f.append(Finding(SEV_INFO, t.id,
                     "open conflict with no inbound edge from a live thing — link "
                     "it from the work it blocks so it returns next session"))
    return f


def version_tuple(v: str) -> tuple[int, int, int]:
    parts = [int(x) for x in re.findall(r"\d+", str(v))[:3]]
    return tuple(parts + [0] * (3 - len(parts)))  # type: ignore[return-value]


def check_version_sync(root: Path) -> list[Finding]:
    """Framework root only: `.markdownllm`, AGENTS.md frontmatter, and the
    latest CHANGELOG entry must agree on the version. The sentinel is what
    domain agents key their refresh off — a stale sentinel silently disables
    domain-refresh for everything shipped since."""
    sentinel = root / ".markdownllm"
    if not sentinel.exists():
        return []
    versions: dict[str, str] = {}
    data = yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}
    if data.get("version"):
        versions[".markdownllm"] = str(data["version"])
    agents = root / "AGENTS.md"
    if agents.exists():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        if meta and meta.get("version"):
            versions["AGENTS.md"] = str(meta["version"])
    changelog = root / "CHANGELOG.md"
    if changelog.exists():
        m = re.search(r"^## \[(\d+(?:\.\d+){1,2})\]",
                      changelog.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            versions["CHANGELOG.md"] = m.group(1)
    if len({version_tuple(v) for v in versions.values()}) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(versions.items()))
        return [Finding(SEV_ERROR, "framework-version",
                f"version sentinel out of sync: {detail} — these must be "
                f"bumped together (domain refresh keys off .markdownllm)")]
    return []


def validate_level3(corpus: Corpus) -> list[Finding]:
    f: list[Finding] = []
    schema = corpus.schema
    if not schema:
        return f
    declared_types = set(schema.get("types") or {}) | set(RESERVED_STATUSES)
    relations = schema.get("relations")

    # `terminal_statuses` coherence: a declared terminal status that is not in
    # its own type's `statuses` can never match, so the declaration silently
    # does nothing — exactly the class of bug this field exists to end. Warning,
    # like the rest of level 3, and the value is ignored at read time
    # (terminal_statuses_for intersects with the vocabulary).
    for typ, tdef in (schema.get("types") or {}).items():
        if not isinstance(tdef, dict) or not isinstance(tdef.get("terminal_statuses"), list):
            continue
        vocab = tdef.get("statuses")
        if not isinstance(vocab, list):
            continue
        stray = sorted({str(s) for s in tdef["terminal_statuses"]} - {str(s) for s in vocab})
        if stray:
            f.append(Finding(SEV_WARNING, "_schema.yaml",
                             f"type `{typ}`: terminal_statuses {stray} not in its "
                             f"`statuses` vocabulary — ignored"))
    for typ in (schema.get("types") or {}):
        if typ in RESERVED_STATUSES:
            tdef = (schema.get("types") or {}).get(typ)
            if isinstance(tdef, dict) and "terminal_statuses" in tdef:
                f.append(Finding(SEV_WARNING, "_schema.yaml",
                                 f"type `{typ}` is framework-reserved — its "
                                 f"terminal_statuses are owned by the tool and this "
                                 f"declaration is ignored"))

    # Field registration (opt-in, like `relations`): when a domain declares a
    # `known_fields` list, any top-level frontmatter key outside CORE_FIELDS ∪
    # known_fields ∪ the per-type required_fields is flagged. This closes the
    # silent-loss hole — a mis-keyed field (e.g. `relations:` typed where
    # `linked_things:` was meant) used to pass clean because the floor only
    # validated the *values* of known fields, never the *set of keys*. Warning,
    # not Error: the whole level-3 family is advisory (schema-gated), and the
    # bug was silence — Warning already ends it. A domain that declares no
    # known_fields gets no field check (no false alarms until it opts in). The
    # descriptive companion is `mdllm index <path> rebuild --signal schema`,
    # which enumerates every field in use — the bootstrap source for the list.
    known_fields = schema.get("known_fields")
    field_allow: set[str] | None = None
    if isinstance(known_fields, list):
        field_allow = set(CORE_FIELDS) | {str(k) for k in known_fields}
        for tdef in (schema.get("types") or {}).values():
            if isinstance(tdef, dict):
                field_allow |= {str(r) for r in (tdef.get("required_fields") or [])}

    for t in corpus.things:
        name = t.id or t.path.name
        typ = str(t.meta.get("type", ""))
        if typ and typ not in declared_types:
            f.append(Finding(SEV_WARNING, name, f"type `{typ}` not declared in _schema.yaml"))
        tdef = (schema.get("types") or {}).get(typ) or {}
        for req in tdef.get("required_fields") or []:
            if req not in t.meta:
                f.append(Finding(SEV_ERROR, name, f"domain-required field `{req}` missing"))
        if isinstance(relations, list):
            for entry in t.meta.get("linked_things") or []:
                if isinstance(entry, dict) and entry.get("relation") not in relations:
                    f.append(Finding(SEV_WARNING, name,
                             f"relation `{entry.get('relation')}` not in declared vocabulary"))
        if field_allow is not None:
            for key in t.meta:
                if str(key) not in field_allow:
                    f.append(Finding(SEV_WARNING, name,
                             f"field `{key}` not in CORE_FIELDS or declared "
                             f"`known_fields` — register it in _schema.yaml or fix "
                             f"the typo"))
    return f


def _git_stdout(root: Path, args: list[str]) -> str | None:
    # Decode git output as UTF-8 explicitly. Thing files are UTF-8; relying on
    # the platform locale (cp1252 on Windows) makes the reader thread raise
    # UnicodeDecodeError on any multibyte content, which subprocess swallows —
    # leaving returncode 0 but stdout None, crashing the caller. errors="replace"
    # keeps a decode edge from ever bricking validation.
    out = subprocess.run(["git", *args], cwd=root, capture_output=True,
                         text=True, encoding="utf-8", errors="replace")
    return out.stdout.strip() if out.returncode == 0 and out.stdout is not None else None


def quarantine_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """The verified flip as an auditable event (verified-flip-enforcement plan).

    The floor cannot verify TRUTH (did a human really review?) — that is
    judgement. It can verify PROCEDURE, because git is a same-builder event
    stream: (1) a `verified: true` whose most recent flip commit IS the
    thing's creation commit had no review window (born verified) — also fired
    pre-commit for a working-tree thing not yet in HEAD; (2) a flip must name
    its human via `verified_by` (ALCOA attributable — forgeable, but a false
    attribution is a falsifiable record, categorically better than an
    anonymous bit). Scope: `origin: external`, the quarantined class.

    Severity: Warning by default; `options: {quarantine: strict}` in
    _schema.yaml raises both to Error (the pre-commit hook then blocks).
    Historical findings heal: re-quarantine and re-flip in a separate,
    attributed commit — the newest flip then no longer matches creation.
    """
    strict = ((corpus.schema or {}).get("options") or {}).get("quarantine") == "strict"
    sev = SEV_ERROR if strict else SEV_WARNING
    out: list[Finding] = []

    # Quarantine age (provenance.md → Validation: "External unverified" — Info).
    # An `origin: external` thing still unverified after 30 days is a divergence
    # aging toward silent default: nothing may rest on it, yet nothing is
    # resurfacing it either. Info, never raised by strict mode — the spec sets
    # this row at Info; the operator's disposition (verify, or record why it
    # stays quarantined) is the route. Same-builder: the thing's own frontmatter.
    today = dt.date.today()
    for t in corpus.things:
        if str(t.meta.get("origin")) != "external" or t.meta.get("verified") is True:
            continue
        created = t.meta.get("created")
        if isinstance(created, dt.datetime):
            created = created.date()
        elif isinstance(created, str) and ISO_RE.match(created):
            created = dt.date.fromisoformat(created[:10])
        if not isinstance(created, dt.date):
            continue
        age = (today - created).days
        if age > 30:
            out.append(Finding(SEV_INFO, t.id or t.path.name,
                       f"`origin: external` and unverified for {age} days "
                       f"(created {created}) — verify it, or record why it "
                       f"stays quarantined (provenance.md: External "
                       f"unverified >30d)"))

    externals = [t for t in corpus.things
                 if str(t.meta.get("origin")) == "external"
                 and t.meta.get("verified") is True]
    if not externals:
        return out
    toplevel = _git_stdout(root, ["rev-parse", "--show-toplevel"])
    for t in externals:
        name = t.id or t.path.name
        vb = t.meta.get("verified_by")
        if not (isinstance(vb, str) and vb.strip()):
            out.append(Finding(sev, name,
                       "`verified: true` without `verified_by` — the flip must "
                       "name its human verifier (quarantine flip discipline; "
                       "provenance.md)"))
        if toplevel is None:
            continue  # not a git repo — the git-keyed half skips, like provenance
        try:
            rel = t.path.resolve().relative_to(Path(toplevel).resolve()).as_posix()
        except ValueError:
            continue
        in_head = subprocess.run(["git", "cat-file", "-e", f"HEAD:{rel}"],
                                 cwd=root, capture_output=True).returncode == 0
        if not in_head:
            out.append(Finding(sev, name,
                       "about to be born `verified: true` — commit it "
                       "unverified first, then flip in a separate attributed "
                       "commit (a same-commit flip has no review window)"))
            continue
        # If HEAD still holds verified != true, the flip is only pending in the
        # working tree — a distinct commit from creation by construction.
        head_text = _git_stdout(root, ["show", f"HEAD:{rel}"])
        if head_text is not None:
            head_meta, _, _ = parse_frontmatter(head_text)
            if not (head_meta and head_meta.get("verified") is True):
                continue
        created = _git_stdout(root, ["log", "--diff-filter=A", "--format=%H",
                                     "-1", "--", rel])
        # Newest commit whose post-image carries verified: true among commits
        # that touched such a line — the most recent flip (so a proper
        # re-verification heals a historical born-verified finding).
        flip = None
        candidates = _git_stdout(root, ["log", "--format=%H",
                                        "-G", r"^verified: *[Tt]rue", "--", rel])
        for c in (candidates or "").splitlines():
            shown = _git_stdout(root, ["show", f"{c}:{rel}"])
            if shown is None:
                continue
            cmeta, _, _ = parse_frontmatter(shown)
            if cmeta and cmeta.get("verified") is True:
                flip = c
                break
        if created and flip and created == flip:
            out.append(Finding(sev, name,
                       f"born `verified: true` — the flip commit is the "
                       f"creation commit ({created[:9]}); no review window "
                       f"existed. Heal: re-quarantine, then re-verify in a "
                       f"separate commit naming `verified_by`"))
    return out


def retrospective_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """retrospective.md → validate.thing.md: a domain with no retrospective in
    over 60 days of active sessions is flagged as one Info observation.

    "Active days" is read mechanically from the commit stream: the corpus must
    be older than 60 days (young domains are silent) AND have committed to
    `things/` within the last 60 (dormant domains are silent — a paused domain
    owes no reflection). Both gates keep the check quiet-when-healthy: it fires
    only where sessions are running and the reflection ritual is not
    (a-check-that-always-fires-teaches-the-operator-to-ignore-it)."""
    first = _git_stdout(root, ["log", "--reverse", "--format=%cs", "--", "things"])
    if not first:
        return []  # no git history over things/ — nothing to say
    try:
        born = dt.date.fromisoformat(first.splitlines()[0].strip())
    except ValueError:
        return []
    today = dt.date.today()
    if (today - born).days <= 60:
        return []
    recent = _git_stdout(root, ["rev-list", "--count", "--since=60.days",
                                "HEAD", "--", "things"])
    if not recent or not recent.isdigit() or int(recent) == 0:
        return []
    newest: dt.date | None = None
    for t in corpus.things:
        if str(t.meta.get("type")) != "retrospective":
            continue
        for fld in ("period_end", "created"):
            v = t.meta.get(fld)
            if isinstance(v, dt.datetime):
                v = v.date()
            elif isinstance(v, str) and ISO_RE.match(v):
                v = dt.date.fromisoformat(v[:10])
            if isinstance(v, dt.date):
                newest = max(newest, v) if newest else v
                break
    if newest is None:
        return [Finding(SEV_INFO, "retrospective-cadence",
                f"no retrospective has ever been written — the domain has been "
                f"active {(today - born).days} days (retrospective.md: monthly, "
                f"or after a significant milestone)")]
    if (today - newest).days > 60:
        return [Finding(SEV_INFO, "retrospective-cadence",
                f"no retrospective since {newest} ({(today - newest).days} days) "
                f"with active sessions in the last 60 — the period's aggregate "
                f"sweeps (conflict scan, schema coherence) have not run")]
    return []


def validate_corpus(root: Path) -> tuple[Corpus, list[Finding]]:
    corpus, findings = scan(root)
    for t in corpus.things:
        findings.extend(validate_level1(t, corpus.schema))
    findings.extend(validate_level2(corpus))
    findings.extend(validate_level3(corpus))
    findings.extend(derivation_findings(corpus))
    return corpus, findings


def derivation_findings(corpus: Corpus) -> list[Finding]:
    """A figure must still agree with the derivation it declares (calc.py).

    An asserted total drifts the moment a line item changes and the total does
    not. Nothing could ever catch that, because nothing knew how the total was
    reached. A `computed:` block says how, and this re-runs it at every commit.

    Severity: Warning by default, `options: {computed: strict}` in
    _schema.yaml raises disagreement to Error (the pre-commit hook then
    blocks). Warning is the default deliberately — a filed return whose box is
    arithmetically odd but is *what was actually filed* must stay recordable;
    recorded truth outranks internal consistency, and only the domain knows
    which of its figures are its own to reconcile.

    Non-evaluability is always a Warning and never silent: an expression the
    floor cannot run is a check the operator believes is running.

    Quiet when healthy: a domain that declares no derivation gets no finding,
    and one whose figures agree gets no finding either.
    """
    from .calc import context_for, evaluate_block, fmt

    strict = ((corpus.schema or {}).get("options") or {}).get("computed") == "strict"
    out: list[Finding] = []
    for t in corpus.things:
        if not isinstance(t.meta.get("computed"), dict):
            continue
        name = t.id or t.path.name
        for d in evaluate_block(t.meta, context_for(t, corpus)):
            if d.error is not None:
                out.append(Finding(SEV_WARNING, name,
                           f"`computed.{d.target}` is not evaluable: {d.error}"))
            elif d.agrees is False:
                out.append(Finding(SEV_ERROR if strict else SEV_WARNING, name,
                           f"`{d.target}` is {fmt(d.asserted)} but its own "
                           f"derivation `{d.expr}` computes {fmt(d.value)}"))
    return out


def example_corpora(root: Path) -> list[Path]:
    """Example domains live in <root>/examples/<name>/ with their own
    AGENTS.md and _schema.yaml. They are excluded from the root corpus walk
    (separate id space, separate schema) but they are NOT exempt from the
    floor: validate discovers and checks each one as its own corpus, so the
    pre-commit hook covers them in the same run."""
    examples = root / "examples"
    if not examples.is_dir():
        return []
    return sorted(d for d in examples.iterdir()
                  if d.is_dir() and (d / "AGENTS.md").exists())


SESSION_GATE_WINDOW_HOURS = 24


def session_gate_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """The session gate (cowork-integrity-estate-sweep Phase 10). A domain may
    declare `options: {session_gate: warn|strict}` in its schema: committing
    then requires a fresh session-start attestation for this clone
    (`<git-dir>/mdllm-attest`, written by `mdllm session-start`, uncommittable
    by construction). The gate exists because every breached Cowork session
    kept a green floor: the only controls it could skip were the ones that
    left no evidence, and a skipped interpretation-anchored control looks
    identical to a performed one. This check makes a contract-less session
    loud at its first write instead of silent for a month, in every harness,
    with no adapter required. Deliberately smaller claim than it may read as:
    the attestation proves the Tier-0 contract was *emitted into this clone's
    session*, not that it was heeded — the heeding residue belongs to the
    register work, and is a categorically smaller failure class than
    never-saw-it. Severity: Warning under `warn`, commit-blocking Error under
    `strict`. Anchor: git-fs (runs in the pre-commit hook via validate)."""
    mode = ((corpus.schema or {}).get("options") or {}).get("session_gate")
    if mode not in ("warn", "strict"):
        return []
    sev = SEV_ERROR if mode == "strict" else SEV_WARNING
    remedy = ("run `python {framework_root}/tools/mdllm.py session-start .` in "
              "this clone — it emits the Tier-0 contract and records the "
              "attestation — then commit")
    gd = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                        capture_output=True, text=True)
    if gd.returncode != 0 or not gd.stdout.strip():
        return []  # not a git repo: nothing will commit, the gate has no boundary to hold
    head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root,
                          capture_output=True, text=True)
    if head.returncode != 0:
        # Unborn HEAD: this is the BIRTH commit — the contract files are being
        # created in it, so there was nothing to have read before it. The gate
        # holds every commit after the first (scaffold's own first commit runs
        # under the hook it just installed; blocking birth would be the gate
        # eating its own scaffolding — caught by CI on 2026-08-08, same day).
        return []
    attest = (root / gd.stdout.strip()).resolve() / "mdllm-attest"
    if not attest.is_file():
        # Two different findings share this branch and the message names both:
        # a fresh clone whose setup has not yet reached session-start (ordering
        # — the attestation CANNOT exist yet), and a clone that has been
        # working without ever emitting the contract (the breach the gate was
        # built from). The floor cannot tell them apart — only the operator's
        # knowledge of where setup stands can — so the severity holds and the
        # wording refuses to accuse setup of a skip (substrate sweep C2).
        return [Finding(sev, "_session-gate",
                        "session gate: no session-start attestation exists for "
                        "this clone — either setup is mid-flight (fresh clone, "
                        "session-start not yet run: ordering, not a skip) or "
                        "this clone has been working without the Tier-0 "
                        "contract; " + remedy)]
    try:
        stamp = attest.read_text(encoding="utf-8").split()[0]
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(stamp)
    except Exception:
        return [Finding(sev, "_session-gate",
                        "session gate: attestation unreadable — " + remedy)]
    if age > dt.timedelta(hours=SESSION_GATE_WINDOW_HOURS):
        hrs = int(age.total_seconds() // 3600)
        return [Finding(sev, "_session-gate",
                        f"session gate: attestation is {hrs}h old (window "
                        f"{SESSION_GATE_WINDOW_HOURS}h) — this session opened on "
                        "yesterday's contract; " + remedy)]
    return []


def cmd_validate(args) -> int:
    root = Path(args.path).resolve()
    reports: list[tuple[Path, Corpus, list[Finding]]] = []
    corpus, findings = validate_corpus(root)
    findings.extend(check_version_sync(root))
    findings.extend(quarantine_findings(root, corpus))
    findings.extend(session_gate_findings(root, corpus))
    findings.extend(retrospective_findings(root, corpus))
    reports.append((root, corpus, findings))
    for sub in example_corpora(root):
        # Example corpora skip the retrospective-cadence check: they are
        # teaching corpora with frozen dates, not domains running sessions.
        sub_corpus, sub_findings = validate_corpus(sub)
        sub_findings.extend(quarantine_findings(sub, sub_corpus))
        reports.append((sub, sub_corpus, sub_findings))

    total_errors = 0
    for rpt_root, rpt_corpus, rpt_findings in reports:
        errors = [x for x in rpt_findings if x.severity == SEV_ERROR]
        warnings = [x for x in rpt_findings if x.severity == SEV_WARNING]
        infos = [x for x in rpt_findings if x.severity == SEV_INFO]
        total_errors += len(errors)

        if not args.quiet or errors:
            print(f"## Validation Report — {rpt_root}")
            print(f"schema: {'_schema.yaml found' if rpt_corpus.schema else 'none (default vocabulary, advisory)'}\n")
            for title, group in (("Errors (must fix)", errors),
                                 ("Warnings (should fix)", warnings),
                                 ("Info (worth knowing)", infos)):
                if group:
                    print(f"### {title}")
                    for x in group:
                        print(f"- **{x.thing}**: {x.message}")
                    print()
            print("### Summary")
            print(f"- Things checked: {len(rpt_corpus.things)}")
            print(f"- Errors: {len(errors)}  Warnings: {len(warnings)}  Info: {len(infos)}")
            clean = len(rpt_corpus.things) - len({x.thing for x in rpt_findings})
            print(f"- Clean: {max(clean, 0)}")
            print()
    return 1 if total_errors else 0
