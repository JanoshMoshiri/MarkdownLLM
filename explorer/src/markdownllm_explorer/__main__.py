"""Command-line entry point."""

from __future__ import annotations

import argparse
import signal
import sys
from pathlib import Path

from .composition import build_runtime
from .core.errors import ExplorerError
from .delivery.http_server import serve


def _port(value: str) -> int:
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def main() -> int:
    parser = argparse.ArgumentParser(description="Explore a MarkdownLLM substrate and domain estate")
    parser.add_argument("--root", type=Path, required=True, help="substrate root")
    parser.add_argument("--domain-dir", default="domain", help="one-level domain directory relative to root")
    parser.add_argument("--port", type=_port, default=0, help="loopback port (default: choose an available port)")
    arguments = parser.parse_args()
    try:
        resolved_root = arguments.root.expanduser().resolve(strict=True)
        runtime = build_runtime(resolved_root, arguments.domain_dir)
        server, url = serve(runtime, arguments.port)
    except (ExplorerError, OSError) as error:
        code = error.code if isinstance(error, ExplorerError) else "startup_failed"
        message = error.public_message if isinstance(error, ExplorerError) else "Explorer could not bind the requested loopback port."
        print(f"Explorer startup failed [{code}]: {message}", file=sys.stderr)
        return 2
    print(f"Root: {resolved_root}", flush=True)
    print(f"MarkdownLLM Explorer: {url}", flush=True)
    print("Read-only local service. Press Ctrl+C to stop.", flush=True)
    if hasattr(signal, "SIGBREAK"):
        # Windows process-group CTRL_BREAK is the testable equivalent of an
        # interactive console interrupt.  Convert it to the same controlled
        # shutdown path as Ctrl+C/SIGINT instead of accepting STATUS_CONTROL_C_EXIT.
        signal.signal(signal.SIGBREAK, _raise_keyboard_interrupt)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.join_active(4.5)
    return 0


def _raise_keyboard_interrupt(signum, frame) -> None:
    raise KeyboardInterrupt


if __name__ == "__main__":
    raise SystemExit(main())
