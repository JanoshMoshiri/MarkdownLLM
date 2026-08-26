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
from pathlib import Path, PurePosixPath

import yaml

from .model import (
    RESERVED_STATUSES, DEFAULT_STATUSES, TERMINAL_STATUSES, CORE_FIELDS,
    is_terminal, origin_is_external, terminal_statuses_for,
    ID_RE, ISO_RE, SEV_ERROR, SEV_WARNING, SEV_INFO,
    Thing, Finding, Corpus, parse_frontmatter, scan,
)
from .yaml_loader import load_yaml
from .repository_view import (
    RepositoryView, RepositoryViewError, RepositoryViewMode,
)
from .structural_refs import (
    iter_structural_references, structural_field_names, structural_shape_errors,
)
from .session_contract import contract_fingerprint

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

    for field, reason in structural_shape_errors(meta):
        f.append(Finding(SEV_ERROR, name, f"`{field}` {reason}"))

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
        for ref in iter_structural_references(meta, validation_only=True):
            fld, rid = ref.field, ref.target
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

    # workflow-run cursor integrity for unpinned runs (workflow-state.md).
    # Keep the legacy/current-definition arm here because validate_level2 is a
    # public pure validator used by callers outside validate_corpus. Pinned
    # membership needs Git I/O and is owned by workflow_run_findings below;
    # structure and target type remain view-independent for both arms.
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
        if t.meta.get("definition_commit") is not None:
            continue  # immutable membership is the Git-backed arm below
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
        has_rel = any(meta.get(field) for field in structural_field_names())
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


_FULL_COMMIT_RE = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")


class WorkflowDefinitionResolver:
    """Resolve immutable workflow definitions once per validation pass.

    Revision binding is Git-backed policy, not generic graph validation.  This
    resolver keeps that I/O at one seam and caches by commit, so many runs on
    one approved definition pay one revision resolution and one batched tree
    read rather than one subprocess chain per run.
    """

    def __init__(self, root: Path, corpus: Corpus):
        self.root = Path(root).resolve()
        self.corpus = corpus
        self.repository_root = (corpus.view.root if corpus.view is not None
                                else self.root)
        self._views: dict[str, RepositoryView] = {}
        self._view_errors: dict[str, str] = {}
        self._corpora: dict[str, Corpus] = {}
        self._definitions: dict[tuple[str, str, str], tuple[Thing | None, str | None]] = {}

    @staticmethod
    def valid_pin(pin: object) -> bool:
        return isinstance(pin, str) and _FULL_COMMIT_RE.fullmatch(pin) is not None

    def _commit_view(self, pin: str) -> tuple[RepositoryView | None, str | None]:
        key = pin.lower()
        if key in self._views:
            return self._views[key], None
        if key in self._view_errors:
            return None, self._view_errors[key]
        try:
            selected = RepositoryView.commit(self.repository_root, pin)
        except RepositoryViewError:
            message = (f"`definition_commit` `{pin}` does not resolve to a "
                       "commit in this repository")
            self._view_errors[key] = message
            return None, message
        self._views[key] = selected
        return selected, None

    def resolve(
        self, pin: str, definition_id: str,
        current_definition: Thing | None,
    ) -> tuple[Thing | None, str | None]:
        """Find ``definition_id`` at ``pin``, current path first then id scan."""
        path_key = ""
        if current_definition is not None:
            try:
                path_key = current_definition.path.resolve().relative_to(
                    self.repository_root).as_posix()
            except ValueError:
                path_key = ""
        cache_key = (pin.lower(), definition_id, path_key)
        cached = self._definitions.get(cache_key)
        if cached is not None:
            return cached

        selected, error = self._commit_view(pin)
        if selected is None:
            result = (None, error)
            self._definitions[cache_key] = result
            return result

        # Fast path: definitions normally retain their current path.  Read that
        # exact blob first; when a definition moved, fall back to an id-indexed
        # corpus scan of the same immutable view. RepositoryView batches both
        # tree and blob reads, and the fallback corpus is cached per commit.
        if path_key and selected.exists(PurePosixPath(path_key)):
            text = selected.read_text(PurePosixPath(path_key))
            meta, body, parse_error = parse_frontmatter(text, source=path_key)
            if (parse_error is None and isinstance(meta, dict)
                    and str(meta.get("id")) == definition_id
                    and str(meta.get("type")) == "workflow-definition"):
                result = (Thing(
                    path=self.repository_root.joinpath(*PurePosixPath(path_key).parts),
                    meta=meta, body=body, source_text=text,
                ), None)
                self._definitions[cache_key] = result
                return result

        pinned = self._corpora.get(pin.lower())
        if pinned is None:
            pinned, _ = scan(self.root, selected)
            self._corpora[pin.lower()] = pinned
        definition = pinned.by_id().get(definition_id)
        if (definition is None
                or str(definition.meta.get("type")) != "workflow-definition"):
            result = (
                None,
                f"`definition_commit` `{pin}` does not carry workflow-definition "
                f"`{definition_id}` (current path miss and id fallback miss)",
            )
        else:
            result = (definition, None)
        self._definitions[cache_key] = result
        return result


