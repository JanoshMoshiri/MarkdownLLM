#!/bin/bash
# review-run: the root half of one review-catch review on the road
# (review-catch-on-the-road, Phase 4). Installed as /usr/local/sbin/review-run
# (root, 755) by `python evals/review-catch/run_reviews.py --install`, and
# launched by the runner as
#   wsl -d review-road -u root -- /usr/local/sbin/review-run [--prepare-only] \
#       VENDOR ARM TRIAL ID MODEL EFFORT TIMEOUT SHOW_MESSAGE
#
# The bundles live in a root-only store, /srv/review-road/bundles (dir 700,
# files 600), where the reviewer cannot read them. For one review this
# script:
#   1. clears anything an earlier, killed review left behind (one review
#      runs at a time): /home/reviewer/work, the stage, review-one's /tmp files;
#   2. copies only this entry's bundle to /home/reviewer/road/stage/<random>.bundle
#      (owner reviewer, 600);
#   3. runs review-shell.sh (the network lock) with review-one as the
#      reviewer, passing the same arguments plus the random stage name.
#      review-one clones from the staged file and deletes it before the
#      harness starts, so during the review no bundle is within reach;
#   4. deletes the staged file if it is still there, and exits with
#      review-one's exit code.
# It does not exec review-shell.sh, so step 4 runs however review-one ends.
set -u

die() { echo "review-run: $1" >&2; exit "${2:-3}"; }

[ "$(id -u)" = 0 ] || die "must run as root" 64
FLAG=()
if [ "${1:-}" = "--prepare-only" ]; then FLAG=(--prepare-only); shift; fi
[ "$#" -eq 8 ] || die "usage: review-run [--prepare-only] VENDOR ARM TRIAL ID MODEL EFFORT TIMEOUT SHOW_MESSAGE" 64
for tok in "$@"; do
  case "$tok" in
    ''|*[!A-Za-z0-9._-]*) die "argument is not a simple token: $tok" 64 ;;
  esac
done
ID=$4

STORE=/srv/review-road/bundles
SRC=$STORE/$ID.bundle
RHOME=/home/reviewer
STAGE=$RHOME/road/stage
[ -f "$SRC" ] || die "no bundle for $ID in $STORE"

rm -rf "$RHOME/work" "$STAGE" /tmp/review-last.* /tmp/review-fp.*
mkdir -p "$STAGE" || die "cannot create $STAGE"
chown reviewer:reviewer "$STAGE" && chmod 700 "$STAGE" || die "cannot set up $STAGE"

NAME=$(head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \n')
STAGED=$STAGE/$NAME.bundle
trap 'rm -f "$STAGED"' EXIT
install -o reviewer -g reviewer -m 600 "$SRC" "$STAGED" || die "cannot stage the bundle"

/usr/local/sbin/review-shell.sh /usr/local/bin/review-one "${FLAG[@]}" "$@" "$NAME"
exit $?
