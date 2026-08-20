"""Neutral process boundary for authenticated Git commands.

Sync, assembly, and publication all need the same small transport mechanics,
but none of those application services should own a dependency of the other
two.  This module owns only command construction, command-scoped credentials,
and output redaction; repository policy remains with its application service.
"""

from __future__ import annotations

import base64
import os
import re
import subprocess
from pathlib import Path


TOKEN_ENV_VARS = ("GH_PAT", "MDLLM_GIT_TOKEN")

_TOKEN_PATTERNS = (
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"ghp_[A-Za-z0-9]+"),
)


def command_token() -> str | None:
    """Return the optional command-scoped Git credential."""
    for variable in TOKEN_ENV_VARS:
        value = os.environ.get(variable, "").strip()
        if value:
            return value
    return None


def redact(text: str, token: str | None = None) -> str:
    """Remove supported credential shapes from process output."""
    for pattern in _TOKEN_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    if token:
        text = text.replace(token, "[REDACTED]")
        encoded = base64.b64encode(
            f"x-access-token:{token}".encode()).decode()
        text = text.replace(encoded, "[REDACTED]")
    return text


def git_command(
        repo: Path,
        *args: str,
        token: str | None = None,
        timeout: float | None = None,
        non_interactive: bool = False,
) -> subprocess.CompletedProcess[str] | None:
    """Run Git with optional process-scoped auth; return ``None`` on timeout.

    ``non_interactive`` is explicit because lifecycle sync must degrade rather
    than prompt, while operator-invoked publication may use ambient credential
    helpers.  A supplied token is encoded only in this child process command;
    it is never written to a URL, environment variable, or Git configuration.
    """
    command = ["git", "-C", str(repo)]
    if token:
        auth = base64.b64encode(
            f"x-access-token:{token}".encode()).decode()
        command += ["-c", f"http.extraheader=Authorization: Basic {auth}"]
    command += list(args)

    env = None
    if non_interactive:
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        env.setdefault("GCM_INTERACTIVE", "never")
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None
