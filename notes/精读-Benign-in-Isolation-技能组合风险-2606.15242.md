# 精读：Benign in Isolation, Harmful in Composition — Security Risks in Agent Skill Ecosystems

> **arXiv**: 2606.15242 | **作者**: Yi Xie, Jiawei Du, Yu Cheng, Jiuan Zhou, Zhaoxia Yin
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐⭐ **C4/C5 的必答风险 + P3（组合性不变量）的直接依据**

---

## 一句话

Skills 是 agent 把 plan 变成 action 的能力层，但单独审查每个 skill 不够——真实任务在共享执行上下文中调用多个 skill，会产生 **Skill Composition Risk (SCR)**：单独看 benign 的 skill，其输出/信任信号/授权线索/副作用沿激活路径传播后变得有害。提出 **SCR-Bench** 在路径级（activated path）而非孤立工件级评估风险。

## 核心概念：Skill Composition Risk (SCR)（摘录 verbatim）

> "a skill that appears benign alone can become harmful when its outputs, trust signals, authorization cues, or side effects influence later invocations along an activated path."

> "agent skill security should be assessed at the level of activated paths rather than isolated artifacts."

## SCR-Bench 三个子基准

| 子基准 | 组合类型 | 关键数据 |
|---|---|---|
| **SCR-CapFlow** | capability-flow（能力流）组合 | 组合下攻击成功率达 **33.6%**，孤立基线近 0 |
| **SCR-TrustLift** | trust-transfer（信任传递）组合 | 5 个 backend 中 4 个攻击成功率 **>96.5%** |
| **SCR-AuthBlur** | authorization-confusion（授权混淆）组合 | L1 上下文下风险审批率比 L0 孤立基线 **+71.8%** |

记录**下游状态变化 + 路径级结果**，而非仅文本意图/表面行为。

---

## 与本研究的对照 —— 重点

### 1. 这是 C4/C5 必须正面回应的风险
- 本架构的**逻辑扩展 = 增加 Skills**（[00-讨论记录与原始构想](00-%E8%AE%A8%E8%AE%BA%E8%AE%B0%E5%BD%95%E4%B8%8E%E5%8E%9F%E5%A7%8B%E6%9E%84%E6%83%B3.md) C5）。本文证明：**单独安全的 Skill 组合后可能不安全**。
- 因此本架构不能宣称"加 Skill 即安全扩展"，必须设计**组合层面的约束**。

### 2. 直接支撑 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) 的命题 P3
- P3（组合性不变量）：$\forall s_{new},\ \text{Inv}(S)\Rightarrow\text{Inv}(S\cup\{s_{new}\})$。本文给出了"为什么需要 P3"的实证：组合攻击成功率高达 96.5%。
- 设计推论：**Harness（契约层）不仅做 intent→executable 的翻译，还必须做 path-aware 的组合约束执行**。这把 Harness 从"翻译器"升级为"组合不变量的强制点"，是本架构的科学承诺。

### 3. 三类风险 → 三类不变量（可写进论文）
| SCR 风险 | 对应本架构应保持的不变量 Inv |
|---|---|
| CapFlow（能力流） | 工具能力不因组合而越权扩散（capability containment） |
| TrustLift（信任传递） | 信任不沿 skill 链非法提升（no trust escalation） |
| AuthBlur（授权混淆） | 授权上下文在组合中保持清晰、不被污染（auth isolation） |

### 4. 方法借鉴
- "path-aware / activated-path 级评估"可直接成为本架构**阶段 3（Reliability paper）**的评估方法论。
- SCR-Bench 可作为本架构逻辑扩展安全性的**现成评测基准**或对比基线。

---

## 可引用句（论文备用）
- 动机段：引"benign alone → harmful in composition"，论证逻辑扩展不是无代价的。
- 方法段：引"assessed at the level of activated paths"，作为本架构组合约束的评估原则。

## 待办
- [ ] 在 [01-C5-双扩展解耦形式化与命题](01-C5-%E5%8F%8C%E6%89%A9%E5%B1%95%E8%A7%A3%E8%80%A6%E5%BD%A2%E5%BC%8F%E5%8C%96%E4%B8%8E%E5%91%BD%E9%A2%98.md) P3 下补充上表（三风险↔三不变量）
- [ ] 阶段 3 实验直接采用/对标 SCR-Bench
