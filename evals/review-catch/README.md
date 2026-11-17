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
  --arm claude-blind --model <full model id> --effort xhigh --trial 1 [--entries r001,r002] [--dry-run]
```

`--model` and `--effort` are both required and never defaulted. Effort is passed to the
CLI explicitly (`--effort <level>` for Claude, `-c model_reasoning_effort="<level>"` for
Codex; `--effort default` passes nothing and leaves the CLI's own) and recorded per trial
as `effort_requested`, and the scorer never pools results that differ in model or effort.

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
- Files are grouped by (arm, model, effort, prompt sha256). Different groups are never
  pooled. A file with no `effort_requested` counts as effort `default`.
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
`--permission-prompts none` and `--output-format stream-json --verbose`, plus
`--effort <level>` unless the effort is `default`.

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
`--output-last-message <file outside the folder>`, plus `-c model_reasoning_effort="<level>"`
unless the effort is `default`. The prompt is sent on stdin (`-`).
Eight features are switched off with `--disable`: `apps`, `plugins`, `hooks`,
`memories`, `multi_agent`, `browser_use`, `computer_use` and `image_generation`. The
first smoke review (2026-11-14) showed that `--ignore-user-config` alone left Codex
dialling the account's connected apps.

The command-line Codex and the desktop app are separate installs and can be different
versions offering different models. The model id passed to `--model` must be one the
command-line build offers; the runner records the build per trial.

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

## On the road

The road arms (`claude-road`, `codex-road`, and `claude-road-message` and
`codex-road-message`, which keep the author's commit message) run each harness whole, as
the operator uses it, inside one isolated machine
(`things/plans/review-catch-on-the-road.md`).

- **The machine.** WSL2 distro `review-road` (Ubuntu 24.04), user `reviewer`, signed in to
  both Claude Code and Codex CLI. No Windows drive and no Windows interop.
  `review-shell.sh` applies the network lock at every entry: the reviewer reaches only
  the two vendors' model and sign-in services, through a local proxy.
- **The repository.** Each entry has a git bundle holding the entry commit and its
  ancestry and nothing later (`road/bundles.json`, leak check per bundle). The bundles live
  in a root-only store, `/srv/review-road/bundles` (root, dir 700, files 600), which the
  reviewer cannot read. A bundle that failed its leak check is refused, and before an arm
  runs the runner checks every store copy's sha256 against the manifest.
- **One review.** The runner calls the root script `review-run` (`road/review-run.sh`,
  installed to `/usr/local/sbin`). It clears anything an earlier review left behind, then
  copies only this entry's bundle to `/home/reviewer/road/stage/<random>.bundle` (owner
  reviewer, 600). It then starts `review-one` (`road/review-one.sh`, installed to
  `/usr/local/bin`) as the reviewer, behind the network lock. `review-one`:
  - clones the staged bundle into a fresh, neutrally named
    `/home/reviewer/work/review.XXXXXXXX`, then deletes the staged bundle;
  - removes the remote, and, unless the arm is a `-message` arm, replaces the HEAD
    commit's message with `Change under review.` (tree, parent, author and committer
    kept). It drops the reflog and every unreachable object, so the original message
    cannot be recovered;
  - runs a preflight before the harness. No `*.bundle` may be under `/home/reviewer` or
    `/tmp`, the store must be unreadable, and no other work directory may exist. If any
    check fails, the harness is not started and the review is void;
  - fingerprints the reviewer's harness configuration, runs the harness in the clone
    under `timeout` with its normal tools and the prompt (`prompt-road.md`) on stdin, and
    fingerprints again;
  - deletes the clone, the staged bundle and its temporary files afterwards, always.

  The harness command lines:
  - Claude: `claude -p --model M --effort E --output-format stream-json --verbose
    --dangerously-skip-permissions --disallowedTools WebSearch,WebFetch --no-session-persistence`
  - Codex: `codex exec --ephemeral --sandbox danger-full-access --model M
    -c model_reasoning_effort="E" -c web_search="disabled" --json --output-last-message <file> -`
- **The configuration fingerprint** covers content hashes of:
  - `~/.claude/settings.json`, `settings.local.json` and `CLAUDE.md`;
  - the `~/.claude/{skills,agents,commands,hooks}` trees;
  - `~/.codex/config.toml` and `AGENTS.md`;
  - the `~/.codex/{skills,rules,prompts}` trees;
  - `~/.bashrc`, `~/.profile` and `~/.gitconfig`.

  Credentials and caches are left out. If anything changed during a review, the review is
  void ("changed the harness configuration") and the arm stops at once. The two-voids
  rule does not apply, because every later review would run on a contaminated
  configuration.
- **The one denied tool is web search**, in both harnesses, because the answer key (the
  later fix) is public. Fetching is blocked by the proxy anyway. Codex's switch is the
  top-level `web_search` setting (`disabled|cached|indexed|live` in codex-cli 0.169.0).

Install, or reinstall after changing any of these files. This writes `review-run`,
`review-one` and the prompt as LF bytes, root-owned. It resets the store's permissions and
checks the three files' sha256 inside the distro:

```
python evals/review-catch/run_reviews.py --install
```

Smoke review, one per vendor (into a scratch folder, never scored):

```
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm claude-road --model claude-opus-5-5 --effort xhigh --trial 0 --entries r001 --out <scratch dir>
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm codex-road  --model gpt-6.1-sol     --effort xhigh --trial 0 --entries r001 --out <scratch dir>
```

`--dry-run` prints the exact `wsl.exe` command lines and touches nothing. `--prepare-only`
runs the staging and clone-and-message steps for each entry and prints the HEAD sha and
message it would review, with the preflight and the fingerprint. It then cleans up; no
harness is launched. Every argument that crosses `wsl.exe` is a simple token (letters,
digits, `. _ - /`). wsl.exe joins its arguments into a `/bin/sh` command line inside the
distro, so the prompt never travels as an argument.

**What is recorded.** Results go to `evals/results/review-catch-road/` by default. Each
file records:

- the sha256 of the prompt, `review-one` and `review-run` (LF bytes), checked against the
  installed copies before every review;
- the store path and that its bundles were checked, the bundle manifest's sha256, and each
  review's bundle sha256 as the manifest gives it and as staged;
- the harness build reported inside the distro, and the HEAD sha reviewed;
- the configuration fingerprint before and after, and the paths that changed;
- the commands run (Codex commands, Claude `Bash` commands) and the tool counts;
- whether any command looks like a test run (`pytest` or `unittest`);
- any command or tool call that names the bundle store (`road_reach`), recorded and not
  voided;
- time, tokens and cost.

**There is no reach rule on the road.** A review is void only when:

- it dies or times out (default 1800 s; the runner adds 180 s for staging and cleanup);
- the preflight fails;
- it changes the harness configuration, which also stops the arm;
- it returns nothing parsable;
- it reads nothing (Claude used no tool at all; Codex executed no command).

These rules are unchanged:

- retry once, and stop after two voids in a row;
- `--effort` is required;
- one review at a time;
- the scorer never pools.

Findings name files from the repository root, the form the set's defects use. The scorer
also accepts an absolute path into the clone (`/home/reviewer/work/review.XXXXXXXX/...`).

## Order of an evening

1. Freeze the set: `mine_set.py --freeze` writes `set.json`.
2. Smoke-test one entry per vendor into a scratch folder with
   `--effort xhigh --trial 0 --out <scratch dir>`.
   Smoke output is never scored, so never pass that folder to `score_reviews.py`.
3. Run five trials of one arm (`--effort xhigh --trial 1` to `--trial 5`) into the default
   `--out`, then the next arm. Keep the same `--model` and `--effort` across an arm's trials;
   a trial at another effort is scored as a separate group, not pooled.

## Smoke review (operator, own terminal)

```
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm claude-blind --model <claude model id> --effort xhigh --trial 0 --entries <one id> --out <scratch dir>
python evals/review-catch/run_reviews.py --set evals/review-catch/set.json --arm codex-blind  --model <codex model id>  --effort xhigh --trial 0 --entries <one id> --out <scratch dir>
```
