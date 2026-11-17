#!/bin/bash
# review-one: one review-catch review on the road, run whole inside the
# review-road distro as the reviewer (review-catch-on-the-road, Phase 4).
# Installed as /usr/local/bin/review-one (root, 755) by
#   python evals/review-catch/run_reviews.py --install
# and started only by the root script review-run, which stages this entry's
# bundle and passes its random name as the last argument:
#   review-one [--prepare-only] VENDOR ARM TRIAL ID MODEL EFFORT TIMEOUT SHOW_MESSAGE STAGE_NAME
#
# VENDOR claude|codex. EFFORT a level, or `default` to pass no effort flag.
# TIMEOUT seconds. SHOW_MESSAGE 1 keeps the author's commit message; 0
# replaces it with exactly "Change under review." (tree, parent, author and
# committer kept; the HEAD sha changes). ARM, TRIAL and ID are checked as
# tokens and otherwise unused: the reviewer's path names none of them.
#
# Steps:
#   1. clone /home/reviewer/road/stage/STAGE_NAME.bundle into a fresh,
#      neutrally named /home/reviewer/work/review.XXXXXXXX, then delete the
#      staged bundle; remove the remote; set the message; drop the reflog and
#      every unreachable object;
#   2. preflight: no *.bundle under /home/reviewer or /tmp, the root bundle
#      store unreadable, no other work directory. If any fails, the harness
#      is not started;
#   3. fingerprint the reviewer's harness configuration (no credentials, no
#      caches), run the harness in the clone under `timeout` with its normal
#      tools and the prompt (/home/reviewer/road/prompt-road.md) on stdin,
#      and fingerprint again. Web search is the one tool denied to both
#      harnesses: the answer key is on the public web.
#
# Output: the harness's stdout stream; for Codex, a line
# =====REVIEW-ONE-LAST-MESSAGE===== and the --output-last-message file;
# then a line =====REVIEW-ONE-META===== and one JSON line. The work
# directory, the staged bundle and the temporary files are deleted
# afterwards, always.
#
# --prepare-only stops before the harness: it prints the HEAD sha and
# message, the repository's state, the preflight and the fingerprint, cleans
# up and exits.
set -u

die() { echo "review-one: $1" >&2; exit "${2:-3}"; }

PREPARE_ONLY=0
if [ "${1:-}" = "--prepare-only" ]; then PREPARE_ONLY=1; shift; fi
[ "$#" -eq 9 ] || die "usage: review-one [--prepare-only] VENDOR ARM TRIAL ID MODEL EFFORT TIMEOUT SHOW_MESSAGE STAGE_NAME" 64
VENDOR=$1 MODEL=$5 EFFORT=$6 TIMEOUT=$7 SHOW=$8 STAGE_NAME=$9

for tok in "$@"; do
  case "$tok" in
    ''|*[!A-Za-z0-9._-]*) die "argument is not a simple token: $tok" 64 ;;
  esac
done
case "$VENDOR" in claude|codex) ;; *) die "vendor must be claude or codex" 64 ;; esac
case "$3" in *[!0-9]*) die "trial must be a number" 64 ;; esac
case "$TIMEOUT" in *[!0-9]*) die "timeout must be a number of seconds" 64 ;; esac
case "$SHOW" in 0|1) ;; *) die "show-message must be 0 or 1" 64 ;; esac
[ "$(id -un)" = reviewer ] || die "must run as reviewer (via review-run)" 64

RHOME=/home/reviewer
ROAD=$RHOME/road
BUNDLE=$ROAD/stage/$STAGE_NAME.bundle
PROMPT=$ROAD/prompt-road.md
WORKROOT=$RHOME/work
WORK= LAST= FPDIR=

