---
type: paper-appendix
title: "附录 — AI4Science 实例化 walkthrough（spec 调用顺序集 + data diagram）"
version: v0.2
date: 2026-06-29
status: 论文实例化附录（配套 [[论文草稿-三层可扩展Agentic-Runtime-综合v0.2]]）
related: ["[[论文草稿-三层可扩展Agentic-Runtime-综合v0.2]]", "[[论文-AOHP操作系统级智能体线束-2606.23449]]", "[[论文-Agent原生内存系统-2606.24775]]"]
---

# 附录：AI4Science 实例化 walkthrough

> 用一个具体 AI4Science 任务走查 `A=⟨S,H,X⟩ + D` 全栈。本附录是论文的「实例化」证据：把抽象的层/命题落到一次真实运行的 **spec 调用顺序** 与 **数据流图** 上。
> **dry-run 用途**：本 walkthrough 也作为 site 中 "Dry Run" 选项的第一个实例（后续可加更多用例）。
> **v0.2 对齐**：本版把用例走查显式对齐第四维（并行度/局部性，见 [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md)）——规划期先 **dry-run 探测每个 sub-goal 的工具集闭包 + Scaffold 环境范围（P13/N7）**，据此按 **工具集不重合（M1/M2）** 切成可并行子 agent；子 agent 各自 **冻结稳定工具集/记忆前缀（P11）**、按 **seed 亲和派生（M4）**、仅沿 **summarized context（M3）** 松耦合传递。这把第一性根因（[§0.5](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md)：agent 唯一能动的是组织 context → 前缀冻结 + 尾部变化）落到一次真实运行上。

---

## 用例 U

> **「基于最新文献，计算筛选目标带隙(~1.3 eV)的钙钛矿候选材料，并产出带引用与可复现脚本的报告。」**

选它是因为它同时压满三层 + 数据子系统：文献(→D2 时序摘要)、已知物性库(→D1 取数)、仿真计算(→code gen + Scaffold + cloud/HPC)、多信号验证(数值合理性 + 引用接地)、报告(→doc skill)、回写(→D2/Ω/D3)。

---

## 一、各层在本用例的实例化

| 层/子系统 | 本用例的具体 spec 实例 |
|---|---|
| **L3 Skills** | `lit-review.skill`、`materials-screening.skill`、`data-report.skill`（各含 I/O schema、call/stop/loop、verification）|
| **L2 Harness** | CapabilityCapsule：`arxiv_search`、`materials_db_query`(D1)、`code_execution`、`dft_screen`(可能 live-code 合成)、`doc_generation`；+ context assembly / policy gate / verifier / audit / 维护子系统 M；**+ partition：按工具集不重合把 sub-goals 切成并行子 agent（M1/M2），规划期 dry-run 探测工具集闭包（P13）** |
| **L1 Scaffold** | ExecutionSpec：microVM(脚本) + GPU serving(模型) + **cloud**(HPC 跑筛选) + **SSO/identity**(机构 HPC 授权) + network allowlist(Materials Project / arXiv)；**+ seed 亲和派生：同工具集子 agent 同 seed 共置复用 / 异工具集 anti-affinity 分散（M4）** |
| **D1** | DataSourceCard：Materials Project API、OQMD、arXiv |
| **D2** | 带时序约束的 SummaryEntry（"截至 T 的带隙 SOTA 方法/数据"，带 evidence_ref）存结构化 DB |
| **D3** | DataUsageSkill：`perovskite-screening` use case 的源选择 + join plan + top-k 权重 |
| **D4** | lifetime：文献时新性("as of"日期)、物性库口径、HPC 访问预算 |
| **Ω** | RunTrace、筛选脚本/结果 artifact、IntermediateRelation(候选↔物性↔文献)、LLM Wiki |

---

## 二、Spec 调用顺序集

> 编号 = 顺序；标注触发的编排原语 O1–O8 与所在面（CP 控制面 / DP 数据面）。

