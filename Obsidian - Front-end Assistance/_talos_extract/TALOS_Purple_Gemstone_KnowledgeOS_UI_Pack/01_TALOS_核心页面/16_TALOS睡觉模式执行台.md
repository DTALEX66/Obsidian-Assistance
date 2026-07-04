---
title: TALOS 睡觉模式执行台
type: talos-sleep-mode-console
status: active
tags: [talos, sleep-mode, execution-log]
cssclasses: [talos-purple-gemstone, talos-sleep-page]
---

# TALOS 睡觉模式执行台

> [!talos-sleep] Sleep Mode Console
> 目标：让自动循环可见、可控、可信。即使不做真实按钮，也要显示暂停/继续/停止状态、当前轮次、队列、边界与 resume point。

## 当前轮次

| 项目 | 当前值 |
|---|---|
| 当前模式 | Sleep Mode / 自动循环 |
| 当前轮次 | Round 01 |
| 当前队列 | 证据核验 → 页面生成 → CSS QA → 执行日志 |
| 最近提交 | 待填写 |
| Resume Point | `继续从 02_TALOS证据矩阵 的 pending 队列开始` |

> [!talos-danger] 安全边界
> 不上传、不删源、不伪造、不移动课程。任何危险动作必须二次确认，并写入执行日志。

## 执行日志

```dataview
TABLE round, action, result, blocker, updated
FROM ""
WHERE type = "talos-execution-log"
SORT updated DESC
LIMIT 20
```

## 自动复盘汇总

| 指标 | 值 | 说明 |
|---|---:|---|
| 完成率 | 0% | 后续由执行日志统计 |
| 失败原因 | 待记录 | 权限、路径、Dataview、CSS冲突 |
| 下一轮建议 | 待生成 | 从 blocker 反推 |
