const { ItemView, Plugin } = require("obsidian");

const TALOS_HOME_VIEW = "talos-home-view";
const TALOS_READING_VIEW = "talos-reading-view";
const TALOS_EVIDENCE_VIEW = "talos-evidence-view";

const mockMetrics = [
  { label: "今日焦点", value: "阅读工作台", tone: "primary" },
  { label: "证据流", value: "待整理", tone: "neutral" },
  { label: "复习状态", value: "预览", tone: "success" }
];

const mockEvidence = [
  { title: "论点片段", body: "从当前材料中提取可复用判断，等待人工确认。", state: "待审核" },
  { title: "引用候选", body: "保留原文上下文，避免自动写入真实笔记。", state: "只读" },
  { title: "项目关联", body: "展示未来可能的 Project Atlas 关联，不触发索引。", state: "模拟" }
];

module.exports = class TalosFrontendPlugin extends Plugin {
  async onload() {
    this.registerView(TALOS_HOME_VIEW, leaf => new TalosHomeView(leaf));
    this.registerView(TALOS_READING_VIEW, leaf => new TalosReadingView(leaf));
    this.registerView(TALOS_EVIDENCE_VIEW, leaf => new TalosEvidenceView(leaf));

    this.addRibbonIcon("gem", "打开 TALOS 前端工作台", () => {
      this.activateView(TALOS_HOME_VIEW);
    });

    this.addCommand({
      id: "open-talos-home",
      name: "打开 TALOS 前端工作台",
      callback: () => this.activateView(TALOS_HOME_VIEW)
    });

    this.addCommand({
      id: "open-talos-reading",
      name: "打开 TALOS 课程阅读界面",
      callback: () => this.activateView(TALOS_READING_VIEW)
    });

    this.addCommand({
      id: "open-talos-evidence",
      name: "打开 TALOS 证据矩阵",
      callback: () => this.activateView(TALOS_EVIDENCE_VIEW)
    });
  }

  async activateView(type) {
    const leaves = this.app.workspace.getLeavesOfType(type);
    let leaf = leaves[0];

    if (!leaf) {
      leaf = this.app.workspace.getLeaf(true);
      await leaf.setViewState({ type, active: true });
    }

    this.app.workspace.revealLeaf(leaf);
  }

  onunload() {}
};

class TalosBaseView extends ItemView {
  constructor(leaf, config) {
    super(leaf);
    this.config = config;
    this.currentState = "ready";
  }

  getViewType() {
    return this.config.type;
  }

  getDisplayText() {
    return this.config.title;
  }

  getIcon() {
    return "gem";
  }

  async onOpen() {
    this.render();
  }

  async onClose() {}

  render() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass("talos-ui-kit-host");

    const root = container.createDiv({
      cls: "talos-ui-kit",
      attr: {
        "data-talos-view": this.config.type,
        "aria-label": this.config.title
      }
    });