```
═══ 阶段 0 · Intake（CP）═══
[01] parse_intent(U)                                    ── 解析目标/约束/“做完”判据
[02] O4 plan: 分解 sub-goals {文献→候选→取物性→筛选→分析→报告}   ── CP
[02b] P13 dry-run: 对每个 sub-goal 探测工具集闭包 τ̂ + Scaffold 环境范围(env_scope)  ── CP（不真正执行，只做能力/资源可行性探测）
[02c] M1/M2 partition(𝒫*)：按"工具集不重合"把 sub-goals 分到并行子 agent，minimize 重合度 ρ(𝒫)  ── CP

═══ 阶段 1 · Skill 激活（CP）═══
[03] activate SkillSpec(lit-review)                     ── required_data_themes=["perovskite","bandgap"]
[04] activate SkillSpec(materials-screening)            ── required_capabilities=[materials_db_query, code_execution, dft_screen]
[05] activate SkillSpec(data-report)                    ── output_format=report{citations 必填}

═══ 阶段 2 · Context 组装（CP→DP）═══
[06] consult D3.DataUsageSkill(perovskite-screening)    ── 取 preferred_sources + semantic_join_plan(top_k,weights)
[07] consult D4.lifetime                                ── 取 freshness("文献 as_of=今日") + HPC nfr_budget
[08] query D2.semantic_join(intent, valid_at=today)     ── DP 在线：取带时序约束 SummaryEntry，每条带 evidence_ref
[09] O2 shots ← D2 正反例 ; O3 output schema ← SkillSpec ── 组装 context

═══ 阶段 3 · 能力路由 + 资源就绪（CP）═══
[10] O1 tool 选择 → CapabilityCapsule{arxiv_search, materials_db_query, code_execution, doc_generation}
[11] (若缺 dft_screen) O5 live-coding → 合成 dft_screen capsule → sandbox 验证 → 注册
[12] O7 model 选择：plan/分析=Opus 级；海量文献初筛=Haiku 级；O8 token 预算分发  ── CP→Scaffold serving
[13] policy gate + ExecutionSpec：SSO 授权机构 HPC、cloud=GPU pool、network allowlist=[MP,arXiv] ── CP
[13b] M4 seed 亲和派生：同工具集子 agent 同 seed 共置(affinity)、异工具集 anti-affinity 分散 → 固定资源下并行度 k_max↑  ── CP→Scaffold

═══ 阶段 4 · 并行执行循环（DP，子 agent 各自: select_action→gate→execute→observe→verify）═══
[13c] 每个子 agent 冻结稳定前缀=⟨工具集 spec + system + 相关 D₃ 用法记忆⟩，任务变量放尾部 → KV-cache 前缀命中 H↑（P11）
[14] execute arxiv_search → D2 已覆盖则跳过(命中共享摘要)            ── 减少重复消化
[15] execute D1.materials_db_query(MP, 候选集物性)                 ── DP 在线取数
[16] O5 code generation：Read/Edit/Bash 写筛选脚本 + 跑测试/lint     ── Harness→Scaffold
[17] execute dft_screen on Scaffold(cloud HPC microVM)            ── DP 计算
[18] observe + verifier/reward：①数值合理性(带隙物理区间/单位) ②引用接地(每条结论有 evidence_ref) ── CP
[19] if 验证失败(带隙非物理 / 结论 unverifiable) → O6 reflect → revise plan → 回 [14/16] ── CP

[19b] 跨子 agent 只传 summarized context（候选 top-k + 关键物性摘要），detail 入 Ω memory 不进下游 context（M3）── DP→CP

═══ 阶段 5 · 产出 + 回写（CP/DP）═══
[20] execute doc_generation → report artifact(含引用、可复现脚本)     ── DP
[21] writeback(M)：新 SummaryEntry 入 D2{claim:"候选X 预测带隙 Y", valid_from=T, evidence_ref=run_id} ── 逻辑追加，不覆盖
[22] write RunTrace + IntermediateRelation → Ω                     ── CP
[23] distill DataUsageSkill 更新 → D3(本次成功源/权重/失败回退)       ── CP（P9 收敛）
```

