# CHANGELOG

## v14 — 2026-07-28

### 收紧中心命题与证据边界

- 将 P1 明确为声明运行域 $\Omega$ 内的**充分条件**，不再暗示必要性或普遍独立；共享的 capability-count $\times$ Scaffold-count 因子实验同时检验逻辑轴、物理轴及其交互，并用共享算力、锁、外部服务配额、授权延迟、调度反馈和可变策略注入再耦合因素。
- Abstract 与贡献列表由五项收束为三项：有界双轴可分离条件、typed capability-to-capacity boundary、可证伪协议。外部数据、上下文分区、IR、locality/dry-run 与 Skill lifecycle 改称 architecture-compatible mechanisms 或 subsystem hypotheses，不再写成 P1 的逻辑推论。
- Table 1 用 `documented / partial / implicit / not documented / proposed` 区分公开证据与缺失证据，避免把“文档未说明”误判为“系统没有”；本文一行也明确为设计目标而非实证结果。

### 修正局部机制的可检验表述

- Prefix cache 增加 model、tokenizer、policy metadata、tool serialization/order 与 token identity 条件；tool-set 稳定和最小重叠改为需直接测量 cache hit 与任务语义的工程启发式。
- Amdahl 式物理扩展假设显式加入共享 Harness、锁、配额、授权后端和调度反馈等再耦合项。
- Satisfaction ratio 限定为版本化、按输出子域登记的 verifier；只有确定性 verifier 或经过校准且阈值预登记的 gate 才能终止派生闭包。
- Capability trace 只声称解释“已准入并激活”的能力，不把未激活候选误写成可观测事实。

### 加固 P15 / P16 / P17

- P15 定义逐输出子域加 process 的向量准入对象 $R(s)$，以 protected/target components、容差和 Pareto-style gate 防止聚合分数掩盖局部退化；协议改为 scalar、output-vector、output-plus-process 三组对照，并加入 oracle 对 process attribution 的反事实核验。
- P16 使用严格 train/validation/held-out 划分：预登记用途、字段、结构描述、指标和 margin，禁止 reconstruction agent 访问源凭据，最终 summary 固定后仅检查 held-out 一次。
- P17 区分 entry-content、registry schema/module 与 cross-registry 三类变更；普通 entry/IR 更新不再被误判为解耦失败，核心可证伪点是单侧变更是否无必要地传播为另一 registry 的 schema/module 修改。

### 图表与产物

- Figure 7 重绘为 Draft → Train → Validate → Staged release → Monitor 两层生命周期，并显示 revalidate、thaw、rollback 与 retire 的可逆路径。
- Figure 8 更新为 P1 共享因子实验、P15 三组向量准入比较、P16/P17 held-out reconstruction 与三类变更矩阵。
- 重建 v14 PDF，并执行全文残留扫描与逐页渲染检查。

## v13 — 2026-07-28

### Table 1 收回单一维度

v10 曾把并发工作 Skillware / GRACE 两行加入 Table 1，v11 已按原文核实下调其评级（GRACE 的 Skill registration 只能记 `n/a`）。但根本问题不是评级高低，而是**表格混了两类不可直接比较的对象**：生产框架与工作流引擎（AutoGen / LangGraph / Temporal……）注册并执行任务能力，而 Skillware 治理的是 Skill 身份与生命周期、GRACE 结构化的是系统指令——它们从未打算覆盖同一组责任，逐格打分需要一长段表注来解释 `n/a`，反而削弱表格的说服力。

- **移除 Skillware / GRACE 两行**，Table 1 恢复为纯生产系统对比；`n/a` 一并消失。
- 表注改为说明表格范围限定于"注册并执行任务能力"的同一设计空间，治理对象不同的并发研究改在 §4 以论证定位而非以评分定位。
- §4 中 Table 1 的引导句同步补充该范围说明（"covers production frameworks and workflow engines only; the concurrent research discussed above is placed by argument rather than by rating"）。

§4 关于 Skillware / GRACE 的边界论述（v9 加入、v10 拆段）全部保留不变——它们本来就在文字里讲清了差异，无需表格重复。

## v12 — 2026-07-27

### 署名

