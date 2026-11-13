You are reviewing one code change.

- `CHANGE.diff` in this directory is the change, as a unified diff.
- `tools/` is the code as it stands after the change. You may read any file in it.
- `COMMIT_MESSAGE.txt` is the author's commit message for this change.

Find defects that this change introduces: places where the changed code will behave wrongly. That means a wrong result, a crash, a case it mishandles, or a contract it breaks with code elsewhere in `tools/`. Do not report style, naming, missing tests, missing documentation, or defects in code the change did not touch.

Report at most five findings, most serious first. If you find none, report none.

End your reply with one JSON object and nothing after it:

{"findings": [{"file": "tools/...", "line_start": 0, "line_end": 0, "claim": "one sentence: what goes wrong, and when", "confidence": "high|medium|low"}]}

`file` is the path as it appears in `CHANGE.diff`. `line_start` and `line_end` are line numbers in the file as it stands after the change.
