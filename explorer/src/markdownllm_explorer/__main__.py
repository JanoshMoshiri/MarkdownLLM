"""Command-line entry point."""

from __future__ import annotations

import argparse
import signal
import sys
import webbrowser
from pathlib import Path

from .composition import build_runtime, build_server
from .core.errors import ExplorerError


def _port(value: str) -> int:
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def main(argv: list[str] | None = None, *, browser_opener=webbrowser.open) -> int:
    parser = argparse.ArgumentParser(description="Explore a MarkdownLLM substrate and domain estate")
    parser.add_argument("--root", type=Path, required=True, help="substrate root")
    parser.add_argument("--domain-dir", default="domain", help="one-level domain directory relative to root")
    parser.add_argument("--port", type=_port, default=0, help="loopback port (default: choose an available port)")
    parser.add_argument("--open-browser", action="store_true", help="open Explorer in the default browser")
    arguments = parser.parse_args(argv)
    try:
        resolved_root = arguments.root.expanduser().resolve(strict=True)
        runtime = build_runtime(resolved_root, arguments.domain_dir)
        server, url = build_server(runtime, arguments.port)
    except (ExplorerError, OSError) as error:
        code = error.code if isinstance(error, ExplorerError) else "startup_failed"
        message = error.public_message if isinstance(error, ExplorerError) else "Explorer could not bind the requested loopback port."
        print(f"Explorer startup failed [{code}]: {message}", file=sys.stderr)
        return 2
    print(f"Root: {resolved_root}", flush=True)
    print(f"MarkdownLLM Explorer: {url}", flush=True)
    print("Read-only local service. Press Ctrl+C to stop.", flush=True)
    # A shell's background job can inherit SIGINT as ignored. Restore it so
    # the Mac launcher's --stop/relaunch can shut down a nohup child cleanly.
    stop_signals = [signal.SIGINT, signal.SIGTERM]
    if hasattr(signal, "SIGBREAK"):
        # Windows process-group CTRL_BREAK is the testable equivalent of an
        # interactive console interrupt.  Convert it to the same controlled
        # shutdown path as Ctrl+C/SIGINT instead of accepting STATUS_CONTROL_C_EXIT.
        stop_signals.append(signal.SIGBREAK)
    previous_handlers = {item: signal.signal(item, _raise_keyboard_interrupt) for item in stop_signals}
    try:
        if arguments.open_browser:
            try:
                opened = browser_opener(url)
            except Exception:
                opened = False
            if opened is False:
                print("Explorer startup failed [browser_unavailable]: Explorer could not open the default browser.", file=sys.stderr)
                return 2
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.join_active(4.5)
        for item, handler in previous_handlers.items():
            signal.signal(item, handler)
    return 0


def _raise_keyboard_interrupt(signum, frame) -> None:
    raise KeyboardInterrupt


if __name__ == "__main__":
    raise SystemExit(main())
