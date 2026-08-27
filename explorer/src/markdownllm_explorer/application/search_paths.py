from __future__ import annotations

from .ports import SourceBrowser, SourceCatalogue


class SearchPaths:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceBrowser) -> None:
        self._catalogue, self._browser = catalogue, browser

    def execute(self, source_id: str, query: str, cursor: str | None = None):
        source = self._catalogue.source(source_id)
        return self._browser.search(source.boundary_token, query, cursor)

