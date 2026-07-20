# PPT 架构页内容：数据层三阶记忆子架构（v2.0）

> **用途**：可直接填入商业版/技术版 PPT 的架构页（Slides 8–11 区域）
> **来源**：[08-数据层修订-三阶记忆子架构](08-%E6%95%B0%E6%8D%AE%E5%B1%82%E4%BF%AE%E8%AE%A2-%E4%B8%89%E9%98%B6%E8%AE%B0%E5%BF%86%E5%AD%90%E6%9E%B6%E6%9E%84.md) · [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) §3quater
> **适配**：中英文对照，保留技术术语，商业版取中文为主、英文括号标注；技术版可全英文

---

## Slide A: 数据层总览 — 三阶记忆子架构

**标题**：AI Native Data: A Three-Tier Memory Subsystem for Enterprise Agents
**副标题**：数据层 v2.0 — 从原始存储到语义索引到经验沉淀

**正文框（左半）**：

```
┌─────────────────────────────────────────────────────────┐
│  Tier 3 · Data Theme（数据主题）                        │
│  ── 自顶向下的经验沉淀层                                 │
│  • 记录“数据被怎么用”：who/what/when/where/why/how        │
│  • Theme 继承/演化/版本化：同类用例直接复用取数路径      │
│  • 对接企业 Semantic Layer（指标定义、口径治理）          │
│  → 控制面：纯决策，不搬运数据                             │
├─────────────────────────────────────────────────────────┤
│  Tier 2 · Index & Link（语义索引）                        │
│  ── 自底向上的语义编译层                                 │
│  • OPIC 离线 agent 集群：持续读取 Raw Data → 提取 facts   │
│  • 5W1H + Which 结构化事实：What/Who/Where/When/Why/How   │
│  • 交叉链接：时间关联、因果链、语义相似、血缘、访问域    │
│  → 生产侧：独立离线 loop；消费侧：semantic join 查询接口 │
├─────────────────────────────────────────────────────────┤
│  Tier 1 · Raw Data（原始数据）                           │
│  ── 物理着陆层，对接 Lakehouse                           │
│  • 原始文件 / 数据库视图 / 报表 / Agent 推理轨迹           │
│  • Schema-on-read：保留 latent 字段，不人为截断          │
│  • 通过 Catalog 逻辑注册，对齐企业权限与审计体系         │
│  → 数据面：on-policy 切片读取（D₁）                       │
└─────────────────────────────────────────────────────────┘
```

**正文框（右半）**：

| 原四接口 | 三阶记忆映射 | 平面归属 |
|---------|-------------|---------|
| D₁ 取数 API | Tier 1 的在线访问接口 | 运行时 DP |
| D₂ 语义总结 | Tier 2 的 OPIC 生产引擎 + 查询接口 | 生产：离线面；消费：DP |
| D₃ 治理 memory | Tier 3 的 Theme 生成器 | 运行时 CP |
| D₄ lifetime | 跨 Tier 1+3 的时效与口径管理 | 运行时 CP |

**底部高亮**：
💡 **双螺旋闭环**：Index（数据告诉你它是什么）↔ Theme（组织告诉数据它意味着什么）—— 每次数据使用反馈给索引，索引进化又支撑更精准的 Theme 复用。

---

## Slide B: Tier 1 · Raw Data — 原始数据湖

**标题**：Tier 1: Raw Data — The Physical Landing Layer
**副标题**：不解释含义，只保证可用、完整、可审计

**正文**：

**企业级 Lakehouse 对接**
- Object Store（S3/OSS/GCS）：原始文件仓，冷热分层
- Table Format（Iceberg / Delta / Hudi）：结构化数据视图，ACID + 时间旅行
- Catalog（Polaris / Unity）：统一命名空间，跨引擎访问
- Streaming（Kafka / Flink）：CDC 与实时入湖

**Raw Data 层的五类原始信息**
1. 原始文件：PDF、Excel、Word、扫描件、音视频转录
2. 数据库连接/视图：ERP / SCM / CRM / SAP / 飞书多维表格
3. 报表与 Dashboard 快照：BI 系统定时导出
4. Agent 推理轨迹：thinking chain、tool call 日志、反思记录、中间产物
5. 外部流数据：API 响应、事件流、IoT 遥测

**核心原则**：Schema-on-read → 原始信息的 latent 结构被完整保留，不因人为建模而截断

> **Karpathy LLM Wiki 的 raw/ 层**：个人知识管理的 "immutable source dump"。企业级 Raw Data 层是其工业规模放大——保留"原始信息不可变"原则，但引入 Lakehouse 的 ACID、分区、Catalog 治理。

---

## Slide C: Tier 2 · Index & Link — 5W1H+Which 语义索引

**标题**：Tier 2: Index & Link — Semantic Compilation by Off-Policy Agents
**副标题**：离线 agent 集群自底向上提取结构化事实，建立交叉关联

**正文（左半：5W1H+Which 本体）**：

