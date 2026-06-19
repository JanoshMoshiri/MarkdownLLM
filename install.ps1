#!/usr/bin/env pwsh
#
# MarkdownLLM installer (Windows / PowerShell 7+).
#
# Run from any folder (downloads + sets everything up):
#   irm https://raw.githubusercontent.com/JanoshMoshiri/MarkdownLLM/main/install.ps1 | iex
#
# Or from inside a checkout you already cloned:
#   ./install.ps1
#
# It checks prerequisites, clones the framework if needed, installs PyYAML and
# the deterministic-floor pre-commit hook, and verifies the result with
# `mdllm doctor`. If git/Python are missing it offers to install them through
# winget (with consent) and otherwise prints the command for you to run.
# Pass -Yes to skip the prompt. Safe to re-run.

param([switch]$Yes)

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
  Say 'Cloning MarkdownLLM into ./MarkdownLLM'
  git clone $RepoUrl MarkdownLLM
  if ($LASTEXITCODE -ne 0) { Stop2 'git clone failed.' }
  $RepoDir = Join-Path (Get-Location).Path 'MarkdownLLM'
}
Set-Location $RepoDir

# --- 4. PyYAML (the only dependency we install for you) ---
Say 'Ensuring PyYAML is available'
RunPy '-c' 'import yaml' 2>$null
if ($LASTEXITCODE -eq 0) {
  Ok 'pyyaml already installed'
} else {
  RunPy '-m' 'pip' 'install' 'pyyaml' | Out-Null
  if ($LASTEXITCODE -eq 0) {
    Ok 'pyyaml installed'
  } else {
    Warn 'automatic pip install failed. Try:'
    Write-Host "       $PyCmd -m pip install --user pyyaml"
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

# --- 6. deterministic floor: pre-commit hook on the framework repo ---
Say 'Installing the deterministic floor (pre-commit hook)'
RunPy 'tools/mdllm.py' 'install-hook' '.' | Out-Null
if ($LASTEXITCODE -eq 0) { Ok 'hook installed' }
else { Warn "hook install reported a problem — see 'mdllm doctor .' output below." }

# --- 7. Claude Code wrapper (non-destructive; harmless for other harnesses) ---
if (-not (Test-Path 'CLAUDE.md')) {
  @'
---
name: MarkdownLLM
description: Definition-driven framework — agents reason within domains you define
---

# MarkdownLLM — Claude Code Instructions

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