**四条结构性约束（对应命题）：**
- **[06–08] 先于 [14]**：先查 D3/D4/D2，命中共享摘要就不重拉原文 → 减少多 agent 争用、降单请求成本（**P7**）。
- **[10–13] 经 Harness 契约，Skill 从不直接绑 Scaffold**：Skill 只声明 `required_capabilities`，由 H 翻译 𝓘→𝓔（**P2**）。
- **[02b–02c/13b] 规划期 dry-run 切分 + seed 亲和**：先探测工具集闭包/环境范围（**P13/N7**）再按工具集不重合切并行子 agent（**M1/M2**），同工具集同 seed 共置（**M4**）→ 重合度 ρ↓、前缀命中 H↑、并行度 k_max↑，吞吐逼近 1/s（**P10**）。这正是 [§0.5](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md) 第一性根因（组织 context = 前缀冻结 + 尾部变化）的一次实例化：稳定工具集/记忆入前缀并冻结（**P11**），跨子 agent 仅传摘要（**M3**）。
- **[21] 逻辑追加 + evidence_ref**：溢出降冷不硬删，旧结论可回指原文，防幻觉（**§4.4.1 S3/S4**）。

---

## 三、Data Diagram（数据流，在线/离线双路）

```
                          ┌──────────── 离线 off-policy loop 𝓛₂（栈外，不被 H 调度）────────────┐
   外部源                 │  arXiv / 期刊 / MP 快照 ─▶ D2.summarize ─▶ SummaryEntry{claim,    │
   (papers, MP, OQMD) ────┼─▶                         (schema-on-read)  valid_from/to,        │
                          │                                          evidence_ref, supersedes}│
                          │                                       └─▶ 写入【结构化摘要 DB】    │
                          │                                          (索引: source/theme/valid)│
                          └──────────────────────────────────────────────────────────────────┘
                                                                       │ ▲
                                   ┌── semantic_join(valid_at=T,top_k) │ │ writeback 新条目 [21]
                                   ▼                                   │ │ (逻辑追加)
  ┌── L3 Skills ──┐  intent/specs ┌──────── L2 Harness（契约/控制面）──┴─┴────────┐
  │ lit-review     │ ────[03-05]─▶│ context assembly ← D2摘要/D3用法/D4时效        │
  │ materials-scr. │              │ O1路由·O5 code-gen·O7 model·O8 token·verifier  │
  │ data-report    │ ◀─报告schema─│ policy gate ──▶ 翻译 𝓘→𝓔                       │
  └────────────────┘              └─────┬──────────────────────────┬──────────────┘
        ▲ 交付 artifact                  │ 执行单元 𝓔                 │ D1 取数(在线)
        │                                ▼                           ▼
        │                    ┌─ L1 Scaffold（数据面）─┐      ┌─ D1 取数 API ─┐
        │                    │ microVM·bash·GPU serving│      │ MP / OQMD 物性 │
        │                    │ cloud HPC·SSO·network   │      └──────┬────────┘
        │                    └───────────┬─────────────┘             │ 物性切片
        │  RunTrace/artifact [22]        │ 计算结果+evidence          │
        └────────────── Ω 工作区 ◀───────┴───────────────────────────┘
                        (RunTrace · IntermediateRelation: 候选↔物性↔文献 · LLM Wiki)
                                  │
                                  └─▶ D3 DataUsageSkill 更新 [23]（取数决策熵↓，P9）
```

**读图三要点：**
1. **两条数据路径分离**：离线 𝓛₂ 把原始文献/库**预消化成带时序约束 SummaryEntry**，不在主请求路径上 → 新增源不抬单请求 token 成本（P7）；在线只做 `D2.semantic_join`(读共享摘要) + `D1.query`(读实时物性)，都经 Harness 契约。
2. **摘要 DB 是共享只读热点**：多 agent/多次运行读同一份 SummaryEntry(快照读)，不各自重拉同一篇 PDF → 消除争用、省重复推理（AOHP 同类机理 token↓）；检索靠 `valid 区间` 索引做时点过滤。
3. **写回单向、逻辑追加**：执行结果 → Ω → 蒸馏新 SummaryEntry 回灌 D2(带 evidence_ref，旧条逻辑失效不删) + 更新 D3，形成「离线总结→在线消费→执行产出→回灌总结」闭环，每个可召回结论都能回指原文，防幻觉。
4. **并行切分是一层正交结构**：Harness 在主路径 *之前* 用 P13 dry-run 探得每个 sub-goal 的工具集闭包，据此按工具集不重合切成并行子 agent（图中 lit-review / materials-screening / data-report 三束互不重合的能力）；子 agent 各自读同一份共享摘要 DB（前缀可冻结、H↑），彼此只沿摘要接口松耦合汇聚 → 串行比 s↓、吞吐逼近 1/s（P10）。切分层与上面的在线/离线数据分离正交，共享同一"高内聚前缀 + 松耦合尾部"不变量。

