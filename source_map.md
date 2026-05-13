# Daily Report Source Map
# For: 半导体投资机构技术总监
# Standard: Investment-grade technical intelligence
# Updated: 2026-04-28

## Content Source Policy (Strict)

### Source Mix Ratio
- **International perspective: 80%** | **Domestic perspective: 20%**
- International sources dominate global technology, finance, and policy analysis
- Domestic sources used ONLY for China-specific signals (policy, local market data, China-only company actions)
- If a domestic source has an international equivalent covering the same topic, use the international one
- Track source nationality per section; exceed 20% domestic = cut and replace

### ACCEPTABLE — Tier 1 (Primary)
- **International Consulting**: McKinsey, BCG, Bain, Deloitte Tech
- **Sell-Side Research**: Bernstein, Morgan Stanley, Goldman Sachs, JP Morgan, Citi, Nomura
- **Technology Research**: Gartner, IDC, Counterpoint, TechInsights, SemiAnalysis, Semi Engineering, EE Times
- **Academic/Technical**: IEEE, ISSCC, VLSI Symposium, Hot Chips, Nature, Science, arXiv (selective)
- **Policy/Geopolitical**: CSIS, RAND, CFR, BIS, CRS, European Commission
- **Company Official**: SEC filings (10-K/10-Q/8-K), earnings call transcripts, official technical blogs
- **Executive Primary**: Direct interviews, keynotes, verified social media (Jensen Huang, Lisa Su, etc.)

### ACCEPTABLE — Tier 2 (Selective, Must Verify)
- **Financial News**: Reuters, Bloomberg, Financial Times, Wall Street Journal (original reporting only)
- **Trade Press**: DigiTimes, EETimes, Semiconductor Engineering (must have named sources)
- **VC/PE Research**: a16z, Sequoia, Greylock, Menlo Ventures (published research notes only)

### ACCEPTABLE — Domestic Sources (Strict 20% Cap)
**ALLOWED ONLY when covering China-exclusive events AND no international equivalent exists:**
- **Policy**: 工信部/发改委/商务部 official announcements (original document, not media interpretation)
- **Financial Data**: 中信证券, 中金公司 sell-side research (named analyst, dated)
- **Supply Chain**: DigiTimes China edition (must have named sources)
- **Company Official**: 公司官方财报电话会, SEC filings (dual-listed companies)
- **Executive Primary**: 马化腾, 李彦宏, 梁汝波 direct interviews/keynotes

**REJECTED domestic sources (zero tolerance):**
- 36kr, 钛媒体, 品玩, 雷锋网, 澎湃新闻科技版, 界面科技 — all domestic tech media
- 微信公众号/自媒体 "深度分析"
- 雪球/东方财富论坛观点
- 知乎/微博大V分析

### UNACCEPTABLE — Explicitly Rejected
- ❌ 36kr, 钛媒体, 品玩, 雷锋网等国内科技快讯媒体
- ❌ Reddit, Hacker News, Twitter threads (as primary source)
- ❌ 自媒体/公众号 "深度分析" 无署名信源
- ❌ "据知情人士" / "业内人士称" 无追踪记录的信源
- ❌ 产品发布会通稿改写
- ❌ 论坛搬运/翻译内容
- ❌ 任何内容的 "中文科技媒体二次传播"

### Citation Standard
Every claim must be traceable to:
- **Research report**: Firm name + analyst name + date
- **Executive statement**: Name + title + event/date + direct quote
- **Policy document**: Agency + document number + date
- **Technical data**: Institution + methodology + date

---

## Section 1: AI Unicorns Model Tech Trends
**Decision relevance**: Compute demand forecast, custom silicon opportunities, cloud capex trajectory

**Tier-1 Sources**:
- SemiAnalysis (Dylan Patel) - absolute must-read for silicon strategy
- TechInsights - chip-level teardowns and cost analysis
- MLCommons benchmark updates - real training/inference performance
- NVIDIA/AMD/Google official technical blogs (not PR blogs)
- arXiv cs.LG/cs.AI (filter: companies + breakthrough architectures)
- Twitter/X: @DylanLJPatel, @dr_simon_gregg, @bindureddy, @karpathy (when he posts)

**Executive Intel**:
- Jensen Huang latest keynote/interview (GTC, earnings call, CNBC)
- Sam Altman (OpenAI) - infrastructure scaling signals
- Demis Hassabis (DeepMind) - research-to-product pipeline

**Red Flags to Ignore**:
- 36kr/钛媒体等国内科技媒体快讯
- 未经芯片实测的"跑分新闻"
- 产品发布会通稿

---

## Section 2: NVIDIA/AMD/Intel Products + AI Software Stack
**Decision relevance**: Incumbent competitive positioning, foundry allocation, supply chain health

