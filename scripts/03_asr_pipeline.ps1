#Requires -Version 5.1
param([Parameter(Mandatory)][string]$SourceDir, [string]$OutputDir = "outputs/transcripts", [string]$ModelSize = "medium", [string]$Language = "zh")
$PSDefaultParameterValues["*:Encoding"] = "utf8BOM"
chcp 65001 | Out-Null

# Python detect
$pythonPath = if (Get-Command python -ErrorAction SilentlyContinue) { "python" }
elseif (Test-Path "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe") { "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" }
else { $null }
if (-not $pythonPath) { Write-Host "错误：找不到 Python"; exit 1 }

# ffmpeg detect
$ffmpegPath = if (Get-Command ffmpeg -ErrorAction SilentlyContinue) { "ffmpeg" }
elseif (Test-Path "$env:SCOOP/apps/ffmpeg/current/bin/ffmpeg.exe") { "$env:SCOOP/apps/ffmpeg/current/bin/ffmpeg.exe" }
else { $null }
if (-not $ffmpegPath) { Write-Host "错误：找不到 ffmpeg"; exit 1 }

# 收集音视频
$audioExts = ".mp3",".m4a",".wav",".flac",".aac",".wma",".ogg"
$videoExts = ".mp4",".avi",".mov",".mkv",".wmv",".flv",".m4v",".webm"
$audioFiles = Get-ChildItem $SourceDir -Recurse -File | Where-Object { $_.Extension.ToLower() -in $audioExts }
$videoFiles = Get-ChildItem $SourceDir -Recurse -File | Where-Object { $_.Extension.ToLower() -in $videoExts }
Write-Host "音频: $($audioFiles.Count)  视频: $($videoFiles.Count)"

# 目录
$aOut = Join-Path $OutputDir "audio"
$vOut = Join-Path $OutputDir "video"
$tOut = Join-Path $OutputDir "temp_audio"
foreach ($d in $aOut,$vOut,$tOut) { New-Item -ItemType Directory -Force -Path $d | Out-Null }

# 转写函数
function Invoke-WhisperTranscribe {
  param($FilePath, $TxtPath, $Lang)
  $logFile = "$TxtPath.whisper.log"
  $outDir = (Split-Path $TxtPath -Parent)
  $cmd = '& ' + $pythonPath + ' -m whisper "' + $FilePath + '" --model ' + $ModelSize + ' --language ' + $Lang + ' --output_dir "' + $outDir + '" --output_format txt'
  Invoke-Expression $cmd 2>&1 | Out-File "$logFile" -Encoding utf8BOM
  return (Test-Path $TxtPath)
}

# 音频
$i = 0
foreach ($af in $audioFiles) {
  $i++
  $rel = $af.FullName.Substring($SourceDir.Length).TrimStart("\","/")
  $outName = [IO.Path]::GetFileNameWithoutExtension($af.Name) + ".txt"
  $outPath = Join-Path $aOut $outName
  if (Test-Path $outPath) { Write-Host "[$i/$($audioFiles.Count)][SKIP] $rel"; continue }
  Write-Host "[$i/$($audioFiles.Count)][Audio] $rel"
  if (-not (Invoke-WhisperTranscribe $af.FullName $outPath $Language)) { Write-Host "  失败: $rel" }
}

# 视频
$j = 0
foreach ($vf in $videoFiles) {
  $j++
  $rel = $vf.FullName.Substring($SourceDir.Length).TrimStart("\","/")
  $outName = [IO.Path]::GetFileNameWithoutExtension($vf.Name) + ".txt"
  $outPath = Join-Path $vOut $outName
  if (Test-Path $outPath) { Write-Host "[$j/$($videoFiles.Count)][SKIP] $rel"; continue }
  Write-Host "[$j/$($videoFiles.Count)][Video] $rel"
  $tempMp3 = Join-Path $tOut "$([IO.Path]::GetFileNameWithoutExtension($vf.Name)).mp3"
  & $ffmpegPath -y -i $vf.FullName -vn -acodec libmp3lame -q:a 2 $tempMp3 2>&1 | Out-Null
  if (-not (Test-Path $tempMp3)) { Write-Host "  抽音频失败: $rel"; continue }
  $ok = Invoke-WhisperTranscribe $tempMp3 $outPath $Language
  Remove-Item $tempMp3 -Force -ErrorAction SilentlyContinue
  if (-not $ok) { Write-Host "  转写失败: $rel" }
}

Write-Host "=== 转写完成 ==="
