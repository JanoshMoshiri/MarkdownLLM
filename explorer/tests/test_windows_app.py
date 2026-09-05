from __future__ import annotations

import threading

import pytest

from markdownllm_explorer.windows_app import (
    DesktopExplorerSession,
    WindowsLaunchArguments,
    run_windows_application,
)


class FakeServer:
    def __init__(self):
        self.started = threading.Event()
        self.stopped = threading.Event()
        self.closed = False
        self.join_timeout = None

    def serve_forever(self, poll_interval=0.2):
        self.started.set()
        self.stopped.wait(timeout=3)

    def shutdown(self):
        self.stopped.set()

    def server_close(self):
        self.closed = True

    def join_active(self, timeout):
        self.join_timeout = timeout


class FakeTraySurface:
    def __init__(self):
        self.labels = []

    def run(self, open_explorer, exit_explorer):
        self.labels = ["Open Explorer", "Exit Explorer"]
        open_explorer()
        exit_explorer()

    def stop(self):
        return


class BlockingTraySurface:
    def __init__(self):
        self.stopped = threading.Event()

    def run(self, open_explorer, exit_explorer):
        self.stopped.wait(timeout=2)

    def stop(self):
        self.stopped.set()


class FinishedServer(FakeServer):
    def serve_forever(self, poll_interval=0.2):
        self.started.set()


class FakeInstanceCoordinator:
    def __init__(self, primary: bool, *, primary_exits: bool = True):
        self.primary = primary
        self.primary_exits = primary_exits
        self.commands = []
        self.exit_waits = []
        self.open_handler = None
        self.exit_handler = None
        self.closed = False

    def send(self, command: str) -> bool:
        self.commands.append(command)
        return True

    def wait_for_primary_exit(self, timeout_seconds: float) -> bool:
        self.exit_waits.append(timeout_seconds)
        return self.primary_exits

    def listen(self, open_handler, exit_handler):
        self.open_handler = open_handler
        self.exit_handler = exit_handler

    def close(self):
        self.closed = True


@pytest.mark.unit
def test_desktop_session_opens_browser_and_shuts_down_cleanly():
    server = FakeServer(); tray = FakeTraySurface(); opened = []
    session = DesktopExplorerSession(server, "http://127.0.0.1:7123/#cap=opaque", opened.append, tray)

    session.run(open_on_start=True)

    assert server.started.is_set()
    assert opened == ["http://127.0.0.1:7123/#cap=opaque"] * 2
    assert tray.labels == ["Open Explorer", "Exit Explorer"]
    assert server.stopped.is_set() and server.closed and server.join_timeout == 4.5
    assert not any(thread.name == "explorer-desktop-server" for thread in threading.enumerate())


@pytest.mark.unit
def test_desktop_session_server_exit_stops_tray():
    server = FinishedServer(); tray = BlockingTraySurface()
    session = DesktopExplorerSession(server, "http://127.0.0.1:7123/#cap=opaque", lambda _: None, tray)

    session.run(open_on_start=False)

    assert server.started.is_set() and tray.stopped.is_set()
    assert server.closed and server.join_timeout == 4.5
    assert not any(thread.name == "explorer-desktop-server" for thread in threading.enumerate())


@pytest.mark.unit
def test_secondary_activation_sends_only_open_without_composing_runtime(tmp_path):
    coordinator = FakeInstanceCoordinator(primary=False)
    arguments = WindowsLaunchArguments(root=tmp_path, domain_dir="domain", port=0, no_browser=False, no_tray=False, request_exit=False)

    result = run_windows_application(
        arguments,
        runtime_builder=lambda *args: pytest.fail("secondary activation must not build runtime"),
        server_factory=lambda *args: pytest.fail("secondary activation must not bind server"),
        coordinator=coordinator,
        browser_opener=lambda url: pytest.fail("secondary process must not receive capability URL"),
        tray_factory=lambda: pytest.fail("secondary process must not create tray"),
        error_reporter=lambda message: pytest.fail(message),
    )

    assert result == 0 and coordinator.commands == ["open"] and not coordinator.exit_waits and coordinator.closed


