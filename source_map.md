# Source Map — Agentic Market Daily V12
# 板块来源地图 + 内容质量标准 + 数据获取政策
# 用途: 定义13板块的权威来源、内容质量要求、数据获取规则
# 更新: 每次新增板块或调整来源层级时追加

## V12模板强制要求（格式锁定，不可变更）
- 输出HTML文件必须严格匹配 /root/.openclaw/workspace/agentic_market_daily_template_v12.html 的结构、CSS变量、板块顺序、字体大小和间距
- **标题固定**：title=Agentic Market Daily | YYYY-MM-DD 和 h1=Agentic Market Daily
- **主题色固定**：青蓝暗色主题
  - `--accent: #00d4ff`（主色：标题、边框、高亮文字）
  - `--highlight: #e94560`（高亮：数字标签、hot标签）
  - `--bg: #0a0e1a`, `--card: #0d1f35`, `--card2: #0a1929`
  - `--text: #e6edf7`, `--text2: #8892b0`, `--border: #1a2d4a`
  - `--success: #4ecca3`, `--warning: #ffc107`, `--danger: #ff4757`
- **板块标题格式固定**：`<div class="section-title"><span class="num">{number}</span> {名称}</div>`
  - `.num` 是圆形数字标签（background: var(--highlight)）
  - 禁止使用 `.section-number` 或其他变体
- **板块顺序固定（13个）**：
  1. 核心持仓实时行情（21只股票，含BUY/HOLD/SPEC BUY标签+分类标签）
  2. 投资人及权威机构最新论点
  3. AI独角兽模型技术动向
  4. NVIDIA / AMD / Intel（财报级信号）
  5. 中国云厂商AI策略
  6. AI Agent应用趋势
  7. Agent接口及生态标准化
  8. 开源社区技术路径深度追踪 & 因果链分析
  9. ToC侧Agent应用及硬件部署形式
  10. 全球交易：大宗商品与金融趋势
  11. 政治突发：地缘与政策对供应链影响
  12. Gen Z研究：15-24岁行为信号
  13. 个性化推荐：值得深度跟踪的信号
- **特殊样式类必须保留**：`.quote-box` `.quote-text` `.quote-source` `.quote-context` `.play-btn`（权威引用块）；`.insight-box` `.label` `.content`（洞察框）；`.signal-list` `.tag` `.tag-hot` `.tag-new` `.tag-key`（信号列表+标签）；`.causal-chain` `.chain-title` `.chain-item` `.key` `.val`（因果链分析）；`.highlight-stock`（股票卡片边框高亮）
- **表格样式固定**：`.data-table` 统一样式，表头 `background: #0a1628; color: var(--accent); border-bottom: 2px solid var(--accent)`，斑马纹 `var(--card2)`
- **禁止**增删板块、调换顺序、合并或拆分板块
- **股票面板格式固定**：21只卡片，每张含：
  - 左上角 `.rec-badge`（BUY/HOLD/SPEC BUY），绝对定位
  - 右上角 `.cat-badge`（芯片/应用/能源），绝对定位
  - 中间：ticker + name + price + **change%（日涨跌幅，从CSV的pct_change字段）**
  - 底部 `.stock-metrics`："核心指标: xxx | xxx | xxx"
  - 底部 `.stock-reason`："推荐: " + 底层逻辑
  - CSS: `.stock-card { position: relative; }`
  - **强制**：价格必须来自ifind API `close`字段，涨跌幅来自`pct_change`字段
- **S4表格格式**：必须包含"日涨跌"列，数据来自ifind API
- **S8 PR链接**：vLLM/SGLang PR编号必须为可点击的GitHub PR链接（如`https://github.com/vllm-project/vllm/pull/12845`）
- 每日仅更新内容（文字、数据、价格），模板结构零变更
- 生成后必须对比 template_v12.html 的结构一致性（section数量、class名、CSS变量）

---

## 输出流程（GitHub Pages部署 - 强制）
1. 生成HTML格式晨报，使用专业暗色主题
2. 保存到 /root/.openclaw/workspace/daily_report_YYYY-MM-DD.html
3. 复制到index.html: cp daily_report_YYYY-MM-DD.html index.html
4. 部署到GitHub Pages:
   - cd /root/.openclaw/workspace
   - git remote set-url origin https://TOKEN@github.com/glrocks/daily-report.git
   - git add -f index.html daily_report_YYYY-MM-DD.html
   - git commit -m "Daily report YYYY-MM-DD"
   - git push origin master --force
