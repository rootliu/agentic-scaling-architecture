# 11 — 可扩展 Agentic Runtime 与可管理性展示总览

> 同步来源：`site/index.html`（中文展示页）与 `site/index-en.html`（英文展示页）  
> 用途：作为 Obsidian 中面向演示/PPT 的入口页，保持与 HTML landing page 的观点、逻辑、术语和案例一致。

## 1. 研究目标

本项目研究一个**可扩展的 agentic runtime**，以及规模化之后的**可管理性**：当 agent 系统持续增加 skills、执行资源、外部数据源和并行 sub-agents 时，runtime 如何仍然保持可审计、可治理、可运维、可演进。

核心目标不是单纯画出三层架构，而是解释并验证：在 LLM 调用具有概率性的前提下，逻辑扩展、物理扩展、数据扩展和并行扩展如何通过显式契约、职责分面、离线子系统和局部性规划实现正交解耦。

## 2. 一句话主张

四条正交切分各自的“加东西”，其一阶成本都应落在**与主请求路径解耦的平面或子系统**上：逻辑扩展落控制面，物理扩展落数据面，数据扩展落离线 off-policy loop，并行扩展落工具集闭包与局部性规划。最终目标是让 agentic runtime **可扩展，也可管理**。

## 3. 架构图读法

展示页中的架构总图按如下顺序阅读：

1. 先看中间的三层运行时核心 `A = <S, H, X>`：Skills、Harness、Scaffold。
2. 再看 Harness 作为契约闸门，如何把上层意图翻译为下层可执行单元。
3. 横向看 CP/DP 职责分流：概率性控制决策进入 CP，高频在线执行路径进入 DP。
4. 右侧的 `𝒟` 是栈外数据子系统，不是第四层，只通过 semantic-join 等受控接口进入主路径。
5. 底部的 P10–P13 描述并行/局部性机制；N8/P14 则把可验证、操作空间闭合的 skill 固化为 code，作为概率控制面的确定性锚。

## 3.1 图谱索引

展示页与 dry-run 页中的每张图都保留可独立阅读的图注；图 0 用作总览导航图，帮助听众先建立全局地图。

- **图 0 · Overview 总览图**：作为演示的第一张全局地图，把三层运行时、CP/DP、栈外数据子系统、并行/局部性和 Skill-as-Code 确定性锚放在同一条阅读路径上。
- **图 1 · 架构总图**：展开三层栈与外部数据子系统，强调 Harness 是逻辑扩展与物理扩展之间的契约闸门。
- **图 2 · Spec 架构图**：解释 Skills 如何用 I/O schema、调用/终止/循环条件把任务材料组织进 LLM context。
- **图 3 · Agent loop**：展示 Skills、Harness、Scaffold 和数据子系统在一次运行中的控制/执行闭环。
- **图 4 · 并行/局部性 walkthrough**：说明 dry-run 如何按工具集闭包切分 sub-agents，并通过 seed affinity、稳定前缀和 summarized context 控制并行成本。
- **图 DR-1/DR-2 与六张详细 Dry Run 图**：用 AI4Science 与 Kronos 两个实例分别说明 spec 调用顺序、概率到确定的固化闭环，以及数据流/回写路径，作为图 1-4 的运行期证据。
- **图 7/8 · Skill 训练与生命周期**：解释 reward 训练、生命周期管理以及 Skill-as-Code 如何把验证过的能力固化为确定性资产。
- **图 9/10 · Data Wiki**：说明自动来源与复杂报告如何进入 Data Wiki，并通过 Data Wiki × Theme Wiki × IR 支持可治理的数据使用。

## 4. 四条正交切分