**Tier-1 Sources**:
- SemiAnalysis (architecture deep-dives)
- AnandTech / Tom's Hardware (launch reviews with die shots)
- IEEE Spectrum / ISSCC proceedings (technical architecture)
- Morgan Stanley / Bernstein semiconductor research notes
- Company 10-K/10-Q "Product Outlook" sections
- SEC filings (capacity commitments, supply agreements)

**Executive Intel**:
- Jensen Huang (NVIDIA) - every earnings call, every GTC keynote
- Lisa Su (AMD) - data center strategy pivots
- 陈立武 (Intel新CEO) - turnaround signals
- Morris Chang / C.C. Wei (TSMC) - capacity and pricing (indirect via supply chain)

**Key Metrics to Track**:
- H100/B200/MI350/Xeon6 实际出货节奏
- CUDA vs ROCm vs OneAPI ecosystem health metrics (GitHub activity, enterprise adoption)
- Foundry allocation shifts (TSMC CoWoS capacity, Samsung yield recovery)

---

## Section 3: China Cloud Vendors AI Strategy
**Decision relevance**: Domestic compute demand, policy risk, alternative supply chain viability

**Tier-1 Sources**:
- 公司官方财报电话会 (Alibaba, Tencent, Baidu, ByteDance if available)
- 36kr Pro / 晚点LatePost (selective, only verified reporting)
- 中信证券/中金公司 TMT 研报 (Chinese sell-side with access)
- 工信部/发改委政策文件 (subsidies, procurement directives)
- DigiTimes China (supply chain visibility)

**Executive Intel**:
- 张勇/蔡崇信 (Alibaba) - AI capex commitment signals
- 马化腾 (Tencent) -混元大模型商业化进展
- 李彦宏 (Baidu) -文心一言企业 uptake
- 梁汝波 (ByteDance) -火山引擎/豆包 scaling

**Key Metrics**:
- DAU/MAU of 豆包/文心/通义 (actual vs claimed)
- 云业务AI收入占比 (Alibaba Cloud, Tencent Cloud)
- 国产GPU/ASIC adoption rate (Huawei Ascend, Biren, MetaX)

---

## Section 4: AI Agent Trends + Open Source Community
**Decision relevance**: Inference workload characteristics, edge AI silicon demand, developer ecosystem shifts

**Tier-1 Sources**:
- GitHub trending (star velocity, not absolute stars)
- LangChain/AutoGPT/MetaGPT official releases
- Hugging Face papers page (filter: agent architectures)
- a16z AI research blog (Andrew Ng, Martin Casado)
- Menlo Ventures "State of Generative AI" reports
- Sequoia / Greylock AI thesis updates

**Technical Signals**:
- MCP protocol adoption rate (GitHub repos, IDE integrations)
- A2A protocol traction
- Agent framework stars vs forks ratio (signal vs noise)
- On-device model deployment (Llama.cpp, mlx, Ollama) - edge silicon demand proxy

---

## Section 5: Agent Interface & Ecosystem Standardization
**Decision relevance**: Platform control points, API economy, middleware opportunities

**Tier-1 Sources**:
- Anthropic MCP spec commits / releases
- Google A2A protocol updates
- OpenAI API changelog (function calling, tool use evolution)
- CNCF / Linux Foundation AI working groups
- IEEE standards track (P3123 AI agent standards)

**Key Events**:
- Major vendor API strategy shifts (pricing, rate limits, new capabilities)
- Skill marketplace / plugin ecosystem traction
- Enterprise integration patterns (Salesforce, ServiceNow, SAP)

---

## Section 6: Global Economy - Financial Instruments & Trends
**Decision relevance**: Macro liquidity, risk appetite, cross-border capital flows, FX impact on semiconductor trade

**Tier-1 Sources**:
- Federal Reserve FOMC minutes + Powell press conference
- ECB / BoJ policy statements
- US Treasury 10Y/2Y spread (recession signal)
- DXY (dollar strength - impacts Asian semiconductor exporters)
- CFTC COT reports (speculative positioning in semis)
- BIS quarterly review (global liquidity)

**Institutional Research**:
- Bridgewater Daily Observations (if accessible)
- Goldman Sachs Global Macro Research
- JP Morgan Global FX Strategy
- Nomura (Asia FX and rates)

**Semiconductor-Specific Macro**:
- WSTS monthly semiconductor billings (leading indicator)
- SE quarterly forecast (industry body data)
- Gartner semiconductor capex forecast

---

## Section 7: Political News → Tech/Finance Impact
**Decision relevance**: Export control impacts, supply chain relocation costs, subsidy arbitrage, tariff exposure

