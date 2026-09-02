[CmdletBinding()]
param(
    [string]$Version = "",
    [string]$VerificationIdentity = "",
    [string]$SignToolPath = "",
    [string]$SignCertificateThumbprint = "",
    [string]$TimestampUrl = ""
)

$ErrorActionPreference = "Stop"
if ($VerificationIdentity -and $VerificationIdentity -notmatch '^[A-Za-z0-9-]+$') {
    throw "VerificationIdentity may contain only ASCII letters, digits, and hyphens."
}
$signingValues = @($SignToolPath, $SignCertificateThumbprint, $TimestampUrl) | Where-Object { $_ }
if ($signingValues.Count -ne 0 -and $signingValues.Count -ne 3) {
    throw "Signing requires SignToolPath, SignCertificateThumbprint, and TimestampUrl together."
}
$signingEnabled = $signingValues.Count -eq 3
if ($signingEnabled) {
    $SignToolPath = (Resolve-Path -LiteralPath $SignToolPath -ErrorAction Stop).Path
    if ($SignCertificateThumbprint -notmatch '^[A-Fa-f0-9]{40}$') {
        throw "SignCertificateThumbprint must be one 40-character SHA-1 certificate thumbprint."
    }
    if ($TimestampUrl -notmatch '^https://') {
        throw "TimestampUrl must use HTTPS."
    }
}
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$explorerRoot = (Resolve-Path (Join-Path $scriptRoot "..\..")).Path
$buildRoot = Join-Path $explorerRoot "build\windows"
$outputRoot = Join-Path $explorerRoot "dist"
$buildEnvironment = Join-Path $explorerRoot ".windows-build-venv"
$buildTools = Join-Path $explorerRoot ".windows-build-tools"
$pyprojectPath = Join-Path $explorerRoot "pyproject.toml"
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
$projectVersion = (& $buildPython -c "import pathlib, sys, tomllib; print(tomllib.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))['project']['version'])" $pyprojectPath).Trim()
if ($LASTEXITCODE -ne 0 -or -not $projectVersion) {
    throw "The Explorer version could not be read from pyproject.toml."
}
if (-not $Version) {
    $Version = $projectVersion
}
elseif ($Version -ne $projectVersion) {
    throw "Requested installer version '$Version' does not match the Explorer source version '$projectVersion'."
}
$buildTarget = $explorerRoot + "[windows-build]"
& $buildPython -m pip install --disable-pip-version-check $buildTarget
if ($LASTEXITCODE -ne 0) { throw "The isolated Windows build dependencies could not be installed." }

& $buildPython (Join-Path $scriptRoot "generate_icons.py") --png $sourcePng --ico $sourceIco
if ($LASTEXITCODE -ne 0) { throw "Application icon generation failed." }

