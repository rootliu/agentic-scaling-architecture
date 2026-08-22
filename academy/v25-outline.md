# v25 大纲：合回单篇《A Contract-Centered Architecture for Scalable and Manageable Agentic Runtimes》

> **状态**: 大纲 v1（2026-08-22） | **决策**: 撤销 2026-08-05 的 v21/v22 拆分，合回单篇
> **计划**: `docs/superpowers/plans/2026-08-22-v25-remerge-and-review-deck.md`
> **目标篇幅**: 38–42 页 / 单套 8 图（v23 两篇合计 55 页，其中 8 图与契约解剖为纯重复）
> **来源**: `enterprise-architecture/paper_source/main.tex`（822 行，记作 **E**）+ `separability-study/paper_source/main.tex`（308 行，记作 **S**）

---

## 0. 合并的四条硬规则

这四条同时消掉上一轮审查的 P0-1/2/3/4 与 P1-5/6/7：

| 规则 | 内容 | 消掉的问题 |
|---|---|---|
| **R1 方法学以 S 为准** | 随机化单位一律 **cluster-period**；删除 `E:631` 的 "The unit of randomization is one independent run" 整句 | P0-3 |
| **R2 契约元组统一** | 全局 **`C=⟨I,O,G,A,B,V⟩`**；`E:219` 与 `E:482` 的 `⟨I,O,G,B,E,T⟩` 逐字段改写（原 `E`→`A`，原 `T`→`V`） | P0-2 |
| **R3 判决升为四态** | `supported` / `falsified` / **`conditional-engineering`** / `inconclusive`。第三态取自 `E:265–267`，原仅企业篇有 | P1-5 |
| **R4 margin 推导规则全局化** | `E:636` 的"每个 margin 须由具名决策推导、记录决策与 owner"适用于**全部** margin，含 `S:250` 的 reset 哨兵 | P1-6 |

标题冲突（P0-1）与零交叉引用（P0-4）随合并自动消失；仍给 `latex_to_preprint.py` 补 `--title` 参数，避免将来再拆时复发。

---

## 1. 章节大纲

### §1 Abstract / Introduction（3 页）
- 来源：`S:3–33`（研究问题与 narrow contribution 表述更收敛，优先）+ `E:11` 的企业动机一段
- 单一研究问题：*can a runtime activate independently deployable capabilities without materially changing capacity response, while scaling capacity without materially changing capability semantics, at an acceptable enforcement cost?*
- 保留 `S:9` 的诚实声明："reports no completed runtime implementation, experiment, dataset, or measured result"
- 0–100,000 agents 的规模表述**只出现一次**，且标注为 measurable design target（v23 已收敛，勿回退）

### §2 责任模型与主命题（5 页）
- 来源：`S:34–96`（四责任对象 + canonical configurations + P1 + 判决规则）
- 四责任对象：Skill（版本化行为）/ Harness（逻辑准入与控制）/ Scaffold（物理执行与隔离）/ 外置数据底座（source authority）
- 三个观测量：`R(c,s)` 运行时响应、`Q(c,s)` 语义结局、`E(c,s)` 执法开销
- **P1 cost-aware separability**：`Y_R` = log period-level p95 latency；`Δ_R` 差分中的差分；`m_R=log(1.10)` 双侧 TOST 等效；`m_Q=0.05` 单侧非劣效
- **【R3 落点】四态判决规则**，其中 conditional-engineering 定义搬自 `E:267`
- **【R4 落点】** margin 推导规则在此首次声明，后续各节引用

### §3 契约边界与架构（6 页）
- 来源：`S:113–206` 为骨架，`E:482` 的字段级 walkthrough 折入（按 R2 改写字母）
- **【R2 落点】** `C=⟨I,O,G,A,B,V⟩`：typed I/O、activated graph、authority/effect set、budgets/binding、version pins
- 逻辑控制 vs 物理执行；bounded composition（typed unmet dependency → 子 agent 准入，不就地授权）
- 外置数据解析；placement / isolation / evidence；版本化 Skill 生命周期
- **威胁模型**（`S:194–206` 五条：TCB / untrusted model output / semi-trusted Skills / untrusted external content / adversary capabilities）
- 保留 `E` 的形式化边界声明："notation for the measurement contract, not a formal operational model"

