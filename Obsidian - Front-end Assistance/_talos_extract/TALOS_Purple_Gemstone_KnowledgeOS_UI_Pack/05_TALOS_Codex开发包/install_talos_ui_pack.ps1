param(
  [Parameter(Mandatory=$true)]
  [string]$VaultPath
)

$ErrorActionPreference = "Stop"
$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$packRoot = Resolve-Path (Join-Path $source "..")

Write-Host "TALOS Purple Gemstone UI Pack installer"
Write-Host "Vault: $VaultPath"

if (!(Test-Path $VaultPath)) { throw "Vault path not found: $VaultPath" }

$snippetDir = Join-Path $VaultPath ".obsidian\snippets"
New-Item -ItemType Directory -Force -Path $snippetDir | Out-Null
Copy-Item -Force (Join-Path $packRoot ".obsidian\snippets\talos-purple-gemstone-knowledgeos.css") $snippetDir

foreach ($dir in @("00_TALOS_入口","01_TALOS_核心页面","02_TALOS_模板","03_TALOS_Canvas","04_TALOS_设计规范","05_TALOS_Codex开发包","06_TALOS_Figma交付包","08_TALOS_资产")) {
  Copy-Item -Recurse -Force (Join-Path $packRoot $dir) (Join-Path $VaultPath $dir)
}

Write-Host "Done. Open Obsidian → Settings → Appearance → CSS snippets → Reload → Enable talos-purple-gemstone-knowledgeos.css"
