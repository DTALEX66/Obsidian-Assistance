#Requires -Version 5.1
param([Parameter(Mandatory)] [string]$SourceDir, [string]$OutputDir = (Join-Path (Get-Location) "outputs"), [string]$CourseName = "")
$PSDefaultParameterValues["*:Encoding"] = "utf8BOM"
chcp 65001 > $null
Write-Host "=== 课程素材扫描器 v1.0 ==="
if (-not (Test-Path $SourceDir)) { Write-Host "错误：源目录不存在"; exit 1 }
if ([string]::IsNullOrEmpty($CourseName)) { $CourseName = Split-Path $SourceDir -Leaf }

$typeMap = @{}
@(".mp4",".avi",".mov",".mkv",".wmv",".flv",".m4v",".webm",".ts")     | %{ $typeMap[$_] = "video" }
@(".mp3",".m4a",".wav",".flac",".aac",".wma",".ogg")                | %{ $typeMap[$_] = "audio" }
@(".pdf")                                                           | %{ $typeMap[$_] = "pdf" }
@(".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg")               | %{ $typeMap[$_] = "image" }
@(".ppt",".pptx",".doc",".docx",".xls",".xlsx")                     | %{ $typeMap[$_] = "document" }
@(".srt",".vtt",".ass",".ssa",".lrc")                               | %{ $typeMap[$_] = "subtitle" }
@(".zip",".rar",".7z",".tar",".gz")                                 | %{ $typeMap[$_] = "archive" }
@(".md")                                                            | %{ $typeMap[$_] = "markdown" }
@(".txt",".html",".htm",".json",".xml",".csv")                      | %{ $typeMap[$_] = "text" }

Write-Host "扫描中 ..."
$allFiles = Get-ChildItem -Path $SourceDir -Recurse -File
Write-Host "  共 $($allFiles.Count) 个文件"

$cats = @{video=0;audio=0;pdf=0;image=0;document=0;subtitle=0;archive=0;markdown=0;text=0;unknown=0;zero=0;risk=0}
$result = @(); $zeroList = @(); $unknownExts = @{}

foreach ($f in $allFiles) {
  $ext = $f.Extension.ToLower()
  $relPath = $f.FullName.Substring($SourceDir.Length).TrimStart("\","/")
  $cat = if ($typeMap.ContainsKey($ext)) { $typeMap[$ext] } else { "unknown" }
  $flags = @()
  if ($f.Length -eq 0) { $flags += "ZERO_BYTES"; $cats.zero++; $zeroList += $relPath }
  if ($ext -in ".locked",".encrypted",".crypt") { $flags += "SUSPECT_ENCRYPTED"; $cats.risk++ }
  if ($f.Length -gt 0 -and $f.Length -lt 1024 -and ($cat -in "pdf","video","audio")) { $flags += "SUSPECT_CORRUPT"; $cats.risk++ }
  if ($cat -eq "unknown") { $unknownExts[$ext]++ }
  $cats[$cat]++
  $result += [PSCustomObject]@{RelativePath=$relPath;Extension=$ext;Category=$cat;SizeMB=[math]::Round($f.Length/1MB,2);RiskFlags=($flags-join";");LastModified=$f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")}
}

Write-Host "扫描完成"
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null }
$safeName = $CourseName -replace "[\\/:*?""<>|]", "_"
$result | Export-Csv -Path (Join-Path $OutputDir "scan_${safeName}.csv") -NoTypeInformation -Encoding utf8BOM
$result | ConvertTo-Json -Depth 3 | Out-File -FilePath (Join-Path $OutputDir "scan_${safeName}.json") -Encoding utf8BOM

$mdLines = @()
$mdLines += "# 素材识别报告：$CourseName"
$mdLines += ""
$mdLines += "- 扫描时间：$(Get-Date -Format yyyy-MM-dd HH:mm:ss)"
$mdLines += "- 源目录：$SourceDir"
$mdLines += "- 文件总数：$($allFiles.Count)"
$mdLines += ""
$mdLines += "## 文件数量汇总"
$mdLines += ""
$mdLines += "| 类别 | 数量 |"
$mdLines += "|---|---|"
foreach($k in $cats.Keys|Sort){$mdLines+="| $k | $($cats[$k]) |"}
if ($zeroList.Count -gt 0) { $mdLines += ""; $mdLines += "## 零字节文件"; $zeroList | %{ $mdLines += "- $_" } }
if ($unknownExts.Keys.Count -gt 0) { $mdLines += ""; $mdLines += "## 未知扩展名"; $unknownExts.Keys|Sort|%{ $mdLines += "- $_ : $($unknownExts[$_])" } }
$mdLines += ""; $mdLines += "---"; $mdLines += "*由 course-scan v1.0 自动生成*"
$mdLines -join "`r`n" | Out-File -FilePath (Join-Path $OutputDir "01_素材识别报告_${safeName}.md") -Encoding utf8BOM
Write-Host "完成。输出目录: $OutputDir"