cleanup() {
  cd /
  rm -rf "$BUNDLE" ${WORK:+"$WORK"} ${LAST:+"$LAST"} ${FPDIR:+"$FPDIR"}
  rmdir "$WORKROOT" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT TERM HUP

[ -f "$BUNDLE" ] || die "no staged bundle $BUNDLE"
[ -f "$PROMPT" ] || die "no prompt $PROMPT"
mkdir -p "$WORKROOT" || die "cannot create $WORKROOT"
WORK=$(mktemp -d "$WORKROOT/review.XXXXXXXX") || die "cannot create a work directory"
LAST=$(mktemp /tmp/review-last.XXXXXXXX) || die "cannot create a last-message file"
FPDIR=$(mktemp -d /tmp/review-fp.XXXXXXXX) || die "cannot create a fingerprint directory"

# ---------------------------------------------------------------- prepare
BUNDLE_SHA=$(sha256sum < "$BUNDLE" | cut -d' ' -f1)
git clone --quiet "$BUNDLE" "$WORK" >&2 || die "clone failed"
rm -f "$BUNDLE"
cd "$WORK" || die "cannot enter $WORK"
git remote remove origin || die "cannot remove origin"
ORIGINAL=$(git rev-parse HEAD)
if [ "$SHOW" = 0 ]; then
  GIT_COMMITTER_NAME=$(git log -1 --format=%cn) \
  GIT_COMMITTER_EMAIL=$(git log -1 --format=%ce) \
  GIT_COMMITTER_DATE=$(git log -1 --format=%cI) \
    git -c commit.gpgsign=false commit --amend --no-verify --allow-empty --quiet \
      -m "Change under review." || die "cannot replace the commit message"
fi
# The amended-away commit (and its message) must not be reachable by any
# route: no reflog, no ORIG_HEAD, no unreachable object left in the pack.
rm -f .git/ORIG_HEAD
git reflog expire --expire=now --all
git gc --prune=now --quiet 2>/dev/null || die "gc failed"
HEAD_SHA=$(git rev-parse HEAD)

# ---------------------------------------------------------------- preflight
PREFLIGHT=""
add_failure() { PREFLIGHT="${PREFLIGHT:+$PREFLIGHT
}$1"; }
LEFT=$(find "$RHOME" /tmp -name '*.bundle' 2>/dev/null | head -n 5 | tr '\n' ' ')
[ -z "$LEFT" ] || add_failure "bundle within reach: $LEFT"
ls /srv/review-road >/dev/null 2>&1 && add_failure "the bundle store /srv/review-road is readable"
OTHERS=$(find "$WORKROOT" -mindepth 1 -maxdepth 1 ! -path "$WORK" 2>/dev/null | head -n 3 | tr '\n' ' ')
[ -z "$OTHERS" ] || add_failure "other work directories: $OTHERS"

# ---------------------------------------------------------------- fingerprint
# The reviewer's harness configuration, credentials and caches excluded:
# content hashes per path, so a rewrite with identical bytes is no change.
FP_PY='
import hashlib, json, os
home = os.path.expanduser("~")
files = [".claude/settings.json", ".claude/settings.local.json", ".claude/CLAUDE.md",
         ".codex/config.toml", ".codex/AGENTS.md", ".bashrc", ".profile", ".gitconfig"]
trees = [".claude/skills", ".claude/agents", ".claude/commands", ".claude/hooks",
         ".codex/skills", ".codex/rules", ".codex/prompts"]
out = {}
# Folders each harness manages itself and rewrites on its own: skills Claude
# Code syncs from the account, and the system skills Codex ships. The first
# road smoke review (2026-11-17) was stopped by Claude Code syncing the former
# on first use. They are not the reviewer changing its configuration.
MANAGED = (".claude/skills/synced/", ".codex/skills/.system/")
def add(rel):
    if rel.replace(os.sep, "/").startswith(MANAGED):
        return
    p = os.path.join(home, rel)
    if os.path.islink(p):
        out[rel] = "link:" + os.readlink(p)
    elif os.path.isfile(p):
        with open(p, "rb") as fh:
            out[rel] = hashlib.sha256(fh.read()).hexdigest()
for rel in files:
    add(rel)
for tree in trees:
    for root, dirs, names in os.walk(os.path.join(home, tree)):
        for n in names + [d for d in dirs if os.path.islink(os.path.join(root, d))]:
            add(os.path.relpath(os.path.join(root, n), home))
print(json.dumps(out, sort_keys=True))
'
fingerprint() { python3 -c "$FP_PY" > "$FPDIR/$1.json" || echo '{}' > "$FPDIR/$1.json"; }
fingerprint before

if [ "$PREPARE_ONLY" = 1 ]; then
  echo "work directory: $WORK"
  echo "staged bundle sha256: $BUNDLE_SHA (staged file now present: $([ -e "$BUNDLE" ] && echo YES || echo no))"
  echo "entry commit (bundle HEAD): $ORIGINAL"
  echo "HEAD reviewed: $HEAD_SHA"
  echo "HEAD tree: $(git rev-parse 'HEAD^{tree}')"
  echo "HEAD parent: $(git rev-parse --verify -q HEAD^ || echo none)"
  echo "HEAD author: $(git log -1 --format='%an <%ae> %aI')"
  echo "HEAD committer: $(git log -1 --format='%cn <%ce> %cI')"
  echo "HEAD message:"
  git log -1 --format=%B | sed 's/^/  | /'
  if [ "$HEAD_SHA" != "$ORIGINAL" ]; then
    if git cat-file -e "$ORIGINAL^{commit}" 2>/dev/null; then
      echo "entry commit object still present: YES (message reachable)"
    else
      echo "entry commit object still present: no"
    fi
  fi
  echo "commits: $(git rev-list --count --all)"
  echo "refs: $(git for-each-ref --format='%(refname)' | tr '\n' ' ')"
  echo "remotes: $(git remote | tr '\n' ' ')"
  echo "reflog entries: $(git log -g --all --format=%H 2>/dev/null | wc -l)"
  echo "unreachable objects: $(git fsck --unreachable --no-reflogs 2>/dev/null | wc -l)"
  echo "preflight: ${PREFLIGHT:-pass}"
  echo "configuration fingerprint: $(sha256sum < "$FPDIR/before.json" | cut -d' ' -f1) over $(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$FPDIR/before.json") paths"
  W=$WORK
  cleanup
  trap - EXIT
  if [ -e "$W" ]; then echo "cleanup: FAILED, $W remains"; exit 1; fi
  echo "cleanup: $W removed"
  exit 0
