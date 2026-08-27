"""Typed errors crossing Explorer application boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorDefinition:
    status: int
    retryable: bool
    public_message: str


ERRORS: dict[str, ErrorDefinition] = {
    "invalid_request": ErrorDefinition(400, False, "The request is invalid."),
    "invalid_path": ErrorDefinition(400, False, "The requested path is invalid."),
    "invalid_cursor": ErrorDefinition(400, False, "The page cursor is invalid."),
    "invalid_query": ErrorDefinition(400, False, "The search query is invalid."),
    "capability_required": ErrorDefinition(401, False, "A launch capability is required."),
    "capability_invalid": ErrorDefinition(401, False, "The launch capability is invalid."),
    "host_forbidden": ErrorDefinition(403, False, "The request host is not permitted."),
    "origin_forbidden": ErrorDefinition(403, False, "The request origin is not permitted."),
    "path_excluded": ErrorDefinition(403, False, "The requested path is not available."),
    "path_outside_source": ErrorDefinition(403, False, "The requested path is outside this source."),
    "route_not_found": ErrorDefinition(404, False, "The requested route does not exist."),
    "source_not_found": ErrorDefinition(404, False, "The requested source does not exist."),
    "file_not_found": ErrorDefinition(404, False, "The requested file does not exist."),
    "method_not_allowed": ErrorDefinition(405, False, "The request method is not allowed."),
    "source_changed": ErrorDefinition(409, True, "The source changed while it was being read."),
    "source_id_collision": ErrorDefinition(409, False, "Two sources have the same normalised identity."),
    "path_type_changed": ErrorDefinition(409, True, "The path changed type while it was being read."),
    "file_too_large": ErrorDefinition(413, False, "The file exceeds the Explorer size limit."),
    "response_too_large": ErrorDefinition(413, False, "The response exceeds the Explorer size limit."),
    "directory_limit": ErrorDefinition(413, False, "The directory exceeds the Explorer scan limit."),
    "binary_unsupported": ErrorDefinition(415, False, "Binary files are not displayed."),
    "encoding_unsupported": ErrorDefinition(415, False, "The file is not supported UTF-8 text."),
    "server_busy": ErrorDefinition(429, True, "Explorer is busy. Try again."),
    "source_unreadable": ErrorDefinition(503, True, "The source cannot be read."),
    "git_unavailable": ErrorDefinition(503, False, "Git history is unavailable for this source."),
    "git_timeout": ErrorDefinition(503, True, "Git did not respond within the time limit."),
    "git_store_external": ErrorDefinition(503, False, "This repository uses an external git store that v1 does not read."),
    "internal_error": ErrorDefinition(500, False, "Explorer could not complete the request."),
}


class ExplorerError(Exception):
    """An expected, safely reportable Explorer failure."""

    def __init__(
        self,
        code: str,
        *,
        source_id: str | None = None,
        relative_path: str | None = None,
        detail: str | None = None,
    ) -> None:
        if code not in ERRORS:
            raise ValueError(f"unknown Explorer error code: {code}")
        self.code = code
        self.source_id = source_id
        self.relative_path = relative_path
        self.detail = detail
        super().__init__(detail or ERRORS[code].public_message)

    @property
    def status(self) -> int:
        return ERRORS[self.code].status

    @property
    def retryable(self) -> bool:
        return ERRORS[self.code].retryable

    @property
    def public_message(self) -> str:
        return ERRORS[self.code].public_message

