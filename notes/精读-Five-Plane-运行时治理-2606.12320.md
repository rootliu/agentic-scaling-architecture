# 精读：A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents

> **arXiv**: 2606.12320 | **作者**: Krti Tallam
> **类型**: 论文精读笔记 | **精读日**: 2026-06-17
> **与本研究关系**: ⭐⭐⭐ **C6（分层 NFR/治理）的最强参照 + "reference architecture" 同类工作**

---

## 一句话

企业安全过去治理的是"数据边界"，但生产级 AI agent 把风险移进了 workflow 内部——一串各自被许可的动作可能合成出无人授权的业务变更。提出一个**运行时治理参考架构**，由四个可组合原语构成：**five-plane 分解**（1 个 reasoning plane 裁决意图 + 4 个 enforcement plane：network/identity/endpoint/data）、**stop-anywhere mediation**、**composite principals with capability attenuation**、**audit as structured evidence substrate**。

## 核心论点（摘录 verbatim）

> "risk moves inside the workflow, into sequences of individually-permitted actions that may transform a business process no one authorized."

> "they evaluate request-time decisions against atomic principals, where agentic systems require stateful evaluation against composite principals whose authority attenuates through delegation chains."

## Five-Plane 架构
| Plane | 角色 |
|---|---|
| **Reasoning Plane** | 裁决意图（adjudicate intent） |
| Network Plane | 执行面 |
| Identity Plane | 执行面 |
| Endpoint Plane | 执行面 |
| Data Plane | 执行面 |

## 四个可组合原语 + 关键贡献
- five-plane decomposition（推理面 + 4 执行面）
- **stop-anywhere mediation**（任意点可中断的中介）
- **composite principals with capability attenuation**（复合主体 + 能力衰减）
- **audit as structured evidence substrate**（审计即结构化证据基底）
- **6 种 interruption primitives** 的 taxonomy（泛化 allow/deny）
- **4 个 correctness invariants**
- 演示对 **7 种生产 agent 威胁**在 5 个 workflow 中的封堵
- 65 页，3 figures, 5 tables，含 reference implementation

---

## 与本研究的对照 —— 重点

### 1. 同为 "reference architecture"，是 C1 的同类工作（需定位区分）
| 维度 | Five-Plane (2606.12320) | 本架构 |
|---|---|---|
| 分面依据 | **治理/安全执行**（reasoning + network/identity/endpoint/data） | **运行时执行栈**（Scaffold/Harness/Skills） |
| 关注 | runtime governance（安全为主） | 双扩展解耦 + 可运营（C5 为核心） |
| 维度性质 | 安全 enforcement 的横切分解 | 功能分层 + 扩展维度 |
| 与本架构关系 | **可作为本架构的安全/治理横切层（C6）嵌入** | 容纳 Five-Plane 作为 NFR 实现 |

→ 两者**不冲突且互补**：Five-Plane 是"治理视角的分面"，可作为本架构**横切关注点（C6 安全/可靠）**在各层的落地方案。论文可表述为"本架构的安全 NFR 可采用 Five-Plane 式的 enforcement 分面实现"。

### 2. 直接支撑 C6（分层 NFR）并提供"科学化"范式
- 本研究最担心"工程而非科学"。Five-Plane 给出了**示范**：它不止分面，还定义 **6 个 interruption primitives + 4 个 correctness invariants**，并证明**封堵 7 种威胁** —— 这是"把工程分层提升为带不变量与可证明性质的科学主张"的范本。
- → 本架构应仿此：为三层定义**不变量 + 可验证性质**（见 [[01-C5-双扩展解耦形式化与命题]] P3），而非仅描述职责。

### 3. "composite principals + capability attenuation" 呼应 P3
- 与 [[精读-Benign-in-Isolation-技能组合风险-2606.15242]] 的组合风险呼应：复合主体的权限沿委托链衰减，正是防止"组合越权"的机制。
- → 可作为本架构 **P3（组合性不变量）中 capability containment** 的具体实现机制。

### 4. "风险在 workflow 内部合成"再次印证逻辑扩展的代价
- 与 SCR 论文同一主题：增加能力/动作序列会合成新风险 → 本架构逻辑扩展（加 Skills）必须配套治理面。

---

## 可引用句
- 引"risk moves inside the workflow ... no one authorized"作为 C6/安全动机。
- 引其"6 interruption primitives + 4 invariants + 7 threats foreclosed"作为"分层可被赋予可证明性质"的范式参照。

## 待办
- [ ] 把 Five-Plane 作为本架构 C6 安全横切层的候选实现写入 [[00-讨论记录与原始构想]]
- [ ] 仿其"primitives + invariants + threats"结构，为本架构补 correctness invariants
