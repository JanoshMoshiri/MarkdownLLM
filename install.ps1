#!/usr/bin/env pwsh
#
# MarkdownLLM installer (Windows / PowerShell 7+).
#
# Run from a release-pinned checkout whose installer hash you verified (the
# exact commands and current hashes are in README.md):
#   ./install.ps1
#
# Direct invocation outside a checkout is also supported, but requires the
# immutable release commit explicitly:
#   ./install.ps1 -Ref <40-character-release-commit>
#
# It checks prerequisites, clones the framework if needed, installs PyYAML and
# the deterministic-floor git hooks (validation, disclosure boundary,
# publication leg), and verifies the result with
# `mdllm doctor`. If git/Python are missing it offers to install them through
# winget (with consent) and otherwise prints the command for you to run.
# Pass -Yes to skip the prompt. Safe to re-run.

param(
  [switch]$Yes,
  [string]$Ref = $env:MARKDOWNLLM_RELEASE_COMMIT
)

$ErrorActionPreference = 'Stop'
$RepoUrl = 'https://github.com/JanoshMoshiri/MarkdownLLM.git'

function Say  ($m) { Write-Host "==> $m" -ForegroundColor Blue }
function Ok   ($m) { Write-Host "  OK   $m" -ForegroundColor Green }
function Warn ($m) { Write-Host "  WARN $m" -ForegroundColor Yellow }
function Stop2($m) { Write-Host "  STOP $m" -ForegroundColor Red; exit 1 }

# Offer (never force) a winget install; fall back to a guided message.
function Ensure-Winget ($Label, $WingetId) {
  $cmd = "winget install -e --id $WingetId --accept-package-agreements --accept-source-agreements"
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "  MISSING $Label" -ForegroundColor Red
    Write-Host "     winget not found. Install $Label, then re-run this script."
    exit 1
  }
  $proceed = $Yes.IsPresent
  if (-not $proceed) {
    Write-Host "  MISSING $Label. winget is available." -ForegroundColor Yellow
    Write-Host "     Install with: $cmd"
    $proceed = (Read-Host '     Proceed? [y/N]') -match '^(y|yes)$'
  }
  if (-not $proceed) { Write-Host '     Skipped — install it yourself, then re-run.'; exit 1 }
  Say "Installing $Label"
  Invoke-Expression $cmd
}

$script:PyCmd = $null
$script:PyPre = @()
function Resolve-Python {
  foreach ($cand in @('python', 'python3', 'py')) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) {
      $pre = if ($cand -eq 'py') { @('-3') } else { @() }
      & $cand @pre '-c' 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>$null
      if ($LASTEXITCODE -eq 0) { $script:PyCmd = $cand; $script:PyPre = $pre; return $true }
    }
  }
  return $false
}
function RunPy { & $script:PyCmd @script:PyPre @args }

Say 'Checking prerequisites'

# --- 1. git ---
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Ensure-Winget 'git' 'Git.Git'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Stop2 'git still not on PATH — open a new terminal (PATH may need a refresh), then re-run.'
}
Ok ("git " + (((git --version) -split ' ')[2]))

# --- 2. python >= 3.10 ---
if (-not (Resolve-Python)) {
  Ensure-Winget 'Python 3.10+' 'Python.Python.3.12'
  if (-not (Resolve-Python)) {
    Stop2 'Python 3.10+ still not found — open a new terminal (PATH may need a refresh), then re-run.'
  }
}
Ok (RunPy '--version')

# --- 3. locate or clone the framework ---
function In-Checkout ($dir) {
  (Test-Path (Join-Path $dir 'tools/mdllm.py')) -and (Test-Path (Join-Path $dir 'AGENTS.md'))
}

$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { $null }
$RepoDir = $null
if ($ScriptDir -and (In-Checkout $ScriptDir)) {
  $RepoDir = $ScriptDir
} elseif (In-Checkout (Get-Location).Path) {
  $RepoDir = (Get-Location).Path
}