5. 向用户推送固定链接: https://glrocks.github.io/daily-report/（每日固定地址，不再使用Cloudflare Tunnel）
6. 部署后立即验证: curl -s https://glrocks.github.io/daily-report/ | grep -c "Agentic Market Daily"

---

## 搜索约束
- 每板块最多2次搜索，避免token耗尽
- 优先使用freshness=day或date_after参数，确保内容当日/昨日新鲜
- 无当日新闻时标注'近期重要信号'并给出时间戳
- 引用来源必须标注具体机构/人名+日期
- 去重：避免与近3日已覆盖topic重复

---

## 内容质量标准
- 国际观点80%，国内20%
- 只引用Tier 1/2来源，拒绝36kr/钛媒体/未署名'据知情人士'
- 芯片板块禁止产品发布通稿/过时信息，仅收录5类信号：财报/业绩、订单/产能变化、战略/并购/管理层变动、技术路线重大分歧、地缘/政策影响
- 每条信息必须通过"so what"测试——"这会改变什么投资决策？"
- 质量而非数量：宁可一个板块只有1条高价值洞察，也不要3条平庸信息
- 时效性优先：如果当日无值得收录的高价值信号，直接标注"当日无重大投资信号"，不要回溯旧信息填充

---

## 13个板块详细要求（按推送顺序）
1. 核心持仓实时行情 1
2. 投资人及权威机构最新论点（深度标准）：核心张力框架+言论考古+观点矩阵。覆盖Marc Andreessen/Ray Dalio/Larry Fink/Jensen Huang/Sundar Pichai/Sam Altman。必须附带播放按钮。
3. AI独角兽模型技术动向（强制覆盖7家公司）：Anthropic、OpenAI、Google、DeepSeek、Bytedance、Moonshot、Minimax。每家公司最新模型发布/融资/安全认证/客户反馈必须覆盖。其他模型信息仅当获得北美或中国客户同步认可时方可收录。每条事件附权威人士评论+数据表格（模型参数/推理成本/市场份额对比）。
4. NVIDIA/AMD/Intel（仅收录5类信号：财报/订单/战略/技术路线/地缘，禁止产品通稿）。强制数据表格+大佬评论。
5. 中国云厂商：阿里/腾讯/百度AI策略、自研芯片、DAU/MAU。强制数据表格。
6. AI Agent：Cursor/Cognition/垂直agent估值、开源生态。附投资人评论。强制数据表格。
7. Agent标准化：MCP/A2A/Skills生态进展。强制数据表格。
8. 开源社区技术路径深度追踪&因果链分析：
    - **开源社区PR/里程碑追踪**：vLLM、SGLang社区近期高star/高评论PR/里程碑，技术point、解决问题、投资含义
    - **大厂技术路径矩阵**：Anthropic/OpenAI/DeepSeek/Google/Moonshot/ByteDance按底层模型/Inference Framework/Agentic AI分类对比
    - **社区vs公司异同**：开源社区 vs 闭源大厂 vs 开源大厂技术路径对比表（推理优化/Agent集成/生态锁定/商业化路径）
    - **因果链分析**：开源推理框架突破→Agentic AI部署成本下降→ToC Agent应用爆发→推理需求结构变化→芯片设计优先级转移。格式：触发因→传导机制→时间尺度→投资预测→证伪信号→推荐标的（TICKER+thesis）
    - **强制数据表格**：PR追踪表（时间/里程碑/PR编号/标题/技术point/解决问题/投资含义）、大厂技术路径矩阵表、社区vs公司异同对比表
9. ToC侧Agent应用及硬件部署形式：端侧AI芯片（NVIDIA Jetson/Intel NPU/AMD Ryzen AI/Qualcomm骁龙X Elite等）。强制数据表格：端侧芯片算力TOPS/功耗/出货量对比。
10. 全球交易：铜/锂/稀土/半导体设备/DRAM-NAND价格趋势+政治因素。强制数据表格。
11. 政治突发：出口管制/关税/地缘冲突对供应链影响。**强制引用政府官方来源**：BIS Federal Register / Commerce Department / European Commission / 国务院关税税则委员会（中国）。禁止引用ASML年报、设备商财报、未验证网站作为政策来源。超过30天的政策信息必须有新变动才能收录。强制数据表格。
12. Gen Z研究：15-24岁平台迁移/消费/社交行为信号。**强制标注调研数据样本量**：每条调研数据必须标注样本量、调研机构、时间、地理范围。禁止连续3条以上引用同一来源。超过14天的调研数据必须有更新数据或新解读。强制数据表格。
13. 个性化推荐：基于用户半导体投资背景的深度信号。附权威分析。

