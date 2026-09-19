"""Who acts at a workflow stage — the declared half of turn-taking.

`workflow-state.md` has always carried *who acts* as two declarations in a
definition's body: execution responsibility, and gate authority. It also
carried the condition under which the execution half becomes data:

    machine-readable modality fields enter only when at least two live
    modules need automation to consume them.

That condition was met on 2026-09-19. Two live workflow definitions run a
two-instance turn-taking loop, and three shell watchers had the role -> wake
table hardcoded in `case` statements. The role was already machine-consumed;
it was consumed from bash. `stages[].actor` promotes an existing fact into
the definition that owns it.

This module is deliberately small and has one reason to change: the meaning
of a stage's `actor`. Two callers read it — `validate` (shape) and `watch`
(which stages wake this role). Neither owns it, so it lives here.

**What an actor is not.** It is not gate authority. A stage may be executed
by an agent and authorised by a human, and `workflow-state.md` keeps that
distinction in prose precisely because collapsing the two would let a
declaration look like permission. `actor` says who *acts*; it never says who
may accept the result. The framework's standing boundary applies unchanged:
the irreversible act stays with the human, and no field relocates it.
"""

from __future__ import annotations

from .model import SEV_ERROR, Corpus, Finding

__all__ = [
    "stage_actors",
    "declared_actors",
    "stages_for_actor",
    "workflow_actor_findings",
]


def stage_actors(stage: object) -> list[str]:
    """The actors declared on one stage, normalised to a list of names.

    Accepts a bare string (one actor) or a list of strings (several — a stage
    two roles may act on is legitimate and needs no separate shape). Anything
    else yields an empty list; the shape check reports it rather than this
    silently accepting it.
    """
    if not isinstance(stage, dict):
        return []
    declared = stage.get("actor")
    if isinstance(declared, str):
        return [declared] if declared.strip() else []
    if isinstance(declared, list):
        return [a.strip() for a in declared
                if isinstance(a, str) and a.strip()]
    return []


def declared_actors(definition_meta: dict) -> set[str]:
    """Every actor named anywhere in a definition's stage set."""
    actors: set[str] = set()
    for stage in (definition_meta or {}).get("stages") or []:
        actors.update(stage_actors(stage))
    return actors


def stages_for_actor(definition_meta: dict, actor: str) -> list[str]:
    """The stage ids at which ``actor`` acts, in declaration order.

    This is the wake table: a watcher armed for a role rises when a thing it
    watches enters one of these stages. Declaration order is preserved because
    a definition's stage order is the author's reading order, and a report
    that reorders it is harder to check against the file.
    """
    matched: list[str] = []
    for stage in (definition_meta or {}).get("stages") or []:
        if not isinstance(stage, dict):
            continue
        stage_id = stage.get("id")
        if isinstance(stage_id, str) and actor in stage_actors(stage):
            matched.append(stage_id)
    return matched


def workflow_actor_findings(corpus: Corpus) -> list[Finding]:
    """Shape-check `stages[].actor` wherever a definition declares one.

    Deliberately narrow. The field is optional, so a definition that declares
    no actor is silent here — every definition written before this field
    existed stays valid, and a domain that never automates a handover never
    meets the check. What is reported is a declaration that cannot be
    consumed: a non-string actor, or an empty one.

    Membership of a *role argument* against these names is `watch`'s check,
    not this one. A definition is not wrong for declaring an actor nothing
    currently watches for.
    """
    findings: list[Finding] = []
    for thing in corpus.things:
        if str(thing.meta.get("type")) != "workflow-definition":
            continue
        name = thing.id or thing.path.name
        for stage in thing.meta.get("stages") or []:
            if not isinstance(stage, dict):
                continue
            stage_id = stage.get("id")
            label = stage_id if isinstance(stage_id, str) else "<unnamed stage>"
            if "actor" not in stage:
                continue
            declared = stage.get("actor")
            if isinstance(declared, str):
                if not declared.strip():
                    findings.append(Finding(
                        SEV_ERROR, name,
                        f"stage `{label}` declares an empty `actor` — name the "
                        "role that acts, or omit the field",
                    ))
                continue
            if isinstance(declared, list):
                if not declared:
                    findings.append(Finding(
                        SEV_ERROR, name,
                        f"stage `{label}` declares an empty `actor` list — name "
                        "the roles that act, or omit the field",
                    ))
                    continue
                for entry in declared:
                    if not isinstance(entry, str) or not entry.strip():
                        findings.append(Finding(
                            SEV_ERROR, name,
                            f"stage `{label}` declares a non-name in `actor` "
                            f"({entry!r}) — every actor is a role name",
                        ))
                continue
            findings.append(Finding(
                SEV_ERROR, name,
                f"stage `{label}` declares `actor` as {type(declared).__name__}"
                " — a role name, or a list of role names",
            ))
    return findings
