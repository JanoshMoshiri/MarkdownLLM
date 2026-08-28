from __future__ import annotations

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import HistoricalDocument, RelativePath

from .ports import CommitDetails, PathAdmission, SourceCatalogue


class ReadHistoricalDocument:
    """Read a file as one commit left it.

    Admission is checked here, before any git invocation, so a path this source
    would refuse in the working tree cannot be reached through history instead.
    That ordering is the point: the object store holds every path the repository
    ever contained, including ones the live reader excludes today.
    """

    def __init__(self, catalogue: SourceCatalogue, history: CommitDetails, admission: PathAdmission) -> None:
        self._catalogue, self._history, self._admission = catalogue, history, admission

    def execute(self, source_id: str, sha: str, path: str) -> HistoricalDocument:
        source = self._catalogue.source(source_id)
        relative = RelativePath.parse(path)
        if not self._admission.admits(source.boundary_token, relative):
            raise ExplorerError("path_excluded")
        return self._history.historical(source.boundary_token, sha, relative)
