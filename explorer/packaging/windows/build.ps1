[CmdletBinding()]
param(
    [string]$Version = "0.2.0"
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$explorerRoot = (Resolve-Path (Join-Path $scriptRoot "..\..")).Path
$buildRoot = Join-Path $explorerRoot "build\windows"
$outputRoot = Join-Path $explorerRoot "dist"
$buildEnvironment = Join-Path $explorerRoot ".windows-build-venv"
$buildTools = Join-Path $explorerRoot ".windows-build-tools"
$sourcePng = Join-Path $explorerRoot "src\markdownllm_explorer\delivery\static\markdownllm-explorer.png"
$sourceIco = Join-Path $scriptRoot "assets\markdownllm-explorer.ico"

function Assert-ChildPath([string]$Candidate, [string]$Parent) {
    $parentPrefix = $Parent.TrimEnd('\') + '\'
    if (-not $Candidate.StartsWith($parentPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to operate outside the Explorer source tree: $Candidate"
    }
}

Assert-ChildPath $buildRoot $explorerRoot
Assert-ChildPath $outputRoot $explorerRoot
if (Test-Path -LiteralPath $buildRoot) {
    Remove-Item -LiteralPath $buildRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $buildRoot, $outputRoot | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $buildEnvironment "Scripts\python.exe"))) {
    $bootstrapPython = (Get-Command python.exe -ErrorAction Stop).Source
    & $bootstrapPython -m venv $buildEnvironment
}
$buildPython = Join-Path $buildEnvironment "Scripts\python.exe"
& $buildPython -m pip install --disable-pip-version-check ".[windows-build]"
if ($LASTEXITCODE -ne 0) { throw "The isolated Windows build dependencies could not be installed." }

& $buildPython (Join-Path $scriptRoot "generate_icons.py") --png $sourcePng --ico $sourceIco
if ($LASTEXITCODE -ne 0) { throw "Application icon generation failed." }

$pyInstallerDist = Join-Path $buildRoot "frozen"
$pyInstallerWork = Join-Path $buildRoot "pyinstaller"
& $buildPython -m PyInstaller --noconfirm --clean --distpath $pyInstallerDist --workpath $pyInstallerWork (Join-Path $scriptRoot "markdownllm-explorer.spec")
if ($LASTEXITCODE -ne 0) { throw "The native application bundle could not be built." }

$makeNsis = (Get-Command makensis.exe -ErrorAction SilentlyContinue).Source
if (-not $makeNsis) {
    foreach ($candidate in @(
        "$env:ProgramFiles\NSIS\makensis.exe",
        "${env:ProgramFiles(x86)}\NSIS\makensis.exe",
        "$env:LOCALAPPDATA\Programs\NSIS\makensis.exe"
    )) {
        if (Test-Path -LiteralPath $candidate) { $makeNsis = $candidate; break }
    }
}
if (-not $makeNsis) {
    New-Item -ItemType Directory -Force -Path $buildTools | Out-Null
    $nsisArchive = Join-Path $buildTools "nsis-3.12.zip"
    $nsisRoot = Join-Path $buildTools "nsis-3.12"
    $expectedNsisHash = "56581F90DB321581C5381193D796FFFCF2D24B2F8FED2160A6C6A3BAA67F2C4F"
    if (-not (Test-Path -LiteralPath $nsisArchive)) {
        Invoke-WebRequest -UseBasicParsing -Uri "https://sourceforge.net/projects/nsis/files/NSIS%203/3.12/nsis-3.12.zip/download" -OutFile $nsisArchive
    }
    $observedNsisHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $nsisArchive).Hash
    if ($observedNsisHash -ne $expectedNsisHash) { throw "The downloaded NSIS archive did not match its pinned SHA-256 digest." }
    if (-not (Test-Path -LiteralPath (Join-Path $nsisRoot "makensis.exe"))) {
        Expand-Archive -LiteralPath $nsisArchive -DestinationPath $buildTools -Force
    }
    $makeNsis = Join-Path $nsisRoot "makensis.exe"
}
if (-not $makeNsis) { throw "makensis.exe was not found after NSIS installation." }

$frozenApplication = Join-Path $pyInstallerDist "MarkdownLLM Explorer"
& $makeNsis "/DAPP_VERSION=$Version" "/DFROZEN_DIR=$frozenApplication" "/DOUTPUT_DIR=$outputRoot" "/DAPP_ICON=$sourceIco" (Join-Path $scriptRoot "explorer.nsi")
if ($LASTEXITCODE -ne 0) { throw "The Windows setup executable could not be built." }

$installer = Join-Path $outputRoot "MarkdownLLM-Explorer-Installer-$Version.exe"
if (-not (Test-Path -LiteralPath $installer)) { throw "Installer output was not created." }
Write-Host "Windows installer: $installer"
