#!/bin/sh
# Network lock for the review-catch road (review-catch-on-the-road, Phase 1).
# Run as root inside the review-road WSL distro, at every start of the distro
# (WSL keeps no firewall state across a restart).
#
# The reviewer user may open connections only to the local proxy. The proxy
# lets through only the two vendors' model and sign-in services; GitHub and
# the rest of the web stay out of reach, because the answer key is public.
set -eu

FILTER=/etc/tinyproxy/filter
cat > "$FILTER" <<'EOF'
(^|\.)anthropic\.com$
(^|\.)claude\.ai$
(^|\.)claude\.com$
(^|\.)openai\.com$
(^|\.)chatgpt\.com$
(^|\.)oaistatic\.com$
EOF

CONF=/etc/tinyproxy/tinyproxy.conf
sed -i -E 's/^#?Filter .*/Filter "\/etc\/tinyproxy\/filter"/' "$CONF"
grep -q '^Filter ' "$CONF" || echo 'Filter "/etc/tinyproxy/filter"' >> "$CONF"
sed -i -E 's/^#?FilterDefaultDeny .*/FilterDefaultDeny Yes/' "$CONF"
grep -q '^FilterDefaultDeny ' "$CONF" || echo 'FilterDefaultDeny Yes' >> "$CONF"
sed -i -E 's/^#?FilterExtended .*/FilterExtended On/' "$CONF"
grep -q '^FilterExtended ' "$CONF" || echo 'FilterExtended On' >> "$CONF"
sed -i -E 's/^#?FilterType .*/FilterType ere/' "$CONF"
sed -i -E 's/^Listen .*//' "$CONF"
echo 'Listen 127.0.0.1' >> "$CONF"
sed -i -E 's/^Port .*/Port 8888/' "$CONF"

mkdir -p /run/tinyproxy /var/log/tinyproxy
chown tinyproxy:tinyproxy /run/tinyproxy /var/log/tinyproxy
pkill -x tinyproxy 2>/dev/null || true
sleep 1
tinyproxy -c "$CONF"
sleep 1
pgrep -x tinyproxy >/dev/null || { echo "proxy did not start" >&2; exit 1; }

RUID=$(id -u reviewer)
iptables -F OUTPUT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -m owner --uid-owner "$RUID" -j REJECT
ip6tables -F OUTPUT 2>/dev/null || true
ip6tables -A OUTPUT -o lo -j ACCEPT 2>/dev/null || true
ip6tables -A OUTPUT -m owner --uid-owner "$RUID" -j REJECT 2>/dev/null || true

PROFILE=/etc/profile.d/review-proxy.sh
cat > "$PROFILE" <<'EOF'
export HTTPS_PROXY=http://127.0.0.1:8888
export HTTP_PROXY=http://127.0.0.1:8888
export https_proxy=http://127.0.0.1:8888
export http_proxy=http://127.0.0.1:8888
export NO_PROXY=localhost,127.0.0.1
export no_proxy=localhost,127.0.0.1
EOF
echo "network lock in place"
