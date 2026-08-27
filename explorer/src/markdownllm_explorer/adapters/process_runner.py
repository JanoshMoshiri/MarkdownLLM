"""Shell-free process execution with deadline and pre-allocation output bounds."""

from __future__ import annotations

import os
import queue
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from markdownllm_explorer.core.errors import ExplorerError


@dataclass(frozen=True)
class ProcessRequest:
    executable: str
    arguments: tuple[str, ...]
    cwd: Path
    environment: dict[str, str]
    timeout_seconds: float
    output_limit: int


@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    output: bytes


class BoundedProcessRunner:
    """Capture combined output without ever retaining more than limit+1 bytes."""

    def run(self, request: ProcessRequest) -> ProcessResult:
        command = [request.executable, *request.arguments]
        creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            process = subprocess.Popen(
                command,
                cwd=request.cwd,
                env=request.environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False,
                creationflags=creationflags,
            )
        except OSError:
            raise ExplorerError("git_unavailable") from None
        # Two fixed-size chunks bound the producer even when a child writes faster
        # than the consumer can validate the configured capture budget.
        chunks: queue.Queue[bytes | BaseException | None] = queue.Queue(maxsize=2)

        def drain() -> None:
            try:
                assert process.stdout is not None
                while True:
                    chunk = process.stdout.read(64 * 1024)
                    if not chunk:
                        break
                    chunks.put(chunk)
            except BaseException as error:  # pragma: no cover - OS pipe failure
                chunks.put(error)
            finally:
                chunks.put(None)

        reader = threading.Thread(target=drain, name="explorer-process-capture", daemon=True)
        reader.start()
        deadline = time.monotonic() + request.timeout_seconds
        captured = bytearray()
        finished = False
        try:
            while not finished:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ExplorerError("git_timeout")
                try:
                    item = chunks.get(timeout=min(remaining, 0.1))
                except queue.Empty:
                    if process.poll() is not None and not reader.is_alive():
                        break
                    continue
                if item is None:
                    finished = True
                elif isinstance(item, BaseException):
                    raise ExplorerError("git_unavailable")
                else:
                    remaining_bytes = request.output_limit + 1 - len(captured)
                    captured.extend(item[:remaining_bytes])
                    if len(captured) > request.output_limit:
                        raise ExplorerError("git_unavailable", detail="git output limit exceeded")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ExplorerError("git_timeout")
            returncode = process.wait(timeout=remaining)
            return ProcessResult(returncode, bytes(captured))
        except ExplorerError:
            process.kill()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:  # pragma: no cover - exceptional OS failure
                pass
            raise
        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:  # pragma: no cover
                pass
            raise ExplorerError("git_timeout") from None
        finally:
            if process.stdout is not None:
                process.stdout.close()