---

---

# 附录补充：基于 Kronos 的股票预测 walkthrough（FinTech）

> 第二个 dry-run 实例。基于本仓库真实 API：`KronosPredictor.predict(df, pred_len, T, top_p, sample_count)`（HF `NeoQuasar/Kronos-*` + Tokenizer），AKShare 取数，gold-kronos 的 ensemble/backtest/paper-trade 管线。

## 用例 K
> **「给定标的与预测时长，用 Kronos 基础模型预测未来 N 根 K 线(OHLCV)，转成交易信号，并产出带回测与可复现脚本的报告。」**

价值点：展示一个端到端的**基础模型时序 skill**——取数(D1)、GPU 托管预训练模型(Scaffold serving)、把概率采样(T/top_p/sample_count)作为循环的一部分、多信号验证(回测指标 + 泄漏检查 + 校准)、把预测作为**带有效期的记录**回写。

## 各层实例化
| 层/子系统 | 实例 |
|---|---|
| **L3 Skills** | `stock-forecast.skill` · `signal-gen.skill` · `backtest-report.skill` |
| **L2 Harness** | capsule：`market_data_fetch`(D1) · `kronos_predict`(GPU 托管) · `ensemble_sampling` · `backtest_run` · `doc_generation`；+ verifier/policy gate/M |
| **L1 Scaffold** | ExecutionSpec：**GPU serving(Kronos-small/base + Tokenizer)** · microVM(回测) · cloud · SSO · network allowlist(AKShare) |
| **D1** | DataSourceCard：AKShare/行情商 — OHLCV+amount，ticker·interval·window |
| **D2** | 带时序约束的 **ForecastEntry**（claim:'[t..t+N] 预测路径'，valid_from/to=预测窗口，evidence_ref=run_id+输入）|
| **D3** | DataUsageSkill：每类标的的数据商/周期、lookback/pred_len、ensemble 权重 |
| **D4** | lifetime：K 线时新性、交易日历、预测有效窗口、推理预算 |
| **Ω** | RunTrace · 预测/回测 artifact · IntermediateRelation(标的↔特征↔信号) · LLM Wiki |

## Spec 调用顺序集
```
[01] parse_intent(标的,时长,风险)              [02] O4 plan {取K线→预测→信号→回测→报告}        ── CP
[02b] P13 dry-run 探工具集闭包/env → M1/M2 按工具集不重合切并行子 agent（如多标的/多周期并行），minimize ρ  ── CP
[03] activate stock-forecast (req=[market_data_fetch,kronos_predict])                          ── CP
[04] activate signal-gen + backtest-report (output=report{指标+脚本})                          ── CP
[05] consult D3(标的类别): 数据商/周期, lookback=400, pred_len=120, ensemble 权重              ── CP
[06] consult D4: K线时新性 + 交易日历 + 预测有效窗口                                            ── CP
[07] query D2.semantic_join(valid_at=now): 近期 ForecastEntry 窗口仍覆盖则复用(跳过重算)        ── DP
[08] O3 output schema ← SkillSpec: 信号{side,size,confidence} / 报告 schema                     ── CP
[09] O1 tool: {market_data_fetch,kronos_predict,ensemble_sampling,backtest_run,doc_generation}  ── CP
[10] O7 model(kronos→GPU; 分析→Opus级) + O8 token 预算                                          ── CP→serving
[11] policy gate + ExecutionSpec: SSO; GPU pool; allowlist=[AKShare]; 不授予下单(只读)          ── CP
[11b] M4 seed 亲和：同 Kronos 模型/工具集子 agent 同 seed 共置复用 serving（异标的 anti-affinity）→ k_max↑；子 agent 冻结前缀=⟨kronos capsule+system⟩，标的/窗口放尾部（P11）  ── CP→Scaffold
[12] execute market_data_fetch → D1: OHLCV+amount, x_timestamp/y_timestamp                      ── DP
[13] execute kronos_predict: KronosPredictor.predict(df,pred_len,T,top_p,sample_count)          ── DP
[14] O5(可选) ensemble_sampling: sample_count>1/多种子 → 分布而非点估计                          ── DP
[15] signal-gen + backtest_run on Scaffold: 预测→{side,size}; held-out 回测                     ── DP
[16] observe + verifier: ①无未来泄漏(y晚于x) ②回测合理(Sharpe/回撤) ③校准度                    ── CP
[17] 验证失败 → O6 reflect: 调 lookback/pred_len/权重 → 回 12/13                                ── CP
[18] execute doc_generation → report(预测图+回测指标+可复现脚本)                                ── DP
[19] writeback(M)→D2: ForecastEntry{claim,valid_from=t,valid_to=t+N,evidence_ref=run_id} 逻辑追加 ── CP
[20] write RunTrace + IntermediateRelation → Ω    [21] distill DataUsageSkill → D3 (P9)         ── CP
```