**Tier-1 Sources**:
- US Department of Commerce BIS (entity list updates, rule changes)
- US Treasury OFAC (sanctions with tech nexus)
- Congressional Research Service (CRS) reports on CHIPS Act II
- CSIS (Center for Strategic and International Studies) - tech policy analysis
- RAND Corporation - geopolitical tech scenarios
- European Commission (Chips Act implementation, state aid notifications)
- 中国商务部/海关总署 (稀土/关键材料出口管制)

**Executive Intel**:
- Gina Raimondo (ex-Commerce) / successor statements on China tech policy
- 中国科技部长 / 工信部部长公开讲话
- TSMC / Samsung / Intel lobbying disclosures (FDI incentives)

**Key Triggers**:
- Entity list additions (especially GPU/cloud compute companies)
- Tariff rate changes (Section 301, EU digital tax)
- Subsidy program launches (CHIPS II, EU Chips Act, K-Chips)
- Critical material export controls (rare earths, neon, KrF photoresist)

---

## Section 8: Personalized Recommendation
**Decision relevance**: Non-obvious signals that may affect portfolio in 6-18 months

**Sources**:
- Nature / Science / IEEE (breakthrough with commercialization timeline)
- MIT Technology Review (annual 10 Breakthrough Technologies)
- a16z / Sequoia / Founders Fund thesis updates
- YC Demo Day themes (3-5 year forward indicator)
- Patent filings (USPTO, WIPO) - early tech direction signals
- Academic conference proceedings (ISSCC, VLSI, IEDM) - 5-year pipeline

**Selection Criteria**:
- Not widely reported in mainstream tech media yet
- Has identifiable commercialization path
- Could materially impact semiconductor demand or competitive dynamics
- User's feedback on previous recommendations incorporated

---

## Section 9: Global 15-24 Youth Behavior & App Landscape
**Decision relevance**: Product design intelligence for Gen Z/Z世代; platform investment theses; next-gen social/mobile monetization models

**Definition**: 15-24岁 = Gen Z core + young Gen Alpha overlap. Globally distinct from older cohorts in content consumption, social formation, and platform loyalty.

**Tier-1 Sources**:
- **Consulting**: Deloitte "Digital Media Trends" / "Gen Z and Media" annual reports; McKinsey "Consumer and Shopper Insights" Gen Z series; BCG Center for Customer Insight youth studies
- **Survey/Research**: Pew Research Center (US youth surveys); YouGov Global Profiles; Ipsos Global Advisor; Gallup "State of the Global Workplace" youth module
- **App Analytics**: data.ai (App Annie) State of Mobile reports; Sensor Tower QTR/annual; Comscore Digital Trends
- **Platform Official**: Snap Inc. "Snapchat Generation" reports; TikTok "What's Next" trend forecasts; Meta "Culture Rising" / Instagram youth insights; Spotify "Culture Next"; Twitch annual reports
- **Academic**: UNESCO Youth Report; OECD "Youth Aspirations" surveys; Journal of Computer-Mediated Communication
- **Financial/Investment**: Morgan Stanley "Teen Survey" (semiannual); Piper Sandler "Taking Stock With Teens"; Goldman Sachs "Millennials + Gen Z" consumer notes

**Tier-2 (Selective)**:
- eMarketer / Insider Intelligence (digital behavior forecasts)
- Kagan / S&P Global (media consumption)
- NPD / Circana (entertainment/consumer tracking)
- Ofcom (UK media regulator youth reports)

**Domestic Sources (20% cap, China-only)**:
- CNNIC (中国互联网络信息中心) youth internet usage reports
- QuestMobile (domestic app usage data)
- 腾讯/字节/阿里 official user insight reports (when disclosed in investor materials)

**Key Metrics to Track**:
- Monthly active users by app (15-24 cohort, regional breakdown)
- Time spent per app / session length / frequency
- Content format preference shift (short video vs long-form vs audio vs text)
- Social graph formation (close friends vs broadcast vs interest-based communities)
- Monetization model adoption (subscription vs ads vs tipping vs commerce)
- Platform migration signals (where are they leaving, where are they going)

**Output Standard for Section 9**:
> "Would this insight change how a product team prioritizes features for the 15-24 demographic?"

**Red Flags**:
- ❌ "年轻人喜欢..." without sample size / methodology / date
- ❌ Single-country data presented as global trend without qualification
- ❌ Platform self-reported metrics without third-party validation
- ❌ "据调研显示" without naming the research firm

---

## Quality Control Checklist (Pre-Publish)

#### Source Mix Verification:
- [ ] International sources ≥80% of total citations
- [ ] Domestic sources ≤20%, and ONLY for China-exclusive events
- [ ] No domestic tech media (36kr/钛媒体/etc.) used anywhere
- [ ] If international equivalent exists for a domestic source, swap it

