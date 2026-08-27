from __future__ import annotations

from .ports import SettingsReader, SourceCatalogue


class GetSettings:
    def __init__(self, catalogue: SourceCatalogue, browser: SettingsReader) -> None:
        self._catalogue, self._browser = catalogue, browser

    def execute(self, source_id: str):
        source = self._catalogue.source(source_id)
        return self._browser.settings(source.boundary_token)
