# Harness Memory 子系统 — 显隐双轨设计

> **来源**: 2026-08-17 用户原话整理
> **类型**: 架构功能清单（Harness 层 memory 子系统）
> **状态**: 草稿 v0.1 -> v0.2（待定问题决议）-> v0.3（用户决议修订：archive 外放/SQLite 除重/哈希索引/小模型=内置 API）-> **v0.4（2026-08-17）**：新增 §2.3--5W1H+Which 七维作为 Memory 基本知识维度
> **定位**: Harness 层 memory 的功能定义，对 [[06-数据平面四组成架构]] D₂/D₃ 接口和 [[08-数据层修订-三阶记忆子架构]] Tier 2/3 的进一步细化，聚焦"agent 可见 vs 系统管理"的显隐二分。
> **关联**: [[06-数据平面四组成架构]] | [[08-数据层修订-三阶记忆子架构]] | [[精读-2606.24775-Agent-Native-Memory-System]] | [[05-控制面与数据面正交切分]] | [[10-Skill-as-Code与确定性固化]]

---

## 0. 核心定位

Memory 是 **Harness 层**的子系统，独立于 LLM 参数权重，位于 agent 侧。它不是 LLM 的 context window（那是瞬时的），而是**持久化、可查询、可共享的 agent 状态基础设施**。

> 关键边界：Memory 属于 Harness，不属于 Skill（Skill 只声明数据需求，不拥有 memory），也不属于 Scaffold（Scaffold 只执行物理存储约束，不做语义管理）。

---

## 1. 显隐双轨架构

### 1.1 显性 Memory（Agent-Visible Memory）

Agent 可以直接看到、通过 API 接口访问的 memory 层。

#### 1.1.1 组织维度

| 维度 | 说明 | 示例 |
|------|------|------|
| **时间线 (Timeline)** | 按 agent context 的时序排列，记录每次交互的完整生命周期 | Session 1 → Turn 3 → Step 5 |
| **角色 (Role)** | 区分不同来源的输入和产出 | User / LLM / Tool Call / Skill Call |
| **内容类型 (Content Type)** | 区分交互阶段和性质 | 输入 / 中间态 / Log / 输出 / Error |
| **对话总结 (Conversation Summary)** | 对对话进行压缩式总结，保留语义要点 | "用户问了X，LLM调用了Y工具，结果Z" |

> 以上四维是 5W1H+Which 七维本体的子集（对应 When / Who / What / How），完整七维知识维度体系见 §2.3。

#### 1.1.2 角色定义

| 角色 | 产生的内容 | 记录格式 |
|------|-----------|----------|
| **User** | 自然语言输入、意图声明、反馈 | 原文 + 意图标注 |
| **LLM** | 推理过程、决策、生成内容 | thinking chain + 输出 + token 计量 |
| **Tool Call** | 工具调用参数、返回结果、执行状态 | call spec + result + latency + status |
| **Skill Call** | 技能激活、合约解析、版本信息 | contract ID + resolved graph + version |

#### 1.1.3 显性 Memory 的 API 接口

```
# 查询接口
memory.query(timeline=<range>, role=<role>, topic=<topic>) → MemoryRecords
memory.summarize(scope=<session|turn|topic>) → Summary
memory.search(semantic_query=<text>) → RankedResults

# 写入接口（由 Harness 在 agent 执行过程中自动调用）
memory.append(role=<role>, content_type=<type>, payload=<data>, context=<ctx>)
memory.log(event=<event>, metadata=<meta>)

# 总结接口
memory.consolidate(scope=<scope>, strategy=<timeline|role|topic>)
```

### 1.2 隐性 Memory（System-Managed Memory）

Agent 不可直接访问，由 Harness 系统管理层维护的配置和部署信息。

| 组件 | 说明 | 管理方 |
|------|------|--------|
| **Tool/API 调用配置** | 端点地址、认证方式、超时、重试策略、限流参数 | Harness 部署配置 |
| **Context 压缩配置** | 压缩触发阈值、压缩策略（摘要/截断/选择性保留）、压缩模型选择 | Harness 运行时管理 |
| **Memory 存储后端配置** | 存储引擎选择（File/DB/向量库）、分区策略、保留策略 | Harness 基础设施层 |
| **多模态压缩模型配置** | 专用小模型的模型选择、推理参数、调用频率 | Harness 系统服务 |

