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

## 目录结构

```
notes/   研究笔记（讨论记录、形式化、文献清单、精读、时间线、原始构想）
site/    可视化 worktree（Apple 风格 HTML 站点，可直接用浏览器打开 site/index.html）
```

### notes/

| 文件 | 内容 |
|---|---|
| `00-讨论记录与原始构想.md` | 主文档：讨论记录 + 架构精化 S1–S8 |
| `01-C5-双扩展解耦形式化与命题.md` | C5 形式化、P1–P6 命题、Skills 二分、二维框架 |
| `02-2026相关论文清单.md` | 文献清单 |
| `03-Harness-System-SubAgents清单.md` | Harness 维护 sub-agents A–E 五类 |
| `04-研究时间线.md` | M1–M14 关键里程碑 |
| `05-控制面与数据面正交切分.md` | 第二维正交切分、P4–P6、概率性控制面 |
| `精读-*.md` | 7 篇 2026 论文精读笔记 |
| `原始构想-用户原话.md` | 原始 input 逐字存档 I-1~I-5 |

### site/

`index.html`（概览）· `architecture.html`（架构 & 主线 + SVG 图）· `references.html`（文献证据）· `timeline.html`（时间线）· `input.html`（原始构想）

## 演进路径

1. **立论** — 参考架构 + C5 解耦命题 + 定位表；形式化层间契约
2. **证解耦** — 物理轴 throughput 曲线；逻辑轴覆盖 vs 成本；消融去 Harness
3. **保安全/可靠** — 组合性安全（对标 SCR-Bench）；Scaffold 隔离
4. **开源系统化** — 多租户 agent 云、按层 NFR、digital-worker
