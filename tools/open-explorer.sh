#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
framework_root="$(cd "${script_dir}/.." && pwd -P)"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "MarkdownLLM Explorer: this launcher is for macOS." >&2
  exit 2
fi

state_root="${HOME:?}/Library/Application Support/MarkdownLLM Explorer/portable"
venv_root="${state_root}/venv"
pid_file="${state_root}/explorer.pid"

owned_process() {
  local pid="$1"
  [[ "${pid}" =~ ^[0-9]+$ ]] || return 1
  kill -0 "${pid}" 2>/dev/null || return 1
  local command_line
  command_line="$(ps -ww -p "${pid}" -o command= 2>/dev/null || true)"
  [[ "${command_line}" == *"mdllm-explorer"* && "${command_line}" == *"${framework_root}"* ]]
}

stop_owned_process() {
  [[ -f "${pid_file}" ]] || return 0
  local pid
  pid="$(tr -d '[:space:]' < "${pid_file}")"
  if ! owned_process "${pid}"; then
    rm -f "${pid_file}"
    return 0
  fi
  kill -INT "${pid}"
  for _ in {1..50}; do
    kill -0 "${pid}" 2>/dev/null || break
    sleep 0.1
  done
  if kill -0 "${pid}" 2>/dev/null; then
    echo "MarkdownLLM Explorer: the existing owned process did not stop." >&2
    return 1
  fi
  rm -f "${pid_file}"
}

if [[ "${1:-}" == "--stop" ]]; then
  if [[ "${2:-}" != "" ]]; then
    echo "Usage: bash tools/open-explorer.sh [--stop]" >&2
    exit 2
  fi
  stop_owned_process
  echo "MarkdownLLM Explorer is stopped."
  exit 0
elif [[ "${1:-}" != "" ]]; then
  echo "Usage: bash tools/open-explorer.sh [--stop]" >&2
  exit 2
fi

python_command=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "${candidate}" >/dev/null 2>&1 \
    && "${candidate}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
    python_command="${candidate}"
    break
  fi
done
if [[ -z "${python_command}" ]]; then
  echo "MarkdownLLM Explorer needs Python 3.10 or newer. Ask Claude Code to install Python, then try again." >&2
  exit 2
fi

mkdir -p "${state_root}"
if [[ ! -x "${venv_root}/bin/python" ]]; then
  "${python_command}" -m venv "${venv_root}"
fi
"${venv_root}/bin/python" -m pip install --disable-pip-version-check --upgrade "${framework_root}/explorer"

stop_owned_process
error_file="$(mktemp "${TMPDIR:-/tmp}/mdllm-explorer.XXXXXX")"
nohup "${venv_root}/bin/mdllm-explorer" --root "${framework_root}" --open-browser >/dev/null 2>"${error_file}" &
explorer_pid=$!
printf '%s\n' "${explorer_pid}" > "${pid_file}"
sleep 2

if ! owned_process "${explorer_pid}"; then
  wait "${explorer_pid}" || true
  echo "MarkdownLLM Explorer did not start:" >&2
  sed -n '1,20p' "${error_file}" >&2
  rm -f "${pid_file}" "${error_file}"
  exit 2
fi

rm -f "${error_file}"
echo "MarkdownLLM Explorer is open. It will keep running until you stop it."
echo "To stop it now: bash tools/open-explorer.sh --stop"
