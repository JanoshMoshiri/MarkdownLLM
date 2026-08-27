from __future__ import annotations

from markdownllm_explorer.core.models import OverviewRecord

from .ports import CommitHistory, SourceBrowser, SourceCatalogue


class GetOverview:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceBrowser, history: CommitHistory) -> None:
        self._catalogue, self._browser, self._history = catalogue, browser, history

    def execute(self, source_id: str, cursor: str | None = None) -> OverviewRecord:
        source = self._catalogue.source(source_id)
        repository = self._history.repository_state(source.boundary_token)
        return OverviewRecord(
            source,
            self._browser.counts(source.boundary_token),
            repository,
            self._history.commits(source.boundary_token, cursor) if repository.kind in {"repository", "unborn"} else _empty_page(),
        )


def _empty_page():
    from datetime import datetime, timezone
    from markdownllm_explorer.core.models import Page
    return Page((), None, False, datetime.now(timezone.utc).isoformat())