- 标题页新增作者署名 **Yaxiao Liu** 与联系邮箱 **rootliu@gmail.com**（新增 `Author` / `Affiliation` 两个段落样式：作者名 12pt Times-Roman 居中，邮箱 10pt 居中）。
- 副标题行原为 "Working preprint | Agentic Runtime Research Project | {date}"，占位性的项目名已由真实署名取代，简化为 "Working preprint | {date}"。
- PDF 元数据 author 字段由占位符 `Agentic Runtime Research Project` 改为 `Yaxiao Liu <rootliu@gmail.com>`。
- 署名信息提取为脚本顶部常量 `AUTHOR` / `AUTHOR_EMAIL`，与 `TITLE` 并列。

## v11 — 2026-07-27

审查方式：核实 v10（在其他机器上完成：拆分 §4/§10.1/§8.5 段落、Table 1 新增 Skillware/GRACE 两行、Figure 4 降高 236→200），逐条比对两篇论文 PDF 原文核实新增表格评级。

### Figure 4 版面回归修复

- **v10 把 `fig:derivation-closure` 高度从 236 降到 200，但图内元素仍按 236 的绝对坐标绘制**，导致 `satisfaction ratio` 框底部越界、三处文字互相压叠（loop 标签压 satisfaction ratio 框、derivation 说明文字与 loop 标签重叠、terminate 框压住 sub-agents 面板）。
- 改为**自底向上的相对布局**：底部预留 `band=34` 给回环路径，左列三个框按 `col_h=38` 依次堆叠，右侧面板顶部对齐主 agent 框顶、底部对齐 `band+14`，子 agent 单元与说明文字均相对面板定位。此后图高变化不再破坏版面。

### Table 1 新增两行评级修正（核对 PDF 原文）

- **GRACE 行**：v10 给 `Skill registration=yes / Policy gates=yes / Replay=partial`。核对 arXiv:2607.09175 全文——**"skill" 出现 0 次**（其结构化对象是系统指令而非 Skill 注册表），"gate" 仅 1 次，8 处 "audit" 全部指*实验后的诊断审计*（post-hoc LLM-as-Judge，明确声明不用于修改 checkpoint 或计算指标），并非运行时审计追踪。→ 改为 `n/a / partial / partial / no / no`。
- **Skillware 行**：v10 给 `Replay=yes`。核对 arXiv:2607.18970 全文——**"replay" 出现 0 次**，3 处 "audit" 指*范畴归属可审计*与*语料快照可审计*（manifest/provenance 级），非 per-run replay。→ Replay 改为 `partial`。
- **表注补充**说明两行并发工作只按其实际覆盖的责任评分，并解释 `n/a` 的含义（GRACE 结构化系统指令而非 Skill registry；其验证是局部编辑准入而非激活路径上的 policy gating），避免 `n/a` 让读者困惑。

### 重建 PDF

- 生成 `output/pdf/..._v11.pdf`（24 页）；全文扫描无残留反斜杠/花括号、无 `Section\d` 断字、无 `sum_`/`frac` 残留；Figure 4 高分辨率目视确认无重叠。

## v10 — 2026-07-26

在其他机器上完成的结构性调整（本机仅核实与修复，见 v11）：

1. **§4 Related Work 拆为三段**，加 `\paragraph` 小标题：Runtime and serving layers / Concurrent work (July 2026) / Production frameworks。
2. **§10.1 延迟讨论拆段**：把"policy evaluation 更便宜 + 开销须摊薄"另起一段，与前面的实测下界讨论分开。
3. **§8.5 告警独立成段**：`\paragraph{Caveat: trustworthiness of process criteria.}`。
4. **Table 1 新增 Skillware / GRACE 两行**（标 † 表示并发工作），表注相应改写。
5. **Figure 4 高度 236 → 200**。

## v9 — 2026-07-25

审查方式：检索 HuggingFace Daily Papers / arXiv 2026 年 7 月 trending 论文，下载并精读 15 篇直接相关工作（PDF 存于 `academy/papers/pdf/`），据此重划新颖性边界；并把用户口述的 harness 强度设计（子 agent 派生闭包）写入论文。

### 新增内容

1. **新增 §7.4 "Derivation-Closure Orchestration" + Figure 4**：形式化用户的编排设计——子 agent 持有相对固定的 tool-set/data-set 从而界定其输出范围；对集合外工具/数据源的引用不就地授予，而是成为派生下一个子 agent 的准入条件；主 agent 不执行任务工具，只做 summarize + semantic join + top-k，并按声明的 σ_out 子域计算 **satisfaction ratio**（新增公式），据此反复调用/派生子 agent 直至达标、预算耗尽或无候选（后者为 typed failure）。新增 `_draw_derivation_closure` 示意图方法。
2. **§2.1 contributions 第 3 条**扩写以涵盖该编排规则。

