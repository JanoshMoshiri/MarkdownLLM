# review-catch

Does a code reviewer catch real defects? A Claude reviewer and a Codex reviewer
see the same changes from the frozen set (`set.json`, written by `mine_set.py --freeze`).
There are four arms: `claude-blind`, `codex-blind`, `claude-message` and `codex-message`. The
`-message` arms also see the author's commit message.

## Files

- `prompt-blind.md` and `prompt-message.md` are the frozen prompts. They are sent
  unchanged, as LF bytes.
- `run_reviews.py` runs one arm for one trial.
- `score_reviews.py` scores complete result files against the set.
- `test_review_catch.py` holds the tests. They launch nothing:
  `python -m pytest -p no:cacheprovider evals/review-catch/test_review_catch.py`

The runner and the scorer use the standard library only. All hashes (prompt, set) are
sha256 over **LF-normalised bytes** (CRLF converted to LF), so a CRLF checkout hashes the
same. The result file records this as `hashes_over`.

## Running

```
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json \
  --arm claude-blind --model <full model id> --trial 1 [--entries r001,r002] [--dry-run]
```

Entries are shuffled with `random.Random(trial)` and reviewed one at a time. Each
review gets a fresh folder at `<system temp>/mdllm-review-catch/<arm>-t<trial>/<entry id>/`.
The folder holds `tools/` at the commit (`git archive`, no `.git`), `CHANGE.diff`
(`git diff <commit>^ <commit> -- tools`), and `COMMIT_MESSAGE.txt` in `-message` arms
only. Before each launch a leak check confirms the folder has exactly those top-level
names and no `.git`. It also confirms no file holds an entry id, or a 7-character prefix
of the entry's commit sha, its fix shas or the set's `repo_head`. Each folder is deleted
once its review is recorded. A `--dry-run` builds the folders, runs the check, prints the
command lines and launches nothing.

A timeout, or an unparsable reply, voids a review. A nonzero exit voids it only when
there is also no parsable reply. A void review is retried once, and two consecutive voids
stop the arm with exit code 2. The result file is written after every review, so a
stopped arm leaves a partial marked `"complete": false`. Results go to
`evals/results/review-catch/<UTC stamp>-<arm>-t<trial>.json`. A result file never holds
an entry's kind, its defects or its fix shas.

**A review that reaches outside its work folder is void**, in both vendors. The void
reason is `reached outside the work folder`, and it is retried once and counts towards
two-in-a-row like any other void. The record keeps the reach list (`outside_reach`) and
the voided attempt.

- **Claude:** a tool call reaches outside when its `file_path`, `path` or `notebook_path`
  resolves outside the folder or has a `..` segment. So does a Glob `pattern` or Grep
  `glob` that is absolute or has a `..` segment. Grep's `pattern` is a content regex, so
  it is not checked.
- **Codex:** each shell command is checked after its shell wrapper is removed
  (`pwsh`/`powershell`/`cmd`/`bash`/`sh -Command|-c|-lc|/c`). It reaches outside when it:
  - invokes `git` in command position (start, or after `;` `&` `|` `(`, `xargs`, `iex`
    and similar);
  - has an absolute path not under the folder: a drive path with either slash, a UNC path,
    or a token starting with `/` and a letter;
  - names `~`, `$HOME`, `%USERPROFILE%`, `%HOMEPATH%` or `$env:`;
  - has a `..` path segment.

  The check is deliberately conservative: when unsure, it flags. Known false positives:
  - Windows switches such as `findstr /s`.
  - Regex arguments that start with `/` and a letter, such as `rg "/api"`.
  - Any path, inside the folder or not, when the temp path contains a space (tokens split
    on spaces).
  - A shell wrapper with switches the unwrapper does not know.

At the end of a run, or a stop, the runner prints one line per review (id, seconds,
findings kept, void or not). It then prints the totals: reviews, voids, retries,
seconds, and cost and tokens when the CLI reports them.

If any finding in a reply lacks `file`, integer `line_start`/`line_end` or `claim`, the
whole reply is void. The first five findings are kept, and the number offered is
recorded.

