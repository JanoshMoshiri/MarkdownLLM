#!/bin/bash
# Enter the review-catch road as the reviewer, with the network lock in
# place. WSL keeps no firewall or daemon state across a restart, so the lock
# is applied at the start of every session.
#   wsl -d review-road -u root -- /usr/local/sbin/review-shell.sh            an interactive shell
#   wsl -d review-road -u root -- /usr/local/sbin/review-shell.sh CMD ARGS   one command as the reviewer
set -eu
/usr/local/sbin/review-network.sh >/dev/null
if [ "$#" -eq 0 ]; then
  exec runuser -l reviewer
fi
exec runuser -l reviewer -c "$(printf '%q ' "$@")"