### 新颖性边界重划（应对 7 月撞车工作）

- **§4 新增三段**：(a) `soni2026gates` 落地了本文视为设计要求的证伪式 release gate + standing invariants（capability token / control ring、有界模型检查、跨 6 个 release 不变），并实测治理开销 ~0.021ms/请求；明确其范围是单运行时安全核，不涉及逻辑/物理双轴分离。(b) `fan2026skillware` 提供了本文原本隐含的 Skill 软件本体论（Artifact/Unit/Host 三分、lifecycle continuity 可测量、138k 语料），本文采纳其词汇，§8.4 相应收窄。(c) `hsu2026grace` 的 typed graph + 局部邻域验证是 IR 原理的独立证据，区别在于结构化对象不同。另补 `wang2026handbook`/`huang2026memoharness`（归入 §11 已割舍的维护子系统）与 `zhang2026misalignment`/`wang2026skillcorpus`/`badhe2026skillsecurity`（operation closure 的现实障碍与路径安全背景）。
- **§8.5 新增"Relation to concurrent work on structured credit assignment"段**：`luo2026gsme`（按 pathology 索引）与 `lin2026wml`（按 workflow node/mechanism 归因）都按*事后推断的失败属性*索引 credit，本文按*契约先验声明的 σ_out 子域*索引，且与 §7.4 运行期 satisfaction ratio 共用同一结构；明确"契约维度是否优于诊断维度"为开放问题而非主张。引 `wang2026compound`（增益仅在 regression control 内置于优化环时复合）作为前提支持。
- **§8.4 收窄**：把"Skill 值得作为有独立 identity 的软件单元"归给 Skillware，本文只主张 freeze-to-code 阶段与其 release gate。
- **§8.2 P17 补充**：引 GRACE 支持"结构化使验证局部化"，并把 P17 的独特性明确为两个 registry 在单侧变更下的相互独立性。

### 实证依据修正

- **§10.1 删除错误推测**：原文推测契约编译延迟为"low tens of milliseconds"，与 `soni2026gates` 实测 0.021ms 差三个数量级；改为引用该实测值作为下界（其只覆盖不变量求值，不含 schema 校验/图构造/绑定），并明确本文不再自行给出估计，交由 Protocol 9.6 测量。

### 评估协议加固

- **9.1 Control**：新增两项混淆控制——固定并报告 harness 检索能力，且在单源/语料库两个规模下分别测（`he2026disclosure` 发现渐进披露收益在强 harness 下趋零、仅在语料库规模决定性）；激活深度固定为一层（同文献发现第二层从不帮忙、有时降准确率）。
- **9.1 Metrics**：聚合 recall 不足——`xue2026longcontext` 观察到 requirement coverage >92% 而结果崩塌；新增"每条声明需求全满足的运行占比"并记录具体被丢弃的需求。
- **9.7 / 9.8 Control**：采用 executor/grader 分离 + first-attempt grading，self-correction 单独计数而非计入通过（`anand2026aeval` 指出自修复自评会把通过率灌水成虚假 100%）；9.8 另要求过程判据须为运行前登记的固定产物。
- **9.8 Falsification 新增一条**：按 `wang2026phantom` 的反事实设计（该文 60 次运行中 15 次为从未发生的失败类别捏造 guardrail），用 oracle 校验每条 rejection reason；若维度标注理由含 oracle 可反驳的虚构违规，则"归因更清晰"主张失效（即便收敛更快）。
- **§8.5 新增告警段**：r_proc 依赖"step 是否满足判据"的判定，故判据须为登记产物而非评分时由模型生成。

### 引用

- 新增 15 条引用（全部经 arXiv API 官方核实标题与完整作者列表，无占位符/截断）；引用总数 24 → 39。
- 15 篇 PDF 下载至 `academy/papers/pdf/`，沿用既有命名约定 `{arxivID}v{n} {Title}.pdf`。
- **参考文献 PDF 统一归位**：vault 原有的 9 篇参考 PDF 一并移入 `academy/papers/pdf/`（共 24 篇），vault 内 `Papers/PDFs/` 目录移除，另删除 `Workspaces/deep research/` 下两处 18 份重复镜像副本。此后 **vault 只保留本人论文的 PDF 与 md**；vault 内 Notes 与 00_Index 的 PDF 链接改为指向 repo 路径。
- 15 篇已导入 **Zotero**（含 PDF 附件），带 `agentic-runtime` / `2026-07` 及分类标签（高危撞车 / P15平行工作 / 协议警告 等）。