def workflow_run_findings(
    root: Path, corpus: Corpus,
    resolver: WorkflowDefinitionResolver | None = None,
) -> list[Finding]:
    """Validate run references, revision pins, membership, and fulfilment shape."""
    by_id = corpus.by_id()
    selected = resolver or WorkflowDefinitionResolver(root, corpus)
    findings: list[Finding] = []
    for run in corpus.things:
        if str(run.meta.get("type")) != "workflow-run":
            continue
        name = run.id or run.path.name
        definition_id = run.meta.get("definition")
        current_stage = run.meta.get("current_stage")
        revision = run.meta.get("definition_commit")
        if revision is None:
            findings.append(Finding(
                SEV_INFO, name,
                "workflow-run has no `definition_commit`; it uses legacy "
                "prior-committed-definition semantics — pin the full commit "
                "whose definition governs the run in a separate commit",
            ))
        elif isinstance(definition_id, str):
            current_definition = by_id.get(definition_id)
            if (current_definition is not None
                    and str(current_definition.meta.get("type"))
                    == "workflow-definition"):
                if not selected.valid_pin(revision):
                    findings.append(Finding(
                        SEV_ERROR, name,
                        "`definition_commit` must be a full 40- or "
                        "64-character Git commit object id",
                    ))
                else:
                    definition, error = selected.resolve(
                        str(revision), definition_id, current_definition)
                    if error is not None:
                        findings.append(Finding(SEV_ERROR, name, error))
                    elif definition is not None and current_stage is not None:
                        stage_ids = {
                            stage["id"]
                            for stage in definition.meta.get("stages") or []
                            if (isinstance(stage, dict)
                                and isinstance(stage.get("id"), str))
                        }
                        if str(current_stage) not in stage_ids:
                            findings.append(Finding(
                                SEV_ERROR, name,
                                f"`current_stage` `{current_stage}` is not a "
                                f"stage in `{definition_id}` at pinned revision "
                                f"`{revision}` (stages: {sorted(stage_ids)})",
                            ))

    return findings