if ($RepoDir) {
  Say "Using existing checkout: $RepoDir"
} else {
  if (Test-Path 'MarkdownLLM') {
    Stop2 "./MarkdownLLM already exists but isn't a framework checkout — move it aside and re-run."
  }
  if ($Ref -notmatch '^[0-9a-fA-F]{40}$') {
    Stop2 'outside a checkout, pass -Ref with the full 40-character release commit; moving branches are not an install authority'
  }
  Say "Fetching MarkdownLLM release commit $Ref into ./MarkdownLLM"
  git init -q MarkdownLLM
  if ($LASTEXITCODE -ne 0) { Stop2 'git init failed.' }
  git -C MarkdownLLM remote add origin $RepoUrl
  if ($LASTEXITCODE -ne 0) { Stop2 'adding origin failed.' }
  git -C MarkdownLLM fetch --depth 1 origin "${Ref}:refs/remotes/origin/verified-release"
  if ($LASTEXITCODE -ne 0) { Stop2 'fetching the release commit failed.' }
  $Fetched = (git -C MarkdownLLM rev-parse FETCH_HEAD).Trim()
  if ($LASTEXITCODE -ne 0 -or $Fetched -ne $Ref.ToLowerInvariant()) {
    Stop2 'fetched commit did not match -Ref.'
  }
  git -C MarkdownLLM checkout -q --detach $Ref
  if ($LASTEXITCODE -ne 0) { Stop2 'checking out the release commit failed.' }
  $RepoDir = Join-Path (Get-Location).Path 'MarkdownLLM'
}
Set-Location $RepoDir

# --- 4. PyYAML (the only dependency we install for you) ---
Say 'Ensuring PyYAML 6.0.3 is available'
RunPy '-c' 'import yaml, sys; sys.exit(0 if yaml.__version__ == "6.0.3" else 1)' 2>$null
if ($LASTEXITCODE -eq 0) {
  Ok 'pyyaml 6.0.3 already installed'
} else {
  RunPy '-m' 'pip' 'install' 'PyYAML==6.0.3' | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Ok 'pyyaml 6.0.3 installed'
  } else {
    Warn 'automatic pip install failed. Try:'
    Write-Host "       $PyCmd -m pip install --user PyYAML==6.0.3"
    Stop2 'install PyYAML, then re-run.'
  }
}

# --- 5. git identity (commits fail without it) ---
$gname = (git config user.name)  2>$null
$gmail = (git config user.email) 2>$null
if (-not $gname -or -not $gmail) {
  Warn 'git identity not fully set — commits will fail until you run:'
  Write-Host '       git config --global user.name  "Your Name"'
  Write-Host '       git config --global user.email "you@example.com"'
}

# --- 6. deterministic floor: git hooks on the framework repo ---
Say 'Installing the deterministic floor (pre-commit + commit-msg + post-commit hooks)'
RunPy 'tools/mdllm.py' 'install-hook' '.' | Out-Null
if ($LASTEXITCODE -eq 0) { Ok 'hooks installed' }
else { Warn "hook install reported a problem — see 'mdllm doctor .' output below." }

# --- 7. Claude Code wrapper (non-destructive; harmless for other harnesses) ---
if (-not (Test-Path 'CLAUDE.md')) {
  @'
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
'@ | Set-Content -Path 'CLAUDE.md' -Encoding utf8
  Ok 'wrote CLAUDE.md (Claude Code -> AGENTS.md). Delete it if your harness auto-discovers AGENTS.md.'
}

# --- 8. verify the whole environment ---
Say 'Verifying the environment (mdllm doctor)'
Write-Host ''
RunPy 'tools/mdllm.py' 'doctor' '.'
Write-Host ''

# --- done ---
Write-Host "Done. MarkdownLLM is ready at: $RepoDir" -ForegroundColor Green
Write-Host ''
Write-Host @"
Next:
  1. Open this folder as a workspace in your agent/editor:
       Set-Location "$RepoDir"
       code .          # VS Code / Copilot / Cursor (or open the folder in your tool)
  2. Let the agent discover AGENTS.md, then tell it what to build, e.g.:
       "I want a domain for tracking architectural decisions across our
        microservices — context, options considered, decision, consequences."
  3. The full paced walkthrough is in docs/first-hour.md.
"@