---

## 内容新鲜度与准确性强制机制（2026-05-12生效）
1. **搜索层强制**：每条搜索必须使用freshness=day或date_after:today-2，禁止无时间筛选的通用搜索
2. **交叉验证强制**：每个关键事实（模型版本/财报数据/价格/人物言论）必须来自≥2个独立来源
3. **模型信息验证**：版本号/发布日期/上下文窗口/定价必须与官方渠道核对，不符则标注"待确认"或不收录
4. **财报数据验证**：必须使用最新已发布季度，禁止回溯上一季度数据填充
5. **股价/价格标注**：必须标注数据日期和来源（如"铜价$9,850/t, 2026-05-12, 来源:Bloomberg"）
6. **人物言论验证**：必须附原始来源链接+发言日期+场合+上下文说明，禁止二手聚合引用
7. **去重拦截**：生成前读取/root/.openclaw/workspace/memory/daily_topics_log.md，近3日已覆盖Topic→不收录；近4-7日→仅新进展跟进
8. **过时信息拦截**：产品发布>30天视为背景信息需新进展；模型发布>14天需新版本/新功能；政策需最新变动
9. **推送前自检清单（必须执行）**：
   - [ ] 所有模型版本号与官方最新一致？
   - [ ] 所有财报数据为最新季度？
   - [ ] 所有价格数据标注日期和来源？
   - [ ] 近7日日志中无重复Topic？
   - [ ] 国际观点≥80%？
   - [ ] 无36kr/钛媒体/未署名"据知情人士"信息？
   - [ ] 每条信息通过"so what"测试？
   - [ ] 开源社区PR编号已在GitHub验证真实存在？（2026-05-13新增）
10. **问责规则**：自检不通过→标注"当日无重大投资信号"，宁可不推也不推过时信息
11. **错误追溯**：如用户指出错误，记录到/root/.openclaw/workspace/memory/accuracy_errors.md并修正规则
12. **生成后动作**：每日晨报生成后追加/root/.openclaw/workspace/memory/daily_topics_log.md

---

## 股票数据强制规则（2026-05-13新增）
1. 价格100%来自ifind API `realtime_price`的`close`字段，禁止搜索引擎回填
2. 变动禁止直接使用`pct_change_1m`（1分钟无意义）。改用`(close-open)/open×100%`计算日内涨跌幅
3. 任一股票API调用失败→该股票标注"价格暂缺"，禁止编造数字
4. 生成前执行stock validation：API获取全部20只→检查close有效性→写入CSV→模板从CSV读取
5. YTD禁止硬编码。如需YTD必须搜索获取+标注来源+交叉验证

---

## Open Source Community PR/Milestone Policy (Added 2026-05-13)
**Scope**: Section 8 (开源社区技术路径深度追踪) — vLLM/SGLang/llama.cpp等开源项目的PR/里程碑追踪表

### 强制规则
1. **禁止编造PR编号**：**绝对禁止**在PR追踪表中编造具体的GitHub Pull Request编号（如"PR #11234"）。模板中PR追踪表的"PR/里程碑"列标题已改为"里程碑/焦点"。
2. **两种填写方式**：
   - **方式A（无真实PR编号时）**：使用描述性文字，如"近期焦点：PD分离支持"、"Milestone: Multi-LoRA并发"、"Release: v0.12.0"
   - **方式B（有真实PR编号时）**：仅当100%确认PR编号在GitHub仓库中真实存在时才使用编号。确认方式：在github.com/{owner}/{repo}/pull/{number} 可访问且非404。
3. **验证步骤（内容生成时执行）**：
   ```
   1. 需要引用具体PR编号时，先访问 https://github.com/vllm-project/vllm/pull/{number}
   2. 页面404 → 禁止在报告中使用该编号，改用方式A描述
   3. 页面存在 → 检查标题/描述与报告内容是否一致
   4. 不一致 → 以实际PR标题为准，修正报告内容
   ```
