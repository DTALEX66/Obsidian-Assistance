#Requires -Version 5.1
param([Parameter(Mandatory)][string]$VaultPath
  ,[Parameter(Mandatory)][string]$CourseName
  ,[string]$SourceDir = "outputs"
  ,[switch]$DryRun
  ,[switch]$Force
)
$PSDefaultParameterValues["*:Encoding"]="utf8BOM"; chcp 65001|Out-Null

if(-not(Test-Path $VaultPath)){Write-Host"错误：Obsidian 库不存在";exit 1}
if(-not$Force){Write-Host"请先确认写入计划。使用 -Force 跳过。"}
if(-not$Force-and -not$DryRun){exit 0}

$sn=$CourseName -replace "[\\/:*?"<>|]","_"

# 创建目录
$base = @(
  "02_课程库/$CourseName"
  ,"03_知识卡片/课程知识卡片"
  ,"04_复习卡片/课程复习卡"
  ,"80_索引数据库/课程索引"
  ,"93_导入报告"
  ,"98_待人工审核确认/$CourseName"
)

$created = @()
foreach($b in $base){
  $p = Join-Path $VaultPath $b
  if(-not(Test-Path $p)){New-Item -ItemType Directory -Force -Path $p|Out-Null;$created+=$p}
}
if($created.Count -gt 0){Write-Host "新创建目录:";$created|%{Write-Host "  $_"}}

# 读取源文件并写入
$files = @(
  @{src="00_课程总览.md";    dst="02_课程库/$CourseName/00_课程总览.md"}
  ,@{src="01_章节拆解.md";   dst="02_课程库/$CourseName/01_章节拆解.md"}
  ,@{src="02_逐节课总结.md"; dst="02_课程库/$CourseName/02_逐节课总结.md"}
  ,@{src="03_实操工作流.md"; dst="02_课程库/$CourseName/03_实操工作流.md"}
  ,@{src="04_术语索引.md";   dst="02_课程库/$CourseName/04_术语索引.md"}
  ,@{src="05_缺失内容检查.md";dst="02_课程库/$CourseName/05_缺失内容检查.md"}
  ,@{src="06_下一步学习计划.md";dst="02_课程库/$CourseName/06_下一步学习计划.md"}
)

$written=@();$skipped=@()
foreach($f in $files){
  $srcPath = Join-Path $SourceDir $f.src
  $dstPath = Join-Path $VaultPath $f.dst
  if(-not(Test-Path $srcPath)){Write-Host "  源文件不存在: $($f.src)";continue}
  if((Test-Path $dstPath)-and -not$Force){$skipped+=$f.dst;Write-Host "  [SKIP] 已存在: $($f.dst)";continue}
  Copy-Item $srcPath $dstPath -Force
  $written+=$f.dst
}
if($written.Count -gt 0){Write-Host "写入文件:";$written|%{Write-Host "  $_"}}
if($skipped.Count -gt 0){Write-Host "跳过(已存在,使用 -Force 覆盖):";$skipped|%{Write-Host "  $_"}}

# 导入报告
$reportPath = Join-Path $VaultPath "93_导入报告/导入报告_$sn.md"
$report = @()
$report+="# 导入报告：$CourseName"
$report+="- 导入时间：$(Get-Date -Format yyyy-MM-dd HH:mm:ss)"
$report+="- 写入文件：$($written.Count)"
$report+="- 跳过文件：$($skipped.Count)"
$report+="- 是否覆盖：$($Force.ToString())"
$report -join "`r`n"|Out-File $reportPath -Encoding utf8BOM
Write-Host "导入报告: $reportPath"