### §4 谱系与 novelty 边界（4 页）
- 来源：`S:98–111` 四个 paragraph 块 + `E:4` 的 Classical foundations 映射段
- 经典谱系：reference monitor（Anderson 1972 / Saltzer-Schroeder 1975）、complete mediation、capability & least authority（Miller 2003）、信息隐藏（Parnas 1972）、策略/机制分离（Hydra, Levin 1975）、控制/数据面（Kreutz 2015）、non-interference（Goguen-Meseguer 1982）、MAPE-K、ISO 25010、排队论与尾延迟
- **【P2-8 落点】必须新增的四篇**（详见 §5）
- novelty 边界表述：不是新的 reference monitor / capability model / scheduler / autonomic loop，而是把既有机制组合成 agentic-runtime 责任模型并使 separability + enforcement cost 可证伪

### §5 参考文献补齐（不单独成节，落在 §4 与 bib）
两篇 bib 取并集去重（33 + 21 → 约 41 条），并新增下列**当前零引用**条目。`academy/papers/pdf/` 已有 PDF，`.gitignore` 排除二进制。

| 优先级 | arXiv | 标题 | 为何必须引 |
|---|---|---|---|
| **必须** | `2605.26112` | From Model Scaling to System Scaling: From Training to Serving of LLM-Based Agentic Systems | 题目即"模型扩展→系统扩展"，与本文 capability/capacity 双轴同一问题域。**当前 novelty boundary 上最大的空洞**；vault 已有专门笔记却未进 bib |
| **必须** | `2607.13987` | Agent Skill Security: Threat Models, Attacks, Defenses, and Evaluation | §3 威胁模型的直接对标，semi-trusted Skills 一条尤其需要 |
| **应当** | `2605.22781` | DeltaBox: Lightweight and Efficient Containers for LLM-Based Agent Sandboxing | Scaffold 隔离基底的具体实现，支撑 resource invariance 义务 |
| **应当** | `2605.18747` | Code as Agent Harness: A Comprehensive Survey of Code-Driven Agentic Systems | Harness 综述，定位 Skill-as-Code；vault 已有笔记 |
| 择要 | `2605.08715` `2606.15376` `2605.14892` `2605.29790` `2606.03698` `2606.12835` | AgentForesight / CoAgent / LIFE 综述 / Evolve as a Team / Multi² / Internet of Agentic AI | 按行文需要择要，勿为凑数全引 |

引用卫生：沿用 2026-07 撞车月的规矩 —— 标题与完整作者列表必须经 arXiv API 核实后才写入 `references.bib`（本仓库有伪造引用元数据的历史，CHANGELOG v4 修 8 条、v8 修 3 条）。

### §6 六项测量义务（5 页）
- 来源：`S:208–235` 全量保留
- 每条义务五项必报输出：instrumentation coverage、observed violations、uncertainty、enforcement cost、Ω exclusions
- 三阈值：覆盖率下限 γ、违规率上限 ν、监测灵敏度下限 η；未覆盖事件按违规计（保守方向）
- 六条：typed closure / complete mediation / effect non-interference / shared-state isolation / resource invariance / scheduler independence
- family-wise error 规则（simultaneous confidence region 或 closed testing，须预登记）
- 盲化诊断注入做灵敏度校准；注入事件排除在实验分子之外
- **【R3 呼应】** 任一义务不过阈 → conditional-engineering result，而非直接 inconclusive

### §7 Cluster-Period 交叉试验（6 页）
- 来源：`S:237–279` 全量保留
- **【R1 落点】** 唯一随机化单位 = cluster-period（system epoch）；"adding inactive registry entries is not a treatment"
- reset/washout 哨兵四项；**【R4 落点】** `±log(1.05)` 与 `-0.025` 必须补具名决策论证，或显式标注"占位待定，投稿前替换"
- 完整序列主估计 + assignment-based ITT 敏感性 + tipping-point
- 估计量与不确定性：混合效应 + 小样本校正 + cluster 级随机化推断；一阶滞后结转项
- **【P1-7 落点】** `E(c,s)` 定义处新增一句：本文估计的是**边际运行时执法开销**；配对回放固定 model/tool 输出，故被拒行为改变后续轨迹的机会成本**不计入 E，而归入 Q(c,s)**
- 功效工作样例（σ=0.4、ρ=0.05、n=500、k≈41 → MDI≈0.08）

