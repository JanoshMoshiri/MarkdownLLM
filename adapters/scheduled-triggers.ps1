# Proactive trigger evaluation (transformation plan Phase 7).
# Runs `mdllm triggers` against a domain and raises a Windows toast when any
# trigger condition is true — deadlines surface without anyone opening a session.
#
# Register daily at 08:00 (run from the framework root):
#   schtasks /Create /TN "MarkdownLLM Triggers" /SC DAILY /ST 08:00 /TR `
#     "pwsh -NoProfile -File '$PWD\adapters\scheduled-triggers.ps1' -DomainPath '$PWD\domain\jmtm-software'"
param(
    [Parameter(Mandatory)] [string]$DomainPath,
    [string]$FrameworkRoot = (Split-Path $PSScriptRoot -Parent)
)

$output = python "$FrameworkRoot\tools\mdllm.py" triggers $DomainPath 2>&1 | Out-String
$logDir = Join-Path $FrameworkRoot "adapters\logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$output | Set-Content (Join-Path $logDir "triggers-$(Get-Date -Format yyyy-MM-dd).log")

if ($output -notmatch "No trigger conditions currently true") {
    # Something needs attention — surface it.
    $hits = ($output -split "`n" | Where-Object { $_ -match "^- " }) -join "`n"
    try {
        # BurntToast module if available; fall back to a message box.
        if (Get-Module -ListAvailable BurntToast) {
            Import-Module BurntToast
            New-BurntToastNotification -Text "MarkdownLLM: triggers firing", $hits
        }
        else {
            Add-Type -AssemblyName System.Windows.Forms
            [System.Windows.Forms.MessageBox]::Show($hits, "MarkdownLLM: triggers firing") | Out-Null
        }
    }
    catch { Write-Warning "Notification failed; see log. $_" }
    exit 2
}
exit 0
