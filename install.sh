#!/usr/bin/env bash
#
# MarkdownLLM installer (macOS / Linux / Git-Bash).
#
# Run from any folder (downloads + sets everything up):
#   curl -fsSL https://raw.githubusercontent.com/JanoshMoshiri/MarkdownLLM/main/install.sh | bash
#
# Or from inside a checkout you already cloned:
#   ./install.sh
#
# It checks prerequisites, clones the framework if needed, installs PyYAML and
# the deterministic-floor git hooks (validation, disclosure boundary,
# publication leg), and verifies the result with
# `mdllm doctor`. If git/Python are missing it offers to install them through
# your OS package manager (with consent) and otherwise prints the command for
# you to run. Pass -y / --yes to skip the prompt. Safe to re-run.

set -euo pipefail

REPO_URL="https://github.com/JanoshMoshiri/MarkdownLLM.git"

if [ -t 1 ]; then
  BLUE='\033[34m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; NC='\033[0m'
else
  BLUE=''; GREEN=''; YELLOW=''; RED=''; NC=''
fi
say()  { printf "${BLUE}==>${NC} %s\n" "$1"; }
ok()   { printf "  ${GREEN}OK${NC}   %s\n" "$1"; }
warn() { printf "  ${YELLOW}WARN${NC} %s\n" "$1"; }
die()  { printf "  ${RED}STOP${NC} %s\n" "$1" >&2; exit 1; }

case "$(uname -s 2>/dev/null || echo other)" in
  Darwin) OS=mac ;;
  Linux)  OS=linux ;;
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  *) OS=other ;;
esac

git_hint() {
  case "$OS" in
    mac)   echo "xcode-select --install   # or: brew install git" ;;
    linux) echo "sudo apt install git     # or your distro's package manager" ;;
    win)   echo "winget install Git.Git" ;;
    *)     echo "see https://git-scm.com/downloads" ;;
  esac
}
py_hint() {
  case "$OS" in
    mac)   echo "brew install python@3.12" ;;
    linux) echo "sudo apt install python3 python3-pip" ;;
    win)   echo "winget install Python.Python.3.12" ;;
    *)     echo "see https://www.python.org/downloads/" ;;
  esac
}

# --- consent-based dependency install (offered, never forced) ---
AUTO_YES=0
for arg in "$@"; do case "$arg" in -y|--yes) AUTO_YES=1 ;; esac; done

PKG=""
case "$OS" in
  mac) command -v brew >/dev/null 2>&1 && PKG="brew" ;;
  win) command -v winget >/dev/null 2>&1 && PKG="winget" ;;
  linux)
    for m in apt-get dnf pacman zypper; do
      command -v "$m" >/dev/null 2>&1 && { PKG="$m"; break; }
    done ;;
esac

install_cmd() { # $1 = git|python -> the install command for $PKG, or empty
  case "$PKG:$1" in
    brew:git)       echo "brew install git" ;;
    brew:python)    echo "brew install python@3.12" ;;
    winget:git)     echo "winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements" ;;
    winget:python)  echo "winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements" ;;
    apt-get:git)    echo "sudo apt-get update && sudo apt-get install -y git" ;;
    apt-get:python) echo "sudo apt-get update && sudo apt-get install -y python3 python3-pip" ;;
    dnf:git)        echo "sudo dnf install -y git" ;;
    dnf:python)     echo "sudo dnf install -y python3 python3-pip" ;;
    pacman:git)     echo "sudo pacman -S --noconfirm git" ;;
    pacman:python)  echo "sudo pacman -S --noconfirm python python-pip" ;;
    zypper:git)     echo "sudo zypper install -y git" ;;
    zypper:python)  echo "sudo zypper install -y python3 python3-pip" ;;
    *) echo "" ;;
  esac
}
hint() { case "$1" in git) git_hint ;; python) py_hint ;; esac; }

maybe_install() { # $1 = key (git|python)  $2 = label
  local key="$1" label="$2" cmd reply
  cmd="$(install_cmd "$key")"
  # no package manager (or no recipe): fall back to a guided message
  if [ -z "$cmd" ]; then
    printf "  ${RED}MISSING${NC} %s\n     install: %s\n     then re-run this script.\n" "$label" "$(hint "$key")" >&2
    exit 1
  fi
  # piped / non-interactive without -y: never surprise-install system software
  if [ "$AUTO_YES" -ne 1 ] && [ ! -t 0 ]; then
    printf "  ${RED}MISSING${NC} %s\n     %s can install it — re-run with -y, or run:\n       %s\n" "$label" "$PKG" "$cmd" >&2
    exit 1
  fi
  if [ "$AUTO_YES" -ne 1 ]; then
    printf "  ${YELLOW}MISSING${NC} %s. %s is available.\n     Install with: %s\n" "$label" "$PKG" "$cmd"
    printf "     Proceed? [y/N] "
    read -r reply </dev/tty 2>/dev/null || reply=""
    case "$reply" in [yY]|[yY][eE][sS]) ;; *) echo "     Skipped — install it yourself, then re-run."; exit 1 ;; esac
  fi
  say "Installing $label"
  eval "$cmd" || true
}

