"""Route HTTP-shaped inputs into application use cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import (
    CollectionItem, CommitDetail, DocumentRecord, EstateSnapshot, HistoricalDocument, OverviewRecord, Page,
    SourceSettingsRecord, TreeNode,
)


class DiscoverEstateUseCase(Protocol):
    def execute(self) -> EstateSnapshot: ...


class OverviewUseCase(Protocol):
    def execute(self, source_id: str, cursor: str | None) -> OverviewRecord: ...


class TreeUseCase(Protocol):
    def execute(self, source_id: str, path: str | None, cursor: str | None) -> Page[TreeNode]: ...


class SearchUseCase(Protocol):
    def execute(self, source_id: str, query: str, cursor: str | None) -> Page[TreeNode]: ...


class CollectionUseCase(Protocol):
    def execute(self, source_id: str, kind: str, cursor: str | None) -> Page[CollectionItem]: ...


class SettingsUseCase(Protocol):
    def execute(self, source_id: str) -> SourceSettingsRecord: ...


class DocumentUseCase(Protocol):
    def execute(self, source_id: str, path: str, mode: str) -> DocumentRecord: ...


class CommitUseCase(Protocol):
    def execute(self, source_id: str, sha: str) -> CommitDetail: ...


class HistoricalDocumentUseCase(Protocol):
    def execute(self, source_id: str, sha: str, path: str) -> HistoricalDocument: ...


@dataclass(frozen=True)
class ExplorerUseCases:
    discover_estate: DiscoverEstateUseCase
    get_overview: OverviewUseCase
    browse_tree: TreeUseCase
    search_paths: SearchUseCase
    list_collection: CollectionUseCase
    get_settings: SettingsUseCase
    read_document: DocumentUseCase
    get_commit: CommitUseCase
    read_historical_document: HistoricalDocumentUseCase


class ApiRoutes:
    def __init__(self, use_cases: ExplorerUseCases) -> None:
        self._use_cases = use_cases

    def dispatch(self, path: str, query: dict[str, list[str]]):
        if path == "/api/v1/estate":
            self._only(query, set())
            return self._use_cases.discover_estate.execute()
        if path == "/api/v1/overview":
            self._only(query, {"source", "cursor"})
            return self._use_cases.get_overview.execute(self._required(query, "source"), self._optional(query, "cursor"))
        if path == "/api/v1/tree":
            self._only(query, {"source", "path", "cursor"})
            return self._use_cases.browse_tree.execute(self._required(query, "source"), self._optional(query, "path"), self._optional(query, "cursor"))
        if path == "/api/v1/search":
            self._only(query, {"source", "q", "cursor"})
            return self._use_cases.search_paths.execute(self._required(query, "source"), self._required(query, "q"), self._optional(query, "cursor"))
        if path == "/api/v1/collection":
            self._only(query, {"source", "kind", "cursor"})
            return self._use_cases.list_collection.execute(self._required(query, "source"), self._required(query, "kind"), self._optional(query, "cursor"))
        if path == "/api/v1/settings":
            self._only(query, {"source"})
            return self._use_cases.get_settings.execute(self._required(query, "source"))
        if path == "/api/v1/document":
            self._only(query, {"source", "path", "mode"})
            return self._use_cases.read_document.execute(self._required(query, "source"), self._required(query, "path"), self._optional(query, "mode") or "rendered")
        if path == "/api/v1/commit":
            self._only(query, {"source", "sha"})
            return self._use_cases.get_commit.execute(self._required(query, "source"), self._required(query, "sha"))
        if path == "/api/v1/commit-file":
            self._only(query, {"source", "sha", "path"})
            return self._use_cases.read_historical_document.execute(
                self._required(query, "source"), self._required(query, "sha"), self._required(query, "path")
            )
        raise ExplorerError("route_not_found")

    @staticmethod
    def _only(query: dict[str, list[str]], allowed: set[str]) -> None:
        if set(query) - allowed or any(len(values) != 1 for values in query.values()):
            raise ExplorerError("invalid_request")

    @staticmethod
    def _required(query: dict[str, list[str]], key: str) -> str:
        value = ApiRoutes._optional(query, key)
        if value is None or value == "":
            raise ExplorerError("invalid_request")
        return value

    @staticmethod
    def _optional(query: dict[str, list[str]], key: str) -> str | None:
        values = query.get(key)
        return values[0] if values else None
