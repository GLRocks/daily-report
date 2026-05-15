# Agentic Market Daily — 格式锁定文档

**生效日期**: 2026-05-12  
**锁定人**: 用户（技术总监）  
**禁止变更**: 标题、主题色、板块顺序、股票面板格式、CSS结构

---

## 不可变更项（Zero Tolerance）

### 1. 标题
- `title` 标签: `Agentic Market Daily | YYYY-MM-DD`
- `h1` 标签: `Agentic Market Daily`
- 禁止任何变体（如"今日晨报"、"晨报"等）

### 2. CSS变量（青蓝暗色主题）
```css
:root {
  --bg: #0a0e1a;
  --card: #0d1f35;
  --card2: #0a1929;
  --text: #e6edf7;
  --text2: #8892b0;
  --accent: #00d4ff;       /* 主色：青蓝色 */
  --highlight: #e94560;    /* 高亮/数字标签：红色 */
  --success: #4ecca3;
  --warning: #ffc107;
  --danger: #ff4757;
  --border: #1a2d4a;
}
```
- `--accent: #00d4ff` 用于标题、边框、高亮文字
- `--highlight: #e94560` 仅用于数字标签背景、hot标签、强调
- 禁止将 `--highlight` 改为其他颜色

### 3. 板块顺序（13个，不可增删/调换）

| # | 板块名称 | 内容锁定 |
|---|---------|---------|
| 1 | **核心持仓实时行情** | 21只股票面板，含BUY/HOLD/SPEC BUY标签+芯片/应用/能源分类标签 |
| 2 | **投资人及权威机构最新论点** | 深度标准：核心张力框架+言论考古+观点矩阵。`.quote-box` + `.play-btn` |
| 3 | **AI独角兽模型技术动向** | 强制覆盖7家公司：Anthropic/OpenAI/Google/DeepSeek/ByteDance/Moonshot/Minimax |
| 4 | **NVIDIA / AMD / Intel（财报级信号）** | 仅5类信号：财报/订单/战略/技术路线/地缘 |
| 5 | **中国云厂商AI策略** | 阿里/腾讯/百度，强制数据表格 |
| 6 | **AI Agent应用趋势** | Cursor/Cognition/垂直agent，附投资人评论 |
| 7 | **Agent接口及生态标准化** | MCP/A2A/Skills，强制数据表格 |
| 8 | **开源社区技术路径深度追踪 & 因果链分析** | PR追踪+大厂矩阵+社区vs公司对比+因果链传导路径 |
| 9 | **ToC侧Agent应用及硬件部署形式** | 端侧AI芯片（Jetson/Intel NPU/AMD Ryzen AI/Qualcomm骁龙X Elite等） |
| 10 | **全球交易：大宗商品与金融趋势** | 铜/锂/稀土/DRAM-NAND，强制数据表格 |
| 11 | **政治突发：地缘与政策对供应链影响** | 出口管制/关税/地缘冲突，强制数据表格 |
| 12 | **Gen Z研究：15-24岁行为信号** | 平台迁移/消费/社交行为，强制数据表格 |
| 13 | **个性化推荐：值得深度跟踪的信号** | 基于半导体投资背景的深度信号 |

### 4. 板块标题格式
```html
<div class="section-title"><span class="num">{number}</span> {板块名称}</div>
```
- `.num` 是圆形数字标签（background: var(--highlight)）
- 禁止使用 `.section-number` 或其他变体

### 5. 股票面板格式（21只卡片）
每张卡片必须包含：
- 左上角: `.rec-badge`（BUY/HOLD/SPEC BUY），绝对定位
- 右上角: `.cat-badge`（芯片/应用/能源），绝对定位
- 中间: `ticker` 代码 + `name` 公司名 + `price` 价格 + `change` 涨跌幅
- 底部 border-top: `.stock-metrics` — "核心指标: xxx | xxx | xxx"
- 底部 border-top: `.stock-reason` — "推荐: " + 底层逻辑
- CSS: `.stock-card { position: relative; }`

### 6. 特殊样式类（必须保留）
- `.quote-box` / `.quote-text` / `.quote-source` / `.quote-context` / `.play-btn` — 权威人士引用块
- `.insight-box` / `.label` / `.content` — 洞察框
- `.signal-list` / `.tag` / `.tag-hot` / `.tag-new` / `.tag-key` — 信号列表+标签
- `.causal-chain` / `.chain-title` / `.chain-item` / `.key` / `.val` — 因果链分析
- `.highlight-stock` — 股票卡片边框高亮

### 7. 表格样式
- `.data-table` — 统一表格样式
- 表头: `background: #0a1628; color: var(--accent); border-bottom: 2px solid var(--accent)`
- 斑马纹: `tr:nth-child(even) { background: var(--card2); }`
- 高亮: `.highlight` / `.up` / `.down`

### 8. 响应式
- `@media (max-width: 768px)` — 股票网格调整为 `minmax(160px, 1fr)`

---

## 可变更项（每日更新）

仅以下内容可变更：
- 股票价格、涨跌幅数据
- 板块内的文字内容、新闻事件、分析观点
- 数据表格中的具体数值
- 权威人士评论的具体言论和日期
- 因果链分析的具体传导路径和推荐标的
- `.highlight-stock` 类名应用（根据当日表现动态标记）

---

## 验证 checklist（每日生成后必须执行）

- [ ] 标题是否为 `Agentic Market Daily`？
- [ ] CSS `--accent` 是否为 `#00d4ff`？
- [ ] CSS `--highlight` 是否为 `#e94560`？
- [ ] 板块数量是否为 **13** 个？
- [ ] 板块顺序是否与上表一致？
- [ ] 投资人论点是否在 **第2位**？
- [ ] 股票面板是否有 21 只卡片？
- [ ] 每张卡片是否有 rec-badge + cat-badge？
- [ ] 特殊样式类（quote-box/play-btn/causal-chain等）是否保留？
- [ ] 文件大小是否在 45KB-60KB 范围内？
- [ ] 是否通过 Cloudflare Tunnel 发布公网链接？

---

## 模板文件路径

- **基准模板**: `/root/.openclaw/workspace/agentic_market_daily_template_v12.html`（56564字节）
- **当日输出**: `/root/.openclaw/workspace/daily_report_YYYY-MM-DD.html`
- **来源**: 用户下载确认版 `19e1bbdd-a3c2-8ef8-8000-0000735cc10e_Agentic_Market_Daily_2026-05-12.html`

---

## 历史变更记录

| 日期 | 变更内容 | 变更人 |
|------|---------|--------|
| 2026-05-12 18:30 | 格式锁定生效，青蓝暗色主题，13板块固定顺序，47KB基准模板 | 技术总监确认 |

---

**违反此文档的格式变更将被视为系统故障，需立即回滚并修复。**
