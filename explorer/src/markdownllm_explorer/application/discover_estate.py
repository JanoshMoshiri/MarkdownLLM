from __future__ import annotations

from .ports import SourceCatalogue


class DiscoverEstate:
    def __init__(self, catalogue: SourceCatalogue) -> None:
        self._catalogue = catalogue

    def execute(self):
        return self._catalogue.discover()

