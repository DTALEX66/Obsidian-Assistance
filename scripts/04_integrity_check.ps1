#Requires -Version 5.1
param([Parameter(Mandatory)][string]$SourceDir,[string]$OcrJson="",[string]$TranscriptDir="",[string]$OutputDir="outputs")
$PSDefaultParameterValues["*:Encoding"]="utf8BOM"; chcp 65001|Out-Null
if(-not(Test-Path $SourceDir)){Write-Host"错误：源目录不存在";exit 1}
$cn=Split-Path $SourceDir -Leaf; $sn=$cn -replace "[\\/:*?"<>|]","_"

# 1. 原始素材分类
$m=@{}
$t=@(".mp4",".avi",".mov",".mkv",".wmv",".flv");$t|%{$m[$_]="video"}
$t=@(".mp3",".m4a",".wav",".flac",".aac",".wma",".ogg");$t|%{$m[$_]="audio"}
$t=@(".pdf");$t|%{$m[$_]="pdf"}
$t=@(".jpg",".jpeg",".png",".gif",".bmp");$t|%{$m[$_]="image"}
$t=@(".ppt",".pptx",".doc",".docx",".xls",".xlsx");$t|%{$m[$_]="document"}
$t=@(".srt",".vtt",".ass");$t|%{$m[$_]="subtitle"}

$g=@{}
Get-ChildItem $SourceDir -Recurse -File|%{$c=if($m.ContainsKey($_.Extension.ToLower())){$m[$_.Extension.ToLower()]}else{"other"};if(-not$g.ContainsKey($c)){$g[$c]=@()};$g[$c]+=$_.FullName}
Write-Host "原始素材:";$g.Keys|Sort|%{Write-Host"  $_ : $($g[$_].Count)"}

# 2. OCR 状态
$ocr=@{}
if(Test-Path $OcrJson){$d=Get-Content $OcrJson -Raw|ConvertFrom-Json;$d.PSObject.Properties|%{$ocr[$_.Name]=$_.Value.status}}
Write-Host "OCR: $($ocr.Count) 条"

# 3. 转写状态
$tr=@()
if(Test-Path $TranscriptDir){$tr=Get-ChildItem $TranscriptDir -Recurse -File -Filter "*.txt"|?{$_.Name -notlike "*.whisper.log"}}
Write-Host "转写: $($tr.Count) 个 .txt"

# 4. 数量
$rawV=$g["video"].Count; $rawA=$g["audio"].Count; $rawP=$g["pdf"].Count
$doneV=($tr|?{$_.Directory.Name -eq "video"}|Measure).Count
$doneA=($tr|?{$_.Directory.Name -eq "audio"}|Measure).Count
$doneP=($ocr.Values|?{$_ -eq "OK"}|Measure).Count
$totalTarget=$rawV+$rawA+$rawP; $totalDone=$doneV+$doneA+$doneP

# 5. 报告
$md=@()
$md+="# 完整性检查报告：$cn"
$md+="- 检查时间：$(Get-Date -Format yyyy-MM-dd HH:mm:ss)"
$md+="- 源目录：$SourceDir"
$md+=""
$md+="## 原始素材";$md+="";$md+="|类别|数量|";$md+="|---|---|"
$g.Keys|Sort|%{$md+="|$_|$($g[$_].Count)|"}
$md+="|**合计**|$(($g.Values|%{$_.Count}|Measure -Sum).Sum)|"
$md+=""
$md+="## 转写/OCR 状态";$md+="";$md+="|类别|已完成|待处理|";$md+="|---|---|---|"
$md+="|视频|$doneV|$($rawV-$doneV)|"
$md+="|音频|$doneA|$($rawA-$doneA)|"
$md+="|PDF|$doneP|$($rawP-$doneP)|"
$md+=""
$md+="## 结论";$md+=""
if($totalTarget-eq0){$md+="源目录中没有可处理素材。"}
elseif($totalDone-ge$totalTarget){$md+="所有素材已处理完毕，可进入总结阶段。"}
else{$md+="尚有 $($totalTarget-$totalDone) 个素材未处理，暂不建议开始总结。"}
$md+="";$md+="---";$md+="*由 integrity-check v1.0 自动生成*"
$md -join "`r`n"|Out-File (Join-Path $OutputDir "完整性检查报告_$sn.md") -Encoding utf8BOM
Write-Host "报告: $(Join-Path $OutputDir "完整性检查报告_$sn.md")"
Write-Host "源: $totalTarget 目标 -> 已完成: $totalDone"