def workflow_transition_findings(
    root: Path, corpus: Corpus, view: RepositoryView | None = None,
    resolver: WorkflowDefinitionResolver | None = None,
) -> list[Finding]:
    """Enforce old -> new workflow edges at the next-commit boundary.

    Membership is a property of the candidate corpus and remains in
    :func:`validate_level2`.  Transition legality needs two explicit views:
    the frozen index tree supplies the candidate cursor, while the prior
    commit supplies both the old cursor and the definition that governed the
    move.  A definition edit in the same commit therefore cannot retroactively
    authorize its own run transition.

    Worktree and historical-commit validation remain useful read surfaces but
    cannot claim to be the exact next commit, so this check deliberately fires
    only for ``RepositoryView.index``.  A repository with no prior commit has
    no old run state to compare and is valid by construction.
    """
    candidate = view or corpus.view
    if candidate is None or candidate.mode is not RepositoryViewMode.INDEX:
        return []
    # Transitions are read off candidate workflow-runs; a corpus with none
    # needs no prior view at all. Without this bail every index-view validate
    # paid a full prior-HEAD corpus scan per corpus (three at the framework
    # root) to verify zero transitions.
    if not any(str(t.meta.get("type")) == "workflow-run"
               for t in corpus.things):
        return []
    try:
        prior_view = RepositoryView.commit(candidate.root, "HEAD")
    except RepositoryViewError:
        return []

    prior, _ = scan(root, prior_view)
    prior_by_id = prior.by_id()
    candidate_by_id = corpus.by_id()
    findings: list[Finding] = []
    selected = resolver or WorkflowDefinitionResolver(root, corpus)

    for run_id, new_run in candidate_by_id.items():
        if str(new_run.meta.get("type")) != "workflow-run":
            continue
        old_run = prior_by_id.get(run_id)
        if old_run is None or str(old_run.meta.get("type")) != "workflow-run":
            continue  # creation is not a transition

        old_stage = old_run.meta.get("current_stage")
        new_stage = new_run.meta.get("current_stage")
        if old_stage is None or new_stage is None or str(old_stage) == str(new_stage):
            continue

        old_revision = old_run.meta.get("definition_commit")
        new_revision = new_run.meta.get("definition_commit")
        if old_revision != new_revision:
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"workflow-run changes both `definition_commit` and "
                f"`current_stage` (`{old_stage}` -> `{new_stage}`) in one "
                "candidate — migrate the governing revision in a separate "
                "meaning-boundary commit before advancing the cursor",
            ))
            continue

        old_definition_id = old_run.meta.get("definition")
        new_definition_id = new_run.meta.get("definition")
        if (not isinstance(old_definition_id, str)
                or not isinstance(new_definition_id, str)):
            # Candidate structural findings already name a missing new
            # pointer.  The old pointer is needed to establish the edge, so
            # make that inability explicit rather than guessing.
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"cannot verify workflow transition `{old_stage}` -> "
                f"`{new_stage}` because the prior or candidate `definition` "
                "pointer is missing",
            ))
            continue
        if old_definition_id != new_definition_id:
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"workflow transition `{old_stage}` -> `{new_stage}` also "
                f"changes `definition` from `{old_definition_id}` to "
                f"`{new_definition_id}` — migrate the definition in a separate "
                "meaning-boundary commit before advancing the cursor",
            ))
            continue

        definition = prior_by_id.get(old_definition_id)
        if (definition is None
                or str(definition.meta.get("type")) != "workflow-definition"):
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"cannot verify workflow transition `{old_stage}` -> "
                f"`{new_stage}`: prior definition `{old_definition_id}` is "
                "missing or is not a workflow-definition",
            ))
            continue

        definition_source = f"prior definition `{old_definition_id}`"
        if old_revision is not None:
            if not selected.valid_pin(old_revision):
                findings.append(Finding(
                    SEV_ERROR, run_id,
                    "cannot verify workflow transition because the prior "
                    "`definition_commit` is not a full Git commit object id",
                ))
                continue
            definition, error = selected.resolve(
                str(old_revision), old_definition_id, definition)
            if error is not None or definition is None:
                findings.append(Finding(
                    SEV_ERROR, run_id,
                    f"cannot verify workflow transition `{old_stage}` -> "
                    f"`{new_stage}`: {error or 'pinned definition is missing'}",
                ))
                continue
            definition_source = (
                f"pinned definition `{old_definition_id}` at `{old_revision}`")

        source_stages = [stage for stage in definition.meta.get("stages") or []
                         if isinstance(stage, dict)
                         and str(stage.get("id")) == str(old_stage)]
        if len(source_stages) != 1:
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"cannot verify workflow transition `{old_stage}` -> "
                f"`{new_stage}`: {definition_source} "
                f"declares {len(source_stages)} source stages named "
                f"`{old_stage}`",
            ))
            continue
        allowed = source_stages[0].get("to")
        if (not isinstance(allowed, list)
                or not all(isinstance(stage, str) for stage in allowed)):
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"cannot verify workflow transition `{old_stage}` -> "
                f"`{new_stage}`: prior stage `{old_stage}` has no valid "
                "`to` edge list",
            ))
            continue
        if str(new_stage) not in allowed:
            findings.append(Finding(
                SEV_ERROR, run_id,
                f"workflow transition `{old_stage}` -> `{new_stage}` is not "
                f"declared by {definition_source} "
                f"(allowed: {allowed})",
            ))
    return findings