@pytest.mark.unit
def test_secondary_exit_command_stops_existing_instance_without_capability(tmp_path):
    coordinator = FakeInstanceCoordinator(primary=False)
    arguments = WindowsLaunchArguments(root=tmp_path, domain_dir="domain", port=0, no_browser=True, no_tray=True, request_exit=True)

    result = run_windows_application(
        arguments,
        runtime_builder=lambda *args: pytest.fail("exit request must not build runtime"),
        server_factory=lambda *args: pytest.fail("exit request must not bind server"),
        coordinator=coordinator,
        browser_opener=lambda url: pytest.fail("exit request must not open browser"),
        tray_factory=lambda: pytest.fail("exit request must not create tray"),
        error_reporter=lambda message: pytest.fail(message),
    )

    assert result == 0 and coordinator.commands == ["exit"] and coordinator.exit_waits == [15.0] and coordinator.closed


@pytest.mark.unit
def test_secondary_exit_fails_closed_when_primary_does_not_terminate(tmp_path):
    coordinator = FakeInstanceCoordinator(primary=False, primary_exits=False)
    arguments = WindowsLaunchArguments(
        root=tmp_path,
        no_browser=True,
        no_tray=True,
        request_exit=True,
    )

    result = run_windows_application(
        arguments,
        runtime_builder=lambda *args: pytest.fail("exit request must not build runtime"),
        server_factory=lambda *args: pytest.fail("exit request must not bind server"),
        coordinator=coordinator,
        browser_opener=lambda url: pytest.fail("exit request must not open browser"),
        tray_factory=lambda: pytest.fail("exit request must not create tray"),
        error_reporter=lambda message: pytest.fail(message),
    )

    assert result == 4
    assert coordinator.commands == ["exit"] and coordinator.exit_waits == [15.0]
    assert coordinator.closed


@pytest.mark.unit
def test_primary_application_wires_existing_runtime_and_in_memory_open_channel(tmp_path):
    coordinator = FakeInstanceCoordinator(primary=True); server = FakeServer(); tray = FakeTraySurface(); opened = []
    runtime = object(); build_calls = []; serve_calls = []
    arguments = WindowsLaunchArguments(root=tmp_path, domain_dir="domains-custom", port=43120, no_browser=False, no_tray=False, request_exit=False)

    result = run_windows_application(
        arguments,
        runtime_builder=lambda root, domain: build_calls.append((root, domain)) or runtime,
        server_factory=lambda value, port: serve_calls.append((value, port)) or (server, "http://127.0.0.1:43120/#cap=secret"),
        coordinator=coordinator,
        browser_opener=opened.append,
        tray_factory=lambda: tray,
        error_reporter=lambda message: pytest.fail(message),
    )

    assert result == 0
    assert build_calls == [(tmp_path, "domains-custom")] and serve_calls == [(runtime, 43120)]
    assert coordinator.open_handler is not None and coordinator.exit_handler is not None and coordinator.closed
    assert opened == ["http://127.0.0.1:43120/#cap=secret"] * 2


@pytest.mark.unit
def test_startup_failure_is_bounded_and_redacted(tmp_path):
    coordinator = FakeInstanceCoordinator(primary=True); messages = []
    arguments = WindowsLaunchArguments(root=tmp_path, domain_dir="domain", port=0, no_browser=False, no_tray=False, request_exit=False)

    result = run_windows_application(
        arguments,
        runtime_builder=lambda *args: (_ for _ in ()).throw(OSError(f"secret path {tmp_path}")),
        server_factory=lambda *args: pytest.fail("server must not run after startup failure"),
        coordinator=coordinator,
        browser_opener=lambda url: pytest.fail("browser must not open after startup failure"),
        tray_factory=lambda: pytest.fail("tray must not open after startup failure"),
        error_reporter=messages.append,
    )

    assert result == 2 and messages == ["Explorer could not start. Check that the selected MarkdownLLM folder still exists and try again."]
    assert str(tmp_path) not in messages[0] and coordinator.closed
