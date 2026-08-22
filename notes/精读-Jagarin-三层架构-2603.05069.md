# 精读：Jagarin — A Three-Layer Architecture for Hibernating Personal Duty Agents on Mobile

> **arXiv**: 2603.05069 | **作者**: Ravi Kiran Kadaboina
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐ **命名/概念撞车排查**（同样叫 "three-layer architecture"，但维度完全不同）

---

## 一句话

为移动端个人 agent 解决"持续后台执行耗电/违反沙箱策略" vs "纯被动 agent 错过时效义务"的悖论，提出三层架构 DAWN / ARIA / ACE，通过**结构化休眠 + 按需唤醒**实现。

## 三层（注意：与本架构的三层是完全不同的切分维度）

| 层 | 名称 | 职责 |
|---|---|---|
| L1 | **DAWN** (Duty-Aware Wake Network) | 端上启发式引擎，从 4 个信号算 urgency score，决定休眠 agent 何时唤醒/升级 |
| L2 | **ARIA** (Agent Relay Identity Architecture) | 商业邮件身份代理，按类别把 inbox 路由到 DAWN handler，消除冷启动 |
| L3 | **ACE** (Agent-Centric Exchange) | 机构→个人 agent 的机器可读通信协议框架，替代面向人的邮件 |

## 关键点

- 核心矛盾是**移动端生命周期管理**（电量/沙箱/时效），非通用 runtime 分层。
- 三层是按"**唤醒决策 / 身份路由 / 通信协议**"切分的**功能管线**，不是"隔离/能力/规约"的运行时栈。
- Flutter Android 原型，临时云 agent 仅在用户发起升级时调用。4 figures, 12 pages。

---

## 与本研究的对照 —— 区分结论

**结论：不构成 novelty 威胁，但必须在论文中显式区分，因为关键词"three-layer architecture + agent"会被检索撞上。**

| 维度 | Jagarin | 本架构 |
|---|---|---|
| 分层依据 | 移动端 duty agent 的生命周期管线（唤醒/路由/通信） | 通用 agent runtime 的执行栈（隔离/能力/规约） |
| 三层语义 | DAWN/ARIA/ACE（决策、身份、协议） | Scaffold/Harness/Skills（执行、契约、规约） |
| 扩展维度 | 无逻辑/物理扩展概念 | C5 双扩展解耦是核心 |
| 部署目标 | 移动端、无持久云状态 | agent 云系统、多租户、可运营 |
| 与互联网部署类比 | 无 | 有（虚机/框架/前端） |

**写进 related work 的一句话**: "尽管同样采用三层划分，Jagarin 的层对应移动端 duty agent 的生命周期管线（唤醒决策、身份路由、通信协议），与本文以执行隔离、能力契约、能力规约为依据的 runtime 栈在划分维度上正交。"

## 待办
- [ ] 在 [[00-讨论记录与原始构想]] 的"区分表"中固化此条
- [ ] 检索是否还有其他 "three-layer/three-tier agent" 论文需一并区分（已知：CHRONOS 2605.23887、MediaClaw 2605.14771）