def version_tuple(v: str) -> tuple[int, int, int]:
    parts = [int(x) for x in re.findall(r"\d+", str(v))[:3]]
    return tuple(parts + [0] * (3 - len(parts)))  # type: ignore[return-value]


def _view_logical(root: Path, relative: str, view: RepositoryView) -> PurePosixPath:
    prefix = Path(root).resolve().relative_to(view.root).as_posix()
    base = PurePosixPath(prefix)
    rel = PurePosixPath(relative)
    return rel if base == PurePosixPath(".") else base / rel


def _candidate_text(root: Path, relative: str,
                    view: RepositoryView | None) -> str | None:
    if view is None:
        path = root / relative
        return path.read_text(encoding="utf-8") if path.is_file() else None
    logical = _view_logical(root, relative, view)
    return view.read_text(logical) if view.exists(logical) else None


def check_version_sync(root: Path,
                       view: RepositoryView | None = None) -> list[Finding]:
    """Framework root only: `.markdownllm`, AGENTS.md frontmatter, and the
    latest CHANGELOG entry must agree on the version. The sentinel is what
    domain agents key their refresh off — a stale sentinel silently disables
    domain-refresh for everything shipped since."""
    sentinel_text = _candidate_text(root, ".markdownllm", view)
    if sentinel_text is None:
        return []
    versions: dict[str, str] = {}
    try:
        data = load_yaml(sentinel_text, source=".markdownllm") or {}
    except yaml.YAMLError as exc:
        return [Finding(SEV_ERROR, "framework-version",
                f"version sentinel is invalid YAML: {exc}")]
    if not isinstance(data, dict):
        return [Finding(SEV_ERROR, "framework-version",
                "version sentinel must be a YAML mapping")]
    if data.get("version"):
        versions[".markdownllm"] = str(data["version"])
    agents_text = _candidate_text(root, "AGENTS.md", view)
    if agents_text is not None:
        meta, _, _ = parse_frontmatter(agents_text)
        if meta and meta.get("version"):
            versions["AGENTS.md"] = str(meta["version"])
    changelog_text = _candidate_text(root, "CHANGELOG.md", view)
    if changelog_text is not None:
        m = re.search(r"^## \[(\d+(?:\.\d+){1,2})\]",
                      changelog_text, re.MULTILINE)
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
        if not origin_is_external(t.meta) or t.meta.get("verified") is True:
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
                 if origin_is_external(t.meta)
                 and t.meta.get("verified") is True]
    if not externals:
        return out
    toplevel = _git_stdout(root, ["rev-parse", "--show-toplevel"])
    # Batch the per-thing git work (floor-sprint-1 F12): HEAD existence and
    # content come from ONE commit view with a prefetched read (the per-thing
    # `cat-file -e` + `show` pair cost two spawns each), and creation commits
    # come from ONE --diff-filter=A walk instead of a log per thing. An
    # import-heavy domain carries dozens of verified externals; per-thing
    # spawns made this check scale with the mirror count.
    head_view = None
    created_map: dict[str, str] = {}
    if toplevel is not None:
        try:
            head_view = RepositoryView.commit(root, "HEAD")
        except RepositoryViewError:
            head_view = None
        if head_view is not None:
            rels = []
            for t in externals:
                try:
                    rels.append(t.path.resolve().relative_to(
                        Path(toplevel).resolve()).as_posix())
                except ValueError:
                    continue
            head_view.prefetch(rels)
            adds = _git_stdout(root, ["log", "--diff-filter=A",
                                      "--format=%x1e%H", "--name-only"])
            for record in (adds or "").split("\x1e"):
                if not record.strip():
                    continue
                sha, _, paths = record.partition("\n")
                for line in paths.splitlines():
                    line = line.strip()
                    if line:
                        # newest-first: first add wins, matching `log -1`
                        created_map.setdefault(line, sha.strip())
    for t in externals:
        name = t.id or t.path.name
        vb = t.meta.get("verified_by")
        if not (isinstance(vb, str) and vb.strip()):
            out.append(Finding(sev, name,
                       "`verified: true` without `verified_by` — the flip must "
                       "name its human verifier (quarantine flip discipline; "
                       "provenance.md)"))
        if toplevel is None or head_view is None:
            continue  # not a git repo — the git-keyed half skips, like provenance
        try:
            rel = t.path.resolve().relative_to(Path(toplevel).resolve()).as_posix()
        except ValueError:
            continue
        if not head_view.exists(rel):
            out.append(Finding(sev, name,
                       "about to be born `verified: true` — commit it "
                       "unverified first, then flip in a separate attributed "
                       "commit (a same-commit flip has no review window)"))
            continue
        # If HEAD still holds verified != true, the flip is only pending in the
        # working tree — a distinct commit from creation by construction.
        try:
            head_text = head_view.read_text(rel)
        except (FileNotFoundError, RepositoryViewError, UnicodeError):
            head_text = None
        if head_text is not None:
            head_meta, _, _ = parse_frontmatter(head_text)
            if not (head_meta and head_meta.get("verified") is True):
                continue
        created = created_map.get(rel)
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


