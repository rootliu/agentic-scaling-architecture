# 03 — Harness System Sub-Agents 清单（文献支撑）

> **来源**: 2026-06-18 arXiv 检索 + vault 笔记对照
> **类型**: 机制目录 / 支撑 S1–S3（[[00-讨论记录与原始构想]] 架构精化）
> **定位**: 论证"system skills 属于 Harness、且走物理轴"——回应 [[原始构想-用户原话]] I-3/I-4

---

## 核心结论

文献中存在一批**专门维护 runtime 自身**的 system-level 机制，可作为 Harness 内部"维护子系统 $M$"的实现。它们对外是固定签名工具，内部 LLM 驱动但指令固定，触发 $\propto$ token 流量 → 归**物理扩展**。

最强一手证据：**ClawVM**（2604.10352）把 compaction/writeback/校验明确定位在 *harness layer*，强调 "deterministic and auditable"，且 "enforcement occurs at the harness layer (prompt assembly, tool mediation, lifecycle observation) rather than within the LLM"。

---

## A. 记忆维护（Memory Maintenance）— 文献最密集，归物理轴

| sub-agent | 职责 | 出处 | 可引用性 |
|---|---|---|---|
| Context Compaction 压缩 | context 超长时摘要压缩，腾 token 预算 | ClawVM (2604.10352)；ETCLOVG C 层 | ✅ 一手 |
| Writeback / Flush 管家 | lifecycle 边界验证后写回持久层，防 "reset 丢状态" | ClawVM「validated writeback at lifecycle boundaries」 | ✅ 一手 |
| Reflection 反思器 | 轨迹 → 洞察（语义过滤器）再注入记忆 | 记忆演进综述 (2605.06716) §5；Reflexion/CLIN | ✅ 一手 |
| Cross-Trajectory 抽象器 | 跨轨迹归纳通用规则/技能（Storage→Experience） | 2605.06716 §6；FLEX/MemSkill | ✅ 一手 |
| 记忆增删/遗忘 GC | 防"无限记忆膨胀污染性能"，时间衰减 | 2605.06716 §4.2「策略性增删」 | ✅ 一手 |
| 自主检索控制器 | 主动判断要不要、要哪种记忆 | 2605.06716 开放挑战 #1/#4 | ⚠️ open problem，列未来工作 |

## B. 上下文组织（Context Curation）

| sub-agent | 职责 | 出处 |
|---|---|---|
| 三级 context 管理（短期/会话/持久） | 决定模型每步可见什么 | ETCLOVG C 层 (2605.18747) ✅ |
| typed pages / 多分辨率表示 | 状态分页 + 按 token 预算选分辨率 | ClawVM (2604.10352) ✅ |
| Memory Tool 工具化记忆 | 记忆读写做成工具调用 | Anthropic 笔记 ⚠️ 待核实出处 |

## C. 验证 / 质量（Verification）

| sub-agent | 职责 | 出处 |
|---|---|---|
| Self-Verification hook | 任务后自检、失败归因、回归反馈 | ETCLOVG V 层；Trivedy（survey 转引 ⚠️） |
| Evaluator-Optimizer 回路 | 生成→评估→反馈→改进 | Anthropic 5 模式 #5 ✅（博客） |
| min-fidelity 不变量校验 | writeback 前校验状态完整性 | ClawVM ✅ |

## D. 编排 / 生命周期（Lifecycle & Orchestration）

| sub-agent | 职责 | 出处 |
|---|---|---|
| Orchestrator-Workers | 中央 LLM 动态分解→委托→综合 | Anthropic 5 模式 #4 ✅ |
| Routing 路由 | 分类输入导向专门分支 | Anthropic 5 模式 #2 ✅ |
| Handoff 管理 | Agent 间状态交接（recall 痛点 0.32） | OpenAI SDK；NLAH (2603.25723) ✅ |
| 生命周期编排（L 层） | 组织状态读写控制流，单→多 agent | ETCLOVG L 层 ✅ |

## E. 工具供给（Tool Supply）— C3 已有，归 Harness 能力供给

| sub-agent | 职责 | 出处 |
|---|---|---|
| Tool Synthesis / AutoHarness | LLM 自动合成代码 harness / 新工具 | AutoHarness (2603.03329) ✅；Tool-Genesis (2603.05578) |
| capsule / capability contract | tool = 含 intent + 契约 + 实现 + 验证 + 生命周期 | Tool-Forge (2605.28000) ✅，intent-scoped 省 99.2% context |

---

## 对架构的影响（写入主线）

1. **S1/S2 成立**：A–D 多为 LLM 驱动的维护机制，文献支持把它们归 Harness 内部（而非 task skills）。
2. **S3 物理轴归属**：A/B/C 虽调模型、吃推理预算，但触发 $\propto$ token 流量 → 归物理轴；P1 因此更干净。
3. **ClawVM 差异声明**：ClawVM 偏确定性规则（deterministic）；本架构维护子系统偏 **LLM 驱动 + 可审计日志**（概率性，靠 logging 保证可审计）。引用时须显式区分。

---

## 候选补充（待评估导入 Zotero）

| 标题 | arXiv | 用途 |
|---|---|---|
| ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents | 2604.10352 | **维护子系统一手证据（强）** |
| AutoHarness: improving LLM agents by automatically synthesizing a code harness | 2603.03329 | C3 tool synthesis |
| Externalization in LLM Agents: Memory, Skills, Protocols and Harness Engineering | 2604.08224 | Harness 四类 externalization 综述 |
| From Storage to Experience: Evolution of LLM Agent Memory Mechanisms | 2605.06716 | 记忆维护机制分类（已在 vault） |

相关：[[00-讨论记录与原始构想]] · [[01-C5-双扩展解耦形式化与命题]] · [[02-2026相关论文清单]] · [[04-研究时间线]] · [[论文-LLMAgent记忆机制演进综述-2605.06716]] · [[Agent Harness 参考架构调研报告]]