    root.createDiv({ cls: "talos-bg-grid", attr: { "aria-hidden": "true" } });
    this.renderHeader(root);
    this.renderStateBar(root);
    this.renderBody(root);
  }

  renderHeader(root) {
    const header = root.createEl("header", { cls: "talos-header" });

    const brand = header.createDiv({ cls: "talos-brand" });
    brand.createDiv({ cls: "talos-mark", text: "T" });
    const titleWrap = brand.createDiv();
    titleWrap.createDiv({ cls: "talos-eyebrow", text: "TALOS / OBSIDIAN FRONTEND" });
    titleWrap.createEl("h1", { text: this.config.title });
    titleWrap.createEl("p", { text: this.config.subtitle });

    const nav = header.createEl("nav", {
      cls: "talos-view-nav",
      attr: { "aria-label": "TALOS 视图切换" }
    });

    this.createNavButton(nav, "工作台", TALOS_HOME_VIEW);
    this.createNavButton(nav, "阅读", TALOS_READING_VIEW);
    this.createNavButton(nav, "证据", TALOS_EVIDENCE_VIEW);
  }

  createNavButton(parent, label, viewType) {
    const button = parent.createEl("button", {
      cls: viewType === this.config.type ? "talos-tab is-active" : "talos-tab",
      text: label,
      attr: {
        type: "button",
        "aria-pressed": viewType === this.config.type ? "true" : "false"
      }
    });

    button.addEventListener("click", () => {
      this.app.workspace.getLeaf(true).setViewState({ type: viewType, active: true });
    });
  }

  renderStateBar(root) {
    const bar = root.createEl("section", {
      cls: "talos-state-bar",
      attr: { "aria-label": "前端状态检查" }
    });

    const status = bar.createDiv({ cls: `talos-status is-${this.currentState}` });
    status.createSpan({ cls: "talos-status-dot", attr: { "aria-hidden": "true" } });
    status.createSpan({ text: this.getStateCopy() });

    const actions = bar.createDiv({ cls: "talos-state-actions" });
    this.createStateButton(actions, "就绪", "ready");
    this.createStateButton(actions, "加载", "loading");
    this.createStateButton(actions, "空状态", "empty");
    this.createStateButton(actions, "错误", "error");
  }

  createStateButton(parent, label, state) {
    const button = parent.createEl("button", {
      cls: this.currentState === state ? "talos-button is-selected" : "talos-button",
      text: label,
      attr: {
        type: "button",
        "aria-pressed": this.currentState === state ? "true" : "false"
      }
    });

    button.addEventListener("click", () => {
      this.currentState = state;
      this.render();
    });
  }

  getStateCopy() {
    if (this.currentState === "loading") return "正在加载前端视图，不访问真实 Vault";
    if (this.currentState === "empty") return "暂无可展示内容，等待用户选择材料";
    if (this.currentState === "error") return "前端状态异常，未执行任何写入";
    return "前端预览就绪，仅使用模拟数据";
  }

  renderBody(root) {
    const main = root.createEl("main", { cls: "talos-main" });

    if (this.currentState === "loading") {
      this.renderLoading(main);
      return;
    }

    if (this.currentState === "empty") {
      this.renderEmpty(main);
      return;
    }

    if (this.currentState === "error") {
      this.renderError(main);
      return;
    }

    this.renderReady(main);
  }

  renderLoading(main) {
    const panel = main.createDiv({ cls: "talos-feedback-panel" });
    panel.createDiv({ cls: "talos-spinner", attr: { "aria-hidden": "true" } });
    panel.createEl("h2", { text: "正在准备界面" });
    panel.createEl("p", { text: "这是前端加载态演示。不会读取课程、索引 Vault 或调用 AI 服务。" });
  }

  renderEmpty(main) {
    const panel = main.createDiv({ cls: "talos-feedback-panel" });
    panel.createDiv({ cls: "talos-empty-icon", text: "—" });
    panel.createEl("h2", { text: "还没有选择材料" });
    panel.createEl("p", { text: "空状态用于真实插件接入前的安全兜底，避免伪造课程或证据内容。" });
  }

  renderError(main) {
    const panel = main.createDiv({ cls: "talos-feedback-panel is-error" });
    panel.createDiv({ cls: "talos-empty-icon", text: "!" });
    panel.createEl("h2", { text: "界面状态异常" });
    panel.createEl("p", { text: "错误态只提示前端问题，不执行修复脚本、不写入 Vault、不修改插件配置。" });
  }

  renderReady(main) {
    main.createEl("p", { text: "Base view ready." });
  }
}

class TalosHomeView extends TalosBaseView {
  constructor(leaf) {
    super(leaf, {
      type: TALOS_HOME_VIEW,
      title: "TALOS 前端工作台",
      subtitle: "Obsidian 内的紫晶知识工作台界面预览"
    });
  }

