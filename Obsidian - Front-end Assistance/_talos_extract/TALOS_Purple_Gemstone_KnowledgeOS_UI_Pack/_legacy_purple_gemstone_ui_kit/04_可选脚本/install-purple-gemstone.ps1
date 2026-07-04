param(
  [Parameter(Mandatory=$true)]
  [string]$VaultPath
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $VaultPath)) {
  throw "Vault path not found: $VaultPath"
}

$snippetDir = Join-Path $VaultPath ".obsidian\snippets"
New-Item -ItemType Directory -Force -Path $snippetDir | Out-Null

$sourceRoot = Split-Path -Parent $PSScriptRoot
$snippetSource = Join-Path $sourceRoot ".obsidian\snippets\purple-gemstone-console.css"
$snippetTarget = Join-Path $snippetDir "purple-gemstone-console.css"

if (Test-Path $snippetTarget) {
  Copy-Item $snippetTarget "$snippetTarget.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
}

Copy-Item $snippetSource $snippetTarget -Force
Copy-Item (Join-Path $sourceRoot "00_操作台") $VaultPath -Recurse -Force
Copy-Item (Join-Path $sourceRoot "01_模板") $VaultPath -Recurse -Force
Copy-Item (Join-Path $sourceRoot "02_Canvas") $VaultPath -Recurse -Force
Copy-Item (Join-Path $sourceRoot "assets") $VaultPath -Recurse -Force

Write-Host "Purple Gemstone Console copied successfully."
Write-Host "Next: Obsidian -> Settings -> Appearance -> CSS snippets -> Reload -> Enable purple-gemstone-console.css"
