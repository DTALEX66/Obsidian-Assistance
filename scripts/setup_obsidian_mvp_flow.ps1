param(
    [Parameter(Mandatory = $true)]
    [string]$VaultPath,

    [string]$InboxFolder = "01_收集箱",
    [string]$AttachmentFolder = "99_附件"
)

$ErrorActionPreference = "Stop"

function Ensure-Dir($path) {
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

function Write-Utf8($path, $content) {
    Ensure-Dir (Split-Path -Parent $path)
    Set-Content -LiteralPath $path -Value $content -Encoding UTF8
}

if (-not (Test-Path -LiteralPath $VaultPath)) {
    throw "Vault path does not exist: $VaultPath"
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $VaultPath "93_导入报告\Obsidian全流程MVP_备份_$stamp"
Ensure-Dir $backupDir

$targets = @(
    ".obsidian\appearance.json",
    ".obsidian\app.json",
    ".obsidian\bookmarks.json",
    ".obsidian\snippets\dt-knowledgeos.css",
    "00_主页\00_知识库总控台.md",
    "$InboxFolder\00_输入箱.md"
)

foreach ($relative in $targets) {
    $src = Join-Path $VaultPath $relative
    if (Test-Path -LiteralPath $src) {
        $dest = Join-Path $backupDir $relative
        Ensure-Dir (Split-Path -Parent $dest)
        Copy-Item -LiteralPath $src -Destination $dest -Force
    }
}

$css = @'
/* Obsidian Assistance MVP UI */
:root {
  --oa-accent: #0071e3;
  --oa-card-radius: 10px;
}

.markdown-preview-view.dashboard h1 {
  letter-spacing: 0;
}

.dashboard .callout {
  border-radius: var(--oa-card-radius);
}

.dashboard .callout[data-callout="hub"] {
  --callout-color: 0, 113, 227;
  --callout-icon: lucide-layout-dashboard;
}

.dashboard table {
  width: 100%;
}
'@

Write-Utf8 (Join-Path $VaultPath ".obsidian\snippets\dt-knowledgeos.css") $css

$appearancePath = Join-Path $VaultPath ".obsidian\appearance.json"
$snippets = @("dt-knowledgeos")
$appearance = [ordered]@{
    accentColor = "#0071e3"
    cssTheme = ""
    enabledCssSnippets = $snippets
}
($appearance | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $appearancePath -Encoding UTF8

$appPath = Join-Path $VaultPath ".obsidian\app.json"
$app = [ordered]@{
    newFileLocation = "folder"
    newFileFolderPath = $InboxFolder
    attachmentFolderPath = $AttachmentFolder
    alwaysUpdateLinks = $true
    showUnsupportedFiles = $true
    userIgnoreFilters = @(".git/", "node_modules/", "venv/", "__MACOSX/")
}
($app | ConvertTo-Json -Depth 20) | Set-Content -LiteralPath $appPath -Encoding UTF8

$home = @'
---
type: dashboard
status: active
cssclasses:
  - dashboard
tags:
  - obsidian
  - knowledgeos
---

# 知识库总控台

> [!hub] 今天从这里开始
> - [[01_收集箱/00_输入箱|输入箱]]
> - [[02_课程库/00_课程库总览|课程库]]
> - [[03_知识卡片/00_知识卡片总览|知识卡片]]
> - [[04_复习卡片/00_复习中心|复习中心]]
> - [[98_待人工审核确认/00_待审核总览|待审核]]
> - [[93_导入报告/00_导入报告总览|导入报告]]

## 当前流程

```mermaid
flowchart LR
  A["输入箱"] --> B["素材识别"]
  B --> C["课程拆解"]
  C --> D["逐节总结"]
  D --> E["知识卡片"]
  E --> F["复习卡片"]
  D --> G["待审核"]
  G --> H["正式入库"]
```

## 最近课程

```dataview
TABLE file.mtime AS 修改时间, status AS 状态, category AS 分类
FROM "02_课程库"
SORT file.mtime DESC
LIMIT 8
```
'@

Write-Utf8 (Join-Path $VaultPath "00_主页\00_知识库总控台.md") $home

$inbox = @'
---
type: inbox
status: active
cssclasses:
  - dashboard
tags:
  - 输入箱
---

# 输入箱

所有新资料先放这里，不直接塞进正式库。

## 待整理

- [ ] 识别素材类型。
- [ ] 判断是否需要 OCR / ASR / 文档转换。
- [ ] 生成课程处理计划。
'@

Write-Utf8 (Join-Path $VaultPath "$InboxFolder\00_输入箱.md") $inbox

$bookmarksPath = Join-Path $VaultPath ".obsidian\bookmarks.json"
$now = [DateTimeOffset]::Now.ToUnixTimeMilliseconds()
$bookmarks = @{
    items = @(
        @{ type = "file"; ctime = $now; path = "00_主页/00_知识库总控台.md"; title = "知识库总控台" },
        @{ type = "file"; ctime = $now; path = "$InboxFolder/00_输入箱.md"; title = "输入箱" }
    )
}
($bookmarks | ConvertTo-Json -Depth 10) | Set-Content -LiteralPath $bookmarksPath -Encoding UTF8

Write-Host "Obsidian MVP flow installed."
Write-Host "Backup: $backupDir"