### For Every Section (Sections 1-8):
- [ ] Information sourced within last 24 hours (`freshness: "day"` or `date_after: yesterday`)
- [ ] Key facts cross-verified from ≥2 independent sources
- [ ] No repetition of topics covered in last 3 days
- [ ] Contains at least one "so what" for semiconductor investment decision-making
- [ ] If citing executive statement, includes exact quote + context (where/when)
- [ ] If citing research report, includes firm name + analyst + date
- [ ] No "据知情人士" without named source or track record

### For Section 9 (Youth Behavior):
- [ ] Information sourced within last 24 hours
- [ ] Data cited from named research firm with sample size + methodology + date
- [ ] Global perspective (≥3 regions represented) unless explicitly China-focused
- [ ] Contains at least one "so what" for product design / platform investment decision
- [ ] No single-country data presented as global trend without qualification
- [ ] Platform metrics cross-verified with third-party analytics (data.ai, Sensor Tower, Comscore)

### Red Lines:
- ❌ No product launch rewrites without technical differentiation analysis
- ❌ No financial media "analysis" that just repeats headlines
- ❌ No content that could have been written by scanning TechCrunch for 10 minutes
- ❌ No generic "trend" statements without specific data points

### Output Standard:
> "Would this paragraph be worth mentioning in a Monday morning investment committee meeting?"
> If no, cut it or deepen it.

## Section 10: 著名投资人及权威机构最新论点
**Decision relevance**: 投资界大佬和权威机构对AI、能源（核聚变）、用户需求的最新原声观点，为估值模型和配置决策提供外部视角

### 覆盖主题
- **AI投资与估值**: AI capex是否过度、应用层何时产生回报、泡沫风险
- **能源（核聚变）**: 核聚变商业化时间线、AI算力对电力的结构性需求
- **用户需求演变**: 消费行为变迁、平台迁移、下一代人机交互

### Tier-1 Sources
- **a16z**: Marc Andreessen, Ben Horowitz — AI投资框架、技术趋势
- **Sequoia Capital**: AI公司估值、SaaS转型判断
- **Goldman Sachs TMT**: AI capex ROI、半导体周期、能源需求
- **Morgan Stanley Tech**: 云资本支出、AI应用层拐点
- **Bernstein Research**: 半导体供应链、Memory周期定位
- **BlackRock / Larry Fink**: 宏观资本流动、地缘风险定价、能源转型
- **Bridgewater / Ray Dalio**: 债务周期、货币政策、宏观拐点
- **CSIS / RAND**: 技术政策、出口管制对投资的影响
- **Gartner / IDC**: 技术采用曲线、IT支出预测
- **Nature / Science Editorial**: 科学突破的投资含义

### 能源/核聚变专项来源
- **Helion Energy / David Kirtley**: 核聚变商业化进展
- **Commonwealth Fusion / Bob Mumgaard**: 等离子体物理与工程突破
- **US DoE / Jennifer Granholm**: 政策与补贴方向
- **Bill Gates / TerraPower**: 核能复兴投资逻辑
- **Sam Altman (OpenAI/Helion投资人)**: AI+能源需求的结构性判断

### 内容格式 (强制)
每条论点必须包含：
```
**论点N: {主题一句话概括}**
> "{权威人士原话，尽量完整直接引语}" — {姓名}, {职位}, {场合/媒体}
来源: {媒体名称}, {日期}
投资含义: {一句话——对估值模型、配置权重、风险敞口的影响}
```

### 权威人士清单 (持续更新)
- **Marc Andreessen** (a16z co-founder): AI投资、技术乐观主义
- **Ray Dalio** (Bridgewater founder): 宏观周期、债务、地缘
- **Larry Fink** (BlackRock CEO): 资本配置、ESG、能源
- **Chamath Palihapitiya**: 科技估值、平台经济
- **Bill Ackman** (Pershing Square): 持仓观点、宏观事件
- **Howard Marks** (Oaktree): 周期定位、风险溢价
- **Jensen Huang** (NVIDIA CEO): AI算力需求、半导体周期
- **Lisa Su** (AMD CEO): 数据中心竞争格局
- **Sam Altman** (OpenAI CEO): AI基础设施、能源需求
- **Demis Hassabis** (DeepMind CEO): AGI时间线、科学AI
- **Satya Nadella** (Microsoft CEO): AI与企业整合
- **Lip-Bu Tan** (Intel CEO): 半导体制造、地缘供应链

---

## Voice/Commentary Sources (权威人士原声映射)

### AI/大模型领域
- **Sam Altman** (OpenAI CEO): 财报会议、参议院听证、博客、公开采访
- **Greg Brockman** (OpenAI President): 政策听证、技术演讲
- **Dario Amodei** (Anthropic CEO): AI安全、政策、公司战略
- **Demis Hassabis** (Google DeepMind CEO): AI能力边界、AGI时间线、科学应用
- **Sundar Pichai** (Google CEO): AI产品战略、搜索/云计算
- **Satya Nadella** (Microsoft CEO): AI与企业整合、Azure战略
- **Mira Murati** (Thinking Machines Lab): 模型训练、安全

