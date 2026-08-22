# 精读：A Policy-Driven Runtime Layer for Agentic LLM Serving

> **arXiv**: 2605.27744 | **作者**: Rui Zhang, Chaeeun Kim, Liting Hu
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐⭐ **最强支撑 + 最大 novelty 威胁**（与本架构 Harness 层定位高度相似）

---

## 一句话

在 agent 框架（懂语义）与推理引擎（懂事件）之间**插入第三层 "agent runtime layer"**，暴露 `observe / score / predict / act` 四个原语，让所有"agent-aware 跨层策略"（缓存、批处理、推测执行、公平性、工具结果记忆化、安全执行等）都插到这一层；并以 KV 缓存（CacheSage）为例验证。

## 核心论点（摘录，verbatim）

> "The agent framework above knows agent identities, role, schemas, and dispatch structure but never sees an engine-level event; the serving engine below sees every event but knows nothing about agents. A surprising number of cross-cutting policies depend on both... Each lives in the seam between the two layers and is currently solved by a one-off patch."

> "we argue this seam is best addressed by an architectural change rather than point fixes: insert a third tier, an agent runtime layer, between the framework and the engine, exposing four primitives (observe, score, predict, act)..., with agent identity as the shared coordinate."

## 关键机制

- **三层定位**: framework（上）/ **agent runtime layer（中）** / serving engine（下）
- **四原语**: observe, score, predict, act —— 任何 agent-aware 策略以此接入
- **共享坐标**: agent identity
- **九类策略**: prefix caching、batch shaping、speculative execution、fairness、tool-result memoization、safety enforcement 等
- **CacheSage**: 在线学习 per-workload 的 agent transition matrix，做 survival-based eviction + between-step prefetch
- **实验结果**: 5 个真实多 agent workload 上，缓存命中率 +13~37pp，平均 TTFT 降 12~29%，throughput 提升 6~14%

---

## 与本研究（三层架构 / C5）的对照 —— 重点

### 1. 这是 C5 与"科学化"主张的**最强外部支撑**
- 它独立论证了"上层懂语义、下层懂事件、二者间存在 seam（接缝），需要一个显式中间层承接跨层策略" —— 这正是 [[01-C5-双扩展解耦形式化与命题]] 中 **命题 P2（契约充分性）** 的现实依据。
- 可直接引用其 "seam" 论述作为本架构 **Harness = 显式契约层** 的动机来源。

### 2. 这也是**最大的 novelty 威胁**，必须做区分
| 维度 | Policy-Driven Runtime Layer (2605.27744) | 本架构 |
|---|---|---|
| 中间层定位 | framework 与 **serving engine** 之间 | Skills 与 **Scaffold（执行/隔离）** 之间 |
| 中间层目标 | 承接**跨层 serving 策略**（缓存/调度/公平性） | 承接**能力契约 + tool synthesis + 组合不变量**（逻辑↔物理翻译） |
| 抽象原语 | observe / score / predict / act | （本架构需自定义：intent→executable 的契约接口，尚未定型） |
| 核心主张 | 跨层策略的统一插入点 | **逻辑/物理扩展解耦**（C5），其层只是手段 |
| 视角 | serving/系统性能视角 | runtime 应用工程 + 双扩展维度 + 数字员工运营 |

**区分要点（写进论文 related work）**: 它解决的是"**serving 栈内**的跨层策略归属问题"；本架构解决的是"**应用可扩展性**的两个正交维度如何解耦"。它的"runtime layer"偏向**推理引擎调度**，本架构的 Harness 偏向**能力/契约**。但二者**都主张插入一个显式中间层**——这一点必须显式致敬并切分边界，否则 reviewer 会判定 C1 缺乏新意。

### 3. 可借用的方法
- 它"把 9 个策略映射到一层"的论证方式，可被本架构借鉴：**把 N 个 NFR（C6）映射到三层**，证明分层的承载力。
- CacheSage 的"agent transition matrix"思路，与本架构 Skills 的"按需加载 + context 组装"（见 [[01]] P1 风险点）相关，可作为物理扩展时降低 context 成本的手段。

---

## 可引用句（论文 related work / motivation 备用）

- 用于动机段：引其 seam 论述，论证"必须有显式中间层"。
- 用于区分段：明确本架构 Harness 的契约对象是 Skills↔Scaffold 的能力翻译，而非 serving 引擎事件。

## 待办
- [ ] 找原文 Figure（四原语示意 / 三层图），摘录到 [[00-讨论记录与原始构想]]
- [ ] 确认其是否讨论"扩展性"——若未涉及逻辑/物理扩展解耦，则 C5 仍是空白（强化 novelty）
