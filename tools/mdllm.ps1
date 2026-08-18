#!/usr/bin/env pwsh
<#
.SYNOPSIS
Runs the MarkdownLLM CLI through a repository-local virtual environment.

.DESCRIPTION
Managed shells can provide Python outside PATH, or provide a minimal Python
without PyYAML. This wrapper prefers the calling repository's
.venv/Scripts/python.exe, then the framework environment, then PATH candidates.
It keeps the public CLI command surface intact without requiring a machine-wide
PATH change.
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$MdllmArguments
)

$ErrorActionPreference = 'Stop'
$frameworkRoot = Split-Path -Parent $PSScriptRoot
$entry = Join-Path $PSScriptRoot 'mdllm.py'

# Manual invocation has two roots just like a rendered lifecycle hook: the
# directly opened repository supplies the first environment candidate, while
# this script's own location supplies the framework environment. Walking for
# the nearest .git avoids a second git/runtime dependency before resolution.
$invocationRoot = $frameworkRoot
try {
    $locationPath = (Get-Location).ProviderPath
    if ($locationPath) {
        $invocationRoot = $locationPath
        $cursor = Get-Item -LiteralPath $locationPath
        while ($null -ne $cursor) {
            if (Test-Path -LiteralPath (Join-Path $cursor.FullName '.git')) {
                $invocationRoot = $cursor.FullName
                break
            }
            $cursor = $cursor.Parent
        }
    }
}
catch {
    $invocationRoot = $frameworkRoot
}

$resolver = Join-Path $PSScriptRoot 'resolve-runtime.ps1'
if (Test-Path -LiteralPath $resolver) {
    . $resolver
    $launch = Resolve-MdllmPython -Root $invocationRoot `
        -FrameworkRoot $frameworkRoot `
        -TimeoutSeconds 10
    if ($launch) {
        & $launch.Executable @($launch.PrefixArguments) $entry @MdllmArguments
        exit $LASTEXITCODE
    }
}

Write-Error 'mdllm: no interpreter with PyYAML was found. Create a repository or framework .venv with Python 3.10+ and PyYAML, or install PyYAML into a candidate, then rerun this same mdllm.ps1 command. Do not substitute a harness-bundled Python unless it passes `-c "import yaml"`.'
