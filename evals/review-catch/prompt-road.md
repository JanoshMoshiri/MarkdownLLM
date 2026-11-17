Review the change made by the last commit in this repository (`HEAD` against its parent).

Find defects the change introduces: places where the changed code will behave wrongly. That means a wrong result, a crash, a case it mishandles, or a contract it breaks with other code. Do not report style, naming, missing tests, missing documentation, or pre-existing defects.

Report at most five findings, most serious first.

Return only one JSON object; use an empty findings array if none:

{"findings": [{"file": "path/from/repository/root", "line_start": 1, "line_end": 1, "claim": "one sentence: what goes wrong, and when", "confidence": "high|medium|low"}]}

`line_start` and `line_end` are 1-based, inclusive line numbers at `HEAD`; use the smallest range that locates the defect.