def retrospective_findings(root: Path, corpus: Corpus,
                           things_dates: list[dt.date] | None = None,
                           ) -> list[Finding]:
    """retrospective.md → validate.thing.md: a domain with no retrospective in
    over 60 days of active sessions is flagged as one Info observation.

    "Active days" is read mechanically from the commit stream: the corpus must
    be older than 60 days (young domains are silent) AND have committed to
    `things/` within the last 60 (dormant domains are silent — a paused domain
    owes no reflection). Both gates keep the check quiet-when-healthy: it fires
    only where sessions are running and the reflection ritual is not
    (a-check-that-always-fires-teaches-the-operator-to-ignore-it).

    ``things_dates`` — newest-first commit dates over `things/` — lets a
    caller that already walked the history (session-start) share the walk
    instead of paying two more git spawns here."""
    today = dt.date.today()
    if things_dates is not None:
        if not things_dates:
            return []
        born = things_dates[-1]
        if (today - born).days <= 60:
            return []
        if not any((today - d).days <= 60 for d in things_dates):
            return []
    else:
        first = _git_stdout(root, ["log", "--reverse", "--format=%cs", "--", "things"])
        if not first:
            return []  # no git history over things/ — nothing to say
        try:
            born = dt.date.fromisoformat(first.splitlines()[0].strip())
        except ValueError:
            return []
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


def validate_corpus(root: Path,
                    view: RepositoryView | None = None) -> tuple[Corpus, list[Finding]]:
    corpus, findings = scan(root, view)
    workflow_resolver = WorkflowDefinitionResolver(root, corpus)
    for t in corpus.things:
        findings.extend(validate_level1(t, corpus.schema))
    findings.extend(validate_level2(corpus))
    findings.extend(workflow_run_findings(root, corpus, workflow_resolver))
    findings.extend(workflow_transition_findings(
        root, corpus, view, workflow_resolver))
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

    Non-evaluability is a Warning by default and an Error in strict mode: an
    expression the floor cannot run is a check the operator believes is
    running, and strict cannot be disabled by a typo.  Corpus exclusions are
    surfaced for the same reason — agreement over a silently smaller input set
    is not a trustworthy aggregate.

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
                out.append(Finding(SEV_ERROR if strict else SEV_WARNING, name,
                           f"`computed.{d.target}` is not evaluable: {d.error}"))
            elif d.agrees is False:
                out.append(Finding(SEV_ERROR if strict else SEV_WARNING, name,
                           f"`{d.target}` is {fmt(d.asserted)} but its own "
                           f"derivation `{d.expr}` computes {fmt(d.value)}"))
            for note in d.notes:
                if str(note).startswith("EXCLUDED "):
                    out.append(Finding(SEV_ERROR if strict else SEV_WARNING,
                               name, f"`computed.{d.target}` used a reduced "
                               f"input set: {note}"))
    return out


