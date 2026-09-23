<#
The dispatcher's tick — one command a scheduler runs on the machine that holds
the substrate (dispatcher-ticks-headless-on-the-substrate-machine-2026-09-23).

It composes the launch with `mdllm dispatch-payload` (the standing prompt,
the scope, the stop condition, the launch context — emitted whole, never
pointed at) and hands it to a harness's headless mode. No application need be
open: the harness must be installed, signed in under the task's user, and
pre-trusted for the tools the run uses. That trust is the operator's grant and
is passed here as -HarnessArgs; the defaults below are a proposal, not a policy.

  .\tools\dispatch\tick.ps1 -Scope domain/<name>
  .\tools\dispatch\tick.ps1 -Scope domain/a,domain/b -Harness codex
  .\tools\dispatch\tick.ps1 -DryRun            # print the command, launch nothing

Register it (the operator's act — one hand-registered task is an install; a
second seat owes the generated, doctor-checked entry the design named):

  schtasks /Create /TN "MarkdownLLM dispatch tick" /SC DAILY /ST 08:00 /RL LIMITED ^
    /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\Jamos\Projects\MarkdownLLM\tools\dispatch\tick.ps1 -Scope domain/<name>"

Guards, in order: one tick at a time per clone (a pid lock under .git/, a
stale lock is taken); every launch carries a stop condition (the prompt
refuses one without); the run's output is logged under .git/mdllm-dispatch/,
per clone, never committed. The digest the run writes is the repo's, per
dispatch-digest-home-2026-08-29.
#>
param(
    [string[]]$Scope = @(),
    [ValidateSet('claude', 'codex')][string]$Harness = 'claude',
    [string]$StopCondition = 'queue drained, or 25 minutes of work, whichever comes first',
    [string]$Name = 'windows-task',
    [string[]]$HarnessArgs,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$stamp = Get-Date -Format 'yyyy-MM-ddTHH-mm-ss'
$logDir = Join-Path $root '.git\mdllm-dispatch'
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir "$stamp.log"
$lock = Join-Path $logDir 'tick.pid'

# One tick at a time. A lock whose process is gone is stale and is taken.
if (Test-Path $lock) {
    $pid0 = Get-Content $lock -ErrorAction SilentlyContinue
    if ($pid0 -and (Get-Process -Id $pid0 -ErrorAction SilentlyContinue)) {
        "tick: another tick is running (pid $pid0) — refusing; exit 3" | Tee-Object -FilePath $log -Append
        exit 3
    }
}
Set-Content $lock $PID
try {
    $context = "$Name@$env:COMPUTERNAME"
    $scopeArgs = @()
    foreach ($s in $Scope) { $scopeArgs += @('--scope', $s) }
    $payload = Join-Path $logDir "$stamp.payload.md"
    Push-Location $root
    try {
        & (Join-Path $root 'tools\mdllm.ps1') dispatch-payload . @scopeArgs `
            --stop-condition $StopCondition --launch-context $context | Set-Content -Path $payload -Encoding utf8
        if ($LASTEXITCODE -ne 0) { throw "dispatch-payload exited $LASTEXITCODE" }
    }
    finally { Pop-Location }

    # The harness command. Both read the whole launch text as their prompt and
    # exit when the run ends; neither needs an application open.
    if (-not $HarnessArgs) {
        $HarnessArgs = switch ($Harness) {
            # Claude Code: headless print mode. The tools a dispatch run needs
            # (git, the floor, file edits) are pre-trusted here — review before
            # registering; widen or narrow to taste.
            'claude' { @('-p', '--output-format', 'text', '--permission-mode', 'acceptEdits',
                         '--allowedTools', 'Bash(git:*)', 'Bash(python:*)', 'Bash(*mdllm*)', 'Edit', 'Write', 'Read', 'Glob', 'Grep') }
            # Codex: one non-interactive turn in the estate root.
            'codex'  { @('exec', '--cd', $root, '--full-auto') }
        }
    }
    $cmdline = "$Harness $($HarnessArgs -join ' ')  < $payload"
    "tick $stamp  context=$context  scope=$(if ($Scope) { $Scope -join ',' } else { '(estate-wide walk)' })" | Tee-Object -FilePath $log -Append
    "launch: $cmdline" | Tee-Object -FilePath $log -Append
    if ($DryRun) { "dry run — payload at $payload, nothing launched" | Tee-Object -FilePath $log -Append; exit 0 }

    Push-Location $root
    try {
        $text = Get-Content $payload -Raw
        if ($Harness -eq 'codex') {
            & $Harness @HarnessArgs $text 2>&1 | Tee-Object -FilePath $log -Append
        } else {
            $text | & $Harness @HarnessArgs 2>&1 | Tee-Object -FilePath $log -Append
        }
        $code = $LASTEXITCODE
    }
    finally { Pop-Location }
    "tick ended: $Harness exited $code" | Tee-Object -FilePath $log -Append
    exit $code
}
finally {
    Remove-Item $lock -ErrorAction SilentlyContinue
}
