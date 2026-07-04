#Requires -Version 5.1
param([Parameter(Mandatory)][string]$CourseName
  ,[string]$TemplateDir = "02_模板"
  ,[string]$OutputDir = "outputs"
  ,[string]$TxtDir = (Join-Path $OutputDir "transcripts")
  ,[string]$OcrJson = (Join-Path $OutputDir "ocr_results.json")
)
$PSDefaultParameterValues["*:Encoding"]="utf8BOM"; chcp 65001|Out-Null
$sn=$CourseName -replace "[\\/:*?"<>|]","_"

# 0. 检查转写完整性
$aTxts=Get-ChildItem (Join-Path $TxtDir "audio") -Filter "*.txt"|?{$_.Name -notlike "*.whisper.log"}
$vTxts=Get-ChildItem (Join-Path $TxtDir "video") -Filter "*.txt"|?{$_.Name -notlike "*.whisper.log"}
Write-Host "音频转写: $($aTxts.Count)  视频转写: $($vTxts.Count)"

# 1. 汇总转写文本
$allText=@()
$aTxts|%{$allText+=@{source="audio";file=$_.Name;text=Get-Content $_.FullName -Raw}}
$vTxts|%{$allText+=@{source="video";file=$_.Name;text=Get-Content $_.FullName -Raw}}

# 2. 汇总 OCR 文本
$ocrTexts=@{}
if(Test-Path $OcrJson){$d=Get-Content $OcrJson -Raw|ConvertFrom-Json;$d.PSObject.Properties|%{$ocrTexts[$_.Name]=$_.Value.ocr_pages.text}}

# 3. 输出汇总 JSON
$summary=@{}
$summary.course=$CourseName
$summary.audio_transcripts=$allText|?{$_.source -eq "audio"}
$summary.video_transcripts=$allText|?{$_.source -eq "video"}
$summary.ocr_texts=$ocrTexts
$summary.summary=$allText|%{$_.text}|Out-String
$summaryPath=Join-Path $OutputDir "course_text_summary_$sn.json"
$summary|ConvertTo-Json -Depth 5|Out-File $summaryPath -Encoding utf8BOM
Write-Host "文本汇总: $summaryPath"

# 4. 输出写入计划模板
$plan=@()
$plan+="# Obsidian 写入计划：$CourseName"
$plan+=""
$plan+="## 待创建目录"
$plan+="- 02_课程库/$CourseName/"
$plan+="- 03_知识卡片/课程知识卡片/"
$plan+="- 04_复习卡片/课程复习卡/"
$plan+="- 80_索引数据库/课程索引/"
$plan+="- 93_导入报告/"
$plan+="- 98_待人工审核确认/$CourseName/"
$plan+=""
$plan+="## 待创建文件"
$plan+="| 文件 | 路径 | 状态 |"
$plan+="|---|---|---|"
$plan+="| 课程总览 | 02_课程库/$CourseName/00_课程总览.md | 待生成 |"
$plan+="| 章节拆解 | 02_课程库/$CourseName/01_章节拆解.md | 待生成 |"
$plan+="| 逐节课总结 | 02_课程库/$CourseName/02_逐节课总结.md | 待生成 |"
$plan+="| 实操工作流 | 02_课程库/$CourseName/03_实操工作流.md | 待生成 |"
$plan+="| 术语索引 | 02_课程库/$CourseName/04_术语索引.md | 待生成 |"
$plan+="| 缺失内容检查 | 02_课程库/$CourseName/05_缺失内容检查.md | 待生成 |"
$plan+="| 下一步学习计划 | 02_课程库/$CourseName/06_下一步学习计划.md | 待生成 |"
$plan+="| 导入报告 | 93_导入报告/导入报告_$sn.md | 待生成 |"
$plan+=""
$plan+="## 待确认事项"
$plan+="- [ ] 人工审核转写准确性"
$plan+="- [ ] 确认术语索引"
$plan+="- [ ] 确认知识卡片数量"
$plan+="- [ ] 确认工作流可执行"
$plan+="- [ ] 确认不覆盖已有文件"
$plan+="- [ ] 确认不修改正式库以外的目录"
$plan+="- [ ] 确认不上传正式库到 GitHub"
$plan+=""
$plan+="## 风险提示"
$plan+="- 共 $($aTxts.Count+$vTxts.Count) 个转写文件"
$plan+="- $(if($ocrTexts.Count -gt 0){$ocrTexts.Count}else{0}) 个 OCR 文本"
$plan+="- 不确定内容已在总结中标记为待人工补充/待人工确认"
$plan+="---"
$plan+="*等待用户确认后方可执行写入*"
$planPath=Join-Path $OutputDir "写入计划_待确认_$sn.md"
$plan -join "`r`n"|Out-File $planPath -Encoding utf8BOM
Write-Host "写入计划: $planPath"