### 芯片/半导体领域
- **Jensen Huang** (NVIDIA CEO): 财报会议、GTC keynote、行业会议
- **Lisa Su** (AMD CEO): 财报、技术发布会、ISSCC
- **Lip-Bu Tan / 陈立武** (Intel CEO): 财报、SIEPR、技术峰会
- **Mark Liu** (TSMC Chairman): 技术路线图、产能规划
- **Kwak Noh-Jung** (SK Hynix CEO): 内存市场、HBM战略
- **Sanjay Mehrotra** (Micron CEO): 存储周期、产能投资

### 投资/宏观领域
- **Marc Andreessen / Ben Horowitz** (a16z): AI投资框架、技术趋势
- **Ray Dalio** (Bridgewater): 宏观周期、地缘政治
- **Larry Fink** (BlackRock CEO): 资本配置、ESG、地缘风险
- **Chamath Palihapitiya**: 科技估值、SPAC/IPO
- **Bill Ackman** (Pershing Square): 持仓观点、宏观
- **Michael Burry**: 市场泡沫、尾部风险
- **Howard Marks** (Oaktree): 周期定位、风险溢价

### 能源/核聚变领域
- **David Kirtley** (Helion Energy CEO): 核聚变商业化时间线
- **Bob Mumgaard** (Commonwealth Fusion CEO): 等离子体物理进展
- **Sam Altman** (OpenAI/Helion投资人): AI+能源需求
- **Bill Gates** (TerraPower): 核能复兴
- **Jennifer Granholm** (US Energy Secretary): 政策与补贴

### 获取权威评论的方法
每条客观事件必须执行以下搜索：
1. `kimi_search("{人物名} latest comments {事件关键词} 2026")` 
2. `kimi_search("{人物名} interview {事件关键词} {日期}")`
3. 从财报会议transcript、 keynote演讲、参议院听证、Bloomberg/Reuters采访中提取直接引语
4. **格式**: `> "[原话]" — {姓名}, {职位}, 来源：{媒体}, {日期}`

---

## Quality Control Checklist (Pre-Publish)

#### Source Mix Verification:
- [ ] International sources ≥80% of total citations
- [ ] Domestic sources ≤20%, and ONLY for China-exclusive events
- [ ] No domestic tech media (36kr/钛媒体/etc.) used anywhere
- [ ] If international equivalent exists for a domestic source, swap it

### Authority Commentary Verification (新增强制项):
- [ ] 每条客观事件附带至少1条相关领域权威人士原声评论
- [ ] 评论格式: `> "[原话]" — {姓名}, {职位}, 来源：{媒体}, {日期}`
- [ ] 评论来源为Tier-1/2媒体，不接受二手解读
- [ ] Section 10 单独存在，不与其他板块合并

### For Every Section (Sections 1-10):
- [ ] Information sourced within last 24 hours (`freshness: "day"` or `date_after: yesterday`)
- [ ] Key facts cross-verified from ≥2 independent sources
- [ ] No repetition of topics covered in last 3 days
- [ ] Contains at least one "so what" for semiconductor investment decision-making
- [ ] If citing executive statement, includes exact quote + context (where/when)
- [ ] If citing research report, includes firm name + analyst + date
- [ ] No "据知情人士" without named source or track record

### For Section 9 (Youth Behavior):
- [ ] Information sourced within last 24 hours
- [ ] Data cited from named research firm with sample size + methodology + date
- [ ] Global perspective (≥3 regions represented) unless explicitly China-focused
- [ ] Contains at least one "so what" for product design / platform investment decision
- [ ] No single-country data presented as global trend without qualification
- [ ] Platform metrics cross-verified with third-party analytics (data.ai, Sensor Tower, Comscore)

### For Section 10 (Investor & Authority Views):
- [ ] 每条论点包含: 主题概括 + 原声引语 + 来源媒体+日期 + 投资含义
- [ ] 覆盖AI/能源/用户需求至少2个主题
- [ ] 引用人物为知名投资人、机构分析师或行业CEO级别
- [ ] 不接受二手评论或媒体解读替代原声
- [ ] 日期为最近7天内，优先24小时内

### Red Lines:
- ❌ No product launch rewrites without technical differentiation analysis
- ❌ No financial media "analysis" that just repeats headlines
- ❌ No content that could have been written by scanning TechCrunch for 10 minutes
- ❌ No generic "trend" statements without specific data points
- ❌ **NEW**: No event without authority commentary attached
- ❌ **NEW**: No Section 10 content mixed into other sections