> 设计原则：隐性 Memory 的变更不需要 agent 知晓——agent 只消费显性 Memory 的查询结果，不感知底层存储和压缩策略的变化。这正是 [[05-控制面与数据面正交切分]] 中"控制面决策不涌入数据面 token 流量"的体现。

---

## 2. Memory 管理操作

### 2.1 查询

| 查询模式 | 说明 | 使用场景 |
|----------|------|----------|
| **按时间线查询** | 指定时间范围，返回该区间内所有角色的记录 | 回顾历史、审计追踪 |
| **按角色查询** | 指定角色（User/LLM/Tool/Skill），返回该角色的所有记录 | 分析工具调用效果、审查 LLM 推理 |
| **按主题整理** | 语义聚类查询，跨时间线和角色提取相关记录 | 跨会话知识沉淀、主题深度分析 |

### 2.2 总结与合并

- **对话总结**: 按时间线对对话进行压缩，保留语义要点
- **角色交叉总结**: 对比不同角色在相同时间段的输入输出，提取协作模式
- **主题合并**: 跨多个会话提取同一主题的累积认知

### 2.3 5W1H+Which：Memory 的基本知识维度（2026-08-17 新增）

**主张：用 5W1H+Which 七维叙事本体（[[08-数据层修订-三阶记忆子架构]] Tier 2 / EMNLP 5W1H+Which 论文）作为显性 Memory 记录的基本知识维度，统一索引与管理 memory 内容。**

**动机**：现有组织维度（时间线/角色/内容类型）只覆盖七维中的三维。补全七维后，memory 记录升级为**叙事原子**（narrative atom），适用性显著扩展。

**七维在 Memory 记录上的具体化**：

| 维度 | Memory 字段 | 与现有维度的关系 | 新增价值 |
|---|---|---|---|
| **What** | `record_type`（输入/中间态/Log/输出/Error） | = 内容类型 | taxonomy 对齐 fact_type，与 Tier 2 同构 |
| **Who** | `role`（User/LLM/Tool/Skill）+ `producers`/`consumers`/`excluded` | = 角色 | 增加"谁消费此记录"与负向授权 |
| **When** | `created_at`/`turn`/`step`/`valid_until` | = 时间线 | 增加记录时效窗口（对齐 D₄ lifetime） |
| **Where** | `source_ref`（session/sandbox/tool endpoint/`access_boundary`） | **新增** | 来源边界：哪个 sandbox、哪个工具端点、什么网络边界 |
| **Why** | `causality_chain`/`triggered_by`/`next_steps`/`later_outcomes` | **新增** | 因果：这次调用为何发生、被什么触发、后续动作、结果如何 |
| **How** | `content_digest`/`key_list`/`short_narrative` | 部分在"对话总结" | 摘要的结构化形态，summarize 的填充目标 |
| **Which** | `temporal_links`/`cross_refs` | **新增** | 关联：与哪些记录同期、有因果/语义/访问域/血缘关系 |

**四项能力跃迁**：

1. **查询能力扩展**（§2.1 的七维化升级）
   - 按因果查："为什么这次 tool call 失败" -> `query(why=...)` 沿 causality_chain 回溯
   - 按关联查："这次错误与哪些记录相关" -> `query(which=...)` 沿五类边（sync/cause/sem/access/blood）扩展
   - 按边界查："这个 sandbox 里发生过什么" -> `query(where=...)` 按 access_boundary 过滤
2. **summarize/consolidate 获得结构化目标**：总结不再是自由文本压缩，而是**七维叙事原子的填充与合并**--专用小模型（§5）的输出 schema 即七维表，可验证、可 diff、可版本化
3. **跨 agent semantic join 获得统一键**（§3 升级）：不同 agent 的摘要共享同一七维 schema，join 键从"embedding 相似度"扩展为**维度级匹配**（Who 相同 + When 重叠 + Which 有因果边 = 高置信 join）--松耦合且语义精确
4. **Memory 直通三阶记忆**：memory 记录天然是 fact atom 格式，OPIC 可直接摄取 agent memory 作为 Tier 2 索引源（§3.3 第一行的落地路径打通）--agent 轨迹沉淀为企业知识图谱

