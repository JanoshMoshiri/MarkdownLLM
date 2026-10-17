#!/bin/sh
# mdllm.sh — the POSIX twin of mdllm.ps1: run the MarkdownLLM CLI through an
# interpreter that can actually import PyYAML, selected the same way the
# installed git hooks select theirs.
#
# Why this exists: `python tools/mdllm.py` assumes the visible interpreter
# carries the floor's one dependency, and on managed shells it often does
# not. The hooks solve that with an embedded candidate walk; a shell line
# that must run BEFORE an agent reads anything — a slash command's `!`
# block, a bootstrap — needs the same walk without a hook to borrow it from.
# The block between the markers below is `hook_contract.SH_RESOLVE`
# verbatim; a test pins the two together so there is one owner.
#
# Usage: sh tools/mdllm.sh <command> [args...]
# From a nested domain: sh ../../tools/mdllm.sh <command> [args...]

set -u
MDLLM_SH_SELF=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
MDLLM="$MDLLM_SH_SELF/mdllm.py"
# Two roots, as in mdllm.ps1: the opened repository (nearest .git up from the
# working directory) supplies the first .venv candidate; the framework —
# derived from this file's own location inside SH_RESOLVE — the second.
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || ROOT="${MDLLM%/*/*}"
# --- begin SH_RESOLVE (hook_contract.py) ---
FW="${MDLLM%/*/*}"
PY=""
PY_PREFIX=""
MDLLM_LAUNCH_DEADLINE=""
MDLLM_DATE=""
MDLLM_TIMEOUT=""
if [ -x /usr/bin/date ] && [ -x /usr/bin/timeout ]; then
  MDLLM_DATE=/usr/bin/date
  MDLLM_TIMEOUT=/usr/bin/timeout
elif timeout --version >/dev/null 2>&1 && date +%s >/dev/null 2>&1; then
  MDLLM_DATE=date
  MDLLM_TIMEOUT=timeout
fi
if [ -n "$MDLLM_DATE" ] && [ -n "$MDLLM_TIMEOUT" ]; then
  MDLLM_LAUNCH_DEADLINE=$(( $("$MDLLM_DATE" +%s) + 10 ))
fi
mdllm_probe() {
  [ -n "$MDLLM_LAUNCH_DEADLINE" ] || return 1
  mdllm_remaining=$(( MDLLM_LAUNCH_DEADLINE - $("$MDLLM_DATE" +%s) ))
  [ "$mdllm_remaining" -gt 0 ] || return 1
  "$MDLLM_TIMEOUT" "$mdllm_remaining" "$@" -c "import yaml" >/dev/null 2>&1
}
MDLLM_WINDOWS_SH="${MSYSTEM:-}"
if [ -z "$PY" ] && [ -x "$ROOT/.venv/bin/python" ] && mdllm_probe "$ROOT/.venv/bin/python"; then
  PY="$ROOT/.venv/bin/python"
fi
if [ -z "$PY" ] && [ -n "$MDLLM_WINDOWS_SH" ] && [ -x "$ROOT/.venv/Scripts/python.exe" ] && mdllm_probe "$ROOT/.venv/Scripts/python.exe"; then
  PY="$ROOT/.venv/Scripts/python.exe"
fi
if [ -z "$PY" ] && [ -x "$FW/.venv/bin/python" ] && mdllm_probe "$FW/.venv/bin/python"; then
  PY="$FW/.venv/bin/python"
fi
if [ -z "$PY" ] && [ -n "$MDLLM_WINDOWS_SH" ] && [ -x "$FW/.venv/Scripts/python.exe" ] && mdllm_probe "$FW/.venv/Scripts/python.exe"; then
  PY="$FW/.venv/Scripts/python.exe"
fi
if [ -z "$PY" ] && command -v python3 >/dev/null 2>&1 && mdllm_probe python3; then
  PY="python3"
fi
if [ -z "$PY" ] && command -v python >/dev/null 2>&1 && mdllm_probe python; then
  PY="python"
fi
if [ -z "$PY" ] && [ -n "$MDLLM_WINDOWS_SH" ] && command -v py >/dev/null 2>&1 && mdllm_probe py "-3"; then
  PY="py"
  PY_PREFIX="-3"
fi
mdllm_python() {
  if [ -n "$PY_PREFIX" ]; then
    "$PY" "$PY_PREFIX" "$@"
  else
    "$PY" "$@"
  fi
}
# --- end SH_RESOLVE ---
if [ -z "$PY" ]; then
  echo "mdllm: no interpreter with PyYAML was found. Create a repository or framework .venv with Python 3.10+ and PyYAML, or install PyYAML into a candidate, then rerun this same mdllm.sh command. Do not substitute a harness-bundled Python unless it passes -c \"import yaml\"." >&2
  exit 127
fi
mdllm_python "$MDLLM" "$@"