### Output Standard:
> "Would this paragraph be worth mentioning in a Monday morning investment committee meeting?"
> If no, cut it or deepen it.

## Section 11: 因果链分析 & 投资预测
**Decision relevance**: 将10个独立板块编织为因果网络，识别跨板块传导的投资信号，输出可验证的预测并推荐标的

### 核心方法论
**因果链不是相关性罗列**。每日必须识别至少1条清晰的因果传导路径：
- **触发因（Trigger）**: 板块X的什么信号是"第一推动力"
- **传导机制（Mechanism）**: 为什么板块Y会因此变化（物理/经济/政策逻辑）
- **时间尺度（Timeline）**: 传导是即时（当日）、短期（1-4周）、还是中期（1-6个月）
- **可证伪性（Falsifiability）**: 什么信号出现会证明这条因果链错误

### 主要传导路径框架（非穷尽，每日根据事件动态选择）

**路径A：政策/地缘 → 供应链 → 算力 → 应用**
```
政治突发(6) → 出口管制/关税 → 芯片供应(2) → 云capex调整(3) → AI模型迭代节奏(1) → Agent应用落地(4/8)
```

**路径B：技术突破 → 算力需求 → 半导体周期 → 估值重估**
```
AI模型突破(1) → 推理/训练需求↑ → 芯片订单↑(2) → 设备/材料需求↑(5) → 云厂商采购↑(3) → 投资人重新定价(10)
```

**路径C：半导体周期 → 财报信号 → capex可持续性 → 泡沫/结构性争论**
```
Memory价格(5) → 芯片公司毛利率(2) → 财报指引 → AI capex ROI辩论(1/3/10) → 估值multiple压缩/扩张
```

**路径D：Gen Z行为 → 平台经济 → 算力需求结构 → 芯片设计优先级**
```
Gen Z平台迁移(9) → 内容/电商/社交模式变革 → 推荐算法算力需求变化 → 推理优化芯片优先级(2/8) → 边缘AI需求
```

**路径E：能源/核聚变 → 算力基础设施 → 电网投资 → 地缘博弈**
```
核聚变进展(10) → 电力成本长期预期 → 数据中心选址策略(3) → 主权AI基础设施投资(6) → 芯片供应链区域化(2)
```

### 输出格式（强制）
```
**【11】因果链分析 & 投资预测**

**因果链 {N}: {一句话概括触发因→结果}**
- **触发因**: {板块X具体信号，附日期和来源}
- **传导机制**: {为什么X导致Y，用一句话经济/物理/政策逻辑解释}
- **时间尺度**: {即时/短期/中期}
- **投资预测**: {具体到"如果X持续，Y将在Z时间内发生W变化"}
- **证伪信号**: {什么事件出现会否定此预测}
- **推荐标的**: 
  - {公司名称} ({TICKER}): {一句话投资逻辑，必须与因果链直接关联}
  - {可选第二家}

**因果链 {N+1}: {第二条因果链，如当日无第二条则省略}**
...
```

### 高价值公司推荐池（持续更新）
以下标的在因果链分析中可被引用，但**仅在因果链直接关联时才推荐**，禁止无关联硬推：

**芯片设计/计算**
- **NVIDIA (NVDA)**: AI GPU垄断地位，Blackwell/Rubin roadmap，推理优化架构
- **AMD (AMD)**: MI350/Zen6 Venice挑战者，性价比策略，x86+GPU双引擎
- **Broadcom (AVGO)**: 定制ASIC (XPU)之王，Google TPU/Meta/Anthropic订单，$100B+ AI收入目标
- **Qualcomm (QCOM)**: Snapdragon X Elite/Orion PC芯片，移动+汽车+IoT边缘AI
- **Intel (INTC)**: 18A turnaround高赔率，foundry服务叙事，最高风险/最高回报

**代工/制造**
- **TSMC (TSM)**: 全球先进制程90%份额，2nm 2026H2量产，HPC占收入61%，23x forward PE vs NVDA 25x
- **Samsung Electronics (005930.KRX)**: HBM追赶者，3nm GAA yield recovery，内存+NAND一体化

**Memory**
- **SK Hynix (000660.KRX)**: HBM市场~50%份额，HBM4 2026H2量产，NVIDIA Rubin核心供应商
- **Micron Technology (MU)**: HBM3E三强之一，eSSD AI服务器存储，长期合约锁定价格

**设备/材料**
- **Lam Research (LRCX)**: 刻蚀设备垄断，HBM堆叠工艺直接受益者，double-digit WFE增长
- **KLA (KLAC)**: 过程控制/检测设备，先进节点yield管理刚需，设备中最稳定的毛利率
- **ASML (ASML)**: EUV光刻机垄断，High-NA EUV 2026-2027交付，芯片制造的"瓶颈中的瓶颈"
- **Applied Materials (AMAT)**: BIS $252M罚款暴露的地缘风险，但设备广度不可替代
- **Cadence (CDNS) / Synopsys (SNPS)**: EDA工具，AI chip设计复杂度↑→EDA需求↑

