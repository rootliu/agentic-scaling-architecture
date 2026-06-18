# 精读：Efficient LLM Serving for Agentic Workflows — A Data Systems Perspective (Helium)

> **arXiv**: 2603.16104 | **作者**: Noppanat Wadlom, Junyi Shen, Yao Lu
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐ **物理扩展（throughput）与 Scaffold 层优化的方法依据**

---

## 一句话

从**数据系统视角**重思 agent serving：把 agentic workflow 建模为 **query plan**，把 LLM 调用当作 **first-class operator**；提出 **Helium**——workflow-aware serving 框架，用 proactive caching + cache-aware scheduling 最大化跨 prompt/KV/workflow 的复用，比 SOTA agent serving 快 **1.56x**。

## 核心论点（摘录 verbatim）

> "Existing LLM serving systems, such as vLLM, focus on optimizing individual inference calls and overlook cross-call dependencies, leading to significant inefficiencies."

> "Helium ... models agentic workloads as query plans and treats LLM invocations as first-class operators. ... bridges classic query optimization principles with LLM serving."

## 关键机制
- 把 workflow 当 **query execution plan**，LLM 调用 = 可组合 operator
- **proactive caching**（主动缓存）+ **cache-aware scheduling**（缓存感知调度）
- 复用范围：prompts、KV states、entire workflows
- 1.56x 加速；强调"end-to-end across workflows"优化的必要性

---

## 与本研究的对照

### 1. 直接支撑 C5 的"物理扩展"维度
- 本架构主张物理扩展 = 增加 Scaffold → 提升 throughput（[[00-讨论记录与原始构想]] C5 / [[01-C5-双扩展解耦形式化与命题]] 定义 2、命题 P1）。
- Helium 证明：**agent serving 的吞吐可通过 workflow 级优化系统性提升**——为本架构"Scaffold 层是 throughput 杠杆"提供方法学依据。
- 阶段 2 的"物理轴吞吐曲线"实验，可把 Helium / vLLM 作为 **baseline**。

### 2. "把 LLM 调用当 first-class operator"对 Harness 设计有启发
- 与 [[精读-Policy-Driven-Runtime-Layer-2605.27744]] 的"agent-aware 中间层"呼应：都主张在 serving 层引入对 agent/workflow 结构的感知。
- 本架构 Harness 可借鉴"query plan"抽象：把 Skills 产生的 intent 编译成可优化的执行计划下发给 Scaffold —— 这能强化 P2（契约层）的工程可行性。

### 3. 边界区分
- Helium 是**纯 serving 性能优化**，不涉及能力/扩展维度划分；本架构关注的是**扩展性解耦**。Helium 属于本架构 Scaffold/Harness 层"可插入的优化技术"，而非竞争性架构。

---

## 可引用句
- 引其"existing systems overlook cross-call dependencies"，论证物理扩展需要 workflow-aware 的 Scaffold 而非朴素堆实例。
- 引其 1.56x 结果作为"物理扩展存在可观优化空间"的证据。

## 待办
- [ ] 阶段 2 实验把 Helium / vLLM 列为 throughput baseline
- [ ] 评估"query plan"抽象能否成为 Harness 契约接口的候选形式
