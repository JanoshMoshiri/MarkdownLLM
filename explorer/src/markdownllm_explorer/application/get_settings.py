from __future__ import annotations

from .ports import SourceBrowser, SourceCatalogue


class GetSettings:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceBrowser) -> None:
        self._catalogue, self._browser = catalogue, browser

    def execute(self, source_id: str):
        source = self._catalogue.source(source_id)
        return self._browser.settings(source.boundary_token)