| 切分 | 解决的问题 | 解耦方式 | 主要笔记 |
| --- | --- | --- | --- |
| 扩展轴：逻辑/物理 | 增加 skill 与增加执行资源不应互相拖拽 | Skills 表达逻辑能力，Scaffold 承载执行/隔离/吞吐，Harness 作为契约层解耦二者 | [[01-C5-双扩展解耦形式化与命题]] |
| CP/DP | LLM 参与控制决策后，系统如何仍可审计和运维 | CP 承载概率性规划、反思、tool synthesis 与治理；DP 承载在线执行、隔离、取数与 serving | [[05-控制面与数据面正交切分]] |
| 栈外数据子系统 | 外部数据持续增加时，主请求路径如何不被压垮 | D1 取数在 DP；D2 语义总结是独立 off-policy loop；D3 治理和 D4 lifetime 在 CP | [[06-数据平面四组成架构]] |
| 并行/局部性 | sub-agents 变多时，如何避免上下文稀释、工具冲突和缓存浪费 | 规划期 dry-run 探测工具集闭包与环境范围，再按工具不重合切分 sub-agents，冻结稳定前缀并用 seed affinity 派生 | [[09-并行度与局部性协同设计]] |

## 5. 三层与数据子系统

- **Skills（Specification Plane）**：负责 specs、I/O schema、调用条件、终止条件和循环条件，把任务相关材料组装并迭代推入 LLM context。task skills 位于此层。
- **Harness（Capability / Contract Plane）**：负责契约翻译、能力供给（tool synthesis）和可管理性子系统 `M`，是逻辑扩展与物理扩展之间的解耦点。
- **Scaffold（Execution / Isolation Plane）**：负责 microVM / sandbox、隔离、算力与推理 serving 容量，刻画系统 throughput `Θ`。
- **Data Subsystem `𝒟`（not a fourth layer）**：刻画 agent 如何理解、访问、治理和维护授权外部数据。它沿在线/离线与 CP/DP 双重分裂，只有受控查询接口进入主路径。

## 6. 创新点总表

| 编号 | 创新点 | 简述 | 命题 |
| --- | --- | --- | --- |
| C5 | 双扩展正交解耦 | 逻辑/物理扩展正交，解耦点是 Harness 契约层 | P1–P3 |
| N0 | 概率性控制面 | LLM 驱动的契约翻译、反思和 tool synthesis 需要审计日志与不变量约束 | P4–P6 |
| N1 | off-policy 语义总结 | 后台 schema-on-read 总结进入不截断 lake，semantic join 按需注入 | P8 |
| N2 | 数据治理即 skill | 将治理从边界控制升级为 per-use-case data-usage skill 的经验沉淀 | P9 |
| N3 | 数据子系统的架构一致性 | 数据子系统沿 CP/DP 自然分裂，复用同一平面不变量 | - |
| N4 | 栈外独立 off-policy loop | 语义总结不是在线步骤，而是有自身 loop、sub-agents 和模型的离线子系统 | - |
| N5 | skill 三分 | task / system / data-usage 三类 skill 共享同一 skill 形式 | - |
| N6 | 工具集切分 sub-agents | 用工具集闭包定义并行独立性、Skills 局部性和 Scaffold seed 边界 | P10–P12 |
| N7 | Dry Run 探测可并行性 | 正式执行前探测工具集闭包与环境范围，再切分 sub-agents | P13 |
| N8 | Skill-as-Code 确定性锚 | 将已验证且操作空间闭合的 skill 固化为 code，降低模型版本漂移 | P14 |

详见 [[07-创新点总结]]、[[10-Skill-as-Code与确定性固化]]。

## 7. Dry Run 实例化

展示页使用两个案例把抽象架构落到一次真实运行：

- **钙钛矿带隙筛选（约 1.3 eV）**：文献进入 D2 时序摘要，物性库进入 D1 取数，仿真触发 code-gen 与 Scaffold cloud/HPC，多信号验证后报告与回写进入 D2/Ω/D3。sub-goals `{文献 → 候选 → 取物性 → 筛选 → 分析 → 报告}` 经 dry-run 切成并行 sub-agents。
- **Kronos 基础模型股票预测**：D1 负责取数，Scaffold 托管 GPU 预训练模型，概率采样进入循环，多信号验证通过回测、泄漏检查和校准完成，预测作为带有效期记录回写。多标的/多周期按工具集切分并行。

