"""Curated Skills and Memory projection over confined filesystem reads."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from markdownllm_explorer.core.collection_policy import memory_group_for
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import BoundaryToken, CollectionItem, FrontmatterState, Page, RelativePath

from .confined_source_reader import ConfinedSourceReader
from .cursors import CursorCodec, CursorState
from .filesystem_catalogue import BoundaryRegistry
from .frontmatter_parser import FrontmatterParser


class CuratedCollectionReader:
    def __init__(
        self, filesystem: ConfinedSourceReader, registry: BoundaryRegistry,
        frontmatter: FrontmatterParser, cursors: CursorCodec, limits: ExplorerLimits,
    ) -> None:
        self._filesystem = filesystem
        self._registry = registry
        self._frontmatter = frontmatter
        self._cursors = cursors
        self._limits = limits

    def collection(self, token: BoundaryToken, kind: str, cursor: str | None) -> Page[CollectionItem]:
        if kind not in {"skills", "memory"}:
            raise ExplorerError("invalid_request")
        boundary = self._registry.by_token(token)
        candidates: list[CollectionItem] = []
        ids: dict[str, list[int]] = {}
        scanned = 0
        partial = False
        try:
            for relative, _ in self._filesystem.iter_files(token):
                scanned += 1
                group = self._group(relative, kind)
                if group:
                    item = self._item(token, relative, kind, group)
                    item_index = len(candidates)
                    candidates.append(item)
                    if item.thing_id:
                        ids.setdefault(item.thing_id, []).append(item_index)
                if scanned >= self._limits.candidate_scan or len(candidates) >= self._limits.memory_candidates:
                    partial = True
                    break
        except ExplorerError as error:
            if error.code != "directory_limit":
                raise
            partial = True
        for indexes in ids.values():
            if len(indexes) > 1:
                for item_index in indexes:
                    item = candidates[item_index]
                    candidates[item_index] = CollectionItem(item.path, item.title, item.group, item.thing_id, item.thing_type, (*item.issues, "duplicate_id"))
        # Groups run Z to A so the sections a reader reaches for most are not
        # buried by an accident of the alphabet; titles inside a group stay A to Z.
        # Two stable passes rather than one key, because a descending string key
        # cannot be expressed by negation the way a numeric one can.
        candidates.sort(key=lambda item: (item.title.casefold(), item.path.value))
        candidates.sort(key=lambda item: item.group.casefold(), reverse=True)
        revision = hashlib.sha256("\n".join(repr(item) for item in candidates).encode()).hexdigest() + ("-partial" if partial else "")
        state = self._cursors.decode(cursor, operation="collection", source=boundary.source.id.value, context=kind)
        if state.revision and state.revision != revision:
            raise ExplorerError("source_changed")
        selected = tuple(candidates[state.offset:state.offset + self._limits.search_page])
        next_cursor = None
        if state.offset + self._limits.search_page < len(candidates):
            next_cursor = self._cursors.encode(CursorState("collection", boundary.source.id.value, kind, state.offset + self._limits.search_page, revision))
        return Page(selected, next_cursor, partial, datetime.now(timezone.utc).isoformat())

    def _item(self, token: BoundaryToken, relative: RelativePath, kind: str, group: str) -> CollectionItem:
        issues: list[str] = []
        title = relative.name.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
        thing_id = thing_type = None
        try:
            raw = self._filesystem.read(token, relative)
            parsed = self._frontmatter.parse(raw.text)
            if parsed.frontmatter.state is FrontmatterState.VALID:
                thing_id = _string(parsed.frontmatter.values.get("id"))
                thing_type = _string(parsed.frontmatter.values.get("type"))
                title = _title(parsed.body) or title
            elif parsed.frontmatter.state is FrontmatterState.INVALID:
                issues.append("frontmatter_invalid")
            elif kind == "memory":
                issues.append("frontmatter_missing")
        except ExplorerError as error:
            issues.append(error.code)
        return CollectionItem(relative, title, group, thing_id, thing_type, tuple(issues))

    @staticmethod
    def _group(relative: RelativePath, kind: str) -> str | None:
        if kind == "skills":
            return "Skills" if relative.parts and relative.parts[0].casefold() == "skills" and relative.name.casefold().endswith((".md", ".markdown")) else None
        return memory_group_for(relative)


def _string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _title(body: str) -> str | None:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None