**网络/互联**
- **Marvell Technology (MRVL)**: 定制芯片+光互连，CPO (co-packaged optics)先行者
- **Coherent (COHR)**: 激光/光器件，硅光/CPO供应链关键节点

**核聚变（间接/嵌入式 exposure）**
- **Alphabet (GOOGL)**: CFS $200MW PPA + 股权投资，fusion as embedded call option
- **Microsoft (MSFT)**: Helion Energy 50MW PPA (2028)，AI数据中心电力需求直接关联
- **Cameco (CCJ)**: 铀矿龙头，nuclear renaissance + 潜在tritium燃料链上游
- **Constellation Energy (CEG)**: 美国最大核电运营商，Microsoft/Helion PPA电力营销方
- **General Electric Vernova (GEV)**: 燃气轮机+电网设备，数据中心电力基础设施

**中国标的（仅限因果链涉及中国市场时使用）**
- **Alibaba (BABA/9988.HK)**: 云+AI，Qwen开源生态，AI收入增速
- **Tencent (0700.HK)**: 混元大模型+微信生态，游戏AI应用
- **Baidu (BIDU)**: 文心一言企业 uptake，自动驾驶Apollo
- **SMIC (0981.HK)**: 国产替代叙事，7nm良率爬坡，设备国产化率

### 推荐标的引用规则
- **禁止无因果链关联的标的推荐**: 不能某天突然说"推荐买入NVDA"而不解释与当日事件的因果联系
- **必须说明时间尺度**: "短期（1-4周）"、"中期（1-6个月）"、"结构性（6个月+）"
- **必须说明证伪条件**: "如果X不发生，此逻辑失效"
- **来源要求**: 推荐标的必须有 sell-side research (Bernstein/MS/GS) 或 公司IR数据支撑，不接受纯技术面推荐

---

## 半月复盘方法论
**触发频率**: 每月1号和16号（即每半月一次）
**输出时间**: 与每日晨报相同（8:07 AM）
**内容形式**: 与每日晨报相同的11板块结构，但更加精炼

### 复盘核心任务
1. **因果链验证/证伪**: 回顾过去15天内每日晨报中的因果链预测，标注哪些被验证、哪些被证伪、哪些尚无定论
2. **预测修正**: 基于新信息修正投资判断，明确"此前预测A→B，现因X信号修正为A→C"
3. **新因果链假设**: 基于半月累积信息，提出新的跨板块传导假设
4. **标的跟踪**: 半月内推荐的标的表现回顾，是否需要调整仓位逻辑
5. **精炼原则**: 每个板块只保留最核心的1-2条信号，剔除已过期/已验证的信息

### 复盘输出格式
```
**半月复盘 | {日期范围}**

**一、因果链验证/证伪**
- [验证] 因果链X（{日期}预测）: {实际发生了什么} → {对投资判断的影响}
- [证伪] 因果链Y（{日期}预测）: {实际与预测相反} → {修正判断}
- [待观察] 因果链Z（{日期}预测）: {尚无定论，需继续跟踪的信号}

**二、修正后的核心投资判断**
{1-3句话，概括半月后最坚定的投资逻辑}

**三、新因果链假设**
- {基于半月累积信息的新假设}

**四、标的跟踪**
- {公司} ({TICKER}): {半月表现简述，逻辑是否仍然成立}

**五、精炼版11板块**
{每个板块1-2条核心信号，不再展开细节，只保留结论}
```

### 复盘与每日晨报的区别
| 维度 | 每日晨报 | 半月复盘 |
|------|---------|---------|
| 信息密度 | 每板块2-4条详细信号 | 每板块1-2条精炼结论 |
| 因果链 | 当日即时传导分析 | 15天累积验证+修正 |
| 预测 | 即时/短期 | 中期/结构性 |
| 标的推荐 | 与当日事件关联 | 半月逻辑一致的高确信标的 |
| 权威评论 | 每条事件附评论 | 只保留最关键的3-5条大佬原声 |
| 篇幅 | 完整详实 | 精炼压缩50% |

---

## Content Freshness & Accuracy Enforcement (Added 2026-05-12)

### 过时信息拦截规则
以下信息类型必须经过时效性判断，超期信息视为"背景"而非"新闻"：

