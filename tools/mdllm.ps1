#!/usr/bin/env pwsh
<#
.SYNOPSIS
Runs the MarkdownLLM CLI through a repository-local virtual environment.

.DESCRIPTION
Managed shells can provide Python outside PATH, or provide a minimal Python
without PyYAML. This wrapper prefers .venv/Scripts/python.exe, then falls back
to python, python3, and the Windows launcher. It keeps the public CLI command
surface intact without requiring a machine-wide PATH change.
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$MdllmArguments
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$entry = Join-Path $PSScriptRoot 'mdllm.py'
$venvPython = Join-Path $root '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $venvPython) {
    & $venvPython $entry @MdllmArguments
    exit $LASTEXITCODE
}

foreach ($name in 'python', 'python3') {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $command) { continue }
    & $command.Source -c 'import sys' 2>$null
    if ($LASTEXITCODE -ne 0) { continue }
    & $command.Source $entry @MdllmArguments
    exit $LASTEXITCODE
}

$launcher = Get-Command py -ErrorAction SilentlyContinue
if ($launcher) {
    & $launcher.Source -3 $entry @MdllmArguments
    exit $LASTEXITCODE
}

Write-Error 'mdllm: Python 3.10+ was not found. Create .venv with PyYAML or install Python.'
