"""Native Windows desktop host for the local Explorer service.

This module is deliberately an outer delivery driver.  The browser application
and its read-only ports remain unchanged; this host only owns Windows lifecycle
concerns such as single-instance activation, the tray, and browser launch.
"""

from __future__ import annotations

import argparse
import ctypes
import getpass
import hashlib
import importlib.resources
import os
import threading
import time
import webbrowser
from dataclasses import dataclass
from multiprocessing.connection import Client, Listener
from pathlib import Path
from typing import Callable, Protocol

from .composition import build_runtime
from .core.errors import ExplorerError
from .delivery.http_server import serve


_STARTUP_MESSAGE = (
    "Explorer could not start. Check that the selected MarkdownLLM folder "
    "still exists and try again."
)
_COMMANDS = {"open", "exit"}
_PIPE_AUTHKEY = b"markdownllm-explorer-local-activation-v1"
_ERROR_ALREADY_EXISTS = 183


class ExplorerServer(Protocol):
    def serve_forever(self, poll_interval: float = 0.2) -> None: ...
    def shutdown(self) -> None: ...
    def server_close(self) -> None: ...
    def join_active(self, timeout: float) -> None: ...


class TraySurface(Protocol):
    def run(self, open_explorer: Callable[[], None], exit_explorer: Callable[[], None]) -> None: ...
    def stop(self) -> None: ...


@dataclass(frozen=True)
class WindowsLaunchArguments:
    root: Path
    domain_dir: str = "domain"
    port: int = 0
    no_browser: bool = False
    no_tray: bool = False
    request_exit: bool = False


class DesktopExplorerSession:
    """Own one server thread and its visible desktop controls."""

    def __init__(
        self,
        server: ExplorerServer,
        url: str,
        browser_opener: Callable[[str], object],
        tray_surface: TraySurface,
    ) -> None:
        self._server = server
        self._url = url
        self._browser_opener = browser_opener
        self._tray_surface = tray_surface
        self._server_thread: threading.Thread | None = None
        self._stopping = threading.Event()

    def open(self) -> None:
        if not self._stopping.is_set():
            self._browser_opener(self._url)

    def stop(self) -> None:
        if self._stopping.is_set():
            return
        self._stopping.set()
        self._server.shutdown()
        self._tray_surface.stop()

    def run(self, *, open_on_start: bool) -> None:
        self._server_thread = threading.Thread(
            target=self._server.serve_forever,
            kwargs={"poll_interval": 0.2},
            name="explorer-desktop-server",
            daemon=False,
        )
        self._server_thread.start()
        try:
            if open_on_start:
                self.open()
            self._tray_surface.run(self.open, self.stop)
        finally:
            self.stop()
            self._server_thread.join(5.0)
            self._server.server_close()
            self._server.join_active(4.5)


class WindowsTraySurface:
    """Small, explicit lifetime surface for a background local service."""

    def __init__(self) -> None:
        self._icon = None
        self._stop_requested = threading.Event()

    def stop(self) -> None:
        self._stop_requested.set()
        if self._icon is not None:
            self._icon.stop()

    def run(self, open_explorer: Callable[[], None], exit_explorer: Callable[[], None]) -> None:
        import pystray
        from PIL import Image

        icon_resource = importlib.resources.files(
            "markdownllm_explorer.delivery.static"
        ).joinpath("markdownllm-explorer.png")
        with icon_resource.open("rb") as icon_stream:
            icon_image = Image.open(icon_stream).convert("RGBA")

        tray_icon: pystray.Icon

        def open_from_tray(icon, item) -> None:
            open_explorer()

        def exit_from_tray(icon, item) -> None:
            exit_explorer()
            icon.stop()

        tray_icon = pystray.Icon(
            "markdownllm-explorer",
            icon_image,
            "MarkdownLLM Explorer",
            pystray.Menu(
                pystray.MenuItem("Open Explorer", open_from_tray, default=True),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit Explorer", exit_from_tray),
            ),
        )
        self._icon = tray_icon
        try:
            if not self._stop_requested.is_set():
                tray_icon.run()
        finally:
            self._icon = None


