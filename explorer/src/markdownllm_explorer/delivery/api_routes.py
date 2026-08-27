"""Route HTTP-shaped inputs into application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from markdownllm_explorer.core.errors import ExplorerError


@dataclass(frozen=True)
class ExplorerUseCases:
    discover_estate: object
    get_overview: object
    browse_tree: object
    search_paths: object
    list_collection: object
    get_settings: object
    read_document: object


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