### §8 数据子系统与中间关系层（5 页）
- 来源：`E` 的数据底座各节 + 笔记 `06`（v0.2 含 §0.5 四接口→三阶记忆）、`08-数据层修订`、`17-DataWiki-ThemeWiki-IR`
- 功能契约视角：$\mathcal{D}=\langle D_1,D_2,D_3,D_4,\Omega\rangle$
- 存储分层视角：三阶记忆 ℳ = ⟨Raw, Index, Theme⟩，与四接口正交
- **IR 中间关系层 + 5W1H+Which 七维**（v24 已从六维升七维，Which 承载时间窗共现与 typed cross-reference）
- Data Wiki / Theme Wiki 双 registry；agent-side memory 显隐双轨
- **注意编号**：三阶记忆命题在笔记侧已由 P10–P12 重编为 **P18–P20**（让位给 §3quater 并行度维度）。论文正文只保留 P1 + 六义务 + P15/P16/P17，P18–P20 属笔记层 ledger，**不进正文命题表**

### §9 企业责任与治理（3 页）
- 来源：`E:777–789`（控制面集中风险、降级模式）+ `E:783` 四条 dispute & escalation 规则
- 证据平面表；owner 划分；争议仲裁；误杀恢复
- 预注册承诺三条（`E:789`）

### §10 次级协议与未来工作（3 页）
- 来源：`S:280–285` + `E` 的 P15/P16/P17 协议
- 次级协议（各带证伪条件）：Harness-bypass ablation、inline-expansion 对比、外置数据重构、dry-run 经济性、生命周期转换
- P15 双子目标 Reward / P16 还原式 reflection / P17 IR 松耦合 —— 明确为**次级**，不进 P1 判决
- 边界（承 2026-07 撞车月）：与 GSME `2607.13683` / WML `2607.20999` 的区别是**契约先验声明的 σ_out 子域** vs **事后诊断的失败属性**；"契约维度是否优于诊断维度"是开放问题，不是本文主张
- Skill 自动训练、跨 registry 变更传播列为 future work

### §11 证据边界、威胁与结论（2 页）
- 来源：`S:287–303`
- **必须保留且不得软化的三条 standing risk**（v22 与 v23 复核连续两轮标记）：
  1. 尚无本文实测结果 —— 仍是 architecture/research-program paper
  2. `supported` 不等于"证明独立"，只表示在预登记 Ω/margin/功效/仪器条件下未触发证伪
  3. 组织与治理实证薄弱 —— owner 划分、争议升级、跨企业可迁移性未经组织研究验证
- 唯一剩余的 P1 级评审项：**LangGraph 等现有系统的逐项对比表仍未落地**（v20 评审第 6 条，至 v23 未解决）
- 结论 + 下一步：单集群 2×2 序列可行性 pilot（目的不是检验 P1，而是验证 reset 哨兵可达成、覆盖率 γ 可达、配对回放可实施）

---

## 2. 图表计划（单套 8 图，消除 P3-10）

两篇当前各有一套同名 8 图（`fig:dual-scaling`、`fig:harness-contract`、`fig:control-data`、`fig:derivation-closure`、`fig:external-data`、`fig:dry-run`、`fig:skill-as-code`、`fig:evaluation-matrix`），合并后只保留一套。配色沿用 `site/` 已迁移的 Tailwind 系：logic `#3B82F6` / contract `#7C3AED` / phys `#EA580C` / data `#059669`。

新增一张（可选，第 9 图）：**四态判决流程图** —— 六义务阈值 → 三个 margin → 四态输出。R3 是本版最大的结构变化，值得一张图。

---

## 3. 命题清单（正文 vs 笔记）

| 层级 | 命题 | 处置 |
|---|---|---|
| **正文主命题** | P1 cost-aware separability | 唯一主张，四态判决 |
| **正文次级** | P15 双子目标 Reward / P16 还原式 reflection / P17 IR 松耦合 | 保留，明确不进 P1 判决 |
| 已撤回 | P2–P14 | v21 起已撤回或并入六项义务；编号保留仅供与旧稿对照 |
| 笔记层 ledger | P18–P20（索引充分性 / Theme 收敛 / 双螺旋增益） | 仅存于笔记 `08-数据层修订`；原 P10–P12，2026-08-22 重编 |

**`notes/07-创新点总结.md` 待重写**（P4-12）：当前仍是 v0.1 / 2026-06-20，登记 P1–P17 + N0–N12，与上述状态严重脱节。重写时须明确标注哪些命题已撤回、哪些降级为笔记层。

---

## 4. 不在本轮

- 不生成 v25 PDF 正文。本轮只到大纲；逐段合并 822 + 308 行 LaTeX 并重排 8 图是下一个独立任务
- 不执行 pilot 实验（standing risk 之首，合并不改变）
- 不改 `site/` 已发布的 HTML 与图
- 不补 LangGraph 对比表（§11 已登记为唯一剩余 P1 项）