**API 扩展**：

```
# 七维统一查询（原 timeline/role 查询是 When/Who 维的特例）
memory.query(what=<record_type>, who=<role|principal>, when=<range>,
             where=<boundary>, why=<causal_anchor>,
             which=<linked_record>, depth=<join_depth>) -> MemoryRecords

# 叙事原子写入（append 时由 Harness 自动补全七维标注，agent 不感知标注细节）
memory.append(role=..., content_type=..., payload=...,
              source_ref={sandbox, tool_endpoint, boundary},
              causality={triggered_by, next_steps},
              links={temporal_window, cross_refs})
```

**与 2608.00101 实证的衔接**：Scaffold 工具清单（[[Scaffold-子系统-功能模块与NFR集成]] §2.2.1）中执行类工具成功率 ~73%、失败重试消耗 4× 算力--`Why` 维的 causality_chain（失败 -> 重试 -> 放弃/成功链）正是挖掘失败模式、沉淀失败经验 Theme 的数据基础；`Which` 维的 temporal_links 则回答"失败是否集中在某时间窗/某依赖版本"（版本漂移检测的语义证据）。

---

## 3. 非功能性需求：跨 Agent 共享

### 3.1 共享架构

```
Agent A ──→ summarize(A.memory) ──┐
                                   ├──→ semantic_join ──→ Agent B 查询结果
Agent B ──→ summarize(B.memory) ──┘
```

### 3.2 设计约束

| 约束 | 说明 | 目的 |
|------|------|------|
| **入口必须经过 summarize** | 其他 agent 不能直接访问原始 memory，必须先访问目标 agent memory 的 summarize 入口 | 控制信息泄露粒度，避免全量暴露 |
| **再经 semantic join 访问** | 在 summarize 基础上，按语义相关性 join 才能获取具体内容 | 保持松耦合——agent 间不直接依赖对方的存储结构 |
| **高内聚** | 每个 agent 的 memory 内部按角色/时间线/主题高内聚组织 | 单个 agent 内部查询高效 |
| **松耦合** | agent 间仅通过 summarize + semantic join 交互，不共享底层存储 | 允许异构存储后端、独立演进 |

### 3.3 与 [[08-数据层修订-三阶记忆子架构]] 的映射

| 本设计 | 三阶记忆 | 关系 |
|--------|---------|------|
| 显性 Memory — 对话总结 | Tier 2 (Index & Link) 的 fact | summarize 产物可被 OPIC 摄取为 fact |
| 显性 Memory — 原始记录 | Tier 1 (Raw Data) 的 agent 轨迹 | 原始记录就是 Raw Data 层的 agent 推理轨迹 |
| 隐性 Memory — 压缩/存储配置 | Tier 3 (Data Theme) 的 NFR 策略 | 部署配置对应 Tier 3 的时效/NFR 治理 |
| 跨 Agent semantic join | D₂ 的 semantic join 接口 | 共享机制复用 D₂ 的查询接口 |

### 3.4 与 [[精读-2606.24775-Agent-Native-Memory-System]] 的映射

| 本设计 | 2606.24775 四模块 | 关系 |
|--------|-------------------|------|
| 显性 Memory 组织（角色/时间线/内容类型） | R (Representation & Storage) | 角色维度是 representation 的组织轴 |
| summarize + semantic join | Q (Retrieval & Routing) | summarize 是 coarse-to-fine routing 的第一级 |
| 隐性 Memory — 压缩配置 | U (Maintenance) | 压缩策略是 maintenance 的核心子操作 |
| 专用小模型处理多模态 | S (Extraction) | 小模型是 schema-constrained extraction 的实现 |

---

## 4. 存储后端

Memory 的物理实现是可插拔的：

| 后端类型 | 适用场景 | 特点 |
|----------|----------|------|
| **File System** | 单 agent、轻量部署、开发调试 | 简单、可读、无依赖 |
| **关系型 DB** | 结构化查询、角色/时间线索引 | 强一致性、SQL 查询 |
| **向量 DB** | 语义检索、主题聚类 | 近邻搜索、embedding 匹配 |
| **图 DB** | 跨角色关联、因果链 | 实体-关系遍历、时序知识图 |
| **混合多引擎** | 企业级生产部署 | 各引擎优势互补，由 Memory Router 路由 |
| **专用小模型** | 多模态内容压缩和管理 | 图片/音频/视频的语义压缩，输出文本摘要写入 memory |

