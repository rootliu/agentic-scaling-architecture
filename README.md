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
| `精读-*.md` | 7 篇 2026 论文精读笔记 |
| `原始构想-用户原话.md` | 原始 input 逐字存档 I-1~I-5 |

### site/

`index.html`（概览）· `architecture.html`（架构 & 主线 + SVG 图）· `references.html`（文献证据）· `timeline.html`（时间线）· `input.html`（原始构想）

## 演进路径

1. **立论** — 参考架构 + C5 解耦命题 + 定位表；形式化层间契约
2. **证解耦** — 物理轴 throughput 曲线；逻辑轴覆盖 vs 成本；消融去 Harness
3. **保安全/可靠** — 组合性安全（对标 SCR-Bench）；Scaffold 隔离
4. **开源系统化** — 多租户 agent 云、按层 NFR、digital-worker