fi

# ---------------------------------------------------------------- review
HARNESS_RUN=0
CODE=0
START=$(date +%s.%N)
END=$START
VERSION=""
if [ -z "$PREFLIGHT" ]; then
  if [ "$VENDOR" = claude ]; then
    VERSION=$(claude --version 2>/dev/null | head -n 1)
    ARGS=(-p --model "$MODEL")
    [ "$EFFORT" = default ] || ARGS+=(--effort "$EFFORT")
    ARGS+=(--output-format stream-json --verbose
           --dangerously-skip-permissions
           --disallowedTools WebSearch,WebFetch
           --no-session-persistence)
  else
    VERSION=$(codex --version 2>/dev/null | head -n 1)
    ARGS=(exec --ephemeral --sandbox danger-full-access --model "$MODEL")
    [ "$EFFORT" = default ] || ARGS+=(-c "model_reasoning_effort=\"$EFFORT\"")
    # Codex's hosted web search: the top-level `web_search` setting
    # (disabled|cached|indexed|live) in codex-cli 0.169.0.
    ARGS+=(-c 'web_search="disabled"'
           --json --output-last-message "$LAST" -)
  fi
  HARNESS_RUN=1
  START=$(date +%s.%N)
  timeout --kill-after=30 "$TIMEOUT" "$VENDOR" "${ARGS[@]}" < "$PROMPT"
  CODE=$?
  END=$(date +%s.%N)
fi
fingerprint after

if [ "$VENDOR" = codex ]; then
  printf '\n=====REVIEW-ONE-LAST-MESSAGE=====\n'
  [ -s "$LAST" ] && cat "$LAST"
fi
printf '\n=====REVIEW-ONE-META=====\n'
RO_CODE=$CODE RO_START=$START RO_END=$END RO_TIMEOUT=$TIMEOUT RO_VERSION=$VERSION \
RO_HEAD=$HEAD_SHA RO_ENTRY_COMMIT=$ORIGINAL RO_VENDOR=$VENDOR RO_SHOW=$SHOW \
RO_BUNDLE_SHA=$BUNDLE_SHA RO_PREFLIGHT=$PREFLIGHT RO_RUN=$HARNESS_RUN RO_FP=$FPDIR \
python3 -c '
import hashlib, json, os
e = os.environ
def load(name):
    try:
        with open(os.path.join(e["RO_FP"], name + ".json")) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None
def digest(m):
    return None if m is None else hashlib.sha256(json.dumps(m, sort_keys=True).encode()).hexdigest()
before, after = load("before"), load("after")
changed = []
if before is None or after is None:
    changed.append("fingerprint unreadable")
else:
    for k in sorted(set(before) | set(after)):
        if k not in before:
            changed.append("~/" + k + " (added)")
        elif k not in after:
            changed.append("~/" + k + " (removed)")
        elif before[k] != after[k]:
            changed.append("~/" + k + " (modified)")
code = int(e["RO_CODE"])
secs = round(float(e["RO_END"]) - float(e["RO_START"]), 1)
ran = e["RO_RUN"] == "1"
print(json.dumps({
    "exit_code": code if ran else None,
    "timed_out": ran and code in (124, 137) and secs >= int(e["RO_TIMEOUT"]),
    "seconds": secs,
    "harness_run": ran,
    "harness_version": e["RO_VERSION"] or None,
    "vendor": e["RO_VENDOR"],
    "head_reviewed": e["RO_HEAD"],
    "entry_commit": e["RO_ENTRY_COMMIT"],
    "message_shown": e["RO_SHOW"] == "1",
    "bundle_sha256": e["RO_BUNDLE_SHA"],
    "preflight_failures": [x for x in e["RO_PREFLIGHT"].split("\n") if x],
    "config_before": digest(before),
    "config_after": digest(after),
    "config_changed": changed,
}))'
exit 0