> 关键设计：Memory 后端选择是**隐性 Memory**（部署配置），agent 不感知。Harness 根据查询模式自动路由到合适的后端——时间线查询走 DB，语义检索走向量库，关联分析走图库。

---

## 5. 专用小模型（多模态压缩）

Memory 子系统可包含一个专用小模型，用于：

| 功能 | 说明 | 输入 | 输出 |
|------|------|------|------|
| **多模态压缩** | 将图片/音频/视频内容压缩为文本摘要 | 多模态 payload | 结构化文本摘要 |
| **Memory 合并** | 对多条相似记录进行语义合并 | 多条 MemoryRecord | 合并后的单条记录 |
| **summarize 生成** | 为跨 agent 共享生成入口摘要 | agent memory 子集 | 压缩摘要 + 关键词 |
| **semantic join 辅助** | 在 join 时做语义匹配和相关性排序 | 查询 + 候选记录 | 排序后的结果 |

> 模型选择：专用小模型可以是微调的 3B-7B 模型，与主 LLM 解耦——成本低、延迟低、可独立更新。这呼应了 [[06-数据平面四组成架构]] 中 D₂ "甚至自己的模型"的设计，以及 [[精读-2606.00288-Model-Native-Computing-Architecture]] 中 ICA 双平面架构的概率执行面辅助层。

---

## 6. 与既有架构的关系

### 6.1 在三层架构中的位置

```
┌─────────────────────────────────────────────┐
│              Skill 层                        │
│  (声明数据需求，不拥有 memory)                │
├─────────────────────────────────────────────┤
│              Harness 层                      │
│  ┌─────────────────────────────────────┐    │
│  │  Memory 子系统 (本笔记)              │    │
│  │  ┌──────────┐  ┌──────────────────┐ │    │
│  │  │ 显性      │  │ 隐性              │ │    │
│  │  │ Memory    │  │ Memory            │ │    │
│  │  │ (agent    │  │ (system-managed) │ │    │
│  │  │  visible) │  │                  │ │    │
│  │  └──────────┘  └──────────────────┘ │    │
│  │  ┌──────────────────────────────────┐│    │
│  │  │ 存储后端 (File/DB/向量/图/小模型)  ││    │
│  │  └──────────────────────────────────┘│    │
│  └─────────────────────────────────────┘    │
│  (逻辑准入、路径构造、策略仲裁、证据捕获)      │
├─────────────────────────────────────────────┤
│              Scaffold 层                     │
│  (物理执行隔离，不管理 memory 语义)            │
└─────────────────────────────────────────────┘
```

### 6.2 与论文 v23 的映射

| 本设计元素 | v23 论文概念 | 对应关系 |
|-----------|-------------|----------|
| 显性 Memory 的角色记录 | evidence plane 的 trace records | Memory 记录是 evidence 的子集 |
| summarize 入口 | enforcement overhead E(c,s) 的 evidence volume | summarize 开销纳入 E(c,s) |
| semantic join | bounded composition 的 verifier/semantic join | 共享机制复用派生闭包的 join |
| 隐性 Memory 的压缩配置 | reset/washout 的 cache 清理策略 | 压缩策略影响 reset sentinel |
| 专用小模型 | 未在 v23 正文中出现 | 可作为 Enterprise Architecture 的扩展 |

---

## 7. 设计决策（2026-08-17 用户决议 v0.3 修订）

### 7.1 Memory 的版本管理：压缩后原始记录是否保留？

**决议：原始记录外放到 archive，不放在近线 memory 里面。**