$pyInstallerDist = Join-Path $buildRoot "frozen"
$pyInstallerWork = Join-Path $buildRoot "pyinstaller"
& $buildPython -m PyInstaller --noconfirm --clean --distpath $pyInstallerDist --workpath $pyInstallerWork (Join-Path $scriptRoot "markdownllm-explorer.spec")
if ($LASTEXITCODE -ne 0) { throw "The native application bundle could not be built." }
$frozenApplication = Join-Path $pyInstallerDist "MarkdownLLM Explorer"
$frozenExecutable = Join-Path $frozenApplication "MarkdownLLM Explorer.exe"
if ($signingEnabled) {
    & $SignToolPath sign /sha1 $SignCertificateThumbprint /fd SHA256 /tr $TimestampUrl /td SHA256 $frozenExecutable
    if ($LASTEXITCODE -ne 0) { throw "The frozen Windows application could not be signed." }
}

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
    $nsisDownload = Join-Path $buildTools "nsis-3.12.zip.part"
    $nsisRoot = Join-Path $buildTools "nsis-3.12"
    $expectedNsisHash = "56581F90DB321581C5381193D796FFFCF2D24B2F8FED2160A6C6A3BAA67F2C4F"
    $nsisUri = "https://sourceforge.net/projects/nsis/files/NSIS%203/3.12/nsis-3.12.zip/download"
    if (Test-Path -LiteralPath $nsisArchive) {
        $cachedNsisHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $nsisArchive).Hash
        if ($cachedNsisHash -ne $expectedNsisHash) {
            Remove-Item -LiteralPath $nsisArchive -Force
        }
    }
    if (-not (Test-Path -LiteralPath $nsisArchive)) {
        Remove-Item -LiteralPath $nsisDownload -Force -ErrorAction SilentlyContinue
        $curl = (Get-Command curl.exe -ErrorAction SilentlyContinue).Source
        if ($curl) {
            & $curl --fail --location --retry 3 --connect-timeout 15 --output $nsisDownload $nsisUri
            if ($LASTEXITCODE -ne 0) { throw "The pinned NSIS archive could not be downloaded." }
        }
        else {
            Invoke-WebRequest -UseBasicParsing -Uri $nsisUri -OutFile $nsisDownload
        }
        $downloadedNsisHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $nsisDownload).Hash
        if ($downloadedNsisHash -ne $expectedNsisHash) {
            Remove-Item -LiteralPath $nsisDownload -Force
            throw "The downloaded NSIS archive did not match its pinned SHA-256 digest."
        }
        Move-Item -LiteralPath $nsisDownload -Destination $nsisArchive
    }
    $observedNsisHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $nsisArchive).Hash
    if ($observedNsisHash -ne $expectedNsisHash) { throw "The downloaded NSIS archive did not match its pinned SHA-256 digest." }
    if (-not (Test-Path -LiteralPath (Join-Path $nsisRoot "makensis.exe"))) {
        Expand-Archive -LiteralPath $nsisArchive -DestinationPath $buildTools -Force
    }
    $makeNsis = Join-Path $nsisRoot "makensis.exe"
}
if (-not $makeNsis) { throw "makensis.exe was not found after NSIS installation." }

$nsisSigningArguments = @()
if ($signingEnabled) {
    $nsisSigningArguments = @(
        "/DSIGNTOOL_PATH=$SignToolPath",
        "/DSIGN_CERTIFICATE_THUMBPRINT=$SignCertificateThumbprint",
        "/DSIGN_TIMESTAMP_URL=$TimestampUrl"
    )
}
$releaseArguments = @(
    "/DAPP_VERSION=$Version",
    "/DFROZEN_DIR=$frozenApplication",
    "/DOUTPUT_DIR=$outputRoot",
    "/DAPP_ICON=$sourceIco"
) + $nsisSigningArguments + @((Join-Path $scriptRoot "explorer.nsi"))
& $makeNsis @releaseArguments
if ($LASTEXITCODE -ne 0) { throw "The Windows setup executable could not be built." }

$installer = Join-Path $outputRoot "MarkdownLLM-Explorer-Installer-$Version.exe"
if (-not (Test-Path -LiteralPath $installer)) { throw "Installer output was not created." }
Write-Host "Windows installer: $installer"

if ($VerificationIdentity) {
    $verificationName = "MarkdownLLM Explorer Verification $VerificationIdentity"
    $verificationOutputName = "MarkdownLLM-Explorer-Verification-$VerificationIdentity-$Version.exe"
    $verificationRegistry = "Software\MarkdownLLM Explorer Verification\$VerificationIdentity"
    $verificationUninstallRegistry = "Software\Microsoft\Windows\CurrentVersion\Uninstall\MarkdownLLM Explorer Verification $VerificationIdentity"
    $verificationArguments = @(
        "/DAPP_VERSION=$Version",
        "/DFROZEN_DIR=$frozenApplication",
        "/DOUTPUT_DIR=$outputRoot",
        "/DAPP_ICON=$sourceIco",
        "/DAPP_NAME=$verificationName",
        "/DAPP_REGISTRY=$verificationRegistry",
        "/DUNINSTALL_REGISTRY=$verificationUninstallRegistry",
        "/DOUTPUT_NAME=$verificationOutputName"
    ) + $nsisSigningArguments + @((Join-Path $scriptRoot "explorer.nsi"))
    & $makeNsis @verificationArguments
    if ($LASTEXITCODE -ne 0) { throw "The isolated Windows verification setup executable could not be built." }
    $verificationInstaller = Join-Path $outputRoot $verificationOutputName
    if (-not (Test-Path -LiteralPath $verificationInstaller)) { throw "Isolated verification installer output was not created." }
    Write-Host "Windows verification installer: $verificationInstaller"
}