class WindowsInstanceCoordinator:
    """Per-user single-instance coordinator carrying commands, never capability data."""

    def __init__(self) -> None:
        identity = hashlib.sha256(getpass.getuser().encode("utf-8")).hexdigest()[:16]
        self._pipe_address = rf"\\.\pipe\MarkdownLLMExplorer-{identity}"
        self._mutex_handle = None
        self._listener: Listener | None = None
        self._listener_thread: threading.Thread | None = None
        self._closing = threading.Event()

        if os.name != "nt":
            self.primary = True
            return

        kernel32 = ctypes.windll.kernel32
        kernel32.CreateMutexW.restype = ctypes.c_void_p
        self._mutex_handle = kernel32.CreateMutexW(
            None, False, f"Local\\MarkdownLLMExplorer-{identity}"
        )
        if not self._mutex_handle:
            raise OSError("could not create application mutex")
        self.primary = kernel32.GetLastError() != _ERROR_ALREADY_EXISTS

    def send(self, command: str) -> bool:
        if command not in _COMMANDS:
            raise ValueError("unsupported instance command")
        if os.name != "nt":
            return False
        payload = command.encode("ascii")
        for _ in range(30):
            try:
                connection = Client(
                    self._pipe_address, family="AF_PIPE", authkey=_PIPE_AUTHKEY
                )
                try:
                    connection.send_bytes(payload)
                finally:
                    connection.close()
                return True
            except (FileNotFoundError, ConnectionRefusedError, OSError):
                time.sleep(0.1)
        return False

    def listen(
        self,
        open_handler: Callable[[], None],
        exit_handler: Callable[[], None],
    ) -> None:
        if os.name != "nt" or not self.primary:
            return
        self._listener = Listener(
            self._pipe_address, family="AF_PIPE", authkey=_PIPE_AUTHKEY
        )

        def receive_commands() -> None:
            while not self._closing.is_set():
                try:
                    connection = self._listener.accept()
                    try:
                        command = connection.recv_bytes(16).decode("ascii")
                    finally:
                        connection.close()
                except (EOFError, OSError, UnicodeError):
                    if self._closing.is_set():
                        break
                    continue
                if command == "open":
                    open_handler()
                elif command == "exit":
                    exit_handler()

        self._listener_thread = threading.Thread(
            target=receive_commands,
            name="explorer-instance-command",
            daemon=True,
        )
        self._listener_thread.start()

    def close(self) -> None:
        self._closing.set()
        if self._listener is not None:
            self._listener.close()
            self._listener = None
        if self._listener_thread is not None:
            self._listener_thread.join(1.0)
            self._listener_thread = None
        if self._mutex_handle and os.name == "nt":
            ctypes.windll.kernel32.CloseHandle(self._mutex_handle)
            self._mutex_handle = None


def run_windows_application(
    arguments: WindowsLaunchArguments,
    *,
    runtime_builder=build_runtime,
    server_factory=serve,
    coordinator: WindowsInstanceCoordinator | None = None,
    browser_opener: Callable[[str], object] | None = None,
    tray_factory: Callable[[], TraySurface] = WindowsTraySurface,
    error_reporter: Callable[[str], None] | None = None,
) -> int:
    """Compose and run the Windows host around the existing Explorer runtime."""

    instance = coordinator or WindowsInstanceCoordinator()
    report = error_reporter or _show_error
    open_browser = browser_opener or _open_default_browser
    try:
        if not instance.primary:
            command = "exit" if arguments.request_exit else "open"
            return 0 if instance.send(command) else 3
        if arguments.request_exit:
            return 0

        resolved_root = arguments.root.expanduser().resolve(strict=True)
        runtime = runtime_builder(resolved_root, arguments.domain_dir)
        server, url = server_factory(runtime, arguments.port)

        if arguments.no_tray:
            return _run_without_tray(
                instance, server, url, open_browser, not arguments.no_browser
            )

        session = DesktopExplorerSession(server, url, open_browser, tray_factory())
        instance.listen(session.open, session.stop)
        session.run(open_on_start=not arguments.no_browser)
        return 0
    except (ExplorerError, OSError, ImportError, RuntimeError):
        report(_STARTUP_MESSAGE)
        return 2
    finally:
        instance.close()


def _run_without_tray(
    instance: WindowsInstanceCoordinator,
    server: ExplorerServer,
    url: str,
    browser_opener: Callable[[str], object],
    open_on_start: bool,
) -> int:
    stopping = threading.Event()

    def open_explorer() -> None:
        if not stopping.is_set():
            browser_opener(url)

    def stop_explorer() -> None:
        stopping.set()
        server.shutdown()

    instance.listen(open_explorer, stop_explorer)
    if open_on_start:
        open_explorer()
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        stopping.set()
        server.server_close()
        server.join_active(4.5)
    return 0


def _port(value: str) -> int:
    try:
        port = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("port must be an integer") from None
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def parse_arguments(argv: list[str] | None = None) -> WindowsLaunchArguments:
    parser = argparse.ArgumentParser(description="MarkdownLLM Explorer for Windows")
    parser.add_argument("--root", type=Path, required=True, help="substrate root")
    parser.add_argument("--domain-dir", default="domain")
    parser.add_argument("--port", type=_port, default=0)
    parser.add_argument("--no-browser", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--no-tray", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--request-exit", action="store_true", help=argparse.SUPPRESS)
    values = parser.parse_args(argv)
    return WindowsLaunchArguments(
        root=values.root,
        domain_dir=values.domain_dir,
        port=values.port,
        no_browser=values.no_browser,
        no_tray=values.no_tray,
        request_exit=values.request_exit,
    )


def _show_error(message: str) -> None:
    if os.name == "nt":
        ctypes.windll.user32.MessageBoxW(
            None, message, "MarkdownLLM Explorer", 0x00000010
        )


def _open_default_browser(url: str) -> bool:
    if os.name != "nt":
        return webbrowser.open(url)
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW.restype = ctypes.c_void_p
    result = shell32.ShellExecuteW(None, "open", url, None, None, 1)
    if not result or int(result) <= 32:
        raise OSError("Windows could not open the default browser")
    return True


def main(argv: list[str] | None = None) -> int:
    return run_windows_application(parse_arguments(argv))


if __name__ == "__main__":
    raise SystemExit(main())
