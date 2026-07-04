param(
  [Parameter(Mandatory=$true)][string]$TargetPath,
  [Parameter(Mandatory=$true)][string]$BackupRoot
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $TargetPath)) {
  Write-Output "Target does not exist, no backup needed: $TargetPath"
  exit 0
}
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$destDir = Join-Path $BackupRoot "backup_$timestamp"
New-Item -ItemType Directory -Force -Path $destDir | Out-Null
$leaf = Split-Path -Leaf $TargetPath
$dest = Join-Path $destDir $leaf
Copy-Item -LiteralPath $TargetPath -Destination $dest -Force
Write-Output "Backed up to: $dest"
