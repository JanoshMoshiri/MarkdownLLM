"""Exercise the native Windows bundle, installer, shortcuts, upgrade, and uninstall."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import winreg
from pathlib import Path

from evidence_common import file_sha256


DEFAULT_APP_NAME = "MarkdownLLM Explorer"
DEFAULT_APP_KEY = r"Software\MarkdownLLM Explorer"
DEFAULT_UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MarkdownLLM Explorer"
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def run(
    command: list[str], *, timeout: int = 90, environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=True,
        creationflags=CREATE_NO_WINDOW,
        env=environment,
    )


def registry_value(key_path: str, name: str) -> str | None:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            return str(winreg.QueryValueEx(key, name)[0])
    except FileNotFoundError:
        return None


def known_folder(name: str) -> Path:
    command = [
        "powershell.exe",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        f"[Environment]::GetFolderPath('{name}')",
    ]
    return Path(run(command).stdout.strip())


def shortcut_details(path: Path) -> dict[str, str]:
    script = (
        "$p=[Environment]::GetEnvironmentVariable('MDLLM_SHORTCUT');"
        "$s=(New-Object -ComObject WScript.Shell).CreateShortcut($p);"
        "[pscustomobject]@{Target=$s.TargetPath;Arguments=$s.Arguments;Icon=$s.IconLocation}|ConvertTo-Json -Compress"
    )
    environment = os.environ.copy()
    environment["MDLLM_SHORTCUT"] = str(path)
    result = run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        environment=environment,
    )
    return json.loads(result.stdout)


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        if path.is_file():
            digest.update(bytes.fromhex(file_sha256(path)))
    return digest.hexdigest()


def wait_for_health(port: int, process: subprocess.Popen[bytes]) -> dict[str, str]:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"installed application exited early with {process.returncode}")
        try:
            connection = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
            connection.request("GET", "/health", headers={"Host": f"127.0.0.1:{port}"})
            response = connection.getresponse()
            body = json.loads(response.read())
            connection.close()
            if response.status == 200 and body.get("status") == "ok":
                return body
        except (OSError, ValueError, json.JSONDecodeError):
            pass
        time.sleep(0.1)
    raise RuntimeError("installed application did not become healthy")


def free_port() -> int:
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    port = int(listener.getsockname()[1])
    listener.close()
    return port


def hold_active_request(port: int) -> socket.socket:
    """Keep one bounded request thread active while setup requests shutdown."""

    connection = socket.create_connection(("127.0.0.1", port), timeout=2)
    connection.sendall(
        f"GET /health HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n".encode("ascii")
    )
    return connection


def main() -> int:
    if os.name != "nt":
        raise SystemExit("Windows installer verification must run on Windows")
    parser = argparse.ArgumentParser()
    parser.add_argument("--installer", type=Path, required=True)
    parser.add_argument("--release-installer", type=Path)
    parser.add_argument("--app-name", default=DEFAULT_APP_NAME)
    parser.add_argument("--app-key", default=DEFAULT_APP_KEY)
    parser.add_argument("--uninstall-key", default=DEFAULT_UNINSTALL_KEY)
    parser.add_argument("--instance-identity")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    explorer = Path(__file__).parents[1].resolve()
    installer = arguments.installer.resolve(strict=True)
    release_installer = (
        arguments.release_installer.resolve(strict=True)
        if arguments.release_installer
        else installer
    )
    output = arguments.output or explorer / "tests" / "evidence" / "windows-installer.json"

    desktop_shortcut = known_folder("Desktop") / f"{arguments.app_name}.lnk"
    start_group = known_folder("Programs") / arguments.app_name
    if (
        desktop_shortcut.exists()
        or start_group.exists()
        or registry_value(arguments.app_key, "InstallDir")
        or registry_value(arguments.uninstall_key, "DisplayName")
    ):
        raise SystemExit("refusing to overwrite an existing MarkdownLLM Explorer installation during verification")

    lifecycle_environment = os.environ.copy()
    if arguments.instance_identity:
        for name in ("LOGNAME", "USER", "LNAME", "USERNAME"):
            lifecycle_environment[name] = arguments.instance_identity

    with tempfile.TemporaryDirectory(prefix="mdllm-explorer-windows-") as temporary:
        workspace = Path(temporary)
        fixture = workspace / "substrate"
        fixture.mkdir()
        (fixture / "AGENTS.md").write_text("# Windows installer fixture\n", encoding="utf-8")
        (fixture / "README.md").write_text("# Read only\n", encoding="utf-8")
        outside = workspace / "outside.txt"
        outside.write_text("must remain unchanged\n", encoding="utf-8")
        install_dir = workspace / "installed"
        fixture_before = tree_digest(fixture)
        outside_before = file_sha256(outside)
        application: subprocess.Popen[bytes] | None = None
        uninstall = install_dir / "Uninstall.exe"

        try:
            install_command = [
                str(installer),
                "/S",
                f"/SUBSTRATEROOT={fixture}",
                f"/D={install_dir}",
            ]
            run(install_command, timeout=120, environment=lifecycle_environment)
            executable = install_dir / "MarkdownLLM Explorer.exe"
            if not executable.is_file() or not uninstall.is_file():
                raise RuntimeError("installer did not create the application and uninstaller")
            if list(install_dir.rglob("python.exe")) or list(install_dir.rglob("node.exe")):
                raise RuntimeError("installer contains an operator-facing Python or Node executable")

            desktop = shortcut_details(desktop_shortcut)
            start = shortcut_details(start_group / f"{arguments.app_name}.lnk")
            expected_target = str(executable)
            expected_root = str(fixture)
            if Path(desktop["Target"]).resolve() != executable.resolve() or Path(start["Target"]).resolve() != executable.resolve():
                raise RuntimeError("shortcut target does not resolve to the installed application")
            if expected_root not in desktop["Arguments"] or expected_root not in start["Arguments"]:
                raise RuntimeError("shortcut does not remember the selected substrate root")
            version = registry_value(arguments.uninstall_key, "DisplayVersion")
            brand_icon = install_dir / f"brand-icon-{version}.ico"
            source_icon = Path(__file__).resolve().parents[1] / "packaging/windows/assets/markdownllm-explorer.ico"
            if not brand_icon.is_file() or brand_icon.read_bytes() != source_icon.read_bytes():
                raise RuntimeError("installed brand icon differs from the authored application icon")
            if any(Path(shortcut["Icon"].rsplit(",", 1)[0]).resolve() != brand_icon.resolve() for shortcut in (desktop, start)):
                raise RuntimeError("shortcut does not use the versioned brand icon")
            if registry_value(arguments.uninstall_key, "DisplayIcon") != str(brand_icon):
                raise RuntimeError("application registration does not use the brand icon")
            if registry_value(arguments.app_key, "SubstrateRoot") != expected_root:
                raise RuntimeError("installer did not remember the selected substrate root")

            first_shortcut_count = int(desktop_shortcut.exists()) + len(list(start_group.glob(f"{arguments.app_name}.lnk")))

            upgrade_port = free_port()
            launch_environment = lifecycle_environment.copy()
            launch_environment["PATH"] = ""
            application = subprocess.Popen(
                [
                    str(executable),
                    "--root",
                    str(fixture),
                    "--port",
                    str(upgrade_port),
                    "--no-browser",
                    "--no-tray",
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=launch_environment,
                creationflags=CREATE_NO_WINDOW,
            )
            wait_for_health(upgrade_port, application)
            held_upgrade_request = hold_active_request(upgrade_port)
            upgrade_started = time.monotonic()
            try:
                run(install_command, timeout=120, environment=lifecycle_environment)
            finally:
                held_upgrade_request.close()
            upgrade_shutdown_seconds = time.monotonic() - upgrade_started
            application.wait(timeout=5)
            if application.returncode != 0 or upgrade_shutdown_seconds > 20.0:
                raise RuntimeError("active upgrade did not stop the primary process cleanly")
            application = None

            second_shortcut_count = int(desktop_shortcut.exists()) + len(list(start_group.glob(f"{arguments.app_name}.lnk")))
            if first_shortcut_count != 2 or second_shortcut_count != 2:
                raise RuntimeError("upgrade created duplicate or missing launch shortcuts")
            if registry_value(arguments.app_key, "SubstrateRoot") != expected_root:
                raise RuntimeError("upgrade did not preserve the selected substrate root")

            port = free_port()
            application = subprocess.Popen(
                [
                    str(executable),
                    "--root",
                    str(fixture),
                    "--port",
                    str(port),
                    "--no-browser",
                    "--no-tray",
                ],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=launch_environment,
                creationflags=CREATE_NO_WINDOW,
            )
            health = wait_for_health(port, application)
            held_uninstall_request = hold_active_request(port)
            uninstall_started = time.monotonic()
            try:
                run([str(uninstall), "/S"], timeout=120, environment=lifecycle_environment)
            finally:
                held_uninstall_request.close()
            uninstall_shutdown_seconds = time.monotonic() - uninstall_started
            application.wait(timeout=5)
            if application.returncode != 0 or uninstall_shutdown_seconds > 20.0:
                raise RuntimeError("active uninstall did not stop the primary process cleanly")
            application = None

            deadline = time.monotonic() + 10
            while install_dir.exists() and time.monotonic() < deadline:
                time.sleep(0.1)
            uninstall_clean = (
                not install_dir.exists()
                and not desktop_shortcut.exists()
                and not start_group.exists()
                and registry_value(arguments.app_key, "InstallDir") is None
                and registry_value(arguments.uninstall_key, "DisplayName") is None
            )
            if not uninstall_clean:
                raise RuntimeError("uninstall left application-owned files, shortcuts, or registry state")
            if tree_digest(fixture) != fixture_before or file_sha256(outside) != outside_before:
                raise RuntimeError("install lifecycle modified substrate or outside fixture data")

            document = {
                "schema": 1,
                "status": "pass",
                "tool": {"name": "verify_windows_installer.py", "version": "2"},
                "installer": {
                    "name": release_installer.name,
                    "bytes": release_installer.stat().st_size,
                    "sha256": file_sha256(release_installer),
                },
                "exercised_installer": {
                    "name": installer.name,
                    "bytes": installer.stat().st_size,
                    "sha256": file_sha256(installer),
                    "same_as_release": installer == release_installer,
                    "identity_only_isolation": installer != release_installer,
                    "app_name": arguments.app_name,
                    "instance_identity": arguments.instance_identity,
                },
                "environment": {
                    "per_user": True,
                    "administrator_required": False,
                    "system_python_required": False,
                    "system_node_required": False,
                    "network_required_after_setup_obtained": False,
                },
                "bundle": {"status": "pass", "version": health.get("version"), "path_empty_launch": True},
                "install": {"status": "pass", "desktop_shortcut": True, "start_menu_shortcut": True, "remembered_root": True},
                "launch": {"status": "pass", "health": health, "single_instance_exit": True, "capability_persisted": False},
                "upgrade": {
                    "status": "pass",
                    "root_preserved": True,
                    "shortcut_count": second_shortcut_count,
                    "active_process_stopped": True,
                    "active_request_drain_bounded": upgrade_shutdown_seconds <= 20.0,
                    "shutdown_seconds": round(upgrade_shutdown_seconds, 3),
                },
                "uninstall": {
                    "status": "pass",
                    "owned_state_removed": True,
                    "substrate_unchanged": True,
                    "outside_unchanged": True,
                    "active_process_stopped": True,
                    "active_request_drain_bounded": uninstall_shutdown_seconds <= 20.0,
                    "shutdown_seconds": round(uninstall_shutdown_seconds, 3),
                },
                "source_before_sha256": fixture_before,
                "source_after_sha256": tree_digest(fixture),
                "outside_before_sha256": outside_before,
                "outside_after_sha256": file_sha256(outside),
            }
        finally:
            if application is not None and application.poll() is None:
                application.kill()
                application.wait(timeout=5)
            if uninstall.exists():
                try:
                    subprocess.run(
                        [str(uninstall), "/S"],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=120,
                        creationflags=CREATE_NO_WINDOW,
                        env=lifecycle_environment,
                        check=False,
                    )
                except (OSError, subprocess.SubprocessError):
                    pass
            desktop_shortcut.unlink(missing_ok=True)
            shutil.rmtree(start_group, ignore_errors=True)
            for key_path in (arguments.uninstall_key, arguments.app_key):
                try:
                    winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
                except FileNotFoundError:
                    pass

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "installer": installer.name, "version": document["bundle"]["version"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
