from __future__ import annotations

from markdownllm_explorer.core.models import CommitDetail, CommitFile

from .ports import CommitDetails, PathAdmission, SourceCatalogue


class GetCommit:
    """List the paths one commit touched, marking which this source may open.

    Git answers what changed; it does not answer what this source is allowed to
    show.  A commit in a substrate repository can name a secret, a path under an
    ignored directory, or a file a nested domain owns.  Admission decides that,
    and a deleted path is never openable because the commit left no content
    behind for it.
    """

    def __init__(self, catalogue: SourceCatalogue, history: CommitDetails, admission: PathAdmission) -> None:
        self._catalogue, self._history, self._admission = catalogue, history, admission

    def execute(self, source_id: str, sha: str) -> CommitDetail:
        source = self._catalogue.source(source_id)
        detail = self._history.detail(source.boundary_token, sha)
        files = tuple(
            CommitFile(
                entry.path,
                entry.change,
                entry.change != "deleted" and self._admission.admits(source.boundary_token, entry.path),
            )
            for entry in detail.files
        )
        return CommitDetail(detail.sha, detail.subject, detail.author_name, detail.authored_at, files, detail.partial)