resolve_py() {
  PY=""
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 \
       && "$cand" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
      PY="$cand"; return 0
    fi
  done
  return 1
}

say "Checking prerequisites"

# --- 1. git ---
command -v git >/dev/null 2>&1 || maybe_install git "git"
command -v git >/dev/null 2>&1 || die "git still not on PATH — open a new terminal (PATH may need a refresh), then re-run."
ok "git $(git --version | awk '{print $3}')"

# --- 2. python >= 3.10 ---
resolve_py || maybe_install python "Python 3.10+"
resolve_py || die "Python 3.10+ still not found — open a new terminal (PATH may need a refresh), then re-run."
ok "$("$PY" --version 2>&1)"

# --- 3. locate or clone the framework ---
in_checkout() { [ -f "$1/tools/mdllm.py" ] && [ -f "$1/AGENTS.md" ]; }

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE+x}" ] && [ -f "${BASH_SOURCE[0]:-}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

REPO_DIR=""
if [ -n "$SCRIPT_DIR" ] && in_checkout "$SCRIPT_DIR"; then
  REPO_DIR="$SCRIPT_DIR"
elif in_checkout "$PWD"; then
  REPO_DIR="$PWD"
fi

if [ -n "$REPO_DIR" ]; then
  say "Using existing checkout: $REPO_DIR"
else
  if [ -e "MarkdownLLM" ]; then
    die "./MarkdownLLM already exists but isn't a framework checkout — move it aside and re-run."
  fi
  say "Cloning MarkdownLLM into ./MarkdownLLM"
  git clone "$REPO_URL" MarkdownLLM
  REPO_DIR="$PWD/MarkdownLLM"
fi
cd "$REPO_DIR"

# --- 4. PyYAML (the only dependency we install for you) ---
say "Ensuring PyYAML is available"
if "$PY" -c 'import yaml' 2>/dev/null; then
  ok "pyyaml already installed"
elif "$PY" -m pip install pyyaml >/dev/null 2>&1; then
  ok "pyyaml installed"
else
  warn "automatic pip install failed. Try one of:"
  echo "       $PY -m pip install --user pyyaml"
  echo "       $PY -m pip install --break-system-packages pyyaml   # PEP 668 environments"
  die "install PyYAML, then re-run."
fi

# --- 5. git identity (commits fail without it) ---
if [ -z "$(git config user.name  || true)" ] || [ -z "$(git config user.email || true)" ]; then
  warn "git identity not fully set — commits will fail until you run:"
  echo '       git config --global user.name  "Your Name"'
  echo '       git config --global user.email "you@example.com"'
fi

# --- 6. deterministic floor: git hooks on the framework repo ---
say "Installing the deterministic floor (pre-commit + commit-msg + post-commit hooks)"
if "$PY" tools/mdllm.py install-hook . >/dev/null; then
  ok "hooks installed"
else
  warn "hook install reported a problem — see 'mdllm doctor .' output below."
fi

# --- 7. Claude Code wrapper (non-destructive; harmless for other harnesses) ---
if [ ! -f CLAUDE.md ]; then
  cat > CLAUDE.md <<'EOF'
---
name: MarkdownLLM
description: Definition-driven framework — agents reason within domains you define
---

# MarkdownLLM — Claude Code Instructions

This is the **framework root's** entry pointer. It is read from two
positions, and it routes each differently:

- **Your workspace is this directory** → the framework's entry file is
  imported below and governs the session.
- **This file arrived inherited from a parent directory** — your workspace
  is a domain nested under this framework → your workspace's own
  `CLAUDE.md` → `AGENTS.md` governs. Do not read or follow the framework
  root's `AGENTS.md`, whether or not the import below expanded: it is the
  framework repo's entry file, not your domain's.

@AGENTS.md
EOF
  ok "wrote CLAUDE.md (Claude Code -> AGENTS.md). Delete it if your harness auto-discovers AGENTS.md."
fi

# --- 8. verify the whole environment ---
say "Verifying the environment (mdllm doctor)"
echo
"$PY" tools/mdllm.py doctor . || true
echo

# --- done ---
printf "${GREEN}Done.${NC} MarkdownLLM is ready at: %s\n\n" "$REPO_DIR"
cat <<EOF
Next:
  1. Open this folder as a workspace in your agent/editor:
       cd "$REPO_DIR"
       code .          # VS Code / Copilot / Cursor (or open the folder in your tool)
  2. Let the agent discover AGENTS.md, then tell it what to build, e.g.:
       "I want a domain for tracking architectural decisions across our
        microservices — context, options considered, decision, consequences."
  3. The full paced walkthrough is in docs/first-hour.md.
EOF
