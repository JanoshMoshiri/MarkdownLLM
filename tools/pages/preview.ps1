<#
Preview the public docs face (docs/) locally, built the way GitHub Pages
builds it — see the Gemfile beside this script. Look before it goes up.

  .\tools\pages\preview.ps1            # serve at http://127.0.0.1:4000/MarkdownLLM/
  .\tools\pages\preview.ps1 -Build     # build once and exit; non-zero on a build error
  .\tools\pages\preview.ps1 -Install   # first run: install the Pages gem set

Needs Ruby 3.3 with the MSYS2 devkit (RubyInstaller; winget id
RubyInstallerTeam.RubyWithDevKit.3.3). The built site goes to a temp folder,
never into docs/ — the repository holds only the site's source.
#>
param(
    [switch]$Build,
    [switch]$Install,
    [int]$Port = 4000
)
$ErrorActionPreference = 'Stop'
$repo = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$ruby = @('C:\Ruby33-x64\bin', "$env:LOCALAPPDATA\Programs\Ruby33-x64\bin") |
    Where-Object { Test-Path (Join-Path $_ 'ruby.exe') } | Select-Object -First 1
if (-not $ruby -and -not (Get-Command ruby -ErrorAction SilentlyContinue)) {
    throw 'Ruby not found. Install it: winget install --id RubyInstallerTeam.RubyWithDevKit.3.3 --exact --scope user'
}
if ($ruby) { $env:PATH = "$ruby;$env:PATH" }
$env:BUNDLE_GEMFILE = Join-Path $PSScriptRoot 'Gemfile'
$env:PAGES_REPO_NWO = 'JanoshMoshiri/MarkdownLLM'   # what jekyll-github-metadata reads on Pages
$site = Join-Path ([IO.Path]::GetTempPath()) 'mdllm-pages-site'

Push-Location $repo
try {
    if ($Install) { bundle install; exit $LASTEXITCODE }
    $common = @('exec', 'jekyll')
    $paths = @('--source', 'docs', '--destination', $site)
    if ($Build) {
        bundle @common build @paths
    } else {
        bundle @common serve @paths --port $Port --host 127.0.0.1 --livereload
    }
    exit $LASTEXITCODE
}
finally { Pop-Location }
