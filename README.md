# Agentic Scaling Architecture

一个 agentic runtime 的三层参考架构研究 —— **Scaffold · Harness · Skills**，
核心主张：agent 的**逻辑可扩展性**与**物理可扩展性**可以正交解耦，解耦点是层间的显式契约。

> 类型：学术研究 · 文献综述期 · 文献对照验证
> 目标：学术论文 + 开源 agent 云系统

## 核心论证

现代云应用早已"前端按流量横扩 / 业务按功能纵展 / 后端按算力扩"——三轴解耦是**已知工程范式**。
本研究的 delta：在每层内嵌**概率性 LLM 调用**的条件下，给出该解耦成立的**充要条件（契约层 H）**与**可证伪判据（P1）**。

## 三层栈

| 层 | 名称 | 职责 | 扩展轴 |
|---|---|---|---|
| L3 | **Skills**（Specification Plane） | specs / I/O schema / 调用·终止·循环条件；组装并推送进 LLM context | 逻辑扩展（𝒯↑） |
| L2 | **Harness**（Capability / Contract Plane） | 契约翻译 + 能力供给（tool synthesis）+ 维护子系统 | 契约（解耦点） |
| L1 | **Scaffold**（Execution / Isolation Plane） | microVM / sandbox / bash / 隔离与算力（含推理 serving 容量） | 物理扩展（Θ↑） |

## 六条可检验命题

- **C1** 三层栈对应"虚机 / 框架运行时 / 前端运行时"
- **C2** Scaffold = microVM 隔离沙盒
- **C3** Harness = memory/context + 外部工具 + LLM 生成新工具
- **C4** Skills = specs / 条件，组装并迭代推送进 context
- **C5 ★** 双扩展维度解耦（核心 novelty）：逻辑扩展=加 Skills；物理扩展=加 Scaffold
- **C6** 分层 NFR：按层设计性能/可靠/可用/安全

## 形式化命题

- **P1**（解耦）：∂Θ/∂\|S\|≈0 且 ∂𝒯/∂\|X\|=0；充要前提 = 维护开销只依赖 token 流量、不依赖 Skills 语义复杂度
- **P2**（契约充分性）：解耦充分条件 = 良定义契约 H，S 与 X 无直接依赖
- **P3**（组合不变量）：逻辑扩展保持安全不变量 Inv(S)⇒Inv(S∪{s})

### 第二维：控制面 / 数据面（2×3 设计矩阵）

在"逻辑/物理扩展"轴之外，叠加分布式系统经典的 **control plane / data plane** 正交切分：数据面承载 token 处理路径（∝ token 流量），控制面承载决策/契约翻译/维护触发/不变量（∝ 状态事件）。

- **P4**（平面分离）：∂L_CP/∂τ̇≈0 且 ∂L_DP/∂|CP规则|≈0
- **P5**（P1 的平面分解）：逻辑扩展作用于控制面、物理扩展作用于数据面 → 正交（P1 的第二个结构性来源）
- **P6**（维护子系统跨面分解）：M 触发逻辑属控制面、推理开销属数据面
- **真正 novelty = 概率性控制面**：控制决策部分由 LLM 驱动，需可审计日志 + 不变量约束其不确定性

### 第三维：数据子系统四组成（agent data plane）

agent 与**外部数据**协同需要一个**略独立于三层栈的数据子系统** `D = <D1, D2, D3, D4, Omega>`：D1 on-policy 取数 API、D2 **off-policy 语义总结平面**（schema-on-read 反 ETL 截断、保留 latent、semantic join 检索）、D3 **数据治理 memory**（把“如何用数据”沉淀为 per-use-case **data-usage skill**）、D4 **lifetime 体系**（时新性 + 业务口径 + 访问 NFR 预算）。D1/D2 由 Harness 直接调用（运行时数据面），D3/D4 为独立 API 供 context 组装查询（运行时控制面）——平面切分第三次成立。

- **P7**（取数解耦）：固定 use case，∂ℓ/∂|src|≈0 —— 加数据源不污染单请求 token 成本（与 P1 物理扩展同构）
- **P8**（语义摘要充分性）：off-policy 摘要 Σ 是取数充分统计量，兼顾覆盖与精度 —— 填补 *Do Agents Need Semantic Metadata?*（2605.28787, Halevy 等）留空的折中路
- **P9**（治理记忆收敛）：随 use case 重复，data-usage skill 使取数决策熵单调不增
- **三连 novelty**：N1 off-policy schema-on-read 语义总结；N2 数据治理从“管边界”升级为“沉淀 skill/memory”（**首次缝合数据治理与 agent skill/记忆理论**）；N3 数据子系统沿 CP/DP 自然分裂、复用同一平面不变量。skill 理论由 task/system **二分**扩为 task/system/data-usage **三分**