| 信息类型 | 新鲜期 | 超期处理 |
|----------|--------|----------|
| 产品发布 | 30天 | 需有新功能/新数据/新版本才能跟进收录 |
| 模型发布 | 14天 | 需有更新版本/新benchmark/新应用才能收录 |
| 财报数据 | 最新季度 | 禁止使用上一季度数据填充，无新财报则标注"等待Q{下一季度}" |
| 政策/法规 | 最新变动 | 已生效政策的重复报道不收录，仅收录新变动/新解读 |
| 股价/价格 | 当日/昨日 | 必须标注日期和来源，禁止使用无日期价格 |
| 人物言论 | 30天 | 超过30天的言论需有新上下文/新事件关联才能引用 |

### 事实验证强制清单
每生成一条信息前，必须回答：
1. **这是什么？** — 具体事件/数据/发布
2. **何时发生？** — 精确日期，与官方渠道核对
3. **来源是谁？** — Tier 1/2来源，具名信源
4. **交叉验证？** — ≥2个独立来源确认
5. **so what？** — 这会改变什么投资决策？
6. **近7日是否已覆盖？** — 读取daily_topics_log.md确认

### 错误追溯记录
- **文件**: `/root/.openclaw/workspace/memory/accuracy_errors.md`
- **触发**: 用户指出过时/不准确信息时立即记录
- **格式**: 错误描述 → 板块 → 根因 → 修正措施 → 状态
- **复盘**: 每周回顾，识别系统性错误模式，更新本文件

### 去重与Topic追踪
- **日志文件**: `/root/.openclaw/workspace/memory/daily_topics_log.md`
- **更新**: 每日晨报生成后自动追加
- **使用**: 生成新晨报前读取，避免近3日重复，近4-7日仅新进展跟进
- **格式**: `YYYY-MM-DD | 板块 | Topic关键词 | 来源 | 投资含义摘要`

### 问责机制
- **核心原则**: 宁可一个板块标注"当日无重大投资信号"，也不推送过时或不准确信息
- **自检不通过**: 直接在输出中标注"本板块因信息不足暂缓推送"，禁止用旧信息填充
- **用户反馈**: 用户指出错误 → 立即记录到accuracy_errors.md → 追溯根因 → 修正机制 → 确认闭环

---

## Source Map Version History
- **2026-04-28**: Initial source map with 8 sections, source tiers, 80/20 policy
- **2026-04-28**: Added Section 9 (Gen Z), voice/commentary sources
- **2026-05-10**: Added Section 11 (Causal Chain Analysis), biweekly review framework
- **2026-05-11**: Added Section 10 (Investor & Authority Views), authority commentary requirements
- **2026-05-12**: Added Content Freshness & Accuracy Enforcement Protocol, stale content blocking rules, fact verification checklist, deduplication system, error tracking
- **2026-05-13**: Added Stock Data Acquisition Policy — 100% ifind API for prices, intraday change only, no search backfill, API failure = halt

---

## Stock Data Acquisition Policy (Added 2026-05-13)
**Scope**: Section 1 (核心持仓实时行情) — 21只股票的价格与变动数据

### 强制规则
1. **价格（Price）**: 100%来自 ifind API `realtime_price` 的 `close` 字段。任何一只股票API调用失败→该股票标注"价格暂缺"，**绝对禁止**搜索引擎回填股价。
2. **变动（Change）**: ifind API的`pct_change_1m`是1分钟涨跌幅（≈0%，无意义），**禁止直接使用**。改用API返回的`open`和`close`计算日内涨跌幅：`(close - open) / open × 100%`。此数值完全来自API，不依赖外部搜索。
3. **YTD/年初至今**: ifind API不直接提供YTD数据。**禁止**在股票卡片中硬编码YTD数字。YTD信息如需显示，必须通过搜索获取并标注"来源：Yahoo Finance/Bloomberg，日期"，且需与至少1个额外来源交叉验证。
4. **数据日期**: 所有股票价格必须标注`数据日期: YYYY-MM-DD`（API查询日期）。禁止显示无日期价格。

### 验证脚本（每日生成前执行）
```
1. 调用 kimi_finance(realtime_price) 获取全部20只股票收盘价
2. 检查每只股票的 close 是否为有效数字（>0，非null）
3. 任一股票失败 → 中止Section 1生成，标注"API数据暂缺"
4. 计算日内涨跌幅：(close - open) / open × 100%
5. 写入 stock_data_YYYY-MM-DD.csv（本地留存，便于追溯）
6. HTML模板从CSV读取数据填充，禁止搜索回填
```

### 错误案例（2026-05-13 INTC）
- **错误**: INTC显示$24.50，真实$120.60
- **根因**: ifind API调用可能遗漏INTC，子代理回退搜索引擎，搜索返回2024年底旧价格
- **后果**: 价格差约5倍，投资决策级错误
- **修正**: 从此规则生效，任何API失败→中止/告警，禁止搜索回填

### 问责
- 违反上述规则→记录到accuracy_errors.md
- 连续2次股票数据错误→暂停cron自动生成，改为手动验证后推送