def example_corpora(root: Path,
                    view: RepositoryView | None = None) -> list[Path]:
    """Example domains live in <root>/examples/<name>/ with their own
    AGENTS.md and _schema.yaml. They are excluded from the root corpus walk
    (separate id space, separate schema) but they are NOT exempt from the
    floor: validate discovers and checks each one as its own corpus, so the
    pre-commit hook covers them in the same run."""
    if view is None:
        examples = root / "examples"
        if not examples.is_dir():
            return []
        return sorted(d for d in examples.iterdir()
                      if d.is_dir() and (d / "AGENTS.md").exists())

    prefix = Path(root).resolve().relative_to(view.root)
    logical_prefix = PurePosixPath(prefix.as_posix())
    names: set[str] = set()
    for logical in view.list_paths():
        try:
            rel = (logical if logical_prefix == PurePosixPath(".")
                   else logical.relative_to(logical_prefix))
        except ValueError:
            continue
        if (len(rel.parts) == 3 and rel.parts[0] == "examples"
                and rel.parts[2] == "AGENTS.md"):
            names.add(rel.parts[1])
    return [root / "examples" / name for name in sorted(names)]


def validation_reports(
    root: Path, view: RepositoryView | None = None,
) -> list[tuple[Path, Corpus, list[Finding]]]:
    """Build the complete validation result used by the CLI boundary.

    Keeping this composition public prevents other mechanical consumers (the
    eval harness in particular) from quietly defining a smaller meaning of
    "validates clean".  Formatting stays in ``cmd_validate``; this function is
    the one semantic-free result boundary.
    """
    # The corpora are independent read-only evaluations over the same
    # immutable view; warm the shared caches single-threaded, then evaluate
    # concurrently — wall approaches the slowest corpus, not the sum
    # (floor-sprint-1 F13). Report order stays deterministic: root first,
    # examples sorted, exactly as the serial composition printed.
    if view is not None:
        view.prefetch(view.list_paths(suffix=".md"))

    def _root_report() -> tuple[Path, Corpus, list[Finding]]:
        corpus, findings = validate_corpus(root, view)
        findings.extend(check_version_sync(root, view))
        findings.extend(quarantine_findings(root, corpus))
        findings.extend(session_gate_findings(root, corpus))
        findings.extend(retrospective_findings(root, corpus))
        return (root, corpus, findings)

    def _example_report(sub: Path) -> tuple[Path, Corpus, list[Finding]]:
        # Example corpora skip retrospective cadence: teaching corpora carry
        # frozen dates rather than live sessions.
        sub_corpus, sub_findings = validate_corpus(sub, view)
        history_root = view.root if view is not None else sub
        sub_findings.extend(quarantine_findings(history_root, sub_corpus))
        return (sub, sub_corpus, sub_findings)

    subs = example_corpora(root, view)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=1 + max(1, len(subs))) as pool:
        root_future = pool.submit(_root_report)
        sub_futures = [pool.submit(_example_report, sub) for sub in subs]
        reports = [root_future.result()]
        reports.extend(f.result() for f in sub_futures)
    return reports


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
    never-saw-it. Token 0 carries the freshness fact; the kernel token
    (session-start-hardening Phase 2) says what the kernel emission DID —
    whole/deferred/elided/absent — and `elided`/`absent` surface as
    Warnings in both modes, never a strict Error (the remedy is a read the
    floor cannot witness; a gate the session cannot clear is a dead end).
    Severity: Warning under `warn`, commit-blocking Error under
    `strict`. Anchor: git-fs (runs in the pre-commit hook via validate)."""
    mode = ((corpus.schema or {}).get("options") or {}).get("session_gate")
    if mode not in ("warn", "strict"):
        return []
    sev = SEV_ERROR if mode == "strict" else SEV_WARNING
    remedy = ("run `mdllm session-start .` through the manual CLI launch "
              "route in this clone's on-disk AGENTS.md — on a direct channel "
              "it emits the operative kernel whole (`--contract` emits the "
              "full Tier-0 contract) and records an attestation whose kernel "
              "token says what landed — then commit")
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
        tokens = attest.read_text(encoding="utf-8").split()
        stamp = tokens[0]
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
    # The kernel token (session-start-hardening Phase 2): the emitter records
    # what it DID with the kernel — whole:<sha>:<lines> / deferred (hook
    # channel, by design) / elided / absent. `elided` means the emission ran
    # but the kernel did not land whole (the remote Cowork evidence: a
    # truncated emission cleared this gate's timestamp-only check unseen).
    # Deliberately a Warning in BOTH modes, never a strict Error: the remedy
    # — read the named file in full — is evidence the floor cannot receive,
    # and a commit-block the session cannot clear is a dead-end gate.
    # Legacy attestations carry no kernel token and stay silent.
    kernel_token = next((t for t in tokens[1:] if t.startswith("kernel=")), "")
    if kernel_token == "kernel=elided":
        return [Finding(SEV_WARNING, "_session-gate",
                        "session gate: the attested emission carried an "
                        "ELIDED kernel — it did not land whole; read the "
                        "kernel file named in the emission in full before "
                        "acting on domain state")]
    if kernel_token == "kernel=absent":
        return [Finding(SEV_WARNING, "_session-gate",
                        "session gate: the attested emission found NO kernel "
                        "file — regenerate it at the framework root "
                        "(`mdllm kernel`) and re-run `mdllm session-start .`")]
    contract_token = next((t for t in tokens[1:]
                           if t.startswith("contract=")), "")
    if contract_token:
        try:
            attested = contract_token.partition("=")[2]
            current = contract_fingerprint(root)
        except Exception:
            attested = current = ""  # unreadable is handled as an advisory below
        if not attested or not current:
            return [Finding(SEV_WARNING, "_session-gate",
                            "session gate: contract fingerprint could not be "
                            "checked — " + remedy)]
        if attested != current:
            return [Finding(sev, "_session-gate",
                            "session gate: the operative Tier-0 contract "
                            "changed after session-start; unrelated HEAD "
                            "movement does not expire the gate, but AGENTS.md "
                            "or kernel changes do — " + remedy)]
    else:
        # Backward-compatible but loud.  A legacy timestamp can establish
        # freshness only; it cannot establish which contract was emitted.
        return [Finding(SEV_WARNING, "_session-gate",
                        "session gate: legacy attestation has no contract "
                        "fingerprint — freshness is known but contract currency "
                        "is not; " + remedy)]
    return []


def cmd_validate(args) -> int:
    root = Path(args.path).resolve()
    mode = getattr(args, "view", "worktree")
    try:
        view = (RepositoryView.index(root) if mode == "index"
                else RepositoryView.worktree(root))
    except RepositoryViewError as exc:
        print(f"mdllm: cannot construct {mode} validation view: {exc}")
        return 1
    reports = validation_reports(root, view)

    total_errors = 0
    for rpt_root, rpt_corpus, rpt_findings in reports:
        errors = [x for x in rpt_findings if x.severity == SEV_ERROR]
        warnings = [x for x in rpt_findings if x.severity == SEV_WARNING]
        infos = [x for x in rpt_findings if x.severity == SEV_INFO]
        total_errors += len(errors)

        if not args.quiet or errors:
            print(f"## Validation Report — {rpt_root}")
            print(f"view: {rpt_corpus.view.identifier if rpt_corpus.view else view.identifier}")
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