- **近线/归档二分**：近线 memory（near-line）只保留摘要（summary）、索引（index）与轻量元数据；被压缩的**原始记录整体外放（offload）到 archive 存储**（对象存储/归档库），不在近线占用查询路径
- 访问模式：默认查询命中近线的摘要与索引；需要原文时经**外放指针**（archive 地址 + content hash）回取 archive，对应 semantic join / 审计场景
- 这与三阶记忆 [[08-数据层修订-三阶记忆子架构]] 一致：近线承担 Tier 2（Index & Link）的职责，archive 承担 Tier 1（Raw Data）的物理着陆--**压缩 = 把数据从近线推到 archive，而不是删除**
- 保留期限在 **archive 侧**管理（对齐 D₄ lifetime 体系）：默认归档 1 年（租户可配），淘汰前生成最终摘要；带审计/合规标记的记录（G-02 replay 要求）永久保留
- 近线 memory 因此保持**小而快**：查询延迟不被原始记录体积拖累

### 7.2 多 agent 并发写入：一致性如何保证？

**决议：写入序列化（serialization），或先写入 SQLite 数据库进行除重（dedup）。**

- **方案 A--序列化写入**：并发写入请求进入串行化队列（per-key 或 per-partition 串行），顺序落盘。简单可靠，适合写吞吐不高的场景
- **方案 B--SQLite 前置除重层（推荐默认）**：各 agent 的写入先落到一个**嵌入式 SQLite** 缓冲库：
  1. 写入时以内容哈希/键约束做**除重**（相同内容不重复落盘，天然幂等）
  2. SQLite 单写者模型（WAL 模式）内部保证写入串行化与崩溃一致性
  3. 后台 flusher 批量把去重后的记录从 SQLite 合并到正式 memory 后端（DB/向量库/图库）
- 两方案可叠加：SQLite 缓冲层本身就是一种持久化的序列化点；除重发生在合并前，节省后端存储与索引成本
- 记录仍带 `(agent_id, seq)` 全序标识，读取侧按逻辑时钟排序；跨 agent 共享读维持 summarize 入口（松耦合，写权限封闭）

### 7.3 Memory 的容量约束：是否纳入 Ω？超容量如何处理？

**决议：memory 纳入容量限制；超出的部分用哈希（hash）来增加索引。**

- **纳入 Ω**：memory 存储容量作为 declared operating region 的组成部分，与 CPU/GPU/Token/Network 配额并列，租户级隔离
- **超容量的哈希索引机制**（content-addressable 思路）：
  1. 容量逼近水位时，对**超出部分**（冷数据/已被摘要覆盖的原始记录）计算内容哈希（如 SHA-256）
  2. 原始内容外放至 archive（呼应 7.1），近线 memory 仅保留**哈希索引项**：`hash -> (archive 地址, 摘要指针, 元数据)`
  3. 哈希索引天然**定长、紧凑**（每条约数十字节），使近线容量与原始数据体积解耦--数据再大，近线索引体积线性可控
  4. 哈希同时服务**去重**：相同内容只存一份（7.2 的除重共用此键），跨 agent 重复记录自动合并
- 读取路径：查询近线摘要/索引 -> 需要原文时按哈希从 archive 精确回取（O(1) 寻址，无需全量扫描）
- 级联水位仍适用：80% 触发后台哈希外放，100% 强制外放最冷数据；**写入永不静默丢弃**

### 7.4 专用小模型的治理：版本更新是否触发 Skill revalidation？

**决议：专用小模型是维护压缩与索引的工具，相当于一个 API--不属于 Skill，属于 Harness 基本内置工具。**

- **归属裁定**：小模型定位为 **Harness 内置工具**（built-in tool），以稳定 API 形态提供服务（压缩、合并、索引维护、summarize 生成、semantic join 辅助），**不在 Skill 生态内**，不走 Skill lifecycle
- 因此其版本更新：
  - **不触发任何 Skill revalidation**（Skill 依赖的是 API 契约，不是模型本体）
  - 走**内置工具的版本管理**：契约保持向后兼容（输入输出 schema 不变），模型本体可独立升级
  - 升级时仅需通过**压缩/索引质量基准**回归（摘要保真度、检索召回率、join 准确率），达标后灰度切换
- 与 [[Scaffold-子系统-功能模块与NFR集成]] 的衔接：小模型 API 的运行实例部署在 Scaffold（作为普通 serving 端点），其版本登记走 Scaffold 管理体系 §4.3；但**语义契约的所有权在 Harness**
- 类比：小模型之于 memory 子系统，如同编译器之于构建系统--是基础设施 API，不是业务能力单元