这两个案例共同说明：同一条 spec 调用顺序中，扩展轴、CP/DP、数据子系统和并行局部性都会留下可观察的一阶足迹。

相关笔记：[[附录-AI4Science实例化walkthrough]]、[[09-并行度与局部性协同设计]]。

## 8. 缩写表

| 缩写 | 含义 |
| --- | --- |
| `S/H/X` | Skills / Harness / Scaffold |
| `CP` | Control Plane，控制面 |
| `DP` | Data Plane，数据面 |
| `D` / `𝒟` | Data Subsystem，栈外数据子系统 |
| `D1-D4` | 数据子系统四部分：取数 API、语义总结、治理记忆、lifetime 预算 |
| `M1-M4` | 局部性机制：stable prefix、context shard、seed affinity、summarized context |
| `T1-T8` | 工具 capsule 类型，用于描述 Harness 可路由的能力集合 |
| `O1-O8` | Harness 中的运行时选择项，例如 tool、shot、schema、plan、code-gen、reflection、model、token |
| `LLM` | Large Language Model，大语言模型 |
| `I/O` | Input / Output，输入/输出 |
| `API` | Application Programming Interface，应用程序接口 |
| `IR` | Intermediate Relation，中间关系层 |
| `5W1H` | When / Where / Who / What / Why / How，事实抽取与报告组织框架 |
| `NFR` | Non-Functional Requirement，非功能需求 |
| `SLA/SLO` | Service-Level Agreement / Objective，服务级别协议 / 服务级别目标 |
| `QPS` | Queries Per Second，每秒请求数 |
| `SDN` | Software-Defined Networking，软件定义网络 |
| `K8s` | Kubernetes，容器编排系统 |
| `MCP` | Model Context Protocol，模型上下文协议 |
| `BI` | Business Intelligence，企业分析与报表 |
| `JSON` | JavaScript Object Notation，结构化数据交换格式 |
| `PPT/PDF/HTML` | 演示、文档、网页输出格式 |
| `microVM` | micro virtual machine，微虚拟机 |
| `GPU` | Graphics Processing Unit，图形处理/加速卡 |
| `HPC` | High Performance Computing，高性能计算 |
| `SSO` | Single Sign-On，单点登录 |
| `OIDC` | OpenID Connect，身份认证协议 |
| `SAML` | Security Assertion Markup Language，企业身份联合协议 |
| `SCIM` | System for Cross-domain Identity Management，跨域身份管理协议 |
| `RBAC` | Role-Based Access Control，基于角色的访问控制 |
| `KMS` | Key Management Service，密钥管理服务 |
| `S3` | Simple Storage Service，对象存储服务 |
| `PrivateLink` | 云内私有连接服务 |
| `DFT` | Density Functional Theory，密度泛函理论 |
| `OHLCV` | Open / High / Low / Close / Volume，开高低收成交量 |
| `KV-cache` | attention key-value cache，注意力键值缓存 |
| `vLLM` | 高吞吐 LLM serving 引擎 |
| `SOTA` | State of the Art，当前最佳或前沿水平 |
| `DB` | Database，数据库 |
| `MP` / `OQMD` | Materials Project / Open Quantum Materials Database，材料数据库 |
| `HF` | Hugging Face，模型与数据托管平台 |
| `EOD` | End of Day，日终数据 |
| `maxDD` | Maximum Drawdown，最大回撤 |
| `RQ` | Research Question，研究问题 |
| `P/N/C` 或 `N/P/C` | Proposition / Novelty / Contribution，命题 / 创新点 / 贡献 |

## 9. 展示入口

- 中文展示页：`site/index.html`
- 英文展示页：`site/index-en.html`
- 详细架构页：`site/architecture.html`
- Dry Run walkthrough：`site/dry-run.html`
- 简要报告：`site/research-brief.md`
