"""Inert Claude Code hook-dispatch recorder — Phase 5R.0 evidence apparatus.

Records, per invocation, everything the 5R.0 gate asks a live dispatch to
establish: the shell (if any) that launched us, argument boundaries, cwd,
the project-root environment variable, stdin receipt, timing, and exit
status. One JSON file per invocation under ``records/``.

Deliberately inert: it never touches the framework, never writes outside its
own directory, and always exits 0. It is apparatus for observing the harness,
not part of the floor.

Cross-platform by construction — the same file is the fixture on Windows and
POSIX so the two evidence records compare like for like. No host path is
baked in; ``install.py`` generates the project configuration at run time.

The 3-second hold is load-bearing: two handlers declared in one group must
produce OVERLAPPING wall-clock windows if the harness dispatches them
concurrently. Without the hold, fast handlers can serialise by accident and
a parallel harness would look sequential.
"""
import datetime
import json
import os
import subprocess
import sys
import time
import uuid

HOLD_SECONDS = 3
MAX_DEPTH = 6


def _parent_chain_posix(pid):
    chain = []
    for _ in range(MAX_DEPTH):
        out = subprocess.run(["ps", "-o", "ppid=,comm=", "-p", str(pid)],
                             capture_output=True, text=True, timeout=15)
        parts = out.stdout.split(None, 1)
        if len(parts) < 2:
            break
        ppid, name = parts[0].strip(), parts[1].strip()
        chain.append({"pid": pid, "name": name})
        if not ppid.isdigit() or int(ppid) <= 1:
            break
        pid = int(ppid)
    return chain


def _parent_chain_windows(pid):
    chain = []
    for _ in range(MAX_DEPTH):
        query = (f"$p = Get-CimInstance Win32_Process -Filter "
                 f"'ProcessId={pid}'; $p.ParentProcessId; $p.Name")
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
             query], capture_output=True, text=True, timeout=15)
        lines = [line.strip() for line in out.stdout.splitlines()
                 if line.strip()]
        if len(lines) < 2:
            break
        ppid, name = lines[0], lines[1]
        chain.append({"pid": pid, "name": name})
        if not ppid.isdigit() or int(ppid) == 0:
            break
        pid = int(ppid)
    return chain


def parent_chain():
    """Which process actually launched us — the shell question, answered by
    the OS rather than by reading the harness's documentation."""
    try:
        if os.name == "nt":
            return _parent_chain_windows(os.getpid())
        return _parent_chain_posix(os.getpid())
    except Exception as exc:            # observation, never failure
        return [{"error": repr(exc)}]


def main():
    start = time.time()
    label = sys.argv[1] if len(sys.argv) > 1 else "unlabelled"

    stdin_data, stdin_error = None, None
    try:
        raw = sys.stdin.read()
        stdin_data = json.loads(raw) if raw.strip() else raw
    except Exception as exc:
        stdin_error = repr(exc)

    record = {
        "label": label,
        "argv": sys.argv,
        "platform": sys.platform,
        "os_name": os.name,
        "start_epoch": start,
        "start_iso": datetime.datetime.now().isoformat(),
        "cwd": os.getcwd(),
        "CLAUDE_PROJECT_DIR": os.environ.get("CLAUDE_PROJECT_DIR"),
        "CLAUDECODE": os.environ.get("CLAUDECODE"),
        "SHELL": os.environ.get("SHELL"),
        "COMSPEC": os.environ.get("COMSPEC"),
        "MSYSTEM": os.environ.get("MSYSTEM"),
        "python": sys.executable,
        "python_version": sys.version,
        "stdin": stdin_data,
        "stdin_error": stdin_error,
        "parent_chain": parent_chain(),
    }
    time.sleep(HOLD_SECONDS)
    record["end_epoch"] = time.time()

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "records")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{label}-{uuid.uuid4().hex[:8]}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2)
    print(f"probe {label} recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
