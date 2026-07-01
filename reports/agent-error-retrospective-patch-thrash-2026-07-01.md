# Agent Error Retrospective: Patch Thrash Prevention

日期：2026-07-01

## 1. 真实触发

在修复 V4 生成器与审计脚本时，连续使用短上下文 `patch` 修改同一小区域，出现多次相邻行误删：

- `generate_course_pack.py` 中曾误删 `course = ...`、`Path(args.report_dir).mkdir(...)`、`print(...)`、`main()`。
- `obsidian_v4_audit.py` 中曾误删 `return {...}`、`parser = argparse.ArgumentParser()`、`result = audit(...)`。

这些不是业务逻辑复杂导致，而是编辑方法错误：短字符串匹配在相邻相似结构中不稳定，连续补丁会放大损坏。

## 2. 根因

1. patch 的 `old_string` 上下文太短。
2. 同一区域连续多次 patch，没有在每次后完整读取目标函数。
3. 修复局部错误时没有立即运行最小语法检查。
4. 对小文件继续做微补丁，而不是整文件重写。

## 3. 新规则

以后出现以下任一情况，必须停止微补丁：

- 同一文件/函数连续两次 patch。
- patch 结果误删相邻必需行。
- linter 报缩进/入口缺失/变量未定义等结构性错误。

改用：

1. 读取完整文件或完整函数。
2. 对短小脚本直接 `write_file` 整文件重写。
3. 立即运行：

```bash
python -m py_compile <file>
```

4. 立即运行该 bug 的最小复现命令。
5. 再运行全量测试与安全审计。

## 4. 本次已验证的收敛命令

```bash
python -m py_compile scripts/*.py scripts/v4/*.py pytest.py
python -m pytest tests -q
python scripts/v4/obsidian_v4_audit.py .
python scripts/v4/generate_course_pack.py --course "Conflict Demo" --output /tmp/v4-dryrun-conflict --apply --dry-run --report-dir /tmp/v4-dryrun-report
```

预期：

- 全量测试通过。
- 安全审计 `ok=true`。
- `--apply --dry-run` 冲突命令失败，并且不写输出文件。

## 5. 技能更新

已把该规则写入 `obsidian-knowledge-base` 技能的 V4 auxiliary-repo engineering mode：

> Patch-thrash prevention rule: if two consecutive patches in the same small file/region delete adjacent required lines, stop using targeted patch for that region. Re-read the whole file or relevant full function, rewrite the complete small file/function with `write_file`, then immediately run syntax checks plus the tight regression command.