4. **来源标注**：PR追踪表中的每一条记录的"里程碑/焦点"字段必须附带可点击的GitHub超链接（`<a href="https://github.com/..." target="_blank" class="source-link">...`），指向对应的PR页面、Release页面或仓库搜索页面。不允许无链接的纯文本描述。

### 错误案例（2026-05-13）
- **错误**: vLLM "PR #11234: PD分离支持"、SGLang "PR #892: Speculative Decode"、vLLM "PR #11120: Chunked Prefill"
- **根因**: 模板中使用占位符编号，每日内容生成时未核实替换，导致虚假编号进入最终报告
- **后果**: 用户到vLLM/SGLang仓库验证发现PR不存在，严重损害报告可信度
- **修正**: 模板中所有具体PR编号改为"近期焦点：描述"；新增本规则写入source_map.md

### 问责
- 违反"禁止编造PR编号"规则→记录到accuracy_errors.md
- 连续2次PR编号造假→暂停Section 8生成，改为仅收录已验证的release/milestone信息

---

## P0修复记录（2026-05-15执行）

### 修复1: 播放按钮真实URL化
- **问题**: `.play-btn` 使用 `<div>` 标签，点击无反应，只有tooltip提示"原声内容请访问上方来源链接"
- **修复**: 全部改为 `<a href="来源URL" class="play-btn" target="_blank">` 真实链接
- **规则追加**: 投资人及权威机构最新论点（S2）中每条言论的`.play-btn`必须链接到来源机构真实URL或相关报道页面，禁止纯CSS样式div
- **模板已更新**: `agentic_market_daily_template_v12.html` 中4条权威言论的播放按钮已改为真实链接

### 修复2: 股票卡片日涨跌幅字段删除
- **问题**: `pct_change_1m`被误用为日涨跌幅，实际为1分钟变动≈0%，展示为日涨跌是误导
- **修复**: 从S1股票卡片中完全移除`<span class="change">`元素，`.price-row`只保留`<span class="price">`
- **规则追加**: S1核心持仓实时行情中，股票卡片禁止展示日涨跌幅。ifind API不提供US stock真实日涨跌，禁止自行计算或搜索回填
- **模板已更新**: 21只股票的change元素已全部移除

### 修复3: S4表格删除"日涨跌"列
- **问题**: S4 NVIDIA/AMD/Intel表格中的"日涨跌"列同样使用错误数据
- **修复**: 删除该列，表格变为：公司/收盘价/YTD/关键催化/投资信号
- **模板已更新**: S4表格已删除日涨跌列

### 修复4: 全文标的评级一致性
- **问题**: S1中QCOM=HOLD但S13信号1建议"投机仓位"；S1中NVDA=BUY（highlight-stock）但S13信号3建议"降级为HOLD"
- **修复**: 
  - QCOM: S1=HOLD, S13=HOLD（统一为HOLD，删除"投机仓位"表述）
  - NVDA: S1=BUY（核心持仓+highlight-stock）, S13=BUY（统一维持BUY，删除降级表述）
  - AMD: S1=BUY, S13=BUY（已一致）
  - Intel: S1=BUY, S13=BUY（统一维持BUY）
- **规则追加**: 同一标的在全文中只能有一个评级。S1股票面板的评级是全篇唯一权威评级，S13个性化推荐中的投资建议必须与S1一致，禁止矛盾

### 修复5: href="#"占位符拦截
- **问题**: 模板曾存在`href="#"`占位符，导致点击跳转页面顶部而非来源页面
- **状态**: 当前模板已无`href="#"`，所有source-link指向真实机构域名
- **规则追加**: 模板中禁止任何`href="#"`的source-link或play-btn。生成后必须执行`grep -c 'href="#"'`检查，>0则预检失败

---

## 专家固化表（2026-05-15追加）