### 数据子系统落地：Data Wiki × Theme Wiki × IR

把 D2/D3 落成两个具名 wiki + 一层中间关系：**Data Wiki**（D2 落地）回答"数据是什么"——常规数据源由 off-policy loop 自动读取，产出 Σ 四段（自然语言总结/格式/关键词/关联关系-外键）；复杂报表（多 sheet、口径漂移）则与人协同构建规范（来源/频率/维护/时效性），并以人常备报表为参照物，经**还原式 reflection**（尝试从总结还原参照报表的部分表格）校验总结质量。**Theme Wiki**（D3 产出侧）回答"产出该长什么样"——收录 σ_out 各结果子域（报表/图表/PPT/分析报告/数据模型程序……）经双子目标 Reward 验证收敛后的可复用模板。两者之间只有一层显式耦合——**IR（Intermediate Relation）**：给定 theme，除 semantic join 命中集外必须显式携带**5W+1H**（When 时效性、Where 使用范围、Who 数据拥有者及授权、What 数据语义、Why 集成逻辑、How 物理访问方式），其余部分保持正交独立、松散耦合。

- **P16**（还原式 reflection）：还原式 reflection 是 P8（摘要充分性）的可操作判据——若 agent 能从 Σ(src) + 参照报表规范还原出参照报表的关键数值/结构，则 Σ 对该 use case 是充分的
- **P17**（IR 松耦合）：数据源变更（Data Wiki 侧）与产出格式变更（Theme Wiki 侧）互不传播，只需更新 IR 记录——是 P2（契约充分性）在数据/产出双 wiki 场景下的实例
- **三连 novelty**：N10 Data Wiki 的人机协同 + 还原式 reflection；N11 Theme Wiki 作为 σ_out 结果子域的复用登记表；N12 IR 中间关系层 + 5W1H——把 §06 契约映射里含糊的"plan"步骤实体化为可审计记录

### 第四维：并行度与局部性协同设计

给定预算 *B*，在前三条解耦切分之上进一步**主动逼近**并行上界：用一根杠杆——**按工具集切分子 agent**——同时定义 Skills 局部性、并行独立性与 Scaffold seed 边界；机制根因是"一次推理 = 内在知识（固定）⊕ context（可变）"，故可控之道是**前缀冻结 + 尾部变化**。

- **P10**（并行度可设计）：s = s₀ + λ·ρ(𝒫)，E = E₀ − μ·c̄_ctx；并行上界是切分设计的函数，而非外生常数
- **P11**（工具集局部性）：子 agent 工具集越稳定，context 跨迭代前缀命中率 H 越高
- **P12**（seed 亲和）：同 seed 共置 + 异 seed 分散，固定资源下可容纳并行子 agent 数 k_max 更高
- **P13**（规划期 dry-run）：主 agent 规划时先 dry-run 候选子任务的工具集闭包与环境范围，据此切分 → ρ↓、H↑（类比 cost-based query planning）
- **novelty N6/N7**：并行度上界可主动设计（对标 ICA 启发式 III 的被动阿姆达尔上界）；规划期局部性预探测把切分依据从"语义"扩展到"工具集闭包 + 环境可行性"

### 确定性锚：Skill-as-Code

对操作空间闭合的 skill（工具集闭合、输出格式固定、分支可枚举），把获取→判断→核验→决策过程固化为 **code**，从"每轮概率生成"退化为"确定执行"——把概率控制面 N0 的二分（概率决策⊕确定护栏）升级为三分（+**确定执行体**）。

- **P14**（跨模型稳定性）：被 code 固化的 skill 输出不随模型版本 θ 演进而漂移，∂output/∂θ≈0
- **novelty N8**：Skill-as-Code 定位为**概率控制面的确定性锚 + 模型版本演进下的契约稳定器**（区别于 CodeAct/AutoHarness/Tool-Forge 的"code 提效/可组合"叙事）

### Skill 训练：双子目标 Reward

把复杂 agent 看作一个**权重固定（frozen）大模型的前端可编辑激活层**——即 skill：⟨goal，输出格式要求，工具集与数据源列表，调用与反思检查标准，正例与反例⟩。训练 agent 本质是针对 goal 的强化学习式 skill 迭代；核心难点是自然语言 goal 的 reward 打分粒度，解法是拆成两个正交子目标：

