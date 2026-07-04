# V4 Demo Vault Smoke Test

生成时间：2026-07-01 20:41

## 1. 目标

在不触碰正式 Obsidian vault 的前提下，验证 V4 生成器能向独立测试 vault 写入完整课程包，并验证覆盖前备份机制。

## 2. 测试范围

测试 vault：`D:/OBS-V4-DEMO`

命令：

```bash
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --vault "D:/OBS-V4-DEMO" --apply --report-dir reports
```

## 3. 首次 apply 结果

生成文件完整，包含：

- `00_课程主页.md`
- `01_课程地图.canvas`
- `02_逐节总结/第01节_示例章节.md`
- `03_知识卡片/概念_输入箱.md`
- `03_知识卡片/方法_课程处理流程.md`
- `03_知识卡片/案例_示例案例.md`
- `04_复习卡片/Q_什么是输入箱.md`
- `05_视觉图解/课程流程图.md`
- `05_视觉图解/课程思维导图.md`
- `05_视觉图解/课程时间线.md`
- `06_项目行动/行动清单.md`
- `07_证据索引/evidence-index.md`
- `08_导入报告.md`

验证结果：

```text
missing: []
canvas: ok
bad_yaml: []
bad_mermaid: []
mojibake: []
```

## 4. 二次 apply 覆盖备份结果

第二次运行同一命令后，safe writer 正确识别覆盖并生成备份：

```text
items: 13
overwrites: 13
backup_paths: 13
backup_files: 15
```

备份目录示例：

```text
D:/OBS-V4-DEMO/93_导入报告/V4_备份_20260701_204109/
```

包含：

- `write-plan.json`
- `write-report.md`
- 被覆盖文件的备份副本

## 5. 仓库状态

测试完成后已恢复运行时报告文件，辅助仓库工作树保持干净。

## 6. 结论

V4 在独立测试 vault 中已验证：

- `--vault --apply` 可真实生成完整课程包。
- Canvas JSON 可解析。
- Markdown frontmatter 正常。
- Mermaid 文件包含代码块。
- 覆盖已有文件前会备份。
- 未写正式 Obsidian vault。