### 渲染 bug 修复（3 处）

- **display equation 从不走数学清理路径**：`code_block()` 直接调 `clean_latex`，而 `clean_latex` 只对 `$...$` 内联公式调用 `clean_math`，导致 `\frac`/`\sum_{}`/`\mapsto`/`\cdot` 在行间公式中全部落空。表现为 `r_proc(s)=1|steps|sum_k ...`（分数塌成并列符号）。现于 `code_block` 内先归一化数学构造再交给 `clean_latex`。
- **`\frac` 完全无处理分支**：新增 `(分子)/(分母)` 转换，正则允许一层嵌套花括号（`\frac{1}{|\mathrm{dom}(\sigma^{out})|}` 需要）。
- **`\sum_{...}` 下标丢失**：新增 `sum over ... of` 转换，同样支持一层嵌套。

### 重建 PDF

- 生成 `output/pdf/..._v9.pdf`（24 页）；全文扫描确认无残留反斜杠/花括号、无词融合、无带空格短横线、无 `Section\d` 断字、无 `sum_`/`frac` 残留、无未解析引用键；Figure 1–8 的 caption 编号与正文引用一致；参考文献 1–39 完整无缺号。

## v8 — 2026-07-25

审查方式：核实用户在其他电脑上完成的 v7 改动（压缩 Abstract、拆分 §8.2/§8.5 段落、新增命题总表、引入 Zep/SoKG/XPEventCore 三条引用、halevy→chen bib key 改名、清理 7 个无用 `_draw_*` 方法），逐条核实新增内容的准确性并修复渲染 bug。

### 引用准确性修正（3 条，全部经 arXiv/HAL 官方页核实）

- **`zep2025`**：作者占位符 "Zep Team" → 实际作者 Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef。
- **`sokg2026`**：标题不全（"Knowledge Graph Construction via QA-Driven Fact Extraction"）→ 补全为 *SocraticKG: Knowledge Graph Construction via QA-Driven Fact Extraction*；作者占位符 "SoKG Team" → 实际作者 Sanghyeok Choi, Woosang Jeon, Kyuseok Yang, Taehyeong Kim。
- **`xpeventcore2024`**：作者列表不全（"Piryani, R. and others"）→ 补全五位作者 Rajesh Piryani, Nathalie Aussenac-Gilles, Nathalie Jane Hernandez, Cédric Lopez, Camille Pradel。
- 验证 7 个被删除的 `_draw_*` 方法（`overview`/`stack`/`ontology`/`double_helix`/`architecture_flow`/`results_bar`/`theme_convergence`）确系死代码，未被本论文任何 figure kind 引用，删除无风险。

### 渲染 bug 修复（2 处）