| 维度 | 字段 | 说明 |
|------|------|------|
| **What** | fact_type | 人物、事件、报告、会议梗概、代码、工具、数据表元数据 |
| **Who** | producers / consumers / excluded | 谁产生的、给谁看、不给谁看 |
| **Where** | raw_sources / upstream_indices / access_boundary | 来源 Raw Data、上游 Index、访问边界（互联网/内网/SAP/飞书） |
| **When** | created / modified / valid_until / obsoleted | 产生、修改、作废时间线 |
| **Why** | causality_chain / triggered_by / next_steps / later_outcomes | 前因后果：触发原因、后续动作、结果反馈 |
| **How** | content_digest / key_list / short_narrative | 内容展开：列表或短叙事 |
| **Which** | temporal_links / cross_refs | 时效段内的关联：时间/因果/语义/血缘/域内链接 |

**正文（右半：链接机制）**：

**Which 维度的五种关联**
- **时间关联**：同一 `when` 窗口内的事实 → 共时链接
- **因果关联**：`why` 中的 triggered_by / next_steps → 因果链
- **语义关联**：`what` + `how` 经 embedding → 相似链接
- **访问关联**：`where` 的 access_boundary 相同 → 域内链接
- **血缘关联**：数据表 FK/PK/ETL 依赖 → 血缘链接

> **OPIC 集群**：Off-Policy Indexing Cluster — 独立 loop、自带 sub-agents、甚至专用模型，类比搜索引擎的爬虫与索引构建。与主 agent 运行时完全异步解耦。

---

## Slide D: Tier 3 · Data Theme — 数据主题与经验记忆

**标题**：Tier 3: Data Theme — Top-Down Experience Memory
**副标题**：把“数据被怎么用”固化为可复用的组织记忆

**正文**：

**Data Theme 的 5W1H 记录**

| 维度 | 示例（Q2 华东区营收分析） |
|------|------------------------|
| **What** | 主题：Q2 华东区营收分析；意图：多表关联 + 时序对比；输出：带图表的 Markdown 报告 |
| **Who** | Agent: financial-analyst-v3；用户：财务总监；受众：管理层周报 |
| **Where** | 数据源：sales_order (D₁) + revenue_summary (Tier 2)；导航路径：华东区 region_dim → 时间筛选 → 关联订单表；工具：SQL 生成、PyPlot、飞书推送 |
| **When** | 查询：2026-06-30 09:00；数据截止：2026-06-28；要求 T+1 |
| **Why** | 问题：Q2 华东是否达标？背景：季度经营分析会；行动：若未达标则触发 #456 成本审计 |
| **How** | 策略：先查 Tier 2 Index 定位口径，再经 D₁ 拉原始明细；关联：sales_order ⋈ region_dim ⋈ product_dim；回退：若华东口径 2024 后变更，自动切换至新口径视图 |

**Theme 的复用与收敛**
1. **匹配**：新请求按 `what` + `who` + `where` 匹配历史 Theme
2. **继承**：命中近似 Theme → 继承 `how`（检索策略）和 `where`（导航路径），微调 `when`/`why`
3. **演化**：执行中发现新数据源或新关联 → 更新 Theme 并标记版本
4. **废弃**：数据口径失效或源下线 → 标记 `stale`，触发 OPIC 重新索引

> **与 P9（治理记忆收敛）对应**：重复同类 use case，Theme 命中率 ↑，决策熵 ℋ ↓，取数从“探索”转化为“利用”。

---

## Slide E: 双螺旋闭环与平面切分

**标题**：The Double-Helix Loop: Index ↔ Theme
**副标题**：自底向上索引 + 自顶向下经验 = 数据认知的飞轮

**正文（上半：双螺旋图示）**：

```
         ┌──────────┐
         │  Raw Data │  ← 物理着陆（Tier 1）
         └────┬─────┘
              │  OPIC 读取
              ▼
         ┌──────────┐
    ┌────│  Index   │────┐  ← 自底向上：5W1H+Which 事实提取（Tier 2）
    │    └──────────┘    │
    │         ↑           │
    │    feedback         │
    │    （使用频次→索引   │
    │     优先级提升）    │
    │         ↓           │
    │    ┌──────────┐    │
    └────│  Theme   │────┘  ← 自顶向下：经验沉淀与复用（Tier 3）
         └──────────┘
              │
              ▼
         Agent Use Case
```

**正文（下半：平面切分）**：

| 三阶记忆 | 生产侧 | 消费侧 | 平面归属 |
|---------|--------|--------|---------|
| **Tier 1 Raw** | 数据入湖、CDC、分区管理（运维） | on-policy 切片读取（D₁） | 生产：运维面；消费：运行时 DP |
| **Tier 2 Index** | OPIC 离线 agent 集群（独立进程） | semantic join 查询接口 | 生产：独立离线面；消费：运行时 DP |
| **Tier 3 Theme** | Theme 沉淀、匹配、演化（低频事件） | Theme 查询、复用、继承 | 纯运行时 CP |

> **关键观察**：Theme 是纯控制面——决定“怎么取数”，但不搬运数据。Theme 复杂度增长不污染数据面 token 成本，直接支持 P4（平面分离）。

---

## Slide F: 与三层栈的映射 — 数据子系统接入 Harness

