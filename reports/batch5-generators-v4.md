# Batch 5 Report：生成器层

## 1. 本批次目标

创建课程包、Canvas、Mermaid、Bases 视图和 YAML schema 生成/校验脚本。

## 2. 已新增文件

- scripts/v4/generate_course_pack.py
- scripts/v4/generate_canvas_map.py
- scripts/v4/generate_mermaid_graph.py
- scripts/v4/generate_bases_views.py
- scripts/v4/validate_yaml_schema.py

## 3. 已修改文件

无。

## 4. 风险点

- 生成器默认 dry-run。
- 写正式 vault 时必须显式 `--apply`，并走 safe_vault_writer。

## 5. 自测结果

- 脚本可编译。
- dry-run 可生成计划。
- Canvas JSON 可解析。

## 6. 下一批次建议

进入 Batch 6，生成 demo 课程。