- **`\S` 替换缺空格**：新增命题总表里 `\S5.3`/`\S9.8`/`\S9.9` 渲染为 "Section5.3" 等无空格形式；`re.sub(r"\\S(?![a-zA-Z])", "Section", text)` 缺少尾随空格 → 改为 `"Section "`。
- **法语重音符号 `\'` 未处理**：`Lopez, C{\'e}dric` 渲染为 "C edric"（缺失字母）；脚本此前只处理了变音符 `\"`（如 `K{\"u}ttler`→"Kuttler"），未处理锐音符 `\'`（以及类似的 `` \` ``/`\^`/`\~`/`\=`/`\.`）→ 新增对应正则，与变音符处理一致地去重音為纯 ASCII（"Cédric"→"Cedric"）。

### 重建 PDF

- 生成 `output/pdf/..._v8.pdf`（20 页），全文扫描确认无残留反斜杠/大括号、无相邻宏融合、无带空格短横线、无陈旧占位符作者名。

## v6 — 2026-07-23

审查方式：本机 v5 PDF 与从 GitHub 拉取的 obsidian/architecture 仓库最新内容逐条比对；聚焦图表引用准确性与行文流畅度。

### 图表 / 引用修正（6 处）

- **§3.2 / §8.4 陈旧交叉引用**：`Section~4.3` → `Section~5.3`（四条假设实际在 §5.3 "Conditional Decoupling"）；`Section~6.1` → `Section~7.1`（frozen prefix 概念实际在 §7.1）。
- **Figure 7 证伪矩阵缺行**：脚本 `_draw_evaluation_matrix` 的 `rows` 列表只有 8 行，缺 §9.4 "Control-Plane Leakage" 对应行（caption 已声明九行）；补齐后图高从 190pt 调整为 250pt 以消除溢出。
- **`\S` / `\Sigma` 替换冲突**：`latex_to_preprint.py` 的裸子串替换 `text.replace(r"\S", "Section")` 会误伤 `\Sigma`（渲染为 "Sectionigma"）；改为 `re.sub(r"\\S(?![a-zA-Z])", ...)`。
- **`\big(` / `\big[` 未处理**：脚本只处理了 `\bigl/\bigr/\Bigl/\Bigr`，论文正文的裸 `\big(`/`\big)`/`\big[`/`\big]`（§8.5 公式）落入通用反斜杠剥离兜底逻辑，融合成 "r_dbig(...)"；补充对应正则。
- **相邻希腊字母宏融合**：`\lambda\rho`、`\mu\bar{c}` 渲染为 "lambdarho"/"mubarc"；新增相邻反斜杠命令间插入空格的预处理，并为 `\lambda`/`\mu`/`\bar{}` 补充替换规则。

### 行文修订

- 全文 24 处 em-dash（`---`）短语堆砌句改写为通顺连接句（改用冒号、分号、"that is"、"such as"、"comprising" 等），保留全部引用、命题编号与章节交叉引用不变。

### 渲染 bug 修复

- `latex_to_preprint.py` 中 `text.replace("--", " - ")` 把合法的英文连字符范围（`(1)--(4)`、`data--output`、`5--20 nodes`、`human--agent`）渲染成带空格的短横线；改为 `text.replace("--", "-")`（`---` 仍按加空格短横处理，`--` 直接收紧）。

## v5 — 2026-07-22

将 vault 两篇最新研究笔记（`12-Skill作为可训练激活层-双子目标Reward`、`13-DataWiki-ThemeWiki-IR中间关系层`）的内容吸收进论文。无新增引用（仅用已有 [2] Chen et al. 与 [20] SkillOpt）；未声称任何实验结果。

### 内容修改

1. **新增 §8.5 "Training Before Freezing: A Dual-Subgoal Reward"**（接 §8.4 Skill-as-Code）：SkillOpt [20] 的单 scalar reward 是其自认局限；本文把 reward 结构化为结果子目标 r_out（沿 σ_out 子域各配独立标注 benchmark 加权）× 过程子目标 r_proc（工具/数据源/逻辑判据/step gate 的稠密即时信号），双维结构化 gate 记录带维度的负反馈；人工角色从每轮判断降为一次性确认评测方法；收敛子目标进入 freeze-to-code——train 与 compile 是 skill 生命周期的两阶段，均归 Harness 维护子系统；主张陈述为可证伪命题 P15 而非结果。
2. **新增 §8.2 "From Query Plan to Intermediate Relation"**（§8.1 之后）：把契约映射的 "plan" 步骤实体化为 IR 记录 theme ↦ ⟨{Σ(src)}, 5W1H⟩，六要素（When 时效 / Where 使用范围 / Who 拥有者授权 / What 数据语义 / Why 集成逻辑 / How 物理访问）逐个定义；Data Wiki（数据语义，复杂报表人机协同构建 + reconstructive reflection 校验，P16）与 Theme Wiki（验证收敛的产出模板登记，来自 σ_out 子域）正交，IR 是唯一显式耦合点（P17）；显式声明贡献边界：工程层显式化与重组，非新检索/数据集成算法（引 [2]）。
3. **§9 新增两条评估协议**：9.8 Dual-Subgoal Reward for Skill Training（P15：冻结 SkillOpt 骨架仅改 gate 的对照；收敛编辑数/子域均衡/人工干预次数指标；双维无增益即证伪）与 9.9 Intermediate-Relation Decoupling and Reconstructive Reflection（P16+P17：只换数据源/只换产出格式两类变更的波及范围；N 份人常用报表的还原准确率差距）。
4. **Figure 7 证伪矩阵**：脚本中矩阵表新增两行（Dual-subgoal reward、IR decoupling），caption 更新为九行。
5. **§11 Limitations 改写范围割舍声明**：维护子系统 M 仍超出范围（skill 训练回路与 IR 维护均归属之）；数据子系统 D1–D4 全量形式化与高阶记忆留在配套笔记，本文仅纳入契约相关部分（IR/5W1H 与 Data Wiki / Theme Wiki 分离）。
6. **§2.1 contributions 与 Abstract 同步**：协议清单补两条；次级贡献中 "Skill-as-Code" 扩为 "train-then-freeze Skill lifecycle"。

## v4 — 2026-07-22

审查方式：v3 PDF 全文与 Obsidian vault（`~/Documents/kimi`）原始构想笔记、8 篇精读笔记逐条比对；References 全部 21 条回 arXiv / 官方页面核实。

### References 修正（8 条，全部经 arXiv 官方页核实）

- **[8] ClawVM (2604.10352)**：标题系编造（原 "Deterministic and Auditable Agentic Runtime Harness"）→ 真实标题 *ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents*；作者 "ClawVM Team" 占位 → Mofasshara Rafique, Laurent Bindschaedler。
- **[18] MemGPT (2310.08560)**：作者列表错乱（Wooders 重复、Raganato/Restom-Gonzalez/Narayan 系编造）→ Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez。
- **[19] RAG (Lewis et al. 2020, NeurIPS)**：删除编造的 "Piktus, Vladimir"，修正断词（Küttler、Rocktäschel）；恢复为 Lewis/Perez/A. Piktus/Petroni/Karpukhin/Goyal/Küttler/M. Lewis/Yih/Rocktäschel/Riedel/Kiela。
- **[2] Semantic Metadata (2605.28787)**：第一作者误为 Halevy → 实为 **Shiyu Chen**（Google），作者序 Chen, Alrashed, Halevy, Noy；标题补全 *…A Comparative Study in Agentic Data Retrieval*；正文 "Halevy et al." → "Chen et al."。
- **[15] AgentScope (2402.14034)**：标题误为 "A Comprehensive yet Lightweight…" → *AgentScope: A Flexible yet Robust Multi-Agent Platform*。
- **[16] Agent-as-a-Service (2505.08446)**：标题与 "Team" 作者系编造 → *Agent-as-a-Service based on Agent Network*（AaaS-AN），Yuhan Zhu, Haojie Liu, Jian Wang, Bing Li, Zikang Yin, Yefei Liao。
- **[17] Autellix (2502.13965)**：第一作者误为 "Liu, Xuting" → 实为 **Michael Luo**（UC Berkeley），全作者列表替换；标题补全 *Autellix: An Efficient Serving Engine for LLM Agents as General Programs*。
- **[20] SkillOpt (2605.23904)**：作者占位 "Wang, Yizheng" → 第一作者实为 **Yifan Yang**（Microsoft），补全 15 作者列表。
- 构建脚本 `latex_to_preprint.py` 修复变音符号（`{\"u}`）转义缺陷，消除 "K uttler" 类断词。

### 内容修改

1. §2.1 "four primary contributions" → "five"（实际列 5 条）。
2. §10.1 契约编译延迟（"low tens of milliseconds" 等）缺乏实验依据 → 改为明确假设表述（待 Protocol 9.6 检验，非实测结果）。
3. Table 1 增加表注：评分基于公开文档与引用来源；"This paper" 行标 †，注明为设计目标而非已验证结果。
4. §7.3 机制 2 后新增 Amdahl 参数化短段：Speedup ≤ 1/(s+(1−s)/N)，s = s₀+λρ，E = E₀−μ·c̄；核心命题"并行度上界是工具集切分设计的函数"，声明为待校准设计假设（源自 vault 笔记 `09` P10）。
5. §11 Limitations 新增范围割舍声明：维护/自管理子系统（system skills 归 Harness 治理、走物理轴）与数据子系统完整四组成（on-policy 取数 API、治理即 data-usage skill、生命周期管理）超出本文范围，对应实验协议（数据轴、并行放置、Skill 训练 reward）留待实现阶段。

### 审查中已确认无误、未改动的部分

- 7 篇精读文献（[1][3][4][5][6][7][9][20]）的观点表述与 vault 精读笔记一致。
- Tool Forge "99.2% task-flow tool context reduction" 与精读笔记逐字一致。
- 核心思想谱系（A=⟨S,H,X⟩、条件解耦四假设、CP/DP、KV 前缀冻结四机制、off-policy loop、Skill-as-Code、dry-run、7 条可证伪协议）与 vault 原始笔记保真对应。
