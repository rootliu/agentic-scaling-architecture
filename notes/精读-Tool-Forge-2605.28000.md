# 精读：Tool Forge — A Validation-Carrying Toolchain for Governed Agentic Execution

> **arXiv**: 2605.28000 | **作者**: Swanand Rao
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐⭐ **Harness 层 tool synthesis（C3）的最直接实现参考 + 开源实现**

---

## 一句话

把"工具层"从手写集成/静态 schema 列表升级为 **validation-carrying toolchain**：将自然语言能力意图转化为**经沙箱验证、编目、带验证证据**的工具工件（capsule），并通过 **token-efficient 的 Router** 以 intent-scoped 会话暴露给 agent（而非把全量 catalog schema 塞进 context）。有开源实现。

## 核心概念（摘录 verbatim）

> "Tool Forge treats a tool as a capsule containing intent, capability contract, implementation, dependency policy, tests, documentation, runtime validation evidence, lifecycle state, credential bindings, and routing metadata."

> "a Router that exposes intent-scoped tool sessions instead of loading full catalog schemas into the model context."

## 关键数据
- Router 83 案例：micro-F1 **0.901**，相比朴素全量 schema 暴露**减少 99.2% 的 task-flow 工具 context**
- 端到端生成 25 案例：生成 25/25 工具 bundle，micro-F1 **0.940**，23/25 通过 live sandbox 验证
- 2 figures, 3 tables；MCP-facing routing；**开源实现**

## 工具合成机制
自然语言能力描述 → 验证过的工件（实现 + 依赖策略 + 测试 + 文档 + 凭证绑定）→ sandbox 验证 → 编目。

---

## 与本研究的对照 —— 重点

### 1. C3（Harness 用 LLM 生成新工具）的最直接实现参考
- 本架构 Harness 的核心能力之一就是"**大模型调用产生新的程序工具**"（[00-讨论记录与原始构想](00-%E8%AE%A8%E8%AE%BA%E8%AE%B0%E5%BD%95%E4%B8%8E%E5%8E%9F%E5%A7%8B%E6%9E%84%E6%83%B3.md) C3，用户原话）。
- Tool Forge 给出了**完整的工程范式**：tool = capsule（含意图、能力契约、实现、测试、验证证据、生命周期、凭证、路由元数据）。
- → 这几乎就是本架构 Harness "tool synthesis" 的落地蓝图，且开源，可作为**阶段 4 实现的直接基础或对标**。

### 2. "capability contract" 直接呼应本架构的契约层（P2）
- Tool Forge 的 capsule 含 **capability contract** —— 与 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 命题 P2"Harness 作为显式契约层"概念同源。
- 可引用其 capsule 结构作为 Harness 契约接口的**具体化候选**（本架构此前留白）。

### 3. Router 的 intent-scoped 加载 → 直接缓解 P1 风险点
- [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) P1 的最大风险：加 Skills 会撑大 context、间接拖垮 throughput。
- Tool Forge 的 Router 用 **intent-scoped session 替代全量 schema 加载，省 99.2% context** —— 这正是"逻辑扩展不损害物理吞吐"的**关键工程支撑**！
- → 可写进论文：**正是因为有 intent-scoped 的按需加载机制，逻辑扩展（加 Skills/工具）才不会线性侵蚀 context 预算，从而保证 P1 的解耦近似成立。**

### 4. governance 对 C6 的支撑
- validation evidence + lifecycle + credential binding + sandbox 验证 → 对应 C6 的可靠性/安全 NFR，且落在 Harness/Scaffold 层。

---

## 可引用句
- 引 capsule 定义作为 Harness 契约接口的具体化。
- 引"99.2% context reduction via intent-scoped routing"作为 P1 解耦可行性的工程证据。

## 待办
- [ ] 查其开源仓库，评估能否作为阶段 4 Harness 实现基础
- [ ] 把 capsule 结构纳入 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 的 H 契约接口定义
- [ ] 把"intent-scoped 按需加载"写入 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) P1 风险缓解
