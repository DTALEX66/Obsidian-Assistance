# TALOS Frontend UI Obsidian Package

这是当前工作区内的 **前端-only Obsidian 插件包**，用于检查 TALOS 界面是否能作为 Obsidian 插件视图接入。

## 范围

本包只做：

- Obsidian 插件视图注册
- TALOS 前端界面渲染
- 模拟数据
- 按钮状态、空状态、加载状态、错误状态
- 响应式布局和可访问性状态

本包不做：

- 读取真实 Vault
- 写入真实笔记
- 扫描课程库
- 启动索引
- 调用 AI
- 修改 `.obsidian` 配置
- 运行 Git 或同步任务

## 文件

- `manifest.json`：Obsidian 插件声明
- `main.js`：前端视图入口，注册工作台、阅读、证据三个视图
- `styles.css`：TALOS 紫晶界面样式，全部使用 `.talos-*` 作用域
- `preview.html`：工作区内浏览器预览页，不需要 Obsidian 环境
- `FRONTEND_AUDIT.md`：前端交付检查记录
- `PIXEL_TUNING.md`：参考图复刻与像素调校记录
- `assets/`：包内 SVG 配图资产

## 如何在工作区检查

当前文件先留在工作区内检查，不写入真实 Vault。

如果之后要在 Obsidian 里打开，需要由用户确认后，再把整个 `talos-frontend-ui` 文件夹复制到：

```text
D:\BaiduSyncdisk\Obsidian知识库\.obsidian\plugins\talos-frontend-ui
```

然后在 Obsidian 中启用 `TALOS Frontend UI` 插件。

## 视图

插件提供三个前端视图：

- `TALOS 前端工作台`
- `TALOS 课程阅读界面`
- `TALOS 证据矩阵`

每个视图都包含：

- 就绪状态
- 加载状态
- 空状态
- 错误状态
- 可键盘聚焦按钮
- 安全边界说明

## 交付检查

- [x] 前端包在当前工作区内
- [x] 不写真实 Vault
- [x] 不读取课程内容
- [x] 不调用网络或 AI
- [x] 不修改 `.obsidian`
- [x] 有 Manifest
- [x] 有主入口
- [x] 有样式作用域
- [x] 有空/加载/错误状态
- [x] 有响应式布局
- [x] 有按钮 hover/focus/selected 状态
- [x] 有工作区预览页
- [x] 有交付审查记录
- [x] 有参考图像素调校记录
- [x] 有包内配图资产，不依赖外部网络
