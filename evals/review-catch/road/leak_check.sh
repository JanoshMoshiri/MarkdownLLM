#!/bin/sh
# Leak check for the review-catch road's bundles, run inside the review-road
# distro (as root, since the store is root-only):
#   sh leak_check.sh [BUNDLE_DIR] > results.tsv
# BUNDLE_DIR (default /srv/review-road/bundles, root-only, so run this as root) holds <id>.bundle and the
# checks.tsv written by build_bundles.py: id, commit, fix commits or "-",
# expected commit count. Each bundle is cloned into a scratch dir and must:
#   a. have HEAD at the entry commit (and advertise nothing but HEAD);
#   b. hold exactly the commit's ancestry, nothing more, nothing missing;
#   c. lack every fix commit (items), or hold no commit committed later than
#      the entry commit (controls);
#   d. after removing origin, have no remotes, no refs and no reflog.
# Output, one line per entry: id, pass|fail, commits, bundle sha256, failures.
set -u
B=${1:-/srv/review-road/bundles}
SCRATCH=/tmp/leak
rm -rf "$SCRATCH" && mkdir -p "$SCRATCH"

tr -d '\r' < "$B/checks.tsv" | while IFS="$(printf '\t')" read -r id sha fixlist expected; do
  [ -n "$id" ] || continue
  d="$SCRATCH/$id"
  fail=""
  add() { fail="${fail:+$fail; }$1"; }
  g() { git -C "$d" "$@"; }

  heads=$(git bundle list-heads "$B/$id.bundle" 2>&1)
  [ "$heads" = "$sha HEAD" ] || add "bundle advertises: $(echo "$heads" | tr '\n' ' ')"

  if ! git clone --quiet "$B/$id.bundle" "$d" 2>"$SCRATCH/$id.err"; then
    add "clone failed: $(tr '\n' ' ' < "$SCRATCH/$id.err")"
    printf '%s\tfail\t0\t%s\t%s\n' "$id" "$(sha256sum < "$B/$id.bundle" | cut -d' ' -f1)" "$fail"
    continue
  fi

  # a. HEAD
  head=$(g rev-parse HEAD 2>/dev/null)
  [ "$head" = "$sha" ] || add "HEAD is $head"

  # b. exactly the ancestry
  g rev-list --all | sort > "$SCRATCH/$id.all"
  g rev-list "$sha" | sort > "$SCRATCH/$id.anc"
  n=$(wc -l < "$SCRATCH/$id.all")
  cmp -s "$SCRATCH/$id.all" "$SCRATCH/$id.anc" || add "commits beyond the ancestry"
  [ "$n" -eq "$expected" ] || add "has $n commits, ancestry has $expected"

  # c. no fix, or nothing later
  if [ "$fixlist" != "-" ]; then
    for f in $(echo "$fixlist" | tr ',' ' '); do
      g cat-file -e "$f^{commit}" 2>/dev/null && add "fix commit $f present"
    done
  else
    own=$(g log -1 --format=%ct "$sha")
    latest=$(g log --all --format=%ct | sort -n | tail -1)
    [ "$latest" -le "$own" ] || add "a commit is committed later than the entry"
  fi

  # d. no remotes, refs or reflog
  g remote remove origin
  [ -z "$(g remote)" ] || add "remotes remain: $(g remote | tr '\n' ' ')"
  [ -z "$(g for-each-ref refs/remotes)" ] || add "remote-tracking refs remain"
  [ -z "$(g for-each-ref)" ] || add "refs remain: $(g for-each-ref --format='%(refname)' | tr '\n' ' ')"
  g reflog expire --expire=now --all
  [ -z "$(g log -g --all --format=%H 2>/dev/null)" ] || add "reflog entries remain"

  verdict=pass
  [ -z "$fail" ] || verdict=fail
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$verdict" "$n" \
    "$(sha256sum < "$B/$id.bundle" | cut -d' ' -f1)" "$fail"
  rm -rf "$d"
done
rm -rf "$SCRATCH"