- **r_out 结果子目标**：沿输出格式 σ_out 的各子域（数字/总结/引用……）独立标注 benchmark 打分，Σ w_d·r_d 汇总
- **r_proc 过程子目标**：是否调用正确工具/数据源、是否完成正确逻辑分析、是否达到进阶标准——稠密即时信号，加快 skill 迭代方向一致性
- **P15**（双子目标分解加速收敛）：双维 reward 比单一 scalar reward 归因更清晰、收敛更快、人工干预更少
- **novelty N9**：把 SkillOpt/GEPA/TextGrad 等单一 scalar/偏好信号升级为**结果子域 benchmark × 过程一致性**的结构化分解

由此推出 skill 完整生命周期：**训练**（双子目标 Reward 迭代收敛）→ **固化**（κ(s) 达阈后编译为 code tool，P14）→ 融入 Harness 工具集供其它 agent 复用；未收敛部分保留自然语言防止过早锁死泛化。

## 目录结构

```
notes/   研究笔记（讨论记录、形式化、文献清单、精读、时间线、原始构想）
site/    可视化 worktree（Apple 风格 HTML 站点，可直接用浏览器打开 site/index.html）
```

### notes/

| 文件 | 内容 |
|---|---|
| `00-讨论记录与原始构想.md` | 主文档：讨论记录 + 架构精化 S1–S9 |
| `01-C5-双扩展解耦形式化与命题.md` | C5 形式化、P1–P9 命题、Skills 三分、三维框架 |
| `02-2026相关论文清单.md` | 文献清单 |
| `03-Harness-System-SubAgents清单.md` | Harness 维护 sub-agents A–E 五类 |
| `04-研究时间线.md` | M1–M15 关键里程碑 |
| `05-控制面与数据面正交切分.md` | 第二维正交切分、P4–P6、概率性控制面 |
| `06-数据平面四组成架构.md` | 第三维数据子系统四组成、P7–P9、三连 novelty、related works |
| `07-创新点总结.md` | Novelty Ledger 单一事实源（C5 + N0–N9） |
| `08-模型原生计算架构-体系结构视角.md` | ICA 六层 ↔ 三层栈映射，消解"控制面确定/概率"冲突 |
| `09-并行度与局部性协同设计.md` | 第四维并行度/局部性、P10–P13、N6/N7 |
| `10-Skill-as-Code与确定性固化.md` | Skill-as-Code 确定性锚、P14、N8 |
| `11-可扩展Agentic-Runtime与可管理性展示总览.md` / `11-Scalable-Agentic-Runtime-and-Manageability-Overview.md` | 面向演示的中/英总览，对齐 site landing page |
| `12-Skill作为可训练激活层-双子目标Reward.md` | Skill 训练机制、双子目标 Reward、P15、N9 |
| `13-DataWiki-ThemeWiki-IR中间关系层.md` | D2/D3 落地为 Data Wiki × Theme Wiki × IR、5W1H、P16/P17、N10–N12 |
| `精读-*.md` | 7+ 篇 2026 论文精读笔记 |
| `原始构想-用户原话.md` | 原始 input 逐字存档 I-1~I-5 |

### site/

`index.html`（概览）· `architecture.html`（架构 & 主线 + SVG 图，含 §10 Skill 训练与生命周期）· `dry-run.html`（AI4Science / Kronos 双用例 walkthrough）· `research-brief.html`（研究简报）· `references.html`（文献证据）· `timeline.html`（时间线）· `input.html`（原始构想）

架构图（`site/figures/`）由 `build-figures.js`（图 1–6，三层架构/agent loop 走查）、`build-figures-skilltrain.js`（图 7 双子目标 Reward 训练环、图 8 Skill 生命周期）与 `build-figures-datawiki.js`（图 9 Data Wiki 构建、图 10 Data/Theme Wiki × IR 组成图）生成，均为中英 SVG+PNG；`render.sh` 负责早期图的 SVG→PDF/PNG 渲染，图 7 起改用 `sharp`（Node）本地渲染。

## 演进路径

1. **立论** — 四条切分参考架构 + C5 解耦命题 + Skill-as-Code 确定性锚 + 双子目标 Reward 训练机制；形式化层间契约、平面切分、并行局部性与 skill 生命周期（train→freeze）
2. **证解耦** — 物理轴 throughput 曲线（baseline=Helium/vLLM）；逻辑轴覆盖 vs 成本；数据轴 P7–P9 实验；消融去 Harness / 平面泄漏注入
3. **保安全/可靠** — 组合性安全（对标 SCR-Bench）；Scaffold 隔离；概率性控制面可审计性指标
4. **开源系统化** — 多租户 agent 云、按层 NFR、digital-worker；数据子系统 𝒟 落地