**标题**：Data Subsystem Integration: How ℳ = ⟨Raw, Index, Theme⟩ Maps to ⟨S, H, X⟩
**副标题**：数据层经 Harness 契约 H 接入三层栈

**正文**：

**契约映射链**

```
Intent (ℐ) ──consult Theme──→ Plan ──Index──→ Locate Facts ──Raw──→ Execution (ℰ)
               (Tier 3, CP)      (Tier 2, DP)      (Tier 1, DP)
```

**三层栈 × 数据层对照**

| 三层栈层级 | 数据层角色 | 交互方式 |
|-----------|-----------|---------|
| **L3 Skills** | 定义数据需求（what 指标、what 口径、what 输出格式） | 通过 H 的 intent 传入 |
| **L2 Harness** | 执行契约翻译：Intent → consult Theme → plan → semantic join → D₁ 取数 | H 直接调用 D₁/D₂ 查询接口 + 查询 D₃/D₄ API |
| **L1 Scaffold** | 提供执行隔离环境：D₁ 的 SQL 查询在 sandbox 内执行、结果安全返回 | 数据面执行 |

**扩展语义**
- **+Raw Data Source** → 数据维扩展（同构于物理扩展 Θ↑），P7 保证单请求成本不变
- **+Index Fact** → 语义覆盖扩大，不污染运行时（OPIC 离线生产）
- **+Theme** → 经验沉淀积累，控制面决策空间扩大，但数据面成本不变（P4 支持）

> **一句话**：数据层不是第四层，而是**略独立于三层栈的 memory substrate**——它通过 Harness 契约接入，但拥有自己的三阶存储空间、自己的离线生产 loop、自己的经验沉淀机制。

---

## Slide G: 数据层的四项 Novelty（可选，放在技术版或附录）

**标题**：Data Layer v2.0: Four Independent Contributions

| # | Novelty | 一句话 | 对标现有工作 |
|---|---------|--------|------------|
| **N1** | 5W1H+Which 企业数据事实本体 | 将新闻学/情报学 5W1H 扩展为“Which”关联维度，泛化到一切企业数据单元 | XPEventCore 仅事件；SoKG 仅文档；均无 Which 维度 |
| **N2** | 双螺旋记忆（Index ↔ Theme） | 自底向上索引 + 自顶向下经验沉淀，闭环反馈 | MemGPT/Letta 仅 agent 自身记忆；Lakehouse Semantic Layer 仅人的治理产物 |
| **N3** | Theme 收敛机制 | 数据使用经验固化为可继承、可版本化的 Theme，取数从探索→利用 | 数据治理（DataGovBench）仅管边界，不沉淀 agent 使用经验 |
| **N4** | 三阶记忆与 CP/DP 第三次正交切分 | Raw↔运维面/DP、Index↔离线面/DP、Theme↔CP，复用同一平面不变量 | 无 |

---

## Slide H: 可证伪实验设计（可选，技术版/附录）

**标题**：How to Validate the Three-Tier Memory Subsystem

| 命题 | 实验设计 | 自变量 | 因变量 | 通过判据 |
|------|---------|--------|--------|---------|
| **P10** 索引充分性 | 四臂对比（裸扫描 / 人工元数据 / 无结构摘要 / 5W1H+Which） | 取数方式 | precision / recall / last-mile 成功率 / token 成本 | (d) precision≈(b) 且 coverage≈(a) 且 cost<(c) |
| **P11** Theme 收敛 | 重复同类 use case n=1..50 | 重复次数 n | Theme 命中率 / 决策熵 ℋ / 成本方差 | 命中率↑、熵↓、方差→0 |
| **P12** 双螺旋增益 | 三臂对比（仅 Raw / Raw+Index / Raw+Index+Theme） | 记忆层级 | 复杂 use case 成功率 / token 成本 / 耗时 | (c) > (b) > (a) |
| **P7** 取数解耦 | 固定 use case，数据源数 1→N | \|src\| | 单请求 token 成本 ℓ | ℓ 基本不随 \|src\| 上升 |
| **P8** 语义摘要充分性 | 三臂对比（裸发现 / 人工元数据 / off-policy Σ） | 取数方式 | precision / recall / last-mile / cost | (c) precision≈(b) 且 coverage≈(a) |
| **P9** 治理收敛 | 重复同类 use case n 次 | n | 决策熵 ℋ(π_data)、成本方差 | 熵与方差随 n 单调不增 |

---

## 使用建议

- **商业版（3 Layer Scalable AI）**：Slides A–D 为核心，Slide E 可选，Slide F 映射到 "AI Native Data" 标题页。每页控制在 5–6 个 bullet points，配合图示。
- **技术版（agentic-runtime-zh）**：Slides A–H 全用，作为 "数据子系统 𝒟" 的完整展开（6–8 页）。建议放在现有 Slide 2（每层规格）和 Slide 3（工作循环）之间，作为独立的数据层专题。
- **字体**：中文用思源黑体 / 微软雅黑，英文用 Inter；颜色建议：Tier 1（深蓝 #1A5276）、Tier 2（青绿 #1ABC9C）、Tier 3（紫色 #9B59B6）。