## Scoring

```
python evals/review-catch/score_reviews.py --set evals/review-catch/set.json \
  --results evals/results/review-catch [--emit-near near.md] [--near-rulings rulings.txt]
```

- Only complete files whose set sha256 matches are counted. The scorer lists the
  skipped files and the reason for each.
- Files are grouped by (arm, model, prompt sha256). Different groups are never pooled.
- **Hit:** a kept finding names the same file (slashes and a leading `./` normalised),
  and its line range, widened by 5 lines on each side, overlaps a defect range.
- **Near miss:** not a hit, but the same file within 30 lines.
- `--emit-near` writes the near misses in a shuffled order, each under an opaque key.
  It shows no arm, vendor, model or trial. A `<name>.key.json` file beside it maps
  each key back to its review.
- `--near-rulings` reads lines of the form `key: hit|miss` and applies them. The keys
  are deterministic, so a rulings file stays valid when the scorer runs again.
- A defect counts as caught when it is hit in a strict majority of trials. The paired
  table and the exact two-sided McNemar test use these majority catches.

## Isolation, per vendor

**Claude** (`claude -p`, the real `claude.exe` behind the npm shim). The flags are
`--safe-mode`, `--restricted`, `--strict-mcp-config`, `--disable-slash-commands`,
`--no-session-persistence`, `--tools Read,Glob,Grep`, `--allowedTools Read,Glob,Grep`,
`--permission-prompts none` and `--output-format stream-json --verbose`.

- `--safe-mode` disables CLAUDE.md, skills, plugins, hooks, MCP servers, commands,
  agents and output styles.
- `--restricted` ignores user, project and local settings, and confines the file tools
  to the working folder.

What could NOT be isolated:

- Admin-managed (policy) settings still apply under both flags.
- The operator's login and account are used. `--bare` would isolate more, but it
  requires `ANTHROPIC_API_KEY` and does not read OAuth, so it is not used.
- Auto-memory is not named in `--safe-mode`'s help. The temp working folder has no
  memory of its own, but this has not been verified.
- The environment variables of the operator's shell are inherited.
- Combining `--safe-mode` with `--restricted` has not been tried in a real run. The
  smoke review below is that check.
- A tool call that reaches outside the folder voids the review (see the void rule above).

**Codex** (`codex exec`, run as `node <npm>/node_modules/@openai/codex/bin/codex.js`).
The flags are `--skip-git-repo-check`, `--ephemeral`, `--ignore-user-config` (no
`config.toml`, so none of its MCP servers, profiles or hooks), `--ignore-rules` (no
execpolicy `.rules`), `--sandbox read-only`, `--cd <folder>`, `--json` and
`--output-last-message <file outside the folder>`. The prompt is sent on stdin (`-`).

What could NOT be isolated:

- `CODEX_HOME` is still used for auth, and the help text gives no flag that skips
  anything else kept there. Global instructions (`AGENTS.md` in `CODEX_HOME`), skills
  and plugins stored there may still load.
- The read-only sandbox blocks writes, not reads. A shell command can read any path on
  the machine, including this repository and its later history. The runner checks every
  command executed (`commands`) and voids a review that reaches outside. That check reads
  the command text, so it cannot see a path that is built at run time. Run arms one at a
  time.
- Codex reports no cost, only token counts. The observed model is whatever `model`
  fields appear in the JSON events, and the list may be empty.
- Admin-managed configuration, if any, and the environment are inherited.

## Order of an evening

1. Freeze the set: `mine_set.py --freeze` writes `set.json`.
2. Smoke-test one entry per vendor into a scratch folder with `--trial 0 --out <scratch dir>`.
   Smoke output is never scored, so never pass that folder to `score_reviews.py`.
3. Run five trials of one arm (`--trial 1` to `--trial 5`) into the default `--out`, then
   the next arm.

## Smoke review (operator, own terminal)

```
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm claude-blind --model <claude model id> --trial 0 --entries <one id> --out <scratch dir>
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm codex-blind  --model <codex model id>  --trial 0 --entries <one id> --out <scratch dir>
```