  renderReady(main) {
    const grid = main.createDiv({ cls: "talos-dashboard-grid" });

    const hero = grid.createEl("section", { cls: "talos-hero-card" });
    hero.createDiv({ cls: "talos-kicker", text: "前端包 / 安全预览" });
    hero.createEl("h2", { text: "打开 Obsidian 后看到的是界面，不是后台任务" });
    hero.createEl("p", { text: "当前包只注册 TALOS 视图、按钮状态和模拟模块。所有数据均为静态预览，不访问真实知识库。" });

    const metricRow = hero.createDiv({ cls: "talos-metric-row" });
    mockMetrics.forEach(item => {
      const card = metricRow.createDiv({ cls: `talos-mini-metric is-${item.tone}` });
      card.createSpan({ text: item.label });
      card.createStrong({ text: item.value });
    });

    const side = grid.createEl("aside", { cls: "talos-side-panel" });
    side.createEl("h3", { text: "接入边界" });
    const list = side.createEl("ul");
    ["不读取 Vault", "不写入笔记", "不启动索引", "不调用 AI", "不修改插件配置"].forEach(text => {
      list.createEl("li", { text });
    });

    const workflow = main.createEl("section", { cls: "talos-section" });
    workflow.createEl("h2", { text: "核心界面模块" });
    const cards = workflow.createDiv({ cls: "talos-card-grid" });
    this.createFeature(cards, "课程阅读", "中央阅读区、摘录面板、证据候选区，适合独立 ItemView。");
    this.createFeature(cards, "证据矩阵", "过滤、状态、引用候选和项目关系，以卡片矩阵呈现。");
    this.createFeature(cards, "复习中心", "作为右侧栏或 Modal 出现，先做前端空/加载/错误状态。");
  }

  createFeature(parent, title, body) {
    const card = parent.createDiv({ cls: "talos-feature-card" });
    card.createEl("h3", { text: title });
    card.createEl("p", { text: body });
  }
}

class TalosReadingView extends TalosBaseView {
  constructor(leaf) {
    super(leaf, {
      type: TALOS_READING_VIEW,
      title: "课程阅读工作区",
      subtitle: "保留 TALOS 核心工作区，让 Obsidian 承担原生外壳"
    });
  }

  renderReady(main) {
    const shell = main.createDiv({ cls: "talos-reading-grid" });

    const documentPane = shell.createEl("article", { cls: "talos-document-pane" });
    documentPane.createDiv({ cls: "talos-kicker", text: "READING VIEW" });
    documentPane.createEl("h2", { text: "阅读材料标题" });
    documentPane.createEl("p", { text: "这里展示课程阅读界面的排版密度、段落节奏和引用候选，不绑定真实课程文件。" });
    documentPane.createEl("blockquote", { text: "关键摘录会以安全的前端预览方式呈现，等待用户手动确认。" });
    documentPane.createEl("p", { text: "生产接入时，左侧文件树、顶部标签页、属性和反链应使用 Obsidian 原生能力，不在 TALOS 内重复实现。" });

    const actionPane = shell.createEl("aside", { cls: "talos-action-pane" });
    actionPane.createEl("h3", { text: "阅读动作" });
    this.createAction(actionPane, "标记重点", "前端按钮态演示");
    this.createAction(actionPane, "生成证据候选", "仅模拟，不调用 AI");
    this.createAction(actionPane, "加入待审核", "仅展示，不写入 Vault");
  }

  createAction(parent, title, body) {
    const row = parent.createDiv({ cls: "talos-action-row" });
    const copy = row.createDiv();
    copy.createStrong({ text: title });
    copy.createSpan({ text: body });
    row.createEl("button", { cls: "talos-icon-button", text: "+", attr: { type: "button", "aria-label": title } });
  }
}

class TalosEvidenceView extends TalosBaseView {
  constructor(leaf) {
    super(leaf, {
      type: TALOS_EVIDENCE_VIEW,
      title: "证据矩阵",
      subtitle: "以模拟数据检查矩阵布局、筛选状态和卡片层级"
    });
  }

  renderReady(main) {
    const toolbar = main.createDiv({ cls: "talos-toolbar" });
    toolbar.createEl("button", { cls: "talos-button is-selected", text: "全部", attr: { type: "button" } });
    toolbar.createEl("button", { cls: "talos-button", text: "待审核", attr: { type: "button" } });
    toolbar.createEl("button", { cls: "talos-button", text: "只读", attr: { type: "button" } });

    const matrix = main.createDiv({ cls: "talos-evidence-grid" });
    mockEvidence.forEach(item => {
      const card = matrix.createDiv({ cls: "talos-evidence-card" });
      card.createDiv({ cls: "talos-card-state", text: item.state });
      card.createEl("h3", { text: item.title });
      card.createEl("p", { text: item.body });
    });
  }
}
