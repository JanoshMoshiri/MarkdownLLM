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

function Test-FloorPython {
    param(
        [Parameter(Mandatory = $true)][string]$Executable,
        [string[]]$PrefixArguments = @()
    )
    try {
        & $Executable @PrefixArguments -c 'import yaml' 2>$null
        return $LASTEXITCODE -eq 0
    }
    catch {
        # Windows PowerShell 5.1 promotes native stderr to RemoteException
        # under ErrorActionPreference=Stop. That is one failed candidate fact,
        # not a reason to terminate resolution.
        return $false
    }
}

$venvPython = Join-Path $root '.venv\Scripts\python.exe'
if (Test-Path -LiteralPath $venvPython) {
    # Same policy as the emitted POSIX resolver (runtime.py): a candidate is
    # usable only if the floor's dependency loads — an incomplete venv must
    # fall through, not crash the CLI.
    if (Test-FloorPython -Executable $venvPython) {
        & $venvPython $entry @MdllmArguments
        exit $LASTEXITCODE
    }
}

foreach ($name in 'python', 'python3') {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $command) { continue }
    # Probe the floor's real dependency, not just interpreter presence — a
    # bare python without PyYAML passes an interpreter-only probe and then
    # crashes the CLI with a traceback naming neither cause (runtime.py owns
    # this rule).
    if (-not (Test-FloorPython -Executable $command.Source)) { continue }
    & $command.Source $entry @MdllmArguments
    exit $LASTEXITCODE
}

$launcher = Get-Command py -ErrorAction SilentlyContinue
if ($launcher) {
    if (Test-FloorPython -Executable $launcher.Source -PrefixArguments @('-3')) {
        & $launcher.Source -3 $entry @MdllmArguments
        exit $LASTEXITCODE
    }
}

Write-Error 'mdllm: no interpreter with PyYAML was found. Create .venv with PyYAML or install Python 3.10+; `python tools/mdllm.py runtime-probe .` reports each candidate once any python is available.'