## 结构性约束（↔ 命题）
- **预测 = 带时序约束的记录**：ForecastEntry 仅在 `[valid_from, valid_to]` 内有效；过期窗口逻辑失效、不静默复用 → 防陈旧信号幻觉（§4.4.1 S3）。
- **泄漏防护经契约**：`y_timestamp` 严格晚于 `x` 窗口；verifier(步16)强制；Skill 不直接在 Scaffold 上拿原始未来 K 线（P2/P3）。
- **概率采样在循环内且可审计**：`T/top_p/sample_count` 是 O5/O8 选择，记入 RunTrace；同输入+种子可复现（N0）。
- **策略上只读**：不授予下单能力；policy gate 对任何交易通道工具 fail-closed（P3 能力围栏）。
- **多标的并行按工具集切分**：规划期 dry-run 探得各标的子任务共享同一 `kronos_predict` 工具集闭包，可同 seed 共置并行（M1/M2/M4），跨子 agent 仅传预测摘要（M3）→ 吞吐逼近 1/s（P10/P13）。

## Data Diagram 要点
1. **预训练模型作为被托管的能力**：`kronos_predict` 是 Scaffold 上 GPU 托管 capsule；增加标的在物理轴扩(加 serving)，不动预测 Skill（P1）。
2. **预测是带有效期的数据**：以 ForecastEntry 落入 D2，仅窗口内有效；后续运行仅在仍有效时复用，否则重算（RQ3/RQ4 教训）。
3. **验证是多信号**：泄漏检查 + 回测指标 + 校准度，而非单一准确率（H9）。
4. **并行度可设计**：多标的/多周期子 agent 工具集不重合、同 seed 共置，前缀冻结（kronos capsule 入前缀）→ H↑、k_max↑，吞吐逼近 1/s（P10–P13，见 [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md)）。

> SVG 数据流图见 site `dry-run-{zh,en}.html` 的 FinTech 选项卡。

---

*创建：2026-06-29 | v0.2 对齐并行度/局部性：2026-07-11 | 配套 [论文草稿-三层可扩展Agentic-Runtime-综合v0.2](%E8%AE%BA%E6%96%87%E8%8D%89%E7%A8%BF-%E4%B8%89%E5%B1%82%E5%8F%AF%E6%89%A9%E5%B1%95Agentic-Runtime-%E7%BB%BC%E5%90%88v0.2.md) §4.4.1 / §5 · [09-并行度与局部性协同设计](09-%E5%B9%B6%E8%A1%8C%E5%BA%A6%E4%B8%8E%E5%B1%80%E9%83%A8%E6%80%A7%E5%8D%8F%E5%90%8C%E8%AE%BE%E8%AE%A1.md)（P10–P13 / M1–M4 / §0.5 机制根因）*
