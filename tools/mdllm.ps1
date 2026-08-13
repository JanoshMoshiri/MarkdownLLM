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

$resolver = Join-Path $PSScriptRoot 'resolve-runtime.ps1'
if (Test-Path -LiteralPath $resolver) {
    . $resolver
    $launch = Resolve-MdllmPython -Root $root -FrameworkRoot $root `
        -TimeoutSeconds 10
    if ($launch) {
        & $launch.Executable @($launch.PrefixArguments) $entry @MdllmArguments
        exit $LASTEXITCODE
    }
}

Write-Error 'mdllm: no interpreter with PyYAML was found. Create .venv with PyYAML or install Python 3.10+; `python tools/mdllm.py runtime-probe .` reports each candidate once any python is available.'