| 板块 | 专家角色 | 权威来源清单 | 搜索策略 |
|---|---|---|---|
| S1 股票 | 量化总监 | ifind API唯一合法来源 | `realtime_price` |
| S2 投资人论点 | 宏观策略师 | Bloomberg/BBC/YouTube原始采访/官方博客 | `freshness:day` + 发言人姓名 |
| S3 模型动向 | 模型技术专家 | 官方GitHub/blog/announcement + Reuters/Bloomberg | `freshness:day` + 模型名称 |
| S4 芯片三巨头 | 半导体设备分析师 | SEC filing/earnings call + SemiAnalysis/Bernstein | 财报季搜索 |
| S5 中国云 | 中国互联网分析师 | 各公司earnings/官方blog + Bloomberg China/Goldman Sachs China | `freshness:day` |
| S6 Agent应用 | 产品经理 | 公司官方数据 + a16z/Greylock/Menlo VC研究 | `freshness:day` |
| S7 标准化 | 生态架构师 | 官方protocol文档 + GitHub MCP/A2A仓库 | 仓库watch |
| S8 开源社区 | 开源技术专家 | GitHub PR/Release页面（必须验证存在） | 仓库直接访问 |
| S9 ToC硬件 | 硬件产品专家 | IDC/Counterpoint/公司官方数据 | `freshness:day` |
| S10 全球交易 | 大宗商品分析师 | LME/Bloomberg Commodities/官方数据 | `freshness:day` |
| S11 政治地缘 | 政策研究员 | BIS Federal Register/Commerce Dept/EU Commission | 政府网站 |
| S12 Gen Z | 用户研究专家 | Deloitte/McKinsey/Pew/Sensor Tower（必须标样本量） | `freshness:day` |
| S13 个性化 | 投资组合经理 | 基于S1-S12信号综合推导 | 内部逻辑 |

**执行规则**：每板块生成前，必须回顾对应专家角色和权威来源清单。来源不在清单中 → 禁止收录。搜索策略不符 → 重新搜索。

---

## 内容质量预检层（2026-05-15追加，机器强制执行）

以下检查项由 `pre_flight_check.py` 在格式检查之后自动执行，任一失败则FATAL中止部署：

### CQ1 模型版本号交叉验证（S3）
- 检查S3中所有模型版本号（如GPT-5.5、Kimi K2.6、Claude 4等）
- 必须与官方最新发布核对（OpenAI blog/Anthropic changelog/Google AI blog）
- 发现过时版本号 → FATAL，标注"版本号待确认"

### CQ2 财报数据时效性（S4）
- 检查S4中所有财报数据
- 禁止使用上一季度数据填充（如Q2已发布则禁止引用Q1）
- 发现回溯数据 → FATAL

### CQ3 PR真实性验证（S8）
- 检查S8中所有GitHub PR编号
- 必须能在 `github.com/{owner}/{repo}/pull/{number}` 访问且非404
- 发现编造PR编号 → FATAL
- PR标题/描述与报告内容不一致 → FATAL

### CQ4 政策来源禁令（S11）
- 检查S11中是否包含ASML年报、设备商财报、未验证网站
- 发现禁止来源 → FATAL
- 政策信息未引用政府官方来源 → FATAL

### CQ5 调研数据样本量（S12）
- 检查S12中每条调研数据是否标注样本量、机构、时间、地理范围
- 发现未标注样本量的调研数据 → FATAL
- 同一来源引用>2次 → FATAL

### CQ6 国际观点占比（全文）
- 检查全文来源国籍分布
- 国内来源（中国媒体/机构）占比>20% → FATAL
- 例外：仅当报道中国独家事件（如工信部政策、中芯财报）时允许

**问责**：以上检查任一项FATAL → 不部署、不推送、通知用户"当日晨报因内容质量未通过延迟"

---

## 搜索执行策略（2026-05-15追加）

### 强制搜索参数
- `freshness:day` 或 `date_after:today-2` — 无时间筛选 = 禁止
- 每板块最多2次搜索
- 来源优先级：Tier 1 > Tier 2 > 禁止

### 交叉验证规则
- 关键事实（模型版本/财报/价格/人物言论）必须≥2个独立来源
- 独立来源定义：不同机构/不同记者/不同语言区

### 验证步骤（机器强制执行）
1. **模型版本**：搜索后访问官方GitHub/blog确认版本号
2. **财报数据**：搜索后访问SEC filing/earnings call transcript确认
3. **PR编号**：搜索后访问GitHub仓库确认PR存在
4. **人物言论**：搜索后访问原始采访/官方博客确认
5. **政策信息**：搜索后访问政府网站确认

**未验证通过 → 不收录该信息，宁可板块留空**

---

