# 精读：From Static Templates to Dynamic Runtime Graphs — A Survey of Workflow Optimization for LLM Agents

> **arXiv**: 2603.22386 | **作者**: Ling Yue, Kushal Raj Bhandari, Ching-Yun Ko, Dhaval Patel, Shuxin Lin, Nianjun Zhou, Jianxi Gao, Pin-Yu Chen, Shaowu Pan
> **类型**: 论文精读笔记（survey） | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐ **提供 vocabulary 与定位框架；其 "scaffold/template/realized graph/trace" 区分对本架构很有用**

---

## 一句话

把 LLM agent 的 workflow 视为 **agentic computation graphs (ACGs)**，按"**结构何时确定**"组织文献：static（部署前固定可复用 scaffold）vs dynamic（运行前/中选择、生成、修订 workflow）；并沿三个维度归类，提出 structure-aware evaluation。

## 三维分类框架

1. **When**：结构何时确定（static vs dynamic）
2. **What**：优化 workflow 的哪一部分
3. **Which signals**：用什么评估信号引导优化（task metrics / verifier signals / preferences / trace-derived feedback）

## 关键区分（对本架构非常有价值）

> 区分三种结构层级：
> - **reusable workflow templates**（可复用模板 = 设计选择）
> - **run-specific realized graphs**（单次运行实例化的图）
> - **execution traces**（实际运行行为）

并提出 **structure-aware evaluation**：在下游任务指标之外，补充 graph-level properties、execution cost、robustness、结构随输入的变化。

---

## 与本研究的对照

### 1. 术语对齐（重要）
- 本综述用 **"workflow scaffold"** 指"部署前固定的可复用工作流骨架"——这与本架构的 **Scaffold（执行/隔离层）** 是**不同含义**！⚠️
- → **命名风险**：本架构的 "Scaffold" 与该综述的 "scaffold" 语义冲突（它指 workflow 模板，本架构指 microVM 执行沙盒）。论文中必须**明确定义并区分**，或考虑改名（见 [00-讨论记录与原始构想](00-%E8%AE%A8%E8%AE%BA%E8%AE%B0%E5%BD%95%E4%B8%8E%E5%8E%9F%E5%A7%8B%E6%9E%84%E6%83%B3.md) 命名建议）。

### 2. 三层结构区分可借用
- 它的 "template / realized graph / trace" 三分，可映射到本架构：
  - template ≈ Skills（规约/可复用设计）
  - realized graph ≈ Harness 在运行时组装的执行计划
  - trace ≈ Scaffold 上的实际执行记录
- → 这给本架构提供了一个**已被 survey 认可的"设计 vs 运行时实例 vs 实际行为"分离视角**，可强化分层的合理性论证。

### 3. structure-aware evaluation 支撑 C5 度量
- 它主张用 graph-level properties + execution cost + robustness 评估 → 与 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 的吞吐/延迟/能力覆盖度量方向一致，可引为评估方法论依据。

### 4. 定位价值
- 作为 survey，是本架构 related work 中"workflow optimization"分支的**定位锚点**和 vocabulary 来源。
- static vs dynamic 的 lens 可用来说明：本架构的逻辑扩展（加 Skills）属于哪一类（更偏 static 可复用规约 + dynamic 运行时组装）。

---

## 可引用句
- 引其 ACG / "when structure is determined" lens 作为定位本架构 Harness 运行时组装能力的坐标。
- 引其 structure-aware evaluation 作为 C5 度量的方法论支撑。

## 待办
- [ ] **解决命名冲突**：本架构 "Scaffold" vs 该综述 "workflow scaffold" —— 在 [00-讨论记录与原始构想](00-%E8%AE%A8%E8%AE%BA%E8%AE%B0%E5%BD%95%E4%B8%8E%E5%8E%9F%E5%A7%8B%E6%9E%84%E6%83%B3.md) 命名决策中明确
- [ ] 把 template/realized-graph/trace 三分纳入本架构层次说明
