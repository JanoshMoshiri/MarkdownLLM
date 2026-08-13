<#+
.SYNOPSIS
Resolve one floor-capable Python invocation within a total deadline.

.DESCRIPTION
Shared Windows encoding of MarkdownLLM's neutral runtime-candidate policy.
Returns a PSCustomObject with Executable and PrefixArguments, or $null. Failed
native probes—including Windows PowerShell 5.1 RemoteException behavior—are
negative candidate facts. The one stopwatch bounds the complete search.
#>

function ConvertTo-MdllmNativeArgument {
    param([Parameter(Mandatory = $true)][string]$Value)
    return '"' + $Value.Replace('\', '\\').Replace('"', '\"') + '"'
}

function Test-MdllmFloorCandidate {
    param(
        [Parameter(Mandatory = $true)]$Candidate,
        [Parameter(Mandatory = $true)][System.Diagnostics.Stopwatch]$Stopwatch,
        [Parameter(Mandatory = $true)][int]$TimeoutMilliseconds
    )
    $remaining = $TimeoutMilliseconds - [int]$Stopwatch.ElapsedMilliseconds
    if ($remaining -le 0) { return $false }

    try {
        $probeArgs = @($Candidate.PrefixArguments) + @('-c', 'import yaml')
        $info = New-Object System.Diagnostics.ProcessStartInfo
        $extension = [IO.Path]::GetExtension($Candidate.Executable)
        if ($extension -in @('.cmd', '.bat')) {
            $info.FileName = $env:COMSPEC
            $inner = (ConvertTo-MdllmNativeArgument $Candidate.Executable) +
                ' ' + (($probeArgs | ForEach-Object {
                    ConvertTo-MdllmNativeArgument ([string]$_)
                }) -join ' ')
            $info.Arguments = '/d /s /c "' + $inner + '"'
        }
        else {
            $info.FileName = $Candidate.Executable
            $info.Arguments = (($probeArgs | ForEach-Object {
                ConvertTo-MdllmNativeArgument ([string]$_)
            }) -join ' ')
        }
        $info.UseShellExecute = $false
        $info.CreateNoWindow = $true
        $info.RedirectStandardOutput = $true
        $info.RedirectStandardError = $true
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $info
        if (-not $process.Start()) { return $false }
        if (-not $process.WaitForExit($remaining)) {
            try { $process.Kill() } catch { }
            return $false
        }
        return $process.ExitCode -eq 0
    }
    catch {
        return $false
    }
    finally {
        if ($process) { $process.Dispose() }
    }
}

function Resolve-MdllmPython {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$FrameworkRoot,
        [int]$TimeoutSeconds = 10
    )
    if ($TimeoutSeconds -le 0) { return $null }
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    $candidates = @(
        @{ Executable = (Join-Path $Root '.venv\Scripts\python.exe'); PrefixArguments = @() },
        @{ Executable = (Join-Path $FrameworkRoot '.venv\Scripts\python.exe'); PrefixArguments = @() },
        @{ Executable = 'python3'; PrefixArguments = @() },
        @{ Executable = 'python'; PrefixArguments = @() },
        @{ Executable = 'py'; PrefixArguments = @('-3') }
    )
    foreach ($candidate in $candidates) {
        if ($watch.Elapsed.TotalSeconds -ge $TimeoutSeconds) { break }
        $resolved = $null
        if (Test-Path -LiteralPath $candidate.Executable) {
            $resolved = $candidate.Executable
        }
        else {
            $found = Get-Command $candidate.Executable -ErrorAction SilentlyContinue
            if ($found) { $resolved = $found.Source }
        }
        if (-not $resolved) { continue }
        $invocation = [PSCustomObject]@{
            Executable = [string]$resolved
            PrefixArguments = @($candidate.PrefixArguments)
        }
        if (Test-MdllmFloorCandidate -Candidate $invocation `
                -Stopwatch $watch -TimeoutMilliseconds ($TimeoutSeconds * 1000)) {
            return $invocation
        }
    }
    return $null
}
