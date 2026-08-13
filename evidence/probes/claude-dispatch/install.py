"""Generate an inert Claude Code dispatch-probe project — 5R.0 apparatus.

Builds a throwaway project whose ``.claude/settings.json`` fires ``probe.py``
on SessionStart, then reports the exact command to run. Every host path is
computed here at run time, so nothing host-specific is ever committed.

    python install.py <target-dir> [--form shell|exec] [--handlers 1|2]
                                   [--interpreter python3]

Design choices that matter to the evidence:

- the project directory name contains a SPACE by default (``probe dir``),
  because quoting defects hide on space-free paths;
- shell form uses POSIX-style forward slashes even on Windows: hook shell
  form runs under sh (Git Bash on Windows), where a backslash inside double
  quotes is an escape;
- exec form uses the native path and passes deliberately awkward argv
  members (embedded quote, backslash, a literal ``$CLAUDE_PROJECT_DIR``) to
  establish whether any re-quoting or expansion layer exists;
- two handlers in ONE matcher group is the parallelism question; the probe's
  hold makes overlap visible.

Nothing here touches the framework floor, and nothing runs Claude for you —
the operator fires the real harness.
"""
import argparse
import json
import pathlib
import shutil
import sys

PROBE = pathlib.Path(__file__).resolve().with_name("probe.py")


def shell_handler(probe: pathlib.Path, interpreter: str, label: str) -> dict:
    # Forward slashes: shell form is sh (Git Bash on Windows).
    return {
        "type": "command",
        "command": (f'{interpreter} "{probe.as_posix()}" {label} '
                    f'"two words"'),
    }


def exec_handler(probe: pathlib.Path, interpreter: str, label: str) -> dict:
    # No shell: argv passes through verbatim, so awkward members are the test.
    return {
        "type": "command",
        "command": interpreter,
        "args": [str(probe), label, "two words", "$CLAUDE_PROJECT_DIR",
                 'a"quote', "back\\slash"],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target")
    parser.add_argument("--form", choices=("shell", "exec"), default="shell")
    parser.add_argument("--handlers", type=int, choices=(1, 2), default=2)
    parser.add_argument("--interpreter", default=None,
                        help="default: python3 on POSIX, python on Windows")
    parser.add_argument("--name", default="probe dir",
                        help="project dir name; contains a space by design")
    args = parser.parse_args(argv)

    interpreter = args.interpreter or (
        "python" if sys.platform == "win32" else "python3")
    project = pathlib.Path(args.target).expanduser().resolve() / args.name
    if project.exists():
        shutil.rmtree(project)
    (project / ".claude").mkdir(parents=True)

    # The probe travels with the project so records land beside it.
    local_probe = project / "probe.py"
    shutil.copy2(PROBE, local_probe)

    build = shell_handler if args.form == "shell" else exec_handler
    labels = ["handler-A", "handler-B"][:args.handlers]
    handlers = [build(local_probe, interpreter, label) for label in labels]

    settings = {"hooks": {"SessionStart": [{"hooks": handlers}]}}
    (project / ".claude" / "settings.json").write_text(
        json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    print(f"probe project: {project}")
    print(f"  form={args.form} handlers={args.handlers} "
          f"interpreter={interpreter}")
    print("\nFire the real harness from that directory, e.g.:")
    print(f'  cd "{project}" && claude -p "Reply with exactly: OK"')
    print("\nThen read records/*.json and correlate with the harness "
          "transcript named in each record's stdin payload.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
