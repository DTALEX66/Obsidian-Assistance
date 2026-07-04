# TALOS Obsidian 兼容与迁移约束

## 目标

当前 `index.html`、`evidence-matrix.html`、`course-reading.html` 继续作为本地可预览 HTML 原型保留。后续如果并入 Obsidian，应迁移为 Obsidian 插件中的自定义视图，而不是依赖外部上传、托管网页或远程 iframe。

## 官方依据

- Obsidian 官方开发文档说明，插件用于用 TypeScript 扩展 Obsidian 功能。
- 官方 Views 文档说明，可以创建自定义 view 来显示插件自己的内容。
- 官方 Manifest 文档说明，插件需要 `manifest.json` 声明 `id`、`name`、`version`、`minAppVersion`、`author` 等元数据。
- 官方 `ItemView` API 文档说明，`ItemView` 可作为自定义视图的基础类。

参考：

- https://docs.obsidian.md/Home
- https://docs.obsidian.md/Plugins/Getting+started/Build+a+plugin
- https://docs.obsidian.md/Plugins/User+interface/Views
- https://docs.obsidian.md/Reference/Manifest
- https://docs.obsidian.md/Reference/TypeScript+API/ItemView

## 推荐迁移路线

1. 保留当前 HTML 原型作为视觉和交互基准。
2. 新建 Obsidian 插件目录，例如 `talos-obsidian-plugin/`。
3. 建立最小插件结构：
   - `manifest.json`
   - `main.ts`
   - `styles.css`
4. 为 TALOS 注册一个自定义 `ItemView`：
   - Home Console -> `TalosHomeView`
   - 证据矩阵 -> `TalosEvidenceView`
   - 课程阅读 -> `TalosCourseView`
5. 把当前 HTML 中的页面模块拆成 TypeScript 渲染函数或组件。
6. 把当前内联 CSS 迁移到插件 `styles.css`，所有选择器加 `talos-` 前缀或挂在插件根容器下。
7. 把当前静态数据改为 Vault 内 Markdown / JSON 文件读写。

## 当前原型必须保留的兼容约束

- 不依赖外部 CDN、远程图片或上传服务。
- 页面继续保持静态 HTML 可预览，方便迁移前做视觉验收。
- 交互逻辑避免框架锁定，优先使用原生 DOM API。
- 可见文本保持中文；技术 ID、文件名、插件 ID 使用英文小写短横线。
- 所有页面入口使用相对路径，未来可映射为 Obsidian command 或 ribbon action。
- CSS 避免污染全局：新增选择器优先使用页面根容器或 `talos-` 命名空间。
- 数据不要写死为不可替换结构；后续应能替换为 Vault 文件读取。

## 插件化时的文件映射

| 当前文件 | Obsidian 插件目标 |
| --- | --- |
| `index.html` | `TalosHomeView` |
| `evidence-matrix.html` | `TalosEvidenceView` |
| `course-reading.html` | `TalosCourseView` |
| 页面内 `<style>` | `styles.css` |
| 页面内 `<script>` | `main.ts` 中的视图逻辑 |
| 任务/证据/课程静态内容 | Vault 内 Markdown / JSON 数据 |

## 暂不做的事

- 不自动写入任何 Obsidian Vault。
- 不访问用户本机 Obsidian 配置目录。
- 不安装 Obsidian 插件依赖。
- 不发布到 Obsidian Community Plugins。
- 不上传任何文件。

## 下一步建议

当 TALOS 页面结构稳定后，再创建 `talos-obsidian-plugin/` 开发包，把当前三个 HTML 页面迁移成自定义视图。迁移前应先确认目标 Vault 数据格式：Markdown frontmatter、JSON sidecar，还是 Canvas 节点。
